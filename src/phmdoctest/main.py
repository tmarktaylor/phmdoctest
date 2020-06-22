from collections import Counter
import inspect
from typing import List

import click
import monotable

from phmdoctest.args import Args
from phmdoctest.fenced import Role, FencedBlock
import phmdoctest.fenced
import phmdoctest.print_capture
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
    identify_code_and_output_blocks(blocks)
    code_and_session_blocks = [
        b for b in blocks if b.role in [Role.CODE, Role.SESSION]
    ]
    apply_skips(args, code_and_session_blocks)
    if args.setup:
        identify_setup_block(args.setup, code_and_session_blocks)
    if args.teardown:
        identify_teardown_block(args.teardown, code_and_session_blocks)
    if args.is_report:
        print_report(args, blocks)

    # build test cases and write to the --outfile path
    if args.outfile:
        test_case_string = build_test_cases(args, blocks)
        with click.open_file(args.outfile, 'w', encoding='utf-8') as ofp:
            ofp.write(test_case_string)


PYTHON_FLAVORS = ['python', 'py3', 'python3']
"""Python fenced code blocks info string will start with one of these."""


def identify_code_and_output_blocks(blocks: List[FencedBlock]) -> None:
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


def identify_setup_block(
       pattern: str, blocks: List[FencedBlock]) -> None:
    """Designate Python code that runs setup_module code.

    Caller should call apply_skips() to blocks before calling here.
    Search the contents of each block for the setup TEXT.
    Report an error if more than one block matches the search.
    If exactly one code block contains TEXT and it is not already
    skipped, designate it as the setup block.
    If the block is skipped then no setup block is identified.
    """
    matches = findall(pattern, blocks)
    if matches:
        if len(matches) == 1:
            first_match = matches[0]
            if first_match.role == Role.CODE:
                first_match.set(Role.SETUP)
                first_match.add_pattern(pattern)
        else:
            message = many_matches_message('setup', matches)
            assert False, message


def identify_teardown_block(
        pattern: str, blocks: List[FencedBlock]) -> None:
    """Designate Python code that runs teardown_module code.

    Caller should call apply_skips() to blocks before calling here.
    Caller should call identify_setup_block() before calling here.
    Search the contents of each block for the teardown TEXT.
    Report an error if more than one block matches the search.
    If exactly one code block contains TEXT and it is not already
    skipped or setup, designate it as the teardown block.
    If the block is skipped or setup then no teardown block is identified.
    """
    matches = findall(pattern, blocks)
    if matches:
        if len(matches) == 1:
            first_match = matches[0]
            if first_match.role == Role.CODE:
                first_match.set(Role.TEARDOWN)
                first_match.add_pattern(pattern)
        else:
            description = 'teardown ' + pattern
            message = many_matches_message(description, matches)
            assert False, message


def many_matches_message(
        description: str, offending_blocks: List[FencedBlock]) -> str:
    """Compose error message listing the offending blocks by line number."""
    line_numbers = [str(b.line) for b in offending_blocks]
    message = (
        'More than one block matched --{}.\nOnly one match is allowed.\n'
        'The matching blocks are at line numbers {}.'
    ).format(description, ', '.join(line_numbers))
    return message


def print_report(args: Args, blocks: List[FencedBlock]) -> None:
    """Print Markdown fenced block report and skips report."""
    report = []
    filename = click.format_filename(args.markdown_file)
    title1 = filename + ' fenced blocks'
    text1 = fenced_block_report(blocks, title=title1)
    report.append(text1)

    roles = [b.role.name for b in blocks]
    counts = Counter(roles)

    number_of_test_cases = counts['CODE'] + counts['SESSION']
    report.append('{} test cases'.format(number_of_test_cases))
    if counts['SKIP_CODE'] > 0:
        report.append('{} skipped code blocks'.format(
            counts['SKIP_CODE']
        ))
    if counts['SKIP_SESSION'] > 0:
        report.append('{} skipped interactive session blocks'.format(
            counts['SKIP_SESSION']
        ))

    # assumes session blocks can never be designated setup or teardown
    num_code_blocks = sum(
        [counts['CODE'], counts['SETUP'], counts['TEARDOWN']]
    )
    num_missing_output = num_code_blocks - counts['OUTPUT']
    assert num_missing_output >= 0, 'sanity check'
    report.append(
        '{} code blocks missing an output block'.format(
            num_missing_output
        )
    )

    if args.skips:
        report.append('')
        title2 = 'skip pattern matches (blank means no match)'
        text2 = skips_report(args.skips, blocks, title=title2)
        report.append(text2)
    print('\n'.join(report))


def fenced_block_report(blocks: List[FencedBlock], title: str = '') -> str:
    """Generate text report about the input file fenced code blocks."""
    table = monotable.MonoTable()
    table.max_cell_height = 7
    table.more_marker = '...'
    cell_grid = []
    for block in blocks:
        if block.role in [Role.SKIP_CODE, Role.SKIP_SESSION]:
            quoted_skips = [r.join(['"', '"']) for r in block.patterns]
            skips = '\n'.join(quoted_skips)
        elif block.role in [Role.SETUP, Role.TEARDOWN]:
            skips = '"' + block.patterns[0] + '"'
        else:
            skips = ''
        cell_grid.append([block.type, block.line, block.role.value, skips])
    headings = [
        'block\ntype', 'line\nnumber', 'test\nrole',
        'matching TEXT pattern\nquoted and one per line']
    formats = ['', '', '', '(width=30)']
    text = table.table(headings, formats, cell_grid, title)    # type: str
    return text


def skips_report(
        skips: List[str], blocks: List[FencedBlock], title: str = '') -> str:
    """Generate text report about the disposition of --skip options."""
    # Blocks with role OUTPUT and SKIP_OUTPUT will always have an
    # empty skip_reasons list even if the linking code block is skipped.
    table = monotable.MonoTable()
    table.max_cell_height = 5
    table.more_marker = '...'
    cell_grid = []
    for skip in skips:
        code_lines = []
        for block in blocks:
            if skip in block.patterns:
                code_lines.append(str(block.line))

        cell_grid.append([skip, ', '.join(code_lines)])
    headings = ['skip pattern', 'matching code block line number(s)']
    formats = ['', '(width=36;wrap)']
    text = table.table(headings, formats, cell_grid, title)    # type: str
    return text


def test_nothing_fails() -> None:
    """Fail if no Python code blocks or sessions were processed."""
    assert False, 'nothing to test'


def test_nothing_passes() -> None:
    """Succeed  if no Python code blocks or sessions were processed."""
    # nothing to test
    pass


_ASSERTION_MESSAGE = 'zero length {} block at line {}'


def build_test_cases(args: Args, blocks: List[FencedBlock]) -> str:
    """Generate test code from the Python fenced code blocks."""
    # repr escapes back slashes from win filesystem paths
    # so it can be part of the generated test module docstring.
    quoted_markdown_path = repr(click.format_filename(args.markdown_file))
    markdown_path = quoted_markdown_path[1:-1]
    docstring_text = 'pytest file built from {}'.format(markdown_path)
    builder = phmdoctest.print_capture.PytestFile(docstring_text)
    number_of_test_cases = 0
    for block in blocks:
        if block.role == Role.SETUP:
            builder.add_setup(
                identifier=more_readable(line_numbers_string(block)),
                code=get_code(block),
                expected_output=get_expected_output(block)
            )

        elif block.role == Role.TEARDOWN:
            builder.add_teardown(
                identifier=more_readable(line_numbers_string(block)),
                code=get_code(block),
                expected_output=get_expected_output(block)
            )

        elif block.role == Role.CODE:
            builder.add_test_case(
                identifier=line_numbers_string(block),
                code=get_code(block),
                expected_output=get_expected_output(block)
            )
            number_of_test_cases += 1

        elif block.role == Role.SESSION:
            session = block.contents
            assert session, _ASSERTION_MESSAGE.format('session', block.line)
            builder.add_interactive_session(str(block.line), session)
            number_of_test_cases += 1

    if number_of_test_cases == 0:
        if args.fail_nocode:
            test_function = inspect.getsource(test_nothing_fails)
        else:
            test_function = inspect.getsource(test_nothing_passes)
        builder.add_source(test_function)
    return str(builder)


def more_readable(text):
    """Replace underscores with blanks."""
    return text.replace('_', ' ')


def line_numbers_string(block: FencedBlock) -> str:
    """Return string showing code/output block file line numbers."""
    code_identifier = 'code_' + str(block.line)
    output_identifier = ''
    if block.output:
        output_identifier = '_output_' + str(block.output.line)
    return code_identifier + output_identifier


def get_code(block: FencedBlock) -> str:
    assert block.contents, _ASSERTION_MESSAGE.format('code', block.line)
    return block.contents


def get_expected_output(block: FencedBlock) -> str:
    if block.output:
        expected_output = block.output.contents
        assert expected_output, _ASSERTION_MESSAGE.format(
            'expected output', block.line)
    else:
        expected_output = ''
    return expected_output
