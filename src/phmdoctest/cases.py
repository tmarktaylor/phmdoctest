"""Top level assembly of the pytest test case file."""

import inspect
from typing import List

import click

from phmdoctest.entryargs import Args
from phmdoctest.fenced import Role, FencedBlock
import phmdoctest.print_capture


def test_nothing_fails() -> None:
    """Fail if no Python code blocks or sessions were processed."""
    assert False, 'nothing to test'


def test_nothing_passes() -> None:
    """Succeed  if no Python code blocks or sessions were processed."""
    # nothing to test
    pass


def build_test_cases(args: Args, blocks: List[FencedBlock]) -> str:
    """Generate test code from the Python fenced code blocks."""
    # repr escapes back slashes from win filesystem paths
    # so it can be part of the generated test module docstring.
    quoted_markdown_path = repr(click.format_filename(args.markdown_file))
    markdown_path = quoted_markdown_path[1:-1]
    docstring_text = 'pytest file built from {}'.format(markdown_path)
    builder = phmdoctest.print_capture.PytestFile(docstring_text)
    number_of_test_cases = 0
    for block in blocks:
        if block.role == Role.CODE:
            builder.add_test_case(
                identifier=line_numbers_string(block),
                code=block.contents,
                expected_output=block.get_output_contents()
            )
            number_of_test_cases += 1

        elif block.role == Role.SESSION:
            session = block.contents
            builder.add_interactive_session(str(block.line), session)
            number_of_test_cases += 1

        elif block.role == Role.SETUP:
            builder.add_setup(
                identifier=more_readable(line_numbers_string(block)),
                code=block.contents
            )

        elif block.role == Role.TEARDOWN:
            builder.add_teardown(
                identifier=more_readable(line_numbers_string(block)),
                code=block.contents
            )

    if number_of_test_cases == 0:
        if args.fail_nocode:
            test_function = inspect.getsource(test_nothing_fails)
        else:
            test_function = inspect.getsource(test_nothing_passes)
        builder.add_source(test_function)
    return str(builder)


def more_readable(text):
    """Replace underscores with blanks."""
    return text.replace('_', ' line ')


def line_numbers_string(block: FencedBlock) -> str:
    """Return string showing code/output block file line numbers."""
    code_identifier = 'code_' + str(block.line)
    output_identifier = ''
    if block.output:
        output_identifier = '_output_' + str(block.output.line)
    return code_identifier + output_identifier
