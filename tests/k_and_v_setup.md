Setup code uses loop variables from functions.setup_module template. 
```py3
v = 'hi'
k = 10
```

#### This test case shows correct values for k, v
Locally when the the for loop in setup_module() exits,
k='k' and v=10.
The globals k, v still have the setup block values and types.
```py3
print(k, v)
```
expected output:
```
10 hi
```
