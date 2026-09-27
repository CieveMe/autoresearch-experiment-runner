import math
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from autoresearch import datasets, schedules
from autoresearch.dataset import make_dataset, split_dataset
from autoresearch.trainers import mlp
from autoresearch.trainers.registry import TRAINERS, get_trainer


def rows():
    data = make_dataset(size=120, seed=5, noise=0.18)
    return split_dataset(data, 0.25)[0]


class AdEMAMixIdentityTests(unittest.TestCase):
    def test_alpha_zero_reproduces_adamw_exactly(self):
        """The slow EMA is the only difference from AdamW, so switching it off must
        reproduce AdamW's trajectory.

        Equal only up to floating-point rounding, not bit for bit: the two rules reach
        the same value through differently associated expressions ((lr·m̂)/d versus
        lr·(m̂/d)), which can differ in the last bit. The comparison is therefore tight
        (1e-12 relative) rather than exact, and the pinned expectations keep their
        8-decimal rounding either way.
        """
        common = {"learning_rate": 0.4, "epochs": 40, "seed": 5}
        adamw = mlp_or_logistic("adamw", common)
        ablation = mlp_or_logistic("ademamix", {**common, "alpha": 0.0, "beta3": 0.9999})
        self.assertEqual(len(adamw), len(ablation))
        for index, (left, right) in enumerate(zip(adamw, ablation)):
            self.assertTrue(
                math.isclose(left, right, rel_tol=1e-12, abs_tol=1e-15),
                f"epoch {index + 1}: {left!r} != {right!r}",
            )

    def test_alpha_above_zero_changes_the_curve(self):
        common = {"learning_rate": 0.4, "epochs": 40, "seed": 5}
        adamw = mlp_or_logistic("adamw", common)
        ademamix = mlp_or_logistic("ademamix", {**common, "alpha": 2.0, "beta3": 0.9999})
        self.assertNotEqual(adamw, ademamix)

    def test_warmup_schedules_follow_the_reference_form(self):
        self.assertEqual(schedules.alpha_schedule(1, 2.0, 4), 0.5)
        self.assertEqual(schedules.alpha_schedule(4, 2.0, 4), 2.0)
        self.assertEqual(schedules.alpha_schedule(9, 2.0, None), 2.0)
        # beta3 warmup interpolates in half-life space and is monotone in the ramp
        values = [schedules.beta3_schedule(step, 0.9999, 8) for step in range(1, 9)]
        self.assertTrue(all(second > first for first, second in zip(values, values[1:])))
        self.assertAlmostEqual(values[-1], 0.9999, places=6)


class ScheduleTests(unittest.TestCase):
    def test_constant_schedule_is_exactly_one(self):
        self.assertEqual(schedules.schedule_factor(7, {"epochs": 120}), 1.0)

    def test_cosine_starts_at_one_and_ends_at_the_floor(self):
        config = {"schedule": "cosine", "epochs": 10, "min_lr_factor": 0.1}
        self.assertAlmostEqual(schedules.schedule_factor(1, config), 1.0, places=6)
        self.assertAlmostEqual(schedules.schedule_factor(10, config), 0.1, places=6)

    def test_warmup_cosine_ramps_then_decays(self):
        config = {"schedule": "warmup_cosine", "epochs": 10, "warmup_steps": 4, "min_lr_factor": 0.0}
        self.assertLess(schedules.schedule_factor(2, config), schedules.schedule_factor(4, config))
        self.assertGreater(schedules.schedule_factor(4, config), schedules.schedule_factor(10, config))

    def test_unknown_schedule_is_rejected(self):
        with self.assertRaises(ValueError):
            schedules.schedule_factor(1, {"schedule": "exponential"})


class MLPTrainerTests(unittest.TestCase):
    def test_gradients_match_numerical_differences(self):
        """A backprop sign/index error looks exactly like 'the method does not work',
        so the analytic gradient is checked against finite differences."""
        train_rows = rows()[:20]
        config = {"hidden_sizes": [3], "seed": 11, "weight_decay": 0.0}
        params = mlp._init_params(len(train_rows[0][0]), [3], 11)
        epsilon = 1e-6
        scale = 1.0 / len(train_rows)
        analytic_gradients = mlp.gradients(train_rows, params)
        for layer, matrix in enumerate(params["weights"]):
            for unit, row in enumerate(matrix):
                for index in range(len(row)):
                    original = row[index]
                    row[index] = original + epsilon
                    high = mlp.loss(train_rows, params, 0.0)
                    row[index] = original - epsilon
                    low = mlp.loss(train_rows, params, 0.0)
                    row[index] = original
                    numerical = (high - low) / (2 * epsilon)
                    analytic = analytic_gradients["weights"][layer][unit][index] * scale
                    self.assertAlmostEqual(numerical, analytic, places=6, msg=f"W{layer}[{unit}][{index}]")

    def test_training_is_deterministic(self):
        config = {"optimizer": "adam", "learning_rate": 0.1, "epochs": 25, "hidden_sizes": [4], "seed": 3}
        first = mlp.fit(rows(), config)
        second = mlp.fit(rows(), config)
        self.assertEqual(first.loss_curve, second.loss_curve)
        self.assertEqual(first.final_loss, second.final_loss)

    def test_learns_something(self):
        config = {"optimizer": "adam", "learning_rate": 0.2, "epochs": 60, "hidden_sizes": [6], "seed": 3}
        result = mlp.fit(rows(), config)
        metrics = mlp.evaluate(rows(), result.params, 0.0)
        self.assertGreater(metrics["accuracy"], 0.8)

    def test_registry_lists_both_trainers(self):
        self.assertEqual(set(TRAINERS), {"logistic", "mlp"})
        with self.assertRaises(ValueError):
            get_trainer("transformer")


class DatasetTests(unittest.TestCase):
    def test_remote_paths_are_refused(self):
        with self.assertRaises(ValueError) as context:
            datasets.load_rows({"source": "csv", "path": "https://example.com/data.csv"})
        self.assertIn("remote datasets are not supported", str(context.exception))

    def test_local_json_round_trip(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "rows.json"
            path.write_text('[{"features": [0.5, -0.5], "label": 1}, {"features": [0.1, 0.2], "label": 0}]', encoding="utf-8")
            loaded = datasets.load_rows({"source": "json", "path": str(path)})
        self.assertEqual(loaded, [([0.5, -0.5], 1), ([0.1, 0.2], 0)])


def mlp_or_logistic(optimizer, config):
    """Run the logistic trainer and return its loss curve (the identity we assert)."""
    from autoresearch.trainers.logistic import fit

    return fit(rows(), {"optimizer": optimizer, **config}).loss_curve


if __name__ == "__main__":
    unittest.main()
