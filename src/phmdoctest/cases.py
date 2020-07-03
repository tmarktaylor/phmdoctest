"""Top level assembly of the pytest test case file."""

import inspect
import itertools
from typing import List

import click

from phmdoctest.entryargs import Args
from phmdoctest.fenced import Role, FencedBlock
from phmdoctest import coder
from phmdoctest import functions


put_imports_here = '\ndef line_by_line_compare_exact(a, b):'
"""Find match pattern to locate where to insert an import statement."""


def build_test_cases(args: Args, blocks: List[FencedBlock]) -> str:
    """Generate test code from the Python fenced code blocks."""
    session_counter = itertools.count(1)

    # repr escapes back slashes from win filesystem paths
    # so it can be part of the generated test module docstring.
    quoted_markdown_path = repr(click.format_filename(args.markdown_file))
    markdown_path = quoted_markdown_path[1:-1]
    docstring_text = 'pytest file built from {}'.format(markdown_path)

    # collect the generated code in a single string
    generated = coder.docstring_and_helpers(docstring_text)
    setup_insertion_point = len(generated)
    number_of_test_cases = 0
    for block in blocks:
        if block.role == Role.CODE:
            code_identifier = 'code_' + str(block.line)
            output_identifier = ''
            if block.output:
                output_identifier = '_output_' + str(block.output.line)
            whole_identifier = code_identifier + output_identifier
            generated += '\n'
            generated += coder.test_case(
                identifier=whole_identifier,
                code=block.contents,
                expected_output=block.get_output_contents()
            )
            number_of_test_cases += 1

        elif block.role == Role.SESSION:
            session = block.contents
            sequence_number = next(session_counter)
            generated += '\n'
            generated += coder.interactive_session(
                sequence_number, block.line, session)
            number_of_test_cases += 1

        elif block.role == Role.SETUP:
            setup_text = '\n'
            setup_text += coder.setup(
                identifier='code line ' + str(block.line),
                code=block.contents,
                setup_doctest=args.setup_doctest
            )

            # insert the setup code near the top of the test file
            top_part = generated[:setup_insertion_point]
            rest = generated[setup_insertion_point:]
            generated = top_part + setup_text + rest
            if args.setup_doctest:
                # insert an import pytest statement
                generated = generated.replace(
                    put_imports_here, 'import pytest\n\n' + put_imports_here)

        elif block.role == Role.TEARDOWN:
            generated += '\n'
            generated += coder.teardown(
                identifier='code line ' + str(block.line),
                code=block.contents
            )

    if number_of_test_cases == 0:
        if args.fail_nocode:
            nocode_func = functions.test_nothing_fails
        else:
            nocode_func = functions.test_nothing_passes
        generated += '\n'
        generated += inspect.getsource(nocode_func)
    return generated
