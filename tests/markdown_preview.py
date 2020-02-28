from readme_renderer.markdown import render
import sys


def main(filename):
    """Create html from a Markdown file.

    This is useful for manually testing the links.
    Issue- does not syntax highlight the fenced code blocks.
    Issue- does not draw box around fenced code blocks.
    """
    with open(filename) as f:
        d = f.read()
    h = render(d, variant='GFM')
    with open(filename + '.html', 'w') as f2:
        f2.write(h)


if __name__ == '__main__':
    """Render to html the Markdown files passed on the command line."""
    for filename in sys.argv[1:]:
        print('rendering', filename)
        main(filename)
