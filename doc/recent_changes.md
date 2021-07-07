## Recent changes
1.2.1 - 2021-07-07

- Bugfix- #16, #15, Issue- Simulator subprocess failed on win venv.
- Code Quality fixes: assert --> raise.
- Make fenced code block info_strings compatible with GitHub pages.

1.2.0 - 2021-06-09

- Add inline annotations.
- Reformat code style with black.
- Rework setup.py/setup.cfg.
- Remove tox.
- Fix bad travis example in README.md.

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
- Bugfix- Issue- README Travis CI example missing "install:".
- Add Development tools API section to the documentation.
- Pin phmdoctest dependency version ranges in setup.py.

0.0.4 - 2020-04-02

- Changes to build documentation on readthedocs.org.
- Inspection fixes.

0.0.3 - 2020-03-18

- Initial upload to Python Package Index.
