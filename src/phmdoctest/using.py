"""Generate test files as specified by configuration file."""
import configparser
from dataclasses import dataclass
from pathlib import Path
import re
from typing import List

try:
    import tomllib  # type: ignore
except ModuleNotFoundError:
    import tomli as tomllib  # type: ignore

import phmdoctest.main
import phmdoctest.tool


def _text_to_words(text: str) -> List[str]:
    """List of words separated by lines or commas from a multi-line string."""
    lines = text.splitlines()
    # chop off "#" + rest of line to remove comments
    comment_free_lines = [re.sub(r"(#.*)$", "", line) for line in lines]
    collapsed_lines = [line.replace(" ", "") for line in comment_free_lines if line]
    words = []
    for line in collapsed_lines:
        words.extend(line.split(","))  # handle comma separated
    return words


@dataclass
class UserConfiguration:
    """Values from [tool.phmdoctest] configuration file section."""

    markdown_globs: List[str]  # files to include
    exclude_globs: List[str]
    output_directory_name: str
    print_options: List[str]


def parse_user_configuration(config_file: Path) -> UserConfiguration:
    """Parse configuration file in one of three configuration file formats."""
    if config_file.name.endswith(".cfg") or config_file.name.endswith(".ini"):
        config = configparser.ConfigParser()
        config.read(config_file)
        cfg_section = "tool.phmdoctest"
        return UserConfiguration(
            markdown_globs=_text_to_words(config[cfg_section]["markdown_globs"]),
            exclude_globs=_text_to_words(config[cfg_section]["exclude_globs"]),
            output_directory_name=config[cfg_section]["output_directory"],
            print_options=_text_to_words(config[cfg_section]["print"]),
        )
    elif config_file.name.endswith(".toml"):
        with open(str(config_file), "rb") as f:
            toml_config = tomllib.load(f)
        toml_section = toml_config["tool"]["phmdoctest"]
        return UserConfiguration(
            markdown_globs=toml_section["markdown_globs"],
            exclude_globs=toml_section["exclude_globs"],
            output_directory_name=toml_section["output_directory"],
            print_options=toml_section["print"],
        )
    else:
        raise ValueError(
            f"File extension must be .cfg, .ini, or .toml, got {config_file.suffix}"
        )


def select_files(config: UserConfiguration, working_directory: Path) -> List[Path]:
    """Look for Markdown files as directed by config. Keep if Python examples."""
    included: List[Path] = []
    for glob in config.markdown_globs:
        included.extend(working_directory.glob(glob))
    skipped: List[Path] = []
    for glob in config.exclude_globs:
        skipped.extend(working_directory.glob(glob))
    tested: List[Path] = []
    for keeper in included:
        if keeper in skipped:
            continue  # Don't append to the tested list.
        python_examples = phmdoctest.tool.detect_python_examples(keeper)
        if python_examples.has_code or python_examples.has_session:
            tested.append(keeper)
    return tested


def generate_using(config_file: Path) -> None:
    """Generate test files as directed by configuration file.

    See doc/configuring.md.
    """
    if not config_file.exists():
        raise FileNotFoundError(str(config_file))
    config = parse_user_configuration(config_file)
    working_directory = Path(".")  # current working directory

    # Assemble list of files to test.
    # Names are relative to the current working directory.
    tested = select_files(config, working_directory)

    p = Path(config.output_directory_name)
    if p.is_absolute():
        gendir = p
    else:
        gendir = working_directory / config.output_directory_name
    phmdoctest.tool.wipe_testfile_directory(gendir)

    file_count = 0
    for markdown in tested:
        testfile = phmdoctest.main.testfile(
            str(markdown), built_from=markdown.as_posix()
        )
        # create the test file name
        outfile_name = "test_" + "__".join(markdown.parts)  # flatten
        outfile = gendir / outfile_name
        outfile = outfile.with_suffix(".py")
        if "filename" in config.print_options:
            print(f"phmdoctest- {markdown.as_posix()} => {outfile.as_posix()}")
        _ = outfile.write_text(testfile, encoding="utf-8")
        file_count += 1
    if "summary" in config.print_options:
        print(
            f"phmdoctest- {config_file.as_posix()} generated {file_count} pytest files"
        )
