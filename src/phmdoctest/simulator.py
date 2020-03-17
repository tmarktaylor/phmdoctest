"""Simulate running a phmdoctest command. Used for testing.

Use during development to verify phmdoctest console commands
will succeed when called by Continuous Integration scripts.
If --outfile writes a file, the file is written in a
temporary directory.
Optionally run pytest on the temporary file.
"""

from collections import namedtuple
import itertools
import os.path
import re
from tempfile import TemporaryDirectory
from typing import List, Optional

from click.testing import CliRunner

from .main import entry_point


TestStatus = namedtuple(
    'TestStatus',
    ['status',    # click.CliRunner().invoke() return value
     'outfile',   # copy of the output file as a string
     'pytest_exit_code'])
"""run_and_pytest() return value."""


counter = itertools.count()
"""
Iterator that counts up from zero. Used for making a filename.

It is used to make a unique basename (or PurePath.name) when
the invoked phmdoctest writes an OUTFILE into the tempdir.
This avoids a pytest error when:
1. simulate_and_pytest() is called a from a
   pytest test case function.
2. simulate_and_pytest() is called a second time from the
   same pytest test case function.
3. both simulate_and_pytest() calls also call pytest.main()

  import file mismatch:
  imported module 'test_1' has this __file__ attribute:
    <temp dir absolute path>test_1.py
  which is not the same as the test file we want to collect:
   <different temp dir absolute path>test_1.py
  HINT: remove __pycache__ / .pyc files and/or use a
  unique basename for your test file modules

  To see this happen set up 1-3 above and patch counter
  here to: counter = itertools.cycle([1])
"""


def run_and_pytest(
        well_formed_command: str,
        pytest_options: Optional[List[str]] = None) -> TestStatus:
    """
    Simulate a phmdoctest command, optionally run pytest.

    If a filename is provided by the --outfile option, the
    command is rewritten replacing the OUTFILE with a
    path to a temporary directory and a synthesized filename.

    To run pytest on an --outfile, pass a list of zero or
    more pytest_options.
    To run pytest the PYPI package pytest must be installed
    since pytest is not required to install phmdoctest.
    Use this command:
        pip install pytest

    Returns TestStatus object.
    TestStatus.status is the CliRunner.invoke return value.

    If an outfile is written or streamed to stdout a copy of it
    is returned in TestStatus.outfile.

    Args:
        well_formed_command
            - starts with phmdoctest
            - followed by MARKDOWN_FILE
            - ends with --outfile OUTFILE (if needed)
            - all other options are between MARKDOWN_FILE and --outfile
            for example:
            phmdoctest MARKDOWN_FILE --skip FIRST --outfile OUTFILE

        pytest_options
            List of strings like this: ['--strict', '-v'].
            Set to empty list to run pytest with no options.
            Set to None to skip pytest.

    Returns:
        TestStatus containing status, outfile, and pytest_exit_code.
    """
    # chop off phmdoctest since invoking by a python function call
    assert well_formed_command.startswith('phmdoctest ')
    command1 = well_formed_command.replace('phmdoctest ', '', 1)
    # simulate commands that don't write OUTFILE.
    wants_help = '--help' in command1
    wants_version = '--version' in command1
    stream_outfile = (
            command1.endswith('--outfile -') or
            command1.endswith('--outfile=-')
    )
    no_outfile = '--outfile' not in command1
    runner = CliRunner()
    if wants_help or wants_version or stream_outfile or no_outfile:
        return TestStatus(
            status=runner.invoke(cli=entry_point, args=command1),
            outfile=None,
            pytest_exit_code=None
        )

    # Simulate commands that write an OUTFILE.
    # Split up the command into pieces.
    # Chop out the path to the markdown file.
    # Drop the rest of the command starting at --outfile and the
    # outfile path since we rename the outfile in the invoked command.
    with TemporaryDirectory() as tmpdirname:
        # Create a new unique filename in the temporary directly to
        # receive the OUTFILE.
        # Rewrite the command to use the new OUTFILE path and
        # split up the command to a list of strings.
        # Calling invoke with the single string form of the
        # rewritten command fails to find the outfile.
        # This might be because it is now an absolute path
        # to the tmpdir.
        # counter's docstring explains its use.
        test_file_name = 'test_' + str(next(counter)) + '.py'
        outfile_path = os.path.join(tmpdirname, test_file_name)
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
        command4 = command3.replace('--skip=', '--skip ')
        # get characters between double quotes including the quotes
        # get runs of non-whitespace characters
        args1 = re.findall(pattern=r'(".*"|\S+)', string=command4)
        # todo- issue breaks if more than double quoted string on the line

        # If both leading and trailing double quotes, remove them.
        args2 = [re.sub('^"(.*)"$', r'\1', arg) for arg in args1]
        phm_args.extend(args2)
        phm_args.extend(['--outfile', outfile_path])
        status = runner.invoke(cli=entry_point, args=phm_args)

        # return now if the command failed
        if status.exit_code:
            return TestStatus(
                status=status,
                outfile=None,
                pytest_exit_code=None
            )

        # Copy the generated pytest file from the isolated filesystem.
        with open(outfile_path, 'r') as fp:
            outfile_text = fp.read()

        pytest_exit_code = None
        if pytest_options is not None:
            import pytest    # type: ignore
            print()    # desirable if terminal shows captured stdout
            pytest_exit_code = pytest.main(pytest_options + [tmpdirname])
        return TestStatus(
            status=status,
            outfile=outfile_text,
            pytest_exit_code=pytest_exit_code
        )
