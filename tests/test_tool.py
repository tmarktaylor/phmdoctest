"""Tests to complete code coverage of tool.py"""
from pathlib import Path

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


def test_detect_python_examples():
    """Show Python examples in Markdown are detected."""
    result1 = phmdoctest.tool.detect_python_examples(
        Path("tests/no_fenced_code_blocks.md")
    )
    assert not result1.has_code
    assert not result1.has_session

    result2 = phmdoctest.tool.detect_python_examples(Path("tests/one_code_block.md"))
    assert result2.has_code
    assert not result2.has_session

    result3 = phmdoctest.tool.detect_python_examples(
        Path("tests/twentysix_session_blocks.md")
    )
    assert not result3.has_code
    assert result3.has_session

    # This file has fenced code blocks at the top level but no info strings.
    result4 = phmdoctest.tool.detect_python_examples(Path("doc/mark_example_raw.md"))
    assert not result4.has_code
    assert not result4.has_session


def test_wipe_testfile_directory(tmp_path):
    """Show that pre-existing *.py are renamed, not deleted."""
    source1 = "test_file1.py"  # Use the filename as the contents of the file.
    source1a = "different test_file1.py"
    source2 = "myfile.py"
    source3 = "something.txt"
    # Create pre-existing pytest file.
    d = tmp_path / ".gendir"
    d.mkdir()
    file1 = d / "test_example1.py"
    file2 = d / "myfile.py"
    file3 = d / "something.txt"
    _ = file1.write_text(source1, encoding="utf-8")
    _ = file2.write_text(source2, encoding="utf-8")
    _ = file3.write_text(source3, encoding="utf-8")
    assert file1.exists()
    assert file2.exists()
    assert file3.exists()
    assert len(list(d.glob("**/*.*"))) == 3, "3 files exist"

    phmdoctest.tool.wipe_testfile_directory(d)
    assert len(list(d.glob("**/*.py"))) == 0, "no .py files"
    assert not file1.exists(), "file1 is gone (it was renamed)."
    assert not file2.exists(), "file2 is gone (it was renamed)."
    preserved1 = d / "notest_example1.sav"
    preserved2 = d / "nomyfile.sav"
    assert preserved1.exists(), "newly renamed file"
    assert preserved2.exists(), "newly renamed file"
    assert len(list(d.glob("**/*.*"))) == 3, "3 files exist"

    # Renamed files still have the original contents.
    # file3 was not modified.
    assert source1 == preserved1.read_text(encoding="utf-8")
    assert source2 == preserved2.read_text(encoding="utf-8")
    assert source3 == file3.read_text(encoding="utf-8")

    # Show that the renamed files still have the original contents
    # even after a second wipe.
    phmdoctest.tool.wipe_testfile_directory(d)
    assert len(list(d.glob("**/*.py"))) == 0, "no .py files"
    assert len(list(d.glob("**/*.*"))) == 3, "3 files exist"
    assert source1 == preserved1.read_text(encoding="utf-8")
    assert source2 == preserved2.read_text(encoding="utf-8")
    assert source3 == file3.read_text(encoding="utf-8")

    # Simulate generating a new test file by writing a new file1 with
    # different contents.
    _ = file1.write_text(source1a, encoding="utf-8")  # modify
    assert file1.exists()
    assert source1a == file1.read_text(encoding="utf-8")
    assert len(list(d.glob("**/*.*"))) == 4, "4 files exist"

    # Show the originally preserved files still exist.
    # The second wipe only removed the new file1 that had source1a contents.
    phmdoctest.tool.wipe_testfile_directory(d)
    assert len(list(d.glob("**/*.py"))) == 0, "no .py files"
    assert len(list(d.glob("**/*.*"))) == 3, "3 files exist"
    assert source1 == preserved1.read_text(encoding="utf-8")
    assert source2 == preserved2.read_text(encoding="utf-8")
    assert source3 == file3.read_text(encoding="utf-8")
