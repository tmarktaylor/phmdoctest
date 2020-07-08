#### doc/test_example2.py
```python3
"""pytest file built from doc/example2.md"""
from itertools import zip_longest


def line_by_line_compare_exact(a, b):
    """Line by line helper compare function with assertion for pytest."""
    a_lines = a.splitlines()
    b_lines = b.splitlines()
    for a_line, b_line in zip_longest(a_lines, b_lines):
        assert a_line == b_line


def test_code_9_output_14(capsys):
    squares = [1, 4, 9, 16, 25]
    print(squares)

    expected_str = """\
[1, 4, 9, 16, 25]
"""
    line_by_line_compare_exact(a=expected_str, b=capsys.readouterr().out)


def test_code_37(capsys):
    a, b = 0, 1
    while a < 1000:
        print(a, end=',')
        a, b = b, a+b

    # Caution- no assertions.


def test_code_44_output_51(capsys):
    words = ['cat', 'window', 'defenestrate']
    for w in words:
        print(w, len(w))

    expected_str = """\
cat 3
window 6
defenestrate 12
"""
    line_by_line_compare_exact(a=expected_str, b=capsys.readouterr().out)


def session_00001_line_75():
    r"""
    >>> a = 'Greetings Planet!'
    >>> a
    'Greetings Planet!'
    >>> b = 12
    >>> b
    12
    """


def test_code_87_output_93(capsys):
    from datetime import date
    d = date.fromordinal(730920)    # 730920th day after 1. 1. 0001
    print(d)

    expected_str = """\
2002-03-11
"""
    line_by_line_compare_exact(a=expected_str, b=capsys.readouterr().out)
```
This page is created from a Markdown file that contains the contents
of a python source file in a syntax highlighted fenced code block.
It is included in the documentation as an example python file.
