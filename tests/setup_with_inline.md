# This is Markdown file setup_with_inline.md

This test shows that inline annotations get processed in
--setup and --teardown blocks.

#### This will be the setup code.

- Use phmdoctest --setup FIRST to select it.
- Setup code does not have an output block.
```py3
mylist = [1, 2, 3]
a, b = 10, 11  # phmdoctest:omit

def raiser():
    assert False  # phmdoctest:pass
```

#### This test case shows the setup names are visible

- The assertion in raiser() did not happen.
- mylist is visible.
```py3

print(mylist)
raiser()
if mylist:                                 # phmdoctest:omit
    print("I should be commented out").
    assert False
```
expected output:
```
[1, 2, 3]
```


#### This will be specified as the teardown code.

- Use phmdoctest --teardown LAST to select it.
- Teardown code does not have an output block.
```py3
mylist.clear()
assert not mylist, "mylist was not emptied"
assert False  # phmdoctest:omit
```
