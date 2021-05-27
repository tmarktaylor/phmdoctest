"""Tests to complete code coverage of tool.py"""
import pytest

import phmdoctest.tool
import verify


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


def test_no_fails_junit_xml():
    """Generate JUnit XML from pytest with no failures."""
    simulator_status = verify.one_example(
        "phmdoctest project.md --outfile discarded.py",
        want_file_name=None,
        pytest_options=["--doctest-modules", "-v"],
        junit_family=verify.JUNIT_FAMILY,
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
