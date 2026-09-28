import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from autoresearch.dataset import make_dataset, split_dataset
from autoresearch.model import SUPPORTED_OPTIMIZERS, epochs_to_target, train
from autoresearch.runner import rank_key


def _rows():
    rows = make_dataset(size=200, seed=3, noise=0.18)
    return split_dataset(rows, 0.25)[0]


class OptimizerTests(unittest.TestCase):
    def test_every_supported_optimizer_trains_deterministically(self):
        rows = _rows()
        configs = {
            "sgd": {"optimizer": "sgd", "learning_rate": 0.3},
            "sgd_momentum": {"optimizer": "sgd_momentum", "learning_rate": 0.2, "momentum": 0.9},
            "adagrad": {"optimizer": "adagrad", "learning_rate": 0.5},
            "rmsprop": {"optimizer": "rmsprop", "learning_rate": 0.1, "decay": 0.9},
            "adam": {"optimizer": "adam", "learning_rate": 0.1},
            "adamw": {"optimizer": "adamw", "learning_rate": 0.1, "weight_decay": 0.01},
            "ademamix": {"optimizer": "ademamix", "learning_rate": 0.05, "alpha": 2.0, "beta3": 0.9999},
            "schedule_free_adamw": {"optimizer": "schedule_free_adamw", "learning_rate": 0.1},
            "schedule_free_sgd": {"optimizer": "schedule_free_sgd", "learning_rate": 0.1},
        }
        self.assertEqual(set(configs), set(SUPPORTED_OPTIMIZERS))
        for name, config in configs.items():
            with self.subTest(optimizer=name):
                first = train(rows, {**config, "epochs": 20})
                second = train(rows, {**config, "epochs": 20})
                self.assertEqual(first[:4], second[:4])
                self.assertEqual(len(first[4]), 20)
                self.assertLess(first[3], 1.0)  # learned something beyond a coin flip

    def test_momentum_and_adaptive_rules_differ_from_plain_sgd(self):
        rows = _rows()
        sgd = train(rows, {"optimizer": "sgd", "learning_rate": 0.3, "epochs": 20})
        momentum = train(rows, {"optimizer": "sgd_momentum", "learning_rate": 0.3, "momentum": 0.9, "epochs": 20})
        self.assertNotAlmostEqual(sgd[3], momentum[3], places=6)

    def test_bias_correction_switch_changes_the_curve(self):
        rows = _rows()
        with_correction = train(rows, {"optimizer": "adam", "learning_rate": 0.4, "epochs": 20})
        without_correction = train(rows, {"optimizer": "adam", "learning_rate": 0.4, "bias_correction": False, "epochs": 20})
        self.assertNotEqual(with_correction[4][0], without_correction[4][0])

    def test_unknown_optimizer_is_rejected(self):
        with self.assertRaises(ValueError):
            train(_rows(), {"optimizer": "nesterov", "epochs": 5})


class EpochsToTargetTests(unittest.TestCase):
    def test_returns_first_epoch_at_or_below_target(self):
        self.assertEqual(epochs_to_target([0.5, 0.4, 0.3, 0.29], 0.3), 3)

    def test_returns_none_when_never_reached(self):
        self.assertIsNone(epochs_to_target([0.5, 0.45], 0.3))


class RankingTests(unittest.TestCase):
    def test_unreached_target_ranks_last(self):
        results = [
            {"name": "never", "epochs_to_target": None, "test_loss": 0.1},
            {"name": "late", "epochs_to_target": 50, "test_loss": 0.2},
            {"name": "early", "epochs_to_target": 5, "test_loss": 0.3},
        ]
        ranked = sorted(results, key=lambda item: rank_key(item, "epochs_to_target", True))
        self.assertEqual([item["name"] for item in ranked], ["early", "late", "never"])


if __name__ == "__main__":
    unittest.main()
