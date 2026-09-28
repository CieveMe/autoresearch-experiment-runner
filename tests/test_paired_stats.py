"""The paired statistics have to be right, and the sentence they produce has to be honest.

Two kinds of check here. The first is arithmetic on hand-computable cases: with ten pairs the sign
test and the Wilcoxon signed-rank test are exact by enumeration, so their answers can be written
down independently (`2 * 2^-10` when every difference has the same sign, 1 when they cancel
exactly). The second is the wording rule: a test that fails to reject must not be reported as
evidence that the two arms are the same, because with ten seeds the power to detect anything but a
large effect is low.
"""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts import paired_stats as stats


class ExactTests(unittest.TestCase):
    def test_sign_test_all_one_way(self):
        result = stats.sign_test([0.01 * (index + 1) for index in range(10)])
        self.assertEqual(result["n_used"], 10)
        self.assertAlmostEqual(result["p_value"], 2 / 2 ** 10, places=12)

    def test_sign_test_cancels_exactly(self):
        differences = [0.1] * 5 + [-0.2] * 5
        self.assertAlmostEqual(stats.sign_test(differences)["p_value"], 1.0, places=12)

    def test_sign_test_with_no_information(self):
        result = stats.sign_test([0.0] * 10)
        self.assertFalse(result["informative"])
        self.assertEqual(result["p_value"], 1.0)

    def test_wilcoxon_all_one_way(self):
        result = stats.wilcoxon_signed_rank([0.01 * (index + 1) for index in range(10)])
        self.assertTrue(result["exact"])
        self.assertAlmostEqual(result["w_plus"], 55.0, places=12)
        self.assertAlmostEqual(result["p_value"], 2 / 2 ** 10, places=12)

    def test_wilcoxon_is_symmetric_under_a_sign_flip(self):
        differences = [0.02, -0.05, 0.11, 0.13, -0.2, 0.003, 0.31, -0.07, 0.05, 0.09]
        forward = stats.wilcoxon_signed_rank(differences)["p_value"]
        backward = stats.wilcoxon_signed_rank([-value for value in differences])["p_value"]
        self.assertEqual(forward, backward)

    def test_wilcoxon_with_tied_magnitudes_has_no_crossing(self):
        """Ties get average ranks; without that the test would depend on the order of equal values."""
        differences = [0.1, 0.1, -0.1, -0.1, 0.2, -0.2, 0.3, -0.3, 0.4, -0.4]
        shuffled = list(reversed(differences))
        self.assertEqual(
            stats.wilcoxon_signed_rank(differences)["p_value"],
            stats.wilcoxon_signed_rank(shuffled)["p_value"],
        )
        self.assertAlmostEqual(stats.wilcoxon_signed_rank(differences)["p_value"], 1.0, places=12)

    def test_holm_matches_the_worked_example(self):
        self.assertAlmostEqual(stats.holm([0.01])[0], 0.01, places=12)
        adjusted = stats.holm([0.01, 0.04, 0.03])
        self.assertAlmostEqual(adjusted[0], 0.03, places=12)
        self.assertAlmostEqual(adjusted[1], 0.06, places=12)
        self.assertAlmostEqual(adjusted[2], 0.06, places=12)

    def test_holm_never_goes_down(self):
        raw = [0.2, 0.01, 0.5, 0.03]
        adjusted = stats.holm(raw)
        for value, corrected in zip(raw, adjusted):
            self.assertGreaterEqual(corrected, value - 1e-12)


class IntervalsAndEffects(unittest.TestCase):
    def test_bootstrap_is_deterministic_and_brackets_the_median(self):
        values = [-0.4, -0.1, -0.05, 0.0, 0.02, 0.05, 0.3, 0.9, -0.2, 0.15]
        first = stats.bootstrap_interval(values)
        second = stats.bootstrap_interval(values)
        self.assertEqual(first, second)
        median = sorted(values)[len(values) // 2]
        self.assertLessEqual(first[0], median)
        self.assertGreaterEqual(first[1], median)

    def test_t_interval_is_symmetric_around_the_mean(self):
        mean, low, high = stats.t_interval([-1.0, 1.0])
        self.assertAlmostEqual(mean, 0.0, places=12)
        self.assertAlmostEqual(mean - low, high - mean, places=12)

    def test_effect_sizes_point_the_same_way_as_the_differences(self):
        better = [-0.4, -0.3, -0.25, -0.2, -0.15, -0.1, -0.05, -0.45, -0.35, -0.5]
        sizes = stats.effect_sizes(better)
        self.assertLess(sizes["cohens_dz"], 0)
        self.assertAlmostEqual(sizes["probability_of_superiority"], 1.0, places=12)
        self.assertAlmostEqual(sizes["rank_biserial"], -1.0, places=12)


class WordingRule(unittest.TestCase):
    def test_a_failed_test_is_not_reported_as_equality(self):
        phrase = stats.evidence_phrase(-0.002, 0.003, 0.7)
        self.assertTrue(phrase.startswith("no evidence of a difference at this budget"))
        self.assertIn("not the same claim as no difference", phrase)

    def test_a_passing_test_is_reported_as_evidence(self):
        phrase = stats.evidence_phrase(-0.01, -0.002, 0.001)
        self.assertTrue(phrase.startswith("evidence of a difference"))
        self.assertNotIn("no evidence", phrase)

    def test_a_p_value_alone_is_not_enough(self):
        """p <= alpha with an interval that straddles zero is not called significant."""
        phrase = stats.evidence_phrase(-0.01, 0.02, 0.01)
        self.assertTrue(phrase.startswith("no evidence"))

    def test_identical_arms_are_reported_as_nothing_to_test(self):
        summary = stats.summarise([0.0] * 10)
        self.assertFalse(summary["informative"])
        self.assertIn("identical in every seed", summary["verdict"])


class CommittedData(unittest.TestCase):
    """Pin two answers on the committed ten-seed files: one clear effect and one that is not."""

    def _comparison(self, suite: str, arm: str, reference: str, metric: str = "test_loss"):
        directory = ROOT / "runs" / f"seed-sweep-{suite}"
        _, series = stats.load_sweep(directory, metric)
        differences = [a - b for a, b in zip(series[arm], series[reference])]
        return stats.summarise(differences)

    def test_a_clear_effect_is_detected(self):
        summary = self._comparison("optimizers", "adagrad", "adam", metric="epochs_to_target")
        self.assertLess(summary["combined_p"], 0.05)
        self.assertGreater(summary["wins"], 8)
        self.assertTrue(summary["verdict"].startswith("evidence of a difference"))

    def test_the_eight_wins_out_of_ten_case_is_not_significant(self):
        """The case that motivated the wording rule: eight wins, and a mean difference of 9e-5."""
        summary = self._comparison("norm-layernorm", "ademamix", "adamw_constant")
        self.assertEqual(summary["wins"], 8)
        self.assertGreater(summary["combined_p"], 0.05)
        self.assertLess(abs(summary["mean"]), 1e-3)
        self.assertTrue(summary["verdict"].startswith("no evidence"))

    def test_a_family_of_comparisons_is_adjusted(self):
        report = stats.build_report(ROOT / "runs", "test_loss", ["optimizers"], None, 0.05)
        self.assertGreater(report["comparisons_tested"], 1)
        for item in report["comparisons"]:
            self.assertGreaterEqual(item["holm_p"], item["combined_p"] - 1e-12)

    def test_every_verdict_comes_from_the_closed_set_of_phrasings(self):
        """No bypass path around the wording rule.

        The rule is only worth having if nothing can print a verdict that did not come from
        `evidence_phrase`. The renderer prints `item["verdict"]` and nothing else, so this test pins the
        closed set of phrasings over the whole corpus and checks that the rendered tables introduce no
        equality claim of their own.
        """
        report = stats.build_report(ROOT / "runs", "test_loss", None, None, 0.05)
        allowed = (
            "evidence of a difference",
            "no evidence of a difference at this budget",
            "the two arms are identical in every seed",
        )
        verdicts = [item["verdict"] for item in report["comparisons"]]
        verdicts += [detail["verdict"] for family in report["claim_families"] for detail in family["detail"]]
        self.assertTrue(verdicts)
        for verdict in verdicts:
            self.assertTrue(verdict.startswith(allowed), verdict)
        markdown = stats.render_markdown(report)
        for forbidden in ("no difference between", "are equal", "no effect", "proves"):
            self.assertNotIn(forbidden, markdown)


if __name__ == "__main__":
    unittest.main()
