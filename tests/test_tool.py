"""Tests to complete code coverage of tool.py"""
import pytest

import phmdoctest.tool


JUNIT_FAMILY = "xunit2"  # Pytest output format for JUnit XML file.


@pytest.mark.parametrize(
    "markdown_filename,num_label_directives",
    [
        ("doc/directive1.md", 3),
        ("doc/directive3.md", 2),
        ("tests/direct.md", 3),  # see note below
    ],
)
def test_directive_chooser(markdown_filename, num_label_directives):
    """FCBChooser fetches from files with a mix of directives."""
    # Note: tests/direct.md has four directives on the final fenced
    # code block at line 38.  Only the top most one is counted.  The
    # other label directives are silently ignored.
    labeled_blocks = phmdoctest.tool.labeled_fenced_code_blocks(markdown_filename)
    assert len(labeled_blocks) == num_label_directives
    chooser = phmdoctest.tool.FCBChooser(markdown_filename)
    for block in labeled_blocks:
        assert len(chooser.contents(block.label))


def test_chooser_did_not_find():
    """FCBChooser.contents() with label with no <--phmdoctest-label-->."""
    labeled = phmdoctest.tool.FCBChooser("README.md")
    contents = labeled.contents("never-will-be-found")
    assert contents == ""


def test_no_fails_junit_xml(example_tester):
    """Generate JUnit XML from pytest with no failures."""
    simulator_status = example_tester(
        "phmdoctest project.md --outfile discarded.py",
        want_file_name=None,
        pytest_options=["--doctest-modules", "-v"],
        junit_family=JUNIT_FAMILY,
    )
    assert simulator_status.runner_status.exit_code == 0
    assert simulator_status.pytest_exit_code == 0
    # Look at the returned JUnit XML to see that the test failed at the
    # point and for the reason we expected.
    # Note that the parsed XML values are all strings.
    suite, fails = phmdoctest.tool.extract_testsuite(simulator_status.junit_xml)
    assert suite.attrib["tests"] == "4"  # run with --report
    assert suite.attrib["errors"] == "0"
    assert suite.attrib["failures"] == "0"
    assert len(fails) == 0


def test_pytest_really_fails(example_tester):
    """Make sure pytest fails due to incorrect expected output in the .md.

    Generate a pytest that will assert.
    """
    simulator_status = example_tester(
        "phmdoctest tests/unexpected_output.md --outfile discarded.py",
        want_file_name=None,
        pytest_options=["--doctest-modules", "-v"],
        junit_family=JUNIT_FAMILY,
    )
    assert simulator_status.pytest_exit_code == 1
    # Look at the returned JUnit XML to see that the test failed at the
    # point and for the reason we expected.
    # Note that the parsed XML values are all strings.
    suite, fails = phmdoctest.tool.extract_testsuite(simulator_status.junit_xml)
    assert suite.attrib["tests"] == "1"
    assert suite.attrib["errors"] == "0"
    assert suite.attrib["failures"] == "1"
    assert fails[0].attrib["name"] == "test_code_4_output_17"
