"""Fixtures used in multiple test files."""
import difflib
import logging
from itertools import zip_longest


import pytest


import phmdoctest.simulator


@pytest.fixture(scope="session")
def checker():
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

    return a_and_b_are_the_same


@pytest.fixture(scope="session")
def example_tester(checker):
    def one_example(
        well_formed_command, want_file_name=None, pytest_options=None, junit_family=""
    ):
        """Simulate running a phmdoctest command and pytest on the result."""
        simulator_status = phmdoctest.simulator.run_and_pytest(
            well_formed_command,
            pytest_options=pytest_options,
            junit_family=junit_family,
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
                checker(want, simulator_status.outfile)
        return simulator_status

    return one_example
