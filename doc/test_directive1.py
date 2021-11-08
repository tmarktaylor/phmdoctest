"""pytest file built from doc/directive1.md"""
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
