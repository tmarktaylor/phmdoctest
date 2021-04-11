"""Test the _phm_setup_doctest_teardown fixture in functions.py."""
import pytest

from phmdoctest.fixture import managenamespace
from phmdoctest.functions import _phm_setup_doctest_teardown

pytestmark = pytest.mark.usefixtures("_phm_setup_doctest_teardown")


def test_setup_doctest_teardown_fixture(
        _phm_setup_doctest_teardown, managenamespace):
    """Show the fixture runs and the namespace is created."""
    items = managenamespace(operation='copy')
    assert items == dict()
