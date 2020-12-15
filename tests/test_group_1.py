"""First group of pytest test cases for phmdoctest."""

import re

import phmdoctest
import phmdoctest.cases
import phmdoctest.main
import phmdoctest.simulator
import quick_links
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

    def verify_found_in_file(self, filename, format_spec='{}'):
        """Format the package version and look for result in caller's file."""
        looking_for = format_spec.format(self.package_version)
        with open(filename, 'r', encoding='utf-8') as f:
            text = f.read()
        assert looking_for in text

    def test_readme_md(self):
        """Check the version near the top of README.md."""
        self.verify_found_in_file('README.md', '# phmdoctest {}')

    def test_index_rst(self):
        """Check the version is anywhere in index.rst."""
        self.verify_found_in_file('index.rst', 'phmdoctest {}\n=============')

    def test_recent_changes(self):
        """Check the version is anywhere in recent_changes.md."""
        self.verify_found_in_file('doc/recent_changes.md', '{} - ')

    def test_conf_py_release(self):
        """Check version in the release = line in conf.py."""
        self.verify_found_in_file('conf.py', "release = '{}'")

    def test_setup_py(self):
        """Check the version anywhere in setup.py."""
        with open('setup.py', 'r', encoding='utf-8') as f:
            setup_text = f.read()
        # keep the part between single or double quotes after version=
        match = re.search(r" *version=['\"]([^'\"]*)['\"]", setup_text, re.M)
        assert match.group(1) == self.package_version


class TestDocBuildVersions:
    """
    Some versions are the same in doc/requirements.txt and setup.py.

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
    with open('doc/requirements.txt', 'r', encoding='utf-8') as f:
        doc_requirements = f.read()
        for line in doc_requirements.splitlines():
            if line.startswith('Click'):
                click_version = line
            if line.startswith('monotable'):
                monotable_version = line
    with open('setup.py', 'r', encoding='utf-8') as f:
        setup = f.read()

    @staticmethod
    def to_setup_style(value):
        """Convert value from requirements.txt style to setup.py style."""
        drop_newline = value.replace('\n', '', 1)
        drop_space = drop_newline.replace(' ', '', 1)
        quoted = drop_space.join(["'", "'"])
        return quoted

    def test_click(self):
        """Click version in doc/requirements.txt same as setup.py"""
        assert self.click_version in self.doc_requirements, 'sanity check'
        expected = self.to_setup_style(self.click_version)
        assert self.setup.count(expected) == 1

    def test_monotable(self):
        """monotable version in doc/requirements.txt same as setup.py"""
        assert self.monotable_version in self.doc_requirements, 'sanity check'
        expected = self.to_setup_style(self.monotable_version)
        assert self.setup.count(expected) == 1


def test_quick_links():
    """Make sure the README.md quick links are up to date."""
    filename = 'README.md'
    with open(filename, 'r', encoding='utf-8') as f:
        readme = f.read()
        github_links = quick_links.make_quick_links(filename, style='github')
        assert github_links in readme


def test_empty_output_block_report():
    """Empty output block get del'd."""
    simulator_status = verify.one_example(
        'phmdoctest tests/empty_output_block.md'
        ' --report --outfile discarded.py',
        want_file_name=None,
        pytest_options=['--doctest-modules', '-v']
    )
    assert simulator_status.runner_status.exit_code == 0
    assert simulator_status.pytest_exit_code == 0
    stdout = simulator_status.runner_status.stdout
    with open('tests/empty_output_report.txt', 'r', encoding='utf-8') as f:
        want = f.read()
    verify.a_and_b_are_the_same(a=want, b=stdout)


def test_empty_code_block_report():
    """Empty code block and associated output block get del'd."""
    simulator_status = verify.one_example(
        'phmdoctest tests/empty_code_block.md'
        ' --report --outfile discarded.py',
        want_file_name=None,
        pytest_options=['--doctest-modules', '-v']
    )
    assert simulator_status.runner_status.exit_code == 0
    assert simulator_status.pytest_exit_code == 0
    stdout = simulator_status.runner_status.stdout
    with open('tests/empty_code_report.txt', 'r', encoding='utf-8') as f:
        want = f.read()
    verify.a_and_b_are_the_same(a=want, b=stdout)


def test_code_does_not_print_fails():
    """Show empty stdout mis-compares with non-empty output block."""
    command = (
        'phmdoctest tests/does_not_print.md --outfile discarded.py'
    )
    simulator_status = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command,
        pytest_options=['--doctest-modules', '-v']
    )
    assert simulator_status.runner_status.exit_code == 0
    assert simulator_status.pytest_exit_code == 1


def test_more_printed_than_expected_fails():
    """Show pytest fails when more lines are printed than expected."""
    command = (
        'phmdoctest tests/missing_some_output.md --outfile discarded.py'
    )
    simulator_status = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command,
        pytest_options=['--doctest-modules', '-v']
    )
    assert simulator_status.runner_status.exit_code == 0
    assert simulator_status.pytest_exit_code == 1


def test_more_expected_than_printed_fails():
    """Show pytest fails when more lines are printed than expected."""
    command = (
        'phmdoctest tests/extra_line_in_output.md --outfile discarded.py'
    )
    simulator_status = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command,
        pytest_options=['--doctest-modules', '-v']
    )
    assert simulator_status.runner_status.exit_code == 0
    assert simulator_status.pytest_exit_code == 1


def test_skip_same_block_twice():
    """Show identifying a skipped code block more than one time is OK."""
    command = (
        'phmdoctest doc/example2.md --skip "Python 3.7" --skip LAST'
        ' --skip LAST --report --outfile discarded.py'
    )
    simulator_status = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command,
        pytest_options=['--doctest-modules', '-v']
    )
    assert simulator_status.runner_status.exit_code == 0
    assert simulator_status.pytest_exit_code == 0


def test_pytest_really_fails():
    """Make sure pytest fails due to incorrect expected output in the .md.

    Generate a pytest that will assert.
    """
    simulator_status = verify.one_example(
        'phmdoctest tests/unexpected_output.md --outfile discarded.py',
        want_file_name=None,
        pytest_options=['--doctest-modules', '-v']
    )
    assert simulator_status.pytest_exit_code == 1


def test_pytest_session_fails():
    """Make sure pytest fails due to incorrect session output in the .md file.

    Generate a pytest that fails pytest.
    """
    simulator_status = verify.one_example(
        'phmdoctest tests/bad_session_output.md --outfile discarded.py',
        want_file_name=None,
        pytest_options=['--doctest-modules', '-v']
    )
    assert simulator_status.pytest_exit_code == 1


def test_project_md():
    """Make sure that project.md generates a file that passes pytest."""
    simulator_status = verify.one_example(
        'phmdoctest project.md --outfile discarded.py',
        want_file_name=None,
        pytest_options=['--doctest-modules', '-v']
    )
    assert simulator_status.runner_status.exit_code == 0
    assert simulator_status.pytest_exit_code == 0


def test_example2_report():
    """Check example2_report.txt used in .travis.yml."""
    simulator_status = verify.one_example(
        'phmdoctest doc/example2.md --skip "Python 3.7" --skip LAST --report'
        ' --outfile discarded.py',
        want_file_name=None,
        pytest_options=None
    )
    assert simulator_status.runner_status.exit_code == 0
    stdout = simulator_status.runner_status.stdout
    with open('tests/example2_report.txt', 'r', encoding='utf-8') as f:
        want = f.read()
    verify.a_and_b_are_the_same(a=want, b=stdout)


def test_blanklines_in_output():
    """Expected output has empty lines and no doctest <BLANKLINE>."""
    command = (
        'phmdoctest tests/output_has_blank_lines.md --outfile discarded.py'
    )
    simulator_status = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command,
        pytest_options=['--doctest-modules', '-v']
    )
    assert simulator_status.runner_status.exit_code == 0
    assert simulator_status.pytest_exit_code == 0
