About the documentation
-----------------------

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

- Github hosts the repository and renders README.md.
- readthedocs.org hosts the HTML and creates the PDF for offline use.
- Nearly everything is in README.md. These aren't:

  - about.md - About the documentation (this page).
  - recent_changes.md - Recent Changes.

Tools
~~~~~

- Sphinx
- recommonmark

recommonmark enables Sphinx to parse Markdown files.

Files
~~~~~

These files are at the project root:

- .readthedocs.yml
- index.rst
- README.md
- conf.py

These files are not part of the documentation.
They are expected values used by the regression test suite.

- doc/test_example1.py
- doc/test_example2.py

Read the Docs hosting
~~~~~~~~~~~~~~~~~~~~~

The Sphinx documentation is hosted by readthedocs.org.
The documentation build dependencies ``doc/requirements.txt`` are
pinned to what is currently available.

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
