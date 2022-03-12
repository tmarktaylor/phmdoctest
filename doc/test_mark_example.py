"""pytest file built from doc/mark_example.md"""
import pytest

from phmdoctest.functions import _phm_compare_exact


def test_code_6_output_11(capsys):
    squares = [1, 4, 9, 16, 25]
    print(squares)

    _phm_expected_str = """\
[1, 4, 9, 16, 25]
"""
    _phm_compare_exact(a=_phm_expected_str, b=capsys.readouterr().out)


@pytest.mark.slow
def test_datetime(capsys):
    from datetime import date

    d = date.fromordinal(730920)  # 730920th day after 1. 1. 0001
    print(d)

    _phm_expected_str = """\
2002-03-11
"""
    _phm_compare_exact(a=_phm_expected_str, b=capsys.readouterr().out)


def session_00001_line_44():
    r"""
    >>> from fractions import Fraction
    >>> Fraction(16, -10)
    Fraction(-8, 5)
    >>> Fraction(123)
    Fraction(123, 1)
    >>> Fraction()
    Fraction(0, 1)
    >>> Fraction('3/7')
    Fraction(3, 7)
    """
