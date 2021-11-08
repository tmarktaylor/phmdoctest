"""Try generating test file from Markdown with HTML <details></details>.

This will show that the Markdown parser sees the fenced code blocks
between the HTML <details> and </details> tags.
The Markdown file is created in the pytester instance from a
string. Note the leading and trailing blank lines.
My IDE Markdown renderer needed them.
"""

from pathlib import Path

import phmdoctest.main
from _pytest.pytester import RunResult

from phmdoctest.tester import testfile_tester


def nofail_noerror_nowarn(result: RunResult) -> None:
    """Check summary from pytester.runpytest RunResult for success."""
    summary_nouns = result.parse_summary_nouns(result.outlines)
    assert summary_nouns.get("failed", 0) == 0
    assert summary_nouns.get("errors", 0) == 0
    assert summary_nouns.get("warnings", 0) == 0
    assert "passed" in summary_nouns


markdown_file_image = """
# This is Markdown file details.md

## mark.skip directive with label directive.
- Use `mark.skip` on Python code blocks.
  A test case gets generated with a @pytest.mark.skip()
  decorator.
- On a code block the label directive gives the
  function name of the generated test case.

<details>

<!--phmdoctest-mark.skip-->
<!--phmdoctest-label test_mark_skip-->
```python
print("testing @pytest.mark.skip().")
```
```
incorrect expected output
```

</details>


## label directive on a session.
This will generate a test case called `doctest_print_coffee()`.
It does not start with test_ to avoid collection as a test item.
<!--phmdoctest-label doctest_print_coffee-->
```py
>>> print("coffee")
coffee
```
"""


def test_sees_inside_details(testfile_tester):
    """Generate a testfile from Markdown with <details> and pytest it."""
    markdown_filename = "details.md"
    p = Path(markdown_filename)
    p.write_text(markdown_file_image, encoding="utf-8")
    testfile = phmdoctest.main.testfile(
        markdown_file=markdown_filename,
    )
    result = testfile_tester(
        contents=testfile,
        pytest_options=["-v", "--doctest-modules"],
    )
    nofail_noerror_nowarn(result)
    result.assert_outcomes(passed=1, skipped=1)
