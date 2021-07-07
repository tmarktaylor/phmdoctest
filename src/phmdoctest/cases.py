"""Compose the pytest test case file."""
import inspect
import textwrap
from io import StringIO
import itertools
from typing import List, Iterator, Optional, Set

import click

from phmdoctest.entryargs import Args
from phmdoctest.fenced import Role, FencedBlock
from phmdoctest.direct import Marker
from phmdoctest import functions
from phmdoctest.inline import apply_inline_commands


def get_block_with_role(blocks: List[FencedBlock], role: Role) -> Optional[FencedBlock]:
    """Get first occurrence of block with the caller's role."""
    for block in blocks:
        if block.role == role:
            return block
    return None


def get_label_name(block: FencedBlock) -> str:
    """Get block's first label directive value, if it has one."""
    label = ""  # return empty string if there is no label directive
    for directive in block.directives:
        if directive.type == Marker.LABEL:
            label = directive.value
            if not label.isidentifier():
                lines = [
                    "<!--phmdoctest-label {}-->".format(label),
                    (
                        "at markdown file line {} ".format(directive.line)
                        + "must be a valid python identifier."
                    ),
                ]
                message = "\n".join(lines)
                raise click.ClickException(message)
    return label


def make_label_unique(label: str, line_num: int, used: Set[str]) -> str:
    """Add suffix to label if it has already been used. Keep track of uses."""
    if label:
        if label in used:
            label = "{}_{}".format(label, line_num)
        used.add(label)
    return label


def get_skipif_minor_number(block: FencedBlock) -> int:
    """Get block's first skipif minor numeric value, if it exists."""
    # Return zero if there is no such directive.
    minor_number = 0
    for directive in block.directives:
        if directive.type == Marker.PYTEST_SKIPIF:
            value = directive.value
            try:
                minor_number = int(value, 10)
                if minor_number < 0:
                    raise ValueError("phmdoctest- must be >= 0")
            except ValueError:
                lines = [
                    Marker.PYTEST_SKIPIF.value + "{}-->".format(value),
                    (
                        "at markdown file line {} ".format(directive.line)
                        + "must be a decimal number and >= zero."
                    ),
                ]
                message = "\n".join(lines)
                raise click.ClickException(message)
    return minor_number


def needs_sys(blocks: List[FencedBlock]) -> bool:
    """See if import sys is needed for mark.skipif expression."""
    for block in blocks:
        # Look for the phmdoctest-mark.skipif<3. directive on code blocks only.
        # If one is found this means import sys is required in the test file.
        if block.role == Role.CODE:
            if get_skipif_minor_number(block):
                return True  # import sys is needed
    return False


def has_pytest_mark_decorator(blocks: List[FencedBlock]) -> bool:
    """True if any code blocks generate @pytest.mark.* decorators."""
    code_blocks = [b for b in blocks if b.role == Role.CODE]
    # Return True if any calls to add_pytest_mark_decorator() write a line
    # to the StringIO file.
    pytest_marks_lines = StringIO()
    for block in code_blocks:
        add_pytest_mark_decorator(pytest_marks_lines, block)
    return len(pytest_marks_lines.getvalue()) > 0


def compose_import_lines(
    blocks: List[FencedBlock],
    needs_setup_or_teardown: bool,
    needs_output_checking: bool,
) -> str:
    """Generate import lines for the test file."""
    needs_fixture = needs_setup_or_teardown or any_names_directives(blocks)
    needs_import_pytest = has_pytest_mark_decorator(blocks)
    lines = list()
    if needs_sys(blocks):
        lines.append("import sys\n\n")
    if needs_fixture or needs_import_pytest:
        lines.append("import pytest\n\n")
    if needs_fixture:
        lines.append("from phmdoctest.fixture import managenamespace\n")
    if needs_output_checking:
        lines.append("from phmdoctest.functions import _phm_compare_exact\n")
    return "".join(lines)


def setup_and_teardown_fixture(
    setup_block: Optional[FencedBlock],
    teardown_block: Optional[FencedBlock],
    setup_doctest: bool,
) -> str:
    """Add functions to handle setup, teardown and setup for doctest."""
    assert setup_block or teardown_block, "Must get at least one."
    src = "\n\n"
    if setup_doctest:
        src += inspect.getsource(functions._phm_setup_doctest_teardown)
    else:
        src += inspect.getsource(functions._phm_setup_teardown)
    # do teardown code replace first so not searching through setup code.
    if teardown_block:
        comment = "# teardown code line {}.\n".format(teardown_block.line)
        code, _ = apply_inline_commands(teardown_block.contents)
        full_code = comment + code
        indented_code = textwrap.indent(full_code, "    ")
        src = src.replace("    # <teardown code here>\n", indented_code, 1)

    if setup_block:
        comment = "# setup code line {}.\n".format(setup_block.line)
        code, _ = apply_inline_commands((setup_block.contents))
        full_code = comment + code
        indented_code = textwrap.indent(full_code, "    ")
        src = src.replace("    # <setup code here>\n", indented_code, 1)

    src += "\n\n"
    markspec = 'pytestmark = pytest.mark.usefixtures("{}")\n'
    if setup_doctest:
        src += markspec.format("_phm_setup_doctest_teardown")
        # Add in more fixtures.
        # 1. Populate the doctest namespace with values from the setup code.
        # 2. session_00000 makes the names visible to the doctests.
        src += "\n\n"
        src += functions.populate_doctest_namespace_str
        src += "\n\n"
        src += inspect.getsource(functions.session_00000)
    else:
        src += markspec.format("_phm_setup_teardown")

    return src


def call_namespace_manager(block: FencedBlock) -> str:
    """Return a code line if there is a share-names or clear-names directive.

    If the block has both directives, ignore the clear-names directive.
    If the block has neither directive return empty string.
    """
    if block.has_directive(Marker.SHARE_NAMES):
        return '    managenamespace(operation="update", additions=locals())\n'
    elif block.has_directive(Marker.CLEAR_NAMES):
        return '    managenamespace(operation="clear")\n'
    else:
        return ""


def has_names_directive(block: FencedBlock) -> bool:
    """Does the code block have a share-names or clear-names directive."""
    assert block.role == Role.CODE, "must be a Python code block."
    return block.has_directive(Marker.SHARE_NAMES) or block.has_directive(
        Marker.CLEAR_NAMES
    )


def any_names_directives(blocks: List[FencedBlock]) -> bool:
    """Return True if the managenamespace fixture is needed to share names."""
    for block in blocks:
        if block.role == Role.CODE:
            if has_names_directive(block):
                return True
    return False


def add_pytest_mark_decorator(writer: StringIO, block: FencedBlock) -> None:
    """If block has a -mark. directive add the pytest.mark decorator.

    If the block has a mark.skip directive, write pytest.mark.skip.
    If the block has a mark.skipif directive, write pytest.mark.skipif.
    """
    for directive in block.directives:
        if directive.type == Marker.PYTEST_SKIP:
            writer.write("\n")
            writer.write("@pytest.mark.skip()")

    mark_format = (
        "@pytest.mark.skipif(sys.version_info < (3, {0}), "
        'reason="requires >=py3.{0}")'
    )
    minor_number = get_skipif_minor_number(block)
    if minor_number:
        writer.write("\n")
        writer.write(mark_format.format(minor_number))


def test_case(block: FencedBlock, used_names: Set[str]) -> str:
    """Add a def test_ function with code and comparison logic.

    Generate a function that has code as its body and
    includes logic to capture and compare the printed output.
    The function is named to be collected by pytest as a test case.
    """
    assert block.role == Role.CODE, "must be a Python code block."
    text = StringIO()
    # The function_name comes from a label directive or is
    # generated from line numbers of the code and output blocks.
    function_name = make_label_unique(get_label_name(block), block.line, used_names)
    if not function_name:
        code_identifier = "test_code_" + str(block.line)
        output_identifier = ""
        if block.output:
            output_identifier = "_output_" + str(block.output.line)
        function_name = code_identifier + output_identifier
    code, num_commented_out_sections = apply_inline_commands(block.contents)
    if num_commented_out_sections:
        function_name += "_{}".format(num_commented_out_sections)
    expected_output = block.get_output_contents()
    # A 'managed' block has the share-names or clear-names directive.
    managed = has_names_directive(block)
    text.write("\n")
    if expected_output:
        if managed:
            src = inspect.getsource(functions.test_managed_code_and_output)
            src = src.replace("test_managed_code_and_output", function_name, 1)
            src += call_namespace_manager(block)
        else:
            src = inspect.getsource(functions.test_code_and_output)
            src = src.replace("test_code_and_output", function_name, 1)

        # indent contents of code block and place at <put code here>.
        indented_code = textwrap.indent(code, "    ")
        src = src.replace("    # <put code here>\n", indented_code, 1)
        src = src.replace("<<<replaced>>>", expected_output, 1)
        text.write(src)
    else:
        # no expected output to check-
        if managed:
            src = inspect.getsource(functions.test_managed_code_only)
            src = src.replace("test_managed_code_only", function_name, 1)
            src += call_namespace_manager(block)
        else:
            src = inspect.getsource(functions.test_code_only)
            src = src.replace("test_code_only", function_name, 1)
        src = src.replace("    pass\n", "\n    # Caution- no assertions.\n")

        # indent contents of code block and place at <put code here>.
        indented_code = textwrap.indent(code, "    ")
        src = src.replace("    # <put code here>\n", indented_code, 1)
        text.write(src)

    return text.getvalue()


def interactive_session(
    block: FencedBlock, session_counter: Iterator[int], used_names: Set[str]
) -> str:
    """Add a do nothing function with doctest session as its docstring.

    Generate the function that has the session as
    its docstring and a function name that prevents it from being
    collected as a test case.
    Run pytest with --doctest-modules to run doctest on the session.
    """
    assert block.role == Role.SESSION, "must be interactive session block."

    # The function_name comes from a label directive or is
    # generated from line number of the interactive session block.
    function_name = make_label_unique(get_label_name(block), block.line, used_names)
    if not function_name:
        sequence_number = next(session_counter)
        sequence_string = format(sequence_number, "05d")
        function_def = "def session_{}_line_{}():\n".format(sequence_string, block.line)
    else:
        function_def = "def " + function_name + "():\n"

    indented_session = textwrap.indent(block.contents, "    ")
    text = StringIO()
    text.write("\n")
    text.write(function_def)
    text.write('    r"""\n')
    text.write(indented_session)
    text.write('    """\n')
    return text.getvalue()


def build_test_cases(args: Args, blocks: List[FencedBlock]) -> str:
    """Generate test code from the Python fenced code blocks."""

    # Keeps track of test case function names set by label directives.
    used_names = set()  # type: Set[str]

    # Sequence number to order sessions.
    session_counter = itertools.count(1)

    # collect the generated code in a single string
    # repr escapes back slashes from win filesystem paths
    # so it can be part of the generated test module docstring.
    quoted_markdown_path = repr(click.format_filename(args.markdown_file))
    markdown_path = quoted_markdown_path[1:-1]
    docstring_text = "pytest file built from {}".format(markdown_path)
    generated = StringIO()
    generated.write('"""' + docstring_text + '"""\n')

    setup_block = get_block_with_role(blocks, Role.SETUP)
    teardown_block = get_block_with_role(blocks, Role.TEARDOWN)

    needs_setup_or_teardown = (setup_block or teardown_block) is not None
    needs_output_check = get_block_with_role(blocks, Role.OUTPUT) is not None

    generated.write(
        compose_import_lines(blocks, needs_setup_or_teardown, needs_output_check)
    )

    # fixture to handle setup and/or teardown and code for setup doctest
    if needs_setup_or_teardown:
        generated.write(
            setup_and_teardown_fixture(
                setup_block=setup_block,
                teardown_block=teardown_block,
                setup_doctest=args.setup_doctest,
            )
        )

    number_of_test_cases = 0
    for block in blocks:
        if block.role == Role.CODE:
            generated.write("\n")
            add_pytest_mark_decorator(generated, block)
            generated.write(test_case(block, used_names))
            number_of_test_cases += 1

        elif block.role == Role.SESSION:
            generated.write("\n")
            generated.write(interactive_session(block, session_counter, used_names))
            number_of_test_cases += 1

    if number_of_test_cases == 0:
        if args.fail_nocode:
            nocode_func = functions.test_nothing_fails
        else:
            nocode_func = functions.test_nothing_passes
        generated.write("\n\n")
        generated.write(inspect.getsource(nocode_func))
    return generated.getvalue()
