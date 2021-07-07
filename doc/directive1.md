# This is Markdown file directive1.md

Directives are HTML comments and are not rendered.
To see the directives press Edit on Github and then
the Raw button.

## skip directive. No test case is generated.
It is OK to put a directive above pre-existing HTML comments.
The HTML comments are not visible when Markdown
is rendered for viewing.

<!--phmdoctest-skip-->
<!-- OK if there is more than one HTML comment here -->
<!-- OK if there is a HTML comment here -->
```python
assert False
```

## skip directive on an expected output block.
A test case is generated that runs the code block but does
not check the expected output.
```python
from datetime import date

date.today()
```

<!--phmdoctest-skip-->
```
datetime.date(2021, 4, 18)
```

## skip directive on Python session.

No test case is generated.
<!--phmdoctest-skip-->
```py
>>> print("Hello World!")
incorrect expected output should fail
if test case is generated
```

## mark.skip directive with label directive.
- Use mark.skip on Python code blocks.
  A test case is generated with a @pytest.mark.skip()
  decorator.
- On a code block the label directive gives the
  function name of the generated test case.

<!--phmdoctest-mark.skip-->
<!--phmdoctest-label test_mark_skip-->
```python
print("testing @pytest.mark.skip().")
```
```
incorrect expected output
```

## mark.skipif directive.

Use mark.skipif on Python code blocks.
A test case is generated with a @pytest.mark.skipif(...)
decorator.  This test case will only run when Python
is version 3.8 or higher. f-string support is new in
Python 3.8.

<!--phmdoctest-label test_fstring-->
<!--phmdoctest-mark.skipif<3.8-->
```python
user = "eric_idle"
print(f"{user=}")
```
```
user='eric_idle'
```

## label directive on a session. 
This will generate a test case called 
`test_print_coffee()`.
<!--phmdoctest-label test_print_coffee-->
```py
>>> print("coffee")
coffee
```
