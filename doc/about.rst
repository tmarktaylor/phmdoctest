About the documentation
=======================

Goals
~~~~~

The documentation is constructed to achieve:

- Everything in the README.
- Python Package Index long description taken from the README.
- README at the Github repository root.
- Examples in the README are fully syntax highlighted.
- README examples are tested by the test suite.
- Downloadable static copy of the documentation for offline use.
- No visible raw ReStructured text in the README rendered by Github.

Implementation:

- Github hosts the repository and renders README.md
- readthedocs.org hosts the HTML and creates the PDF for offline use.
- Nearly everything is in README.md. These aren't:

  - about.md - About the documentation (this page)
  - recent_changes.md - Recent Changes.

Tools
~~~~~

- Sphinx
- recommonmark

recommonmark enables Sphinx to parse Markdown files.

Files
~~~~~

root

- .readthedocs.yml
- index.rst
- README.md

/doc

- conf.py
- about.rst
- recent_changes.md
- requirements.txt
- example1.md
- example2.md

The next 2 files are expected values used by the regression test suite.
They are not run as test cases. To avoid excluding them in the
pytest command line they were moved out of the tests folder.
They probably should be in a new folder.

- doc/test_example1.py
- doc/test_example2.py

Read the Docs hosting
~~~~~~~~~~~~~~~~~~~~~

The Sphinx documentation is hosted by readthedocs.org.
The versions in [doc/requirements.txt](requirements.txt) have been
pinned to what is currently available.

Issues
~~~~~~

- Sphinx insisted on an index.rst at the root.  README.md and index.md
  did not work. The currently commented out conf.py configuration
  def setup(app): did not solve this. This configuration is probably
  incorrect.

- Sphinx issues warnings for .md files not accesible through the toc tree.
  Since phmdoctest processes Markdown files there are several .md files
  that are examples in the docs and also processed by the test cases.

- Mkdocs was considered but could not be configured to build with README.md
  at the repository root.
  This problems is potentially solved by using Symlinks in the repository.
  That was not attempted. recommonmark and black use them to help build
  their documentation.

(excluded from contents)
~~~~~~~~~~~~~~~~~~~~~~~~

This section is here only to suppress Sphinx WARNING: document isn't
included in any toctree.  These files are referenced from README.md.

   example1.md | example2.md | test_example2.md

.. toctree::
   :maxdepth: 0
   :hidden:

   example1.md
   example2.md
   test_example2.md
