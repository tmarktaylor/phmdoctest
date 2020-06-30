# This is Markdown file example3.md
#### This is the setup code.
The code creates mylist.
The setup logic makes it global to the test module.
```py3
mylist = [5, 6, 7]
assert mylist, 'mylist is not properly initialized'
```

# todo- test case to assign to a tuple: a, b = 3, 4

#### This test case modifies mylist.
```py3
mylist.append(8)
print(mylist)
```
expected output:
```
[5, 6, 7, 8]
```

#### The next test case sees the modified mylist.
```py3
print(mylist == [5, 6, 7, 8])
```
expected output:
```
True
```

#### The session can't access mylist.
Sessions cannot access the global variables created
by the setup code.  Sessions run in an isolated context.
```py
>>> mylist.append(9)    #doctest:+IGNORE_EXCEPTION_DETAIL
Traceback (most recent call last):
    ...
NameError:
```

#### The teardown code is here.
```py3
mylist.clear()
assert not mylist, 'mylist is not properly destroyed'
```