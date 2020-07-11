"""Test cases for code templates in functions.py."""
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
    """The template should add an empty dict as attribute to passed object."""
    class AModule:
        pass
    my_module = AModule()
    phmdoctest.functions.setup_module(my_module)
    assert my_module._session_globals == dict()


def test_def_teardown_module():
    phmdoctest.functions.teardown_module()
