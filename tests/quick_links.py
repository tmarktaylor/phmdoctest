"""Create Markdown links suitable for use as a Quick Links section."""
import re


def remove_fenced_code_blocks(lines, fence="```"):
    """Return lines not starting with fence or between fences."""
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


heading_level = "## "  # note trailing space


def make_quick_links(filename, style=None):
    """Generate links for a quick links section."""
    with open(filename, encoding="utf-8") as f:
        lines = f.readlines()
    lines = [line.rstrip() for line in lines]  # lose newlines
    # README.md has fenced code blocks that enclose other
    # fenced code blocks.  The outer blocks use ~~~ as the fence.
    # Remove the outer fenced code blocks first.
    lines = remove_fenced_code_blocks(lines, "~~~")
    lines = remove_fenced_code_blocks(lines)
    links = []
    for line in lines:
        if line.startswith(heading_level):
            title = line.replace(heading_level, "")
            label = "[" + title + "]"
            link = title.lower()
            if style == "github":
                link = link.replace(" ", "-")
            else:
                # note- this only worked in the Sphinx 1.8.5 docs
                some_punctuation = ","
                link = re.sub("[" + some_punctuation + "]", "", link)
                link = link.replace("-", " ")
                # convert runs of space to single dash
                link = re.sub("[ ]+", "-", link)
                # remove runs of - at the start of a line
                link = re.sub("^[-]+", "", link)

            link = "(#" + link + ")"
            links.append(label + link)
    return " |\n".join(links)


# def make_sphinx_readme(readme_filename, sphinx_readme_filename):
#     """Write a copy README.md with new quick links for Sphinx on RTD."""
#     with open(readme_filename, 'r', encoding='utf-8') as f1:
#         readme = f1.read()
#         github_links = make_quick_links(readme_filename, style='github')
#         sphinx_links = make_quick_links(readme_filename)
#         sphinx_readme = readme.replace(github_links, sphinx_links)
#     with open(sphinx_readme_filename, 'w', encoding='utf-8') as f2:
#         f2.write(sphinx_readme)


if __name__ == "__main__":
    text = make_quick_links("../README.md", style="github")
    print(text)
    print()
    num_links = text.count("\n") + 1
    print("created {} links, {} characters".format(num_links, len(text)))
    # print('making README_sphinx.md...')
    # make_sphinx_readme('../README.md', '../README_sphinx.md')
