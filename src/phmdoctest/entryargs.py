"""Click processed command line arguments and more."""

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
        "built_from",
    ],
)
"""Command line arguments with some renames."""
