"""Check test_example2.md includes same code as doc/test_example2.py."""

import phmdoctest.tool
import verify


def test_markdown_wrapper_test_example2():
    """Fenced code block in test_example2.md == file test_example2.py."""
    with open('doc/test_example2.py', 'r', encoding='utf-8') as f:
        want = f.read()
    blocks = phmdoctest.tool.fenced_code_blocks('doc/test_example2.md')
    assert len(blocks) == 1
    got = blocks[0]
    verify.a_and_b_are_the_same(a=want, b=got)
