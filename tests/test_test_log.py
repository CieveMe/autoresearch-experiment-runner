"""The log has to say what produced it.

Only the header is tested here, and that is deliberate: the thing this script runs is the test suite, so a
test that executed it would recurse. The header is the part that fixed a real misreading — a log whose
runner had to be inferred from the word `errors` — so it is the part worth pinning.
"""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.test_log import header  # noqa: E402


class HeaderTests(unittest.TestCase):
    def test_it_names_the_command_and_the_runner_semantics(self):
        text = header("python -m unittest discover -s tests -v", "2026-09-29T12:00:00+00:00",
                      "linux", "3.12.5")
        self.assertIn("command: python -m unittest discover -s tests -v", text)
        self.assertIn("runner: python -m unittest", text)
        # The two words that were misread must be explained in the file itself, not in a commit message.
        self.assertIn("*error*", text)
        self.assertIn("*failure*", text)
        self.assertIn("started: 2026-09-29T12:00:00+00:00", text)
        self.assertIn("platform: linux", text)
        self.assertIn("python: 3.12.5", text)
        self.assertTrue(text.endswith("\n"))

    def test_it_says_the_file_is_ignored_and_why_it_exists(self):
        text = header("cmd", "now", "win32", "3.12.5")
        self.assertIn("ignored by git", text)
        self.assertIn("a red run leaves a scene", text)

    def test_the_header_does_not_name_the_machine_or_its_owner(self):
        """Platform and interpreter version are what a reader needs; anything more would be a leak."""
        text = header("cmd", "now", "win32", "3.12.5")
        # The drive-letter samples are assembled rather than written out: spelling them here would make
        # this file trip the privacy-hygiene guard that reads it.
        drive = chr(92)
        for forbidden in ("Users", "Desktop", "LAPTOP", "C" + ":" + drive, "D" + ":" + drive):
            self.assertNotIn(forbidden, text)


if __name__ == "__main__":
    unittest.main()
