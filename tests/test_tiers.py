"""Tiering may save local time; it may never hide coverage.

These tests pin the three conditions that make the split acceptable: `core` is a strict
subset of `full`, the label of a partial run always names what it skipped, and the scorer's
score line carries the tier it came from.
"""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.repro import SUITES, TIERS, suites_for_tier, tier_label


class TierTests(unittest.TestCase):
    def test_core_is_a_strict_subset_of_full(self):
        core = set(suites_for_tier("core"))
        full = set(suites_for_tier("full"))
        self.assertTrue(core < full, "core must be a strict subset of full")
        self.assertEqual(full, set(SUITES))

    def test_the_difference_is_exactly_the_capacity_suites(self):
        skipped = set(suites_for_tier("full")) - set(suites_for_tier("core"))
        expected = {name for name, suite in SUITES.items() if suite.get("tier") == "capacity"}
        self.assertEqual(skipped, expected)
        self.assertTrue(skipped, "the tier split is pointless unless something is skipped")

    def test_a_partial_run_always_names_what_it_skipped(self):
        core = suites_for_tier("core")
        label = tier_label("core", core)
        self.assertIn("tier=core", label)
        self.assertIn("NOT run", label)
        for name in set(suites_for_tier("full")) - set(core):
            self.assertIn(name, label)

    def test_a_full_run_says_so(self):
        label = tier_label("full", suites_for_tier("full"))
        self.assertIn("tier=full", label)
        self.assertIn("all suites", label)

    def test_unknown_tier_is_rejected(self):
        self.assertEqual(TIERS, ("core", "full"))
        with self.assertRaises(ValueError):
            suites_for_tier("quick")

    def test_scorer_score_line_mentions_the_tier(self):
        from scripts.score_task import _score_directory  # noqa: F401  (import check only)

        source = (ROOT / "scripts" / "score_task.py").read_text(encoding="utf-8")
        self.assertIn("tier_label", source)
        self.assertIn("submission score:", source)


if __name__ == "__main__":
    unittest.main()
