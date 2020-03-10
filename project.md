### project.md

This is an example Markdown file placed at the top level
of phmdoctest to be used by the .travis.yml example
in README.md.

It is needed because the test case Python file 
generated from README.md is confusing.

Here is a Python source code example inspired by 
[What’s New In Python 3.5](https://docs/python.org/3/whatsnew/3.5.html#pep-484-type-hints).

```python
# An example with type hints 
def greeting(name: str) -> str:
    return 'Hello ' + name
print(greeting('World'))
```

And the output it produces:
```
Hello World
```

