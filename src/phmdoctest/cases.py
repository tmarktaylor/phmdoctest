"""Top level assembly of the pytest test case file."""

import inspect
from io import StringIO
import itertools
from typing import List, Optional

import click

from phmdoctest.entryargs import Args
from phmdoctest.fenced import Role, FencedBlock
from phmdoctest import coder
from phmdoctest import functions


def get_block(blocks: List[FencedBlock], role: Role) -> Optional[FencedBlock]:
    """Get first occurrence of block with the caller's role."""
    for block in blocks:
        if block.role == role:
            return block
    return None


def build_test_cases(args: Args, blocks: List[FencedBlock]) -> str:
    """Generate test code from the Python fenced code blocks."""
    session_counter = itertools.count(1)

    # collect the generated code in a single string
    #
    # repr escapes back slashes from win filesystem paths
    # so it can be part of the generated test module docstring.
    quoted_markdown_path = repr(click.format_filename(args.markdown_file))
    markdown_path = quoted_markdown_path[1:-1]
    docstring_text = 'pytest file built from {}'.format(markdown_path)
    generated = StringIO()
    generated.write('"""' + docstring_text + '"""\n')

    setup_block = get_block(blocks, Role.SETUP)
    teardown_block = get_block(blocks, Role.TEARDOWN)
    needs_fixture = (setup_block is not None) or (teardown_block is not None)
    needs_checking = get_block(blocks, Role.OUTPUT) is not None
    generated.write(coder.compose_import_lines(needs_fixture, needs_checking))

    # fixture to handle setup and/or teardown and code for setup doctest
    if needs_fixture:
        generated.write(coder.setup_and_teardown_fixture(
            setup_block=setup_block,
            teardown_block=teardown_block,
            setup_doctest=args.setup_doctest
        ))

    number_of_test_cases = 0
    for block in blocks:
        if block.role == Role.CODE:
            code_identifier = 'code_' + str(block.line)
            output_identifier = ''
            if block.output:
                output_identifier = '_output_' + str(block.output.line)
            whole_identifier = code_identifier + output_identifier
            generated.write('\n')
            generated.write(coder.test_case(
                name=whole_identifier,
                code=block.contents,
                expected_output=block.get_output_contents()
            ))
            number_of_test_cases += 1

        elif block.role == Role.SESSION:
            session = block.contents
            sequence_number = next(session_counter)
            generated.write('\n')
            generated.write(coder.interactive_session(
                sequence_number, block.line, session))
            number_of_test_cases += 1

    if number_of_test_cases == 0:
        if args.fail_nocode:
            nocode_func = functions.test_nothing_fails
        else:
            nocode_func = functions.test_nothing_passes
        generated.write('\n')
        generated.write(inspect.getsource(nocode_func))
    return generated.getvalue()
