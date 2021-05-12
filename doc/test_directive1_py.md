#### doc/test_directive1.py
```python3
"""pytest file built from doc/directive1.md"""
import sys

import pytest

from phmdoctest.functions import _phm_compare_exact


def test_code_23_output_29():
    from datetime import date
    date.today()

    # Caution- no assertions.


@pytest.mark.skip()
def test_mark_skip(capsys):
    print('testing @pytest.mark.skip().')

    _phm_expected_str = """\
incorrect expected output
"""
    _phm_compare_exact(a=_phm_expected_str, b=capsys.readouterr().out)


@pytest.mark.skipif(sys.version_info < (3, 8), reason="requires >=py3.8")
def test_fstring(capsys):
    user = 'eric_idle'
    print(f'{user=}')

    _phm_expected_str = """\
user='eric_idle'
"""
    _phm_compare_exact(a=_phm_expected_str, b=capsys.readouterr().out)


def test_print_coffee():
    r"""
    >>> print('coffee')
    coffee
    """
```
This page is created from a Markdown file that contains the contents
of a python source file in a syntax highlighted fenced code block.
It is included in the documentation as an example python file.