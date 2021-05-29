"""Find phmdoctest Directives in HTML comment Nodes."""
from collections import namedtuple
from enum import Enum
from typing import List, Optional

import commonmark.node  # type: ignore


class Marker(Enum):
    """HTML comment before a fenced code block."""

    SKIP = "<!--phmdoctest-skip-->"
    PYTEST_SKIP = "<!--phmdoctest-mark.skip-->"
    PYTEST_SKIPIF = "<!--phmdoctest-mark.skipif<3."  # No space, no "-->".
    LABEL = "<!--phmdoctest-label "  # Note trailing space, no "-->".
    SETUP = "<!--phmdoctest-setup-->"
    TEARDOWN = "<!--phmdoctest-teardown-->"
    SHARE_NAMES = "<!--phmdoctest-share-names-->"
    CLEAR_NAMES = "<!--phmdoctest-clear-names-->"


Directive = namedtuple(
    "Directive",
    [
        "type",  # Enum
        "value",
        "line",
        "literal",  # commonmark.node.Node literal value
    ],
)
"""Information from a phmdoctest HTML comment marker."""


def extract_value(literal: str, marker: Marker) -> str:
    """Strip both ends of the HTML comment, return what's left."""
    # The marker's Enum.value string matches the first part of the
    # HTML comment literal. Keep the rest of the literal
    # after the space, but not the '->>'.
    # Remove leading/trailing whitespace.
    text = literal[len(marker.value) :]
    text = text.replace("-->", "")
    return text.strip()


def find_one_directive(node: commonmark.node) -> Optional[Directive]:
    """Get a phmdoctest Directive instance from a HTML comment node."""
    assert node.t == "html_block", "Must be HTML"
    assert node.html_block_type == 2, "Must be a HTML comment"
    for marker in Marker:
        if node.literal == marker.value:
            return Directive(
                type=marker, value="", line=node.sourcepos[0][0], literal=node.literal
            )
        elif node.literal.startswith(Marker.LABEL.value):
            # The label marker carries a value.
            return Directive(
                type=Marker.LABEL,
                value=extract_value(node.literal, Marker.LABEL),
                line=node.sourcepos[0][0],
                literal=node.literal,
            )
        elif node.literal.startswith(Marker.PYTEST_SKIPIF.value):
            return Directive(
                type=Marker.PYTEST_SKIPIF,
                value=extract_value(node.literal, Marker.PYTEST_SKIPIF),
                line=node.sourcepos[0][0],
                literal=node.literal,
            )
    return None


def get_directives(node: commonmark.node.Node) -> List[Directive]:
    """Scan adjacent preceding HTML comments for phmdoctest markers."""

    # The scan looks backward in the document tree from the current node
    # and continues until a non HTML comment node is encountered.
    # Each HTML comment is checked to see if it is a phmdoctest
    # directive.  If it is, a Directive namedtuple is assembled
    # and added to a list.
    # This list is reversed so that the Directive(s) are in file order.
    # If no phmdoctest directives are found an empty list is returned.
    directives = list()
    loop_count = 0
    prev = node.prv
    stop = False
    while prev and not stop:
        # Silently abort the loop after too many iterations.
        loop_count += 1
        if loop_count > 100:
            break
        if prev.t == "html_block" and prev.html_block_type == 2:
            one = find_one_directive(prev)
            if one:
                directives.append(one)
            prev = prev.prv
        else:
            # I originally had a break here, but coverage 5.2 with C extension
            # never saw a False outcome of the if prev.t... conditional.
            stop = True
    return list(reversed(directives))
