#!/usr/bin/env python3
"""Run the unit suite and keep its output, with the command that produced it written at the top.

Why a script rather than a shell one-liner: a log whose origin has to be inferred is a log that gets
misread. That happened here — a run reported `FAILED (errors=1)`, and the word `errors` was read with
`pytest`'s semantics while the command had been `python -m unittest`, where an exception in a test body is
an *error* and an assertion failure is a *failure*. The reading was wrong and the conclusion drawn from it
was wrong. A header removes the inference: it names the runner, the exact command, the interpreter and the
platform, so a log opened months later says what produced it.

The header deliberately records nothing that identifies the machine or its owner beyond the platform name
and the interpreter version — those are what a reader needs to interpret a failure, and they are the same
fields the experiment environment reports.

Usage:
    python scripts/test_log.py            # writes runs/test-last.log and echoes to stdout
    make test-log                         # the same thing
"""

from __future__ import annotations

import datetime
import platform
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LOG = ROOT / "runs" / "test-last.log"
PATTERN = "tests"


def header(command: str, when: str, platform_name: str, python_version: str) -> str:
    """The first lines of every log: what produced it, and when.

    Kept pure so it can be tested without running the suite — the suite is what this script runs, and a
    test that ran it would recurse.
    """
    return (
        f"# command: {command}\n"
        f"# runner: python -m unittest (an exception in a test body is an *error*, "
        f"an assertion failure is a *failure*)\n"
        f"# started: {when}\n"
        f"# platform: {platform_name}  python: {python_version}\n"
        "# this file is ignored by git (runs/*); it exists so a red run leaves a scene\n"
    )


def main(argv: list | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    pattern = argv[0] if argv else PATTERN
    command = f"python -m unittest discover -s {pattern} -v"
    started = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
    text = header(command, started, sys.platform, platform.python_version())
    result = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", pattern, "-v"],
                            cwd=str(ROOT), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
                            encoding="utf-8", errors="replace")
    text += result.stdout or ""
    DEFAULT_LOG.parent.mkdir(parents=True, exist_ok=True)
    DEFAULT_LOG.write_text(text, encoding="utf-8")
    sys.stdout.write(text)
    print(f"\n[test_log] wrote {DEFAULT_LOG.relative_to(ROOT)} ({len(text)} chars), exit {result.returncode}")
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
