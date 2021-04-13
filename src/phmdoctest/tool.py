"""General purpose tools get fenced code blocks from Markdown."""

from typing import IO, List
from xml.etree import ElementTree

import commonmark    # type: ignore
import commonmark.node    # type: ignore


def fenced_code_blocks(markdown_filename: str) -> List[str]:
    """Return Markdown fenced code block contents as a list of strings.

    Args:
        markdown_filename
            Path to the Markdown file.

    Returns:
        List of strings, one for the contents of each Markdown
        fenced code block.
    """
    with open(markdown_filename, encoding='utf-8') as fp:
        nodes = fenced_block_nodes(fp)
        return [node.literal for node in nodes]


def fenced_block_nodes(fp: IO[str]) -> List[commonmark.node.Node]:
    """Get markdown fenced code blocks as list of Node objects.

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
        if node.t == 'code_block' and node.is_fenced:
            nodes.append(node)
    return nodes


def extract_testsuite(junit_xml_string):
    """Return testsuite tree and list of failing trees from JUnit XML.

    Args:
        junit_xml_string
            String containing JUnit xml returned by
            phmdoctest.simulator.run_and_pytest().

    Returns:
         tuple testsuite tree, list of failed test case trees

    """
    root = ElementTree.fromstring(junit_xml_string)
    suite = root.find('testsuite')
    failed_test_cases = []
    for case in suite:
        if case.find('failure') is not None:
            failed_test_cases.append(case)
    return suite, failed_test_cases
