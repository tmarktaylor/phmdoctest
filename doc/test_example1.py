"""pytest file built from doc/example1.md"""
from phmdoctest.functions import _phm_compare_exact


def session_00001_line_6():
    r"""
    >>> print("Hello World!")
    Hello World!
    """


def test_code_14_output_28(capsys):
    from enum import Enum

    class Floats(Enum):
        APPLES = 1
        CIDER = 2
        CHERRIES = 3
        ADUCK = 4

    for floater in Floats:
        print(floater)

    _phm_expected_str = """\
Floats.APPLES
Floats.CIDER
Floats.CHERRIES
Floats.ADUCK
"""
    _phm_compare_exact(a=_phm_expected_str, b=capsys.readouterr().out)
