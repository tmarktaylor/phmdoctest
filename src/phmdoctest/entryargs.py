from collections import namedtuple

Args = namedtuple(
    'Args',
    [
        'markdown_file',
        'outfile',
        'skips',
        'is_report',
        'fail_nocode',
        'setup',
        'teardown'
    ]
)
"""Command line arguments with some renames."""
