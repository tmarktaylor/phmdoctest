#### doc/directive2.md
~~~
# This is Markdown file directive2.md

Directives are HTML comments and are not rendered.
To see the directives press Edit on Github and then
the Raw button.

#### This will be marked as the setup code.
The setup logic makes the names assigned here global to the test module.
The code assigns the names math, mylist, a, b, and the function doubler().
Setup code does not have an output block.
Note the `<!--phmdoctest-setup-->` directive in the Markdown file.
<!--phmdoctest-setup-->
```python
import math

mylist = [1, 2, 3]
a, b = 10, 11

def doubler(x):
    return x * 2
```

#### This test case shows the setup names are visible.
```python
print("math.pi=", round(math.pi, 3))
print(mylist)
print(a, b)
print("doubler(16)=", doubler(16))
```
expected output:
```
math.pi= 3.142
[1, 2, 3]
10 11
doubler(16)= 32
```

#### This test case modifies mylist.
The objects created by the --setup code can be modified
and blocks run afterward will see the changes.  
```python
mylist.append(4)
print(mylist)
```
expected output:
```
[1, 2, 3, 4]
```

#### This test case sees the modified mylist.
```python
print(mylist == [1, 2, 3, 4])
```
expected output:
```
True
```

#### This will be marked as the teardown code.
Teardown code does not have an output block.
Note `<!--phmdoctest-teardown-->` directive in the Markdown file.
<!--phmdoctest-teardown-->
```python
mylist.clear()
assert not mylist, "mylist was not emptied"
```
~~~
This page is created from a Markdown file that contains the contents
of a Markdown source file in a fenced code block.
It shows the HTML comments which are not visible in rendered Markdown.
It is included in the documentation as an example raw Markdown file.
