"""Create Markdown wrappers around the project's example .py files."""
top = '#### <put filename here>\n```python3\n'


bottom = """```
This page is created from a Markdown file that contains the contents
of a python source file in a syntax highlighted fenced code block.
It is included in the documentation as an example python file.
"""


def wrap_one_file(name):
    text = top.replace('<put filename here>', name)
    with open(name, 'r', encoding='utf-8') as f:
        text += f.read()
    text += bottom
    outfile_name = name.replace('.py', '_py.md')
    if input('ok to write ' + outfile_name + ' [Y/n]? >> ') == 'Y':
        with open(outfile_name, 'w', encoding='utf-8') as f:
            print('writing', outfile_name)
            f.write(text)


def main():
    # also add a test case to test_wrapped_examples.py.
    wrap_one_file('doc/test_example2.py')
    wrap_one_file('doc/test_setup.py')
    wrap_one_file('doc/test_setup_doctest.py')


if __name__ == '__main__':
    main()
