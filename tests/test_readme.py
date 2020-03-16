import inspect
import re
import textwrap

import pytest

import phmdoctest.main
import phmdoctest.simulator
import phmdoctest.print_capture
import phmdoctest.tool
import verify

# Caution:
# This test file is run by pytest.
# The call to invoke_and_pytest() will re-enter pytest main.
# Pytest captures stdout and so do both CliRunner.invoke()
# and the pytest main run by invoke_and_pytest().


def setup_module():
    """Collect Markdown fenced code blocks contents from README.md."""
    # test cases below iterate through the blocks.
    global readme_blocks
    readme_blocks = iter(phmdoctest.tool.fenced_code_blocks('README.md'))


def test_raw_example1_md():
    """README raw markdown is same as file tests/example1.md."""
    want = next(readme_blocks)
    with open('tests/example1.md') as fp:
        got = fp.read()
        verify.a_and_b_are_the_same(want, got)


def test_example1():
    """Make sure generated --outfile is as expected; Run pytest.

    Check the copy of test_example1.py in the fenced code block.
    """
    # The helper checks the generated --outfile against the disk file.
    example1_command = next(readme_blocks)
    want = next(readme_blocks)
    _ = verify.one_example(
        example1_command,
        want_file_name='doc/test_example1.py',
        pytest_options=None
    )
    # Make sure the copy of test_example1.py in README.md
    # is the same as the disk file.
    with open('doc/test_example1.py') as fp:
        got = fp.read()
        verify.a_and_b_are_the_same(want, got)

    # Run again and call pytest to make sure the file works with pytest.
    _ = verify.one_example(
        example1_command,
        want_file_name=None,
        pytest_options=['--strict', '-v']
    )


def test_report():
    """README report output is same as produced by the command."""
    report_command = next(readme_blocks)
    want = next(readme_blocks)
    result = phmdoctest.simulator.run_and_pytest(
        report_command, pytest_options=None)
    got = result.status.stdout
    verify.a_and_b_are_the_same(want, got)


def test_skip_example():
    """Make sure generated --outfile and --report are as expected."""
    skip_command = next(readme_blocks)
    want = next(readme_blocks)    # get the skip report
    short_form_command = next(readme_blocks)
    result = verify.one_example(
        skip_command,
        want_file_name='doc/test_example2.py',
        pytest_options=None
    )
    got = result.status.stdout
    verify.a_and_b_are_the_same(want, got)

    # test the first -s form of the --skip
    result = verify.one_example(
        short_form_command,
        want_file_name='doc/test_example2.py',
        pytest_options=None
    )
    got = result.status.stdout
    verify.a_and_b_are_the_same(want, got)


def test_outfile_to_stdout():
    """Make sure generated --outfile and --report are as expected."""
    outfile_command1 = next(readme_blocks)
    outfile_command2 = next(readme_blocks)
    result = verify.one_example(
        outfile_command1,
        want_file_name='doc/test_example2.py',
        pytest_options=None
    )
    with open('doc/test_example2.py') as fp:
        want = fp.read()
    got = result.status.stdout
    verify.a_and_b_are_the_same(want, got)

    result = verify.one_example(
        outfile_command2,
        want_file_name='doc/test_example2.py',
        pytest_options=None
    )
    got = result.status.stdout
    verify.a_and_b_are_the_same(want, got)


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
    verify.a_and_b_are_the_same(want2, got3)


def test_yaml():
    """Show Markdown example and travis.yml have the same commands."""
    example_text = next(readme_blocks)
    install = '- pip install "." pytest'
    mkdir = '- mkdir tests/tmp'
    command = (
        '- phmdoctest project.md --report'
        ' --outfile tests/tmp/test_project_readme.py'
    )
    test = '- pytest --strict tests'
    assert install in example_text
    assert mkdir in example_text
    assert command in example_text
    assert test in example_text

    with open('.travis.yml', 'r', encoding='utf-8') as f:
        travis_text = f.read()
        assert install in travis_text
        assert mkdir in travis_text
        assert command in travis_text
        assert test in travis_text


# Developers: Changes here must be mirrored in a fenced code block in README.md.
# Runnable version of example code in README.md.
# The guts of this function are an exact copy of example in README.md.
def example_code():
    import phmdoctest.simulator
    command = 'phmdoctest tests/example2.md --report --outfile test_me.py'
    result = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command,
        pytest_options=['--strict', '-v']
    )
    assert result.status.exit_code == 0
    assert result.pytest_exit_code == 0


def test_simulator_python_code():
    """Assure the guts of example_code() above are same as in Markdown."""
    want1 = next(readme_blocks)
    want2 = textwrap.indent(want1, '    ')
    got1 = inspect.getsource(example_code)
    got2 = got1.replace('def example_code():\n', '')
    verify.a_and_b_are_the_same(want2, got2)
    # also make sure the code runs with no assertions
    example_code()


def test_consumed_all_fenced_code_blocks():
    """Verify no left over fenced code blocks from README.md"""
    with pytest.raises(StopIteration):
        _ = next(readme_blocks)
