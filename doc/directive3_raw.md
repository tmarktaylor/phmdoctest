# doc/directive3.md
~~~
# This is Markdown file directive3.md

Directives are HTML comments and are not rendered.
To see the directives press Edit on GitHub and then
the Raw button.

## share-names and clear-names directives.

First a normal test case with no directives.
This generates a test case.  The name `not_shared` is local to
the function test_code_13_output_17().
```python
not_shared = "Hello World!"
print(not_shared)
```
```
Hello World!
```

This verifies `not_shared` is not visible.
<!--phmdoctest-label test_not_visible-->
```python
try:
    print(not_shared)
except NameError:
    pass
else:
    assert False, "did not get expected NameError"
```

## Share the names assigned here with later Python code blocks.
The share-names directive makes the names assigned here
global to the test module.  The names are visible to all Python code blocks
occurring later in the Markdown source file. The code assigns the
names string, x, y, z, grades, and the function incrementer().
Place the `<!--phmdoctest-share-names-->` directive in the Markdown file.

<!--phmdoctest-label test_directive_share_names-->
<!--phmdoctest-share-names-->
```python
import string

x, y, z = 77, 88, 99

def incrementer(x):
    return x + 1

grades = ["A", "B", "C"]
```

## This test case shows the shared names are visible.
```python
print("string.digits=", string.digits)
print(incrementer(10))
print(grades)
print(x, y, z)
```
expected output:
```
string.digits= 0123456789
11
['A', 'B', 'C']
77 88 99
```

## This test case modifies grades.
The objects created by the share-names code block can be modified
and blocks run afterward will see the changes.
```python
grades.append("D")
```

## This test case sees the modified grades.
```python
print(grades == ["A", "B", "C", "D"])
```
expected output:
```
True
```

## This test case shares another name.
<!--phmdoctest-share-names-->
```python
hex_digits = string.hexdigits
print(hex_digits)
```

A Python block with the share-names directive can
have an output block.

```
0123456789abcdefABCDEF
```

## Use clear-names directive to un-share.

First notice that hex_digits shared by the last test case
is visible.
The clear-names directive un-shares any previously shared names.
The names will no longer be visible to Python code
blocks occurring later in the Markdown source file.
The clearing does not happen until after the test case runs.
This test case is the same as the previous test case to show
that mylist is still visible.
<!--phmdoctest-clear-names-->
```python
print("Names are cleared after the code runs.")
print(grades == ["A", "B", "C", "D"])
print(hex_digits)
```
expected output:
```
Names are cleared after the code runs.
True
0123456789abcdefABCDEF
```

Here we show that grades and digits are no longer visible.
```python
try:
    print(grades)
except NameError:
    pass
else:
    assert False, "expected NameError for grades"
try:
    print(hex_digits)
except NameError:
    pass
else:
    assert False, "expected NameError for hex_digits"
```
~~~
The above fenced code block contains the contents of a Markdown file.
It shows the HTML comments which are not visible in rendered Markdown.
It is included in the documentation as an example raw Markdown file.
