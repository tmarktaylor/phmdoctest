"""Logic used by pytest test cases."""

import difflib
import inspect
from itertools import zip_longest
import textwrap

import phmdoctest.simulator

JUNIT_FAMILY = "xunit2"  # Pytest output format for JUnit XML file


def a_and_b_are_the_same(a, b):
    """Compare function with assert and line by line ndiff stdout."""
    a_lines = a.splitlines()
    b_lines = b.splitlines()
    for a_line, b_line in zip_longest(a_lines, b_lines):
        if a_line != b_line:
            diffs = difflib.ndiff(a_lines, b_lines)
            for line in diffs:
                print(line)
            assert False


def example_code_checker(callable_function, example_string):
    """Check that the body of the function matches the string."""
    want1 = inspect.getsource(callable_function)
    got = textwrap.indent(example_string, "    ")
    # Drop the def function_name line.
    newline_index = want1.find("\n")
    assert newline_index > -1, "must have a newline"
    assert len(want1) > newline_index + 2, "must have more after newline"
    want2 = want1[newline_index + 1 :]
    a_and_b_are_the_same(want2, got)


def one_example(
    well_formed_command, want_file_name=None, pytest_options=None, junit_family=""
):
    """Simulate running a phmdoctest command and pytest on the result."""
    simulator_status = phmdoctest.simulator.run_and_pytest(
        well_formed_command, pytest_options=pytest_options, junit_family=junit_family
    )
    # check that the phmdoctest command succeeded
    exit_code = simulator_status.runner_status.exit_code
    assert exit_code == 0, exit_code
    if pytest_options is None:
        assert simulator_status.pytest_exit_code is None

    # check the OUTFILE against the expected value
    if want_file_name is not None:
        with open(want_file_name) as f:
            want = f.read()
            a_and_b_are_the_same(want, simulator_status.outfile)
    return simulator_status
