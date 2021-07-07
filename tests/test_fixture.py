"""Tests for managenamespace fixture in fixture.py."""
import sys

import pytest

from phmdoctest.fixture import managenamespace
import verify


# Note:
# The two check_integrity() exceptions listed here.
# 1.   raise AttributeError(no_originals)
# 2.   raise AttributeError(no_extras)
#
# Require manual testing.
# Edit fixture.py and run pytest on this file to inject the error.
#
# 1. namespace_names.add('verify')    # add this line above the 1st raise.
#
# 2. namespace_names.add('bogus')    # add this line above the 2nd raise.


def test_managenamespace_outfile():
    """Show that managenamespace.md generates test_managenamespace.py."""

    # Generate an outfile from tests/managenamespace.md and
    # compare it to the test suite file tests/test_managenamespace.py.
    #
    # When pytest runs tests/test_managenamespace.py the
    # fixture managenamespace is imported and update() is called.
    # The line _ = additions.pop('sys', None) is called.
    #
    # The combination of import sys at the top of the test file
    # and import sys in the example code is needed to test
    # that line of code.
    command = "phmdoctest tests/managenamespace.md --outfile discarded.py"
    _ = verify.one_example(
        command, want_file_name="tests/test_managenamespace.py", pytest_options=None
    )


def test_update_item_removals(managenamespace):
    """Try an update with names that get popped before the update."""
    # 'sys' below exercises the _ = additions.pop('sys', None) line in the
    # fixture source code.
    items = {
        "sys": None,
        "managenamespace": None,
        "doctest_namespace": None,
        "capsys": None,
        "_phm_expected_str": None,
        "example_variable": 1111,
    }
    managenamespace(operation="update", additions=items)
    namespace_copy = managenamespace(operation="copy")
    assert "example_variable" in namespace_copy
    assert namespace_copy["example_variable"] == 1111
    assert "sys" not in namespace_copy
    assert "managenamespace" not in namespace_copy
    assert "doctest_namespace" not in namespace_copy
    assert "capsys" not in namespace_copy
    assert "_phm_expected_str" not in namespace_copy

    # Clear the namespace.
    managenamespace(operation="clear", additions=None)
    namespace_copy = managenamespace(operation="copy")
    assert len(namespace_copy) == 0

    # Add more items to the namespace.
    more_items = {"A": None, "B": None, "C": None}
    managenamespace(operation="update", additions=more_items)
    namespace_copy = managenamespace(operation="copy")
    assert len(namespace_copy) == 3
    for name in more_items.keys():
        assert name in namespace_copy


def test_check_attribute_name_asserts(managenamespace):
    """Update asserts if an item is in the original module namespace."""
    items = {"verify": None}
    with pytest.raises(AttributeError) as exc_info:
        managenamespace(operation="update", additions=items)
    want = "phmdoctest- Not allowed to replace module level name verify because"
    assert want in str(exc_info.value)


def test_illegal_operation(managenamespace):
    """Update asserts if operation in not 'update', 'copy', or 'clear'."""
    items = {"E": None, "F": None}
    with pytest.raises(ValueError) as exc_info:
        managenamespace(operation="bogus", additions=items)
    want = 'phmdoctest- operation="bogus" is not allowed'
    assert want in str(exc_info.value)
