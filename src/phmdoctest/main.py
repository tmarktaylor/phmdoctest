"""phmdoctest entry point."""
from typing import List, Optional

import click

from phmdoctest.entryargs import Args
from phmdoctest.fenced import FencedBlock, Role
import phmdoctest.cases
import phmdoctest.fenced
import phmdoctest.fillrole
import phmdoctest.report
import phmdoctest.tool


@click.command()
@click.argument(
    "markdown_file",
    nargs=1,
    type=click.Path(
        exists=True,
        dir_okay=False,
        allow_dash=True,
    ),
)
@click.option(
    "--outfile",
    nargs=1,
    help='Write generated test case file to path TEXT. "-"' " writes to stdout.",
)
@click.option(
    "-s",
    "--skip",
    multiple=True,
    help=(
        "Any Python code or interactive session block that contains"
        " the substring TEXT is not tested."
        " More than one --skip TEXT is ok."
        " Double quote if TEXT contains spaces."
        ' For example --skip="python 3.7" will skip every Python block that'
        ' contains the substring "python 3.7".'
        " If TEXT is one of the 3 capitalized strings FIRST SECOND LAST"
        " the first, second, or last Python code or session block in the"
        " Markdown file is skipped."
    ),
)
@click.option(
    "--report", is_flag=True, help="Show how the Markdown fenced code blocks are used."
)
@click.option(
    "--fail-nocode",
    is_flag=True,
    help=(
        "This option sets behavior when the Markdown file has no Python"
        " fenced code blocks or interactive session blocks"
        " or if all such blocks are skipped."
        " When this option is present the generated pytest file"
        " has a test function called test_nothing_fails() that"
        " will raise an assertion."
        " If this option is not present the generated pytest file"
        " has test_nothing_passes() which will never fail."
    ),
)
@click.option(
    "-u",
    "--setup",
    nargs=1,
    help=(
        "The Python code block that contains the substring TEXT"
        " is run at test module setup time. Variables assigned"
        " at the outer level are visible as globals to the other"
        " Python code blocks."
        " TEXT should match exactly one code block."
        " If TEXT is one of the 3 capitalized strings FIRST SECOND LAST"
        " the first, second, or last Python code or session block in the"
        " Markdown file is matched."
        " A block will not match --setup if it matches --skip,"
        " or if it is a session block."
        " Use --setup-doctest below to grant Python sessions access"
        " to the globals."
    ),
)
@click.option(
    "-d",
    "--teardown",
    nargs=1,
    help=(
        "The Python code block that contains the substring TEXT"
        " is run at test module teardown time."
        " TEXT should match exactly one code block."
        " If TEXT is one of the 3 capitalized strings FIRST SECOND LAST"
        " the first, second, or last Python code or session block in the"
        " Markdown file is matched."
        " A block will not match --teardown if it matches either"
        " --skip or --setup, or if it is a session block."
    ),
)
@click.option(
    "--setup-doctest",
    is_flag=True,
    help=(
        "Make globals created by the --setup Python code block"
        " or setup directive visible to"
        " session blocks and only when they are tested with the pytest"
        " --doctest-modules option.  Please note that pytest runs"
        " doctests in a separate context that only runs doctests."
        " This option is ignored if there is no --setup option."
    ),
)
@click.version_option()  # type: ignore
# Note- docstring for entry point shows up in click's usage text.
def entry_point(
    markdown_file, outfile, skip, report, fail_nocode, setup, teardown, setup_doctest
):
    args = Args(
        markdown_file=markdown_file,
        outfile=outfile,
        skips=skip,
        is_report=report,
        fail_nocode=fail_nocode,
        setup=setup,
        teardown=teardown,
        setup_doctest=setup_doctest,
        built_from="",  # not supplied by the Click command line.
    )
    blocks = _configure_block_roles(args)
    if args.is_report:
        phmdoctest.report.print_report(args, blocks)

    # build test cases and write to the --outfile path
    if args.outfile:
        test_case_string = phmdoctest.cases.build_test_cases(args, blocks)
        with click.open_file(args.outfile, "w", encoding="utf-8") as ofp:
            ofp.write(test_case_string)


def _configure_block_roles(args: Args) -> List[FencedBlock]:
    """Find markdown blocks and pair up code and output blocks."""
    with click.open_file(args.markdown_file, "r", encoding="utf-8") as fp:
        blocks = phmdoctest.fenced.convert_nodes(phmdoctest.tool.fenced_block_nodes(fp))
    phmdoctest.fillrole.identify_code_output_session_blocks(blocks)
    phmdoctest.fillrole.del_problem_blocks(blocks)
    code_and_session_blocks = [b for b in blocks if b.role in [Role.CODE, Role.SESSION]]
    phmdoctest.fillrole.apply_skips(args, code_and_session_blocks)
    phmdoctest.fillrole.find_and_designate_setup(args.setup, code_and_session_blocks)
    phmdoctest.fillrole.find_and_designate_teardown(
        args.teardown, code_and_session_blocks
    )
    return blocks


def testfile(
    markdown_file: str = "",
    *,
    skips: Optional[List[str]] = None,
    fail_nocode: bool = False,
    setup: Optional[str] = None,
    teardown: Optional[str] = None,
    setup_doctest: bool = False,
    built_from: str = "",
) -> str:
    """Run with callers keyword arguments and default values.

    Return a string that contains the generated pytest file.
    The parameters are described by the command line help.
    Each string in the list skips is described by the --skip TEXT
    command line option.

    Args:
        markdown_file
            Path to the Markdown input file.

    Keyword Args:
        skips
            List[str]. Do not test blocks with substring TEXT.

        fail_nocode
            Markdown file with no code blocks generates a failing test.

        setup
            Run block with substring TEXT at test module setup time.

        teardown
            Run block with substring TEXT at test module teardown time.

        setup_doctest
            Make globals created by the setup Python code block
            or setup directive visible to Python interactive session >>> blocks.
            Caution: The globals are set at Pytest Session scope and are visible
            to all tests run by --doctest-modules.

        built_from
            Text that follows "built from" in test file's docstring.
            When empty string the docstring built from text is derived
            from markdown_file.

    Returns:
        String containing the contents of the generated pytest file.
    """
    if skips is None:
        skips = []
    args = Args(
        markdown_file=markdown_file,
        outfile="",
        skips=skips,
        is_report=False,
        fail_nocode=fail_nocode,
        setup=setup,
        teardown=teardown,
        setup_doctest=setup_doctest,
        built_from=built_from,
    )
    blocks = _configure_block_roles(args)
    return phmdoctest.cases.build_test_cases(args, blocks)
