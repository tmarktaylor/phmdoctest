# This is Markdown file example2.md
#### Fenced code block expected output block pair.
Since phmdoctest works with Python source code and terminal output there
are no console prompts `>>>` and `...` in the source code and the print()
statement is required to produce the expected output.  

Example code adapted from the Python Tutorial:
```py3
squares = [1, 4, 9, 16, 25]
print(squares)
```
expected output:
```
[1, 4, 9, 16, 25]
```

#### Another fenced code block expected output block pair.
Example code adapted from What's new in Python:
```py3
# Formatted string literals require Python 3.7
name = "Fred"
print(f"He said his name is {name}.")
```
expected output:
```
He said his name is Fred.
```

#### Here is a second fenced code block with no info string.
```
doesn't have an info string
```

#### Here are two Python code blocks in a row and one output block at the end.
The first one:
```py3
a, b = 0, 1
while a < 1000:
    print(a, end=',')
    a, b = b, a+b
```
The second one. This means the preceding code block has no output block.
```py3
words = ['cat', 'window', 'defenestrate']
for w in words:
    print(w, len(w))
```
And the expected output block for the second code block:

```
cat 3
window 6
defenestrate 12
```

#### A fenced code block with yaml info string.

```yaml
dist: xenial
language: python
sudo: false
```

#### A fenced block with text info string

```text
some text
```

#### One more code plus expected output pair.

Example borrowed from Python Standard Library datetime documentation.
```py3
from datetime import date
d = date.fromordinal(730920) # 730920th day after 1. 1. 0001
print(d)
```

```
2002-03-11
```
