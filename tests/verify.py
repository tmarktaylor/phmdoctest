"""Logic used by pytest test cases."""

from itertools import zip_longest

import phmdoctest.simulator


def a_and_b_are_the_same(a, b):
    """Line by line helper compare function with assertion for pytest."""
    a_lines = a.splitlines()
    b_lines = b.splitlines()
    for a_line, b_line in zip_longest(a_lines, b_lines):
        assert a_line == b_line, str(a_line) + '|' + str(b_line)


def one_example(
        well_formed_command,
        want_file_name=None,
        pytest_options=None):
    """Simulate running a phmdoctest command and pytest on the result."""
    simulator_status = phmdoctest.simulator.run_and_pytest(
        well_formed_command, pytest_options=pytest_options)
    # check that the phmdoctest command succeeded
    exit_code = simulator_status.runner_status.exit_code
    assert exit_code == 0, exit_code

    # check the OUTFILE against the expected value
    if want_file_name is not None:
        with open(want_file_name) as f:
            want = f.read()
            a_and_b_are_the_same(simulator_status.outfile, want)
    return simulator_status
