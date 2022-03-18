"""Check main.generate_using() printing. Check configuring.md."""
import configparser
from pathlib import Path

import pytest

import phmdoctest.main
import phmdoctest.tool

# Fenced code blocks that have the phmdoctest-label directive.
labeled = phmdoctest.tool.FCBChooser("doc/configuring.md")


def test_bogus_configs():
    """Call generate_using() with non-existent configuration file."""
    with pytest.raises(FileNotFoundError):
        phmdoctest.main.generate_using(config_file=Path("bogus.toml"))
    with pytest.raises(ValueError):
        # Can't generate from a .py file.
        phmdoctest.main.generate_using(config_file=Path("setup.py"))


@pytest.fixture()
def line_sorted_checker(checker):
    """Return Callable(str, str) that sorts each arg's lines first."""

    def sorted_checker(a: str, b: str):
        """Split each string into lines, sort them, reconstitute string, then compare."""
        a_lines = a.splitlines()
        a_sorted = sorted(a_lines)
        a_string = "\n".join(a_sorted)
        b_lines = b.splitlines()
        b_sorted = sorted(b_lines)
        b_string = "\n".join(b_sorted)
        checker(a_string, b_string)

    return sorted_checker


def test_using_toml_config(line_sorted_checker, capsys):
    """Call generate_using() with .toml configuration file."""
    want = """
phmdoctest- project.md => .gendir-suite-toml/test_project.py
phmdoctest- doc/directive1.md => .gendir-suite-toml/test_doc__directive1.py
phmdoctest- doc/directive2.md => .gendir-suite-toml/test_doc__directive2.py
phmdoctest- doc/directive3.md => .gendir-suite-toml/test_doc__directive3.py
phmdoctest- doc/example1.md => .gendir-suite-toml/test_doc__example1.py
phmdoctest- doc/example2.md => .gendir-suite-toml/test_doc__example2.py
phmdoctest- doc/inline_example.md => .gendir-suite-toml/test_doc__inline_example.py
phmdoctest- tests/managenamespace.md => .gendir-suite-toml/test_tests__managenamespace.py
phmdoctest- tests/one_code_block.md => .gendir-suite-toml/test_tests__one_code_block.py
phmdoctest- tests/output_has_blank_lines.md => .gendir-suite-toml/test_tests__output_has_blank_lines.py
phmdoctest- tests/setup_only.md => .gendir-suite-toml/test_tests__setup_only.py
phmdoctest- tests/twentysix_session_blocks.md => .gendir-suite-toml/test_tests__twentysix_session_blocks.py
phmdoctest- tests/generate.toml generated 12 pytest files
"""
    phmdoctest.main.generate_using(config_file=Path("tests/generate.toml"))
    drop_newline = want.lstrip()
    line_sorted_checker(drop_newline, capsys.readouterr().out)


def test_using_cfg_config(line_sorted_checker, capsys):
    """Call generate_using() with .cfg configuration file."""
    want = """
phmdoctest- project.md => .gendir-suite-cfg/test_project.py
phmdoctest- doc/directive1.md => .gendir-suite-cfg/test_doc__directive1.py
phmdoctest- doc/directive2.md => .gendir-suite-cfg/test_doc__directive2.py
phmdoctest- doc/directive3.md => .gendir-suite-cfg/test_doc__directive3.py
phmdoctest- doc/example1.md => .gendir-suite-cfg/test_doc__example1.py
phmdoctest- doc/example2.md => .gendir-suite-cfg/test_doc__example2.py
phmdoctest- doc/inline_example.md => .gendir-suite-cfg/test_doc__inline_example.py
phmdoctest- tests/managenamespace.md => .gendir-suite-cfg/test_tests__managenamespace.py
phmdoctest- tests/one_code_block.md => .gendir-suite-cfg/test_tests__one_code_block.py
phmdoctest- tests/output_has_blank_lines.md => .gendir-suite-cfg/test_tests__output_has_blank_lines.py
phmdoctest- tests/setup_only.md => .gendir-suite-cfg/test_tests__setup_only.py
phmdoctest- tests/twentysix_session_blocks.md => .gendir-suite-cfg/test_tests__twentysix_session_blocks.py
phmdoctest- tests/generate.cfg generated 12 pytest files
"""
    phmdoctest.main.generate_using(config_file=Path("tests/generate.cfg"))
    drop_newline = want.lstrip()
    line_sorted_checker(drop_newline, capsys.readouterr().out)


def test_using_ini_config(checker, capsys):
    """Run with no printing."""
    phmdoctest.main.generate_using(config_file=Path("tests/generate_quietly.ini"))
    assert len(capsys.readouterr().out) == 0


def test_using_summary_only(checker, capsys):
    """Run with the print summary option only."""
    phmdoctest.main.generate_using(config_file=Path("tests/generate_summary.toml"))
    summary = "phmdoctest- tests/generate_summary.toml generated 12 pytest files"
    checker(summary, capsys.readouterr().out)


def test_invocations_cfg():
    """Output directory same in configuring.md example and setup.cfg."""
    invocations = labeled.contents(label="invocations")
    setup = Path("setup.cfg").read_text(encoding="utf-8")
    gendir = ".gendir-cfg"
    assert gendir in invocations
    assert f"output_directory = {gendir}" in setup


def test_invocations_ini():
    """Output directory same in configuring.md example and tox.ini."""
    invocations = labeled.contents(label="invocations")
    tox = Path("tox.ini").read_text(encoding="utf-8")
    gendir = ".gendir-ini"
    assert gendir in invocations
    assert f"output_directory = {gendir}" in tox


def test_invocations_toml():
    """Output directory same in configuring.md example and pyproject.toml."""
    invocations = labeled.contents(label="invocations")
    pyproject = Path("pyproject.toml").read_text(encoding="utf-8")
    gendir = ".gendir-toml"
    assert gendir in invocations
    assert f'output_directory = "{gendir}"' in pyproject


def test_cfg_example(checker):
    """Check the example .cfg file fenced code block in configuring.md."""
    want = labeled.contents(label="generate-cfg")
    got = Path("tests/generate.cfg").read_text(encoding="utf-8")
    checker(want, got)


def test_toml_example(checker):
    """Check the example .toml file fenced code block in configuring.md."""
    want = labeled.contents(label="generate-toml")
    got = Path("tests/generate.toml").read_text(encoding="utf-8")
    checker(want, got)


def test_tox_usage(checker):
    """Check setup.cfg and tox.ini [phmdoctest.tool] sections are mostly the same."""
    setup_config = configparser.ConfigParser()
    setup_config.read("setup.cfg")
    setup_tool = setup_config["tool.phmdoctest"]

    tox_config = configparser.ConfigParser()
    tox_config.read("tox.ini")
    tox_tool = tox_config["tool.phmdoctest"]

    assert setup_tool["markdown_globs"] == tox_tool["markdown_globs"]
    assert setup_tool["exclude_globs"] == tox_tool["exclude_globs"]
    assert setup_tool["print"] == tox_tool["print"]
    assert ".gendir-cfg" in setup_tool["output_directory"]
    assert ".gendir-ini" in tox_tool["output_directory"]


def test_absolute_outdir(tmp_path):
    """Try absolute path in config file output_directory key."""
    # Create destination directory.
    tempdir = tmp_path / "outdir"
    tempdir.mkdir(mode=0o700)
    assert tempdir.exists()
    assert tempdir.is_absolute()
    assert len(list(tempdir.glob("**/*.*"))) == 0, "Must be empty."
    # Create a new configuration file with an absolute output_directory.
    # We are cheating a little by writing it to the same directory
    # where the test files will be saved.
    config_file = tempdir / Path("rewritten.cfg")
    contents = Path("tests/generate.cfg").read_text(encoding="utf-8")
    contents = contents.replace(".gendir-suite-cfg", str(tempdir))
    contents = contents.replace("print = filename, summary", "print = summary")
    _ = config_file.write_text(contents, encoding="utf-8")
    phmdoctest.main.generate_using(config_file=config_file)
    assert config_file.exists(), "In output_directory and didn't get wiped."
    assert (Path(tempdir) / "test_project.py").exists()
    assert (Path(tempdir) / "test_doc__directive1.py").exists()
    assert (Path(tempdir) / "test_doc__directive2.py").exists()
    assert (Path(tempdir) / "test_doc__directive3.py").exists()
    assert (Path(tempdir) / "test_doc__example1.py").exists()
    assert (Path(tempdir) / "test_doc__example2.py").exists()
    assert (Path(tempdir) / "test_doc__inline_example.py").exists()
    assert (Path(tempdir) / "test_tests__managenamespace.py").exists()
    assert (Path(tempdir) / "test_tests__one_code_block.py").exists()
    assert (Path(tempdir) / "test_tests__output_has_blank_lines.py").exists()
    assert (Path(tempdir) / "test_tests__setup_only.py").exists()
    assert (Path(tempdir) / "test_tests__twentysix_session_blocks.py").exists()
    assert len(list(tempdir.glob("**/*.*"))) == 13, "12 test files and .cfg file."
