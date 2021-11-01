"""Exercise the testfile_creator and testfile_tester fixtures.

The test cases here partially duplicate test cases that call
simulator.run_and_pytest() in other test files.
The purpose here is to build and run a pytest file using
the fixtures in tester.py. The testfile_tester fixture
uses the pytester fixture to run the pytest file.
"""
import sys
from pathlib import Path

import click
from phmdoctest.tester import testfile_creator
from phmdoctest.tester import testfile_tester
import phmdoctest.tool
from _pytest.pytester import RunResult
import pytest


def nofail_noerror_nowarn(result: RunResult) -> None:
    """Check summary from pytester.runpytest RunResult for success."""
    summary_nouns = result.parse_summary_nouns(result.outlines)
    assert summary_nouns.get("failed", 0) == 0
    assert summary_nouns.get("errors", 0) == 0
    assert summary_nouns.get("warnings", 0) == 0
    assert "passed" in summary_nouns


def onefailed(result):
    """Check pytester RunResult for 1 test failure, No errors, no warnings."""
    summary_nouns = result.parse_summary_nouns(result.outlines)
    assert summary_nouns.get("failed", 0) == 1
    assert summary_nouns.get("errors", 0) == 0
    assert summary_nouns.get("warnings", 0) == 0


def test_project_md(testfile_creator, testfile_tester):
    """Generate pytest file from project.md and run it with pytester."""
    testfile = testfile_creator("project.md")
    result = testfile_tester(
        contents=testfile, pytest_options=["-v", "--doctest-modules"]
    )
    nofail_noerror_nowarn(result)


def test_project_md_no_options(testfile_creator, testfile_tester):
    """Run testfile with no pytest_options."""
    testfile = testfile_creator("project.md")
    result = testfile_tester(contents=testfile)
    nofail_noerror_nowarn(result)


@pytest.fixture()
def testfile_checker(pytester, checker):
    """Return callable that compares pre existing file to testfile.

    This fixture is designed to run in a test case that injects the
    pytester fixture. Pytester sets the current working directory
    to a temporary directory while it is active. pytester.copy_example()
    provides relative access to the project's directory.
    """

    def check_it(existing_filename, testfile):
        """Compare pre existing file to testfile."""
        expected_file = pytester.copy_example(existing_filename)
        expected_contents = Path(expected_file).read_text(encoding="utf-8")
        checker(expected_contents, testfile)

    return check_it


def test_doc_example1_md(testfile_creator, testfile_tester, testfile_checker):
    """Generate pytest file from example1.md and run it with pytester."""
    testfile = testfile_creator("doc/example1.md")
    result = testfile_tester(
        contents=testfile, pytest_options=["-v", "--doctest-modules"]
    )
    nofail_noerror_nowarn(result)
    testfile_checker("doc/test_example1.py", testfile)


def test_doc_example2_md(testfile_creator, testfile_tester, testfile_checker):
    """Generate pytest file from example2.md and run it in pytester."""
    testfile = testfile_creator("doc/example2.md", skips=["Python 3.7", "LAST"])
    result = testfile_tester(
        contents=testfile, pytest_options=["-v", "--doctest-modules"]
    )
    nofail_noerror_nowarn(result)
    testfile_checker("doc/test_example2.py", testfile)


def test_doc_directive1_md(testfile_creator, testfile_tester, testfile_checker):
    """Generate pytest file from directive1.md and run it in pytester."""
    testfile = testfile_creator("doc/directive1.md")
    result = testfile_tester(
        contents=testfile,
        testfile_name="test_my_directive1_md.py",
        pytest_options=["-v", "--doctest-modules"],
    )
    nofail_noerror_nowarn(result)
    summary_nouns = result.parse_summary_nouns(result.outlines)
    if sys.version_info >= (3, 8):
        assert summary_nouns.get("passed", 0) == 3
        assert summary_nouns.get("skipped", 0) == 1
    else:
        assert summary_nouns.get("passed", 0) == 2
        assert summary_nouns.get("skipped", 0) == 2
    testfile_checker("doc/test_directive1.py", testfile)


def test_doc_directive2_md(testfile_creator, testfile_tester, testfile_checker):
    """Generate pytest file from directive2.md and run it in pytester."""
    testfile = testfile_creator("doc/directive2.md")
    result = testfile_tester(
        contents=testfile, pytest_options=["-v", "--doctest-modules"]
    )
    nofail_noerror_nowarn(result)
    testfile_checker("doc/test_directive2.py", testfile)


def test_doc_directive3_md(testfile_creator, testfile_tester, testfile_checker):
    """Generate pytest file from directive3.md and run it in pytester."""
    testfile = testfile_creator("doc/directive3.md")
    result = testfile_tester(
        contents=testfile, pytest_options=["-v", "--doctest-modules"]
    )
    nofail_noerror_nowarn(result)
    testfile_checker("doc/test_directive3.py", testfile)


def test_doc_inline_example_md(testfile_creator, testfile_tester, testfile_checker):
    """Generate pytest file from inline_example.md and run it in pytester."""
    testfile = testfile_creator("doc/inline_example.md")
    result = testfile_tester(
        contents=testfile, pytest_options=["-v", "--doctest-modules"]
    )
    nofail_noerror_nowarn(result)
    testfile_checker("doc/test_inline_example.py", testfile)


def test_doc_setup_md(testfile_creator, testfile_tester, testfile_checker):
    """Generate pytest file from setup.md and run it in pytester."""
    testfile = testfile_creator("doc/setup.md", setup="FIRST", teardown="LAST")
    result = testfile_tester(
        contents=testfile, pytest_options=["-v", "--doctest-modules"]
    )
    nofail_noerror_nowarn(result)
    testfile_checker("doc/test_setup.py", testfile)


def test_doc_setup_doctest_md(testfile_creator, testfile_tester, testfile_checker):
    """Generate pytest file from setup_doctest.md and run it in pytester."""
    testfile = testfile_creator(
        "doc/setup_doctest.md",
        setup="FIRST",
        teardown="LAST",
        setup_doctest=True,
    )
    result = testfile_tester(
        contents=testfile, pytest_options=["-v", "--doctest-modules"]
    )
    nofail_noerror_nowarn(result)
    testfile_checker("doc/test_setup_doctest.py", testfile)


def test_tests_bad_session_output_md(testfile_creator, testfile_tester):
    """Generate pytest file from bad_session_output.md and run it in pytester.

    A Python interactive session example that has wrong output.
    """
    testfile = testfile_creator("tests/bad_session_output.md")
    result = testfile_tester(
        contents=testfile, pytest_options=["-v", "--doctest-modules"]
    )
    onefailed(result)


def test_tests_bad_skipif_number_md(testfile_creator):
    """Try to generate pytest file from bad_skipif_number.md.

    Illegal skipif directive minor number.
    """
    with pytest.raises(click.exceptions.ClickException):
        _ = testfile_creator("tests/bad_skipif_number.md")


def test_tests_does_not_print_md(testfile_creator, testfile_tester):
    """Generate pytest file from does_not_print.md and run it in pytester.

    Example code didn't call print().
    """
    testfile = testfile_creator("tests/does_not_print.md")
    result = testfile_tester(
        contents=testfile, pytest_options=["-v", "--doctest-modules"]
    )
    onefailed(result)


def test_tests_managenamespace_md(testfile_creator, testfile_tester):
    """Generate pytest file from managenamespace.md and run it in pytester."""
    # Note- testfile_name= is set to avoid collection error with
    # test_managenamespace.py.
    testfile = testfile_creator("tests/managenamespace.md")
    result = testfile_tester(
        contents=testfile,
        testfile_name="test_my_managenamespace_md.py",
        pytest_options=["-v", "--doctest-modules"],
    )
    if sys.version_info >= (3, 8):
        nofail_noerror_nowarn(result)
    else:
        summary_nouns = result.parse_summary_nouns(result.outlines)
        assert summary_nouns.get("skipped", 0) == 1


def test_tests_no_code_blocks_md(testfile_creator, testfile_tester):
    """Generate pytest file from no_code_blocks.md and run it in pytester."""
    testfile = testfile_creator("tests/no_code_blocks.md")
    result = testfile_tester(
        contents=testfile, pytest_options=["-v", "--doctest-modules"]
    )
    nofail_noerror_nowarn(result)


def test_tests_no_fenced_code_blocks_md(testfile_creator, testfile_tester):
    """Generate pytest file from no_fenced_code_blocks.md and run it in pytester."""
    testfile = testfile_creator("tests/no_fenced_code_blocks.md")
    result = testfile_tester(
        contents=testfile, pytest_options=["-v", "--doctest-modules"]
    )
    nofail_noerror_nowarn(result)


def test_tests_one_code_block_md(testfile_creator, testfile_tester):
    """Generate pytest file from one_code_block.md and run it in pytester."""
    testfile = testfile_creator("tests/one_code_block.md")
    result = testfile_tester(
        contents=testfile, pytest_options=["-v", "--doctest-modules"]
    )
    nofail_noerror_nowarn(result)


def test_tests_one_mark_skip_md(testfile_creator, testfile_tester):
    """Generate pytest file from one_mark_skip.md and run it in pytester."""
    testfile = testfile_creator("tests/one_mark_skip.md")
    result = testfile_tester(
        contents=testfile, pytest_options=["-v", "--doctest-modules"]
    )
    summary_nouns = result.parse_summary_nouns(result.outlines)
    assert summary_nouns.get("failed", 0) == 0
    assert summary_nouns.get("errors", 0) == 0
    assert summary_nouns.get("warnings", 0) == 0
    assert summary_nouns.get("skipped", 0) == 1


def test_tests_setup_only_md(testfile_creator, testfile_tester):
    """Generate pytest file from setup_only.md and run it in pytester."""
    testfile = testfile_creator("tests/setup_only.md")
    result = testfile_tester(
        contents=testfile, pytest_options=["-v", "--doctest-modules"]
    )
    nofail_noerror_nowarn(result)


def test_tests_setup_with_inline_md(testfile_creator, testfile_tester):
    """Generate pytest file from setup_with_inline.md and run it in pytester."""
    # Note- testfile_name= is set to avoid collection error with
    # test_setup_with_inline.py.
    testfile = testfile_creator(
        "tests/setup_with_inline.md",
        setup="FIRST",
        teardown="LAST",
    )
    result = testfile_tester(
        contents=testfile,
        testfile_name="test_my_setup_with_inline_md.py",
        pytest_options=["-v", "--doctest-modules"],
    )
    nofail_noerror_nowarn(result)


def test_tests_unexpected_output_md(testfile_creator, testfile_tester):
    """Generate pytest file from unexpected_output.md and run it in pytester."""
    testfile = testfile_creator("tests/unexpected_output.md")
    result = testfile_tester(
        contents=testfile, pytest_options=["-v", "--doctest-modules"]
    )
    onefailed(result)


def test_no_blocks_left_to_test_fails(testfile_creator, testfile_tester):
    """Generate a pytest file that asserts when no blocks to test."""

    # This test case provides coverage for use of skips= and fail_nocode=.
    testfile = testfile_creator(
        "tests/unexpected_output.md",
        skips=["FIRST", "SECOND"],
        fail_nocode=True,
    )
    result = testfile_tester(
        contents=testfile,
        pytest_options=["-v", "--doctest-modules"],
    )
    onefailed(result)


def test_junit_xml(testfile_creator, testfile_tester):
    """Use testfile_tester to create a junit xml file with a failing test case."""
    testfile = testfile_creator("tests/unexpected_output.md")
    result = testfile_tester(
        contents=testfile,
        pytest_options=[
            "-v",
            "--doctest-modules",
            "--junit-xml=junit.xml",
            "-o junit_family=xunit2",
        ],
    )
    onefailed(result)
    # The junit.xml file is created in pytester's temporary directory.
    junit_xml_contents = Path("junit.xml").read_text(encoding="utf-8")
    suite, fails = phmdoctest.tool.extract_testsuite(junit_xml_contents)
    assert suite.attrib["tests"] == "1"
    assert suite.attrib["errors"] == "0"
    assert suite.attrib["failures"] == "1"
    assert fails[0].attrib["name"] == "test_code_4_output_17"
