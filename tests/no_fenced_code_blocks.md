### Markdown file that has no fenced code blocks.

This file covers the use case where phmdoctest is given
a Markdown file with no fenced code blocks with
the `--report` option.

The report will not have the table of fenced code blocks.

A line of code in report.print_report checks for
produces the table only if the list of blocks is
not empty.

Running phmdoctest with this file produces branch
coverage for the branch taken when the list of
blocks is empty.
