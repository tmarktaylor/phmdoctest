# This is Markdown file tests/ignored_directives.md

Example borrowed from Python Standard Library
fractions documentation.

Here are some phmdoctest directives that don't work on doctests.
They are ignored and reported as such.

<!--phmdoctest-mark.skip-->
<!--phmdoctest-share-names-->
<!--phmdoctest-mark.slow-->
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
