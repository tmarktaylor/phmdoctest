import doctest
import re

import pytest

import phmdoctest.main
import phmdoctest.simulator

# Caution:
# This test file is run by pytest.
# The call to invoke_and_pytest() will re-enter pytest main.
# Pytest captures stdout and so do both CliRunner.invoke()
# and the pytest main run by invoke_and_pytest().


def fenced_code_blocks_contents_list(markdown_filename):
    """Return Markdown fenced code block contents as a list of strings."""
    with open(markdown_filename, encoding='utf-8') as fp:
        nodes = phmdoctest.main.fenced_block_nodes(fp)
        return [node.literal for node in nodes]


def line_by_line_compare_exact(want, got):
    """Line by line helper compare function with assertion for pytest."""
    if want:
        want_lines = want.splitlines()
        got_lines = got.splitlines()
        for want_line, got_line in zip(want_lines, got_lines):
            assert want_line == got_line


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
    return result


def setup_module():
    """Collect Markdown fenced code blocks contents from README.md."""
    # test cases below iterate through the blocks.
    global readme_blocks
    readme_blocks = iter(fenced_code_blocks_contents_list('README.md'))


def test_raw_example1_md():
    """README raw markdown is same as file tests/example1.md."""
    want = next(readme_blocks)
    with open('tests/example1.md') as fp:
        got = fp.read()
        line_by_line_compare_exact(want, got)


def test_example1():
    """Make sure generated --outfile is as expected; Run pytest.

    Check the copy of test_example1.py in the fenced code block.
    """
    # The helper checks the generated --outfile against the disk file.
    example1_command = next(readme_blocks)
    _ = example_helper(
        example1_command,
        want_file_name='doc/test_example1.py',
        pytest_options=None
    )
    # Make sure the copy of test_example1.py in README.md
    # is the same as the disk file.
    want = next(readme_blocks)
    with open('doc/test_example1.py') as fp:
        got = fp.read()
        line_by_line_compare_exact(want, got)

    # Run again and call pytest to make sure the file works with pytest.
    _ = example_helper(
        example1_command,
        want_file_name=None,
        pytest_options=['--strict', '-vv']
    )


def test_report():
    """README report output is same as produced by the command."""
    report_command = next(readme_blocks)
    result = phmdoctest.simulator.run_and_pytest(
        report_command, pytest_options=None)
    want = next(readme_blocks)
    got = result.status.stdout
    line_by_line_compare_exact(want, got)


def test_skip_example():
    """Make sure generated --outfile and --report are as expected."""
    skip_command = next(readme_blocks)
    result = example_helper(
        skip_command,
        want_file_name='doc/test_example2.py',
        pytest_options=None
    )
    want = next(readme_blocks)    # get the skip report
    got = result.status.stdout
    line_by_line_compare_exact(want, got)

    # test the first -s form of the --skip
    short_form_command = next(readme_blocks)
    result = example_helper(
        short_form_command,
        want_file_name='doc/test_example2.py',
        pytest_options=None
    )
    got = result.status.stdout
    line_by_line_compare_exact(want, got)


def test_outfile_to_stdout():
    """Make sure generated --outfile and --report are as expected."""
    outfile_command1 = next(readme_blocks)
    result = example_helper(
        outfile_command1,
        want_file_name='doc/test_example2.py',
        pytest_options=None
    )
    with open('doc/test_example2.py') as fp:
        want = fp.read()
    got = result.status.stdout
    line_by_line_compare_exact(want, got)

    outfile_command2 = next(readme_blocks)
    result = example_helper(
        outfile_command2,
        want_file_name='doc/test_example2.py',
        pytest_options=None
    )
    got = result.status.stdout
    line_by_line_compare_exact(want, got)


def test_usage():
    """Example usage near the bottom."""
    # Note- There may be differences in whitespace between
    #       the README.md fenced code block and the
    #       phmdoctest --help output caused by the
    #       the terminal width when the installed
    #       phmdoctest command is executed.
    # Note- This test runs phmdoctest by calling the simulator
    #       which calls  Click.CliRunner.invoke().  invoke()
    #       displays entry-point as the calling program.
    #       The test here replaces 'entry-point' with 'phmdoctest'.
    result = phmdoctest.simulator.run_and_pytest(
        'phmdoctest --help', pytest_options=None)
    want1 = next(readme_blocks)
    want2 = re.sub(r'\s+', ' ', want1)

    got1 = result.status.stdout
    got2 = got1.replace('entry-point', 'phmdoctest', 1)
    got3 = re.sub(r'\s+', ' ', got2)
    assert want2 == got3


def test_yaml():
    """Show that first few lines of .travis.yml are same as in Markdown."""
    with open('.travis.yml', 'r', encoding='utf-8') as f:
        got1 = f.read()
    want = next(readme_blocks)
    # Take the same number of characters from the file .travis.yml
    # as are in the Markdown fenced code block.
    got2 = got1[:len(want)]
    line_by_line_compare_exact(want, got2)


def example_code():
    import phmdoctest.simulator
    command = 'phmdoctest tests/example2.md --report --outfile test_me.py'
    result = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command,
        pytest_options=['--strict', '-vv']
    )
    assert result.status.exit_code == 0
    assert result.pytest_exit_code == 0


def test_simulator_python_code():
    """Assure the guts of example_code() above are same as in Markdown."""
    import inspect
    import textwrap
    want1 = next(readme_blocks)
    want2 = textwrap.indent(want1, '    ')
    got1 = inspect.getsource(example_code)
    got2 = got1.replace('def example_code():\n', '')
    line_by_line_compare_exact(want2, got2)
    # also make sure the code runs with no assertions
    example_code()


def test_consumed_all_fenced_code_blocks():
    """Verify no left over fenced code blocks from README.md"""
    with pytest.raises(StopIteration):
        _ = next(readme_blocks)


# This test case is expected to fail when run.
# If it does not fail something isn't right.
@pytest.mark.xfail(strict=True)
def test_unexpected_output_pytests():
    """Make sure pytest fails due to incorrect expected output in the .md."""
    _ = example_helper(
        'phmdoctest tests/unexpected_output.md --outfile test_unexpected_output.py',
        want_file_name=None,
        pytest_options=['--strict', '-vv']
    )
