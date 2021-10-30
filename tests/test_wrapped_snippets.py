"""pytest test cases to check markdown wrapped files."""
from pathlib import Path

import phmdoctest.tool


def check_first_block(markdown_path, contents_path, checker_function):
    """Check that first FCB in Markdown is same as the file contents."""
    want = Path(contents_path).read_text(encoding="utf-8")
    blocks = phmdoctest.tool.fenced_code_blocks(markdown_path)
    got = blocks[0]
    checker_function(a=want, b=got)


def test_test_example2_py_md(checker):
    """The copy of .py file in fenced code block is the same as the file."""
    check_first_block(
        markdown_path="doc/test_example2_py.md",
        contents_path="doc/test_example2.py",
        checker_function=checker,
    )


def test_test_setup_py_md(checker):
    """The copy of .py file in fenced code block is the same as the file."""
    check_first_block(
        markdown_path="doc/test_setup_py.md",
        contents_path="doc/test_setup.py",
        checker_function=checker,
    )


# directive1 files


def test_directive1_raw_md(checker):
    """The copy of .md file in fenced code block is the same as the file."""
    check_first_block(
        markdown_path="doc/directive1_raw.md",
        contents_path="doc/directive1.md",
        checker_function=checker,
    )


def test_directive1_report_txt_md(checker):
    """The copy of .md file in fenced code block is the same as the file."""
    check_first_block(
        markdown_path="doc/directive1_report_txt.md",
        contents_path="doc/directive1_report.txt",
        checker_function=checker,
    )


def test_test_directive1_py_md(checker):
    """The copy of .md file in fenced code block is the same as the file."""
    check_first_block(
        markdown_path="doc/test_directive1_py.md",
        contents_path="doc/test_directive1.py",
        checker_function=checker,
    )


# directive2 files


def test_directive2_raw_md(checker):
    """The copy of .md file in fenced code block is the same as the file."""
    check_first_block(
        markdown_path="doc/directive2_raw.md",
        contents_path="doc/directive2.md",
        checker_function=checker,
    )


def test_directive2_report_txt_md(checker):
    """The copy of .md file in fenced code block is the same as the file."""
    check_first_block(
        markdown_path="doc/directive2_report_txt.md",
        contents_path="doc/directive2_report.txt",
        checker_function=checker,
    )


def test_test_directive2_py_md(checker):
    """The copy of .md file in fenced code block is the same as the file."""
    check_first_block(
        markdown_path="doc/test_directive2_py.md",
        contents_path="doc/test_directive2.py",
        checker_function=checker,
    )


# directive3 files


def test_directive3_raw_md(checker):
    """The copy of .md file in fenced code block is the same as the file."""
    check_first_block(
        markdown_path="doc/directive3_raw.md",
        contents_path="doc/directive3.md",
        checker_function=checker,
    )


def test_directive3_report_txt_md(checker):
    """The copy of .md file in fenced code block is the same as the file."""
    check_first_block(
        markdown_path="doc/directive3_report_txt.md",
        contents_path="doc/directive3_report.txt",
        checker_function=checker,
    )


def test_test_directive3_py_md(checker):
    """The copy of .md file in fenced code block is the same as the file."""
    check_first_block(
        markdown_path="doc/test_directive3_py.md",
        contents_path="doc/test_directive3.py",
        checker_function=checker,
    )


def test_test_setup_doctest_py_md(checker):
    """The copy of .py file in fenced code block is the same as the file."""
    check_first_block(
        markdown_path="doc/test_setup_doctest_py.md",
        contents_path="doc/test_setup_doctest.py",
        checker_function=checker,
    )


def test_test_inline_example_py_md(checker):
    """The copy of .py file in fenced code block is the same as the file."""
    check_first_block(
        markdown_path="doc/test_inline_example_py.md",
        contents_path="doc/test_inline_example.py",
        checker_function=checker,
    )


def test_test_project_test_py_md(checker):
    """The copy of .py file in fenced code block is the same as the file."""
    check_first_block(
        markdown_path="doc/project_test_py.md",
        contents_path="tests/project_test.py",
        checker_function=checker,
    )
