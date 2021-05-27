"""Assign role in test file generation to fenced code blocks."""

from typing import List, Optional

import click

from phmdoctest.direct import Marker
from phmdoctest.entryargs import Args
from phmdoctest.fenced import Role, FencedBlock


PYTHON_FLAVORS = ["python", "py3", "python3"]
"""Python fenced code blocks info string will start with one of these."""


def identify_code_output_session_blocks(blocks: List[FencedBlock]) -> None:
    """
    Designate which blocks are Python or session and guess which are output.

    The block.type is a copy of the Markdown fenced code block info_string.
    This string may start with the language intended for syntax coloring.
    A block is an output block if it has an empty markdown info field
    and follows a designated python code block.

    A block is a session block if the info_string starts with 'py'
    and the first line of the block starts with the session prompt '>>> '.
    """
    for block in blocks:
        for flavor in PYTHON_FLAVORS:
            if block.type.startswith(flavor):
                block.set(Role.CODE)
        if block.contents.startswith(">>> ") and block.type.startswith("py"):
            block.set(Role.SESSION)

    # When we find an output block we update the preceding
    # code block with a link to it.
    previous_block = None
    for block in blocks:
        if previous_block is not None:
            if not block.type and previous_block.role == Role.CODE:
                block.set(Role.OUTPUT)
                previous_block.set_link_to_output(block)
        previous_block = block
    # If we didn't find an output block for a code block
    # it can still be run, but there will be no comparison
    # to expected output.  If assertions are needed, they can
    # be added to the code block.


def del_problem_blocks(blocks: List[FencedBlock]) -> None:
    """Re-designate blocks that can't be used."""
    # Rather than asserting and blowing up the caller, just set the
    # blocks we can't deal with aside for later discovery in the report.
    empty_blocks = [b for b in blocks if not b.contents]
    for block in empty_blocks:
        if block.role == Role.CODE:
            block.set(Role.DEL_CODE)
            if block.output:
                block.output.set(Role.DEL_OUTPUT)
        elif block.role == Role.OUTPUT:
            block.set(Role.DEL_OUTPUT)


def apply_skips(args: Args, blocks: List[FencedBlock]) -> None:
    """Designate Python code/session blocks that are exempt from testing."""
    # Do skip requests from the command line.
    for pattern in args.skips:
        found = findall(pattern, blocks)
        for block in found:
            block.skip(pattern)
    # Do skip requests marked as a skip directive on the block.
    for block in blocks:
        for directive in block.directives:
            if directive.type == Marker.SKIP:
                block.skip()
        # If the code block has an output block check if it has a skip
        # directive.
        if block.output:
            for directive in block.output.directives:
                if directive.type == Marker.SKIP:
                    block.output.skip()


def findall(pattern: str, blocks: List[FencedBlock]) -> List[FencedBlock]:
    """Return list of blocks that contain search pattern."""
    found = []  # type: List[FencedBlock]
    if pattern == "FIRST":
        found.append(blocks[0])
    elif pattern == "LAST":
        found.append(blocks[-1])
    elif pattern == "SECOND" and len(blocks) > 1:
        found.append(blocks[1])
    if pattern not in ["FIRST", "SECOND", "LAST"]:
        for block in blocks:
            if block.contents.find(pattern) > -1:
                found.append(block)
    return found


def find_only_one_by_pattern(
    pattern: str, blocks: List[FencedBlock], command_line_option_name: str
) -> Optional[FencedBlock]:
    """Find a single block containing pattern, die if more matches."""
    matches = findall(pattern, blocks)
    if not matches:
        return None
    if len(matches) == 1:
        return matches[0]
    # More than one block matched the search pattern provided
    # by a command line option.  Raise an exception.
    line_numbers = [str(b.line) for b in matches]
    message = (
        "More than one block matched command line {}.\n"
        "Only one match is allowed.\n"
        "The matching blocks are at line numbers {}."
    ).format(command_line_option_name, ", ".join(line_numbers))
    raise click.ClickException(message)


def find_only_one_by_marker(
    blocks: List[FencedBlock], marker: Marker
) -> Optional[FencedBlock]:
    """Find 1 block that has directive indicated by Marker, die if more."""
    found = []
    for block in blocks:
        for directive in block.directives:
            if directive.type == marker:
                found.append(block)
    if not found:
        return None
    if len(found) == 1:
        return found[0]
    # More than one block has the directive
    line_numbers = [str(b.line) for b in found]
    message = (
        "More than 1 block has directive {}.\nThe blocks are at line numbers {}."
    ).format(marker.value, ", ".join(line_numbers))
    raise click.ClickException(message)


def check_for_error(block1: FencedBlock, block2: FencedBlock, name: str) -> None:
    """Raise an exception if the two blocks are different."""
    if block1.line != block2.line:
        message = (
            "More than one block is designated as {}.\n"
            "The blocks are at line numbers {}, {}."
        ).format(name, block1.line, block2.line)
        raise click.ClickException(message)


def find_and_designate_setup(pattern: str, blocks: List[FencedBlock]) -> None:
    """Find and designate Python code block as setup.

    Search the contents of each block for the pattern.
    Raise an exception if more than one block matches the search.
    Repeat the search this time looking for blocks with a
    SETUP directive.
    Raise an exception if more than one block has a SETUP directive.
    If we found a block by both methods (search pattern and directive),
    we can continue if they are the same block.
    If exactly one code block is identified and it
    has not been changed from Role.CODE set it to the Role.SETUP.
    Setup code can't have an output block since there is
    no way to generate code for it.
    If there is one, change its role to DEL_OUTPUT so it will show up
    in the report.
    """
    if pattern is None:
        match = None
    else:
        match = find_only_one_by_pattern(pattern, blocks, "--setup or -u")
    marked = find_only_one_by_marker(blocks, Marker.SETUP)
    if match is not None and marked is not None:
        check_for_error(match, marked, "setup")
    block = match or marked
    if block and block.role == Role.CODE:
        block.set(Role.SETUP)
        if pattern is not None:
            block.add_pattern(pattern)
        if block.output is not None:
            block.output.set(Role.DEL_OUTPUT)


def find_and_designate_teardown(pattern: str, blocks: List[FencedBlock]) -> None:
    """Find and designate Python code block as teardown.

    Search the contents of each block for the pattern.
    Raise an exception if more than one block matches the search.
    Repeat the search this time looking for blocks with a
    TEARDOWN directive.
    Raise an exception if more than one block has a TEARDOWN directive.
    If we found a block by both methods (search pattern and directive),
    we can continue if they are the same block.
    If exactly one code block is identified and it
    has not been changed from Role.CODE set it to the Role.TEARDOWN.
    Teardown code can't have an output block since there is
    no way to generate code for it.
    If there is one, change its role to DEL_OUTPUT so it will show up
    in the report.
    """
    if pattern is None:
        match = None
    else:
        match = find_only_one_by_pattern(pattern, blocks, "--teardown or -d")
    marked = find_only_one_by_marker(blocks, Marker.TEARDOWN)
    if match is not None and marked is not None:
        check_for_error(match, marked, "teardown")
    block = match or marked
    if block and block.role == Role.CODE:
        if pattern is not None:
            block.add_pattern(pattern)
        block.set(Role.TEARDOWN)
        if block.output is not None:
            block.output.set(Role.DEL_OUTPUT)
