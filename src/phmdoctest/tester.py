"""testfile_creator and testfile_tester pytest fixtures."""
from pathlib import Path
from typing import List
from typing import Optional

import phmdoctest.main
import pytest
from _pytest.pytester import RunResult

# mypy: ignore_errors

# Note- Because testfile_tester uses pytester it can't be used in the
#       same test function with simulator.run_and_pytest() because pytester
#       changes the current working directory when it is activated.
# Note- pytester requires conftest.py in tests folder with
#       pytest_plugins = ["pytester"]
# Note- Requires pytest >= 6.2.


@pytest.fixture()
def testfile_creator(pytestconfig):  # type: ignore
    """Fixture creates the pytest test file contents from the Markdown file.

    A Markdown file, in a folder relative to the pytest command line
    invocation directory is processed by phmdoctest to create a
    pytest file which is returned as a string.

    This fixture is needed to produce the pytest test file when using the
    fixture testfile_tester below because pytester changes the current
    working directory when it is activated.

    The fixture injects a function with the following signature. Please
    consult the source in tester.py.
    The returned function calls phmdoctest.main.testfile() to generate
    the pytest test file from Markdown.

    Args:
        markdown_file
            Path to the Markdown input file. This file name is relative
            to the working directory of the command that invokes pytest.
            Typically this is the root of the repository.

    Keyword Args:
        skips
            List[str]. Do not test blocks with substring TEXT.

        fail_nocode
            Markdown file with no code blocks generates a failing test.

        setup
            Run block with substring TEXT at test module setup time.

        teardown
            Run block with substring TEXT at test module teardown time.

        setup_doctest
            Make globals created by the setup Python code block
            or setup directive visible to Python interactive session >>> blocks.
            Caution: The globals are set at Pytest Session scope and are visible
            to all tests run by --doctest-modules.

    Returns:
        String containing the contents of the generated pytest file.
    """

    def create_testfile(
        markdown_file: str = "",
        *,
        skips: Optional[List[str]] = None,
        fail_nocode: bool = False,
        setup: Optional[str] = None,
        teardown: Optional[str] = None,
        setup_doctest: bool = False,
    ) -> str:
        """Creates the pytest test file contents from the Markdown file."""
        invoke_path = Path(pytestconfig.invocation_params.dir)
        absolute_path = invoke_path / markdown_file
        test_file_contents = phmdoctest.main.testfile(
            markdown_file=str(absolute_path),
            skips=skips,
            fail_nocode=fail_nocode,
            setup=setup,
            teardown=teardown,
            setup_doctest=setup_doctest,
            built_from=markdown_file,
        )
        return test_file_contents

    return create_testfile


@pytest.fixture()
def testfile_tester(pytester):  # type: ignore
    """Fixture runs pytester.runpytest with the caller's pytest file string.

    Stores the caller's pytest test file `contents`
    in a temporary directory hosted by pytest. Run pytest on it
    using `pytest_options`.
    Typically the caller runs testfile_creator to generate the test file.
    See example usage in the files tests/test_examples.py
    and tests/test_details.py.

    The fixture injects a function with the following signature. Please
    consult the source in tester.py.

    - pytester requires conftest.py in tests folder with
      pytest_plugins = ["pytester"]
    - Requires pytest >= 6.2.

    Args:
        contents
            String containing the contents of a pytest test file.

        testfile_name
            Name given to the test file when it is stored in the
            pytester temporary directory.

        pytest_options
            List of strings of pytest command line options
            that are passed to pytester.

    Returns:
        pytest RunResult returned by pytester.runpytest().
    """

    def test_testfile(
        contents: str = "",
        testfile_name: str = "testfile_tester_test.py",
        pytest_options: Optional[List[str]] = None,
    ) -> RunResult:
        """Run pytester.runpytest with the caller's pytest file string."""
        assert len(contents), "Must not be empty string."
        kwargs = {testfile_name: contents}
        pytester.makepyfile(**kwargs)
        if pytest_options is None:
            run_result: RunResult = pytester.runpytest()
        else:
            run_result = pytester.runpytest(*pytest_options)
        return run_result

    return test_testfile
