# phmdoctest 1.0.1

## Introduction

Python syntax highlighted Markdown doctest

Command line program to test Python syntax highlighted code
examples in Markdown.

- Synthesizes a pytest test file from examples in Markdown.
- Reads these from Markdown fenced code blocks:
  - Python interactive sessions described by [doctest][4].
  - Python source code and expected terminal output.
- No extra tags or html comments needed in the Markdown. No Markdown edits at all.
- The test cases are run later by calling pytest.  
- Get code coverage by running pytest with [coverage][6].
- Select Python source code blocks as setup and teardown code.
- Setup applies to code blocks and optionally to session blocks.
- An included Python library: [Latest Development tools API][10].
  - runs phmdoctest and can run pytest too. *(simulator.py)*
  - functions to read fenced code blocks from Markdown. *(tool.py)*
 

##### master branch status
[![](https://img.shields.io/pypi/l/phmdoctest.svg)](https://github.com/tmarktaylor/phmdoctest/blob/master/LICENSE.txt)
[![](https://img.shields.io/pypi/v/phmdoctest.svg)](https://pypi.python.org/pypi/phmdoctest)
[![](https://img.shields.io/pypi/pyversions/phmdoctest.svg)](https://pypi.python.org/pypi/phmdoctest)

[![](https://readthedocs.org/projects/phmdoctest/badge/?version=latest)](https://phmdoctest.readthedocs.io/en/latest/?badge=latest)
[![](https://travis-ci.org/tmarktaylor/phmdoctest.svg?branch=master)](https://travis-ci.org/tmarktaylor/phmdoctest)
[![](https://codecov.io/gh/tmarktaylor/phmdoctest/coverage.svg?branch=master)](https://codecov.io/gh/tmarktaylor/phmdoctest?branch=master)

[Documentation](https://phmdoctest.readthedocs.io/en/latest/) |
[Homepage](https://github.com/tmarktaylor/phmdoctest) |
[Build][12] |
[Codecov](https://codecov.io/gh/tmarktaylor/phmdoctest?branch=master) |
[License](https://github.com/tmarktaylor/phmdoctest/blob/master/LICENSE.txt)

[Introduction](#introduction) |
[Installation](#installation) |
[Sample usage](#sample-usage) |
[--report](#--report) |
[Identifying blocks](#identifying-blocks) |
[skipping blocks](#skipping-blocks) |
[--skip](#--skip) |
[-s short form of --skip](#-s-short-form-of---skip) |
[--fail-nocode](#--fail-nocode) |
[--setup](#--setup) |
[--teardown](#--teardown) |
[Setup example](#setup-example) |
[Setup for sessions](#setup-for-sessions) |
[Execution context](#execution-context) |
[Send outfile to stdout](#send-outfile-to-stdout) |
[Usage](#usage) |
[Run on Travis CI](#run-on-travis-ci) |
[Run as a Python module](#run-as-a-python-module) |
[Call from Python](#call-from-python) |
[Hints](#hints) |
[Related projects](#related-projects) |
[Recent changes](#recent-changes)
 
## Installation
It is advisable to install in a virtual environment.

    python -m pip install phmdoctest

## Sample usage

Given the Markdown file [example1.md](doc/example1.md)
shown in raw form here...

~~~
# This is Markdown file example1.md

## Interactive Python session (doctest)

```pycon 
>>> print('Hello World!')
Hello World!
```

## Source Code and terminal output
 
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


def session_00001_line_6():
    r"""
    >>> print('Hello World!')
    Hello World!
    """


def test_code_14_output_27(capsys):
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
to test the Markdown session, code, and expected output blocks.

    pytest --doctest-modules
    
Or these two commands:

    pytest
    python -m doctest test_example1.py

The `line_6` in the function name `session_00001_line_6` is the 
line number in [example1.md](doc/example1.md) of the first line
of the interactive session. `00001` is a sequence number to
order the doctests. 

The `14` in the function name `test_code_14_output_27` is the
line number of the first line
of python code. `27` shows the line number of the expected 
terminal output.

One test case function is generated for each: 

- Markdown fenced code block interactive session 
- Python-code/expected-output Markdown fenced code block pair

The `--report` option below shows the blocks discovered and
how they are tested.
   
## --report

To see the [GFM fenced code blocks][3] in the MARKDOWN_FILE use the 
`--report` option like this:

```
phmdoctest doc/example2.md --report
```

which lists the fenced code blocks it found in
the file [example2.md](doc/example2.md).
The `test role` column shows how each fenced code block is tested.  

```
         doc/example2.md fenced blocks
-----------------------------------------------
block    line  test     matching TEXT pattern
type   number  role     quoted and one per line
-----------------------------------------------
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
py         75  session
py3        87  code
           93  output
pycon     101  session
-----------------------------------------------
7 test cases.
1 code blocks missing an output block.
```

## Identifying blocks

The PYPI [commonmark][7] project provides code to extract fenced code
blocks from Markdown. Specification [CommonMark Spec][8] and website [CommonMark][9].

Python code, expected output, and Python interactive sessions are extracted.

Only [GFM fenced code blocks][3] are considered.

A block is a session block if the info_string starts with 'py' 
and the first line of the block starts with the
session prompt: `'>>> '`.
 
To be treated as Python code the opening fence should start 
with one of these:

    ```python
    ```python3
    ```py3

and the block contents can't start with `'>>> '`.

[project.md](project.md) has more examples of code and session blocks.

It is ok if the [info string][11]
is laden with additional text, it will be ignored.  The
entire info string will be shown in the block type column of the
report.

Output blocks are fenced code blocks that immediately follow a
Python block and start with an opening fence like this which
has an empty info string.

    ```

A Python code block has no output
if it is followed by any of:

- Python code block
- Python session block
- a fenced code block with a non-empty info string
  
Test code is generated for it, but there will be no
assertion statement.

## skipping blocks

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
- Both Python code and session blocks are searched.
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
- `--skip FIRST` skips the first Python block.
- `--skip SECOND` skips the second Python block.
- `--skip LAST` skips the final Python block.

## --skip

This command
```
phmdoctest doc/example2.md --skip "Python 3.7" --skip LAST --report --outfile test_example2.py
```

Produces the report
```
           doc/example2.md fenced blocks
----------------------------------------------------
block    line  test          matching TEXT pattern
type   number  role          quoted and one per line
----------------------------------------------------
py3         9  code
           14  output
py3        20  skip-code     "Python 3.7"
           26  skip-output
           31  --
py3        37  code
py3        44  code
           51  output
yaml       59  --
text       67  --
py         75  session
py3        87  code
           93  output
pycon     101  skip-session  "LAST"
----------------------------------------------------
5 test cases.
1 skipped code blocks.
1 skipped interactive session blocks.
1 code blocks missing an output block.

  skip pattern matches (blank means no match)
------------------------------------------------
skip pattern  matching code block line number(s)
------------------------------------------------
Python 3.7    20
LAST          101
------------------------------------------------
```
 
and creates the output file [test_example2.py](doc/test_example2_py.md)


## -s short form of --skip

This is the same command as above using the short `-s` form of the --skip option
in two places.
It produces the same report and outfile.
```
phmdoctest doc/example2.md -s "Python 3.7" -sLAST --report --outfile test_example2.py
```

## --fail-nocode

This option produces a pytest file that will always
fail when no Python code or session blocks are found.

If no Python code or session blocks are found in the
Markdown file a pytest file is still generated.
This also happens when `--skip` eliminates all the
Python code blocks. 
The generated pytest file will have the function
`def test_nothing_passes()`.

If the option `--fail-nocode` is passed the
function is `def test_nothing_fails()` which raises an
assertion. 

## --setup

A single Python code block can assign names visible to
other code blocks by giving the `--setup TEXT` option.
The rules for `TEXT` are the same as for `--skip TEXT` plus...

- Only one block can match `TEXT`.
- The block cannot match a block that is skipped.
- The block cannot be a session block even though session
  blocks are searched for `TEXT`.
- It is ok if the block has an output block. It will be ignored.

The setup block is run by the pytest `setup_module()` fixture
in the generated test file.

Here is an example setup block from 
[setup.md](doc/setup.md):
```py3
import math
mylist = [1, 2, 3]
a, b = 10, 11
def doubler(x):
    return x * 2
```

The `--setup` option modifies the execution context of the
Python code blocks in the Markdown file.
The names `math`, `mylist`, `a`, `b`, and `doubler` are visible
to the other Python code blocks and the objects can be modified.

## --teardown

A single Python code block can supply code run by the pytest
`teardown_module()` fixture. Use the `--teardown TEXT` option.
The rules for `TEXT` are the same as for `--setup` above except
`TEXT` won't match a setup block. 

## Setup example

For the Markdown file [setup.md](doc/setup.md)
run this command to see how the blocks are tested. 

```
phmdoctest doc/setup.md --setup FIRST --teardown LAST --report
```

```
           doc/setup.md fenced blocks
------------------------------------------------
block    line  test      matching TEXT pattern
type   number  role      quoted and one per line
------------------------------------------------
py3         9  setup     "FIRST"
py3        18  code
           25  output
py3        35  code
           40  output
py3        45  code
           49  output
py3        56  teardown  "LAST"
------------------------------------------------
3 test cases.
```

This command
```
phmdoctest doc/setup.md --setup FIRST --teardown LAST --outfile test_setup.py
```
creates the test file
[test_setup.py](doc/test_setup_py.md)

## Setup for sessions
The pytest option `--doctest-modules` is required to 
run doctest on sessions.  Pytest runs doctests in
a separate context.
For more on this see [Execution context](#execution-context) below.

To allow sessions to see the variables assigned by the `--setup`
code block, add the option `--setup-doctest`

Here is an example with setup code and sessions
[setup_doctest.md](doc/setup_doctest.md). The first part
of this file is a copy of setup.md.
Since the sessions are tested in a separate context from the 
code blocks they are placed together at the end of the file.

This command  uses the short form of setup and teardown. -u for up and -d for down.
```
phmdoctest doc/setup_doctest.md -u FIRST -d LAST --setup-doctest --outfile test_setup_doctest.py
```
It creates the test file
[test_setup_doctest.py](doc/test_setup_doctest_py.md)

## Execution context

When run without `--setup`

- pytest and doctest determine the order of test case execution.
- phmdoctest assumes test code and session execution is in file order.
- Test case order is not significant.
- Code and expected output run within a function body of a pytest test case.
- If pytest is invoked with `--doctest-modules`: 
  - Sessions are run in a separate doctest execution context.
  - Otherwise sessions are not run.

#### With `--setup`

- names assigned by setup code are visible to code blocks.
- code blocks can modify the objects created by the setup code. 
- code block test case order is significant.
- session order is not significant.
- If pytest is run with `--doctest-modules`:
  - pytest runs two separate contexts: one for sessions, one for code blocks.
  - setup and teardown code is run twice, once by each context.
  - the names assigned by the setup code block 
    are `are not` visible to the sessions.

#### With `--setup` and `--setup-doctest`
Same as previous section plus:
- the names assigned by the setup code block 
  are visible to the sessions.
- sessions can modify the objects created by the setup code. 
- session order is significant.
- Sessions and code blocks are still running in separate contexts
  isolated from each other.
- A session can't affect a code block and a code block can't affect
  a session.

#### Pytest live logging demos
The live logging demos reveal pytest execution contexts. 
Pytest Live Logs show the
execution order of setup_module(), test cases, sessions, and
teardown_module().
The demos are in one of the Travis CI builds.
- Look for the build log here [Build][12].
- Go to the Python 3.7 build which runs tox.
- Go to the Job Log tab.
- Look for the tox demo environment commands near the end.



## Send outfile to stdout
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
  --outfile TEXT       Write generated test case file to path TEXT. "-" writes
                       to stdout.

  -s, --skip TEXT      Any Python code or interactive session block that
                       contains the substring TEXT is not tested. More than
                       one --skip TEXT is ok. Double quote if TEXT contains
                       spaces. For example --skip="python 3.7" will skip every
                       Python block that contains the substring "python 3.7".
                       If TEXT is one of the 3 capitalized strings FIRST
                       SECOND LAST the first, second, or last Python code or
                       session block in the Markdown file is skipped.

  --report             Show how the Markdown fenced code blocks are used.
  --fail-nocode        This option sets behavior when the Markdown file has no
                       Python fenced code blocks or interactive session blocks
                       or if all such blocks are skipped. When this option is
                       present the generated pytest file has a test function
                       called test_nothing_fails() that will raise an
                       assertion. If this option is not present the generated
                       pytest file has test_nothing_passes() which will never
                       fail.

  -u, --setup TEXT     The Python code block that contains the substring TEXT
                       is run at test module setup time. Variables assigned at
                       the outer level are visible as globals to the other
                       Python code blocks. TEXT should match exactly one code
                       block. If TEXT is one of the 3 capitalized strings
                       FIRST SECOND LAST the first, second, or last Python
                       code or session block in the Markdown file is matched.
                       A block will not match --setup if it matches --skip, or
                       if it is a session block. Use --setup-doctest below to
                       grant Python sessions access to the globals.

  -d, --teardown TEXT  The Python code block that contains the substring TEXT
                       is run at test module teardown time. TEXT should match
                       exactly one code block. If TEXT is one of the 3
                       capitalized strings FIRST SECOND LAST the first,
                       second, or last Python code or session block in the
                       Markdown file is matched. A block will not match
                       --teardown if it matches either --skip or --setup, or
                       if it is a session block.

  --setup-doctest      Make globals created by the --setup Python code block
                       visible to session blocks and only when they are tested
                       with the pytest --doctest-modules option.  Please note
                       that pytest runs doctests in a separate context that
                       only runs doctests. This option is ignored if there is
                       no --setup option.

  --version            Show the version and exit.
  --help               Show this message and exit.
```

## Run on Travis CI  

The partial script shown below is for Python 3.5 on [Travis CI][5].
The script steps are:

- Install phmdoctest (the ".") and install pytest.
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
        - phmdoctest project.md --report --outfile tests/tmp/test_project.py
        - pytest --doctest-modules -vv tests
```

## Run as a Python module

To run phmdoctest from the command line a Python module:

`python -m phmdoctest doc/example2.md --report`

## Call from Python

To call phmdoctest from within a Python script
`phmdoctest.simulator` offers the function `run_and_pytest()`.
It simulates running phmdoctest from the command line.
- useful during development
- creates the --outfile in a temporary directory
- optionally runs pytest on the outfile 

Please see the [Latest Development tools API section][10] or
the docstring of the function `run_and_pytest()` in the file `simulator.py.` 
pytest_options are passed as a list of strings as shown below.

```python
import phmdoctest.simulator
command = 'phmdoctest doc/example1.md --report --outfile test_me.py'
simulator_status = phmdoctest.simulator.run_and_pytest(
    well_formed_command=command,
    pytest_options=['--doctest-modules', '-v']
)
assert simulator_status.runner_status.exit_code == 0
assert simulator_status.pytest_exit_code == 0
```

## Hints

- To read the Markdown file from the standard input stream.
  Use `-` for MARKDOWN_FILE.
- Write the test file to a temporary directory so that
  it is always up to date.
- Its easy to use --output by mistake instead of `--outfile`.
- If Python code block has no output, put assert statements in the code.
- Use pytest option `--doctest-modules` to test the sessions. 
- Markdown indented code blocks ([Spec][8] section 4.4) are ignored.
- simulator_status.runner_status.exit_code == 2 is the click 
  command line usage error.
- Since phmdoctest generates code, the input file should be from a trusted
  source.
- An empty code block is given the role `del-code`. It is not tested. 
- Use special TEXT values FIRST, SECOND, LAST for `--setup` 
  and `--teardown` since they only match one block.
- The name `_session_globals` is reserved and should not be
  used in setup blocks.  
  
## Related projects
- rundoc
- byexample
- sphinx.ext.doctest
- sybil
- doxec
- egtest

## Recent changes 
[Recent changes](doc/recent_changes.md)

[3]: https://github.github.com/gfm/#fenced-code-blocks
[11]: https://github.github.com/gfm/#info-string
[10]: https://phmdoctest.readthedocs.io/en/latest/doc/api.html
[7]: https://pypi.org/project/commonmark
[8]: https://spec.commonmark.org
[9]: https://commonmark.org
[4]: https://docs.python.org/3/library/doctest.html
[5]: https://docs.travis-ci.com
[6]: https://pypi.python.org/project/coverage
[12]: https://travis-ci.org/tmarktaylor/phmdoctest