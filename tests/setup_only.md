#### Setup directive, but not teardown directive.
<!--phmdoctest-setup-->
```py3
import math
mylist = [1, 2, 3]
a, b = 10, 11
def doubler(x):
    return x * 2
```

```py3
print('math.pi=', round(math.pi, 3))
print(mylist)
print(a, b)
print('doubler(16)=', doubler(16))
```
expected output:
```
math.pi= 3.142
[1, 2, 3]
10 11
doubler(16)= 32
```