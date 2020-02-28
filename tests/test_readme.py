import re

import pytest

import phmdoctest.main
import phmdoctest.simulator

# Caution:
# This test file is run by pytest.
# The call to invoke_and_pytest() will re-enter pytest main.
# Pytest captures stdout and so do both CliRunner.invoke()
# and the pytest main run by invoke_and_pytest().


def list_of_fcb_contents(markdown_filename):
    """Return Markdown fenced code block contents as a list of strings."""
    with open(markdown_filename, encoding='utf-8') as fp:
        nodes = phmdoctest.main.fenced_block_nodes(fp)
        return [node.literal for node in nodes]


def setup_module():
    """Collect Markdown fenced code blocks contents from README.md."""
    # Several test_readme_* test cases below iterate through the blocks.
    global readme_blocks
    readme_blocks = iter(list_of_fcb_contents('README.md'))


def line_by_line_compare_exact(want, got):
    """Line by line helper compare function with assertion for pytest."""
    if want:
        want_lines = want.splitlines()
        got_lines = got.splitlines()
        for want_line, got_line in zip(want_lines, got_lines):
            assert want_line == got_line


def test_readme_raw_example1_md():
    """README.md raw markdown is same as file tests/example1.md."""
    got = next(readme_blocks)
    with open('tests/example1.md') as fp:
        want = fp.read()
        line_by_line_compare_exact(want, got)


def test_readme_example1_py():
    """README.md code block is the same as file test_example1.py."""
    got = next(readme_blocks)
    with open('doc/test_example1.py') as fp:
        want = fp.read()
        line_by_line_compare_exact(want, got)


# todo- new example
# todo- still need to check stdout for --report
# todo- still need to check stdout for --skip options
# todo- still need to check stdout for --outfile "-"


def collapse_whitespace(text):
    # collapse runs of whitespace to a single blank
    return re.sub(r'\s+', ' ', text)


def test_readme_usage_py():
    """README.md example usage (near the bottom of README.md)."""
    # Note- There may be differences in whitespace between
    #       the README.md fenced code block and the
    #       phmdoctest --help output caused by the
    #       the terminal width when the installed
    #       phmdoctest command is executed.
    # Note- This test runs phmdoctest by calling the simulator
    #       which calls  Click.CliRunner.invoke().  invoke()
    #       displays entry-point as the calling program.
    #       The test here replaces 'entry-point' with 'phmdoctest'.
    _ = next(readme_blocks)    # todo- delete
    _ = next(readme_blocks)    # todo- delete
    _ = next(readme_blocks)    # todo- delete
    result = phmdoctest.simulator.run_and_pytest(
        'phmdoctest --help', pytest_options=None)
    want1 = result.status.stdout
    want2 = want1.replace('entry-point', 'phmdoctest', 1)
    want3 = collapse_whitespace(want2)
    got1 = next(readme_blocks)
    got2 = collapse_whitespace(got1)
    assert want3 == got2


def example_helper(
        phmdoctest_command,
        want_file_name=None,
        pytest_options=None):
    """Simulate running a phmdoctest command and pytest on the result."""
    result = phmdoctest.simulator.run_and_pytest(
        phmdoctest_command, pytest_options=pytest_options)
    # check that the phmdoctest command succeeded
    assert result.status.exit_code == 0

    # check the OUTFILE against the expected value
    if want_file_name is not None:
        with open(want_file_name) as f:
            want = f.read()
            line_by_line_compare_exact(result.outfile, want)

    if pytest_options is not None:
        assert result.pytest_exit_code == 0


def test_example1():
    """Make sure generated --outfile is as expected."""
    example_helper(
        'phmdoctest tests/example1.md --outfile test_example1.py',
        want_file_name='doc/test_example1.py',
        pytest_options=None
    )


def test_example1_plus_pytest():
    """Make sure pytest succeeds on generated --outfile."""
    example_helper(
        'phmdoctest tests/example1.md --outfile test_example1.py',
        want_file_name=None,
        pytest_options=['--strict', '-vv']
    )


# This test case is expected to fail when run.
# If it does not fail something isn't right.
@pytest.mark.xfail(strict=True)
def test_unexpected_output_pytests():
    """Make sure pytest fails due to incorrect expected output in the .md."""
    example_helper(
        'phmdoctest tests/unexpected_output.md --outfile test_unexpected_output.py',
        want_file_name=None,
        pytest_options=['--strict', '-vv']
    )
