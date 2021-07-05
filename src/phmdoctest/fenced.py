"""Fenced code block data structures."""

from enum import Enum

from typing import List, Optional

import commonmark.node  # type: ignore
import phmdoctest.direct


class Role(Enum):
    """Role that markdown fenced code block plays in testing."""

    UNKNOWN = "--"
    CODE = "code"
    OUTPUT = "output"
    SESSION = "session"
    SKIP_CODE = "skip-code"
    SKIP_OUTPUT = "skip-output"
    SKIP_SESSION = "skip-session"
    SETUP = "setup"
    TEARDOWN = "teardown"
    DEL_CODE = "del-code"
    DEL_OUTPUT = "del-output"


class FencedBlock:
    """Augment selected fields from commonmark node."""

    def __init__(self, node: commonmark.node.Node) -> None:
        """Extract fields from commonmark fenced code block node."""
        self.type = node.info
        self.line = node.sourcepos[0][0] + 1
        self.role = Role.UNKNOWN
        self.contents = node.literal  # type: str
        self.output = None  # type: Optional["FencedBlock"]
        self.patterns = list()  # type: List[str]
        self.directives = phmdoctest.direct.get_directives(node)

    def __str__(self) -> str:
        return "FencedBlock(role={}, line={})".format(self.role.value, self.line)

    def set(self, role: Role) -> None:
        """Set the role for the fenced code block in subsequent testing."""
        self.role = role

    def add_pattern(self, pattern: str) -> None:
        """Add the TEXT value that identified the block"""
        self.patterns.append(pattern)

    def set_link_to_output(self, fenced_block: "FencedBlock") -> None:
        """Save a reference to the code block's output block."""
        assert self.role == Role.CODE, "only allowed to be code"
        assert fenced_block.role == Role.OUTPUT, "only allowed to be output"
        self.output = fenced_block

    def get_output_contents(self) -> str:
        """Return contents of linked output block or empty str if no link."""
        # First, check if the block has an output block.
        # Then, check the role of the output block to make sure it
        # hasn't been changed to SKIP_OUTPUT (by a skip directive placed
        # on the output block).
        if self.output and self.output.role == Role.OUTPUT:
            return self.output.contents
        else:
            return ""

    def skip(self, pattern: str = "") -> None:
        """Skip an already designated code block. Re-skip is OK.

        pattern is the TEXT value that identified the block.
        """
        if self.role == Role.CODE:
            self.set(Role.SKIP_CODE)
            if self.output:
                self.output.set(Role.SKIP_OUTPUT)
        elif self.role == Role.SESSION:
            self.set(Role.SKIP_SESSION)
        elif self.role == Role.OUTPUT:
            self.set(Role.SKIP_OUTPUT)
        else:
            # It is not OK to call skip on a block that is not
            # code, session, or output (from above tests)
            # unless it is already skipped as tested in the any()
            # statement here.
            if not any(
                [
                    self.role == Role.SKIP_CODE,
                    self.role == Role.SKIP_SESSION,
                    self.role == Role.SKIP_OUTPUT,
                ]
            ):
                assert False, "cannot skip a block with {}.".format(self.role)
        if pattern:
            self.patterns.append(pattern)

    def has_directive(self, marker: phmdoctest.direct.Marker) -> bool:
        """Return true if marker is the type of one of the directives."""
        for directive in self.directives:
            if directive.type == marker:
                return True
        return False


def convert_nodes(nodes: List[commonmark.node.Node]) -> List[FencedBlock]:
    """Create FencedBlock objects from commonmark fenced code block nodes."""
    blocks = []
    for node in nodes:
        blocks.append(FencedBlock(node))
    return blocks
