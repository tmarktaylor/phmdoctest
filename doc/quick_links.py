"""Create Markdown links suitable for use as a Quick Links section."""
import re


def remove_fenced_code_blocks(lines, fence='```'):
    """"Return lines not starting with fence or between fences."""
    skipping = False
    for line in lines:
        if skipping and line.startswith(fence):
            skipping = False
            continue

        if not skipping and line.startswith(fence):
            skipping = True
            continue

        if not skipping:
            yield line


paragraph_level = '## '    # note trailing space


def make_quick_links(filename):
    """"Generate links for a quick links section.

    quicklinks_section_heading is case significant
    """
    with open(filename, encoding='utf-8') as f:
        lines = f.readlines()
    lines = [line.rstrip() for line in lines]    # lose newlines
    # README.md has fenced code blocks that enclose other
    # fenced code blocks.  The outer blocks use ~~~ as the fence.
    # Remove the outer fenced code blocks first.
    lines = remove_fenced_code_blocks(lines, '~~~')
    lines = remove_fenced_code_blocks(lines)
    links = []
    for line in lines:
        if line.startswith(paragraph_level):
            title = line.replace(paragraph_level, '')
            label = '[' + title + ']'
            link = title.lower()
            # remove some punctuation chars
            some_punctuation = ','
            link = re.sub('[' + some_punctuation + ']', '', link)
            link = link.replace('-', ' ')
            # convert runs of space to single dash
            link = re.sub('[ ]+', '-', link)
            # remove runs of - at the start of a line
            link = re.sub('^[-]+', '', link)
            link = '(#' + link + ')'
            links.append(label + link)
    text = ' |\n'.join(links)
    print(text)
    print()
    print('created {} links, {} characters'.format(len(links), len(text)))


if __name__ == '__main__':
    make_quick_links('../README.md')