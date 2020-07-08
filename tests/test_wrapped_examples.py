"""pytest test cases to check markdown wrapped python files."""

import phmdoctest.tool
import verify


def test_test_example2_py_md():
    """The copy of .py file in fenced code block is the same as the file."""
    with open('doc/test_example2.py', 'r', encoding='utf-8') as f:
        want = f.read()
    blocks = phmdoctest.tool.fenced_code_blocks('doc/test_example2_py.md')
    got = blocks[0]
    verify.a_and_b_are_the_same(a=want, b=got)


def test_test_setup_py_md():
    """The copy of .py file in fenced code block is the same as the file."""
    with open('doc/test_setup.py', 'r', encoding='utf-8') as f:
        want = f.read()
    blocks = phmdoctest.tool.fenced_code_blocks('doc/test_setup_py.md')
    got = blocks[0]
    verify.a_and_b_are_the_same(a=want, b=got)


def test_test_setup_doctest_py_md():
    """The copy of .py file in fenced code block is the same as the file."""
    with open('doc/test_setup_doctest.py', 'r', encoding='utf-8') as f:
        want = f.read()
    blocks = phmdoctest.tool.fenced_code_blocks(
        'doc/test_setup_doctest_py.md')
    got = blocks[0]
    verify.a_and_b_are_the_same(a=want, b=got)
