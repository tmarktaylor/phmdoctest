# Examples of code and session blocks

This file (project.md) has some example code and session blocks
including a doctest directive example.

## An example with a blank line in the output

Note no <BLANKLINE> directive in the output block of a Python
code block output block pair.

```python
def greeting(name: str) -> str:
    return 'Hello' + '\n\n' + name
print(greeting('World!'))
```

Here is the output it produces.
```
Hello

World!
```

## Interactive Python session requires `<BLANKINE>` in the expected output

Blank lines in the expected output must be replaced with `<BLANKLINE>`.
To see the `<BLANKLINE>` navigate to [project.md unrendered][1].


```py
>>> print('Hello\n\nWorld!')
Hello
<BLANKLINE>
World!
```

## Interactive Python session with doctest directive

Here is an interactive Python session showing an
expected exception and use of the doctest directive
`IGNORE_EXCEPTION_DETAIL`.
To see the doctest directive navigate to [project.md unrendered][1].


```py
>>> int('def')    #doctest:+IGNORE_EXCEPTION_DETAIL
Traceback (most recent call last):
    ...
ValueError:
```

## Session with `py` as the fenced code block info_string

```py
>>> coffee = 5
>>> coding = 5
>>> enjoyment = 10
>>> print(coffee + coding)
10
>>> coffee + coding == enjoyment
True
```

[1]: https://raw.githubusercontent.com/tmarktaylor/phmdoctest/master/project.md
