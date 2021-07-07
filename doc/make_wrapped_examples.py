"""Create Markdown wrappers around the project's example .py files."""
top = "#### <put filename here>\n```python\n"

bottom = """```
This page is created from a Markdown file that contains the contents
of a python source file in a syntax highlighted fenced code block.
It is included in the documentation as an example python file.
"""

raw_top = "#### <put filename here>\n~~~\n"

raw_bottom = """~~~
This page is created from a Markdown file that contains the contents
of a Markdown source file in a fenced code block.
It shows the HTML comments which are not visible in rendered Markdown.
It is included in the documentation as an example raw Markdown file.
"""

text_bottom = """~~~
This page is created from a text file that contains the contents
of a plain text file in a fenced code block.
It is included in the documentation as an example text file.
"""


def nag():
    print("If a new file...")
    print("Consider adding a test case to test_wrapped_examples.py.")
    print("And add to examples.rst")
    print()


def prompt_to_write_file(outfile_name, text):
    if input("ok to write " + outfile_name + " [Y/n]? >> ") == "Y":
        with open(outfile_name, "w", encoding="utf-8") as f:
            print("writing", outfile_name)
            f.write(text)


def wrap_one_file(name):
    text = top.replace("<put filename here>", name)
    with open(name, "r", encoding="utf-8") as f:
        text += f.read()
    text += bottom
    outfile_name = name.replace(".py", "_py.md")
    prompt_to_write_file(outfile_name, text)


def wrap_raw_markdown(name):
    text = raw_top.replace("<put filename here>", name)
    with open(name, "r", encoding="utf-8") as f:
        text += f.read()
    text += raw_bottom
    outfile_name = name.replace(".md", "_raw.md")
    prompt_to_write_file(outfile_name, text)


def wrap_text(name):
    text = raw_top.replace("<put filename here>", name)
    with open(name, "r", encoding="utf-8") as f:
        text += f.read()
    text += text_bottom
    outfile_name = name.replace(".txt", "_txt.md")
    prompt_to_write_file(outfile_name, text)


def main():
    nag()
    # also add a test case to test_wrapped_examples.py.
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


if __name__ == "__main__":
    main()
