"""Test cases for code templates in functions.py."""
import inspect

import pytest

import phmdoctest.functions


def test_phm_compare_exact():
    """Exercise the expected output checker for code blocks."""
    # No assertion since a, b are the same.
    phmdoctest.functions._phm_compare_exact(
        a='123\n456\n7890',
        b='123\n456\n7890'
    )

    with pytest.raises(AssertionError):
        phmdoctest.functions._phm_compare_exact(
            a='',
            b='123\n456\n7890x'
        )

    with pytest.raises(AssertionError):
        phmdoctest.functions._phm_compare_exact(
            a='123\n456\n7890',
            b=''
        )

    with pytest.raises(AssertionError):
        phmdoctest.functions._phm_compare_exact(
            a='123\n456\n7890',
            b='123\n456\n7890x'
        )

    with pytest.raises(AssertionError):
        phmdoctest.functions._phm_compare_exact(
            a='123\n456\n7890',
            b='123\n456\n7890x'
        )


def test_phm_compare_exact_prints(capsys):
    """Exercise the expected output checker for code blocks."""
    with pytest.raises(AssertionError):
        phmdoctest.functions._phm_compare_exact(
            a='123zzz\n456aaa\n7890ccc',
            b='123zzz\n4x6aaa\n7890ccc'
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


def test_def_test_code_and_output():
    """Painful way to eliminate 2 coverage missed statements."""
    # The function coder.test_code_and_output() is used as
    # a template to generate Python code.
    # It accepts the pytest fixture called capsys when the
    # generated pytest is run.
    # phmodctest doesn't call this function so it shows up
    # in the coverage report as a missed statement.
    # Here a test mock up of the fixture is created that
    # provides the expected value as its out attribute.
    class MockReadouterr:
        def __init__(self):
            self.out = '<<<replaced>>>'

    class MockCapsys:
        @staticmethod
        def readouterr():
            return MockReadouterr()

    phmdoctest.functions.test_code_and_output(MockCapsys())


def test_def_code_only():
    """The only purpose is to get code coverage."""
    phmdoctest.functions.test_code_only()


def test_def_test_nothing_fails():
    """This is done for code coverage of the function."""
    with pytest.raises(AssertionError):
        phmdoctest.functions.test_nothing_fails()


def test_def_test_nothing_passes():
    """This is done for code coverage of the function."""
    phmdoctest.functions.test_nothing_passes()
