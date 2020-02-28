"""pytest file built from tests/example1.md"""


def line_compare_exact(want, got):
    """Line by line helper compare function with assertion for pytest."""
    if want:
        want_lines = want.splitlines()
        got_lines = got.splitlines()
        assert want_lines == got_lines


def test_code_3_output_16(capsys):
    from enum import Enum

    class Floats(Enum):
        APPLES = 1
        CIDER = 2
        CHERRIES = 3
        ADUCK = 4
    for floater in Floats:
        print(floater)

    expected_str = """\
Floats.APPLES
Floats.CIDER
Floats.CHERRIES
Floats.ADUCK
"""
    line_compare_exact(want=expected_str, got=capsys.readouterr().out)
