# This is Markdown file inline_example.md

To comment out sections of Python code blocks use inline annotations.

- phmdoctest:pass
- phmdoctest:omit

This example shows use of phmdoctest:omit to comment out one line
at a time in two places.
```python
def cause_assertion():
    print("before assert...")
    assert False                  # phmdoctest:omit
    print("after assert.")
    print("bye")  # phmdoctest:omit

cause_assertion()
```
Expected output:
```
before assert...
after assert.
```

This example shows use of phmdoctest:omit to comment out an
indented section.

```python
def prints_too_much(condition):
    print("called with", condition)
    if condition:             # phmdoctest:omit
        print("-" * 50)
        # note the section continues across blank lines

        print("=" * 50)
        print("*" * 50)

    # Can't use phmdoctest:omit on the next line because
    # the else: line would get a Python SyntaxError.
    if condition:
        # So use phmdoctest:pass on the next line.
        print("condition is true")  # phmdoctest:pass
    else:
        print("condition is false")
    print("done")

prints_too_much(True)
prints_too_much(False)
```
Expected output:
```
called with True
done
called with False
condition is false
done
```
