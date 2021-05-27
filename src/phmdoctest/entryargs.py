"""Click processed command line arguments collected into a single type."""

from collections import namedtuple

Args = namedtuple(
    "Args",
    [
        "markdown_file",
        "outfile",
        "skips",
        "is_report",
        "fail_nocode",
        "setup",
        "teardown",
        "setup_doctest",
    ],
)
"""Command line arguments with some renames."""
