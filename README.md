# phmdoctest 0.0.6

## Introduction

Python syntax highlighted Markdown doctest

Command line program to test Python syntax highlighted code
examples in Markdown.

- No extra tags or html comments needed in the Markdown. No Markdown edits at all.
- No `<BLANKLINE>` needed in output. [doctest][4].
- Synthesizes a pytest test file from examples in Markdown.
- Reads Python source code and expected
  terminal output from Markdown fenced code blocks.
- The test cases are run later by calling pytest.  
- Get code coverage by running pytest with [coverage][6]. 
- An included Python library: [Development tools API][10].
  - runs phmdoctest and can run pytest too. *(simulator.py)*
  - functions to read fenced code blocks from Markdown. *(tool.py)*

phmdoctest does **not** do:
- setup and teardown
- catch exceptions
- ellipsis comparisons
- Python console >>>, ...

##### master branch status
[![](https://img.shields.io/pypi/l/phmdoctest.svg)](https://github.com/tmarktaylor/phmdoctest/blob/master/LICENSE.txt)
[![](https://img.shields.io/pypi/v/phmdoctest.svg)](https://pypi.python.org/pypi/phmdoctest)
[![](https://img.shields.io/pypi/pyversions/phmdoctest.svg)](https://pypi.python.org/pypi/phmdoctest)

[![](https://readthedocs.org/projects/phmdoctest/badge/?version=latest)](https://phmdoctest.readthedocs.io/en/latest/?badge=latest)
[![](https://travis-ci.org/tmarktaylor/phmdoctest.svg?branch=master)](https://travis-ci.org/tmarktaylor/phmdoctest)
[![](https://codecov.io/gh/tmarktaylor/phmdoctest/coverage.svg?branch=master)](https://codecov.io/gh/tmarktaylor/phmdoctest?branch=master)

[Documentation](https://phmdoctest.readthedocs.io/en/latest/) |
[Homepage](https://github.com/tmarktaylor/phmdoctest) |
[Build](https://travis-ci.org/tmarktaylor/phmdoctest) |
[Codecov](https://codecov.io/gh/tmarktaylor/phmdoctest?branch=master) |
[License](https://github.com/tmarktaylor/phmdoctest/blob/master/LICENSE.txt)


## Installation
    pip install phmdoctest

## Sample usage

Given the Markdown file [example1.md](doc/example1.md)
shown in raw form here...

~~~
# This is Markdown file example1.md
Code:
```python3
from enum import Enum

class Floats(Enum):
    APPLES = 1
    CIDER = 2
    CHERRIES = 3
    ADUCK = 4
for floater in Floats:
    print(floater)
```

sample output:
```
Floats.APPLES
Floats.CIDER
Floats.CHERRIES
Floats.ADUCK
```
~~~

the command...
```
phmdoctest doc/example1.md --outfile test_example1.py
```

creates the python source code file `test_example1.py` shown here...

```python
"""pytest file built from doc/example1.md"""
from itertools import zip_longest


def line_by_line_compare_exact(a, b):
    """Line by line helper compare function with assertion for pytest."""
    a_lines = a.splitlines()
    b_lines = b.splitlines()
    for a_line, b_line in zip_longest(a_lines, b_lines):
        assert a_line == b_line


def test_code_4_output_17(capsys):
    from enum import Enum

    class Floats(Enum):
        APPLES = 1
        CIDER = 2
        CHERRIES = 3
        ADUCK = 4
    for floater in Floats:
        print(floater)

    expected_str = """\
Floats.APPLES
Floats.CIDER
Floats.CHERRIES
Floats.ADUCK
"""
    line_by_line_compare_exact(a=expected_str, b=capsys.readouterr().out)
```

Then run a pytest command something like this in your terminal
to test the Markdown code and expected output blocks.

    pytest --strict 

The `4` in the function name `test_code_4_output_17` is the
line number in [example1.md](doc/example1.md) of the first line
of python code. `17` shows the line number of the expected 
terminal output.

phmdoctest tries to generate one test case function for each 
Python-code/expected-output Markdown fenced code block pair.
The `--report` option below shows the blocks discovered and
how phmdoctest will test them.
   
## --report option

To see the [GFM fenced code blocks][3] in the MARKDOWN_FILE use the 
--report option like this:

```
phmdoctest doc/example2.md --report
```

which lists the fenced code blocks it found in
the file [example2.md](doc/example2.md).
The `test role` column shows how phmdoctest 
will test each fenced code block.  

```
        doc/example2.md fenced blocks
----------------------------------------------
block    line  test    skip pattern/reason
type   number  role    quoted and one per line
----------------------------------------------
py3         9  code
           14  output
py3        20  code
           26  output
           31  --
py3        37  code
py3        44  code
           51  output
yaml       59  --
text       67  --
py3        74  code
           80  output
----------------------------------------------
5 test cases
1 code blocks missing an output block
```

## How phmdoctest identifies code and output blocks

phmdoctest uses the PYPI [commonmark][7] project to extract fenced code
blocks from Markdown. Specification [CommonMark Spec][8] and website [CommonMark][9].

Only [GFM fenced code blocks][3] are considered.

To be treated as Python code the opening fence should start 
with one of these:

    ```python
    ```python3
    ```py3

It is ok if the [info string](https://github.github.com/gfm/#info_string)
is laden with additional text, phmdoctest will ignore it.  The
entire info string will be shown in the block type column of the
report.

Output blocks are fenced code blocks that immediately follow a
Python block and start with an opening fence like this which
has an empty info string.

    ```

If a Python block is followed by another Python block or a fenced code block
with a non-empty info string the first Python block has no output. 
phmdoctest will still generate test code for it, but there will be no
assertion statement.

## Skipping Python blocks with the --skip option

If you don't want to generate test cases for Python
blocks use the `--skip TEXT` option. More than one `--skip TEXT` 
is allowed.

The code in each Python block is searched 
for the substring `TEXT`.  Zero, one or more blocks will contain
the substring. These blocks will not generate test cases in the
output file.

- The Python code in the fenced code block is searched.
- The info string is **not** searched.
- Output blocks are **not** searched.
- Only Python code blocks are searched.
- Case is significant.

The report shows which Python blocks are skipped
in the test role column and the Python blocks that 
matched each --skip TEXT in the skips section.

This option makes it **very easy** to **inadvertently exclude**
Python blocks from the test cases.  In the event no test cases are
generated, the option `--fail-nocode` described below is useful.

Three special `--skip TEXT` strings work a little differently.
They select one of the first, second, or last of the Python blocks.
Only Python blocks are counted.
- `--skip FIRST` skips the first Python block
- `--skip SECOND` skips the second Python block
- `--skip LAST` skips the final Python block

## --skip Example

This command
```
phmdoctest doc/example2.md --skip "Python 3.7" --skip LAST --report --outfile test_example2.py
```

Produces the report
```
           doc/example2.md fenced blocks
---------------------------------------------------
block    line  test         skip pattern/reason
type   number  role         quoted and one per line
---------------------------------------------------
py3         9  code
           14  output
py3        20  skip-code    "Python 3.7"
           26  skip-output
           31  --
py3        37  code
py3        44  code
           51  output
yaml       59  --
text       67  --
py3        74  skip-code    "LAST"
           80  skip-output
---------------------------------------------------
3 test cases
2 skipped code blocks
1 code blocks missing an output block

  skip pattern matches (blank means no match)
------------------------------------------------
skip pattern  matching code block line number(s)
------------------------------------------------
Python 3.7    20
LAST          74
------------------------------------------------
```
 
and creates the output file [test_example2.py][2]

## -s short option form of --skip

This is the same command as above using the short `-s` form of the --skip option
in two places.
It produces the same report and outfile.
```
phmdoctest doc/example2.md -s "Python 3.7" -sLAST --report --outfile test_example2.py
```

## --fail-nocode

This option produces a pytest file that will always
fail when no Python code blocks are found.

If phmdoctest doesn't find any Python code blocks in the
Markdown file a pytest file is still generated.
This also happens when `--skip` eliminates all the
Python code blocks. 
The generated pytest file will have the function
`def test_nothing_passes()`.

If the option `--fail-nocode` is passed to phmdoctest the
function is `def test_nothing_fails()` which raises an
assertion.
 

## Send outfile to standard output
To redirect the above outfile to the standard output stream use one
of these two commands.

Be sure to leave out `--report` when sending --outfile to standard output.
```
phmdoctest doc/example2.md -s "Python 3.7" -sLAST --outfile -
```
or
```
phmdoctest doc/example2.md -s "Python 3.7" -sLAST --outfile=-
```

## Usage

`phmdoctest --help`

```
Usage: phmdoctest [OPTIONS] MARKDOWN_FILE

Options:
  --outfile TEXT   Write generated test case file to path TEXT. "-" writes to
                   stdout.
  -s, --skip TEXT  Any Python block that contains the substring TEXT is not
                   tested. More than one --skip TEXT is ok. Double quote if
                   TEXT contains spaces. For example --skip="python 3.7" will
                   skip every Python block that contains the substring "python
                   3.7". If TEXT is one of the 3 capitalized strings FIRST
                   SECOND LAST the first, second, or last Python block in the
                   Markdown file is skipped. The fenced code block info string
                   is not searched.
  --report         Show how the Markdown fenced code blocks are used.
  --fail-nocode    This option sets behavior when the Markdown file has no
                   Python fenced code blocks or if all such blocks are
                   skipped. When this option is present the generated pytest
                   file has a test function called test_nothing_fails() that
                   will raise an assertion. If this option is not present the
                   generated pytest file has test_nothing_passes() which will
                   never fail.
  --version        Show the version and exit.
  --help           Show this message and exit.
```

## Running on Travis CI  

The partial script shown below is for Python 3.5 on [Travis CI][5].
The script steps are:

- Install pytest.
- Create a new directory to take the generated test file.
- Run phmdoctest to generate the test file and print the report.
- Run pytest suite.

Writing the generated test files to a new directory
assures an existing test file is not overwritten by mistake.

```yaml
dist: xenial
language: python
sudo: false

matrix:
  include:
    - python: 3.5
      install:
        - pip install "." pytest
      script:
        - mkdir tests/tmp
        - phmdoctest project.md --report --outfile tests/tmp/test_project_readme.py
        - pytest --strict -vv tests
```

## Running phmdoctest from the command line as a Python module

Here is an example:

`python -m phmdoctest doc/example2.md --report`

## Testing phmdoctest from within a Python script

`phmdoctest.simulator` offers the function `run_and_pytest()`
which simulates running phmdoctest from the command line.
- useful during development
- creates the --outfile in a temporary directory
- optionally runs pytest on the outfile 

Please see the [Development tools API section][10] or
the docstring of the function `run_and_pytest()` in the file `simulator.py.` 
pytest_options are passed as a list of strings as shown below.

```python
import phmdoctest.simulator
command = 'phmdoctest doc/example1.md --report --outfile test_me.py'
simulator_status = phmdoctest.simulator.run_and_pytest(
    well_formed_command=command,
    pytest_options=['--strict', '-v']
)
assert simulator_status.runner_status.exit_code == 0
assert simulator_status.pytest_exit_code == 0
```

## Hints

- phmdoctest can read the Markdown file from the standard input stream.
  Use `-` for MARKDOWN_FILE.
- Write the test file to a temporary directory so that
  it is always up to date.
- Its easy to use --output by mistake instead of `--outfile`.
- If Python code block has no output, put assert statements in the code.
- phmdoctest ignores Markdown indented code blocks ([Spec][8] section 4.4).
  

## Related projects
- rundoc
- byexample
- doexec
- egtest

[Recent Changes](doc/recent_changes.md)

[3]: https://github.github.com/gfm/#fenced-code-blocks
[10]: https://phmdoctest.readthedocs.io/en/latest/doc/api.html
[2]: https://github.com/tmarktaylor/phmdoctest/blob/master/src/phmdoctest/doc/test_example2.py
[7]: https://pypi.org/project/commonmark
[8]: https://spec.commonmark.org
[9]: https://commonmark.org
[4]: https://docs.python.org/3/library/doctest.html
[5]: https://docs.travis-ci.com
[6]: https://pypi.python.org/project/coverage
