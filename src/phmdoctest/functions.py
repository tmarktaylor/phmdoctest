"""Functions customized and copied into generated code."""

from itertools import zip_longest


# mypy: ignore_errors


# The function below is copied into the generated python source
def line_by_line_compare_exact(a, b):
    """Line by line helper compare function with assertion for pytest."""
    a_lines = a.splitlines()
    b_lines = b.splitlines()
    for a_line, b_line in zip_longest(a_lines, b_lines):
        assert a_line == b_line


# The function below is used as a template to generate python source
# code to be written to a file.
# It is coded here as compiled python so the IDE can check for
# syntax and style.
# Python introspection of the function's source code provides the
# source code as a string.
#
# This template will be customized by replacing:
# - The _identifier substring of the function name.
# - Insert example code indented 4 spaces on a new line
#   after the def statement.
# - Triple quoted string contents with the expected output.
def test_identifier(capsys):
    expected_str = """\
<<<replaced>>>"""
    line_by_line_compare_exact(a=expected_str, b=capsys.readouterr().out)


def test_nothing_fails():
    """Fail if no Python code blocks or sessions were processed."""
    assert False, 'nothing to test'


def test_nothing_passes():
    """Succeed  if no Python code blocks or sessions were processed."""
    # nothing to test
    pass


# This template will be customized by:
# 1. adding a function docstring.
# 2. adding the callers code block.
# 3. optionally removing the _session_globals logic.
#
# By observation:
# k, v would be present in a locals() call after the for loop exits.
# k, v do not show up in the locals() call below which is part of the
# for statement because they are assigned within the scope of the
# for loop.  The Python Language Reference hints that this is the
# way it works, but didn't seem very explicit.
def setup_module(thismodulebypytest):
    """<put docstring here>"""
    # <put code block here>

    # variable to hold copies for testing sessions
    _session_globals = dict()

    # assign the local variables created so far to the module and
    # optionally save copies for testing sessions.
    for k, v in locals().items():
        # The value thismodulebypytest passed by pytest is the module
        # object that contains this function.
        # It shows up in locals(), so just ignore it.
        if k == "thismodulebypytest":
            continue
        setattr(thismodulebypytest, k, v)

        # make copies for testing sessions
        # assign the local variables to _session_globals.
        if k != "_session_globals":
            _session_globals[k] = v


# The fixture copies globals created by the --setup code
# into the pytest namespace supplied to doctests when
# doing pytest --doctest-modules.
# This code is included only if phmdoctest option --setup-doctest.
populate_doctest_namespace_str = """\
@pytest.fixture()
def populate_doctest_namespace(doctest_namespace):
    for k, v in _session_globals.items():
        doctest_namespace[k] = v
"""


# This part is only needed for testing sessions.
# It populates doctest namespace from _session_globals.
def session_00000():
    r"""
    >>> getfixture('populate_doctest_namespace')
    """


# This template will be customized by:
# 1. adding a function docstring.
# 2. adding the callers code block.
# 3. remove the line with the pass statement.
# note- the pass is needed to prevent inspect from dropping the comment.
def teardown_module():
    """<put docstring here>"""
    # <put code block here>
    pass
