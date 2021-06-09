"""pytest file built from doc/setup_doctest.md"""
import pytest

from phmdoctest.fixture import managenamespace
from phmdoctest.functions import _phm_compare_exact


@pytest.fixture(scope="module")
def _phm_setup_doctest_teardown(doctest_namespace, managenamespace):
    # setup code line 9.
    import math

    mylist = [1, 2, 3]
    a, b = 10, 11

    def doubler(x):
        return x * 2

    managenamespace(operation="update", additions=locals())
    # update doctest namespace
    additions = managenamespace(operation="copy")
    for k, v in additions.items():
        doctest_namespace[k] = v
    yield
    # teardown code line 86.
    mylist.clear()
    assert not mylist, "mylist was not emptied"

    managenamespace(operation="clear")


pytestmark = pytest.mark.usefixtures("_phm_setup_doctest_teardown")


@pytest.fixture()
def populate_doctest_namespace(doctest_namespace, managenamespace):
    additions = managenamespace(operation="copy")
    for k, v in additions.items():
        doctest_namespace[k] = v


def session_00000():
    r"""
    >>> getfixture('populate_doctest_namespace')
    """


def test_code_20_output_27(capsys):
    print("math.pi=", round(math.pi, 3))
    print(mylist)
    print(a, b)
    print("doubler(16)=", doubler(16))

    _phm_expected_str = """\
math.pi= 3.142
[1, 2, 3]
10 11
doubler(16)= 32
"""
    _phm_compare_exact(a=_phm_expected_str, b=capsys.readouterr().out)


def test_code_37_output_42(capsys):
    mylist.append(4)
    print(mylist)

    _phm_expected_str = """\
[1, 2, 3, 4]
"""
    _phm_compare_exact(a=_phm_expected_str, b=capsys.readouterr().out)


def test_code_47_output_51(capsys):
    print(mylist == [1, 2, 3, 4])

    _phm_expected_str = """\
True
"""
    _phm_compare_exact(a=_phm_expected_str, b=capsys.readouterr().out)


def session_00001_line_69():
    r"""
    >>> mylist.append(55)
    >>> mylist
    [1, 2, 3, 55]
    """


def session_00002_line_76():
    r"""
    >>> mylist
    [1, 2, 3, 55]
    >>> round(math.pi, 3)
    3.142
    """
