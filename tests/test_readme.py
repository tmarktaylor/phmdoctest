"""pytest test cases for examples in fenced code blocks in README.md."""

import inspect
import re
import textwrap

import pytest

import phmdoctest.main
import phmdoctest.simulator
import phmdoctest.tool
import verify

# Caution:
# This test file is run by pytest.
# The call to invoke_and_pytest() will start pytest in a
# subprocess.
# Pytest captures stdout and so does CliRunner.invoke().


readme_blocks = []


def setup_module():
    """Collect Markdown fenced code blocks contents from README.md.

    The test cases here must be run in order because they
    pop items from the list readme_blocks.

    This means using a pytest -k KEY more specific than
    "-k test_readme" risks taking the wrong block from the
    iterator readme_blocks causing all subsequent test_readme
    test case to fail.
    """
    # test cases below iterate through the blocks.
    global readme_blocks
    readme_blocks = iter(phmdoctest.tool.fenced_code_blocks('README.md'))


def test_raw_example1_md():
    """README raw markdown is same as file doc/example1.md."""
    want = next(readme_blocks)
    with open('doc/example1.md', 'r', encoding='utf-8') as fp:
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
    with open('doc/test_example1.py', 'r', encoding='utf-8') as fp:
        got = fp.read()
        verify.a_and_b_are_the_same(want, got)

    # Run again and call pytest to make sure the file works with pytest.
    simulator_status = verify.one_example(
        example1_command,
        want_file_name=None,
        pytest_options=['--doctest-modules', '-v']
    )
    assert simulator_status.pytest_exit_code == 0


def test_report():
    """README report output is same as produced by the command."""
    report_command = next(readme_blocks)
    want = next(readme_blocks)
    simulator_status = phmdoctest.simulator.run_and_pytest(
        report_command, pytest_options=None)
    got = simulator_status.runner_status.stdout
    verify.a_and_b_are_the_same(want, got)


def test_skip_example():
    """Make sure generated --outfile and --report are as expected."""
    skip_command = next(readme_blocks)
    want = next(readme_blocks)    # get the skip report
    short_form_command = next(readme_blocks)
    simulator_status = verify.one_example(
        skip_command,
        want_file_name='doc/test_example2.py',
        pytest_options=None
    )
    got1 = simulator_status.runner_status.stdout
    verify.a_and_b_are_the_same(want, got1)

    # test the first -s form of the --skip
    simulator_status = verify.one_example(
        short_form_command,
        want_file_name='doc/test_example2.py',
        pytest_options=None
    )
    got2 = simulator_status.runner_status.stdout
    verify.a_and_b_are_the_same(want, got2)


def test_setup_first_fcb():
    """Make sure example setup fenced code block same as in the file."""
    want = next(readme_blocks)    # get the setup block example
    blocks = phmdoctest.tool.fenced_code_blocks('doc/setup.md')
    got = blocks[0]
    verify.a_and_b_are_the_same(want, got)


def test_setup_report_example():
    """Make sure report in README is correct."""
    command = next(readme_blocks)
    want = next(readme_blocks)    # get the report
    simulator_status = verify.one_example(
        command,
        want_file_name=None,
        pytest_options=None
    )
    got1 = simulator_status.runner_status.stdout
    verify.a_and_b_are_the_same(want, got1)


def test_setup():
    """Make sure --setup --outfile is correct."""
    command = next(readme_blocks)
    _ = verify.one_example(
        command,
        want_file_name='doc/test_setup.py',
        pytest_options=None
    )


def test_setup_doctest():
    """Make sure --setup-doctest --outfile is correct."""
    command = next(readme_blocks)
    _ = verify.one_example(
        command,
        want_file_name='doc/test_setup_doctest.py',
        pytest_options=None
    )


def test_outfile_to_stdout():
    """Make sure generated --outfile and --report are as expected."""
    outfile_command1 = next(readme_blocks)
    outfile_command2 = next(readme_blocks)
    simulator_status = verify.one_example(
        outfile_command1,
        want_file_name=None,
        pytest_options=None
    )
    with open('doc/test_example2.py', 'r', encoding='utf-8') as fp:
        want = fp.read()
    got1 = simulator_status.runner_status.stdout
    verify.a_and_b_are_the_same(want, got1)

    simulator_status = verify.one_example(
        outfile_command2,
        want_file_name=None,
        pytest_options=None
    )
    got2 = simulator_status.runner_status.stdout
    verify.a_and_b_are_the_same(want, got2)


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
    simulator_status = phmdoctest.simulator.run_and_pytest(
        'phmdoctest --help', pytest_options=None)
    want1 = next(readme_blocks)
    want2 = re.sub(r'\s+', ' ', want1)

    got1 = simulator_status.runner_status.stdout
    got2 = got1.replace('entry-point', 'phmdoctest', 1)
    got3 = re.sub(r'\s+', ' ', got2)
    verify.a_and_b_are_the_same(want2, got3)


def test_yaml():
    """Show Markdown example and .travis.yml have the same commands."""
    markdown_example_text = next(readme_blocks)
    expected = """\
dist: xenial
language: python
sudo: false

matrix:
  include:
    - python: 3.5
      install:
        - pip install "." pytest
      script:
        - mkdir tests/tmp
        - phmdoctest project.md --report --outfile tests/tmp/test_project.py
        - pytest --doctest-modules -vv tests"""
    verify.a_and_b_are_the_same(expected, markdown_example_text)
    with open('.travis.yml', 'r', encoding='utf-8') as f:
        travis_text = f.read()
        assert travis_text.startswith(expected)


# Developers: Changes here must be mirrored in a Markdown FCB in README.md.
# Runnable version of example code in README.md.
# The guts of this function are an exact copy of example in README.md.
def example_code():
    import phmdoctest.simulator
    command = 'phmdoctest doc/example1.md --report --outfile test_me.py'
    simulator_status = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command,
        pytest_options=['--doctest-modules', '-v']
    )
    assert simulator_status.runner_status.exit_code == 0
    assert simulator_status.pytest_exit_code == 0


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
