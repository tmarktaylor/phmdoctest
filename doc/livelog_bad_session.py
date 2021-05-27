"""Demo showing how pytest responds to session failure with -x."""
import logging


def setup_module(thismodulebypytest):
    logging.debug("setup_module-")


def session_00000():
    r"""
    >>> print('session_00000')
    didn't print exactly session_00000 so should fail
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
    assert False  # fail the test case, won't be executed since -x fail above


def session_00002():
    r"""
    >>> print('session_00002')
    session_00002
    """


def test_3(capsys):
    logging.debug("test_3-")


def teardown_module():
    logging.debug("teardown_module-")
