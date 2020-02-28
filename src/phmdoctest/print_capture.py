import inspect
import textwrap


def line_compare_exact(want, got):
    """Line by line helper compare function with assertion for pytest."""
    if want:
        want_lines = want.splitlines()
        got_lines = got.splitlines()
        assert want_lines == got_lines


# The function below is used as a template to generate python source
# code to be written to a file.
# It is coded here as compiled python so the IDE can check for
# syntax and style.
# Python introspection of the function's source code provides the
# source code as a string.
#
# This template will be customized by replacing:
# - The _identifier substring of the function name.
# - Insert example code indented 4 spaces on a new line after the def statement.
# - Triple quoted string contents with the expected output.
def test_identifier(capsys):
    expected_str = """\
<<<replaced>>>"""
    line_compare_exact(want=expected_str, got=capsys.readouterr().out)


class PytestFile:
    def __init__(self, description=''):
        docstring = '"""' + description + '"""'
        self.lines = [docstring]
        self.empty_line()
        self.empty_line()
        # copy the helper function def
        self.lines.append(inspect.getsource(line_compare_exact))
        self.has_module_code = False
        self.has_teardown = False

    def __str__(self):
        return '\n'.join(self.lines)

    def empty_line(self):
        """Add an empty line to the file."""
        self.lines.append('')

    @staticmethod
    def remove_output_check(source):
        """Set the expected output to the empty string."""
        ix = source.index('    expected_str = """')
        source = source[:ix] + '    # Caution- no assertions.\n'
        return source

    def add_test_case(self, identifier, code, expected_output):
        """Add a def test_ function with code and comparison logic."""
        assert identifier.isidentifier(), 'must be a valid python identifier'
        self.empty_line()
        src = inspect.getsource(test_identifier)
        src = src.replace('identifier', identifier, 1)
        indented_code = textwrap.indent(code, '    ')
        src = src.replace('(capsys):', '(capsys):\n' + indented_code, 1)
        if expected_output:
            src = src.replace('<<<replaced>>>', expected_output, 1)
        else:
            src = self.remove_output_check(src)
        self.lines.append(src)
