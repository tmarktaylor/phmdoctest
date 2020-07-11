"""Assign role in test file generation to fenced code blocks."""

from typing import List

import click

from phmdoctest.entryargs import Args
from phmdoctest.fenced import Role, FencedBlock


PYTHON_FLAVORS = ['python', 'py3', 'python3']
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
        if block.contents.startswith('>>> ') and block.type.startswith('py'):
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
    for pattern in args.skips:
        found = findall(pattern, blocks)
        for block in found:
            block.skip(pattern)


def findall(pattern: str, blocks: List[FencedBlock]) -> List[FencedBlock]:
    """Return list of blocks that contain search pattern."""
    found = []     # type: List[FencedBlock]
    if pattern == 'FIRST':
        found.append(blocks[0])
    elif pattern == 'LAST':
        found.append(blocks[-1])
    elif pattern == 'SECOND' and len(blocks) > 1:
        found.append(blocks[1])
    if pattern not in ['FIRST', 'SECOND', 'LAST']:
        for block in blocks:
            if block.contents.find(pattern) > -1:
                found.append(block)
    return found


def find_and_designate_setup_or_teardown(
        role: Role, pattern: str, blocks: List[FencedBlock]) -> None:
    """Find and designate Python code block as setup or teardown.

    Search the contents of each block for the pattern.
    Report an error if more than one block matches the search.
    If exactly one code block contains pattern and it
    has not been changed from Role.CODE set it to the caller's role.
    Setup and teardown code can't have an output block since there is
    no way to generate code for it.
    If there is one, change its role to DEL_OUTPUT so it will show up
    in the report.
    """
    assert role in [Role.SETUP, Role.TEARDOWN], 'only these roles please'
    matches = findall(pattern, blocks)
    if matches:
        if len(matches) == 1:
            first_match = matches[0]
            if first_match.role == Role.CODE:
                first_match.set(role)
                first_match.add_pattern(pattern)
                if first_match.output is not None:
                    first_match.output.set(Role.DEL_OUTPUT)
        else:
            # More than one block matched the search pattern.
            # The logic here can only get code from a single block.
            description = ''    # avoid inspection nag
            if role == Role.SETUP:
                description = '--setup {0} (or -u{0})'.format(pattern)
            else:
                # can only be teardown because of aseert above
                description = '--teardown {0} (or -d{0})'.format(pattern)
            line_numbers = [str(b.line) for b in matches]
            message = (
                'More than one block matched command line {}.\n'
                'Only one match is allowed.\n'
                'The matching blocks are at line numbers {}.'
            ).format(description, ', '.join(line_numbers))
            raise click.ClickException(message)
