"""This repository is public, so the things that identify the machine it was produced on must not be in it.

The check was performed by hand more than once — `rg` over the docs for drive-letter paths, personal email
domains and a phone-number shape — and every time it came back clean. A check that both sides re-run by
memory is the thing this repository's own defect family is about (see `docs/defect-family.md`, the footnote
on "which copy is in play"), so it is now a test.

The patterns are deliberately **generic**: they describe the classes of string that must not leak (a local
absolute path, a personal mailbox, a mainland-China mobile number, a private key) rather than naming any
specific value, because writing the specific value here to forbid it would defeat the purpose. Names that
cannot be expressed generically, such as the project directory this repository was developed in, stay a
manual check — there is no way to assert them in a public file without putting them in a public file.
"""

import re
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Files and directories that are not part of the repository's content.
SKIP_DIRECTORIES = {".git", "__pycache__", ".npm-cache", "node_modules", ".venv", "venv"}
SKIP_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".pdf", ".zip", ".gz", ".whl", ".pyc", ".svg"}

PATTERNS = {
    # A drive letter, not any letter before a colon: a string literal holding an escaped newline puts a
    # letter, a colon and a backslash in a row, and a first version of this pattern read that trailing
    # letter as a drive letter. The lookbehind keeps the match to a letter that starts a token — which
    # also means this file must not spell the offending three characters out, not even here.
    "a local absolute path": re.compile(r"(?<![A-Za-z0-9])[A-Za-z]:\\"),
    "a personal mailbox": re.compile(r"[\w.+-]+@(?:gmail|163|126|qq|outlook|hotmail|yahoo)\.[A-Za-z]{2,}"),
    "a mainland-China mobile number": re.compile(r"(?<!\d)1[3-9]\d{9}(?!\d)"),
    "a private key": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
}

# `runs/` holds committed experiment output, and one of its files legitimately reads an environment
# variable to redact it; scanning is still correct, but the token shapes below are what a leak would look
# like rather than a variable name.


def iter_text_files():
    """The files this repository would publish.

    With a `.git` directory present the list is `git ls-files`, which is exactly "what would be
    committed" — local scratch output under `runs/` is ignored by git and is therefore not part of the
    public tree, so failing on it would be wrong. In a copy without `.git` (the container image, the
    scorer's tree) the whole copy is scanned instead, with the same skip lists.
    """
    if (ROOT / ".git").exists():
        result = subprocess.run(["git", "ls-files", "-z"], cwd=str(ROOT), stdout=subprocess.PIPE,
                                stderr=subprocess.DEVNULL)
        if result.returncode == 0:
            candidates = [ROOT / name for name in result.stdout.decode("utf-8", "replace").split("\0") if name]
        else:
            # Fail closed: if the tracked-file list cannot be read, scan everything rather than nothing.
            # A guard that silently checks no files is the failure mode this file exists to avoid.
            candidates = sorted(ROOT.rglob("*"))
    else:
        candidates = sorted(ROOT.rglob("*"))
    for path in candidates:
        try:
            # Files can appear and disappear while a scan runs — `__pycache__` entries are rewritten by
            # the very suite that calls this — so every filesystem step is inside the guard. One run of
            # this suite failed once, without a reproducible cause, before this; the scan must not be the
            # thing that decides whether a run goes green.
            if not path.is_file():
                continue
            if any(part in SKIP_DIRECTORIES for part in path.parts):
                continue
            if path.suffix.lower() in SKIP_SUFFIXES:
                continue
            if path.stat().st_size > 8 * 1024 * 1024:
                continue
            yield path, path.read_text(encoding="utf-8", errors="replace")
        except OSError:  # pragma: no cover - unreadable or vanished file, not a leak
            continue


def scan_text(text: str, name: str = "text") -> list:
    """Return one string per identifying match: `<name>:<line>: <what it is>`."""
    offenders = []
    for label, pattern in PATTERNS.items():
        for match in pattern.finditer(text):
            line = text.count("\n", 0, match.start()) + 1
            offenders.append(f"{name}:{line}: {label}")
    return offenders


class PrivacyHygieneTests(unittest.TestCase):
    def test_no_identifying_strings_in_the_tree(self):
        offenders = []
        for path, text in iter_text_files():
            offenders.extend(scan_text(text, str(path.relative_to(ROOT))))
        self.assertEqual(offenders, [], "the public tree carries identifying strings:\n" + "\n".join(offenders))

    def test_the_check_can_fail(self):
        """A guard that cannot fail is the failure mode this repository keeps finding (case 6a).

        The negative control goes through the same `scan_text` the real check uses, so it exercises the
        detection path and not only the regexes: a first version of this file called its sample check
        against the patterns directly while the scan itself was never proven able to report anything.
        """
        samples = {
            "a local absolute path": "see " + "D:" + "\\somewhere\\file.txt",
            "a personal mailbox": "write to someone" + "@" + "gmail.com",
            "a mainland-China mobile number": "call 1" + "3812345678",
            "a private key": "-----BEGIN " + "RSA PRIVATE KEY-----",
        }
        for label, sample in samples.items():
            with self.subTest(label=label):
                reported = scan_text(sample, "sample.txt")
                self.assertTrue(any(label in entry for entry in reported), reported)

    def test_a_colon_before_an_escaped_newline_is_not_a_path(self):
        """The false positive the first version had, described without writing the pattern itself.

        `"...tests:` followed by an escaped newline contains a letter, a colon and a backslash in a row,
        and the first pattern read that as a drive-letter path. Naming the offending three characters here
        literally would make this file trip its own check, which is a small lesson in itself.
        """
        innocent = 'raise AssertionError("the scored copy cannot run tests:\\n" + tail)'
        self.assertEqual(scan_text(innocent, "sample.py"), [])


if __name__ == "__main__":
    unittest.main()
