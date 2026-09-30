"""Release documents make claims, so the claims get checked.

`docs/release-notes-vX.Y.Z.published.md` is the body that gets published verbatim with the tag, and its
*name* asserts that the version is out. A prepared body can sit in the tree for a while under the queue's
deferral (`docs/release-corrections-pending.md`), and during that time the name would be false — which is
the class of problem this repository keeps finding: a claim that is true of one moment and reads as if it
were true of every moment.

The rule is one-directional on purpose. A body whose tag does not exist yet must say so in its text; a body
whose tag does exist may keep that sentence, because it is stamped with the date it was written. That way
publishing a release never requires editing its body afterwards, which hard rule 3 forbids.
"""

import re
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

BODY_NAME = re.compile(r"^release-notes-(v\d+\.\d+\.\d+)\.published\.md$")
STATUS_MARKER = "not yet tagged"


def version_of(name: str):
    match = BODY_NAME.match(name)
    return match.group(1) if match else None


def unmarked_bodies(texts, tagged):
    """Bodies whose name claims a release, whose tag does not exist, and which do not say so.

    Kept as a pure function so the negative control can feed it a crippled input instead of relying on the
    repository being wrong on purpose.
    """
    return sorted(name for name, text in texts.items()
                  if version_of(name) and version_of(name) not in tagged
                  and STATUS_MARKER not in text.lower())


class ReleaseBodyStatusTests(unittest.TestCase):
    def test_a_body_whose_tag_does_not_exist_says_so(self):
        texts = {path.name: path.read_text(encoding="utf-8")
                 for path in sorted((ROOT / "docs").glob("release-notes-v*.published.md"))}
        self.assertTrue(texts, "no release bodies found: that would make this check vacuous")
        tagged = self._tags()
        if tagged is None:
            self.skipTest("no readable git metadata here, so the tag set cannot be compared")
        self.assertEqual(
            unmarked_bodies(texts, tagged), [],
            "these bodies have no tag yet and do not say so; add the sentence 'prepared, not yet tagged' "
            "with the date it was written, so the file name cannot be read as evidence that the version "
            "was released:\n",
        )

    def test_the_check_reports_an_unmarked_body(self):
        """Negative control: without the sentence the same function has to name the file."""
        unmarked = {"release-notes-v9.9.9.published.md": "this body claims a release and says nothing."}
        self.assertEqual(unmarked_bodies(unmarked, set()), list(unmarked))
        marked = {name: "Status: prepared, not yet tagged (2026-09-30)." for name in unmarked}
        self.assertEqual(unmarked_bodies(marked, set()), [])
        self.assertEqual(unmarked_bodies(unmarked, {"v9.9.9"}), [])

    @staticmethod
    def _tags():
        if not (ROOT / ".git").exists():
            return None
        result = subprocess.run(["git", "tag", "--list"], cwd=str(ROOT), stdout=subprocess.PIPE,
                                stderr=subprocess.DEVNULL)
        if result.returncode != 0:
            return None
        return set(result.stdout.decode("utf-8", "replace").split())


if __name__ == "__main__":
    unittest.main()
