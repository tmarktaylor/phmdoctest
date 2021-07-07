"""Test the _phm_setup_teardown fixture in functions.py."""
import logging

import pytest

from phmdoctest.fixture import managenamespace
from phmdoctest.functions import _phm_setup_teardown

pytestmark = pytest.mark.usefixtures("_phm_setup_teardown")


def test_setup_teardown_fixture(_phm_setup_teardown, managenamespace):
    """Show the fixture runs.  Run namespace operations."""

    # The namespace should be empty.
    items = managenamespace(operation="copy")
    assert items == dict()

    # A module level global in the test file can't be modified.
    with pytest.raises(AttributeError) as exc_info:
        bogus_name = "pytestmark"
        logging.debug("tests- Trying to add %s", bogus_name)
        items = {bogus_name: 0}
        managenamespace(operation="update", additions=items)
    logging.debug("tests- An assertion was raised")
    assert "pre-exists" in str(exc_info.value)
    assert bogus_name in str(exc_info.value)

    # See an update reflected in a copy.
    logging.debug("tests- trying an update, then a copy.")
    more_items = {"zero": 0, "one": 1, "myset": set([7, 8, 9])}
    managenamespace(operation="update", additions=more_items)
    copy_of_more_items = managenamespace(operation="copy")
    assert more_items == copy_of_more_items
    logging.debug("tests- copy is the same as the update additions.")

    # Try an unsupported operation
    with pytest.raises(ValueError):
        managenamespace(operation="bogus")

    # Try update, but no additions
    with pytest.raises(ValueError):
        managenamespace(operation="update")

    # Try update, but additions is not a mapping
    with pytest.raises(TypeError):
        managenamespace(operation="update", additions=set([1, 2, 3]))
