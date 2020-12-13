"""Return pieces of code as strings for a pytest test file."""

import inspect
import textwrap

import click

from phmdoctest import functions


def docstring_and_helpers(description: str = '') -> str:
    """Initial few lines of the test file."""
    text = [
        '"""', description, '"""\n',
        'from itertools import zip_longest\n',
        '\n\n',
        inspect.getsource(functions.line_by_line_compare_exact)
    ]
    return ''.join(text)


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
    text = [
        '\n',
        'def session_{}_line_{}():\n'.format(
            sequence_string, line_number),
        '    r"""\n',
        indented_session,
        '    """\n'
    ]
    return ''.join(text)


def caller_did_not_use_reserved_name(identifier: str, code: str) -> None:
    """Immediate exit if caller used a reserved name."""
    reserved = '_session_globals'
    if reserved in code:
        message = (
            'The reserved name {} is used\n'
            'somewhere in --setup {}.\n'
            'It is not allowed anywhere in the block although\n'
            'it only causes problems for doctests\n'
            'if assigned at the top level.'
        ).format(reserved, identifier)
        raise click.ClickException(message)


def setup(identifier: str, code: str, setup_doctest: bool) -> str:
    """Add code as part of pytest setup_module fixture.

    Generate the function body for pytest fixture setup_module.
    It keeps track of code's variable assignments.
    It copies them out to the module object passed to the fixture.
    Passing setup_doctest=True indicates the variable assignments
    are wanted in doctest namespace.
    The namespace is created when pytest is running with --doctest-modules.
    """
    caller_did_not_use_reserved_name(identifier, code)
    src = '\n'
    src += inspect.getsource(functions.setup_module)
    src = src.replace('<put docstring here>', identifier)
    indented_code = textwrap.indent(code, '    ')
    src = src.replace('    # <put code block here>\n', indented_code)
    if setup_doctest:
        # add call to set_as_session_globals()
        src += '    set_as_session_globals(thismodulebypytest, locals())\n'
    src += '\n'
    src += '\n'
    src += inspect.getsource(functions.set_as_module_attributes)

    if not setup_doctest:
        return src
    else:
        text = [
            src,
            '\n',
            '\n',
            # Add function, called from above, to copy the
            # code block's names up to a new dict at the module level.
            inspect.getsource(functions.set_as_session_globals),
            '\n',
            '\n',

            # Add a fixture to inject the code block's names
            # into pytest's doctest namespace.
            # The doctest namespace is created when pytest is
            # run with --doctest-modules.
            functions.populate_doctest_namespace_str,
            '\n',
            '\n',
            # add a session that invokes the fixture above
            inspect.getsource(functions.session_00000)
        ]
        return ''.join(text)


def teardown(identifier: str, code: str) -> str:
    """Generate the function body for pytest fixture teardown_module."""
    text = ['\n']
    src = inspect.getsource(functions.teardown_module)
    src = src.replace('    pass\n', '')
    src = src.replace('<put docstring here>', identifier)
    src = src.replace('    # <put code block here>\n', '')
    text.append(src)
    text.append(textwrap.indent(code, '    '))
    return ''.join(text)
