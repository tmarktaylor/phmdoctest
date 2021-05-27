### Skipif directive has non-numeric minor number.

<!--phmdoctest-label test_fstring-->
<!--phmdoctest-mark.skipif<3.A-->
```python
user = 'eric_idle'
print(f"{user=}")
```
```
user='eric_idle'
```
