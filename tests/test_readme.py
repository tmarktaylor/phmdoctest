"""pytest test cases for examples in fenced code blocks in README.md."""

import inspect
from pathlib import Path
import re
import textwrap

import phmdoctest.main
import phmdoctest.direct
import phmdoctest.inline
import phmdoctest.simulator
import phmdoctest.tool

# Caution:
# This test file is run by pytest.
# The call to invoke_and_pytest() will start pytest in a
# subprocess.
# Pytest captures stdout and so does CliRunner.invoke().

# Fenced code blocks that have the phmdoctest-label directive.
labeled = phmdoctest.tool.FCBChooser("README.md")


def example_code_checker(callable_function, example_string, checker_function):
    """Check that the body of the function matches the string."""
    want1 = inspect.getsource(callable_function)
    got = textwrap.indent(example_string, "    ")
    # Drop the def function_name line.
    newline_index = want1.find("\n")
    assert newline_index > -1, "must have a newline"
    assert len(want1) > newline_index + 2, "must have more after newline"
    want2 = want1[newline_index + 1 :]
    checker_function(want2, got)


def test_directive_example_raw(checker):
    """README raw markdown is same as the disk file."""
    want = labeled.contents(label="directive-example-raw")
    got = Path("tests/one_mark_skip.md").read_text(encoding="utf-8")
    checker(want, got)


def test_directive_example(example_tester, checker):
    """Make sure generated --outfile is as expected; Run pytest.

    Check the --outfile against the copy in the fenced code block.
    """
    example1_command = labeled.contents(label="directive-example-command")
    want = labeled.contents(label="directive-example-outfile")
    simulator_status = example_tester(
        example1_command,
        want_file_name=None,
        pytest_options=["--doctest-modules", "-v"],
    )
    # Fenced code block in README.md is the same as the --outfile.
    got = simulator_status.outfile
    checker(want, got)
    assert simulator_status.pytest_exit_code == 0


def test_ci_example():
    """The bash lines in README are also in workflows/install.yml.

    The fenced code block in README.md uses a different filename than
    install.yml.  We need to replace README.md with project.md.
    We need to replace test_readme.py with test_project.py.
    """

    # The goal of this test is fail if either install.yml
    # or the fenced code block example is changed in one, but not
    # both places.
    fcb = labeled.contents(label="ci-example")
    fcb_lower_case = fcb.lower()
    fcb_lines = fcb_lower_case.splitlines()
    edited_lines_in_fcb = [line.replace("readme", "project") for line in fcb_lines]
    whole_file = Path(".github/workflows/install.yml").read_text(encoding="utf-8")
    lines_in_file = whole_file.splitlines()
    stripped_lines_in_file = [line.strip() for line in lines_in_file]
    assert len(edited_lines_in_fcb) == 3
    for line in edited_lines_in_fcb:
        assert line in stripped_lines_in_file, "line must be somewhere in file"


def test_actions_usage_md(checker):
    """Cut and paste from ci.yml to actions_usage.md is the same."""
    blocks = phmdoctest.tool.fenced_code_blocks("doc/actions_usage.md")
    got = blocks[0]
    whole_file = Path(".github/workflows/ci.yml").read_text(encoding="utf-8")
    m = re.search(
        pattern=r"(jobs:.*\n)\n  coverage:", string=whole_file, flags=re.DOTALL
    )
    want = m.group(1)
    checker(a=want, b=got)


def test_raw_example1_md(checker):
    """README raw markdown is same as file doc/example1.md."""
    want = labeled.contents(label="example1-raw")
    got = Path("doc/example1.md").read_text(encoding="utf-8")
    checker(want, got)


def test_example1(example_tester, checker):
    """Make sure generated --outfile is as expected; Run pytest.

    Check the copy of test_example1.py in the fenced code block.
    """
    # The helper checks the generated --outfile against the disk file.
    example1_command = labeled.contents(label="example1-command")
    want = labeled.contents(label="example1-outfile")
    _ = example_tester(
        example1_command, want_file_name="doc/test_example1.py", pytest_options=None
    )
    # Make sure the copy of test_example1.py in README.md
    # is the same as the disk file.
    got = Path("doc/test_example1.py").read_text(encoding="utf-8")
    checker(want, got)

    # Run again and call pytest to make sure the file works with pytest.
    simulator_status = example_tester(
        example1_command,
        want_file_name=None,
        pytest_options=["--doctest-modules", "-v"],
    )
    assert simulator_status.pytest_exit_code == 0


def test_report(checker):
    """README report output is same as produced by the command."""
    report_command = labeled.contents(label="report-command")
    want = labeled.contents(label="example2-report")
    simulator_status = phmdoctest.simulator.run_and_pytest(
        report_command, pytest_options=None
    )
    assert simulator_status.runner_status.exit_code == 0
    assert simulator_status.pytest_exit_code is None
    got = simulator_status.runner_status.stdout
    checker(want, got)


def test_intro_to_directives():
    """Verify correct spelling of the skip directive."""
    text = labeled.contents(label="intro-to-directives")
    lines = text.splitlines()
    assert lines[0] == phmdoctest.direct.Marker.SKIP.value
    assert lines[1] == "<!--Another HTML comment-->"


# Developers: Changes here must be mirrored in a Markdown FCB in README.md.
# Runnable version of FCBChooser example code in README.md.
# The guts of this function are an exact copy of example in README.md.
def chooser_example_code():
    import phmdoctest.tool

    chooser = phmdoctest.tool.FCBChooser("doc/my_markdown_file.md")
    text = chooser.contents(label="my-fenced-code-block")
    print(text)


def test_fcb_chooser(capsys, checker):
    """Check 3 parts of the label on any fenced code block example."""
    # 1. The .md shown in the fenced code block is the same
    #    as the file on disk.
    want = labeled.contents(label="my-markdown-file")
    got = Path("doc/my_markdown_file.md").read_text(encoding="utf-8")
    checker(want, got)

    # 2. The Python code example in the fenced code block is the same as
    #    the body of the function chooser_example_code() above.
    example_code_checker(
        callable_function=chooser_example_code,
        example_string=labeled.contents(label="fetch-it"),
        checker_function=checker,
    )

    # 3. The example output shown in the fenced code block is
    #    the same as the output from running chooser_example_code().
    want3 = labeled.contents(label="fetched-contents")
    assert want3
    chooser_example_code()
    got3 = capsys.readouterr().out
    assert got3.endswith("\n\n"), "FCB newline + print() newline"
    got3 = got3[:-1]  # drop the newline that print() added.
    checker(want3, got3)


def test_setup_first_fcb(checker):
    """Make sure example setup fenced code block same as in the file."""
    want = labeled.contents(label="setup-md-first-block")
    blocks = phmdoctest.tool.fenced_code_blocks("doc/setup.md")
    got = blocks[0]
    checker(want, got)


def test_directive1_example(example_tester, checker):
    """Make sure generated --outfile and --report are as expected."""

    # Note that the report_command is hard coded here.
    # The command shown in README.md is not tested.
    report_command = "phmdoctest doc/directive1.md --report"

    directive_command = labeled.contents(label="directive-1-outfile")
    _ = example_tester(
        directive_command, want_file_name="doc/test_directive1.py", pytest_options=None
    )
    want = Path("doc/directive1_report.txt").read_text(encoding="utf-8")
    simulator_status = example_tester(
        report_command, want_file_name=None, pytest_options=None
    )
    got = simulator_status.runner_status.stdout
    checker(want, got)


def test_directive2_example(example_tester, checker):
    """Make sure generated --outfile and --report are as expected."""

    # Note that the report_command is hard coded here.
    # The command shown in README.md is not tested.
    report_command = "phmdoctest doc/directive2.md --report"

    directive_command = labeled.contents(label="directive-2-outfile")
    _ = example_tester(
        directive_command, want_file_name="doc/test_directive2.py", pytest_options=None
    )
    want = Path("doc/directive2_report.txt").read_text(encoding="utf-8")
    simulator_status = example_tester(
        report_command, want_file_name=None, pytest_options=None
    )
    got = simulator_status.runner_status.stdout
    checker(want, got)


def test_directive3_example(example_tester, checker):
    """Make sure generated --outfile and --report are as expected."""

    # Note that the report_command is hard coded here.
    # The command shown in README.md is not tested.
    report_command = "phmdoctest doc/directive3.md --report"

    directive_command = labeled.contents(label="directive-3-outfile")
    _ = example_tester(
        directive_command, want_file_name="doc/test_directive3.py", pytest_options=None
    )
    want = Path("doc/directive3_report.txt").read_text(encoding="utf-8")
    simulator_status = example_tester(
        report_command, want_file_name=None, pytest_options=None
    )
    got = simulator_status.runner_status.stdout
    checker(want, got)


def test_inline_pass(checker):
    """Show the result block is produced by the code block."""
    code = labeled.contents(label="pass-code")
    assert code
    want, num_commented_out = phmdoctest.inline.apply_inline_commands(code)
    got = labeled.contents(label="pass-result")
    assert num_commented_out == 1
    checker(want, got)


def test_inline_omit(checker):
    """Show the result block is produced by the code block."""
    code = labeled.contents(label="omit-code")
    assert code
    want, num_commented_out = phmdoctest.inline.apply_inline_commands(code)
    got = labeled.contents(label="omit-result")
    assert num_commented_out == 2
    checker(want, got)


def test_inline_example(example_tester):
    """Make sure generated --outfile is as the same as on disk."""
    directive_command = labeled.contents(label="inline-outfile")
    _ = example_tester(
        directive_command,
        want_file_name="doc/test_inline_example.py",
        pytest_options=None,
    )


def test_skip_example(example_tester, checker):
    """Make sure generated --outfile and --report are as expected."""
    skip_command = labeled.contents(label="skip-command")
    want = labeled.contents(label="skip-report")
    short_form_command = labeled.contents(label="short-skip-command")
    simulator_status = example_tester(
        skip_command, want_file_name="doc/test_example2.py", pytest_options=None
    )
    got1 = simulator_status.runner_status.stdout
    checker(want, got1)

    # test the first -s form of the --skip
    simulator_status = example_tester(
        short_form_command, want_file_name="doc/test_example2.py", pytest_options=None
    )
    got2 = simulator_status.runner_status.stdout
    checker(want, got2)


def test_setup_report_example(example_tester, checker):
    """Make sure report in README is correct."""
    command = labeled.contents(label="setup-command-report")
    want = labeled.contents(label="setup-report")
    simulator_status = example_tester(command, want_file_name=None, pytest_options=None)
    got1 = simulator_status.runner_status.stdout
    checker(want, got1)


def test_setup(example_tester):
    """Make sure --setup --outfile is correct."""
    command = labeled.contents(label="setup-command-outfile")
    _ = example_tester(command, want_file_name="doc/test_setup.py", pytest_options=None)


def test_setup_doctest(example_tester):
    """Make sure --setup-doctest --outfile is correct."""
    command = labeled.contents(label="setup-doctest-outfile")
    _ = example_tester(
        command, want_file_name="doc/test_setup_doctest.py", pytest_options=None
    )


def test_outfile_to_stdout(example_tester, checker):
    """Make sure generated --outfile and --report are as expected."""
    outfile_command1 = labeled.contents(label="outfile-dash1")
    outfile_command2 = labeled.contents(label="outfile-dash2")
    simulator_status = example_tester(
        outfile_command1, want_file_name=None, pytest_options=None
    )
    want = Path("doc/test_example2.py").read_text(encoding="utf-8")
    got1 = simulator_status.runner_status.stdout
    checker(want, got1)

    simulator_status = example_tester(
        outfile_command2, want_file_name=None, pytest_options=None
    )
    got2 = simulator_status.runner_status.stdout
    checker(want, got2)


def test_usage(checker):
    """Example usage near the bottom."""
    # Note- There may be differences in whitespace between
    #       the README.md fenced code block and the
    #       phmdoctest --help output caused by the
    #       the terminal width when the installed
    #       phmdoctest command is executed.
    # Note- This test runs phmdoctest by calling the simulator
    #       which calls  Click.CliRunner.invoke().  invoke()
    #       displays entry-point as the calling program.
    #       The test here replaces 'entry-point' with 'phmdoctest'.
    simulator_status = phmdoctest.simulator.run_and_pytest(
        "phmdoctest --help", pytest_options=None
    )
    assert simulator_status.runner_status.exit_code == 0
    assert simulator_status.pytest_exit_code is None
    want1 = labeled.contents(label="usage")
    want2 = re.sub(r"\s+", " ", want1)

    got1 = simulator_status.runner_status.stdout
    got2 = got1.replace("entry-point", "phmdoctest", 1)
    got3 = re.sub(r"\s+", " ", got2)
    checker(want2, got3)


def test_testfile(checker):
    """Assure the guts of the callable_function are same as in Markdown."""
    example_code_checker(
        callable_function=test_testfile_example_code,
        example_string=labeled.contents(label="main-testfile"),
        checker_function=checker,
    )


# Runnable version of example code in README.md.
# The guts of this function are an exact copy of the example
# in README.md with label main-testfile.
# Note that this file is collected and run by pytest.
# Show main.testfile() usage. Verify correct file is generated.
def test_testfile_example_code():
    from pathlib import Path
    import phmdoctest.main

    generated_testfile = phmdoctest.main.testfile(
        "doc/setup.md",
        setup="FIRST",
        teardown="LAST",
    )
    expected = Path("doc/test_setup.py").read_text(encoding="utf-8")
    assert expected == generated_testfile


def test_simulator(checker):
    """Assure the guts of callable_function are same as in Markdown."""
    example_code_checker(
        callable_function=test_simulator_example_code,
        example_string=labeled.contents(label="simulator"),
        checker_function=checker,
    )


# Runnable version of example code in README.md.
# The guts of this function are an exact copy of the example
# in README.md with label simulator.
# Note that this file is collected and run by pytest.
# Show simulator.run_and_pytest() usage.
def test_simulator_example_code():
    import phmdoctest.simulator

    command = "phmdoctest doc/example1.md --report --outfile temporary.py"
    simulator_status = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command, pytest_options=["--doctest-modules", "-v"]
    )
    assert simulator_status.runner_status.exit_code == 0
    assert simulator_status.pytest_exit_code == 0


def test_quick_links():
    """Make sure the README.md quick links are up to date."""
    filename = "README.md"
    readme = Path("README.md").read_text(encoding="utf-8")
    github_links = make_quick_links(filename)
    # There must be at least one blank line after the last link.
    assert github_links + "\n\n" in readme


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


def make_label(title):
    """Make the [] part of a link.  Rewrite if last word is 'option'."""
    # Special handling if the last word of the title is option.
    # The word option indicates the preceding word should have the
    # prefix '--' in the link label since it is a command line option.
    # Titles with '--' seem to break on GitHub pages.
    parts = title.split()
    if parts[-1] == "option":
        parts.pop(-1)
        parts[-1] = "--" + parts[-1]
    title = " ".join(parts)
    return "[" + title + "]"


def make_quick_links(filename):
    """Generate links for a quick links section."""
    header_level = "## "  # note trailing space
    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()
    lines = [line.rstrip() for line in lines]  # lose newlines
    # README.md has fenced code blocks that enclose other
    # fenced code blocks.  The outer blocks use ~~~ as the fence.
    # Remove the outer fenced code blocks first.
    lines = remove_fenced_code_blocks(lines, "~~~")
    lines = remove_fenced_code_blocks(lines)
    links = []
    for line in lines:
        if line.startswith(header_level):
            assert "--" not in line, "Please rewrite to avert breakage on Pages."
            title = line.replace(header_level, "")
            label = make_label(title)
            link = title.lower()
            link = link.replace(" ", "-")
            link = "(#" + link + ")"
            links.append(label + link)
    return " |\n".join(links)


if __name__ == "__main__":
    # To generate quick links, from repository root run: python tests/test_readme.py
    text = make_quick_links("README.md")
    print(text)
    print()
    num_links = text.count("\n") + 1
    print("created {} links, {} characters".format(num_links, len(text)))
