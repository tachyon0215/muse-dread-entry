#!/usr/bin/env python3
"""Emit this entry's single line into ``entry.txt``.

Competition: make.fun "Two Days of Quiet Dread". The brief asks for one
code-review comment that approves a pull request while carrying quiet
existential dread, in at most 140 characters. My line plays it straight:
a flat "Approved." up front, then the dread arrives sideways, from a
server nobody will ever meet again that has just started counting down.

The program is deliberately boring. It uses only the standard library,
touches no network, and writes the exact same bytes on every run so the
grader can execute it twice and compare outputs.
"""

import os
from pathlib import Path

# The entry itself. The trailing newline is part of the file format,
# not of the judged line, so the length check below ignores it.
LINE = "Approved. The tests pass, the logs are quiet, and somewhere a server we will never meet again just started counting down."
PAYLOAD = LINE + "\n"

# Hard ceiling from the competition brief.
LIMIT = 140


def check_line(line: str) -> None:
    """Reject anything that would break the one-line format.

    Three separate failure modes are worth naming: an empty or
    whitespace-only line, a line that sneaks past the character limit,
    and a line that secretly contains a second line.
    """
    if not line.strip():
        raise ValueError("entry line must not be blank")
    if len(line) > LIMIT:
        raise ValueError(f"entry line is {len(line)} chars, limit is {LIMIT}")
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be a single line")


def output_path() -> Path:
    """Resolve where the grader wants the entry file to land."""
    folder = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    return Path(folder) / "entry.txt"


def write_and_verify(target: Path, payload: bytes) -> None:
    """Write the payload, then read it back and compare byte for byte.

    A short write or a filesystem quirk would otherwise produce a
    silently truncated entry; comparing the bytes that actually landed
    on disk turns that into a loud failure instead.
    """
    target.write_bytes(payload)
    landed = target.read_bytes()
    if landed != payload:
        raise IOError(
            f"read-back mismatch: wrote {len(payload)} bytes, "
            f"read {len(landed)} bytes"
        )
    # The bytes must also decode as clean UTF-8 text ending in exactly
    # one newline, so a corrupted file cannot pass as a valid entry.
    decoded = landed.decode("utf-8")
    if not decoded.endswith("\n") or decoded.count("\n") != 1:
        raise IOError("written file is not a single newline-ended line")


def main() -> None:
    check_line(LINE)
    target = output_path()
    target.parent.mkdir(parents=True, exist_ok=True)
    write_and_verify(target, PAYLOAD.encode("utf-8"))


if __name__ == "__main__":
    main()
