"""Top level assembly of the pytest test case file."""

import inspect
import itertools
from typing import List

import click

from phmdoctest.entryargs import Args
from phmdoctest.fenced import Role, FencedBlock
from phmdoctest import coder


def test_nothing_fails() -> None:
    """Fail if no Python code blocks or sessions were processed."""
    assert False, 'nothing to test'


def test_nothing_passes() -> None:
    """Succeed  if no Python code blocks or sessions were processed."""
    # nothing to test
    pass


def build_test_cases(args: Args, blocks: List[FencedBlock]) -> str:
    """Generate test code from the Python fenced code blocks."""
    session_counter = itertools.count(1)

    # repr escapes back slashes from win filesystem paths
    # so it can be part of the generated test module docstring.
    quoted_markdown_path = repr(click.format_filename(args.markdown_file))
    markdown_path = quoted_markdown_path[1:-1]
    docstring_text = 'pytest file built from {}'.format(markdown_path)
    test_code = coder.docstring_and_helpers(docstring_text)
    number_of_test_cases = 0
    for block in blocks:
        if block.role == Role.CODE:
            code_identifier = 'code_' + str(block.line)
            output_identifier = ''
            if block.output:
                output_identifier = '_output_' + str(block.output.line)
            whole_identifier = code_identifier + output_identifier

            test_case_str = coder.test_case(
                identifier=whole_identifier,
                code=block.contents,
                expected_output=block.get_output_contents()
            )
            test_code += '\n'
            test_code += test_case_str
            number_of_test_cases += 1

        elif block.role == Role.SESSION:
            session = block.contents
            sequence_number = next(session_counter)
            session_str = coder.interactive_session(
                sequence_number, str(block.line), session)
            test_code += '\n'
            test_code += session_str
            number_of_test_cases += 1

        elif block.role == Role.SETUP:
            setup_str = coder.setup(
                identifier='code line ' + str(block.line),
                code=block.contents
            )
            test_code += '\n'
            test_code += setup_str

        elif block.role == Role.TEARDOWN:
            teardown_str = coder.teardown(
                identifier='code line ' + str(block.line),
                code=block.contents
            )
            test_code += '\n'
            test_code += teardown_str

    if number_of_test_cases == 0:
        if args.fail_nocode:
            nocode_func = test_nothing_fails
        else:
            nocode_func = test_nothing_passes
        test_code += '\n'
        test_code += inspect.getsource(nocode_func)
    return test_code
