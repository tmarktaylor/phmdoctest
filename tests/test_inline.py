import ast

import pytest

import phmdoctest.inline
import verify


def test_starts_with_comment():
    assert phmdoctest.inline.starts_with_comment("#")
    assert phmdoctest.inline.starts_with_comment(" #")
    assert phmdoctest.inline.starts_with_comment("  #")
    assert phmdoctest.inline.starts_with_comment("   #")
    assert phmdoctest.inline.starts_with_comment("    #")
    assert phmdoctest.inline.starts_with_comment("\t #")
    assert phmdoctest.inline.starts_with_comment("#    #")
    assert phmdoctest.inline.starts_with_comment(" \t \n # \n")


def test_not_starts_with_comment():
    assert phmdoctest.inline.starts_with_comment("a#") == False
    assert phmdoctest.inline.starts_with_comment("a #") == False
    assert phmdoctest.inline.starts_with_comment(" b #") == False
    assert phmdoctest.inline.starts_with_comment("  b #") == False
    assert phmdoctest.inline.starts_with_comment("   c #") == False
    assert phmdoctest.inline.starts_with_comment("\t \n    z# \n") == False


def test_num_newlines_at_end():
    assert phmdoctest.inline.num_newlines_at_end("") == 0
    assert phmdoctest.inline.num_newlines_at_end(" ") == 0
    assert phmdoctest.inline.num_newlines_at_end("\n") == 1
    assert phmdoctest.inline.num_newlines_at_end("  \n ") == 0
    assert phmdoctest.inline.num_newlines_at_end("\n \n \n\n") == 2


def test_num_indented():
    assert phmdoctest.inline.num_indented("") == 0
    assert phmdoctest.inline.num_indented(" ") == 0
    assert phmdoctest.inline.num_indented("  ") == 0
    assert phmdoctest.inline.num_indented("   ") == 0
    assert phmdoctest.inline.num_indented("X") == 0
    assert phmdoctest.inline.num_indented(" X") == 1
    assert phmdoctest.inline.num_indented("  X") == 2
    assert phmdoctest.inline.num_indented("   X") == 3
    assert phmdoctest.inline.num_indented("    X") == 4
    assert phmdoctest.inline.num_indented("     X") == 5
    assert phmdoctest.inline.num_indented("X   Y   Z") == 0
    assert phmdoctest.inline.num_indented(" X   Y   Z") == 1
    assert phmdoctest.inline.num_indented("  X   Y   Z") == 2
    assert phmdoctest.inline.num_indented("   X   Y   Z") == 3
    assert phmdoctest.inline.num_indented("    X   Y   Z") == 4
    assert phmdoctest.inline.num_indented("     X   Y   Z") == 5


def test_is_blank():
    assert phmdoctest.inline.isblank("") == True
    assert phmdoctest.inline.isblank(" ") == True
    assert phmdoctest.inline.isblank("\t ") == True
    assert phmdoctest.inline.isblank(" \n ") == True
    assert phmdoctest.inline.isblank("\t\t\t\t") == True
    assert phmdoctest.inline.isblank("A") == False
    assert phmdoctest.inline.isblank("A ") == False
    assert phmdoctest.inline.isblank(" Z") == False
    assert phmdoctest.inline.isblank("       A") == False
    assert phmdoctest.inline.isblank("A       ") == False
    assert phmdoctest.inline.isblank("       Z") == False


def test_is_empty_comment():
    assert phmdoctest.inline.is_empty_comment("#") == True
    assert phmdoctest.inline.is_empty_comment("#    ") == True
    assert phmdoctest.inline.is_empty_comment("    #    ") == True
    assert phmdoctest.inline.is_empty_comment("        #") == True


# Note: The code examples should conform to the Black code style.
# There should be at least 2 spaces before the inline "#".
# There should be 1 space after a start of line # character.
def test_omit_one_line():
    code = """\
def myfunc():
    import math

    mylist = [1, 2, 3]  # phmdoctest:omit
    a, b = 10, 11
"""

    want = """\
def myfunc():
    import math

    # mylist = [1, 2, 3]  # phmdoctest:omit
    a, b = 10, 11
"""

    got, num_changed_sections = phmdoctest.inline.apply_inline_commands(code)
    assert num_changed_sections == 1
    verify.a_and_b_are_the_same(want, got)
    # Make sure the example code and expected result are legal Python.
    # Be aware that this test case will be run on all Python versions
    # supported by phmdoctest.
    ast.parse(code)
    ast.parse(want)


def test_pass_on_last_line():
    code = """\
def myfunc():
    import math

    mylist = [1, 2, 3]
    a, b = 10, 11  # phmdoctest:pass
"""

    want = """\
def myfunc():
    import math

    mylist = [1, 2, 3]
    pass  # a, b = 10, 11  # phmdoctest:pass
"""

    got, num_changed_sections = phmdoctest.inline.apply_inline_commands(code)
    assert num_changed_sections == 1
    verify.a_and_b_are_the_same(want, got)
    ast.parse(code)
    ast.parse(want)


def test_omit_line_before_blank():
    code = """\
def myfunc():
    import math

    mylist = [1, 2, 3]
    a, b = 10, 11          # phmdoctest:omit

    def doubler(x):
        if x > 5:
            x += 2
            #x += 3
            x += 4
        # comment
        return x
"""

    want = """\
def myfunc():
    import math

    mylist = [1, 2, 3]
    # a, b = 10, 11          # phmdoctest:omit

    def doubler(x):
        if x > 5:
            x += 2
            #x += 3
            x += 4
        # comment
        return x
"""

    got, num_changed_sections = phmdoctest.inline.apply_inline_commands(code)
    assert num_changed_sections == 1
    verify.a_and_b_are_the_same(want, got)
    ast.parse(code)
    ast.parse(want)


def test_omit_if_at_bottom():
    code = """\
def myfunc():
    import math

    mylist = [1, 2, 3]
    a, b = 10, 11

    def doubler(x):
        if x > 5:
            x += 2
            #x += 3
            x += 4
        # comment
        return x

        return x * 2

    for item in mylist:
        print(item)
        print(item * 2)

if __name__ == "__main__":   # phmdoctest:omit
    myfunc()        
"""

    want = """\
def myfunc():
    import math

    mylist = [1, 2, 3]
    a, b = 10, 11

    def doubler(x):
        if x > 5:
            x += 2
            #x += 3
            x += 4
        # comment
        return x

        return x * 2

    for item in mylist:
        print(item)
        print(item * 2)

# if __name__ == "__main__":   # phmdoctest:omit
#     myfunc()        
"""

    got, num_changed_sections = phmdoctest.inline.apply_inline_commands(code)
    assert num_changed_sections == 1
    verify.a_and_b_are_the_same(want, got)
    ast.parse(code)
    ast.parse(want)


def test_blankline_in_omitted_pass_ignored():
    code = """\
def myfunc():
    import math

    mylist = [1, 2, 3]
    a, b = 10, 11

    def doubler(x):  # phmdoctest:omit
        if x > 5:
            x += 2
            #x += 3
            x += 4  # phmdoctest:pass
        # comment
        x = 9

        return x * 2

    for item in mylist:
        print(item)
        print(item * 2)

if __name__ == "__main__":
    myfunc()
"""

    want = """\
def myfunc():
    import math

    mylist = [1, 2, 3]
    a, b = 10, 11

    # def doubler(x):  # phmdoctest:omit
    #     if x > 5:
    #         x += 2
    #         #x += 3
    #         x += 4  # phmdoctest:pass
    #     # comment
    #     x = 9
    #
    #     return x * 2

    for item in mylist:
        print(item)
        print(item * 2)

if __name__ == "__main__":
    myfunc()
"""

    got, num_changed_sections = phmdoctest.inline.apply_inline_commands(code)
    assert num_changed_sections == 1
    verify.a_and_b_are_the_same(want, got)
    ast.parse(code)
    ast.parse(want)


def test_omit_to_end():
    code = """\
def myfunc():
    import math

    mylist = [1, 2, 3]
    a, b = 10, 11

    def doubler(x):  # phmdoctest:omit
        if x > 5:
            x += 2
            #x += 3
            x += 4
        # comment
        x = 9

        return x * 2
"""

    want = """\
def myfunc():
    import math

    mylist = [1, 2, 3]
    a, b = 10, 11

    # def doubler(x):  # phmdoctest:omit
    #     if x > 5:
    #         x += 2
    #         #x += 3
    #         x += 4
    #     # comment
    #     x = 9
    #
    #     return x * 2
"""

    got, num_changed_sections = phmdoctest.inline.apply_inline_commands(code)
    assert num_changed_sections == 1
    verify.a_and_b_are_the_same(want, got)
    ast.parse(code)
    ast.parse(want)


def test_pass_on_first_line():
    code = """\
def myfunc():
    import math    # phmdoctest:pass

    mylist = [1, 2, 3]
    a, b = 10, 11

    def doubler(x):
        if x > 5:
            x += 2
            #x += 3
            x += 4
        # comment
        x = 9

        return x * 2

    for item in mylist:
        print(item)
        print(item * 2)

if __name__ == "__main__":
    myfunc()
"""

    want = """\
def myfunc():
    pass  # import math    # phmdoctest:pass

    mylist = [1, 2, 3]
    a, b = 10, 11

    def doubler(x):
        if x > 5:
            x += 2
            #x += 3
            x += 4
        # comment
        x = 9

        return x * 2

    for item in mylist:
        print(item)
        print(item * 2)

if __name__ == "__main__":
    myfunc()
"""

    got, num_changed_sections = phmdoctest.inline.apply_inline_commands(code)
    assert num_changed_sections == 1
    verify.a_and_b_are_the_same(want, got)
    ast.parse(code)
    ast.parse(want)


def test_omit_on_elif():
    code = """\
a = 50
if a < 5:
    c = "good"
elif a < 10:        # phmdoctest:omit
    c = "better"
elif a < 15:
    c = "best"
else:
    c = "mediocre"
"""

    want = """\
a = 50
if a < 5:
    c = "good"
# elif a < 10:        # phmdoctest:omit
#     c = "better"
elif a < 15:
    c = "best"
else:
    c = "mediocre"
"""

    got, num_changed_sections = phmdoctest.inline.apply_inline_commands(code)
    assert num_changed_sections == 1
    verify.a_and_b_are_the_same(want, got)
    ast.parse(code)
    ast.parse(want)


def session_commented_elif_passes():
    r"""\
    >>> a = 50
    >>> if a < 5:
    ...     c = "good"
    ... # elif a < 10:
    ... #     c = "better"
    ... elif a < 15:
    ...     c = "best"
    ... else:
    ...     c = "mediocre"
    """


def test_pass_needed():
    code = """\
a = 10
if a < 5:
    c = "good"  # phmdoctest:pass
elif a < 10:
    c = "better"
elif a < 15:
    c = "best"
else:
    c = "mediocre"
"""

    want = """\
a = 10
if a < 5:
    pass  # c = "good"  # phmdoctest:pass
elif a < 10:
    c = "better"
elif a < 15:
    c = "best"
else:
    c = "mediocre"
"""

    got, num_changed_sections = phmdoctest.inline.apply_inline_commands(code)
    assert num_changed_sections == 1
    verify.a_and_b_are_the_same(want, got)
    ast.parse(code)
    ast.parse(want)


def test_omit_else():
    code = """\
a = 10
if a < 5:
    c = "good"
else:                # phmdoctest:omit
    c = "mediocre"
"""

    want = """\
a = 10
if a < 5:
    c = "good"
# else:                # phmdoctest:omit
#     c = "mediocre"
"""

    got, num_changed_sections = phmdoctest.inline.apply_inline_commands(code)
    assert num_changed_sections == 1
    verify.a_and_b_are_the_same(want, got)
    ast.parse(code)
    ast.parse(want)


def test_omit_if_with_else():
    """It is possible to break the code with a misplaced :omit.
    Here the if part is commented out.
    The commenting stops at the else since it is at the same
    indent level as the if.
    This introduces the syntax error since a statement can't start with else.
    """
    code = """\
a = 10
if a < 5:                # phmdoctest:omit
    c = "good"
else:
    c = "mediocre"
"""

    want = """\
a = 10
# if a < 5:                # phmdoctest:omit
#     c = "good"
else:
    c = "mediocre"
"""

    got, num_changed_sections = phmdoctest.inline.apply_inline_commands(code)
    assert num_changed_sections == 1
    verify.a_and_b_are_the_same(want, got)
    ast.parse(code)
    with pytest.raises(SyntaxError):
        ast.parse(want)


def session_skip_else():
    r"""\
    >>> a = 10
    >>> if a < 5:
    ...     c = "good"
    ... else:  #doctest:+SKIP
    ...     c = "better"
    """


def session_no_pass_needed():
    # Note A phmdoctest:pass must be used where the #doctest:+SKIP
    # shown below works fine.
    r"""\
    >>> a = 0
    >>> if a < 5:
    ...     c = "good"  #doctest:+SKIP
    ... elif a < 10:
    ...     c = "better"
    ... elif a < 15:
    ...     c = "best"
    ... else:
    ...     c = "mediocre"
    """


def session_doctest_skip_elif():
    r"""\
    >>> a = 50
    >>> if a < 5:
    ...     c = "good"
    ... elif a < 10:        #doctest:+SKIP
    ...     c = "better"
    ... elif a < 15:
    ...     c = "best"
    ... else:
    ...     c = "mediocre"
    """


def session_passes():
    r"""\
    >>> a = 50
    >>> if a < 5:
    ...     c = "good"
    ... elif a < 10:
    ...     c = "better"
    ... elif a < 15:
    ...     c = "best"
    ... else:
    ...     c = "mediocre"
    """


def test_no_inline_commands():
    code = """\
def myfunc():
    import math

    mylist = [1, 2, 3]
    a, b = 10, 11

    def doubler(x):
        if x > 5:
            x += 2
            #x += 3
            x += 4
        # comment
        x = 9

        return x * 2

    for item in mylist:
        print(item)
        print(item * 2)

if __name__ == "__main__":
    myfunc()
"""

    want = """\
def myfunc():
    import math

    mylist = [1, 2, 3]
    a, b = 10, 11

    def doubler(x):
        if x > 5:
            x += 2
            #x += 3
            x += 4
        # comment
        x = 9

        return x * 2

    for item in mylist:
        print(item)
        print(item * 2)

if __name__ == "__main__":
    myfunc()
"""

    got, num_changed_sections = phmdoctest.inline.apply_inline_commands(code)
    assert num_changed_sections == 0
    verify.a_and_b_are_the_same(want, got)
    ast.parse(code)
    ast.parse(want)
