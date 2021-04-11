import inspect
import logging

import pytest


@pytest.fixture(scope="module")
def managenamespace(request):
    """Create and manipulate namespace implemented in the module."""
    logging.debug('managenamespace-')
    already_exists = (
        'Not allowed to replace module level name {} because\n'
        'it pre-exists in the module at pytest time.'
    )
    no_originals = 'no original module attributes allowed in namespace.'
    no_extras = 'current attributes == original + namespace.'
    m = request.module
    original_attributes = set([name for name, _ in inspect.getmembers(m)])
    namespace_names = set()

    def check_attribute_name(name):
        """Check that name was not an attribute of the original test module.

        It is an error to overwrite or delete any of the
        the module attributes present in the source file.
        """
        assert name not in original_attributes, already_exists.format(name)

    def check_integrity():
        """Check module's attributes are original or in the namespace."""
        current_attributes = set([name for name, _ in inspect.getmembers(m)])
        assert original_attributes.isdisjoint(namespace_names), no_originals
        assert current_attributes == original_attributes.union(
            namespace_names), no_extras

    def show_namespace():
        """Log the names currently in the namespace."""
        names = ', '.join(namespace_names)
        logging.debug('manager- namespace= %s', names)

    def manager(operation, additions=None):
        """Maintain namespace with update, copy, and clear operations.

        The namespace for the test cases as attributes assigned to the
        enclosing module object.  The attribute names are stored in the
        dict namespace_names.

        Args:
            operation
                - update add items to the namespace
                - copy returns a shallow copy of the namespace.
                - clear removes all items from the namespace.

            additions
                Mapping of names and values of variables that should be
                added to the namespace.
        """
        if operation == 'clear':
            names = ', '.join(list(namespace_names))
            logging.debug('manager- clearing= %s', names)
            for name in namespace_names:
                check_attribute_name(name)
                delattr(m, name)
            namespace_names.clear()
            show_namespace()
            return None
        elif operation == 'copy':
            logging.debug('manager- returning a copy')
            shallow_copy = dict()
            for name in namespace_names:
                shallow_copy[name] = getattr(m, name)
            return shallow_copy
        elif operation == 'update':
            assert additions is not None, 'need additions to do an update'
            assert isinstance(additions, dict), 'must be a mapping'
            # Remove some items from additions that don't belong in the
            # namespace.
            # The operation="update" caller may have passed locals() called
            # inside a pytest test function.  Ignore the two fixtures:
            #     managenamespace
            #     doctest_namespace (from pytest)
            # The code from functions._phm_setup_doctest_teardown is an
            # example of passing the fixtures into a test function that calls
            # managenamespace.manager().
            _ = additions.pop('managenamespace', 1)
            _ = additions.pop('doctest_namespace', 1)
            added_names = ', '.join(additions.keys())
            if added_names:
                logging.debug('manager- adding= %s', added_names)
            for k, v in additions.items():
                check_attribute_name(k)
                setattr(m, k, v)
                namespace_names.add(k)
            check_integrity()
            show_namespace()
        else:
            assert False, 'operation={} is not allowed'.format(
                repr(operation))

    return manager
