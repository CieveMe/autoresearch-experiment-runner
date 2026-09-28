"""Any suite that claims to run multiple seeds must actually vary the seed.

This is the regression test for a bug that had no visible symptom: trial configs did not
inherit the experiment's `seed`, so a "10-seed" MLP sweep varied the data split while every
run initialised from identical weights. The numbers still looked plausible, which is exactly
why the contract needs an assertion rather than a comment.
"""

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from autoresearch.runner import TRIAL_INHERITED_KEYS, merge_trial_config
from scripts.repro import SUITES


def config_path(suite):
    return ROOT / suite["config"]


class SeedContractTests(unittest.TestCase):
    def test_seed_is_an_inherited_key(self):
        self.assertIn("seed", TRIAL_INHERITED_KEYS)

    def test_every_suite_trial_receives_the_experiment_seed(self):
        for name, suite in SUITES.items():
            config = json.loads(config_path(suite).read_text(encoding="utf-8"))
            if "seed" not in config:
                continue
            with self.subTest(suite=name):
                trials = [{"name": "baseline", **config["baseline"]}, *config["experiments"]]
                for trial in trials:
                    merged = merge_trial_config(config, trial)
                    self.assertIn("seed", merged, f"{name}/{trial['name']}")
                    self.assertEqual(merged["seed"], config["seed"])

    def test_a_multi_seed_sweep_produces_distinct_seeds_not_a_fixed_value(self):
        """The seed the sweep writes must reach the trial, so trainers that initialise
        from it (the MLP) actually vary across seeds."""
        for name, suite in SUITES.items():
            config = json.loads(config_path(suite).read_text(encoding="utf-8"))
            with self.subTest(suite=name):
                trials = [{"name": "baseline", **config["baseline"]}, *config["experiments"]]
                seeds = set()
                for seed in range(10):
                    seeded = {**config, "seed": seed}
                    for trial in trials:
                        seeds.add(merge_trial_config(seeded, trial)["seed"])
                self.assertEqual(len(seeds), 10, f"{name}: expected ten distinct seeds")

    def test_mlp_initialisation_follows_the_seed(self):
        """Two seeds must give different initial weights, or the sweep is measuring less
        than it claims."""
        from autoresearch.trainers.mlp import _init_params

        first = _init_params(2, [4], 0)
        second = _init_params(2, [4], 1)
        self.assertNotEqual(first, second)


if __name__ == "__main__":
    unittest.main()
