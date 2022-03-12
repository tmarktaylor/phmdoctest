"""Test <!--phmdoctest-mark.ATTRIBUTE--> directive."""

from pathlib import Path
from _pytest.pytester import RunResult
import pytest

import click

import phmdoctest.main
from phmdoctest.tester import testfile_creator
from phmdoctest.tester import testfile_tester


# 1. To avoid PytestUnknownMarkWarning we register the markers using
#    pytester and pytester.makeini().
# 2. We also use pytester to run pytest on the generated test file
#    with the -m option.


def test_doc_mark_example_md(testfile_creator, pytester, checker):
    """Generate pytest file from mark_example.md and compare to existing file."""
    testfile = testfile_creator("doc/mark_example.md")
    expected_file = pytester.copy_example("doc/test_mark_example.py")
    expected_contents = Path(expected_file).read_text(encoding="utf-8")
    checker(expected_contents, testfile)


def nofail_noerror_nowarn(result: RunResult) -> None:
    """Check summary from pytester.runpytest RunResult for success."""
    summary_nouns = result.parse_summary_nouns(result.outlines)
    assert summary_nouns.get("failed", 0) == 0
    assert summary_nouns.get("errors", 0) == 0
    assert summary_nouns.get("warnings", 0) == 0
    assert "passed" in summary_nouns


def test_run_mark_example(pytester, testfile_creator, testfile_tester):
    """Test <!--phmdoctest-mark.ATTRIBUTE--> directive."""

    # Register the "slow" marker to avoid PytestUnknownMarkWarning.
    pytester.makeini("[pytest]\nmarkers =\n    slow: marks tests as slow")
    testfile = testfile_creator("doc/mark_example.md")
    result1 = testfile_tester(
        contents=testfile, pytest_options=["-v", "--doctest-modules"]
    )
    nofail_noerror_nowarn(result1)
    # Expecting: collected 7 items, all passed.
    summary_nouns = result1.parse_summary_nouns(result1.outlines)
    assert summary_nouns.get("passed", 0) == 3

    result2 = testfile_tester(
        contents=testfile, pytest_options=["-v", "--doctest-modules", "-m", "slow"]
    )
    nofail_noerror_nowarn(result2)
    result2.stdout.fnmatch_lines("*2 deselected*")
    summary_nouns = result2.parse_summary_nouns(result2.outlines)
    assert summary_nouns.get("passed", 0) == 1

    result3 = testfile_tester(
        contents=testfile, pytest_options=["-v", "--doctest-modules", "-m", "not slow"]
    )
    nofail_noerror_nowarn(result3)
    result3.stdout.fnmatch_lines("*1 deselected*")
    summary_nouns = result3.parse_summary_nouns(result3.outlines)
    assert summary_nouns.get("passed", 0) == 2


one_mark_md_file_image = """
# This is Markdown file one_mark.md

## mark.ATTRIBUTE directive.

<!--phmdoctest-mark.network-->
```python
print("testing @pytest.mark.network on a test case.")
```
```
testing @pytest.mark.network on a test case.
```
"""


def test_one_mark_attribute(pytester, testfile_tester):
    """Generate/run test files from a file with a single mark.ATTRIBUTE directive."""
    pytester.makeini("[pytest]\nmarkers =\n    network: marks tests that need network")
    markdown_filename = "one_mark.md"
    p = Path(markdown_filename)
    p.write_text(one_mark_md_file_image, encoding="utf-8")
    testfile = phmdoctest.main.testfile(
        markdown_file=markdown_filename,
    )
    result1 = testfile_tester(
        contents=testfile,
        pytest_options=["-v", "-m", "network"],
    )
    nofail_noerror_nowarn(result1)
    result1.assert_outcomes(passed=1)

    # Run pytest again
    result2 = testfile_tester(
        contents=testfile,
        pytest_options=["-v", "-m", "not network"],
    )
    summary_nouns = result2.parse_summary_nouns(result2.outlines)
    assert summary_nouns.get("failed", 0) == 0
    assert summary_nouns.get("errors", 0) == 0
    assert summary_nouns.get("warnings", 0) == 0
    assert summary_nouns.get("deselected", 0) == 1


bad_mark_md_file_image = """
# This is Markdown file bad_mark.md

## mark.ATTRIBUTE directive.  Where ATTRIBUTE is not a valid Python identifier.

<!--phmdoctest-mark.1-network-->
```python
print("testing @pytest.mark.1-network on a test case.")
```
```
testing @pytest.mark.network on a test case.
```
"""


def test_mark_attribute_not_identifier(pytester):
    """Generate/run test files from a file with a single mark.ATTRIBUTE directive."""
    pytester.makeini("[pytest]\nmarkers =\n    network: marks tests that need network")
    markdown_filename = "bad_mark.md"
    p = Path(markdown_filename)
    p.write_text(bad_mark_md_file_image, encoding="utf-8")
    with pytest.raises(click.exceptions.ClickException) as exc_info:
        _ = phmdoctest.main.testfile(markdown_file=markdown_filename)
    assert "<!--phmdoctest-mark.1-network-->\nat markdown file line 6" in str(
        exc_info.value
    )
