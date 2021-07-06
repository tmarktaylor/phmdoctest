"""Third group of pytest test cases for phmdoctest."""
import pytest
import click

import phmdoctest
import phmdoctest.cases
import phmdoctest.main
import phmdoctest.simulator
import verify


def test_missing_setup_for_setup_doctest():
    """Caller specifies --setup-doctest, but no --setup."""
    command = "phmdoctest doc/setup_doctest.md --setup-doctest --report"
    simulator_status = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command, pytest_options=None
    )
    assert simulator_status.runner_status.exit_code == 0
    assert simulator_status.pytest_exit_code is None
    stdout = simulator_status.runner_status.stdout
    # no blocks set to role setup
    assert not ("  setup" in stdout)
    want2 = "No setup block found, not honoring --setup-doctest."
    assert want2 in stdout


def test_no_match_for_setup():
    """Caller specifies --setup TEXT, but no block matches TEXT."""
    command = "phmdoctest doc/setup_doctest.md --setup NOTMATCHED --report"
    simulator_status = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command, pytest_options=None
    )
    assert simulator_status.runner_status.exit_code == 0
    assert simulator_status.pytest_exit_code is None
    stdout = simulator_status.runner_status.stdout
    # no blocks set to role setup
    assert not ("  setup" in stdout)
    assert "No setup block found." in stdout


def test_too_many_matches_for_setup():
    """Caller specifies --setup TEXT, but >1 blocks match TEXT."""
    command = "phmdoctest doc/setup_doctest.md --setup print --report"
    simulator_status = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command, pytest_options=None
    )
    assert simulator_status.runner_status.exit_code == 1
    assert simulator_status.pytest_exit_code is None
    stdout = simulator_status.runner_status.stdout
    assert "Error: More than one block matched command line" in stdout
    assert "--setup or -u." in stdout
    assert "Only one match is allowed." in stdout
    assert "The matching blocks are at line numbers 20, 37, 47" in stdout


def test_setup_is_not_code_block():
    """Caller --setup matches, but it is not a code block."""
    command = 'phmdoctest doc/setup_doctest.md --setup="mylist.append(55)" --report'
    simulator_status = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command, pytest_options=None
    )
    assert simulator_status.runner_status.exit_code == 0
    assert simulator_status.pytest_exit_code is None
    stdout = simulator_status.runner_status.stdout
    assert not ("  setup" in stdout)
    assert "No setup block found." in stdout


def test_setup_is_not_skipped_block():
    """Caller --setup matches, but the block is skipped."""
    command = "phmdoctest doc/setup_doctest.md --skip FIRST --setup FIRST` --report"
    simulator_status = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command, pytest_options=None
    )
    assert simulator_status.runner_status.exit_code == 0
    assert simulator_status.pytest_exit_code is None
    stdout = simulator_status.runner_status.stdout
    assert not ("  setup" in stdout)
    assert "No setup block found." in stdout


def test_setup_has_output_block():
    """The --setup block has an output block which gets role del-output."""
    command = "phmdoctest tests/empty_output_block.md --setup 19 --report"
    simulator_status = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command, pytest_options=None
    )
    assert simulator_status.runner_status.exit_code == 0
    assert simulator_status.pytest_exit_code is None
    stdout = simulator_status.runner_status.stdout
    assert 'python      22  setup       "19"' in stdout
    assert "            29  del-output" in stdout
    assert '2 blocks marked "del-". They are not tested.' in stdout


def test_no_match_for_teardown():
    """Caller specifies --teardown TEXT, but no block matches TEXT."""
    command = "phmdoctest doc/setup_doctest.md --teardown NOTMATCHED --report"
    simulator_status = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command, pytest_options=None
    )
    assert simulator_status.runner_status.exit_code == 0
    assert simulator_status.pytest_exit_code is None
    stdout = simulator_status.runner_status.stdout
    # no blocks set to role setup
    assert not ("  teardown" in stdout)
    want2 = "No teardown block found."
    assert want2 in stdout


def test_too_many_matches_for_teardown():
    """Caller specifies --teardown TEXT, but >1 blocks match TEXT."""
    command = "phmdoctest doc/setup_doctest.md --teardown round --report"
    simulator_status = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command, pytest_options=None
    )
    assert simulator_status.runner_status.exit_code == 1
    assert simulator_status.pytest_exit_code is None
    stdout = simulator_status.runner_status.stdout
    assert "Error: More than one block matched command line" in stdout
    assert "--teardown or -d." in stdout
    assert "Only one match is allowed." in stdout
    assert "The matching blocks are at line numbers 20, 76" in stdout


def test_teardown_is_same_as_setup_block():
    """Caller --teardown matches, but it matches setup block."""
    command = "phmdoctest doc/setup_doctest.md --setup True --teardown True --report"
    simulator_status = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command, pytest_options=None
    )
    assert simulator_status.runner_status.exit_code == 0
    assert simulator_status.pytest_exit_code is None
    stdout = simulator_status.runner_status.stdout
    assert not ("  teardown" in stdout)
    assert "No teardown block found." in stdout


def test_teardown_is_not_code_block():
    """Caller --teardown matches, but it is not a code block."""
    command = "phmdoctest doc/setup_doctest.md --teardown True --report"
    simulator_status = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command, pytest_options=None
    )
    assert simulator_status.runner_status.exit_code == 0
    assert simulator_status.pytest_exit_code is None
    stdout = simulator_status.runner_status.stdout
    assert not ("  teardown" in stdout)
    assert "No teardown block found." in stdout


def test_run_setup_example():
    """Verify the setup example passes pytest."""
    command = (
        "phmdoctest doc/setup.md --setup FIRST --teardown LAST"
        " --report --outfile discarded.py"
    )
    simulator_status = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command, pytest_options=["--doctest-modules", "-v"]
    )
    assert simulator_status.runner_status.exit_code == 0
    assert simulator_status.pytest_exit_code == 0
    stdout = simulator_status.runner_status.stdout
    assert 'python       9  setup     "FIRST"' in stdout
    assert 'python      58  teardown  "LAST"' in stdout


def test_simulator_ill_formed_command():
    """Make sure simulator dies with badly formed command."""
    command = "python -m phmdoctest tests/bogus.md --outfile discarded.py"
    with pytest.raises(ValueError) as exc_info:
        _ = phmdoctest.simulator.run_and_pytest(
            well_formed_command=command, pytest_options=None
        )
    assert "well_formed_command must start with phmdoctest" in str(exc_info.value)


def test_simulator_setup_equals_quoted():
    """run_and_pytest() parses quoted --setup= argument."""
    command = (
        'phmdoctest doc/setup.md --setup="import math" --teardown LAST'
        " --report --outfile discarded.py"
    )
    simulator_status = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command, pytest_options=["--doctest-modules", "-v"]
    )
    assert simulator_status.runner_status.exit_code == 0
    assert simulator_status.pytest_exit_code == 0
    stdout = simulator_status.runner_status.stdout
    assert 'python       9  setup     "import math"' in stdout


def test_simulator_setup_space_quoted():
    """run_and_pytest() parses quoted --setup TEXT argument."""
    command = (
        'phmdoctest doc/setup.md --setup "import math" --teardown LAST'
        " --report --outfile discarded.py"
    )
    simulator_status = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command, pytest_options=["--doctest-modules", "-v"]
    )
    assert simulator_status.runner_status.exit_code == 0
    assert simulator_status.pytest_exit_code == 0
    stdout = simulator_status.runner_status.stdout
    assert 'python       9  setup     "import math"' in stdout


def test_simulator_teardown_equals_quoted():
    """run_and_pytest() parses quoted --teardown="TEXT" argument."""
    command = (
        'phmdoctest doc/setup.md -uFIRST --teardown="not emptied"'
        " --report --outfile discarded.py"
    )
    simulator_status = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command, pytest_options=["--doctest-modules", "-v"]
    )
    assert simulator_status.runner_status.exit_code == 0
    assert simulator_status.pytest_exit_code == 0
    stdout = simulator_status.runner_status.stdout
    assert 'python      58  teardown  "not emptied"' in stdout


def test_simulator_teardown_space_quoted():
    """run_and_pytest() parses quoted --teardown "TEXT" argument."""
    command = (
        'phmdoctest doc/setup.md -uFIRST --teardown "not emptied"'
        " --report --outfile discarded.py"
    )
    simulator_status = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command, pytest_options=["--doctest-modules", "-v"]
    )
    assert simulator_status.runner_status.exit_code == 0
    assert simulator_status.pytest_exit_code == 0
    stdout = simulator_status.runner_status.stdout
    assert 'python      58  teardown  "not emptied"' in stdout


def test_teardown_without_setup():
    """Just a teardown block which doesn't access any globals"""
    command = (
        'phmdoctest doc/example2.md --teardown "import date"'
        ' --skip "Python 3.7" --report --outfile discarded.py'
    )
    simulator_status = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command, pytest_options=["--doctest-modules", "-v"]
    )
    assert simulator_status.runner_status.exit_code == 0
    assert simulator_status.pytest_exit_code == 0
    stdout = simulator_status.runner_status.stdout
    assert 'python      87  teardown     "import date"' in stdout
    assert "            94  del-output" in stdout


def test_run_setup_doctest_example():
    """Verify the --setup-doctest example passes pytest."""
    command = (
        "phmdoctest doc/setup_doctest.md --setup FIRST --teardown LAST"
        " --setup-doctest --report --outfile discarded.py"
    )
    simulator_status = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command, pytest_options=["--doctest-modules", "-v"]
    )
    assert simulator_status.runner_status.exit_code == 0
    assert simulator_status.pytest_exit_code == 0
    stdout = simulator_status.runner_status.stdout
    assert 'python       9  setup     "FIRST"' in stdout
    assert 'python      86  teardown  "LAST"' in stdout


def test_setup_no_teardown():
    """setup_only.md has setup, but no teardown directive."""
    command = "phmdoctest tests/setup_only.md --report --outfile discarded.py"
    simulator_status = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command, pytest_options=["--doctest-modules", "-v"]
    )
    assert simulator_status.runner_status.exit_code == 0
    assert simulator_status.pytest_exit_code == 0
    stdout = simulator_status.runner_status.stdout
    assert "py3         4  setup   -setup" in stdout
    assert "py3        12  code" in stdout
    assert "           19  output" in stdout


def test_no_blocks_left_to_test_passing():
    """Generate a pytest file that passes when no blocks to test."""
    command = (
        "phmdoctest doc/example1.md -sFIRST"
        " --skip SECOND --report --outfile discarded.py"
    )
    simulator_status = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command, pytest_options=["--doctest-modules", "-v"]
    )
    assert simulator_status.runner_status.exit_code == 0
    assert simulator_status.pytest_exit_code == 0
    assert "def test_nothing_passes()" in simulator_status.outfile


def test_no_blocks_left_to_test_fails():
    """Generate a pytest file that asserts when no blocks to test."""
    command = (
        "phmdoctest doc/example1.md -sFIRST --fail-nocode"
        " --skip SECOND --report --outfile discarded.py"
    )
    simulator_status = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command, pytest_options=["--doctest-modules", "-v"]
    )
    assert simulator_status.runner_status.exit_code == 0
    assert simulator_status.pytest_exit_code == 1  # pytest failed
    assert "def test_nothing_fails()" in simulator_status.outfile


def test_no_code_blocks():
    """Process .md that has no code blocks."""
    command = "phmdoctest tests/no_code_blocks.md --report --outfile discarded.py"
    simulator_status = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command, pytest_options=["--doctest-modules", "-v"]
    )
    assert simulator_status.runner_status.exit_code == 0
    assert simulator_status.pytest_exit_code == 0
    assert "def test_nothing_passes()" in simulator_status.outfile


def test_empty_code_blocks_report():
    """Report counts empty code and output blocks."""
    command = "phmdoctest tests/empty_code_block.md --report"
    simulator_status = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command, pytest_options=None
    )
    assert simulator_status.runner_status.exit_code == 0
    assert simulator_status.pytest_exit_code is None
    stdout = simulator_status.runner_status.stdout
    with open("tests/empty_code_report.txt", "r", encoding="utf-8") as f:
        want = f.read()
    verify.a_and_b_are_the_same(want, stdout)


def test_missing_markdown_file():
    """Usage error for MARKDOWN_FILE that does not exist."""
    command = "phmdoctest tests/bogus.md --outfile discarded.py"
    simulator_status = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command, pytest_options=["--doctest-modules", "-v"]
    )
    assert simulator_status.runner_status.exit_code == click.UsageError.exit_code
    assert simulator_status.outfile is None
    assert simulator_status.pytest_exit_code is None


def test_bad_usage_option():
    """Usage error for misspelled option."""
    command = "phmdoctest doc/example1.md --misspelled --outfile discarded.py"
    simulator_status = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command, pytest_options=["--doctest-modules", "-v"]
    )
    want = click.UsageError.exit_code
    got = simulator_status.runner_status.exit_code
    assert got == want
    assert simulator_status.outfile is None
    assert simulator_status.pytest_exit_code is None


def test_label_is_not_identifier():
    """Code block has a label directive that is not a Python identifier."""
    command = "phmdoctest tests/label_not_identifier.md --outfile discarded.py"
    simulator_status = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command, pytest_options=["--doctest-modules", "-v"]
    )
    assert simulator_status.runner_status.exit_code == 1
    stdout = simulator_status.runner_status.stdout
    assert "line 3 must be a valid python identifier." in stdout


def test_same_label_twice():
    """Two code block have the same label directive value."""
    command = "phmdoctest tests/label_used_twice.md --outfile discarded.py"
    simulator_status = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command, pytest_options=["--doctest-modules", "-v"]
    )
    assert simulator_status.runner_status.exit_code == 0
    assert "def k_and_v(capsys)" in simulator_status.outfile
    assert "def k_and_v_16(capsys)" in simulator_status.outfile


def test_bad_skipif_minor_number():
    """Skipif directive has non-numeric minor number."""
    command = 'phmdoctest tests/bad_skipif_number.md --skip="eric_idle" --outfile discarded.py'
    simulator_status = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command, pytest_options=None
    )
    assert simulator_status.runner_status.exit_code == 1
    stdout = simulator_status.runner_status.stdout
    assert "line 15 must be a decimal number and >= zero." in stdout

    command = (
        'phmdoctest tests/bad_skipif_number.md --skip="palin" --outfile discarded.py'
    )
    simulator_status = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command, pytest_options=None
    )
    assert simulator_status.runner_status.exit_code == 1
    stdout = simulator_status.runner_status.stdout
    assert "line 4 must be a decimal number and >= zero." in stdout


def test_extra_setup_block():
    """Setup directive on first block, --setup SECOND."""
    command = "phmdoctest doc/directive2.md --setup SECOND --outfile discarded.py"
    simulator_status = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command, pytest_options=["--doctest-modules", "-v"]
    )
    assert simulator_status.runner_status.exit_code == 1
    stdout = simulator_status.runner_status.stdout
    assert "More than one block is designated as setup" in stdout
    assert "The blocks are at line numbers 25, 14" in stdout


def test_extra_teardown_block():
    """Teardown directive on a block, --teardown="round(math.pi, 3)"."""
    command = (
        'phmdoctest doc/directive2.md --teardown="round(math.pi, 3)" '
        "--outfile discarded.py"
    )
    simulator_status = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command, pytest_options=["--doctest-modules", "-v"]
    )
    assert simulator_status.runner_status.exit_code == 1
    stdout = simulator_status.runner_status.stdout
    assert "More than one block is designated as teardown" in stdout
    assert "The blocks are at line numbers 25, 64" in stdout


def test_setup_directive_on_2_blocks():
    """Two blocks have a setup directive. Only 1 is allowed."""
    command = "phmdoctest tests/direct.md --outfile discarded.py"
    simulator_status = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command, pytest_options=["--doctest-modules", "-v"]
    )
    assert simulator_status.runner_status.exit_code == 1
    stdout = simulator_status.runner_status.stdout
    assert "More than 1 block has directive <!--phmdoctest-setup-->." in stdout
    assert "The blocks are at line numbers 77, 116." in stdout


def test_ok_same_block_setup_2_ways():
    """OK if same block designated setup by directive and command line."""
    command = "phmdoctest doc/directive2.md --setup FIRST --outfile discarded.py"
    simulator_status = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command, pytest_options=["--doctest-modules", "-v"]
    )
    assert simulator_status.runner_status.exit_code == 0


def test_ok_same_block_teardown_2_ways():
    """OK if same block designated teardown by directive and command line."""
    command = "phmdoctest doc/directive2.md --teardown LAST --outfile discarded.py"
    simulator_status = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command, pytest_options=["--doctest-modules", "-v"]
    )
    assert simulator_status.runner_status.exit_code == 0
