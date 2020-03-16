import re

import click
import pytest

import phmdoctest
import phmdoctest.main
import phmdoctest.simulator
import verify


class TestSameVersions:
    """Verify same release version string in all places.

    Obtain the version string from various places in the source tree
    and check that they are all the same.
    This test does not prove the version is correct.

    Whitespace around the equals sign in the version statement IS significant.
    """
    module_version_attribute = phmdoctest.__version__

    def test_readme_md(self):
        """Check the version in the second line of README.md."""
        with open('README.md', 'r', encoding='utf-8') as f:
            readme_text = f.readlines()[1]
        assert readme_text.startswith('## version ')
        assert self.module_version_attribute in readme_text

    def test_setup_py(self):
        """Check the version anywhere in setup.py."""
        with open('setup.py', 'r', encoding='utf-8') as f:
            setup_text = f.read()
        # keep the part between single or double quotes after version=
        match = re.search(r" *version=['\"]([^'\"]*)['\"]", setup_text, re.M)
        assert match.group(1) == self.module_version_attribute


def test_skip_same_block_twice():
    """Show identifying a skipped code block more than one time is OK."""
    command = (
        'phmdoctest tests/example2.md --skip "Python 3.7" --skip LAST'
        ' --skip LAST --report --outfile discarded.py'
    )
    result = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command,
        pytest_options=['--strict', '-v']
    )
    assert result.status.exit_code == 0
    assert result.pytest_exit_code == 0


def test_pytest_really_fails():
    """Make sure pytest fails due to incorrect expected output in the .md."""
    with pytest.raises(AssertionError) as excinfo:
        _ = verify.one_example(
            'phmdoctest tests/unexpected_output.md --outfile test_unexpected_output.py',
            want_file_name=None,
            pytest_options=['--strict', '-v']
        )
    assert excinfo.type == AssertionError


def test_def_test_nothing_fails():
    """This is done for code coverage of the function."""
    with pytest.raises(AssertionError):
        phmdoctest.main.test_nothing_fails()


def test_def_test_nothing_passes():
    """This is done for code coverage of the function."""
    phmdoctest.main.test_nothing_passes()


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


def test_skip_first():
    """Verify --skip FIRST."""
    command = (
        'phmdoctest tests/example2.md --skip "Python 3.7" -sFIRST'
        ' --skip LAST --report --outfile discarded.py'
    )
    result = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command,
        pytest_options=['--strict', '-v']
    )
    assert result.status.exit_code == 0
    assert result.pytest_exit_code == 0
    assert 'py3         9  skip-code    "FIRST"' in result.status.stdout
    assert 'FIRST         9' in result.status.stdout


def test_skip_second():
    """Verify --skip SECOND."""
    command = (
        'phmdoctest tests/example2.md --skip SECOND'
        ' --report --outfile discarded.py'
    )
    result = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command,
        pytest_options=['--strict', '-v']
    )
    assert result.status.exit_code == 0
    assert result.pytest_exit_code == 0
    assert 'py3        20  skip-code    "SECOND"' in result.status.stdout
    assert 'SECOND        20' in result.status.stdout


def test_skip_second_when_only_one():
    """Verify --skip SECOND selects no block when only 1 code block."""
    command = (
        'phmdoctest tests/example1.md -sFIRST'
        ' --skip SECOND --report --outfile discarded.py'
    )
    result = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command,
        pytest_options=['--strict', '-v']
    )
    assert result.status.exit_code == 0
    assert result.pytest_exit_code == 0
    assert 'def test_nothing_passes()' in result.outfile
    assert 'SECOND\n' in result.status.stdout


def test_skip_second_when_more_than_one():
    """Verify --skip SECOND when more than 1 code block."""
    command = (
        'phmdoctest tests/example2.md -sFIRST'
        ' --skip SECOND --report --outfile discarded.py'
    )
    result = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command,
        pytest_options=['--strict', '-v']
    )
    assert result.status.exit_code == 0
    assert result.pytest_exit_code == 0
    assert 'py3        20  skip-code    "SECOND"' in result.status.stdout
    assert 'SECOND        20' in result.status.stdout


def test_skip_code_tha_has_no_output_block():
    """Verify --skip SECOND when more than 1 code block."""
    command = (
        'phmdoctest tests/example2.md --skip="while a < 1000:"'
        ' --report --outfile discarded.py'
    )
    result = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command,
        pytest_options=['--strict', '-v']
    )
    assert result.status.exit_code == 0
    assert result.pytest_exit_code == 0
    assert 'py3        37  skip-code  "while a < 1000:"' in result.status.stdout
    assert 'while a < 1000:  37' in result.status.stdout


def test_no_blocks_left_to_test_passing():
    """Generate a pytest file that passes when no blocks to test."""
    command = (
        'phmdoctest tests/example1.md -sFIRST'
        ' --skip SECOND --report --outfile discarded.py'
    )
    result = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command,
        pytest_options=['--strict', '-v']
    )
    assert result.status.exit_code == 0
    assert result.pytest_exit_code == 0
    assert 'def test_nothing_passes()' in result.outfile


def test_no_blocks_left_to_test_fails():
    """Generate a pytest file that asserts when no blocks to test."""
    command = (
        'phmdoctest tests/example1.md -sFIRST --fail-nocode'
        ' --skip SECOND --report --outfile discarded.py'
    )
    result = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command,
        pytest_options=['--strict', '-v']
    )
    assert result.status.exit_code == 0
    assert result.pytest_exit_code == 1    # pytest failed
    assert 'def test_nothing_fails()' in result.outfile


def test_no_code_blocks():
    """Process .md that has no code blocks."""
    command = (
        'phmdoctest tests/no_code_blocks.md'
        ' --report --outfile discarded.py'
    )
    result = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command,
        pytest_options=['--strict', '-v']
    )
    assert result.status.exit_code == 0
    assert result.pytest_exit_code == 0
    assert 'def test_nothing_passes()' in result.outfile


def test_missing_markdown_file():
    """Usage error for MARKDOWN_FILE that does not exist."""
    command = 'phmdoctest tests/bogus.md --outfile discarded.py'
    result = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command,
        pytest_options=['--strict', '-v']
    )
    assert result.status.exit_code == click.UsageError.exit_code
    assert result.outfile is None
    assert result.pytest_exit_code is None


def test_bad_usage_option():
    """Usage error for misspelled option."""
    command = 'phmdoctest tests/example1.md --troper --outfile discarded.py'
    result = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command,
        pytest_options=['--strict', '-v']
    )
    assert result.status.exit_code == click.UsageError.exit_code
    assert result.outfile is None
    assert result.pytest_exit_code is None