"""The threshold curve is the fix for a weakness we admitted: a single `epochs_to_target`
number is a slice of a function. These tests pin the analysis rather than the data."""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.threshold_curve import (
    _winner_label,
    crossing_stability,
    crossing_threshold,
    markdown,
    svg,
    table,
    threshold_grid,
    tied_band,
)


def payload():
    return {
        "task": "synthetic",
        "metric": "epochs_to_target",
        "target_loss": 0.2,
        "trainer": "logistic",
        "results": [
            {
                "name": "fast_then_shallow",
                # reaches 0.2 quickly, but its floor is 0.15
                "loss_curve": [0.6, 0.3, 0.2, 0.18, 0.15],
            },
            {
                "name": "slow_then_deep",
                # slower at first, floor 0.10
                "loss_curve": [0.6, 0.4, 0.3, 0.2, 0.1],
            },
        ],
    }


class ThresholdGridTests(unittest.TestCase):
    def test_grid_spans_best_floor_to_worst_floor(self):
        grid = threshold_grid(payload(), steps=5)
        self.assertEqual(len(grid), 5)
        self.assertAlmostEqual(grid[0], 0.10, places=9)
        self.assertAlmostEqual(grid[-1], 0.15, places=9)
        self.assertEqual(grid, sorted(grid))

    def test_table_marks_thresholds_nobody_reaches(self):
        grid = [0.05, 0.12, 0.25]
        curves = table(payload(), grid)
        # slow_then_deep: floor 0.10, so 0.05 is unreachable, 0.12 arrives at epoch 5 and 0.25 at 4
        self.assertEqual(curves["slow_then_deep"], [None, 5, 4])
        # fast_then_shallow: floor 0.15, so 0.25 arrives at epoch 3 and nothing tighter ever does
        self.assertEqual(curves["fast_then_shallow"], [None, None, 3])

    def test_markdown_names_the_fastest_arm_per_row(self):
        grid = [0.12, 0.25]
        text = markdown(payload(), grid, table(payload(), grid))
        self.assertIn("| 0.1200 |", text)
        self.assertIn("slow_then_deep", text)
        self.assertIn("fast_then_shallow", text)
        self.assertIn("`slow_then_deep`", text)

    def test_markdown_reports_the_pinned_threshold(self):
        grid = threshold_grid(payload(), steps=5)
        text = markdown(payload(), grid, table(payload(), grid))
        self.assertIn("pinned threshold is **0.2**", text)

    def test_svg_has_a_line_per_arm_and_a_target_marker(self):
        grid = [0.12, 0.2, 0.25]
        rendered = svg(payload(), grid, table(payload(), grid))
        self.assertTrue(rendered.startswith("<svg"))
        self.assertIn("stroke-dasharray", rendered)  # the pinned target marker
        self.assertGreaterEqual(rendered.count("<polyline"), 2)
        self.assertIn("epochs to reach the threshold", rendered)

    def test_output_is_deterministic(self):
        grid = [0.12, 0.2, 0.25]
        first = svg(payload(), grid, table(payload(), grid))
        second = svg(payload(), grid, table(payload(), grid))
        self.assertEqual(first, second)


class TieHandlingTests(unittest.TestCase):
    """A tie is not a ranking. Resolving one alphabetically invents a conclusion, which is
    exactly the bug this class was written after."""

    def test_identical_arms_are_reported_as_a_tie_not_a_winner(self):
        self.assertEqual(_winner_label([(5, "adam"), (5, "ademamix")]), "tie: adam, ademamix")
        self.assertEqual(_winner_label([(4, "adam"), (5, "ademamix")]), "adam")
        self.assertEqual(_winner_label([]), "never reached")

    def test_identical_curves_have_no_crossing(self):
        payload = {
            "task": "tie",
            "results": [
                {"name": "a", "loss_curve": [0.6, 0.3, 0.2, 0.1]},
                {"name": "b", "loss_curve": [0.6, 0.3, 0.2, 0.1]},
            ],
        }
        self.assertIsNone(crossing_threshold(payload, "a", "b"))
        self.assertGreater(tied_band(payload, "a", "b"), 0.0)

    def test_a_real_crossing_is_still_found(self):
        """The shape that matters in practice: an arm that converges deepest but slowly, and an
        arm that arrives early at a higher threshold and then overfits (its curve rises again).
        The grid spans [best floor, worst final loss], so the crossing sits inside it."""
        payload = {
            "task": "cross",
            "results": [
                {"name": "deeper_but_slow", "loss_curve": [0.6, 0.5, 0.4, 0.3, 0.2]},
                {"name": "early_then_overfits", "loss_curve": [0.6, 0.25, 0.4, 0.45, 0.5]},
            ],
        }
        crossing = crossing_threshold(payload, "deeper_but_slow", "early_then_overfits")
        self.assertIsNotNone(crossing)
        self.assertGreater(crossing, 0.24)
        self.assertLess(crossing, 0.26)

    def test_crossing_stability_counts_seeds_with_and_without_a_crossing(self):
        identical = {
            "task": "tie",
            "results": [
                {"name": "a", "loss_curve": [0.6, 0.3, 0.2, 0.1]},
                {"name": "b", "loss_curve": [0.6, 0.3, 0.2, 0.1]},
            ],
        }
        crossing = {
            "task": "cross",
            "results": [
                {"name": "a", "loss_curve": [0.6, 0.5, 0.4, 0.3, 0.2]},
                {"name": "b", "loss_curve": [0.6, 0.25, 0.4, 0.45, 0.5]},
            ],
        }
        result = crossing_stability([identical, crossing], "a", "b", pinned=0.2, steps=20)
        self.assertEqual(result["seeds"], 2)
        self.assertEqual(result["crossings_found"], 1)
        self.assertEqual(len(result["crossing_values"]), 2)


if __name__ == "__main__":
    unittest.main()
