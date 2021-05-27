"""Print report about fenced code blocks and how they are used."""

from collections import Counter
from typing import List

import click
import monotable

from phmdoctest.entryargs import Args
from phmdoctest.fenced import FencedBlock


def print_report(args: Args, blocks: List[FencedBlock]) -> None:
    """Print Markdown fenced block report and skips report."""
    report = []
    filename = click.format_filename(args.markdown_file)
    title1 = filename + " fenced blocks"
    if blocks:
        text1 = fenced_block_report(blocks, title=title1)
        report.append(text1)

    roles = [b.role.name for b in blocks]
    counts = Counter(roles)

    number_of_test_cases = counts["CODE"] + counts["SESSION"]
    report.append("{} test cases.".format(number_of_test_cases))
    if counts["SKIP_CODE"] > 0:
        report.append("{} skipped code blocks.".format(counts["SKIP_CODE"]))
    if counts["SKIP_SESSION"] > 0:
        report.append(
            "{} skipped interactive session blocks.".format(counts["SKIP_SESSION"])
        )

    num_missing_output = counts["CODE"] - counts["OUTPUT"]
    if num_missing_output:
        report.append("{} code blocks with no output block.".format(num_missing_output))

    # del blocks are blocks that will be ignored.
    num_del = counts["DEL_CODE"] + counts["DEL_OUTPUT"]
    if num_del:
        report.append('{} blocks marked "del-". They are not tested.'.format(num_del))

    # Note if caller wanted --setup and its not happening.
    # Note if caller wanted --setup-doctest and its not happening.
    # This occurs if:
    #     no --setup option
    #     setup block was not found
    #     setup block was skipped
    if args.setup_doctest and not counts["SETUP"]:
        report.append("No setup block found, not honoring --setup-doctest.")
    else:
        if args.setup and not counts["SETUP"]:
            report.append("No setup block found.")

    # Note if caller wanted --teardown and its not happening.
    if args.teardown and not counts["TEARDOWN"]:
        report.append("No teardown block found.")

    if args.skips:
        report.append("")
        title2 = "skip pattern matches (blank means no match)"
        text2 = skips_report(args.skips, blocks, title=title2)
        report.append(text2)
    print("\n".join(report))


def fenced_block_report(blocks: List[FencedBlock], title: str = "") -> str:
    """Generate text report about the input file fenced code blocks."""
    table = monotable.MonoTable()
    table.max_cell_height = 7
    table.more_marker = "..."
    cell_grid = []
    for block in blocks:
        # assemble list of matching TEXT search strings from the command line
        patterns = [r.join(['"', '"']) for r in block.patterns]

        # Add to the patterns list the shortened names of any directives
        for d in block.directives:
            name = d.literal.replace("<!--phmdoctest", "")
            name = name.replace("-->", "")
            patterns.append(name)
        cell = "\n".join(patterns)
        cell_grid.append([block.type, block.line, block.role.value, cell])
    headings = [
        "block\ntype",
        "line\nnumber",
        "test\nrole",
        "TEXT or directive\nquoted and one per line",
    ]
    formats = ["", "", "", "(width=40)"]
    text = table.table(headings, formats, cell_grid, title)  # type: str
    return text


def skips_report(skips: List[str], blocks: List[FencedBlock], title: str = "") -> str:
    """Generate text report about the disposition of --skip options."""
    # Blocks with role OUTPUT and SKIP_OUTPUT will always have an
    # empty skip_reasons list even if the linking code block is skipped.
    table = monotable.MonoTable()
    table.max_cell_height = 5
    table.more_marker = "..."
    cell_grid = []
    for skip in skips:
        code_lines = []
        for block in blocks:
            if skip in block.patterns:
                code_lines.append(str(block.line))

        cell_grid.append([skip, ", ".join(code_lines)])
    headings = ["skip pattern", "matching code block line number(s)"]
    formats = ["", "(width=36;wrap)"]
    text = table.table(headings, formats, cell_grid, title)  # type: str
    return text
