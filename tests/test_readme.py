"""pytest test cases for examples in fenced code blocks in README.md."""

import re

import phmdoctest.main
import phmdoctest.direct
import phmdoctest.inline
import phmdoctest.simulator
import phmdoctest.tool
import verify
import quick_links

# Caution:
# This test file is run by pytest.
# The call to invoke_and_pytest() will start pytest in a
# subprocess.
# Pytest captures stdout and so does CliRunner.invoke().

# Fenced code blocks that have the phmdoctest-label directive.
labeled = phmdoctest.tool.FCBChooser("README.md")


def test_directive_example_raw():
    """README raw markdown is same as the disk file."""
    want = labeled.contents(label="directive-example-raw")
    with open("tests/one_mark_skip.md", "r", encoding="utf-8") as fp:
        got = fp.read()
        verify.a_and_b_are_the_same(want, got)


def test_directive_example():
    """Make sure generated --outfile is as expected; Run pytest.

    Check the --outfile against the copy in the fenced code block.
    """
    example1_command = labeled.contents(label="directive-example-command")
    want = labeled.contents(label="directive-example-outfile")
    simulator_status = verify.one_example(
        example1_command,
        want_file_name=None,
        pytest_options=["--doctest-modules", "-v"],
    )
    # Fenced code block in README.md is the same as the --outfile.
    got = simulator_status.outfile
    verify.a_and_b_are_the_same(want, got)
    assert simulator_status.pytest_exit_code == 0


def test_raw_example1_md():
    """README raw markdown is same as file doc/example1.md."""
    want = labeled.contents(label="example1-raw")
    with open("doc/example1.md", "r", encoding="utf-8") as fp:
        got = fp.read()
        verify.a_and_b_are_the_same(want, got)


def test_example1():
    """Make sure generated --outfile is as expected; Run pytest.

    Check the copy of test_example1.py in the fenced code block.
    """
    # The helper checks the generated --outfile against the disk file.
    example1_command = labeled.contents(label="example1-command")
    want = labeled.contents(label="example1-outfile")
    _ = verify.one_example(
        example1_command, want_file_name="doc/test_example1.py", pytest_options=None
    )
    # Make sure the copy of test_example1.py in README.md
    # is the same as the disk file.
    with open("doc/test_example1.py", "r", encoding="utf-8") as fp:
        got = fp.read()
        verify.a_and_b_are_the_same(want, got)

    # Run again and call pytest to make sure the file works with pytest.
    simulator_status = verify.one_example(
        example1_command,
        want_file_name=None,
        pytest_options=["--doctest-modules", "-v"],
    )
    assert simulator_status.pytest_exit_code == 0


def test_report():
    """README report output is same as produced by the command."""
    report_command = labeled.contents(label="report-command")
    want = labeled.contents(label="example2-report")
    simulator_status = phmdoctest.simulator.run_and_pytest(
        report_command, pytest_options=None
    )
    assert simulator_status.runner_status.exit_code == 0
    assert simulator_status.pytest_exit_code is None
    got = simulator_status.runner_status.stdout
    verify.a_and_b_are_the_same(want, got)


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


def test_fcb_chooser(capsys):
    """Check 3 parts of the label on any fenced code block example."""
    # 1. The .md shown in the fenced code block is the same
    #    as the file on disk.
    want = labeled.contents(label="my-markdown-file")
    with open("doc/my_markdown_file.md", "r", encoding="utf-8") as fp:
        got = fp.read()
    verify.a_and_b_are_the_same(want, got)

    # 2. The Python code example in the fenced code block is the same as
    #    the body of the function chooser_example_code() above.
    verify.example_code_checker(
        callable_function=chooser_example_code,
        example_string=labeled.contents(label="fetch-it"),
    )

    # 3. The example output shown in the fenced code block is
    #    the same as the output from running chooser_example_code().
    want3 = labeled.contents(label="fetched-contents")
    assert want3
    chooser_example_code()
    got3 = capsys.readouterr().out
    assert got3.endswith("\n\n"), "FCB newline + print() newline"
    got3 = got3[:-1]  # drop the newline that print() added.
    verify.a_and_b_are_the_same(want3, got3)


def test_setup_first_fcb():
    """Make sure example setup fenced code block same as in the file."""
    want = labeled.contents(label="setup-md-first-block")
    blocks = phmdoctest.tool.fenced_code_blocks("doc/setup.md")
    got = blocks[0]
    verify.a_and_b_are_the_same(want, got)


def test_directive1_example():
    """Make sure generated --outfile and --report are as expected."""

    # Note that the report_command is hard coded here.
    # The command shown in README.md is not tested.
    report_command = "phmdoctest doc/directive1.md --report"

    directive_command = labeled.contents(label="directive-1-outfile")
    _ = verify.one_example(
        directive_command, want_file_name="doc/test_directive1.py", pytest_options=None
    )

    with open("doc/directive1_report.txt") as f:
        want = f.read()
    simulator_status = verify.one_example(
        report_command, want_file_name=None, pytest_options=None
    )
    got = simulator_status.runner_status.stdout
    verify.a_and_b_are_the_same(want, got)


def test_directive2_example():
    """Make sure generated --outfile and --report are as expected."""

    # Note that the report_command is hard coded here.
    # The command shown in README.md is not tested.
    report_command = "phmdoctest doc/directive2.md --report"

    directive_command = labeled.contents(label="directive-2-outfile")
    _ = verify.one_example(
        directive_command, want_file_name="doc/test_directive2.py", pytest_options=None
    )

    with open("doc/directive2_report.txt") as f:
        want = f.read()
    simulator_status = verify.one_example(
        report_command, want_file_name=None, pytest_options=None
    )
    got = simulator_status.runner_status.stdout
    verify.a_and_b_are_the_same(want, got)


def test_directive3_example():
    """Make sure generated --outfile and --report are as expected."""

    # Note that the report_command is hard coded here.
    # The command shown in README.md is not tested.
    report_command = "phmdoctest doc/directive3.md --report"

    directive_command = labeled.contents(label="directive-3-outfile")
    _ = verify.one_example(
        directive_command, want_file_name="doc/test_directive3.py", pytest_options=None
    )

    with open("doc/directive3_report.txt") as f:
        want = f.read()
    simulator_status = verify.one_example(
        report_command, want_file_name=None, pytest_options=None
    )
    got = simulator_status.runner_status.stdout
    verify.a_and_b_are_the_same(want, got)


def test_inline_pass():
    """Show the result block is produced by the code block."""
    code = labeled.contents(label="pass-code")
    assert code
    want, num_commented_out = phmdoctest.inline.apply_inline_commands(code)
    got = labeled.contents(label="pass-result")
    assert num_commented_out == 1
    verify.a_and_b_are_the_same(want, got)


def test_inline_omit():
    """Show the result block is produced by the code block."""
    code = labeled.contents(label="omit-code")
    assert code
    want, num_commented_out = phmdoctest.inline.apply_inline_commands(code)
    got = labeled.contents(label="omit-result")
    assert num_commented_out == 2
    verify.a_and_b_are_the_same(want, got)


def test_inline_example():
    """Make sure generated --outfile is as the same as on disk."""
    directive_command = labeled.contents(label="inline-outfile")
    _ = verify.one_example(
        directive_command,
        want_file_name="doc/test_inline_example.py",
        pytest_options=None,
    )


def test_skip_example():
    """Make sure generated --outfile and --report are as expected."""
    skip_command = labeled.contents(label="skip-command")
    want = labeled.contents(label="skip-report")
    short_form_command = labeled.contents(label="short-skip-command")
    simulator_status = verify.one_example(
        skip_command, want_file_name="doc/test_example2.py", pytest_options=None
    )
    got1 = simulator_status.runner_status.stdout
    verify.a_and_b_are_the_same(want, got1)

    # test the first -s form of the --skip
    simulator_status = verify.one_example(
        short_form_command, want_file_name="doc/test_example2.py", pytest_options=None
    )
    got2 = simulator_status.runner_status.stdout
    verify.a_and_b_are_the_same(want, got2)


def test_setup_report_example():
    """Make sure report in README is correct."""
    command = labeled.contents(label="setup-command-report")
    want = labeled.contents(label="setup-report")
    simulator_status = verify.one_example(
        command, want_file_name=None, pytest_options=None
    )
    got1 = simulator_status.runner_status.stdout
    verify.a_and_b_are_the_same(want, got1)


def test_setup():
    """Make sure --setup --outfile is correct."""
    command = labeled.contents(label="setup-command-outfile")
    _ = verify.one_example(
        command, want_file_name="doc/test_setup.py", pytest_options=None
    )


def test_setup_doctest():
    """Make sure --setup-doctest --outfile is correct."""
    command = labeled.contents(label="setup-doctest-outfile")
    _ = verify.one_example(
        command, want_file_name="doc/test_setup_doctest.py", pytest_options=None
    )


def test_outfile_to_stdout():
    """Make sure generated --outfile and --report are as expected."""
    outfile_command1 = labeled.contents(label="outfile-dash1")
    outfile_command2 = labeled.contents(label="outfile-dash2")
    simulator_status = verify.one_example(
        outfile_command1, want_file_name=None, pytest_options=None
    )
    with open("doc/test_example2.py", "r", encoding="utf-8") as fp:
        want = fp.read()
    got1 = simulator_status.runner_status.stdout
    verify.a_and_b_are_the_same(want, got1)

    simulator_status = verify.one_example(
        outfile_command2, want_file_name=None, pytest_options=None
    )
    got2 = simulator_status.runner_status.stdout
    verify.a_and_b_are_the_same(want, got2)


def test_usage():
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
    verify.a_and_b_are_the_same(want2, got3)


# Developers: Changes here must be mirrored in a Markdown FCB in README.md.
# Runnable version of example code in README.md.
# The guts of this function are an exact copy of example in README.md.
def simulator_example_code():
    import phmdoctest.simulator

    command = "phmdoctest doc/example1.md --report --outfile test_me.py"
    simulator_status = phmdoctest.simulator.run_and_pytest(
        well_formed_command=command, pytest_options=["--doctest-modules", "-v"]
    )
    assert simulator_status.runner_status.exit_code == 0
    assert simulator_status.pytest_exit_code == 0


def test_simulator():
    """Assure the guts of the function are same as in Markdown."""
    verify.example_code_checker(
        callable_function=simulator_example_code,
        example_string=labeled.contents(label="simulator"),
    )

    # also make sure the code runs with no assertions
    simulator_example_code()


def test_quick_links():
    """Make sure the README.md quick links are up to date."""
    filename = "README.md"
    with open(filename, "r", encoding="utf-8") as f:
        readme = f.read()
        github_links = quick_links.make_quick_links(filename, style="github")
        # There must be at least one blank line after the last link.
        assert github_links + "\n\n" in readme
