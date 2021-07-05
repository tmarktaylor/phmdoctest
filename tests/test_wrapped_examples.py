"""pytest test cases to check markdown wrapped files."""

import phmdoctest.tool
import verify


def check_first_block(markdown_path, contents_path):
    """Check that first FCB in Markdown is same as the file contents."""
    with open(contents_path, "r", encoding="utf-8") as f:
        want = f.read()
    blocks = phmdoctest.tool.fenced_code_blocks(markdown_path)
    got = blocks[0]
    verify.a_and_b_are_the_same(a=want, b=got)


def test_test_example2_py_md():
    """The copy of .py file in fenced code block is the same as the file."""
    check_first_block(
        markdown_path="doc/test_example2_py.md", contents_path="doc/test_example2.py"
    )


def test_test_setup_py_md():
    """The copy of .py file in fenced code block is the same as the file."""
    check_first_block(
        markdown_path="doc/test_setup_py.md", contents_path="doc/test_setup.py"
    )


# directive1 files


def test_directive1_raw_md():
    """The copy of .md file in fenced code block is the same as the file."""
    check_first_block(
        markdown_path="doc/directive1_raw.md", contents_path="doc/directive1.md"
    )


def test_directive1_report_txt_md():
    """The copy of .md file in fenced code block is the same as the file."""
    check_first_block(
        markdown_path="doc/directive1_report_txt.md",
        contents_path="doc/directive1_report.txt",
    )


def test_test_directive1_py_md():
    """The copy of .md file in fenced code block is the same as the file."""
    check_first_block(
        markdown_path="doc/test_directive1_py.md",
        contents_path="doc/test_directive1.py",
    )


# directive2 files


def test_directive2_raw_md():
    """The copy of .md file in fenced code block is the same as the file."""
    check_first_block(
        markdown_path="doc/directive2_raw.md", contents_path="doc/directive2.md"
    )


def test_directive2_report_txt_md():
    """The copy of .md file in fenced code block is the same as the file."""
    check_first_block(
        markdown_path="doc/directive2_report_txt.md",
        contents_path="doc/directive2_report.txt",
    )


def test_test_directive2_py_md():
    """The copy of .md file in fenced code block is the same as the file."""
    check_first_block(
        markdown_path="doc/test_directive2_py.md",
        contents_path="doc/test_directive2.py",
    )


# directive3 files


def test_directive3_raw_md():
    """The copy of .md file in fenced code block is the same as the file."""
    check_first_block(
        markdown_path="doc/directive3_raw.md", contents_path="doc/directive3.md"
    )


def test_directive3_report_txt_md():
    """The copy of .md file in fenced code block is the same as the file."""
    check_first_block(
        markdown_path="doc/directive3_report_txt.md",
        contents_path="doc/directive3_report.txt",
    )


def test_test_directive3_py_md():
    """The copy of .md file in fenced code block is the same as the file."""
    check_first_block(
        markdown_path="doc/test_directive3_py.md",
        contents_path="doc/test_directive3.py",
    )


def test_test_setup_doctest_py_md():
    """The copy of .py file in fenced code block is the same as the file."""
    check_first_block(
        markdown_path="doc/test_setup_doctest_py.md",
        contents_path="doc/test_setup_doctest.py",
    )


def test_test_inline_example_py_md():
    """The copy of .py file in fenced code block is the same as the file."""
    check_first_block(
        markdown_path="doc/test_inline_example_py.md",
        contents_path="doc/test_inline_example.py",
    )
