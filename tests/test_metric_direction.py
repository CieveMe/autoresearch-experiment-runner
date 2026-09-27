import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from autoresearch.runner import LOWER_IS_BETTER_METRICS, is_lower_is_better, rank_key


class MetricDirectionTests(unittest.TestCase):
    def test_every_metric_the_runner_can_rank_has_a_known_direction(self):
        """A metric missing here silently inverts the ranking (this happened once)."""
        for metric in ("test_loss", "train_loss", "epochs", "duration_ms", "epochs_to_target"):
            with self.subTest(metric=metric):
                self.assertTrue(is_lower_is_better(metric))
        for metric in ("test_accuracy", "train_accuracy"):
            with self.subTest(metric=metric):
                self.assertFalse(is_lower_is_better(metric))

    def test_epochs_to_target_is_ranked_ascending(self):
        self.assertIn("epochs_to_target", LOWER_IS_BETTER_METRICS)
        results = [
            {"name": "slow", "epochs_to_target": 42, "test_loss": 0.1},
            {"name": "fast", "epochs_to_target": 4, "test_loss": 0.2},
        ]
        ranked = sorted(results, key=lambda item: rank_key(item, "epochs_to_target", is_lower_is_better("epochs_to_target")))
        self.assertEqual(ranked[0]["name"], "fast")


if __name__ == "__main__":
    unittest.main()
