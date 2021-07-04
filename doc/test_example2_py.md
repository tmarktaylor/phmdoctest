#### doc/test_example2.py
```python
"""pytest file built from doc/example2.md"""
from phmdoctest.functions import _phm_compare_exact


def test_code_9_output_14(capsys):
    squares = [1, 4, 9, 16, 25]
    print(squares)

    _phm_expected_str = """\
[1, 4, 9, 16, 25]
"""
    _phm_compare_exact(a=_phm_expected_str, b=capsys.readouterr().out)


def test_code_37():
    a, b = 0, 1
    while a < 1000:
        print(a, end=",")
        a, b = b, a + b

    # Caution- no assertions.


def test_code_44_output_51(capsys):
    words = ["cat", "window", "defenestrate"]
    for w in words:
        print(w, len(w))

    _phm_expected_str = """\
cat 3
window 6
defenestrate 12
"""
    _phm_compare_exact(a=_phm_expected_str, b=capsys.readouterr().out)


def session_00001_line_75():
    r"""
    >>> a = "Greetings Planet!"
    >>> a
    'Greetings Planet!'
    >>> b = 12
    >>> b
    12
    """


def test_code_87_output_94(capsys):
    from datetime import date

    d = date.fromordinal(730920)  # 730920th day after 1. 1. 0001
    print(d)

    _phm_expected_str = """\
2002-03-11
"""
    _phm_compare_exact(a=_phm_expected_str, b=capsys.readouterr().out)
```
This page is created from a Markdown file that contains the contents
of a python source file in a syntax highlighted fenced code block.
It is included in the documentation as an example python file.
