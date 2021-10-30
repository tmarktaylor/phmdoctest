.. toctree::
   :maxdepth: 2

Development tools API for version 1.3.0
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Python API to generate a pytest file.
=====================================
.. module:: phmdoctest.main

.. autofunction:: testfile


Test with Pytest fixtures.
==========================

.. module:: phmdoctest.tester

.. autofunction:: testfile_creator

.. autofunction:: testfile_tester


Simulate the command line.
==========================

.. module:: phmdoctest.simulator

.. autofunction:: run_and_pytest


Read contents of Markdown fenced code blocks.
=============================================

.. module:: phmdoctest.tool

.. autoclass::  FCBChooser
.. automethod:: FCBChooser.__init__
.. automethod:: FCBChooser.contents

.. autofunction:: labeled_fenced_code_blocks

.. autofunction:: fenced_code_blocks

.. autofunction:: fenced_block_nodes


Get elements from test suite JUnit XML output.
==============================================

.. autofunction:: extract_testsuite
