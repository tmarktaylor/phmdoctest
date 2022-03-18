# Using a configuration file

Just pass the configuration filename as the first argument instead
of a Markdown file. The other command line options are ignored.
The config file may be formatted as '.toml', .ini. or '.cfg'.
The phmdoctest configuration section `[tool.phmdoctest]` may
be added to pre-existing configuration files.

A separate invocation of pytest is needed to run the generated test files.

Here are some example invocations using a configuration file
that have the phmdoctest configuration section. These
configuration files are in the phmdoctest repository.

<!--phmdoctest-label invocations-->
```
phmdoctest pyproject.toml
pytest -v --doctest-modules .gendir-toml

phmdoctest setup.cfg
pytest -v --doctest-modules .gendir-cfg

phmdoctest tox.ini
pytest -v --doctest-modules .gendir-ini
```

You can also pass a configuration file by Python.
Look for the Python API in the readthedocs documentation.
See the section Development tools API 1.4.0.

This is a good starting point template section for a .toml format file.
```toml
[tool.phmdoctest]
# https://pypi.org/project/phmdoctest
# Writes pytest files generated from Markdown to output_directory.
# Invoke pytest separately to run the generated pytest files.

markdown_globs = [
    "README.md"
    "doc/*.md",
]
exclude_globs = [
]

output_directory = ".gendir-typical-toml"
print = ["filename", "summary"]
```

- Filenames and globs are relative to the current
  working directory of the shell that invokes phmdoctest.
- The output_directory can be relative or absolute.

Please see Python standard library pathlib Path.glob(pattern)
for glob syntax.
The `**` glob pattern indicates recursive directory search. We
could do the whole repository with (.toml)
`markdown_globs = ["**/*.md"]`

The generated test files get written to the directory specified
by `output_directory`.

The directory specified by `output_directory` is cleaned of all *.py
files before new test files are generated.
Pre-existing *.py files in the output directory are renamed. If
output_directory inadvertently gets pointed at a Python
source directory, the renamed files can be recovered by renaming them.

The `markdown_globs` key specifies Markdown files to select for
test file generation. The globs may be one per line or comma separated.
Comments are OK on separate lines or at the end of a line.

The `exclude_globs` key specifies Markdown files that should not
generate test files. Markdown files that don't have any Python examples
are automatically excluded.

The `print` key directs printing.

- If `filename` is present the filename is printed after test file generation
  and before the generated test file is written.
- If `summary` is present the number of test files generated
  is printed last.

To prevent printing everything set `print` like this:

```
# .ini, .cfg
print =

# .toml
print = []
```

Here is an example .cfg format configuration file used
for testing this project.
The .ini format is the same.

<!--phmdoctest-label generate-cfg-->
```cfg
# tests/generate.cfg
[tool.phmdoctest]
# https://pypi.org/project/phmdoctest
# Writes pytest files generated from Markdown to output_directory.
# Invoke pytest separately to run the generated pytest files.
markdown_globs =
    # Refer to Python standard library Path.glob(pattern)
    project.md
    doc/*.md
    tests/managenamespace.md  # inline comments are ok
    tests/one_code_block.md
    tests/output_has_blank_lines.md
    tests/setup_only.md
    tests/twentysix_session_blocks.md

exclude_globs =
    # Don't test files matching globs below:
    # Reason- needs command line args.
    doc/setup.md
    doc/setup_doctest.md
    # Reason- contains an already generated test file.
    doc/*_raw.md
    doc/*_py.md
    # Reason- need to register markers to avoid PytestUnknownMarkWarning.
    doc/mark_example.md

output_directory = .gendir-suite-cfg
print = filename, summary
```

This is the equivalent .toml format.

<!--phmdoctest-label generate-toml-->
```toml
# tests/generate.toml
[tool.phmdoctest]
# https://pypi.org/project/phmdoctest
# Writes pytest files generated from Markdown to output_directory.
# Invoke pytest separately to run the generated pytest files.

markdown_globs = [
    # Refer to Python standard library Path.glob(pattern)
    "project.md",
    "doc/*.md",
    "tests/managenamespace.md",
    "tests/one_code_block.md",
    "tests/output_has_blank_lines.md",
    "tests/setup_only.md",
    "tests/twentysix_session_blocks.md",
]
exclude_globs = [
    # Don't test files matching globs below:
    # Reason- needs command line args.
    "doc/setup.md",
    "doc/setup_doctest.md",
    # Reason- contains an already generated test file.
    "doc/*_raw.md",
    "doc/*_py.md",
    # Reason- need to register markers to avoid PytestUnknownMarkWarning.
    "doc/mark_example.md",
]

output_directory = ".gendir-suite-toml"
print = ["filename", "summary"]
```
