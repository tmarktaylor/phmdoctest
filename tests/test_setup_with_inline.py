"""pytest file built from tests/setup_with_inline.md"""
import pytest

from phmdoctest.fixture import managenamespace
from phmdoctest.functions import _phm_compare_exact


@pytest.fixture(scope="module")
def _phm_setup_teardown(managenamespace):
    # setup code line 11.
    mylist = [1, 2, 3]
    # a, b = 10, 11  # phmdoctest:omit

    def raiser():
        pass  # assert False  # phmdoctest:pass

    managenamespace(operation="update", additions=locals())
    yield
    # teardown code line 41.
    mylist.clear()
    assert not mylist, "mylist was not emptied"
    # assert False  # phmdoctest:omit

    managenamespace(operation="clear")


pytestmark = pytest.mark.usefixtures("_phm_setup_teardown")


def test_code_23_output_32_1(capsys):

    print(mylist)
    raiser()
    # if mylist:                                 # phmdoctest:omit
    #     print("I should be commented out").
    #     assert False

    _phm_expected_str = """\
[1, 2, 3]
"""
    _phm_compare_exact(a=_phm_expected_str, b=capsys.readouterr().out)
