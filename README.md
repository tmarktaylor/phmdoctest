# phmdoctest

   `~~~`Python syntax highlighted Markdown doctest

Command line program to test Python syntax highlighted code
examples in Markdown.

- No extra tags or html comments or needed in the Markdown.
- Synthesizes a pytest test file from examples in Markdown.
- Examples take the form of Python source code and expected
  terminal output placed in Markdown fenced code blocks.
- The test cases are run separately by calling pytest.
- A separate Python library runs phmdoctest and can run pytest too.

todo- license shield link
[![](https://img.shields.io/pypi/l/phmdoctest.svg)]()
[![PyPI](https://img.shields.io/pypi/v/phmdoctest.svg)](https://pypi.python.org/pypi/phmdoctest)
[![PyPI Python Versions](https://img.shields.io/pypi/pyversions/phmdoctest.svg)](https://pypi.python.org/pypi/phmdoctest)

[Python Package Index/phmdoctest](https://pypi.python.org/pypi/phmdoctest)

#### master branch status

[![Build Status](https://travis-ci.org/tmarktaylor/phmdoctest.svg?branch=master)](https://travis-ci.org/tmarktaylor/phmdoctest) on [Travis CI](https://travis-ci.org/)
[![Code Coverage](https://codecov.io/gh/tmarktaylor/phmdoctest/coverage.svg?branch=master)](https://codecov.io/gh/tmarktaylor/phmdoctest?branch=master)


#### Installation
    pip install phmdoctest

## Sample usage

Given the Markdown file [tests/example1.md][1]
shown in raw form here...

~~~
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

    phmdoctest tests/example1.md --outfile test_example1.py

creates the python source code file [test_example1.py][2] also shown here...

```python
"""pytest file built from tests/example1.md"""


def line_compare_exact(want, got):
    """Line by line helper compare function with assertion for pytest."""
    if want:
        want_lines = want.splitlines()
        got_lines = got.splitlines()
        assert want_lines == got_lines


def test_code_3_output_16(capsys):
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
    line_compare_exact(want=expected_str, got=capsys.readouterr().out)

```

Then run a pytest command something like this in your terminal
to test the Markdown code and expected output blocks.

    pytest --strict 

The `3` in the function name `test_code_3_output_16` is the
line number in [tests/example1.md][1] of the first line
of python code. `16` shows the line number of the expected 
terminal output.

phmdoctest tries to generate one test case function for each 
Python-code/expected-output Markdown fenced code block pair.
The `--report` option below shows the blocks discovered and
how phmdoctest will test them.
   
## --report option

To see the [GFM fenced code blocks][3] in the MARKDOWN_FILE use the 
--report option like this:

```
phmdoctest tests/example1.md --report
```

which lists the fenced code blocks it found.  The `test role` column
shows how phmdoctest designated the fenced code block.

```
        tests/example1.md fenced blocks
------------------------------------------------
block      line  test    skip pattern/reason
type     number  role    quoted and one per line
------------------------------------------------
python3       3  code
             16  output
------------------------------------------------
1 test cases
0 code blocks missing an output block
```

## How phmdoctest identifies code and output blocks

Only [GFM fenced code blocks][3] are considered.

To be treated as Python code the opening fence should start 
with one of these:

~~~
```python
```python3
```py3
~~~ 

It is ok if the [info string](https://github.github.com/gfm/#info_string)
is laden with additional text, phmdoctest will ignore it.  The
entire info string will be shown in the Block type column of the
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

The report shows which Python blocks are skipped
in the test role column and the Python blocks that 
matched each --skip TEXT in the skips section.

This option makes it **very easy** to **inadvertently exclude**
Python blocks from the test cases.

Three special `--skip TEXT` strings work a little differently.
They select one of the first, second, or last of the Python blocks.
Only Python blocks are counted.
- `--skip FIRST` skips the first Python block
- `--skip SECOND` skips the second Python block
- `--skip LAST` skips the final Python block

skip example code here  
report example here
 
## Usage

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
  --version        Show the version and exit.
  --help           Show this message and exit.
```

## Hints

- phmdoctest can read the Markdown file from the standard input stream.
  Use `-` for MARKDOWN_FILE.
- Write the test file to a temporary directory so that
  it is always up to date.

## Running phmdoctest from Python.

## Simulator. run_and_pytest


## Related PYPI programs
- rundoc
- byexample
- doexec


[1]: tests/example1.md
[2]: doc/test_example1.py
[3]: https://github.github.com/gfm/#fenced-code-blocks
