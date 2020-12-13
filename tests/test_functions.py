"""Test cases for code templates in functions.py."""
import inspect

import pytest

import phmdoctest.functions


def test_def_test_identifier():
    """Painful way to eliminate 2 coverage missed statements."""
    # The function coder.test_identifier() is used as
    # a template to generate Python code.
    # It accepts the pytest fixture called capsys when the
    # generated pytest is run.
    # phmodctest doesn't call this function so it shows up
    # in the coverage report as a missed statement.
    # Here a test mock up of the fixture is created that
    # provides the expected value as its out attribute.
    class MockReadouterr:
        def __init__(self):
            self.out = '<<<replaced>>>'

    class MockCapsys:
        @staticmethod
        def readouterr():
            return MockReadouterr()

    phmdoctest.functions.test_identifier(MockCapsys())


def test_def_test_nothing_fails():
    """This is done for code coverage of the function."""
    with pytest.raises(AssertionError):
        phmdoctest.functions.test_nothing_fails()


def test_def_test_nothing_passes():
    """This is done for code coverage of the function."""
    phmdoctest.functions.test_nothing_passes()


def test_def_setup_module():
    """The template should not add any attribute to passed object."""
    # functions.setup_module() calls set_as_module_attributes().
    # functions.setup_module() had no callers code.
    # So the number of attributes in my_module should not change.
    class AModule:
        pass
    my_module = AModule()
    before = inspect.getmembers(my_module)
    phmdoctest.functions.setup_module(my_module)
    after = inspect.getmembers(my_module)
    assert len(before) == len(after), 'no more attributes'


def test_def_set_as_module_attributes():
    """The template should add an empty dict as attribute to passed object."""
    # The class AModule will show up in locals() and should be copied
    # as an attribute to the module thismodulebypytest.
    # The string remark is also a local and should be copied as well.
    class AModule:
        pass
    remark = 'enjoys coffee and coding'
    thismodulebypytest = AModule()
    phmdoctest.functions.set_as_module_attributes(
        thismodulebypytest, locals())
    assert thismodulebypytest.AModule, 'exists'
    assert thismodulebypytest.remark == 'enjoys coffee and coding'


def test_def_set_as_session_globals():
    """The template should add an empty dict as attribute to passed object."""
    # The class AModule will show up in locals() and should be copied into
    # thismodulebypytest._session_globals by set_as_session_globals().
    class AModule:
        pass
    thismodulebypytest = AModule()
    phmdoctest.functions.set_as_session_globals(thismodulebypytest, locals())
    assert 'AModule' in thismodulebypytest._session_globals
    assert 'thismodulebypytest' not in thismodulebypytest._session_globals


def test_def_teardown_module():
    phmdoctest.functions.teardown_module()
