"""Pytest fixture imported by generated code."""
import inspect
import logging

import pytest

# mypy: ignore_errors


@pytest.fixture(scope="module")
def managenamespace(request):
    """Create and manipulate namespace implemented in the module."""
    logging.debug("managenamespace-")
    already_exists = (
        "phmdoctest- Not allowed to replace module level name {} because\n"
        "it pre-exists in the module at pytest time."
    )
    no_originals = "phmdoctest- no original module attributes allowed in namespace."
    no_extras = "phmdoctest- current attributes == original + namespace."
    m = request.module
    original_attributes = set([name for name, _ in inspect.getmembers(m)])
    namespace_names = set()

    def check_attribute_name(name):
        """Check that name was not an attribute of the original test module.

        It is an error to overwrite any of the
        the module attributes present in the source file.
        """
        if name in original_attributes:
            raise AttributeError(already_exists.format(name))

    def check_integrity():
        """Check module's attributes are original or in the namespace."""
        current_attributes = set([name for name, _ in inspect.getmembers(m)])
        if not original_attributes.isdisjoint(namespace_names):
            raise AttributeError(no_originals)
        if current_attributes != original_attributes.union(namespace_names):
            raise AttributeError(no_extras)

    def show_namespace():
        """Log the names currently in the namespace."""
        names = ", ".join(namespace_names)
        logging.debug("manager- namespace= %s", names)

    def manager(operation, additions=None):
        """Maintain namespace with update, copy, and clear operations.

        The namespace for the test cases is attributes assigned to the
        enclosing module object.  The attribute names are stored in the
        set namespace_names. The attribute values are stored in the
        module that imports this fixture.

        Args:
            operation
                - update add items to the namespace
                - copy returns a shallow copy of the namespace.
                - clear removes all items from the namespace.

            additions
                Mapping of names and values of variables that should be
                added to the namespace.
        """
        if operation == "clear":
            names = ", ".join(list(namespace_names))
            logging.debug("manager- clearing= %s", names)
            for name in namespace_names:
                check_attribute_name(name)
                delattr(m, name)
            namespace_names.clear()
            show_namespace()
            return None
        elif operation == "copy":
            logging.debug("manager- returning a copy")
            shallow_copy = dict()
            for name in namespace_names:
                shallow_copy[name] = getattr(m, name)
            return shallow_copy
        elif operation == "update":
            if additions is None:
                raise ValueError("phmdoctest- need additions to do an update")
            if not isinstance(additions, dict):
                raise TypeError("phmdoctest- must be a mapping")
            # Remove some items from additions that don't belong or
            # can't belong in the namespace.
            # Items that don't belong are the fixtures used by the test
            # case and the local variable _phm_expected_str.
            #     managenamespace
            #     capsys
            #     doctest_namespace
            #     _phm_expected_str
            _ = additions.pop("managenamespace", None)
            _ = additions.pop("doctest_namespace", None)
            _ = additions.pop("capsys", None)
            _ = additions.pop("_phm_expected_str", None)
            #
            # Items that can't be in the namespace are the imports:
            #     pytest
            #     sys
            # These imports may be at the top level of the generated test
            # file.  If they are present in additions they will
            # cause check_attribute_name() to raise an exception.
            # sys is imported for the phmdoctest-mark.skipif<3. directive.
            # Users might have one or both of them in their code block.
            _ = additions.pop("pytest", None)
            if "sys" in additions and "sys" in original_attributes:
                _ = additions.pop("sys", None)
            added_names = ", ".join(additions.keys())
            if added_names:
                logging.debug("manager- adding= %s", added_names)
            for k, v in additions.items():
                check_attribute_name(k)
                setattr(m, k, v)
                namespace_names.add(k)
            check_integrity()
            show_namespace()
        else:
            raise ValueError(
                'phmdoctest- operation="{}" is not allowed'.format(operation)
            )

    return manager
