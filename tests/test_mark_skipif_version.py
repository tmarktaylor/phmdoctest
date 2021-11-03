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


pytest_file_image = '''"""pytest file built from doc/directive1.md"""
import sys

import pytest

from phmdoctest.functions import _phm_compare_exact


def test_code_23():
    from datetime import date

    date.today()

    # Caution- no assertions.


@pytest.mark.skip()
def test_mark_skip(capsys):
    print("testing @pytest.mark.skip().")

    _phm_expected_str = """\
incorrect expected output
"""
    _phm_compare_exact(a=_phm_expected_str, b=capsys.readouterr().out)


@pytest.mark.skipif(sys.version_info < (3, 8), reason="requires >=py3.8")
def test_i_ratio(capsys):
    b = 10
    print(b.as_integer_ratio())

    _phm_expected_str = """\
(10, 1)
"""
    _phm_compare_exact(a=_phm_expected_str, b=capsys.readouterr().out)


def doctest_print_coffee():
    r"""
    >>> print("coffee")
    coffee
    """
'''

minor = sys.version_info[1] + 1
pytest_file_image1 = pytest_file_image.replace("(3, 8)", "(3, " + str(minor) + ")")
pytest_file_image2 = pytest_file_image1.replace("py3,8", "(py3." + str(minor))


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
