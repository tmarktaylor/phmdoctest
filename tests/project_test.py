"""Example pytest usage of testfile_creator and testfile_tester fixtures.

pytester requires conftest.py in tests folder with pytest_plugins = [“pytester”]
Requires pytest >= 6.2.
"""

from phmdoctest.tester import testfile_creator
from phmdoctest.tester import testfile_tester


def test_generate_run_project(testfile_creator, testfile_tester):
    """Generate pytest file from project.md and run it with pytester."""
    testfile = testfile_creator("project.md")
    result = testfile_tester(
        contents=testfile, pytest_options=["-v", "--doctest-modules"]
    )
    result.assert_outcomes(passed=4)
