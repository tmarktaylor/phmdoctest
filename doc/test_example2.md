# Generated test file test_example2.py
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
```