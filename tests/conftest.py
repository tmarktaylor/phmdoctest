"""Fixtures used in multiple test files."""
import difflib
from itertools import zip_longest
from pathlib import Path

import pytest


import phmdoctest.simulator


pytest_plugins = ["pytester"]


@pytest.fixture()
def checker():
    """Return Callable(str, str) that runs difflib.ndiff. Multi-line str's ok."""

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


@pytest.fixture()
def example_tester(checker):
    """Return Callable that runs a phmdoctest command and checks the --outfile."""

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
            want = Path(want_file_name).read_text(encoding="utf-8")
            checker(want, simulator_status.outfile)
        return simulator_status

    return one_example
