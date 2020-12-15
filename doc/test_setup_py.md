#### doc/test_setup.py
```python3
"""pytest file built from doc/setup.md"""
from itertools import zip_longest


def line_by_line_compare_exact(a, b):
    """Line by line helper compare function with assertion for pytest."""
    a_lines = a.splitlines()
    b_lines = b.splitlines()
    for a_line, b_line in zip_longest(a_lines, b_lines):
        assert a_line == b_line


def setup_module(thismodulebypytest):
    """code line 9"""
    import math
    mylist = [1, 2, 3]
    a, b = 10, 11
    def doubler(x):
        return x * 2

    set_as_module_attributes(thismodulebypytest, locals())


def set_as_module_attributes(m, mapping):
    """Assign items in mapping as names in object m."""
    for k, v in mapping.items():
        # The value thismodulebypytest passed by pytest
        # shows up in locals() but is not part of the callers
        # code block so don't copy it to the module namespace.
        if k == "thismodulebypytest":
            continue
        setattr(m, k, v)


def test_code_18_output_25(capsys):
    print('math.pi=', round(math.pi, 3))
    print(mylist)
    print(a, b)
    print('doubler(16)=', doubler(16))

    expected_str = """\
math.pi= 3.142
[1, 2, 3]
10 11
doubler(16)= 32
"""
    line_by_line_compare_exact(a=expected_str, b=capsys.readouterr().out)


def test_code_35_output_40(capsys):
    mylist.append(4)
    print(mylist)

    expected_str = """\
[1, 2, 3, 4]
"""
    line_by_line_compare_exact(a=expected_str, b=capsys.readouterr().out)


def test_code_45_output_49(capsys):
    print(mylist == [1, 2, 3, 4])

    expected_str = """\
True
"""
    line_by_line_compare_exact(a=expected_str, b=capsys.readouterr().out)


def teardown_module():
    """code line 56"""
    mylist.clear()
    assert not mylist, 'mylist was not emptied'
```
This page is created from a Markdown file that contains the contents
of a python source file in a syntax highlighted fenced code block.
It is included in the documentation as an example python file.
