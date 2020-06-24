from typing import List

import click

from phmdoctest.entryargs import Args
from phmdoctest.fenced import Role, FencedBlock
import phmdoctest.cases
import phmdoctest.fenced
import phmdoctest.print_capture
import phmdoctest.report
import phmdoctest.tool


@click.command()
@click.argument(
    'markdown_file',
    nargs=1,
    type=click.Path(
        exists=True,
        dir_okay=False,
        allow_dash=True,    # type: ignore
    )
)
@click.option(
    '--outfile',
    nargs=1,
    help=(
        'Write generated test case file to path TEXT. "-"'
        ' writes to stdout.'
    )
)
@click.option(
    '-s', '--skip',
    multiple=True,
    help=(
        'Any Python code or interactive session block that contains'
        ' the substring TEXT is not tested.'
        ' More than one --skip TEXT is ok.'
        ' Double quote if TEXT contains spaces.'
        ' For example --skip="python 3.7" will skip every Python block that'
        ' contains the substring "python 3.7".'
        ' If TEXT is one of the 3 capitalized strings FIRST SECOND LAST'
        ' the first, second, or last Python code or session block in the'
        ' Markdown file is skipped.'
    )
)
@click.option(
    '--report',
    is_flag=True,
    help='Show how the Markdown fenced code blocks are used.'
)
@click.option(
    '--fail-nocode',
    is_flag=True,
    help=(
        'This option sets behavior when the Markdown file has no Python'
        ' fenced code blocks or interactive session blocks'
        ' or if all such blocks are skipped.'
        ' When this option is present the generated pytest file'
        ' has a test function called test_nothing_fails() that'
        ' will raise an assertion.'
        ' If this option is not present the generated pytest file'
        ' has test_nothing_passes() which will never fail.'
    )
)
@click.option(
    '-u', '--setup',
    nargs=1,
    help=(
            'The Python code block that contains the substring TEXT'
            ' is run at test module setup time.  Variables assigned'
            ' at the outer level are visible as globals to the other'
            ' Python code blocks.'
            ' Python sessions cannot access the globals.'
            ' TEXT should match exactly one code block.'
            ' If TEXT is one of the 3 capitalized strings FIRST SECOND LAST'
            ' the first, second, or last Python code or session block in the'
            ' Markdown file is matched.'
            ' A block will not match --setup if it matches --skip,'
            ' or if it is a session block.'
    )
)
@click.option(
    '-d', '--teardown',
    nargs=1,
    help=(
            'The Python code block that contains the substring TEXT'
            ' is run at test module teardown time.'
            ' TEXT should match exactly one code block.'
            ' If TEXT is one of the 3 capitalized strings FIRST SECOND LAST'
            ' the first, second, or last Python code or session block in the'
            ' Markdown file is matched.'
            ' A block will not match --teardown if it matches either'
            ' --skip or --setup, or if it is a session block.'
    )
)
@click.version_option()
# Note- docstring for entry point shows up in click's usage text.
def entry_point(
        markdown_file, outfile, skip, report, fail_nocode, setup, teardown):
    args = Args(
        markdown_file=markdown_file,
        outfile=outfile,
        skips=skip,
        is_report=report,
        fail_nocode=fail_nocode,
        setup=setup,
        teardown=teardown
    )

    # Find markdown blocks and pair up code and output blocks.
    with click.open_file(args.markdown_file, encoding='utf-8') as fp:
        blocks = phmdoctest.fenced.convert_nodes(
            phmdoctest.tool.fenced_block_nodes(fp))
    identify_code_output_session_blocks(blocks)
    del_problem_blocks(blocks)
    code_and_session_blocks = [
        b for b in blocks if b.role in [Role.CODE, Role.SESSION]
    ]
    apply_skips(args, code_and_session_blocks)
    if args.setup:
        find_and_designate_setup_or_teardown(
            Role.SETUP, args.setup, code_and_session_blocks)
    if args.teardown:
        find_and_designate_setup_or_teardown(
            Role.TEARDOWN, args.teardown, code_and_session_blocks)
    if args.is_report:
        phmdoctest.report.print_report(args, blocks)

    # build test cases and write to the --outfile path
    if args.outfile:
        test_case_string = phmdoctest.cases.build_test_cases(args, blocks)
        with click.open_file(args.outfile, 'w', encoding='utf-8') as ofp:
            ofp.write(test_case_string)


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


# todo- need test cases for empty code, session, output blocks <-----------------------------
# todo- need del block list in the report               <-----------------------------
def del_problem_blocks(blocks: List[FencedBlock]) -> None:
    """Re-designate blocks that can't be used."""
    # Rather than asserting and blowing up the caller, just set the
    # blocks we can't deal with aside for later discovery in
    # del'd block list section the report.
    empty_blocks = [b for b in blocks if not b.contents]
    for block in empty_blocks:
        if block.role == Role.CODE:
            block.set(Role.DEL_CODE)
        elif block.role == Role.OUTPUT:
            block.set(Role.DEL_OUTPUT)
        elif block.role == Role.SESSION:
            block.set(Role.DEL_SESSION)


# todo- test cases for the new ClickException <--------------------------------------
# todo- create special role type that has two values setup, teardown <-------------------
def find_and_designate_setup_or_teardown(
        role: Role, pattern: str, blocks: List[FencedBlock]) -> None:
    """Find and designate Python code block as setup or teardown.

    Search the contents of each block for the pattern.
    Report an error if more than one block matches the search.
    If exactly one code block contains pattern and it
    has not been changed from Role.CODE set it to the caller's role.
    Setup and teardown code can't have an output block since there is
    no way to generate code for it.
    If there is one, change it role to DEL_OUTPUT so it will show up
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
                description = '--setup {0} or -u{0}'.format(pattern)
            elif role == Role.TEARDOWN:
                description = '--teardown {0} or -d{0}'.format(pattern)
            line_numbers = [str(b.line) for b in matches]
            message = (
                'More than one block matched command line {}.\n'
                'Only one match is allowed.\n'
                'The matching blocks are at line numbers {}.'
            ).format(description, ', '.join(line_numbers))
            raise click.ClickException(message)
