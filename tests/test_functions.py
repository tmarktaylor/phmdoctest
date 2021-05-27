"""Test cases for code templates in functions.py."""
import pytest

from phmdoctest.fixture import managenamespace
import phmdoctest.functions


def test_phm_compare_exact():
    """Exercise the expected output checker for code blocks."""
    # No assertion since a, b are the same.
    phmdoctest.functions._phm_compare_exact(a="123\n456\n7890", b="123\n456\n7890")

    with pytest.raises(AssertionError):
        phmdoctest.functions._phm_compare_exact(a="", b="123\n456\n7890x")

    with pytest.raises(AssertionError):
        phmdoctest.functions._phm_compare_exact(a="123\n456\n7890", b="")

    with pytest.raises(AssertionError):
        phmdoctest.functions._phm_compare_exact(a="123\n456\n7890", b="123\n456\n7890x")

    with pytest.raises(AssertionError):
        phmdoctest.functions._phm_compare_exact(a="123\n456\n7890", b="123\n456\n7890x")


def test_phm_compare_exact_prints(capsys):
    """Exercise the expected output checker for code blocks."""
    with pytest.raises(AssertionError):
        phmdoctest.functions._phm_compare_exact(
            a="123zzz\n456aaa\n7890ccc", b="123zzz\n4x6aaa\n7890ccc"
        )
    expected = """\
  123zzz
- 456aaa
?  ^

+ 4x6aaa
?  ^

  7890ccc
"""
    got = capsys.readouterr().out
    assert expected == got


# The fixtures and functions in functions.py are not invoked
# by phmdoctest.  The source code is read by Python standard
# library inspect module, modified, and then written to the
# phmdoctest --outfile.
#
# The test cases here that start with test_def get code
# coverage of functions.py.


class MockReadouterr:
    """Simulate pytest capsys fixture function member readouterr."""

    def __init__(self):
        self.out = "<<<replaced>>>"


class MockCapsys:
    """Simulate pytest capsys fixture."""

    @staticmethod
    def readouterr():
        return MockReadouterr()


def test_def_test_code_and_output():
    """Painful way to eliminate 2 coverage missed statements."""
    phmdoctest.functions.test_code_and_output(MockCapsys())


def test_def_code_only():
    """The only purpose is to get code coverage."""
    phmdoctest.functions.test_code_only()


def test_def_test_managed_code_and_output(managenamespace):
    """The only purpose is to get code coverage."""
    phmdoctest.functions.test_managed_code_and_output(MockCapsys(), managenamespace)


def test_def_test_managed_code_only(managenamespace):
    """The only purpose is to get code coverage."""
    phmdoctest.functions.test_managed_code_only(managenamespace)


def test_def_test_nothing_fails():
    """This is done for code coverage of the function."""
    with pytest.raises(AssertionError):
        phmdoctest.functions.test_nothing_fails()


def test_def_test_nothing_passes():
    """This is done for code coverage of the function."""
    phmdoctest.functions.test_nothing_passes()
