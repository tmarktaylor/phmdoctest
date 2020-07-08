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

    # variable to hold copies for testing sessions
    _session_globals = dict()

    # assign the local variables created so far to the module and
    # optionally save copies for testing sessions.
    for k, v in locals().items():
        # The value thismodulebypytest passed by pytest is the module
        # object that contains this function.
        # It shows up in locals(), so just ignore it.
        if k == "thismodulebypytest":
            continue
        setattr(thismodulebypytest, k, v)

        # make copies for testing sessions
        # assign the local variables to _session_globals.
        if k != "_session_globals":
            _session_globals[k] = v


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
