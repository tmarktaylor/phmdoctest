<!--phmdoctest-skip-->
<!-- an HTML comment -->
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

#### Interactive Python session requires `<BLANKINE>` in the expected output 

Blank lines in the expected output must be replaced with `<BLANKLINE>`.
To see the `<BLANKLINE>` navigate to [project.md unrendered][1]. 


<!-- an HTML comment -->
<!--phmdoctest-skip-->
```pycon
>>> print('Hello\n\nWorld!')
Hello
<BLANKLINE>
World!
```

#### Session with `py` as the fenced code block info_string

<!--phmdoctest-label coffee_session -->
<!-- some other tool -->
<!--phmdoctest-label NO_TRAILING_SPACE-->
<!--phmdoctest-label   EXTRA_SPACES  -->
```pycon
>>> coffee = 5
>>> coding = 5
>>> enjoyment = 10
>>> print(coffee + coding)
10
>>> coffee + coding == enjoyment
True
```

<!--phmdoctest-clear-names-->





```
The phmdoctest-clear-names directive above is seen
even though there are five blank line between it
and the fenced code block.  
```


<!--phmdoctest-clear-names-->
some text that causes backwards marker scan to terminate
```
The phmdoctest-clear-names directive above 
some text is not found by phmdoctest because
it does not immediately precede the fenced code block.
```

<!-- first HTML comment -->
<!-- second HTML comment -->
<!--phmdoctest-setup-->
<!--third HTML comment -->
<!--phmdoctest-teardown-->
<!--phmdoctest-share-names-->
<!--fourth HTML comment -->
<!--fifth HTML comment -->
```python
def greeting(name: str) -> str:
    return 'Hello' + '\n\n' + name
print(greeting('World!'))
```

Here is the output it produces.
<!--phmdoctest-skip-->
```
Hello

World!
```

<!--phmdoctest-mark.skip-->
```python
def greeting(name: str) -> str:
    return 'Hello' + '\n\n' + name
print(greeting('World!'))
```


The next html line breaks the scan for directives
<title>Some non-comment HTML</title>


<!--phmdoctest-mark.skipif<3.8-->
<!--phmdoctest-share-names-->
```python
def greeting(name: str) -> str:
    return 'Hello' + '\n\n' + name
print(greeting('World!'))
```


## This is an example of use of skip and label directives
<!--phmdoctest-setup-->
<!--phmdoctest-label my-hello-world-->
<!--phmdoctest-skip-->
```python
print('Hello World!')
```

```
Hello World!
```

## Skip and label directives on the expected output block
```python
print('Hello World!')
```

<!--phmdoctest-label my-hello-world-output-->
<!--phmdoctest-skip-->
```
Hello World!
```
