# This is Markdown file mark_example.md
## Fenced code block expected output block pair.

Example code adapted from the Python Tutorial:
```python
squares = [1, 4, 9, 16, 25]
print(squares)
```
expected output:
```
[1, 4, 9, 16, 25]
```

## The code block has 2 directives:

- phmdoctest-label test_datetime
- phmdoctest-mark.slow

The first directive names the generated test function.

The second directive add @pytest.mark.slow decorator. slow is
a pytest user defined marker that is used to select/deselect
test cases using the pytest --marker command line option.

<!--phmdoctest-label test_datetime-->
<!--phmdoctest-mark.slow-->
```python
from datetime import date

d = date.fromordinal(730920)  # 730920th day after 1. 1. 0001
print(d)
```

```
2002-03-11
```

## A doctest session

Example borrowed from Python Standard Library
fractions documentation.

```py
>>> from fractions import Fraction
>>> Fraction(16, -10)
Fraction(-8, 5)
>>> Fraction(123)
Fraction(123, 1)
>>> Fraction()
Fraction(0, 1)
>>> Fraction('3/7')
Fraction(3, 7)
```
