"""Rewrite code as directed by inline commands in comments."""
import re
from typing import List, Tuple


def starts_with_comment(line: str) -> bool:
    """True if string starts with zero or more whitespace then # char."""
    return re.match(pattern=r"^\s*#", string=line) is not None


def num_newlines_at_end(code: str) -> int:
    """Return the number of consecutive newlines at the end of the string."""
    m = re.search(pattern=r"(\n*)$", string=code)
    consecutive = 0
    if m:
        consecutive = len(m.group(1))
    return consecutive


def num_indented(line: str) -> int:
    """Number of spaces the string is indented if indented with only spaces."""
    m = re.match(pattern=r"^(\s*)\S", string=line)
    indentation = 0
    if m:
        indentation = len(m.group(1))
    return indentation


def isblank(line: str) -> bool:
    """True if the entire string is whitespace."""
    m = re.match(pattern=r"^\s*$", string=line)
    return m is not None


def is_empty_comment(line: str) -> bool:
    """True if the string is just one # and the rest whitespace."""
    despaced = re.sub(r"\s*", "", string=line)
    return despaced == "#"


def has_inline_omit(line: str) -> bool:
    """True if line ends with a omit command."""
    return line.endswith("phmdoctest:omit")


def has_inline_pass(line: str) -> bool:
    """True if line ends with a pass command."""
    return line.endswith("phmdoctest:pass")


def prepend_pass_statement(line: str) -> str:
    """Prepend pass at indent level and comment out the line."""
    colno = num_indented(line)
    right_side = line[colno:]
    indent = " " * colno
    return indent + "pass  # " + right_side


class BlockCommenter:
    """Accumulate and comment out a block of lines with # at column_number."""

    def __init__(self, column_index: int):
        """Prepare to comment out lines at column_index indent."""
        self.colno = column_index
        self.block = []  # type: List[str]

    def add(self, line: str) -> None:
        """Add line to list of lines to be commented out."""
        self.block.append(line)

    def comment_out_line(self, line: str) -> str:
        """Comment out one line with # at the colno."""
        if len(line) > self.colno:
            right_side = " " + line[self.colno :]
        else:
            right_side = ""
        indent = " " * self.colno
        return indent + "#" + right_side

    def comment_out(self) -> List[str]:
        """Return list of lines with commenting applied at column number."""
        commented = [self.comment_out_line(line) for line in self.block]
        # Replace commented out blank lines at the end with empty lines.
        backwards = reversed(commented)
        fixed = []
        keep_checking = True
        for line in backwards:
            if keep_checking:
                if is_empty_comment(line):
                    fixed.append("")
                else:
                    keep_checking = False
                    fixed.append(line)
            else:
                fixed.append(line)
        return list(reversed(fixed))


def apply_inline_commands(code: str) -> Tuple[str, int]:
    """Rewrite code as directed by #phmdoctest:omit and other commands.

    Return a tuple: Modified (or not) code, number of commented out sections.
    """
    rewritten = []
    num_commented_out_sections = 0
    commenter = None
    lines = code.splitlines()
    while lines:
        line = lines.pop(0)
        if commenter is None:
            # Looking for inline commands.
            if starts_with_comment(line):
                rewritten.append(line)

            elif has_inline_pass(line):
                rewritten.append(prepend_pass_statement(line))
                num_commented_out_sections += 1

            elif has_inline_omit(line):
                commenter = BlockCommenter(num_indented(line))
                commenter.add(line)
            else:
                rewritten.append(line)
        else:
            # A blank line has no indent level.
            # It may have some stray spaces.  These are removed.
            if isblank(line):
                commenter.add("")

            # Check if the line is indented the same or less than the omit
            # command's statement.
            elif num_indented(line) <= commenter.colno:
                # If so this line signals the end of the
                # lines to be commented out.
                # Put this line back in the lines to do
                num_commented_out_sections += 1
                rewritten.extend(commenter.comment_out())
                commenter = None
                lines.insert(0, line)
            else:
                # Collect this line to comment out later.
                commenter.add(line)

    if commenter is not None:
        # End of input reached while collecting lines to comment out.
        num_commented_out_sections += 1
        rewritten.extend(commenter.comment_out())

    # Restore a run of one or more new lines that may be at the end
    # of the caller's code string.
    rewritten.extend([""] * num_newlines_at_end(code))
    rewritten_str = "\n".join(rewritten)
    if num_commented_out_sections:
        return rewritten_str, num_commented_out_sections
    else:
        return code, num_commented_out_sections
