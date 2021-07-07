### Skipif directive has non-numeric or negative minor number.

<!--phmdoctest-label test_fstring1-->
<!--phmdoctest-mark.skipif<3.A-->
```python
user = 'eric_idle'
print(f"{user=}")
```

```
user='eric_idle'
```

<!--phmdoctest-label test_fstring2-->
<!--phmdoctest-mark.skipif<3.-1-->
```python
user = 'palin'
print(f"{user=}")
```

```
user='palin'
```
