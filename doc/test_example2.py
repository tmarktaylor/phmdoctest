"""pytest file built from tests/example2.md"""


def line_compare_exact(want, got):
    """Line by line helper compare function with assertion for pytest."""
    if want:
        want_lines = want.splitlines()
        got_lines = got.splitlines()
        assert want_lines == got_lines


def test_code_9_output_14(capsys):
    squares = [1, 4, 9, 16, 25]
    print(squares)

    expected_str = """\
[1, 4, 9, 16, 25]
"""
    line_compare_exact(want=expected_str, got=capsys.readouterr().out)


def test_code_37(capsys):
    a, b = 0, 1
    while a < 1000:
        print(a, end=',')
        a, b = b, a+b

    # Caution- no assertions.


def test_code_44_output_51(capsys):
    words = ['cat', 'window', 'defenestrate']
    for w in words:
        print(w, len(w))

    expected_str = """\
cat 3
window 6
defenestrate 12
"""
    line_compare_exact(want=expected_str, got=capsys.readouterr().out)
