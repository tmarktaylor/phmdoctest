"""pytest file built from doc/setup_doctest.md"""
from itertools import zip_longest

import pytest


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
    set_as_session_globals(thismodulebypytest, locals())


def set_as_module_attributes(m, mapping):
    """Assign items in mapping as names in object m."""
    for k, v in mapping.items():
        # The value thismodulebypytest passed by pytest
        # shows up in locals() but is not part of the callers
        # code block so don't copy it to the module namespace.
        if k == "thismodulebypytest":
            continue
        setattr(m, k, v)


def set_as_session_globals(m, mapping):
    """Create a dict in the module m's namespace to hold globals."""
    # The globals later get copied to the session namespace.
    setattr(m, "_session_globals", dict())

    for k, v in mapping.items():
        # The value thismodulebypytest passed by pytest is the module
        # object that contains this function.
        # It shows up in locals(), so just ignore it.
        if k == "thismodulebypytest":
            continue
        m._session_globals[k] = v


@pytest.fixture()
def populate_doctest_namespace(doctest_namespace):
    for k, v in _session_globals.items():
        doctest_namespace[k] = v


def session_00000():
    r"""
    >>> getfixture('populate_doctest_namespace')
    """


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


def session_00001_line_67():
    r"""
    >>> mylist.append(55)
    >>> mylist
    [1, 2, 3, 55]
    """


def session_00002_line_74():
    r"""
    >>> mylist
    [1, 2, 3, 55]
    >>> round(math.pi, 3)
    3.142
    """


def teardown_module():
    """code line 84"""
    mylist.clear()
    assert not mylist, 'mylist was not emptied'
