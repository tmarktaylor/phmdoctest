"""First group of pytest test cases for phmdoctest."""
import configparser
import copy
import re

import pytest

import phmdoctest
import phmdoctest.cases
from phmdoctest.fenced import Role
import phmdoctest.main
import phmdoctest.simulator
import phmdoctest.tool
import verify


# Caution:
# This test file is run by pytest.
# The call to invoke_and_pytest() will start pytest in a
# subprocess.
# Pytest captures stdout and so does CliRunner.invoke().


class TestSameVersions:
    """Verify same release version string in all places.

    Obtain the version string from various places in the source tree
    and check that they are all the same.
    Compare all the occurrences to phmdoctest.__version__.
    This test does not prove the version is correct.
    Whitespace may be significant in some cases.
    """

    package_version = phmdoctest.__version__

    def verify_found_in_file(self, filename, format_spec="{}"):
        """Format the package version and look for result in caller's file."""
        looking_for = format_spec.format(self.package_version)
        with open(filename, "r", encoding="utf-8") as f:
            text = f.read()
        assert looking_for in text

    def test_readme_md(self):
        """Check the version near the top of README.md."""
        self.verify_found_in_file("README.md", "# phmdoctest {}")

    def test_index_rst(self):
        """Check the version is anywhere in index.rst."""
        self.verify_found_in_file("index.rst", "phmdoctest {}\n=============")

    def test_recent_changes(self):
        """Check the version is anywhere in recent_changes.md."""
        self.verify_found_in_file("doc/recent_changes.md", "{} - ")

    def test_conf_py_release(self):
        """Check version in the release = line in conf.py."""
        self.verify_found_in_file("conf.py", 'release = "{}"')

    def test_setup_cfg(self):
        """Check the version in setup.cfg."""
        config = configparser.ConfigParser()
        config.read("setup.cfg")
        metadata_version = config["metadata"]["version"]
        assert metadata_version == self.package_version


def test_requirements_file():
    """setup.cfg install_requires == requirements.txt.

    Whitespace should not be significant.
    The config file parser returns a string for the key
    "install_requires". The string has embedded newlines.
    The string starts with a blank first line.
    The comment lines are removed from requirements.txt.
    All the blanks are removed from each line.
    """
    config = configparser.ConfigParser()
    config.read("setup.cfg")
    config_lines = config["options"]["install_requires"].splitlines()
    config_lines = [line.replace(" ", "") for line in config_lines if line]
    with open("requirements.txt", "r", encoding="utf-8") as f:
        text = f.read()
    lines = text.splitlines()
    lines = [line for line in lines if not line.startswith("#")]
    requirements_lines = [line.replace(" ", "") for line in lines if line]
    assert requirements_lines == config_lines


def test_doc_requirements_file():
    """
    Some versions are the same in doc/requirements.txt and setup.cfg.

    Click and monotable versions should be the same.

    For the Sphinx documentation build on readthedocs.org (RTD)
    specific versions are pinned by the file doc/requirements.txt.

    For Sphinx autodoc the phmdoctest dependencies Click and monotable
    are installed so that the RTD build can import phmdoctest to look
    for docstrings.

    Note that commonmark is also a phmdoctest dependency. Because it is
    pinned to different versions in doc/requirements.txt and setup.py
    it is not tested here.
    """
    with open("requirements.txt", "r", encoding="utf-8") as f:
        setup_requirements = f.read()
        for line in setup_requirements.splitlines():
            if line.startswith("Click"):
                setup_click = line.replace(" ", "")
            if line.startswith("monotable"):
                setup_monotable = line.replace(" ", "")

    with open("doc/requirements.txt", "r", encoding="utf-8") as f:
        doc_requirements = f.read()
        for line in doc_requirements.splitlines():
            if line.startswith("Click"):
                doc_click = line.replace(" ", "")
            if line.startswith("monotable"):
                doc_monotable = line.replace(" ", "")

    assert setup_click == doc_click
    assert setup_monotable == doc_monotable


def test_empty_output_block_report():
    """Empty output block get del'd."""
    simulator_status = verify.one_example(
        "phmdoctest tests/empty_output_block.md" " --report --outfile discarded.py",
        want_file_name=None,
        pytest_options=["--doctest-modules", "-v"],
    )
    assert simulator_status.runner_status.exit_code == 0
    assert simulator_status.pytest_exit_code == 0
    stdout = simulator_status.runner_status.stdout
    with open("tests/empty_output_report.txt", "r", encoding="utf-8") as f:
        want = f.read()
    verify.a_and_b_are_the_same(a=want, b=stdout)


def test_empty_code_block_report():
    """Empty code block and associated output block get del'd."""
    simulator_status = verify.one_example(
        "phmdoctest tests/empty_code_block.md" " --report --outfile discarded.py",
        want_file_name=None,
        pytest_options=["--doctest-modules", "-v"],
    )
    assert simulator_status.runner_status.exit_code == 0
    assert simulator_status.pytest_exit_code == 0
    stdout = simulator_status.runner_status.stdout
    with open("tests/empty_code_report.txt", "r", encoding="utf-8") as f:
        want = f.read()
    verify.a_and_b_are_the_same(a=want, b=stdout)


def test_no_markdown_fenced_code_blocks():
    """Show --report works when there is nothing to report."""
    simulator_status = verify.one_example(
        "phmdoctest tests/no_fenced_code_blocks.md" " --report --outfile discarded.py",
        want_file_name=None,
        pytest_options=["--doctest-modules", "-v"],
    )
    assert simulator_status.runner_status.exit_code == 0
    assert simulator_status.pytest_exit_code == 0
    stdout = simulator_status.runner_status.stdout
    assert "0 test cases." in stdout


def test_code_does_not_print_fails():
    """Show empty stdout mis-compares with non-empty output block."""
    command = "phmdoctest tests/does_not_print.md --outfile discarded.py"
    simulator_status = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command, pytest_options=["--doctest-modules", "-v"]
    )
    assert simulator_status.runner_status.exit_code == 0
    assert simulator_status.pytest_exit_code == 1


def test_more_printed_than_expected_fails():
    """Show pytest fails when more lines are printed than expected."""
    command = "phmdoctest tests/missing_some_output.md --outfile discarded.py"
    simulator_status = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command, pytest_options=["--doctest-modules", "-v"]
    )
    assert simulator_status.runner_status.exit_code == 0
    assert simulator_status.pytest_exit_code == 1


def test_more_expected_than_printed_fails():
    """Show pytest fails when more lines are printed than expected."""
    command = "phmdoctest tests/extra_line_in_output.md --outfile discarded.py"
    simulator_status = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command, pytest_options=["--doctest-modules", "-v"]
    )
    assert simulator_status.runner_status.exit_code == 0
    assert simulator_status.pytest_exit_code == 1


def test_skip_same_block_twice():
    """Show identifying a skipped code block more than one time is OK."""
    command = (
        'phmdoctest doc/example2.md --skip "Python 3.7" --skip LAST'
        " --skip LAST --report --outfile discarded.py"
    )
    simulator_status = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command, pytest_options=["--doctest-modules", "-v"]
    )
    assert simulator_status.runner_status.exit_code == 0
    assert simulator_status.pytest_exit_code == 0


def test_pytest_really_fails():
    """Make sure pytest fails due to incorrect expected output in the .md.

    Generate a pytest that will assert.
    """
    simulator_status = verify.one_example(
        "phmdoctest tests/unexpected_output.md --outfile discarded.py",
        want_file_name=None,
        pytest_options=["--doctest-modules", "-v"],
        junit_family=verify.JUNIT_FAMILY,
    )
    assert simulator_status.pytest_exit_code == 1
    # Look at the returned JUnit XML to see that the test failed at the
    # point and for the reason we expected.
    # Note that the parsed XML values are all strings.
    suite, fails = phmdoctest.tool.extract_testsuite(simulator_status.junit_xml)
    assert suite.attrib["tests"] == "1"
    assert suite.attrib["errors"] == "0"
    assert suite.attrib["failures"] == "1"
    assert fails[0].attrib["name"] == "test_code_4_output_17"


def test_pytest_session_fails():
    """Make sure pytest fails due to incorrect session output in the .md file.

    Generate a pytest that fails pytest.
    """
    simulator_status = verify.one_example(
        "phmdoctest tests/bad_session_output.md --outfile discarded.py",
        want_file_name=None,
        pytest_options=["--doctest-modules", "-v"],
    )
    assert simulator_status.pytest_exit_code == 1


def test_project_md():
    """Make sure that project.md generates a file that passes pytest."""
    simulator_status = verify.one_example(
        "phmdoctest project.md --outfile discarded.py",
        want_file_name=None,
        pytest_options=["--doctest-modules", "-v"],
    )
    assert simulator_status.runner_status.exit_code == 0
    assert simulator_status.pytest_exit_code == 0


def test_example2_report():
    """Check example2_report.txt."""
    simulator_status = verify.one_example(
        'phmdoctest doc/example2.md --skip "Python 3.7" --skip LAST --report'
        " --outfile discarded.py",
        want_file_name=None,
        pytest_options=None,
    )
    assert simulator_status.runner_status.exit_code == 0
    assert simulator_status.pytest_exit_code is None
    stdout = simulator_status.runner_status.stdout
    with open("tests/example2_report.txt", "r", encoding="utf-8") as f:
        want = f.read()
    verify.a_and_b_are_the_same(a=want, b=stdout)


def test_setup_with_inline():
    """Do inline annotations in setup and teardown blocks."""
    command = (
        "phmdoctest tests/setup_with_inline.md -u FIRST -d LAST --outfile discarded.py"
    )
    simulator_status = verify.one_example(
        well_formed_command=command,
        want_file_name="tests/test_setup_with_inline.py",
        pytest_options=["--doctest-modules", "-v"],
    )
    assert simulator_status.runner_status.exit_code == 0


def test_blanklines_in_output():
    """Expected output has empty lines and no doctest <BLANKLINE>."""
    command = "phmdoctest tests/output_has_blank_lines.md --outfile discarded.py"
    simulator_status = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command,
        pytest_options=["--doctest-modules", "-v"],
        junit_family=verify.JUNIT_FAMILY,
    )
    assert simulator_status.runner_status.exit_code == 0
    assert simulator_status.pytest_exit_code == 0


def test_one_mark_skip():
    """A single <!--phmdoctest-mark.skip--> directive."""
    command = "phmdoctest tests/one_mark_skip.md --outfile discarded.py"
    simulator_status = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command,
        pytest_options=["--doctest-modules", "-v"],
    )
    assert simulator_status.runner_status.exit_code == 0
    assert simulator_status.pytest_exit_code == 0


def test_no_namespace_manager_call_generated():
    """phmdoctest.cases.call_namespace_manager() returns empty string."""
    # In cases.py there is never a call to call_namespace_manager()
    # with neither share-names or clear-names directives.
    # Coverage reports a missing statement.
    # Fix by calling with a block that doesn't have those directives.
    with open("tests/direct.md", encoding="utf-8") as fp:
        blocks = phmdoctest.fenced.convert_nodes(phmdoctest.tool.fenced_block_nodes(fp))
    code_line = phmdoctest.cases.call_namespace_manager(blocks[0])
    assert code_line == ""


def test_fenced_role_skipping():
    """Check FencedBlock.skip() for blocks with different roles."""
    # Obtain a single FencedBlock instance to try with different roles.
    # Make a copy of the first block below, modify the role,
    # and call skip() on it.  The good roles don't raise an assertion,
    # the bad roles do.
    with open("tests/direct.md", encoding="utf-8") as fp:
        blocks = phmdoctest.fenced.convert_nodes(phmdoctest.tool.fenced_block_nodes(fp))
    good_roles = [
        Role.CODE,
        Role.OUTPUT,
        Role.SESSION,
        Role.SKIP_CODE,
        Role.SKIP_OUTPUT,
        Role.SKIP_SESSION,
    ]
    for role in good_roles:
        block = copy.copy(blocks[0])
        block.role = role
        block.skip(pattern="no-assertion-expected")

    bad_roles = [
        Role.UNKNOWN,
        Role.SETUP,
        Role.TEARDOWN,
        Role.DEL_CODE,
        Role.DEL_OUTPUT,
    ]
    for role in bad_roles:
        block = copy.copy(blocks[0])
        block.role = role
        with pytest.raises(AssertionError) as exc_info:
            block.skip(pattern="assertion-is-expected")
        assert "cannot skip a block with " + str(role) in str(exc_info.value)

    # Assure that every Role enum value gets tested.
    number_of_roles_tried = len(set(good_roles + bad_roles))
    assert len(Role) == number_of_roles_tried, "missed some roles"
