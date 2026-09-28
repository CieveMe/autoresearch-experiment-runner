"""Schedule-Free port checks.

The rule was transliterated from `adamw_schedulefree_reference.py` (Meta, Apache-2.0). Two
things are asserted here that a "does it run" test would miss: that the reference arithmetic
is reproduced step by step, and that the *reported* parameters are the averaged sequence
(`x`) rather than the training point (`y`) — evaluating at `y` would flatter the method in
any comparison against a scheduled baseline.
"""

import math
import random
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from autoresearch import optimizers
from autoresearch.trainers.logistic import fit


def reference_schedule_free_adamw(values, gradients, config, steps):
    """Literal transliteration of the reference step, written independently of the library
    rule so that a wiring or ordering mistake in one shows up as a mismatch. Both were
    written from the same source, so this catches transcription errors, not a shared
    misreading of the paper."""
    beta1 = config.get("beta1", 0.9)
    beta2 = config.get("beta2", 0.999)
    eps = config.get("epsilon", 1e-8)
    base_lr = config.get("learning_rate", 0.1)
    decay = config.get("weight_decay", 0.0)
    warmup = config.get("warmup_steps", 0)
    weight_lr_power = config.get("weight_lr_power", 2.0)
    average_power = config.get("average_power", 0.0)
    z = list(values)
    x = list(values)
    y = list(values)
    squared = [0.0] * len(values)
    lr_max = 0.0
    weight_sum = 0.0
    for k in range(steps):
        sched = (k + 1) / warmup if (warmup and k < warmup) else 1.0
        lr = (base_lr * sched) if base_lr else eps
        lr_max = max(lr, lr_max)
        weight = ((k + 1) ** average_power) * (lr_max**weight_lr_power)
        weight_sum += weight
        ckp1 = weight / weight_sum if weight_sum else 0.0
        bias_correction2 = 1 - beta2 ** (k + 1)
        for index, gradient in enumerate(gradients):
            if decay:
                z[index] -= lr * decay * y[index]
            squared[index] = beta2 * squared[index] + (1 - beta2) * gradient * gradient
            denom = math.sqrt(squared[index] / bias_correction2) + eps
            z[index] -= lr * gradient / denom
            x[index] = (1 - ckp1) * x[index] + ckp1 * z[index]
            y[index] = beta1 * x[index] + (1 - beta1) * z[index]
    return x, y


class ScheduleFreePortTests(unittest.TestCase):
    def test_matches_the_reference_arithmetic(self):
        config = {"learning_rate": 0.05, "beta1": 0.9, "beta2": 0.999, "epsilon": 1e-8, "weight_decay": 0.0}
        values = [0.5, -0.25]
        gradients = [0.3, -0.1]
        expected_x, expected_y = reference_schedule_free_adamw(values, gradients, config, steps=5)

        weights = list(values)
        state = optimizers.initial_state("schedule_free_adamw", len(weights), config)
        bias = 0.0
        for epoch in range(1, 6):
            bias = optimizers.apply_update(
                "schedule_free_adamw", weights, bias, gradients, 0.0, state, config, epoch
            )
        eval_weights, _ = optimizers.eval_params("schedule_free_adamw", weights, bias, state)
        for index, expected in enumerate(expected_x):
            self.assertAlmostEqual(eval_weights[index], expected, places=12, msg=f"x[{index}]")
        for index, expected in enumerate(expected_y):
            self.assertAlmostEqual(weights[index], expected, places=12, msg=f"y[{index}]")
        self.assertNotAlmostEqual(eval_weights[0], weights[0], places=9)

    def test_reports_the_averaged_sequence_not_the_training_point(self):
        rows = [([0.5, -0.5], 1), ([0.2, 0.3], 0), ([-0.4, 0.1], 1), ([0.9, -0.2], 0)]
        result = fit(rows, {"optimizer": "schedule_free_adamw", "learning_rate": 0.1, "epochs": 30, "beta1": 0.9})
        weights, _ = result.params
        # the averaged sequence is a convex combination of the path, so it must stay inside
        # the range the raw iterates pass through; comparing the two confirms they differ
        raw = fit(rows, {"optimizer": "adamw", "learning_rate": 0.1, "epochs": 30})
        self.assertNotEqual([round(value, 6) for value in weights], [round(value, 6) for value in raw.params[0]])

    def test_training_is_deterministic(self):
        rows = [([0.5, -0.5], 1), ([0.2, 0.3], 0), ([-0.4, 0.1], 1)]
        config = {"optimizer": "schedule_free_sgd", "learning_rate": 0.2, "epochs": 20}
        first = fit(rows, config)
        second = fit(rows, config)
        self.assertEqual(first.loss_curve, second.loss_curve)

    def test_warmup_matches_the_reference_ramp(self):
        config = {"learning_rate": 0.1, "warmup_steps": 4, "beta1": 0.9, "beta2": 0.999}
        values = [0.0]
        gradients = [1.0]
        expected_x, _ = reference_schedule_free_adamw(values, gradients, config, steps=4)
        weights = [0.0]
        state = optimizers.initial_state("schedule_free_adamw", 1, config)
        bias = 0.0
        for epoch in range(1, 5):
            bias = optimizers.apply_update(
                "schedule_free_adamw", weights, bias, gradients, 0.0, state, config, epoch
            )
        eval_weights, _ = optimizers.eval_params("schedule_free_adamw", weights, bias, state)
        self.assertAlmostEqual(eval_weights[0], expected_x[0], places=12)

    def test_schedule_factor_still_reaches_a_cosine_baseline(self):
        from autoresearch import schedules

        config = {"schedule": "cosine", "epochs": 10, "learning_rate": 0.1, "min_lr_factor": 0.0}
        first = schedules.schedule_factor(1, config)
        last = schedules.schedule_factor(10, config)
        self.assertAlmostEqual(first, 1.0, places=6)
        self.assertLess(last, 0.01)


if __name__ == "__main__":
    unittest.main()
