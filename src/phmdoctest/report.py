from collections import Counter
from typing import List

import click
import monotable

from phmdoctest.entryargs import Args
from phmdoctest.fenced import Role, FencedBlock


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
