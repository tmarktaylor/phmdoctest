"""Simulate running a phmdoctest command. Used for testing.

Use during development to verify phmdoctest console commands
will succeed when called by Continuous Integration scripts.
If --outfile writes a file, the file is written in a
temporary directory.
Optionally run pytest on the temporary file.
"""

from pathlib import Path
import re
import subprocess
import sys
from tempfile import TemporaryDirectory
from typing import List, Optional, NamedTuple

import click.testing

from phmdoctest.main import entry_point


SimulatorStatus = NamedTuple(
    "SimulatorStatus",
    [
        ("runner_status", click.testing.Result),
        ("outfile", Optional[str]),
        ("pytest_exit_code", Optional[int]),
        ("junit_xml", Optional[str]),
    ],
)
"""run_and_pytest() return value."""


def run_and_pytest(
    well_formed_command: str,
    pytest_options: Optional[List[str]] = None,
    junit_family: Optional[str] = None,
) -> SimulatorStatus:
    """
    Simulate a phmdoctest command, optionally run pytest.

    If a filename is provided by the ``--outfile`` option, the
    command is rewritten replacing the OUTFILE with a
    path to a temporary directory and a synthesized filename.

    To run pytest on an ``--outfile``, pass a list of zero or
    more pytest_options.  pytest is run in a subprocess.

    The PYPI package pytest must be installed separately
    since pytest is not required to install phmdoctest.
    Use this command: ``pip install pytest``

    Returns SimulatorStatus object.
    SimulatorStatus.runner_status is the CliRunner.invoke return value.

    If an outfile is streamed to stdout a copy of it
    is found in simulator_status.runner_status.stdout.

    If calling run_and_pytest() from a pytest file, try adding the
    pytest option ``--capture=tee-sys`` to the command running
    pytest on the file.

    For example on a checkout of phmdoctest the command line:

    ``python -m pytest tests -v --capture=tee-sys``

    will print the outputs from the subprocess.run() invocations
    of pytest on the ``--outfile`` written to the temporary directory.
    A wild guess would be that the subprocess inherited changes
    made to the parent by --capture=tee-sys.

    Args:
        well_formed_command
            - starts with phmdoctest
            - followed by MARKDOWN_FILE
            - ends with ``--outfile`` OUTFILE (if needed)
            - all other options are between MARKDOWN_FILE and ``--outfile``
              for example:
              ``phmdoctest MARKDOWN_FILE --skip FIRST --outfile OUTFILE``

        pytest_options
            List of strings like this: ``["--doctest-modules", "-v"]``.
            Set to empty list to run pytest with no options.
            Set to None to skip pytest.

        junit_family
            Configures the format of the Pytest generated JUnit XML string
            returned in SimulatorStatus.  The value is used for the
            Pytest configuration option of the same name.
            Set to None or the empty string to skip XML generation.

    Returns:
        SimulatorStatus containing runner_status, outfile,
        pytest_exit_code, and generated JUnit XML.
    """
    if not well_formed_command.startswith("phmdoctest "):
        raise ValueError("phmdoctest- well_formed_command must start with phmdoctest")

    # trim off any trailing whitespace
    command0 = well_formed_command.rstrip()
    # chop off phmdoctest since invoking by a python function call
    command1 = command0.replace("phmdoctest ", "", 1)
    # simulate commands that don't write OUTFILE.
    wants_help = "--help" in command1
    wants_version = "--version" in command1
    stream_outfile = command1.endswith("--outfile -") or command1.endswith(
        "--outfile=-"
    )
    no_outfile = "--outfile" not in command1
    runner = click.testing.CliRunner()
    if wants_help or wants_version or stream_outfile or no_outfile:
        return SimulatorStatus(
            runner_status=runner.invoke(cli=entry_point, args=command1),
            outfile=None,
            pytest_exit_code=None,
            junit_xml="",
        )

    # Simulate commands that write an OUTFILE.
    # Split up the command into pieces.
    # Chop out the path to the markdown file.
    # Drop the rest of the command starting at --outfile and the
    # outfile path since we rename the outfile in the invoked command.
    with TemporaryDirectory() as tmpdir:
        # Create a filename in the temporary directory to
        # receive the OUTFILE.
        # Rewrite the command to use the new OUTFILE path and
        # split up the command to a list of strings.
        # Calling invoke with the single string form of the
        # rewritten command fails to find the outfile.
        # This might be because it is now an absolute path
        # to the tmpdir.
        markdown_path, command2 = command1.split(maxsplit=1)
        markdown_name = Path(markdown_path).name
        outfile_name = "test_" + markdown_name.replace(".md", ".py")
        outfile_path = Path(tmpdir) / outfile_name
        command3 = command2[: command2.find("--outfile")].strip()

        # Split up the rest of the command into pieces to pass to
        # runner.invoke().
        #
        # Developers:
        # Note the --outfile part has already been removed from command3.
        # If a new option that takes TEXT is added, add code here
        # to replace its '='.
        #
        # Special code to handle a --skip TEXT where TEXT is double quoted.
        # For example
        #    --skip="Python 3.7"
        #         or
        #    --skip "Python 3.7"
        command4a = command3.replace("--skip=", "--skip ")
        command4b = command4a.replace("--setup=", "--setup ")
        command4 = command4b.replace("--teardown=", "--teardown ")

        # get characters between double quotes including the quotes
        # get runs of non-whitespace characters
        args1 = re.findall(pattern=r'("[^"]*"|\S+)', string=command4)
        # If both leading and trailing double quotes, remove them.
        args2 = [re.sub('^"([^"]*)"$', r"\1", arg) for arg in args1]
        phm_args = [markdown_path]
        phm_args.extend(args2)
        phm_args.extend(["--outfile", str(outfile_path)])
        runner_status = runner.invoke(cli=entry_point, args=phm_args)

        # return now if the command failed
        if runner_status.exit_code:
            return SimulatorStatus(
                runner_status=runner_status,
                outfile=None,
                pytest_exit_code=None,
                junit_xml="",
            )

        # Copy the generated pytest file from the temporary directory.
        outfile_text = outfile_path.read_text(encoding="utf-8")

        if pytest_options is None:
            return SimulatorStatus(
                runner_status=runner_status,
                outfile=outfile_text,
                pytest_exit_code=None,
                junit_xml="",
            )
        else:
            # Run python -m pytest [options] in a subprocess.
            commandline = [sys.executable, "-m", "pytest"] + pytest_options
            if junit_family:
                junit_name = outfile_name.replace(".py", ".xml")
                junit_path = Path(tmpdir) / junit_name
                commandline.append("--junitxml=" + str(junit_path))
                commandline.append("-o junit_family=" + junit_family)
            commandline.append(tmpdir)
            completed = subprocess.run(commandline)

            xml = ""
            if junit_family:
                xml = junit_path.read_text(encoding="utf-8")

            return SimulatorStatus(
                runner_status=runner_status,
                outfile=outfile_text,
                pytest_exit_code=completed.returncode,
                junit_xml=xml,
            )
