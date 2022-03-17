.. toctree::
   :maxdepth: 2

Development tools API version 1.4.0
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Generate a pytest file.
=======================
.. module:: phmdoctest.main

.. autofunction:: testfile


Generate pytest files using a configuration file.
=================================================
.. autofunction:: generate_using


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

.. autoclass:: FCBChooser
.. automethod:: FCBChooser.__init__
.. automethod:: FCBChooser.contents

.. autoclass:: LabeledFCB
.. autofunction:: labeled_fenced_code_blocks

.. autofunction:: fenced_code_blocks

.. autofunction:: fenced_block_nodes


Get elements from test suite JUnit XML output.
==============================================

.. autofunction:: extract_testsuite


Check a Markdown file for Python examples.
==========================================

.. autoclass:: PythonExamples
.. autofunction:: detect_python_examples


Prepare directory for generated test files.
===========================================

.. autofunction:: wipe_testfile_directory
