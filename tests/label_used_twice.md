### Two code blocks use the same label directive value.

<!--phmdoctest-label k_and_v-->
```py3
k = 10
v = 'hi'
print(k, v)
```
expected output:
```
10 hi
```

<!--phmdoctest-label k_and_v-->
```py3
k = 1000
v = 'globe'
print(k, v)
```
expected output:
```
1000 globe
```
