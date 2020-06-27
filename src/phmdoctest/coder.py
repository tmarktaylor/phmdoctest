"""pytest test case file code generator."""

from io import StringIO
import inspect
from itertools import zip_longest
import textwrap


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


# todo- This template will be customized by TBV
# todo- explain why do k, v not show up in locals()
def setup_module(thismodulebypytest):
    # <put identifier here>
    # <put code here>
    # end of code
    # assign the variables created in the code to the module
    for k, v in locals().items():
        # The value thismodulebypytest passed by pytest
        # is the module object that contains this function.
        # It shows up in locals(), so just ignore it.
        if k == 'thismodulebypytest':
            continue
        setattr(thismodulebypytest, k, v)


# note- the pass is needed to prevent inspect from dropping the comment.
def teardown_module():
    # <put identifier here>
    pass


def docstring_and_helpers(description: str = '') -> str:
    stream = StringIO()
    stream.write('"""' + description + '"""\n')
    stream.write('from itertools import zip_longest\n')
    stream.write('\n')
    stream.write('\n')
    stream.write(inspect.getsource(line_by_line_compare_exact))
    output = stream.getvalue()
    stream.close()
    return output


def _remove_output_check(source: str) -> str:
    """Replace the expected output with a Caution message."""
    ix = source.index('    expected_str = """')
    source = source[:ix] + '    # Caution- no assertions.\n'
    return source


def test_case(identifier: str, code: str, expected_output: str) -> str:
    """Add a def test_ function with code and comparison logic."""
    assert identifier.isidentifier(), 'must be a valid python identifier'
    src = inspect.getsource(test_identifier)
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
        sequence_number: int, identifier: str, session: str) -> str:
    """Add a do nothing function with doctest session as its docstring."""
    sequence_string = format(sequence_number, '05d')
    indented_session = textwrap.indent(session, '    ')
    stream = StringIO()
    stream.write('\n')
    stream.write('def session_{}_line_{}():\n'.format(
        sequence_string, identifier))
    stream.write('    r"""\n')
    stream.write(indented_session)
    stream.write('    """\n')
    output = stream.getvalue()
    stream.close()
    return output


def setup(identifier: str, code: str) -> str:
    """Add code as module level setup code."""
    stream = StringIO()
    stream.write('\n')
    src = inspect.getsource(setup_module)
    src = src.replace('<put identifier here>', identifier)
    indented_code = textwrap.indent(code, '    ')
    src = src.replace('    # <put code here>\n', indented_code)
    stream.write(src)
    output = stream.getvalue()
    stream.close()
    return output


def teardown(identifier: str, code: str) -> str:
    """Add teardown code to teardown fixture."""
    stream = StringIO()
    stream.write('\n')
    src = inspect.getsource(teardown_module)
    src = src.replace('    pass\n', '')
    src = src.replace('<put identifier here>', identifier)
    stream.write(src)
    indented_code = textwrap.indent(code, '    ')
    stream.write(indented_code)
    output = stream.getvalue()
    stream.close()
    return output
