"""General purpose tools get fenced code blocks from Markdown."""
from collections import namedtuple
from pathlib import Path
from typing import IO, Optional, List, NamedTuple, Tuple
from xml.etree import ElementTree
from xml.etree.ElementTree import Element

import commonmark  # type: ignore
import commonmark.node  # type: ignore

import phmdoctest.direct
import phmdoctest.fillrole


class FCBChooser:
    """Select labeled fenced code block from the Markdown file."""

    def __init__(self, markdown_filename: str):
        """Gather labelled Markdown fenced code blocks in the file.

        Args:
            markdown_filename:
                Path to the Markdown file as a string.
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
"""Describes a fenced code block that has a label directive. (collections.namedtuple).

    Args:
        label
            The label directive's value.

        line
            Markdown file line number of block contents.

        contents
            Fenced code block contents.
"""


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
            Path to the Markdown file as a string.

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
            Path to the Markdown file as a string.

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


PythonExamples = namedtuple("PythonExamples", ["has_code", "has_session"])
"""Presence of Python fenced code blocks in Markdown. (collections.namedtuple)

    Args:
        has_code
            True if detected at least one fenced code block with Python code.

        has_session
            True if detected at least one fenced code block with Python
            interactive session (doctest).
"""


def detect_python_examples(markdown_path: Path) -> "PythonExamples":
    """Return whether .md has any Python highlighted fenced code blocks.

     This includes Python code blocks and Python doctest interactive session
     blocks. These blocks may or may not generate test cases once processed
     by phmdoctest.test_file() and collected.

     - We don't care here if the code block is followed by expected output.
     - This logic does not check if the block has any phmdoctest skip,
       mark.skip, or mark.skipif directives.
     - This logic does not check if the block would be skipped by
       a phmdoctest command line --skip option.

    Args:
         markdown_path
             pathlib.Path of input Markdown file.

    """
    with open(markdown_path, "r", encoding="utf-8") as fp:
        fenced = fenced_block_nodes(fp)
    has_code = any(phmdoctest.fillrole.is_python_block(node) for node in fenced)
    has_session = any(phmdoctest.fillrole.is_doctest_block(node) for node in fenced)
    return PythonExamples(
        has_code=has_code,
        has_session=has_session,
    )


def _with_stem(path: Path, stem: str) -> Path:
    """Replacement for pathlib.PurePath.with_stem() which is new Python 3.9."""
    return path.with_name(stem + path.suffix)


def wipe_testfile_directory(target_dir: Path) -> None:
    """Create and/or clean target_dir directory to receive generated testfiles.

    Create target_dir if needed for writing generated pytest files.
    Prevent future use of pre-existing .py files in target_dir.

        - The FILENAME.py files found in target_dir are renamed
          to noFILENAME.sav.
        - If a noFILENAME.sav already exists it is not modified.
        - Files in target_dir with other extensions are not modified.
        - A FILENAME.py pre-existing in target_dir is only renamed
          and not deleted.
          This allows for recovery of .py files when target_dir gets pointed
          by mistake to a directory with Python source files.

    Args:
        target_dir
            pathlib.Path of destination directory for generated test files.
    """

    # create if needed
    target_dir.mkdir(mode=0o700, parents=True, exist_ok=True)

    # Clean out or preserve pre-existing Python files.
    for existing_path in target_dir.glob("*.py"):
        preserve_path = existing_path.with_suffix(".sav")
        preserve_path = _with_stem(preserve_path, "no" + existing_path.stem)
        if preserve_path.exists():
            # A no*.sav already exists, so we assume it was created by
            # a prior pytest invocation. It is possible the user mis-typed
            # the --phmdmoctest-generate DIR on the command line and
            # may want to recover .py files later.
            # We can't overwrite a .sav file since it may hold a
            # preserved .py file.
            # Since pytest invocations only write files named test_*.py
            # the file about to be deleted here is named test_*.py and
            # it was created by a previous invocation of this plugin.
            assert existing_path.name.startswith("test_")
            assert existing_path.suffix == ".py"
            existing_path.unlink()  # delete the file
        else:
            # rename the file
            existing_path.replace(preserve_path)
