"""General purpose tools get fenced code blocks from Markdown."""
from typing import IO, Optional, List, NamedTuple, Tuple
from xml.etree import ElementTree
from xml.etree.ElementTree import Element

import commonmark  # type: ignore
import commonmark.node  # type: ignore

import phmdoctest.direct


class FCBChooser:
    """Select labeled fenced code block from the Markdown file."""

    def __init__(self, markdown_filename: str):
        """Gather labelled Markdown fenced code blocks in the file.

        Args:
            markdown_filename:
                Path to the Markdown file
        """
        self._blocks = labeled_fenced_code_blocks(markdown_filename)

    def contents(self, label: str = "") -> str:
        """Return contents of the labeled fenced code block with label.

        Args:
            label
                Value of label directive placed on the fenced code block
                in the Markdown file.

        Returns:
            Contents of the labeled fenced code block as a string
            or empty string if the label is not found. Fenced code block
            strings typically end with a newline.
        """
        for block in self._blocks:
            if block.label == label:
                return block.contents
        return ""


LabeledFCB = NamedTuple(
    "LabeledFCB",
    [
        ("label", str),  # the label directive's value
        ("line", str),  # Markdown file line number of block contents
        ("contents", str),  # fenced code block contents
    ],
)
"""Information about a fenced code block that has a label directive."""


def labeled_fenced_code_blocks(markdown_filename: str) -> List[LabeledFCB]:
    """Return Markdown fenced code blocks that have label directives.

    Label directives are placed immediately before a fenced code block
    in the Markdown source file. The directive can be placed before any
    fenced code block.
    The label directive is the HTML comment ``<!--phmdoctest-label VALUE-->``
    where VALUE is typically a legal Python identifier. The space must
    be present before VALUE.
    The label directive is also used to name the test function
    in generated code.  When used that way, it must be a valid
    Python identifier.
    If there is more than one label directive on the block, the
    label value that occurs earliest in the file is used.

    Args:
        markdown_filename
            Path to the Markdown file.

    Returns:
        List of LabeledFCB objects.

        LabeledFCB is a NamedTuple with these fields:

        - label is the value of a label directive
          placed in a HTML comment before the fenced code block.
        - line is the line number in the Markdown file where the block
          starts.
        - contents is the fenced code block contents as a string.
    """
    with open(markdown_filename, "r", encoding="utf-8") as fp:
        nodes = fenced_block_nodes(fp)
        labeled_blocks = []
        for node in nodes:
            directives = phmdoctest.direct.get_directives(node)
            for directive in directives:
                if directive.type == phmdoctest.direct.Marker.LABEL:
                    block = LabeledFCB(
                        label=directive.value,
                        line=node.sourcepos[0][0] + 1,
                        contents=node.literal,
                    )
                    labeled_blocks.append(block)
                    break
    return labeled_blocks


def fenced_code_blocks(markdown_filename: str) -> List[str]:
    """Return Markdown fenced code block contents as a list of strings.

    Args:
        markdown_filename
            Path to the Markdown file.

    Returns:
        List of strings, one for the contents of each Markdown
        fenced code block.
    """
    with open(markdown_filename, "r", encoding="utf-8") as fp:
        nodes = fenced_block_nodes(fp)
        return [node.literal for node in nodes]


def fenced_block_nodes(fp: IO[str]) -> List[commonmark.node.Node]:
    """Get markdown fenced code blocks as list of Node objects.

    Deprecation Watch: This function may be labelled as deprecated in a
    future version of phmdoctest.  It returns a data type defined by
    the commonmark package.

    Args:
        fp
            file object returned by open().

    Returns:
         List of commonmark.node.Node objects.
    """
    nodes = []
    doc = fp.read()
    parser = commonmark.Parser()
    ast = parser.parse(doc)
    walker = ast.walker()
    # Presumably, because fenced code blocks nodes are leaf nodes
    # they will only be entered once by the walker.
    for node, entering in walker:
        if node.t == "code_block" and node.is_fenced:
            nodes.append(node)
    return nodes


def extract_testsuite(junit_xml_string: str) -> Tuple[Optional[Element], List[Element]]:
    """Return testsuite tree and list of failing trees from JUnit XML.

    Args:
        junit_xml_string
            String containing JUnit xml returned by
            pytest or phmdoctest.simulator.run_and_pytest().

    Returns:
         tuple testsuite tree, list of failed test case trees
    """
    root = ElementTree.fromstring(junit_xml_string)
    suite = root.find("testsuite")
    failed_test_cases = []
    if suite is not None:
        for case in suite:
            if case.find("failure") is not None:
                failed_test_cases.append(case)
    return suite, failed_test_cases
