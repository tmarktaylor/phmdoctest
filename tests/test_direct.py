"""Test HTML comment directives."""
import pytest

import phmdoctest.direct
import phmdoctest.tool


fenced_block_nodes = []
"""Fenced code blocks from .md file as commonmark.node.Node structures."""


def setup_module():
    """Collect Markdown fenced code block Node structures from direct.md.

    The test cases here must be run in order because they
    consume items from the list readme_blocks.

    This means using a pytest -k KEY more specific than
    "-k test_direct" risks taking the wrong block from the
    iterator readme_blocks causing all subsequent test_readme
    test case to fail.
    """
    # test cases below iterate through the blocks.
    global fenced_block_nodes
    with open("tests/direct.md", "r", encoding="utf-8") as fp:
        nodes = phmdoctest.tool.fenced_block_nodes(fp)
        fenced_block_nodes = iter(nodes)


def fenced_block_node_directives():
    """Get the directives from the next node in the .md file."""
    node = next(fenced_block_nodes)
    return phmdoctest.direct.get_directives(node)


def test_skip_before_comment():
    directives = fenced_block_node_directives()
    assert len(directives) == 1
    marker = directives[0]
    assert marker.type == phmdoctest.direct.Marker.SKIP
    assert marker.value == ""
    assert marker.line == 1
    assert marker.literal == "<!--phmdoctest-skip-->"


def test_no_directive_on_output_block():
    directives = fenced_block_node_directives()
    assert len(directives) == 0


def test_comment_skip_on_session():
    directives = fenced_block_node_directives()
    assert len(directives) == 1
    marker = directives[0]
    assert marker.type == phmdoctest.direct.Marker.SKIP
    assert marker.value == ""
    assert marker.line == 23
    assert marker.literal == "<!--phmdoctest-skip-->"


def test_label_on_session():
    directives = fenced_block_node_directives()
    assert len(directives) == 3
    marker0 = directives[0]
    assert marker0.type == phmdoctest.direct.Marker.LABEL
    assert marker0.value == "coffee_session"
    assert marker0.line == 33
    assert marker0.literal == "<!--phmdoctest-label coffee_session -->"

    marker1 = directives[1]
    assert marker1.type == phmdoctest.direct.Marker.LABEL
    assert marker1.value == "NO_TRAILING_SPACE"
    assert marker1.line == 35
    assert marker1.literal == "<!--phmdoctest-label NO_TRAILING_SPACE-->"

    marker2 = directives[2]
    assert marker2.type == phmdoctest.direct.Marker.LABEL
    assert marker2.value == "EXTRA_SPACES"
    assert marker2.line == 36
    assert marker2.literal == "<!--phmdoctest-label   EXTRA_SPACES  -->"


# Note- There is no limit to number of blank lines
# between the directive and the fenced code block.
def test_blank_lines_below_marker():
    """Empty lines between direct and fenced code block are OK."""
    # This type of usage should be avoided.
    directives = fenced_block_node_directives()
    assert len(directives) == 1
    marker = directives[0]
    assert marker.type == phmdoctest.direct.Marker.CLEAR_NAMES
    assert marker.value == ""
    assert marker.line == 47
    assert marker.literal == "<!--phmdoctest-clear-names-->"


def test_not_found_text_below_marker():
    """The comment must be placed immediately before the fenced code block."""
    # There is some text between the comment and the fenced code block.
    directives = fenced_block_node_directives()
    assert len(directives) == 0


def test_the_rest_mixed_with_comments():
    directives = fenced_block_node_directives()
    assert len(directives) == 3
    marker0 = directives[0]
    assert marker0.type == phmdoctest.direct.Marker.SETUP
    assert marker0.value == ""
    assert marker0.line == 70
    assert marker0.literal == "<!--phmdoctest-setup-->"

    marker1 = directives[1]
    assert marker1.type == phmdoctest.direct.Marker.TEARDOWN
    assert marker1.value == ""
    assert marker1.line == 72
    assert marker1.literal == "<!--phmdoctest-teardown-->"

    marker2 = directives[2]
    assert marker2.type == phmdoctest.direct.Marker.SHARE_NAMES
    assert marker2.value == ""
    assert marker2.line == 73
    assert marker2.literal == "<!--phmdoctest-share-names-->"


def test_comment_skip_on_output():
    # The block has no info_string
    directives = fenced_block_node_directives()
    assert len(directives) == 1
    marker = directives[0]
    assert marker.type == phmdoctest.direct.Marker.SKIP
    assert marker.value == ""
    assert marker.line == 83
    assert marker.literal == "<!--phmdoctest-skip-->"


def test_mark_skip():
    directives = fenced_block_node_directives()
    assert len(directives) == 1
    marker = directives[0]
    assert marker.type == phmdoctest.direct.Marker.PYTEST_SKIP
    assert marker.value == ""
    assert marker.line == 90
    assert marker.literal == "<!--phmdoctest-mark.skip-->"


def test_skipif_sharenames():
    directives = fenced_block_node_directives()
    assert len(directives) == 2
    marker = directives[0]
    assert marker.type == phmdoctest.direct.Marker.PYTEST_SKIPIF
    assert marker.value == "8"
    assert marker.line == 102
    assert marker.literal == "<!--phmdoctest-mark.skipif<3.8-->"
    marker = directives[1]
    assert marker.type == phmdoctest.direct.Marker.SHARE_NAMES
    assert marker.value == ""
    assert marker.line == 103
    assert marker.literal == "<!--phmdoctest-share-names-->"


def test_skip_plus_label():
    directives = fenced_block_node_directives()
    assert len(directives) == 3
    marker = directives[0]
    assert marker.type == phmdoctest.direct.Marker.SETUP
    assert marker.line == 112
    marker = directives[1]
    assert marker.type == phmdoctest.direct.Marker.LABEL
    assert marker.value == "my-hello-world"
    assert marker.line == 113
    assert marker.literal == "<!--phmdoctest-label my-hello-world-->"
    marker = directives[2]
    assert marker.type == phmdoctest.direct.Marker.SKIP
    assert marker.value == ""
    assert marker.line == 114
    assert marker.literal == "<!--phmdoctest-skip-->"

    # get directives from the output block
    directives = fenced_block_node_directives()
    assert len(directives) == 0


def test_skip_output_plus_label():
    # no directives expected on the Python code block
    directives = fenced_block_node_directives()
    assert len(directives) == 0
    # Get the output block  directives
    directives = fenced_block_node_directives()
    assert len(directives) == 2
    marker = directives[0]
    assert marker.type == phmdoctest.direct.Marker.LABEL
    assert marker.value == "my-hello-world-output"
    assert marker.line == 128
    assert marker.literal == "<!--phmdoctest-label my-hello-world-output-->"
    marker = directives[1]
    assert marker.type == phmdoctest.direct.Marker.SKIP
    assert marker.value == ""
    assert marker.line == 129
    assert marker.literal == "<!--phmdoctest-skip-->"


def test_consumed_all_nodes():
    """Verify no left over Nodes from direct.md"""
    with pytest.raises(StopIteration):
        _ = fenced_block_node_directives()


def test_circuit_breaker():
    """Patch FCB Node prev points to self to spin traversal logic."""
    with open("tests/direct.md", "r", encoding="utf-8") as fp:
        nodes = phmdoctest.tool.fenced_block_nodes(fp)
    n = nodes[0]
    # Rig node n so that its prv pointer points to node n (itself).
    # Rig node n so that it looks like an HTML comment.
    # These changes simulate an endless "while prev:" loop in
    # src/phmdoctest/direct.py::get_directives().
    # This triggers the loop_count > 100: break.
    self = n.nxt.prv
    n.prv = self
    n.t = "html_block"
    n.html_block_type = 2
    d = phmdoctest.direct.get_directives(n)
    assert len(d) == 0
