#### doc/test_directive3.py
```
"""pytest file built from doc/directive3.md"""
import pytest

from phmdoctest.fixture import managenamespace
from phmdoctest.functions import _phm_compare_exact


def test_code_13_output_17(capsys):
    not_shared = "Hello World!"
    print(not_shared)

    _phm_expected_str = """\
Hello World!
"""
    _phm_compare_exact(a=_phm_expected_str, b=capsys.readouterr().out)


def test_not_visible():
    try:
        print(not_shared)
    except NameError:
        pass
    else:
        assert False, "did not get expected NameError"

    # Caution- no assertions.


def test_directive_share_names(managenamespace):
    import string

    x, y, z = 77, 88, 99

    def incrementer(x):
        return x + 1

    grades = ["A", "B", "C"]

    # Caution- no assertions.
    managenamespace(operation="update", additions=locals())


def test_code_53_output_60(capsys):
    print("string.digits=", string.digits)
    print(incrementer(10))
    print(grades)
    print(x, y, z)

    _phm_expected_str = """\
string.digits= 0123456789
11
['A', 'B', 'C']
77 88 99
"""
    _phm_compare_exact(a=_phm_expected_str, b=capsys.readouterr().out)


def test_code_70():
    grades.append("D")

    # Caution- no assertions.


def test_code_75_output_79(capsys):
    print(grades == ["A", "B", "C", "D"])

    _phm_expected_str = """\
True
"""
    _phm_compare_exact(a=_phm_expected_str, b=capsys.readouterr().out)


def test_code_85_output_93(capsys, managenamespace):
    hex_digits = string.hexdigits
    print(hex_digits)

    _phm_expected_str = """\
0123456789abcdefABCDEF
"""
    _phm_compare_exact(a=_phm_expected_str, b=capsys.readouterr().out)
    managenamespace(operation="update", additions=locals())


def test_code_108_output_114(capsys, managenamespace):
    print("Names are cleared after the code runs.")
    print(grades == ["A", "B", "C", "D"])
    print(hex_digits)

    _phm_expected_str = """\
Names are cleared after the code runs.
True
0123456789abcdefABCDEF
"""
    _phm_compare_exact(a=_phm_expected_str, b=capsys.readouterr().out)
    managenamespace(operation="clear")


def test_code_121():
    try:
        print(grades)
    except NameError:
        pass
    else:
        assert False, "expected NameError for grades"
    try:
        print(hex_digits)
    except NameError:
        pass
    else:
        assert False, "expected NameError for hex_digits"

    # Caution- no assertions.
```
This page is created from a Markdown file that contains the contents
of a python source file in a syntax highlighted fenced code block.
It is included in the documentation as an example python file.

