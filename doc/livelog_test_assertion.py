"""Demo showing how pytest responds to test case failure with -x.

Since pytest runs sessions first, the sessions must all pass --doctest-modules
before we can demo a failing test_*() function.
"""
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
    assert False  # fail the test case


def session_00002():
    r"""
    >>> print('session_00002')
    session_00002
    """


def test_3(capsys):
    logging.debug("test_3-")


def teardown_module():
    logging.debug("teardown_module-")
