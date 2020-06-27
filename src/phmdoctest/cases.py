"""Top level assembly of the pytest test case file."""

import inspect
from io import StringIO
import itertools
from typing import List

import click

from phmdoctest.entryargs import Args
from phmdoctest.fenced import Role, FencedBlock
import phmdoctest.coder


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
    testfile = StringIO()
    docstring_text = 'pytest file built from {}'.format(markdown_path)
    testfile.write(phmdoctest.coder.docstring_and_helpers(docstring_text))
    number_of_test_cases = 0
    for block in blocks:
        if block.role == Role.CODE:
            test_case_str = phmdoctest.coder.test_case(
                identifier=line_numbers_string(block),
                code=block.contents,
                expected_output=block.get_output_contents()
            )
            testfile.write('\n')
            testfile.write(test_case_str)
            number_of_test_cases += 1

        elif block.role == Role.SESSION:
            session = block.contents
            sequence_number = next(session_counter)
            session_str = phmdoctest.coder.interactive_session(
                sequence_number, str(block.line), session)
            testfile.write('\n')
            testfile.write(session_str)
            number_of_test_cases += 1

        elif block.role == Role.SETUP:
            setup_str = phmdoctest.coder.setup(
                identifier=more_readable(line_numbers_string(block)),
                code=block.contents
            )
            testfile.write('\n')
            testfile.write(setup_str)

        elif block.role == Role.TEARDOWN:
            teardown_str = phmdoctest.coder.teardown(
                identifier=more_readable(line_numbers_string(block)),
                code=block.contents
            )
            testfile.write('\n')
            testfile.write(teardown_str)

    if number_of_test_cases == 0:
        if args.fail_nocode:
            fail_nocode_str = inspect.getsource(test_nothing_fails)
        else:
            fail_nocode_str = inspect.getsource(test_nothing_passes)
        testfile.write('\n')
        testfile.write(fail_nocode_str)
    output = testfile.getvalue()
    testfile.close()
    return output


def more_readable(text: str) -> str:
    """Replace underscores with blanks."""
    return text.replace('_', ' line ')


def line_numbers_string(block: FencedBlock) -> str:
    """Return string showing code/output block file line numbers."""
    code_identifier = 'code_' + str(block.line)
    output_identifier = ''
    if block.output:
        output_identifier = '_output_' + str(block.output.line)
    return code_identifier + output_identifier
