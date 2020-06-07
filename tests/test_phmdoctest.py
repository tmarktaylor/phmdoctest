"""pytest test cases for phmdoctest."""

import re

import click
import pytest

import phmdoctest
import phmdoctest.main
import phmdoctest.simulator
import phmdoctest.print_capture
import verify


# Caution:
# This test file is run by pytest.
# The call to invoke_and_pytest() will start pytest in a
# subprocess.
# Pytest captures stdout and so does CliRunner.invoke().

class TestSameVersions:
    """Verify same release version string in all places.

    Obtain the version string from various places in the source tree
    and check that they are all the same.
    Compare all the occurrences to phmdoctest.__version__.
    This test does not prove the version is correct.
    Whitespace may be significant in some cases.
    """
    package_version = phmdoctest.__version__

    def verify_found_in_file(self, filename, format_spec='{}'):
        """Format the package version and look for result in caller's file."""
        looking_for = format_spec.format(self.package_version)
        with open(filename, 'r', encoding='utf-8') as f:
            text = f.read()
        assert looking_for in text

    def test_readme_md(self):
        """Check the version near the top of README.md."""
        self.verify_found_in_file('README.md', '# phmdoctest {}')

    def test_index_rst(self):
        """Check the version is anywhere in index.rst."""
        self.verify_found_in_file('index.rst', 'phmdoctest {}\n=============')

    def test_recent_changes(self):
        """Check the version is anywhere in recent_changes.md."""
        self.verify_found_in_file('doc/recent_changes.md', '{} - ')

    def test_conf_py_release(self):
        """Check version in the release = line in conf.py."""
        self.verify_found_in_file('conf.py', "release = '{}'")

    def test_setup_py(self):
        """Check the version anywhere in setup.py."""
        with open('setup.py', 'r', encoding='utf-8') as f:
            setup_text = f.read()
        # keep the part between single or double quotes after version=
        match = re.search(r" *version=['\"]([^'\"]*)['\"]", setup_text, re.M)
        assert match.group(1) == self.package_version


class TestDocBuildVersions:
    """
    Some versions are the same in doc/requirements.txt and setup.py.

    Click and monotable versions should be the same.

    For the Sphinx documentation build on readthedocs.org (RTD)
    specific versions are pinned by the file doc/requirements.txt.

    For Sphinx autodoc the phmdoctest dependencies Click and monotable
    are installed so that the RTD build can import phmdoctest to look
    for docstrings.

    Note that commonmark is also a phmdoctest dependency. Because it is
    pinned to different versions in doc/requirements.txt and setup.py
    it is not tested here.
    """
    with open('doc/requirements.txt', 'r', encoding='utf-8') as f:
        doc_requirements = f.read()
        for line in doc_requirements.splitlines():
            if line.startswith('Click'):
                click_version = line
            if line.startswith('monotable'):
                monotable_version = line
    with open('setup.py', 'r', encoding='utf-8') as f:
        setup = f.read()

    @staticmethod
    def to_setup_style(value):
        """Convert value from requirements.txt style to setup.py style."""
        drop_newline = value.replace('\n', '', 1)
        drop_space = drop_newline.replace(' ', '', 1)
        quoted = drop_space.join(["'", "'"])
        return quoted

    def test_click(self):
        """Click version in doc/requirements.txt same as setup.py"""
        assert self.click_version in self.doc_requirements, 'sanity check'
        expected = self.to_setup_style(self.click_version)
        assert self.setup.count(expected) == 1

    def test_monotable(self):
        """monotable version in doc/requirements.txt same as setup.py"""
        assert self.monotable_version in self.doc_requirements, 'sanity check'
        expected = self.to_setup_style(self.monotable_version)
        assert self.setup.count(expected) == 1


def test_def_test_nothing_fails():
    """This is done for code coverage of the function."""
    with pytest.raises(AssertionError):
        phmdoctest.main.test_nothing_fails()


def test_def_test_nothing_passes():
    """This is done for code coverage of the function."""
    phmdoctest.main.test_nothing_passes()


def test_empty_output_block_fails():
    """Empty output block causes phmdoctest to raise AssertionError."""
    command = (
        'phmdoctest tests/empty_output_block.md --outfile discarded.py'
    )
    simulator_status = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command,
        pytest_options=None
    )
    exc = simulator_status.runner_status.exception
    assert 'zero length expected output block' in str(exc)
    assert simulator_status.runner_status.exit_code == 1


def test_code_does_not_print_fails():
    """Show empty stdout mis-compares with non-empty output block."""
    command = (
        'phmdoctest tests/does_not_print.md --outfile discarded.py'
    )
    simulator_status = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command,
        pytest_options=['--strict', '-v']
    )
    assert simulator_status.runner_status.exit_code == 0
    assert simulator_status.pytest_exit_code == 1


def test_more_printed_than_expected_fails():
    """Show pytest fails when more lines are printed than expected."""
    command = (
        'phmdoctest tests/missing_some_output.md --outfile discarded.py'
    )
    simulator_status = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command,
        pytest_options=['--strict', '-v']
    )
    assert simulator_status.runner_status.exit_code == 0
    assert simulator_status.pytest_exit_code == 1


def test_more_expected_than_printed_fails():
    """Show pytest fails when more lines are printed than expected."""
    command = (
        'phmdoctest tests/extra_line_in_output.md --outfile discarded.py'
    )
    simulator_status = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command,
        pytest_options=['--strict', '-v']
    )
    assert simulator_status.runner_status.exit_code == 0
    assert simulator_status.pytest_exit_code == 1


def test_skip_same_block_twice():
    """Show identifying a skipped code block more than one time is OK."""
    command = (
        'phmdoctest doc/example2.md --skip "Python 3.7" --skip LAST'
        ' --skip LAST --report --outfile discarded.py'
    )
    simulator_status = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command,
        pytest_options=['--strict', '-v']
    )
    assert simulator_status.runner_status.exit_code == 0
    assert simulator_status.pytest_exit_code == 0


def test_pytest_really_fails():
    """Make sure pytest fails due to incorrect expected output in the .md.

    Generate a pytest that will assert.
    """
    simulator_status = verify.one_example(
        'phmdoctest tests/unexpected_output.md --outfile test_unexpected_output.py',
        want_file_name=None,
        pytest_options=['--strict', '-v']
    )
    assert simulator_status.pytest_exit_code == 1


def test_def_test_identifier():
    """Painful way to eliminate 2 coverage missed statements."""
    # The function print_capture.test_identifier() is used as
    # a template to generate Python code.
    # It accepts the pytest fixture called capsys when the
    # generated pytest is run.
    # phmodctest doesn't call this function so it shows up
    # in the coverage report as a missed statement.
    # Here a test mock up of the fixture is created that
    # provides the expected value as its out attribute.
    class MockReadouterr:
        def __init__(self):
            self.out = '<<<replaced>>>'

    class MockCapsys:
        @staticmethod
        def readouterr():
            return MockReadouterr()

    phmdoctest.print_capture.test_identifier(MockCapsys())


def test_blanklines_in_output():
    """Expected output has empty lines and does not have doctest <BLANKLINE>."""
    command = (
        'phmdoctest tests/output_has_blank_lines.md --outfile discarded.py'
    )
    simulator_status = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command,
        pytest_options=['--strict', '-v']
    )
    assert simulator_status.runner_status.exit_code == 0
    assert simulator_status.pytest_exit_code == 0


def test_skip_first():
    """Verify --skip FIRST."""
    command = (
        'phmdoctest doc/example2.md --skip "Python 3.7" -sFIRST'
        ' --skip LAST --report --outfile discarded.py'
    )
    simulator_status = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command,
        pytest_options=['--strict', '-v']
    )
    assert simulator_status.runner_status.exit_code == 0
    assert simulator_status.pytest_exit_code == 0
    stdout = simulator_status.runner_status.stdout
    assert 'py3         9  skip-code    "FIRST"' in stdout
    assert 'FIRST         9' in stdout


def test_skip_second():
    """Verify --skip SECOND."""
    command = (
        'phmdoctest doc/example2.md --skip SECOND'
        ' --report --outfile discarded.py'
    )
    simulator_status = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command,
        pytest_options=['--strict', '-v']
    )
    assert simulator_status.runner_status.exit_code == 0
    assert simulator_status.pytest_exit_code == 0
    stdout = simulator_status.runner_status.stdout
    assert 'py3        20  skip-code    "SECOND"' in stdout
    assert 'SECOND        20' in stdout


def test_skip_second_when_only_one():
    """Verify --skip SECOND selects no block when only 1 code block."""
    command = (
        'phmdoctest doc/example1.md -sFIRST'
        ' --skip SECOND --report --outfile discarded.py'
    )
    simulator_status = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command,
        pytest_options=['--strict', '-v']
    )
    assert simulator_status.runner_status.exit_code == 0
    assert simulator_status.pytest_exit_code == 0
    assert 'def test_nothing_passes()' in simulator_status.outfile
    assert 'SECOND\n' in simulator_status.runner_status.stdout


def test_skip_second_when_more_than_one():
    """Verify --skip SECOND when more than 1 code block."""
    command = (
        'phmdoctest doc/example2.md -sFIRST'
        ' --skip SECOND --report --outfile discarded.py'
    )
    simulator_status = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command,
        pytest_options=['--strict', '-v']
    )
    assert simulator_status.runner_status.exit_code == 0
    assert simulator_status.pytest_exit_code == 0
    stdout = simulator_status.runner_status.stdout
    assert 'py3        20  skip-code    "SECOND"' in stdout
    assert 'SECOND        20' in stdout


def test_skip_code_that_has_no_output_block():
    """Skip code with no output block."""
    command = (
        'phmdoctest doc/example2.md --skip SECOND --skip="while a < 1000:"'
        ' --report --outfile discarded.py'
    )
    simulator_status = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command,
        pytest_options=['--strict', '-v']
    )
    assert simulator_status.runner_status.exit_code == 0
    assert simulator_status.pytest_exit_code == 0
    stdout = simulator_status.runner_status.stdout
    assert 'py3        20  skip-code    "SECOND"' in stdout
    assert 'py3        37  skip-code    "while a < 1000:"' in stdout
    assert 'SECOND           20' in stdout
    assert 'while a < 1000:  37' in stdout


def test_skip_matches_start_of_contents():
    """Skip pattern matching first characters of code block."""
    command = (
        'phmdoctest doc/example2.md --skip SECOND --skip="Python 3.7"'
        '  --skip="words =" --report --outfile discarded.py'
    )
    simulator_status = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command,
        pytest_options=['--strict', '-vv']
    )
    assert simulator_status.runner_status.exit_code == 0
    assert simulator_status.pytest_exit_code == 0
    stdout = simulator_status.runner_status.stdout
    assert 'words =       44' in stdout


# words = ['cat', 'window', 'defenestrate']

def test_multiple_skips_report():
    """More than one skip applied to the same Python code block."""
    command = 'phmdoctest doc/example2.md --report -sprint -slen'
    simulator_status = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command,
        pytest_options=None
    )
    assert simulator_status.runner_status.exit_code == 0
    stdout = simulator_status.runner_status.stdout
    assert '                            "len"' in stdout
    assert 'len           44' in stdout


def test_no_blocks_left_to_test_passing():
    """Generate a pytest file that passes when no blocks to test."""
    command = (
        'phmdoctest doc/example1.md -sFIRST'
        ' --skip SECOND --report --outfile discarded.py'
    )
    simulator_status = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command,
        pytest_options=['--strict', '-v']
    )
    assert simulator_status.runner_status.exit_code == 0
    assert simulator_status.pytest_exit_code == 0
    assert 'def test_nothing_passes()' in simulator_status.outfile


def test_no_blocks_left_to_test_fails():
    """Generate a pytest file that asserts when no blocks to test."""
    command = (
        'phmdoctest doc/example1.md -sFIRST --fail-nocode'
        ' --skip SECOND --report --outfile discarded.py'
    )
    simulator_status = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command,
        pytest_options=['--strict', '-v']
    )
    assert simulator_status.runner_status.exit_code == 0
    assert simulator_status.pytest_exit_code == 1    # pytest failed
    assert 'def test_nothing_fails()' in simulator_status.outfile


def test_no_code_blocks():
    """Process .md that has no code blocks."""
    command = (
        'phmdoctest tests/no_code_blocks.md'
        ' --report --outfile discarded.py'
    )
    simulator_status = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command,
        pytest_options=['--strict', '-v']
    )
    assert simulator_status.runner_status.exit_code == 0
    assert simulator_status.pytest_exit_code == 0
    assert 'def test_nothing_passes()' in simulator_status.outfile


def test_missing_markdown_file():
    """Usage error for MARKDOWN_FILE that does not exist."""
    command = 'phmdoctest tests/bogus.md --outfile discarded.py'
    simulator_status = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command,
        pytest_options=['--strict', '-v']
    )
    assert (
        simulator_status.runner_status.exit_code ==
        click.UsageError.exit_code
    )
    assert simulator_status.outfile is None
    assert simulator_status.pytest_exit_code is None


def test_bad_usage_option():
    """Usage error for misspelled option."""
    command = 'phmdoctest doc/example1.md --troper --outfile discarded.py'
    simulator_status = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command,
        pytest_options=['--strict', '-v']
    )
    assert (
        simulator_status.runner_status.exit_code == click.UsageError.exit_code
    )
    assert simulator_status.outfile is None
    assert simulator_status.pytest_exit_code is None
