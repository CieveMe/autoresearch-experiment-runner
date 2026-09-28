"""The figures have to be valid, deterministic and inside their own canvas.

An SVG that silently draws outside the viewBox looks fine in a terminal and wrong in a paper, so the
geometry is checked numerically rather than by eye: every circle and every line segment must sit
inside the declared width and height, and regenerating a figure must produce identical bytes.
"""

import sys
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts import figures


def _numbers(root: ET.Element, attribute: str):
    for element in root.iter():
        value = element.get(attribute)
        if value is not None:
            try:
                yield float(value)
            except ValueError:
                continue


class FigureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = figures.build_report(ROOT / "runs", "test_loss", None, None, 0.05)
        cls.schedule_free = figures.forest_rows(cls.report, "schedule-free")
        cls.ademamix = figures.forest_rows(cls.report, "AdEMAMix")
        cls.stability = figures.stability_table(ROOT / "runs")

    def _check_inside(self, svg: str):
        root = ET.fromstring(svg)
        width = float(root.get("width"))
        height = float(root.get("height"))
        self.assertGreater(width, 0)
        self.assertGreater(height, 0)
        for value in _numbers(root, "x"):
            self.assertGreaterEqual(value, -1.0)
            self.assertLessEqual(value, width + 1.0)
        for value in _numbers(root, "cx"):
            self.assertLessEqual(value, width + 1.0)
        for value in _numbers(root, "y"):
            self.assertGreaterEqual(value, -1.0)
            self.assertLessEqual(value, height + 1.0)
        for value in _numbers(root, "cy"):
            self.assertLessEqual(value, height + 1.0)
        return root

    def test_forest_covers_every_suite_in_the_family(self):
        self.assertEqual(len(self.schedule_free), 10)
        self.assertEqual(len(self.ademamix), 11)
        svg = figures.forest_svg(self.schedule_free, "t", "s")
        root = self._check_inside(svg)
        labels = [element.text or "" for element in root.iter() if element.tag.endswith("text")]
        for row in self.schedule_free:
            self.assertTrue(any(row["suite"] in label for label in labels), row["suite"])

    def test_the_established_case_is_marked_and_named(self):
        svg = figures.forest_svg(self.schedule_free, "t", "s")
        row = next(item for item in self.schedule_free if item["suite"] == "capacity-h16x16")
        self.assertLessEqual(row["adjusted_p"], 0.05)
        self.assertIn(f'adjusted p = {row["adjusted_p"]:.3f}', svg)
        self.assertIn(figures.ACCENT, svg)

    def test_stability_scatter_has_one_point_per_suite(self):
        svg = figures.stability_svg(self.stability)
        root = self._check_inside(svg)
        # Sixteen suites pin a target; `main` does not, and is deliberately not plotted.
        self.assertEqual(len(self.stability), 16)
        self.assertNotIn("main", [row["suite"] for row in self.stability])
        circles = [element for element in root.iter() if element.tag.endswith("circle")]
        self.assertEqual(len(circles), len(self.stability))

    def test_the_noise_statistics_are_reproducible_and_disagree_with_the_old_table(self):
        """Pin the two counterexamples that broke the sigma/reproducibility correlation.

        `optimizers-mlp` has almost the lowest noise in the corpus and five different winners;
        `activation-relu` has higher noise and a single winner in all ten seeds. A correlation that
        both of those violate is not a correlation, and the hand-assembled column in §5.13 said
        otherwise.
        """
        by_suite = {row["suite"]: row for row in self.stability}
        mlp = by_suite["optimizers-mlp"]
        self.assertAlmostEqual(mlp["sigma_best"], 0.02019, places=4)
        self.assertEqual(mlp["winners"], 5)
        relu = by_suite["activation-relu"]
        self.assertAlmostEqual(relu["sigma_best"], 0.02172, places=4)
        self.assertEqual(relu["winners"], 1)
        self.assertEqual(relu["modal_winner"], "adamw_cosine")
        self.assertEqual(relu["modal_winner_count"], 10)
        # The suite the old table quoted 0.0646 for: that value belongs to adamw_constant, not to the
        # suite's best arm, which is what the column claimed.
        h8x8 = by_suite["capacity-h8x8"]
        self.assertAlmostEqual(h8x8["sigma_best"], 0.02271, places=4)
        self.assertEqual(h8x8["best"], "adagrad")

    def test_empty_input_still_produces_a_valid_figure(self):
        svg = figures.forest_svg([], "t", "s")
        self.assertIn("no comparisons available", svg)
        self._check_inside(svg)

    def test_generation_is_deterministic(self):
        first = figures.forest_svg(self.schedule_free, "t", "s")
        second = figures.forest_svg(self.schedule_free, "t", "s")
        self.assertEqual(first, second)
        self.assertEqual(figures.stability_svg(self.stability), figures.stability_svg(self.stability))

    def test_committed_figures_match_the_generator(self):
        """A committed figure that no longer matches the data is worse than no figure."""
        directory = ROOT / "runs" / "figures"
        if not directory.exists():  # pragma: no cover - figures are committed
            self.skipTest("figures not generated in this checkout")
        expected = {
            "forest-schedule-free.svg": figures.forest_svg(
                self.schedule_free, "Schedule-Free AdamW vs a tuned cosine: paired differences",
                "Ten-seed paired comparison per suite; negative favours Schedule-Free"),
            "forest-ademamix.svg": figures.forest_svg(
                self.ademamix, "AdEMAMix vs AdamW at matched settings: paired differences",
                "Ten-seed paired comparison per suite; negative favours AdEMAMix"),
            "noise-vs-stability.svg": figures.stability_svg(self.stability),
        }
        for name, content in expected.items():
            self.assertEqual((directory / name).read_text(encoding="utf-8"), content, name)


if __name__ == "__main__":
    unittest.main()
