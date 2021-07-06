# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

py_sources_path = os.path.abspath("./src")
sys.path.insert(0, py_sources_path)

# -- Project information -----------------------------------------------------

# This file is placed in the project root directory rather than /doc.

# Configuration for Sphinx 1.8.5

project = "phmdoctest"
copyright = "2021, Mark Taylor"
author = "Mark Taylor"

# The full version, including alpha/beta/rc tags
release = "1.2.1"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ["recommonmark", "sphinx.ext.autodoc", "sphinx.ext.napoleon"]

source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# tmarktaylor: The documentation sources are at the project root.
# Any .md, .rst, or folders at the project root that don't
# belong in the documentation should be listed here.
#

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [
    "tests",
    "src",
    ".tox",
    ".pytest_cache",
    "_build",
    "Thumbs.db",
    ".DS_Store",
    # for personal dev environments
    ".export*",
]

master_doc = "index"

# -- Options for HTML output -------------------------------------------------

on_rtd = os.environ.get("READTHEDOCS", None) == "True"
if not on_rtd:
    import sphinx_rtd_theme

    html_theme = "sphinx_rtd_theme"
    html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
# html_theme = 'alabaster'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = []  # ['_static']
