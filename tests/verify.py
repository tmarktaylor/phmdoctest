"""Logic used by pytest test cases."""

import difflib
from itertools import zip_longest
from xml.etree import ElementTree

import phmdoctest.simulator

JUNIT_FAMILY = 'xunit2'    # Pytest output format for JUnit XML file


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


def one_example(
        well_formed_command,
        want_file_name=None,
        pytest_options=None,
        junit_family=''):
    """Simulate running a phmdoctest command and pytest on the result."""
    simulator_status = phmdoctest.simulator.run_and_pytest(
        well_formed_command,
        pytest_options=pytest_options,
        junit_family=junit_family)
    # check that the phmdoctest command succeeded
    exit_code = simulator_status.runner_status.exit_code
    assert exit_code == 0, exit_code

    # check the OUTFILE against the expected value
    if want_file_name is not None:
        with open(want_file_name) as f:
            want = f.read()
            a_and_b_are_the_same(want, simulator_status.outfile)
    return simulator_status


def extract_testsuite(junit_xml_string):
    """Return testsuite tree and list of failing trees from JUnit XML."""
    root = ElementTree.fromstring(junit_xml_string)
    suite = root.find('testsuite')
    failed_test_cases = []
    for case in suite:
        if case.find('failure') is not None:
            failed_test_cases.append(case)
    return suite, failed_test_cases


