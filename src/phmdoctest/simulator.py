"""Simulate running a phmdoctest command. Used for testing.

Use during development to verify phmdoctest console commands
will succeed when called by Continuous Integration scripts.
If --outfile writes a file, the file is written in a
temporary directory.
Optionally run pytest on the temporary file.
"""

import os.path
import re
import subprocess
from tempfile import TemporaryDirectory
from typing import List, Optional, NamedTuple

import click.testing

from phmdoctest.main import entry_point


SimulatorStatus = NamedTuple(
    'SimulatorStatus',
    [('runner_status', click.testing.Result),
     ('outfile', Optional[str]),
     ('pytest_exit_code', Optional[int])
     ])
"""run_and_pytest() return value."""


def run_and_pytest(
        well_formed_command: str,
        pytest_options: Optional[List[str]] = None) -> SimulatorStatus:
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
            List of strings like this: ``['--strict',
            '--doctest-modules', '-v']``.
            Set to empty list to run pytest with no options.
            Set to None to skip pytest.

    Returns:
        SimulatorStatus containing runner_status, outfile,
        and pytest_exit_code.
    """
    assert well_formed_command.startswith('phmdoctest ')
    # trim off any trailing whitespace
    command0 = well_formed_command.rstrip()
    # chop off phmdoctest since invoking by a python function call
    command1 = command0.replace('phmdoctest ', '', 1)
    # simulate commands that don't write OUTFILE.
    wants_help = '--help' in command1
    wants_version = '--version' in command1
    stream_outfile = (
            command1.endswith('--outfile -') or
            command1.endswith('--outfile=-')
    )
    no_outfile = '--outfile' not in command1
    runner = click.testing.CliRunner()
    if wants_help or wants_version or stream_outfile or no_outfile:
        return SimulatorStatus(
            runner_status=runner.invoke(cli=entry_point, args=command1),
            outfile=None,
            pytest_exit_code=None
        )

    # Simulate commands that write an OUTFILE.
    # Split up the command into pieces.
    # Chop out the path to the markdown file.
    # Drop the rest of the command starting at --outfile and the
    # outfile path since we rename the outfile in the invoked command.
    with TemporaryDirectory() as tmpdirname:
        # Create a filename in the temporary directory to
        # receive the OUTFILE.
        # Rewrite the command to use the new OUTFILE path and
        # split up the command to a list of strings.
        # Calling invoke with the single string form of the
        # rewritten command fails to find the outfile.
        # This might be because it is now an absolute path
        # to the tmpdir.
        outfile_path = os.path.join(tmpdirname, 'test_sim_tmpdir.py')
        markdown_path, command2 = command1.split(maxsplit=1)
        command3 = command2[:command2.find('--outfile')].strip()
        phm_args = [markdown_path]

        # Split up the rest of the command into pieces to pass to
        # runner.invoke().
        #
        # Developers:
        # Since the --outfile part has already been removed from command3
        # the only possible option remaining that takes TEXT is --skip.
        # If a new option that takes TEXT is added, add code here
        # to replace its '='.
        #
        # Special code to handle a --skip TEXT where TEXT is double quoted.
        # For example
        #    --skip="Python 3.7"
        #         or
        #    --skip "Python 3.7"
        command4a = command3.replace('--skip=', '--skip ')
        command4b = command4a.replace('--setup=', '--setup ')
        command4 = command4b.replace('--teardown=', '--teardown ')

        # get characters between double quotes including the quotes
        # get runs of non-whitespace characters
        args1 = re.findall(pattern=r'("[^"]*"|\S+)', string=command4)
        # If both leading and trailing double quotes, remove them.
        args2 = [re.sub('^"([^"]*)"$', r'\1', arg) for arg in args1]
        phm_args.extend(args2)
        phm_args.extend(['--outfile', outfile_path])
        runner_status = runner.invoke(cli=entry_point, args=phm_args)

        # return now if the command failed
        if runner_status.exit_code:
            return SimulatorStatus(
                runner_status=runner_status,
                outfile=None,
                pytest_exit_code=None
            )

        # Copy the generated pytest file from the temporary directory.
        with open(outfile_path, 'r', encoding='utf-8') as fp:
            outfile_text = fp.read()

        pytest_exit_code = None
        if pytest_options is not None:
            completed = subprocess.run(
                ['python', '-m', 'pytest'] + pytest_options + [tmpdirname],
            )
            pytest_exit_code = completed.returncode

        return SimulatorStatus(
            runner_status=runner_status,
            outfile=outfile_text,
            pytest_exit_code=pytest_exit_code
        )
