"""pytest test case file code generator."""

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


class PytestFile:
    def __init__(self, description: str = ''):
        docstring = '"""' + description + '"""'
        self.lines = [docstring]
        self.lines.append('from itertools import zip_longest')
        self._empty_line()
        self._empty_line()
        # copy the helper function def
        self.lines.append(inspect.getsource(line_by_line_compare_exact))

    def __str__(self) -> str:
        return '\n'.join(self.lines)

    def _empty_line(self) -> None:
        """Add an empty line to the file."""
        self.lines.append('')

    @staticmethod
    def _remove_output_check(source: str) -> str:
        """Replace the expected output with a Caution message."""
        ix = source.index('    expected_str = """')
        source = source[:ix] + '    # Caution- no assertions.\n'
        return source

    def add_test_case(
            self, identifier: str, code: str, expected_output: str) -> None:
        """Add a def test_ function with code and comparison logic."""
        assert identifier.isidentifier(), 'must be a valid python identifier'
        self._empty_line()
        src = inspect.getsource(test_identifier)
        src = src.replace('identifier', identifier, 1)

        # indent contents of code block and place after '(capysy):\n'
        indented_code = textwrap.indent(code, '    ')
        src = src.replace('(capsys):', '(capsys):\n' + indented_code, 1)

        if expected_output:
            src = src.replace('<<<replaced>>>', expected_output, 1)
        else:
            src = self._remove_output_check(src)
        self.lines.append(src)

    def add_source(self, source: str) -> None:
        """Add the source code as is to the generated test file."""
        self._empty_line()
        self.lines.append(source)
