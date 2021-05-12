.. toctree::
   :maxdepth: 2

Development tools API
~~~~~~~~~~~~~~~~~~~~~


Read contents of Markdown fenced code blocks
============================================

.. module:: phmdoctest.tool

.. autoclass::  FCBChooser
.. automethod:: FCBChooser.__init__
.. automethod:: FCBChooser.contents

.. autofunction:: labeled_fenced_code_blocks

.. autofunction:: fenced_code_blocks

.. autofunction:: fenced_block_nodes


Get elements from test suite JUnit XML output
=============================================

.. autofunction:: extract_testsuite


Test phmdoctest from within a python script
===========================================

.. module:: phmdoctest.simulator

.. autofunction:: run_and_pytest
