"""Demo showing how pytest organizes execution context and test order."""
import logging


def setup_module(thismodulebypytest):
    logging.debug("setup_module-")


def session_00000():
    r"""
    >>> print('session_00000')
    session_00000
    """


def session_00001():
    r"""
    >>> print('session_00001')
    session_00001
    """


def test_1(capsys):
    logging.debug("test_1-")


def test_2(capsys):
    logging.debug("test_2-")


def session_00002():
    r"""
    >>> print('session_00002')
    session_00002
    """


def test_3(capsys):
    logging.debug("test_3-")


def teardown_module():
    logging.debug("teardown_module-")
