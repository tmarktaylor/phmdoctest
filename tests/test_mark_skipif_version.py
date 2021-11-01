"""Try pytester @pytest.mark.skip() and @pytest.mark.skipif.

Patch @pytest.mark.skipif(sys.version_info in the testfile image below.
Set the minor number in the mark.skipif statement to 1
higher than the currently running Python version.
"""

import sys

from _pytest.pytester import RunResult
import pytest

from phmdoctest.tester import testfile_tester


def nofail_noerror_nowarn(result: RunResult) -> None:
    """Check summary from pytester.runpytest RunResult for success."""
    summary_nouns = result.parse_summary_nouns(result.outlines)
    assert summary_nouns.get("failed", 0) == 0
    assert summary_nouns.get("errors", 0) == 0
    assert summary_nouns.get("warnings", 0) == 0
    assert "passed" in summary_nouns


pytest_file_image = '''"""module docstring"""
import sys

import pytest


def test_code_23():
    from datetime import date

    date.today()

    # Caution- no assertions.


@pytest.mark.skip()
def test_mark_skip(capsys):
    assert False, "expected to skip the test" 

@pytest.mark.skipif(sys.version_info < (major, minor), reason="requires >=pymajor.minor")
def test_mark_skipif(capsys):
    assert False, "expected to skip the test" 


def doctest_print_coffee():
    r"""
    >>> print("coffee")
    coffee
    """
'''

assert pytest_file_image.count("major") == 2
assert pytest_file_image.count("minor") == 2
major = sys.version_info[0]
minor = sys.version_info[1] + 1
pytest_file_image1 = pytest_file_image.replace("major", str(major))
pytest_file_image2 = pytest_file_image1.replace("minor", str(minor))
assert pytest_file_image2.count("major") == 0
assert pytest_file_image2.count("minor") == 0


def test_pytest_skips(testfile_tester):
    """Generate pytest file from managenamespace.md and run it in pytester."""
    # Note- testfile_name= is set to avoid collection error with
    # test_managenamespace.py.
    python_version = sys.version_info

    result = testfile_tester(
        contents=pytest_file_image2,
        pytest_options=["-v", "--doctest-modules"],
    )
    nofail_noerror_nowarn(result)
    result.assert_outcomes(passed=2, skipped=2)
    # uncomment to manually see the version
    # print(pytest_file_image2)
    # assert False
