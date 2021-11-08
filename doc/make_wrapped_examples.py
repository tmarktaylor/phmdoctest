"""Create Markdown wrappers around the project's example .py files."""
from pathlib import Path

top = "# <put filename here>\n```python\n"

bottom = """```
The above syntax highlighted fenced code block contains the
contents of a python source file.
It is included in the documentation as an example python file.
"""

raw_top = "# <put filename here>\n~~~\n"

raw_bottom = """~~~
The above fenced code block contains the contents of a Markdown file.
It shows the HTML comments which are not visible in rendered Markdown.
It is included in the documentation as an example raw Markdown file.
"""

text_bottom = """~~~
The above fenced code block contains the contents of a plain text file.
It is included in the documentation as an example text file.
"""


def nag():
    print("If a new file...")
    print("Consider adding a test case to test_wrapped_snippets.py.")
    print("And add to examples.rst")
    print()


def prompt_to_write_file(outfile_name, text):
    if input("ok to write " + outfile_name + " [Y/n]? >> ") == "Y":
        print("writing", outfile_name)
        _ = Path("outfile_name").write_text(text, encoding="utf-8")


def wrap_one_file(name, outname=None):
    text = top.replace("<put filename here>", name)
    text += Path(name).read_text(encoding="utf-8")
    text += bottom
    if outname is not None:
        outfile_name = outname
    else:
        outfile_name = name.replace(".py", "_py.md")
    prompt_to_write_file(outfile_name, text)


def wrap_raw_markdown(name):
    text = raw_top.replace("<put filename here>", name)
    text += Path(name).read_text(encoding="utf-8")
    text += raw_bottom
    outfile_name = name.replace(".md", "_raw.md")
    prompt_to_write_file(outfile_name, text)


def wrap_text(name):
    text = raw_top.replace("<put filename here>", name)
    text += Path(name).read_text(encoding="utf-8")
    text += text_bottom
    outfile_name = name.replace(".txt", "_txt.md")
    prompt_to_write_file(outfile_name, text)


def main():
    nag()
    # also add a test case to test_wrapped_snippets.py.
    wrap_one_file("doc/test_example2.py")
    wrap_one_file("doc/test_setup.py")
    wrap_one_file("doc/test_setup_doctest.py")

    wrap_raw_markdown("doc/directive1.md")
    wrap_one_file("doc/test_directive1.py")
    wrap_text("doc/directive1_report.txt")

    wrap_raw_markdown("doc/directive2.md")
    wrap_one_file("doc/test_directive2.py")
    wrap_text("doc/directive2_report.txt")

    wrap_raw_markdown("doc/directive3.md")
    wrap_one_file("doc/test_directive3.py")
    wrap_text("doc/directive3_report.txt")

    wrap_one_file("doc/test_inline_example.py")
    wrap_one_file("tests/project_test.py", outname="doc/project_test_py.md")


if __name__ == "__main__":
    main()
