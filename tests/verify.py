import phmdoctest.print_capture
import phmdoctest.simulator


def _verify_a_and_b_are_the_same(a, b):
    """Line by line helper compare function with assertion for pytest."""
    a_lines = a.splitlines()
    b_lines = b.splitlines()
    for a_line, b_line in zip(a_lines, b_lines):
        assert a_line == b_line


def one_example(
        well_formed_command,
        want_file_name=None,
        pytest_options=None):
    """Simulate running a phmdoctest command and pytest on the result."""
    result = phmdoctest.simulator.run_and_pytest(
        well_formed_command, pytest_options=pytest_options)
    # check that the phmdoctest command succeeded
    assert result.status.exit_code == 0

    # check the OUTFILE against the expected value
    if want_file_name is not None:
        with open(want_file_name) as f:
            want = f.read()
            # phmdoctest.print_capture.line_by_line_compare_exact(
            _verify_a_and_b_are_the_same(result.outfile, want)

    if pytest_options is not None:
        assert result.pytest_exit_code == 0
    return result
