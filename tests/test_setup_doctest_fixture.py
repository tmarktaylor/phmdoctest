"""Run the codeless _phm_setup_doctest_teardown fixture in functions.py."""
import pytest

from phmdoctest.fixture import managenamespace
from phmdoctest.functions import _phm_setup_doctest_teardown

pytestmark = pytest.mark.usefixtures("_phm_setup_doctest_teardown")


def test_setup_doctest_teardown_fixture(_phm_setup_doctest_teardown, managenamespace):
    """Show the fixture runs and the namespace is created."""
    # This is the fixture with placeholders for setup and teardown code.
    # There is no way to get code coverage of the
    # doctest_namespace assignment in the loop.
    items = managenamespace(operation="copy")
    assert items == dict()
