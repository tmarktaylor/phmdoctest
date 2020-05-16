"""Show type information is packaged for distribution. Run mypy on this file.
"""

import click
import commonmark.node    # type: ignore
from typing import List

import phmdoctest.simulator
import phmdoctest.tool


def test_mypy_likes_run_and_pytest() -> None:
    """Usage error for misspelled option."""
    command = 'phmdoctest doc/example1.md --troper --outfile discarded.py'
    simulator_status = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command,
        pytest_options=['--strict', '-v']
    )
    assert (
            simulator_status.runner_status.exit_code == click.UsageError.exit_code
    )
    assert simulator_status.outfile is None
    assert simulator_status.pytest_exit_code is None


def test_mypy_likes_fenced_code_blocks() -> None:
    """Read fenced code block in test_example2.md."""
    blocks = phmdoctest.tool.fenced_code_blocks('doc/test_example2.md')
    assert len(blocks) == 1


def test_mypy_likes_fenced_block_nodes() -> None:
    """Read fenced code block commonmark Nodes from test_example2.md."""
    with open('doc/test_example2.md', encoding='utf-8') as fp:
        nodes = phmdoctest.tool.fenced_block_nodes(fp)    # type: List[commonmark.node.Node]
        assert len(nodes) > 0
