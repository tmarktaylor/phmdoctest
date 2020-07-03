"""Return pieces of code as strings for a pytest test file."""

import inspect
import textwrap

from phmdoctest import functions


def docstring_and_helpers(description: str = '') -> str:
    """Initial few lines of the test file."""
    text = '"""' + description + '"""\n'
    text += 'from itertools import zip_longest\n'
    text += '\n'
    text += '\n'
    return text + inspect.getsource(functions.line_by_line_compare_exact)


def _remove_output_check(source: str) -> str:
    """Replace the expected output with a Caution message."""
    ix = source.index('    expected_str = """')
    source = source[:ix] + '    # Caution- no assertions.\n'
    return source


def test_case(identifier: str, code: str, expected_output: str) -> str:
    """Add a def test_ function with code and comparison logic.

    Generate a function that has code as its body and
    includes logic to capture and compare the printed output.
    The function is named to be collected by pytest as a test case.
    """
    assert identifier.isidentifier(), 'must be a valid python identifier'
    src = inspect.getsource(functions.test_identifier)
    src = src.replace('identifier', identifier, 1)

    # indent contents of code block and place after '(capysy):\n'
    indented_code = textwrap.indent(code, '    ')
    src = src.replace('(capsys):', '(capsys):\n' + indented_code, 1)

    if expected_output:
        src = src.replace('<<<replaced>>>', expected_output, 1)
    else:
        src = _remove_output_check(src)
    return '\n' + src


def interactive_session(
        sequence_number: int, line_number: int, session: str) -> str:
    """Add a do nothing function with doctest session as its docstring.

    Generate the function that has the session as
    its docstring and a function name that prevents it from being
    collected as a test case.
    Run pytest with --doctest-modules to run doctest on the session.
    """
    sequence_string = format(sequence_number, '05d')
    indented_session = textwrap.indent(session, '    ')
    text = '\n'
    text += 'def session_{}_line_{}():\n'.format(
        sequence_string, line_number)
    text += '    r"""\n'
    text += indented_session
    return text + '    """\n'


_session_globals_match = (
    '    # <variable to hold copies for testing sessions>\n'
    '    _session_globals = dict()\n\n'
)

_needs_indent = (
    '# <make copies for testing sessions>\n'
    '# This code is included only if phmdoctest option --setup-doctest.\n'
    '# assign the local variables to _session_globals.\n'
    'if k != "_session_globals":\n'
    '    _session_globals[k] = v\n\n'
)
_make_copies_match = textwrap.indent(_needs_indent, '        ')


def setup(identifier: str, code: str, setup_doctest: bool) -> str:
    """Add code as part of pytest setup_module fixture.

    Generate the function body for pytest fixture setup_module.
    Keep track of code's variable assignments.
    Copy them out to the module object passed to the fixture.
    Passing setup_doctest=True indicates the variable assignments
    are wanted in doctest namespace.
    The namespace is created when pytest is running with --doctest-modules.
    """
    text = '\n'
    src = inspect.getsource(functions.setup_module)
    src = src.replace('<put docstring here>', identifier)
    indented_code = textwrap.indent(code, '    ')
    src = src.replace('    # <put code block here>\n', indented_code)
    text += src
    text += '\n'

    if setup_doctest:
        # Keep track of code's variable assignments and add
        # elements to inject them into pytest's doctest namespace
        # that is created when pytest is  running with --doctest-modules.
        # add the fixture to inject values into the doctest namespace
        text += '\n'
        src2 = inspect.getsource(functions.populate_doctest_namespace)
        text += src2
        text += '\n'

        # add a session that invokes the fixture above
        text += '\n'
        src3 = inspect.getsource(functions.session_00000)
        text += src3
    else:
        # remove code to save session globals
        src = src.replace(_session_globals_match, '')
        src = src.replace(_make_copies_match, '')
        text += src
    return text


def teardown(identifier: str, code: str) -> str:
    """Generate the function body for pytest fixture teardown_module."""
    text = '\n'
    src = inspect.getsource(functions.teardown_module)
    src = src.replace('    pass\n', '')
    src = src.replace('<put docstring here>', identifier)
    src = src.replace('    # <put code block here>\n', '')
    text += src
    indented_code = textwrap.indent(code, '    ')
    return text + indented_code
