"""Functions customized and copied into generated code."""
import difflib
from itertools import zip_longest

import pytest

# mypy: ignore_errors


# The function below is copied into the generated python source
def _phm_compare_exact(a, b):
    """Line by line helper compare function with assertion for pytest."""
    a_lines = a.splitlines()
    b_lines = b.splitlines()
    for a_line, b_line in zip_longest(a_lines, b_lines):
        if a_line != b_line:
            diffs = difflib.ndiff(a_lines, b_lines)
            for line in diffs:
                print(line)
            assert False


@pytest.fixture(scope="module")
def _phm_setup_teardown(managenamespace):
    # <setup code here>

    managenamespace(operation='update', additions=locals())
    yield
    # <teardown code here>

    managenamespace(operation='clear')


@pytest.fixture(scope="module")
def _phm_setup_doctest_teardown(managenamespace, doctest_namespace):
    # <setup code here>

    managenamespace(operation='update', additions=locals())
    # update doctest namespace
    additions = managenamespace(operation='copy')
    for k, v in additions.items():
        doctest_namespace[k] = v
    yield
    # <teardown code here>

    managenamespace(operation='clear')


# The function below is used as a template to generate python source
# code to be written to a file.
# It is coded here as compiled python so the IDE can check for
# syntax and style.
# Python introspection of the function's source code provides the
# source code as a string.
#
# This template will be customized by replacing:
# - The _code_and_output substring of the function name.
# - Insert example code indented 4 spaces at the
#   <put code here> placeholder.
# - Triple quoted string contents with the expected output.
def test_code_and_output(capsys):
    # <put code here>

    expected_str = """\
<<<replaced>>>"""
    _phm_compare_exact(a=expected_str, b=capsys.readouterr().out)


# This template will be customized by replacing:
# - The _code_only substring of the function name.
# - Insert example code indented 4 spaces at the
#   <put code here> placeholder.
def test_code_only():
    # <put code here>
    pass


def test_nothing_fails():
    """Fail if no Python code blocks or sessions were processed."""
    assert False, 'nothing to test'


def test_nothing_passes():
    """Succeed  if no Python code blocks or sessions were processed."""
    # nothing to test
    pass


# The fixture copies globals created by the --setup code
# into the pytest namespace supplied to doctests when
# doing pytest --doctest-modules.
# This code is included only if phmdoctest option --setup-doctest.
populate_doctest_namespace_str = """\
@pytest.fixture()
def populate_doctest_namespace(doctest_namespace, managenamespace):
    additions = managenamespace(operation='copy')
    for k, v in additions.items():
        doctest_namespace[k] = v
"""


# This part is only needed for testing sessions.
# It populates the doctest namespace.
def session_00000():
    r"""
    >>> getfixture('populate_doctest_namespace')
    """
