# This is Markdown file example2.md
## Fenced code block expected output block pair.
In order for phmdoctest to work with Python source code and
terminal output add print statements to the
source code to produce the expected output.

Example code adapted from the Python Tutorial:
```python
squares = [1, 4, 9, 16, 25]
print(squares)
```
expected output:
```
[1, 4, 9, 16, 25]
```

## Another fenced code block expected output block pair.
Example code adapted from What's new in Python:
```python
# Formatted string literals require Python 3.7
name = "Fred"
print(f"He said his name is {name}.")
```
expected output:
```
He said his name is Fred.
```

## Here is a second fenced code block with no info string.
```
doesn't have an info string
```

## Here are two Python code blocks in a row and one output block at the end.
The first one:
```python
a, b = 0, 1
while a < 1000:
    print(a, end=",")
    a, b = b, a + b
```
The second one. This means the preceding code block has no output block.
```python
words = ["cat", "window", "defenestrate"]
for w in words:
    print(w, len(w))
```
The expected output block for the second code block:

```
cat 3
window 6
defenestrate 12
```

## A fenced code block with yaml info string.

```yaml
dist: xenial
language: python
sudo: false
```

## A fenced block with text info string

```text
some text
```

## A doctest session
Here is a Python interactive session.  It is described by
the Python Standard Library module doctest.  Note there is
no need for an empty line at the end of the session.
```py
>>> a = "Greetings Planet!"
>>> a
'Greetings Planet!'
>>> b = 12
>>> b
12
```

## One more code plus expected output pair.

Example borrowed from Python Standard Library datetime documentation.
```python
from datetime import date

d = date.fromordinal(730920)  # 730920th day after 1. 1. 0001
print(d)
```

```
2002-03-11
```

## Another doctest session (skipped in test_example2.py)

Example borrowed from Python Standard Library
fractions documentation.
```py
>>> from fractions import Fraction
>>> Fraction(16, -10)
Fraction(-8, 5)
>>> Fraction(123)
Fraction(123, 1)
>>> Fraction()
Fraction(0, 1)
>>> Fraction('3/7')
Fraction(3, 7)
```
