"""pytest file built from doc/inline_example.md"""
from phmdoctest.functions import _phm_compare_exact


def test_code_11_output_21_2(capsys):
    def cause_assertion():
        print("before assert...")
        # assert False                  # phmdoctest:omit
        print("after assert.")
        # print("bye")  # phmdoctest:omit

    cause_assertion()

    _phm_expected_str = """\
before assert...
after assert.
"""
    _phm_compare_exact(a=_phm_expected_str, b=capsys.readouterr().out)


def test_code_29_output_52_2(capsys):
    def prints_too_much(condition):
        print("called with", condition)
        # if condition:             # phmdoctest:omit
        #     print("-" * 50)
        #     # note the section continues across blank lines
        #
        #     print("=" * 50)
        #     print("*" * 50)

        # Can't use phmdoctest:omit on the next line because
        # the else: line would get a Python SyntaxError.
        if condition:
            # So use phmdoctest:pass on the next line.
            pass  # print("condition is true")  # phmdoctest:pass
        else:
            print("condition is false")
        print("done")

    prints_too_much(True)
    prints_too_much(False)

    _phm_expected_str = """\
called with True
done
called with False
condition is false
done
"""
    _phm_compare_exact(a=_phm_expected_str, b=capsys.readouterr().out)
