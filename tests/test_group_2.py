"""Second group of pytest test cases for phmdoctest."""
from pathlib import Path

import phmdoctest
import phmdoctest.cases
import phmdoctest.main
import phmdoctest.simulator


def test_skip_first():
    """Verify --skip FIRST."""
    command = (
        'phmdoctest doc/example2.md --skip "Python 3.7" -sFIRST'
        " --skip LAST --report --outfile discarded.py"
    )
    simulator_status = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command, pytest_options=["--doctest-modules", "-v"]
    )
    assert simulator_status.runner_status.exit_code == 0
    assert simulator_status.pytest_exit_code == 0
    stdout = simulator_status.runner_status.stdout
    assert 'python       9  skip-code     "FIRST"' in stdout
    assert "FIRST         9" in stdout


def test_skip_second():
    """Verify --skip SECOND."""
    command = "phmdoctest doc/example2.md --skip SECOND --report --outfile discarded.py"
    simulator_status = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command, pytest_options=["--doctest-modules", "-v"]
    )
    assert simulator_status.runner_status.exit_code == 0
    assert simulator_status.pytest_exit_code == 0
    stdout = simulator_status.runner_status.stdout
    assert 'python      20  skip-code    "SECOND"' in stdout
    assert "SECOND        20" in stdout


def test_skip_first_session():
    """Verify --skip FIRST skips a session block."""
    command = (
        "phmdoctest tests/twentysix_session_blocks.md -sFIRST"
        " --report --outfile discarded.py"
    )
    simulator_status = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command, pytest_options=["--doctest-modules", "-v"]
    )
    assert simulator_status.runner_status.exit_code == 0
    assert simulator_status.pytest_exit_code == 0
    stdout = simulator_status.runner_status.stdout
    assert 'py          3  skip-session  "FIRST"' in stdout
    assert "FIRST         3" in stdout


def test_skip_second_session():
    """Verify --skip SECOND skips a session block."""
    command = (
        "phmdoctest tests/twentysix_session_blocks.md -sSECOND"
        " --report --outfile discarded.py"
    )
    simulator_status = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command, pytest_options=["--doctest-modules", "-v"]
    )
    assert simulator_status.runner_status.exit_code == 0
    assert simulator_status.pytest_exit_code == 0
    stdout = simulator_status.runner_status.stdout
    assert 'py          8  skip-session  "SECOND"' in stdout
    assert "SECOND        8" in stdout


def test_skip_second_when_only_one():
    """Verify --skip SECOND selects no block when only 1 code block."""
    command = (
        "phmdoctest tests/one_code_block.md -sFIRST"
        " --skip SECOND --report --outfile discarded.py"
    )
    simulator_status = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command, pytest_options=["--doctest-modules", "-v"]
    )
    assert simulator_status.runner_status.exit_code == 0
    assert simulator_status.pytest_exit_code == 0
    assert "def test_nothing_passes()" in simulator_status.outfile
    assert "SECOND\n" in simulator_status.runner_status.stdout


def test_skip_second_when_more_than_one():
    """Verify --skip SECOND when more than 1 code block."""
    command = (
        "phmdoctest doc/example2.md -sFIRST"
        " --skip SECOND --report --outfile discarded.py"
    )
    simulator_status = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command, pytest_options=["--doctest-modules", "-v"]
    )
    assert simulator_status.runner_status.exit_code == 0
    assert simulator_status.pytest_exit_code == 0
    stdout = simulator_status.runner_status.stdout
    assert 'python      20  skip-code    "SECOND"' in stdout
    assert "SECOND        20" in stdout


def test_skip_code_that_has_no_output_block():
    """Skip code with no output block."""
    command = (
        'phmdoctest doc/example2.md --skip SECOND --skip="while a < 1000:"'
        " --report --outfile discarded.py"
    )
    simulator_status = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command, pytest_options=["--doctest-modules", "-v"]
    )
    assert simulator_status.runner_status.exit_code == 0
    assert simulator_status.pytest_exit_code == 0
    stdout = simulator_status.runner_status.stdout
    assert 'python      20  skip-code    "SECOND"' in stdout
    assert 'python      37  skip-code    "while a < 1000:"' in stdout
    assert "SECOND           20" in stdout
    assert "while a < 1000:  37" in stdout


def test_skip_matches_start_of_contents():
    """Skip pattern matching first characters of code block."""
    command = (
        'phmdoctest doc/example2.md --skip SECOND --skip="Python 3.7"'
        '  --skip="words =" --report --outfile discarded.py'
    )
    simulator_status = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command, pytest_options=["--doctest-modules", "-v"]
    )
    assert simulator_status.runner_status.exit_code == 0
    assert simulator_status.pytest_exit_code == 0
    stdout = simulator_status.runner_status.stdout
    assert "words =       44" in stdout


def test_multiple_skips_report():
    """More than one skip applied to the same Python code block."""
    command = "phmdoctest doc/example2.md --report -sprint -slen"
    simulator_status = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command, pytest_options=None
    )
    assert simulator_status.runner_status.exit_code == 0
    assert simulator_status.pytest_exit_code is None
    stdout = simulator_status.runner_status.stdout
    assert '                            "len"' in stdout
    assert "len           44" in stdout


def test_one_skip_many_matches(checker):
    """Every block matches the skip pattern presenting multi-line report."""
    command = "phmdoctest tests/twentysix_session_blocks.md" ' --skip=">>>" --report'
    simulator_status = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command, pytest_options=None
    )
    assert simulator_status.runner_status.exit_code == 0
    assert simulator_status.pytest_exit_code is None
    stdout = simulator_status.runner_status.stdout
    want = Path("tests/twentysix_report.txt").read_text(encoding="utf-8")
    checker(want, stdout)


def test_no_output_blocks():
    """Generate test with no expected output comparison."""
    command = "phmdoctest tests/twentysix_session_blocks.md" " --outfile discarded.py"
    simulator_status = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command, pytest_options=None
    )
    assert simulator_status.runner_status.exit_code == 0
    assert simulator_status.pytest_exit_code is None
    assert simulator_status.outfile
    assert "phm_compare_exact" not in simulator_status.outfile
    assert "expected_str" not in simulator_status.outfile
