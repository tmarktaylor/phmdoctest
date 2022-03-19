"""A way to test lots of Markdown files using the pytester testfile_* fixtures."""

from pathlib import Path
import sys

from _pytest.pytester import RunResult
import pytest

from phmdoctest.tester import testfile_creator
from phmdoctest.tester import testfile_tester
import phmdoctest.tool


# Note- The fixture testfile_tester uses a pytest provided plugin development
#       fixture called pytester.
# Note- pytester requires conftest.py in tests folder with
#       pytest_plugins = ["pytester"]
# Note- Requires pytest >= 6.2.
class TestMany:
    """Prune and test list of .md files found by searching for files."""

    p = Path(".")
    # Test these files.
    # These are example and test input Markdown files in the repos.
    # They are relative to the pytest invocation directory.
    # Note that this test duplicates 6 of the tests in test_examples.py.
    markdown_paths = list(p.glob("doc/*.md"))
    markdown_paths.append(Path("project.md"))  # Normally this is README.md.
    markdown_paths.append(Path("tests/managenamespace.md"))
    markdown_paths.append(Path("tests/one_code_block.md"))
    markdown_paths.append(Path("tests/output_has_blank_lines.md"))
    markdown_paths.append(Path("tests/setup_only.md"))
    markdown_paths.append(Path("tests/twentysix_session_blocks.md"))
    globs_to_skip = [
        # Don't test files matching globs below:
        # Reason- needs command line args.
        "doc/setup.md",
        "doc/setup_doctest.md",
        # Reason- contains an already generated test file.
        "doc/*_raw.md",
        "doc/*_py.md",
        # Reason- need to register markers to avoid PytestUnknownMarkWarning.
        "doc/mark_example.md",
    ]
    paths_to_skip = []
    for glob in globs_to_skip:
        paths_to_skip.extend(p.glob(glob))
    tested = []
    for p in markdown_paths:
        if p in paths_to_skip:
            continue
        python_examples = phmdoctest.tool.detect_python_examples(p)
        if python_examples.has_code or python_examples.has_session:
            tested.append(p)
    # Note: If none of the files in the list tested have doctests the
    #       --doctest-modules pytest option below is not needed.

    @pytest.mark.skipif(sys.version_info < (3, 8), reason="requires >=py3.8")
    @pytest.mark.parametrize("markdown_name", tested)
    def test_md(self, markdown_name, testfile_creator, testfile_tester):
        """Generate pytest file and run it with pytester."""
        testfile = testfile_creator(markdown_name.as_posix())
        # create the test file name
        p = Path(markdown_name).with_suffix(".py")
        myname = "test_many_md_" + "__".join(p.parts)  # flatten
        result = testfile_tester(
            contents=testfile,
            testfile_name=myname,
            pytest_options=["-v", "--doctest-modules"],
        )
        summary_nouns = result.parse_summary_nouns(result.outlines)
        assert summary_nouns.get("failed", 0) == 0
        assert summary_nouns.get("errors", 0) == 0
        assert summary_nouns.get("warnings", 0) == 0
        assert "passed" in summary_nouns
