# Recent changes
1.3.0 - 2021-11-08

- Add main.testfile().
- Add testfile_creator and testfile_tester fixtures.
- Bugfix- Issue- Generated test name has output_NN when skip
  directive on output block.
- Bugfix- Issue- mark.skipif example code causes pytest AST fail at
  assertion rewrite time. Happens on skipped Python version.
  Replaced with code that compiles on the skipped version.
- Drop Python 3.7 add Python 3.10.

tests:

- Add mode=0o700 to mkdir() calls in test .yml files.
- Run tests in virtual envirionments. ci.yml.
- Add test_details.py.
- Add Appveyor to CI to show pytest items.
- Rework requirements files. Add tests.
- Refactor new fixtures to conftest.py.
- Rework/refactor quick_links test logic.
- Add test to find trailing spaces in sources.
- Tox no longer used in test suite.

docs:
- Bugfix- Issue- Markdown header level out of sequence.
- Loosen doc dependencies.
- Fenced code block info_string pycon -> py.
- Sphinx with myst_parser for docs.

style:
- Style/pep8/inspection fixes.
- Path and open changes.
- Remove trailing spaces from ~25 files.


1.2.1 - 2021-07-07

- Bugfix- #16, #15, Issue- Simulator subprocess failed on win venv.
- Code Quality fixes: assert --> raise.
- Make fenced code block info_strings compatible with GitHub pages.
- Restored tox.ini.

1.2.0 - 2021-06-09

- Add inline annotations.
- Reformat code style with black.
- Rework setup.py/setup.cfg.
- Remove tox.
- Fix bad example in README.md.

1.1.1 - 2021-05-14

- Bugfix- Pull Request #6, Issue #8 --outfile missing `import pytest`.
- Documentation typo fixes.

1.1.0 - 2021-05-12

- Add test directives taken from HTML comments in .md.
- Implement setup/teardown with Pytest fixtures.
- Use difflib.ndiff to show unexpected output.
- Add simulator feature to return JUnitXML from pytest.

1.0.1 - 2020-12-16

- Bugfix- Issue #4- pytest fails in pypy3 if using --setup, --setup-doctest.
- Removed pytest --strict option since not needed.

1.0.0 - 2020-07-12

- New feature to do setup and teardown code block.

0.1.0 - 2020-06-14

- New feature to handle Python interactive sessions.

0.0.6 - 2020-06-07

- Bugfix- Issue- Skip pattern matching start of code ignored.

0.0.5 - 2020-04-20

- Bugfix- Issue- Won't fail if Python code block doesn't print.
- Bugfix- Issue- README CI example missing "install:".
- Add Development tools API section to the documentation.
- Pin phmdoctest dependency version ranges in setup.py.

0.0.4 - 2020-04-02

- Changes to build documentation on readthedocs.org.
- Inspection fixes.

0.0.3 - 2020-03-18

- Initial upload to Python Package Index.
