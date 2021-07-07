# phmdoctest 1.2.1

## Introduction

Python syntax highlighted Markdown doctest

Command line program to test Python syntax highlighted code
examples in Markdown.

- Writes a pytest test file that tests Python examples in
  README and other Markdown files.
- Reads these from Markdown fenced code blocks:
  - Python interactive sessions described by [doctest][4].
  - Python source code and expected terminal output.
- The test cases are run later by calling pytest.  
- Simple use case is possible with no Markdown edits at all.
- More features selected by adding HTML comment **directives**
  to the Markdown.
  - Set test case name.
  - Add a pytest.mark.skip decorator.
  - Promote names defined in a test case to module level globals.
  - Label any fenced code block for later retrieval (API).
- Add inline annotations to comment out sections of code.  
- Get code coverage by running pytest with [coverage][6].
- Select Python source code blocks as setup and teardown code.
- Setup applies to code blocks and optionally to session blocks.
- An included Python library: [Latest Development tools API][10].
  - functions to read fenced code blocks from Markdown. *(tool.py)*
  - runs phmdoctest and can run pytest too. *(simulator.py)*
  - extract testsuite tree and list of failing trees from JUnit XML. *(tool.py)*
  

##### master branch status
[![](https://img.shields.io/pypi/l/phmdoctest.svg)](https://github.com/tmarktaylor/phmdoctest/blob/master/LICENSE.txt)
[![](https://img.shields.io/pypi/v/phmdoctest.svg)](https://pypi.python.org/pypi/phmdoctest)
[![](https://img.shields.io/pypi/pyversions/phmdoctest.svg)](https://pypi.python.org/pypi/phmdoctest)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

[![Usage Test](https://github.com/tmarktaylor/phmdoctest/actions/workflows/install.yml/badge.svg)](https://github.com/tmarktaylor/phmdoctest/actions/workflows/install.yml)
[![CI Test](https://github.com/tmarktaylor/phmdoctest/actions/workflows/ci.yml/badge.svg)](https://github.com/tmarktaylor/phmdoctest/actions/workflows/ci.yml)
[![](https://readthedocs.org/projects/phmdoctest/badge/?version=latest)](https://phmdoctest.readthedocs.io/en/latest/?badge=latest)
[![](https://codecov.io/gh/tmarktaylor/phmdoctest/coverage.svg?branch=master)](https://codecov.io/gh/tmarktaylor/phmdoctest?branch=master)

[Website](https://tmarktaylor.github.io/phmdoctest) |
[Docs](https://phmdoctest.readthedocs.io/en/latest/) |
[Repos](https://github.com/tmarktaylor/phmdoctest) |
[Build][12] |
[Codecov](https://codecov.io/gh/tmarktaylor/phmdoctest?branch=master) |
[License](https://github.com/tmarktaylor/phmdoctest/blob/master/LICENSE.txt)


[Introduction](#introduction) |
[Installation](#installation) |
[Sample Usage](#sample-usage) |
[Sample usage without directives](#sample-usage-without-directives) |
[--report](#--report) |
[Identifying blocks](#identifying-blocks) |
[Directives](#directives) |
[skip](#skip) |
[label on code and sessions](#label-on-code-and-sessions) |
[label on any fenced code block](#label-on-any-fenced-code-block) |
[pytest skip](#pytest-skip) |
[pytest skipif](#pytest-skipif) |
[setup](#setup) |
[teardown](#teardown) |
[share-names](#share-names) |
[clear-names](#clear-names) |
[label skip and mark example](#label-skip-and-mark-example) |
[setup and teardown example](#setup-and-teardown-example) |
[share-names clear-names example](#share-names-clear-names-example) |
[Inline annotations](#inline-annotations) |
[skipping blocks with --skip](#skipping-blocks-with---skip) |
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
[Run as a Python module](#run-as-a-python-module) |
[Call from Python](#call-from-python) |
[Hints](#hints) |
[Directive hints](#directive-hints) |
[Related projects](#related-projects)



[Changes](doc/recent_changes.md) |
[Contributions](CONTRIBUTING.md) |
[About](doc/about.md)


## Installation
It is advisable to install in a virtual environment.

    python -m pip install phmdoctest

## Sample Usage

Given the Markdown file shown in raw form here...
<!--phmdoctest-label directive-example-raw-->
~~~
<!--phmdoctest-mark.skip-->
<!--phmdoctest-label test_example-->
```python
print("Hello World!")
```
```
incorrect expected output
```
~~~

the command...
<!--phmdoctest-label directive-example-command-->
```
phmdoctest tests/one_mark_skip.md --outfile test_one_mark_skip.py
```

creates the python source code file shown here...
<!--phmdoctest-label directive-example-outfile-->
```python
"""pytest file built from tests/one_mark_skip.md"""
import pytest

from phmdoctest.functions import _phm_compare_exact


@pytest.mark.skip()
def test_example(capsys):
    print("Hello World!")

    _phm_expected_str = """\
incorrect expected output
"""
    _phm_compare_exact(a=_phm_expected_str, b=capsys.readouterr().out)
```

Run the --outfile with pytest...
```
$ pytest -vv test_one_mark_skip.py

test_one_mark_skip.py::test_example SKIPPED 
```

- The HTML comments in the Markdown are phmdoctest **directives**.
- The mark.skip directive adds the @pytest.mark.skip() line.
- The label directive names the test case function.
- List of  [Directives](#directives)
- Directives are not required.


## Sample usage without directives

Given the Markdown file [example1.md](doc/example1.md)
shown in raw form here...

<!--phmdoctest-label example1-raw-->
~~~
# This is Markdown file example1.md

## Interactive Python session (doctest)

```py 
>>> print("Hello World!")
Hello World!
```

## Source Code and terminal output
 
Code:
```python
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
<!--phmdoctest-label example1-command-->
```
phmdoctest doc/example1.md --outfile test_example1.py
```

creates the python source code file `test_example1.py` shown here...

<!--phmdoctest-label example1-outfile-->
```python
"""pytest file built from doc/example1.md"""
from phmdoctest.functions import _phm_compare_exact


def session_00001_line_6():
    r"""
    >>> print("Hello World!")
    Hello World!
    """


def test_code_14_output_28(capsys):
    from enum import Enum

    class Floats(Enum):
        APPLES = 1
        CIDER = 2
        CHERRIES = 3
        ADUCK = 4

    for floater in Floats:
        print(floater)

    _phm_expected_str = """\
Floats.APPLES
Floats.CIDER
Floats.CHERRIES
Floats.ADUCK
"""
    _phm_compare_exact(a=_phm_expected_str, b=capsys.readouterr().out)
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

The `14` in the function name `test_code_14_output_28` is the
line number of the first line
of python code. `28` shows the line number of the expected 
terminal output.

One test case function is generated for each: 

- Markdown fenced code block interactive session 
- Python-code/expected-output Markdown fenced code block pair

The `--report` option below shows the blocks discovered and
how they are tested.
   
## --report

To see the [GFM fenced code blocks][3] in the MARKDOWN_FILE use the 
`--report` option like this:

<!--phmdoctest-label report-command-->
```
phmdoctest doc/example2.md --report
```

which lists the fenced code blocks it found in
the file [example2.md](doc/example2.md).
The `test role` column shows how each fenced code block is tested.  

<!--phmdoctest-label example2-report-->
```
         doc/example2.md fenced blocks
------------------------------------------------
block     line  test     TEXT or directive
type    number  role     quoted and one per line
------------------------------------------------
python       9  code
            14  output
python      20  code
            26  output
            31  --
python      37  code
python      44  code
            51  output
yaml        59  --
text        67  --
py          75  session
python      87  code
            94  output
py         102  session
------------------------------------------------
7 test cases.
1 code blocks with no output block.
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

plus the block contents can't start with `'>>> '`.

The examples use the info_strings `python` for code and `py` for sessions
since they render with coloring on GitHub, readthedocs, GitHub Pages,
and Python package index.

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

## Directives

Directives are HTML comments containing test generation commands.
They are edited into the Markdown file immediately before a fenced
code block. It is OK if other HTML comments are present.
The `<!--phmdoctest-skip-->` directive is shown in the
raw Markdown below.
With the skip directive no test code will be
generated from the fenced code block.

<!--phmdoctest-label intro-to-directives-->
~~~
<!--phmdoctest-skip-->
<!--Another HTML comment-->
```python
print("Hello World!")
```
Expected Output
```
Hello World!
```
~~~

List of Directives
```
       Directive HTML comment      |    Use on blocks
---------------------------------- | ---------------------
<!--phmdoctest-skip-->             | code, session, output
<!--phmdoctest-label IDENTIFIER--> | code, session
<!--phmdoctest-label TEXT-->       | any
<!--phmdoctest-mark.skip-->        | code
<!--phmdoctest-mark.skipif<3.N-->  | code
<!--phmdoctest-setup-->            | code
<!--phmdoctest-teardown-->         | code 
<!--phmdoctest-share-names-->      | code
<!--phmdoctest-clear-names-->      | code
```

[Directive hints](#directive-hints)

## skip
The skip directive or `--skip TEXT` command line option 
prevents code generation for the code or session block.
The skip directive can be placed on an expected output block.
There it prevents checking expected against actual output.
[Example.](#label-skip-and-mark-example)

## label on code and sessions
When used on a Python code block or session the label directive
changes the name of the generated test function.
[Example.](#label-skip-and-mark-example)
Two generated tests, the first without a label,
shown in pytest -v terminal output:

```
test_readme.py::test_code_93 FAILED 
test_readme.py::test_beta_feature FAILED
``` 

## label on any fenced code block
On any fenced code block, the label directive identifies the block
for later retrieval by the class `phmdoctest.tool.FCBChooser()`.
The `FCBChooser` is used separately from phmdoctest in
a different pytest file. This allows the test developer to write
additional test cases for fenced code blocks that are not handled by
phmdoctest. The directive value can be any string.

<!--phmdoctest-label my-markdown-file-->
~~~
### This is file doc/my_markdown_file.md

<!--phmdoctest-label my-fenced-code-block-->
```
The label directive can be placed on any fenced code block.
```
~~~
Here is Python code to fetch it:

<!--phmdoctest-label fetch-it-->
```python
import phmdoctest.tool

chooser = phmdoctest.tool.FCBChooser("doc/my_markdown_file.md")
text = chooser.contents(label="my-fenced-code-block")
print(text)
```
Output:

<!--phmdoctest-label fetched-contents-->
```
The label directive can be placed on any fenced code block.
```

## pytest skip
The `<!--phmdoctest-mark.skip-->`  directive generates a test
case with a `@pytest.mark.skip()` decorator. 
[Example.](#label-skip-and-mark-example)


## pytest skipif
The `<!--phmdoctest-mark.skipif<3.N-->`  directive generates 
a test case with the pytest decorator
`@pytest.mark.skipif(sys.version_info < (3, N), reason="requires >=py3.N")`.
N is a Python minor version number.
[Example.](#label-skip-and-mark-example)

## setup
A single Python code block can assign names visible to
other code blocks by adding a setup directive or
using the [--setup](#--setup) command line option.

Names assigned by the setup block
are copied to the test module's global namespace after
the setup block runs.

Here is an example setup block from 
[setup.md](doc/setup.md):
<!--phmdoctest-label setup-md-first-block-->
```python
import math

mylist = [1, 2, 3]
a, b = 10, 11

def doubler(x):
    return x * 2
```

Using setup modifies the execution context of the
Python code blocks in the Markdown file.
The names `math`, `mylist`, `a`, `b`, and `doubler` are visible
to the other Python code blocks. The objects can be modified.
[Example.](#setup-and-teardown-example)

## teardown
Selects a single Python code block that runs
at test module teardown time.
A teardown block can also be designated
using the [--teardown](#--teardown) command line option.
[Example.](#setup-and-teardown-example)
 
## share-names
Names assigned by the Python code block are copied to
the test module as globals after the test code runs. This happens at run
time. These names are now visible to subsequent 
test cases generated for Python code blocks in the Markdown file.
share-names modifies the execution context as described for
the setup directive above.
The share-names directive can be used on more than one
code block.
[Example.](#share-names-clear-names-example)

This directive effectively joins its Python code block to the
following Python code blocks in the Markdown file. 

## clear-names
After the test case generated for the Python code block
with the clear-names directive runs, all names that were
created by one or more preceding share-names directives
are deleted. The names that were shared are no longer visible.
This directive also deletes the names assigned by setup.
[Example.](#share-names-clear-names-example)

## label skip and mark example
The file [directive1.md](doc/directive1_raw.md) contains
example usage of label, skip, and mark directives.
The command below generates
[test_directive1.py](doc/test_directive1_py.md).
`phmdoctest doc/directive1.md --report`
produces this
[report](doc/directive1_report_txt.md).

<!--phmdoctest-label directive-1-outfile-->
```
phmdoctest doc/directive1.md --outfile test_directive1.py
```


## setup and teardown example
The file [directive2.md](doc/directive2_raw.md) contains
example usage of label, skip, and mark directives. 
The command below generates
[test_directive2.py](doc/test_directive2_py.md).
`phmdoctest doc/directive2.md --report`
produces this
[report](doc/directive2_report_txt.md).

<!--phmdoctest-label directive-2-outfile-->
```
phmdoctest doc/directive2.md --outfile test_directive2.py
```

## share-names clear-names example
The file [directive3.md](doc/directive3_raw.md) contains
example usage of share-names and clear-names directives. 
The command below generates
[test_directive3.py](doc/test_directive3_py.md).
`phmdoctest doc/directive3.md --report`
produces this
[report](doc/directive3_report_txt.md).
<!--phmdoctest-label directive-3-outfile-->
```
phmdoctest doc/directive3.md --outfile test_directive3.py
```


## Inline annotations

Inline annotations comment out sections of code.
They can be added to the end of lines in Python code blocks.
They should be in a comment. 

- `phmdoctest:omit` comments out a section of code.  The line it is on, 
  plus following lines at greater indent are commented out.
- `phmdoctest:pass` comments out one line of code and prepends the pass statement.

Here is a snippet showing how to place `phmdoctest:pass` in the code.
The second block shows the code that is generated. Note there is no `#`
immediately before `phmdoctest:pass`. It is not required.
<!--phmdoctest-label pass-code-->
```python
import time
def takes_too_long():
    time.sleep(100)    # delay for awhile. phmdoctest:pass
takes_too_long()
```

<!--phmdoctest-label pass-result-->
```python
import time
def takes_too_long():
    pass  # time.sleep(100)    # delay for awhile. phmdoctest:pass
takes_too_long()
```

Use `phmdoctest:omit` on single or multi-line statements. Note that two
time.sleep(99) calls were commented out. They follow and are indented more
that the `if condition:`line with `phmdoctest:omit`.

<!--phmdoctest-label omit-code-->
```python
import time                      # phmdoctest:omit

condition = True
if condition:       # phmdoctest:omit
    time.sleep(99)
    time.sleep(99)
```

<!--phmdoctest-label omit-result-->
```python
# import time                      # phmdoctest:omit

condition = True
# if condition:       # phmdoctest:omit
#     time.sleep(99)
#     time.sleep(99)
```

Inline annotation processing counts the number of commented
out sections and adds the count as the suffix 
`_N` to the name of the pytest function in the
generated test file.

Inline annotations are similar, but less powerful
than the Python standard library **doctest** directive `#doctest+SKIP`.
Improper use of `phmdoctest:omit` can cause Python syntax errors.

The examples above are snippets that illustrate how to
use inline annotations. 
Here is an example that produces a pytest file from Markdown.
The command below takes [inline_example.md](doc/inline_example.md) and generates
[test_inline_example.py](doc/test_inline_example_py.md).
<!--phmdoctest-label inline-outfile-->
```
phmdoctest doc/inline_example.md --outfile test_inline_example.py
```


## skipping blocks with --skip

If you don't want to generate test cases for Python
blocks precede the block with a **skip** directive or
use the `--skip TEXT` option. More than one **skip** directive 
or`--skip TEXT`is allowed.

The following describes using `--skip TEXT`.  
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

<!--phmdoctest-label skip-command-->
```
phmdoctest doc/example2.md --skip "Python 3.7" --skip LAST --report --outfile test_example2.py
```

Produces the report

<!--phmdoctest-label skip-report-->
```
            doc/example2.md fenced blocks
-----------------------------------------------------
block     line  test          TEXT or directive
type    number  role          quoted and one per line
-----------------------------------------------------
python       9  code
            14  output
python      20  skip-code     "Python 3.7"
            26  skip-output
            31  --
python      37  code
python      44  code
            51  output
yaml        59  --
text        67  --
py          75  session
python      87  code
            94  output
py         102  skip-session  "LAST"
-----------------------------------------------------
5 test cases.
1 skipped code blocks.
1 skipped interactive session blocks.
1 code blocks with no output block.

  skip pattern matches (blank means no match)
------------------------------------------------
skip pattern  matching code block line number(s)
------------------------------------------------
Python 3.7    20
LAST          102
------------------------------------------------
```
 
and creates the output file [test_example2.py](doc/test_example2_py.md)


## -s short form of --skip

This is the same command as above using the short `-s` form of the --skip option
in two places.
It produces the same report and outfile.
<!--phmdoctest-label short-skip-command-->
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
Please see the [setup](#setup) directive above.
The rules for `TEXT` are the same as for `--skip TEXT` plus...

- Only one block can match `TEXT`.
- The block cannot match a block that is skipped.
- The block cannot be a session block even though session
  blocks are searched for `TEXT`.
- It is ok if the block has an output block. It will be ignored.


## --teardown

A single Python code block can supply code run by the pytest
`teardown_module()` fixture. Use the `--teardown TEXT` option.
Please see the [teardown](#teardown) directive above.
The rules for `TEXT` are the same as for `--setup` above except
`TEXT` won't match a setup block. 

## Setup example

For the Markdown file [setup.md](doc/setup.md)
run this command to see how the blocks are tested. 

<!--phmdoctest-label setup-command-report-->
```
phmdoctest doc/setup.md --setup FIRST --teardown LAST --report
```

<!--phmdoctest-label setup-report-->
```
            doc/setup.md fenced blocks
-------------------------------------------------
block     line  test      TEXT or directive
type    number  role      quoted and one per line
-------------------------------------------------
python       9  setup     "FIRST"
python      20  code
            27  output
python      37  code
            42  output
python      47  code
            51  output
python      58  teardown  "LAST"
-------------------------------------------------
3 test cases.
```

This command
<!--phmdoctest-label setup-command-outfile-->
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

This command  uses the short form of setup and teardown. 
-u for set**up** and -d for tear**down**.
<!--phmdoctest-label setup-doctest-outfile-->
```
phmdoctest doc/setup_doctest.md -u FIRST -d LAST --setup-doctest --outfile test_setup_doctest.py
```
It creates the test file
[test_setup_doctest.py](doc/test_setup_doctest_py.md)

## Execution context

When run without `--setup`

- Pytest and doctest determine the order of test case execution.
- phmdoctest assumes test code and session execution is in file order.
- Test case order is not significant.
- Code and expected output run within a function body of a pytest test case.
- If pytest is invoked with `--doctest-modules`: 
  - Sessions are run in a separate doctest execution context.
  - Otherwise sessions are not run.

#### With `--setup`

- Names assigned by setup code are visible to code blocks.
- Code blocks can modify the objects created by the setup code. 
- Code block test case order is significant.
- Session order is not significant.
- If pytest is run with `--doctest-modules`:
  - pytest runs two separate contexts: one for sessions, one for code blocks.
  - setup and teardown code is run twice, once by each context.
  - the names assigned by the setup code block 
    are `are not` visible to the sessions.

#### With `share-names`
- Only following code blocks can modify the shared objects.
- Shared objects will **not** be visible to sessions 
  if pytest is run with `--doctest-modules`.
- After running a code block with `clear-names`
  - Shared objects will no longer be visible.
  - Names assigned by setup code will no longer be visible.
  
#### With `--setup` and `--setup-doctest`
Same as the setup section plus:
- names assigned by the setup code block 
  are visible to the sessions.
- Sessions can modify the objects created by the setup code. 
- Session order is significant.
- Sessions and code blocks are still running in separate contexts
  isolated from each other.
- A session can't affect a code block and a code block can't affect
  a session.
- Names assigned by the setup code block are globally visible
  to the entire test suite via the Pytest doctest_namespace
  fixture.  See hint near the end [Hints](#Hints).

#### Pytest live logging demos
The live logging demos reveal pytest execution contexts. 
Pytest Live Logs show the
execution order of setup_module(), test cases, sessions, and
teardown_module().
The demos are in one of the Travis CI builds.
- Look for the build log here [Build][12].
- Go to last job called Pytest Live Log Demo.
- Go to the Job Log tab.

There are 2 more demo invocations in the workflow action
called Pytest Live Log Demo.  


## Send outfile to stdout
To redirect the above outfile to the standard output stream use one
of these two commands.

Be sure to leave out `--report` when sending --outfile to standard output.
<!--phmdoctest-label outfile-dash1-->
```
phmdoctest doc/example2.md -s "Python 3.7" -sLAST --outfile -
```
or
<!--phmdoctest-label outfile-dash2-->
```
phmdoctest doc/example2.md -s "Python 3.7" -sLAST --outfile=-
```

## Usage

`phmdoctest --help`

<!--phmdoctest-label usage-->
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

--setup-doctest        Make globals created by the --setup Python code block
                       or setup directive visible to session blocks and only
                       when they are tested with the pytest --doctest-modules
                       option.  Please note that pytest runs doctests in a
                       separate context that only runs doctests. This option
                       is ignored if there is no --setup option.
                       
  --version            Show the version and exit.
  --help               Show this message and exit.
```

## Run as a Python module

To run phmdoctest from the command line:

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

<!--phmdoctest-label simulator-->
```python
import phmdoctest.simulator

command = "phmdoctest doc/example1.md --report --outfile test_me.py"
simulator_status = phmdoctest.simulator.run_and_pytest(
    well_formed_command=command, pytest_options=["--doctest-modules", "-v"]
)
assert simulator_status.runner_status.exit_code == 0
assert simulator_status.pytest_exit_code == 0
```

## Hints

- To read the Markdown file from the standard input stream.
  Use `-` for MARKDOWN_FILE.
- Write the test file to a temporary directory so that
  it is always up to date.
- It is easy to use --output by mistake instead of `--outfile`.
- If Python code block has no output, put assert statements in the code.
- Use pytest option `--doctest-modules` to test the sessions. 
- Markdown indented code blocks ([Spec][8] section 4.4) are ignored.
- simulator_status.runner_status.exit_code == 2 is the click 
  command line usage error.
- Since phmdoctest generates code, the input file should be from a trusted
  source.
- An empty code block is given the role `del-code`. It is not tested. 
- Use special TEXT values FIRST, SECOND, LAST for the command
  line options `--setup` and `--teardown` since they only match one block.
- The variable names `managenamespace`, `doctest_namespace`,
  `capsys`, and `_phm_expected_str` should not be used in 
  Markdown Python code blocks since they may be used in generated code.
- Setup and teardown code blocks cannot have expected output.  
- To have pytest collect a code block with the label directive
  start the value with `test_`.
- With the `--setup-doctest` option, names assigned by the setup code
  block are globally visible to the entire test suite.
  This is due to the scope of the Pytest doctest_namespace
  fixture.  Using a separate pytest command to test
  just the phmdoctest test file is recommended.
- The module phmdoctest.fixture is imported at pytest time
  to support setup, teardown, share-names, and clear-names features. 

## Directive hints

- Only put one of setup, teardown, share-names, or 
  clear-names on a code block.
- Only one block can be setup. Only one block can be teardown.
- The setup or teardown block can't have an expected output block.  
- Label directive may be used, but does not generate a test
  case name on setup and teardown blocks.
- Directives displayed in the `--report` start with a dash like
  this: `-label test_fstring`.
- Code generated by Python blocks with setup and teardown
  directives runs at the pytest fixture `scope="module"` level. 
- Code generated by Python blocks with share-names and
  clear-names directives are **collected** and run by pytest
  like any other test case. 
- A malformed HTML comment ending is bad. Make sure
  it ends with both dashes like `-->`.  Running with `--report`
  will expose that problem.
- The setup, teardown, share-names, and clear-names directives
  have logging. To see the log messages,
  run pytest with the option:
  `--log-cli-level=DEBUG --color=yes`
- There is no limit to number of blank lines after
  the directive HTML comment but before the fenced code block.
  
## Related projects
- rundoc
- byexample
- sphinx.ext.doctest
- sybil
- doxec
- egtest
- pytest-codeblocks

[3]: https://github.github.com/gfm/#fenced-code-blocks
[11]: https://github.github.com/gfm/#info-string
[10]: https://phmdoctest.readthedocs.io/en/latest/doc/api.html
[7]: https://pypi.org/project/commonmark
[8]: https://spec.commonmark.org
[9]: https://commonmark.org
[4]: https://docs.python.org/3/library/doctest.html
[6]: https://pypi.python.org/project/coverage
[12]: https://travis-ci.com/tmarktaylor/phmdoctest
