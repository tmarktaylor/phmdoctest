"""
Show type information is packaged for distribution. Run mypy on this file.

Run pytest here to get code coverage of FencedBlock.__str__().
Run pytest here as well to assure the code runs without error.
"""

import commonmark.node  # type: ignore
from typing import List

import phmdoctest.fenced
import phmdoctest.main
import phmdoctest.simulator
import phmdoctest.tool


def test_fenced_block_dunder_str() -> None:
    """Check result from FencedBlock.__str__()."""
    with open("doc/example1.md", "r", encoding="utf-8") as fp:
        blocks = phmdoctest.fenced.convert_nodes(phmdoctest.tool.fenced_block_nodes(fp))
        assert str(blocks[0]) == "FencedBlock(role=--, line=6)"


def test_mypy_likes_run_and_pytest() -> None:
    """Compile time use of run_and_pytest() to be type checked by mypy."""
    command = "phmdoctest doc/example1.md --report"
    simulator_status = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command, pytest_options=None
    )
    assert simulator_status.runner_status.exit_code == 0
    assert simulator_status.pytest_exit_code is None


def test_mypy_likes_fenced_code_blocks() -> None:
    """Compile time use of fenced_code_blocks() to be type checked by mypy."""
    blocks = phmdoctest.tool.fenced_code_blocks("doc/example1.md")
    assert len(blocks) > 0


def test_mypy_likes_fenced_block_nodes() -> None:
    """Compile time use of fenced_block_nodes() to be type checked by mypy."""
    with open("doc/example1.md", "r", encoding="utf-8") as fp:
        nodes = phmdoctest.tool.fenced_block_nodes(
            fp
        )  # type: List[commonmark.node.Node]    # noqa: E501
        assert len(nodes) > 0
