"""Return pieces of code as strings for a pytest test file."""
import inspect
from io import StringIO
import textwrap

from phmdoctest.fenced import FencedBlock
from phmdoctest import functions


def compose_import_lines(needs_fixture: bool, needs_checking: bool) -> str:
    """Generate import lines for the test file."""
    lines = list()
    if needs_fixture:
        lines.append('import pytest\n\n')
        lines.append('from phmdoctest.fixture import managenamespace\n')
    if needs_checking:
        lines.append(
            'from phmdoctest.functions import _phm_compare_exact\n')
    return ''.join(lines)


def test_case(name: str, code: str, expected_output: str) -> str:
    """Add a def test_ function with code and comparison logic.

    Generate a function that has code as its body and
    includes logic to capture and compare the printed output.
    The function is named to be collected by pytest as a test case.
    """
    assert name.isidentifier(), 'must be a valid python identifier'
    src = '\n'
    if expected_output:
        src += inspect.getsource(functions.test_code_and_output)
        src = src.replace('code_and_output', name, 1)

        # indent contents of code block and place at <put code here>.
        indented_code = textwrap.indent(code, '    ')
        src = src.replace('    # <put code here>\n', indented_code, 1)
        src = src.replace('<<<replaced>>>', expected_output, 1)
    else:
        src += inspect.getsource(functions.test_code_only)
        src = src.replace('code_only', name, 1)
        src = src.replace('    pass\n', '\n    # Caution- no assertions.\n')

        # indent contents of code block and place at <put code here>.
        indented_code = textwrap.indent(code, '    ')
        src = src.replace('    # <put code here>\n', indented_code, 1)

    return src


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
    text = StringIO()
    text.write('\n')
    text.write('def session_{}_line_{}():\n'.format(
            sequence_string, line_number),)
    text.write('    r"""\n')
    text.write(indented_session)
    text.write('    """\n')
    return text.getvalue()


def setup_and_teardown_fixture(
    setup_block: FencedBlock,
    teardown_block: FencedBlock,
    setup_doctest: bool
) -> str:
    """Add functions to handle setup, teardown and setup for doctest."""
    assert setup_block or teardown_block, 'Must get at least one.'
    src = '\n\n'
    if setup_doctest:
        src += inspect.getsource(functions._phm_setup_doctest_teardown)
    else:
        src += inspect.getsource(functions._phm_setup_teardown)
    # do teardown code replace first so not searching through setup code.
    if teardown_block:
        comment = '# teardown code line {}.\n'.format(teardown_block.line)
        code = comment + teardown_block.contents
        indented_code = textwrap.indent(code, '    ')
        src = src.replace(
            '    # <teardown code here>\n', indented_code, 1)

    if setup_block:
        comment = '# setup code line {}.\n'.format(setup_block.line)
        code = comment + setup_block.contents
        indented_code = textwrap.indent(code, '    ')
        src = src.replace(
            '    # <setup code here>\n', indented_code, 1)

    src += '\n\n'
    format_spec = 'pytestmark = pytest.mark.usefixtures("{}")\n'
    if setup_doctest:
        src += format_spec.format('_phm_setup_doctest_teardown')
        # Add in more fixtures.
        # 1. Populate the doctest namespace with values from the setup code.
        # 2, session_00000 make the names visible to the doctests.
        src += '\n\n'
        src += functions.populate_doctest_namespace_str
        src += '\n\n'
        src += inspect.getsource(functions.session_00000)
    else:
        src += format_spec.format('_phm_setup_teardown')

    return src
