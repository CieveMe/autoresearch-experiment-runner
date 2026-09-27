import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from autoresearch.runner import config_sha256
from scripts.score_task import NEGATIVE_CONTROLS
from scripts.seed_sweep import _aggregate, parse_seeds
from scripts.verify_results import DEFAULT_EXPECTED, verify

VERIFIED_RESULTS = ROOT / "runs" / "demo-verified" / "results.json"


class ConfigHashTests(unittest.TestCase):
    def test_newline_style_does_not_change_the_config_hash(self):
        """A Windows checkout must report the same revision hash as a Linux one."""
        with tempfile.TemporaryDirectory() as directory:
            lf = Path(directory) / "lf.json"
            crlf = Path(directory) / "crlf.json"
            cr = Path(directory) / "cr.json"
            payload = b'{\n  "seed": 7\n}\n'
            lf.write_bytes(payload)
            crlf.write_bytes(payload.replace(b"\n", b"\r\n"))
            cr.write_bytes(payload.replace(b"\n", b"\r"))
            self.assertEqual(config_sha256(lf), config_sha256(crlf))
            self.assertEqual(config_sha256(lf), config_sha256(cr))

    def test_real_config_keeps_its_recorded_hash(self):
        expected = json.loads(DEFAULT_EXPECTED.read_text(encoding="utf-8"))
        self.assertEqual(
            config_sha256(ROOT / "examples" / "classification.json"),
            expected["config_sha256"],
        )


class VerifyTests(unittest.TestCase):
    def test_committed_verified_run_matches_expectations(self):
        if not VERIFIED_RESULTS.exists():
            self.skipTest("runs/demo-verified/results.json is not part of this working tree")
        failures, checks = verify(VERIFIED_RESULTS, DEFAULT_EXPECTED)
        self.assertTrue(checks)
        self.assertEqual(failures, [])

    def test_tampered_number_is_rejected(self):
        if not VERIFIED_RESULTS.exists():
            self.skipTest("runs/demo-verified/results.json is not part of this working tree")
        payload = json.loads(VERIFIED_RESULTS.read_text(encoding="utf-8"))
        for item in payload["results"]:
            if item["name"] == "adam_reproduction":
                item["test_loss"] = 0.5
        with tempfile.TemporaryDirectory() as directory:
            tampered = Path(directory) / "results.json"
            tampered.write_text(json.dumps(payload), encoding="utf-8")
            failures, _ = verify(tampered, DEFAULT_EXPECTED)
        self.assertTrue(any("trial[adam_reproduction].test_loss" in failure for failure in failures))


class SeedSweepTests(unittest.TestCase):
    def test_parse_seeds_accepts_ranges_and_lists(self):
        self.assertEqual(parse_seeds("0-2"), [0, 1, 2])
        self.assertEqual(parse_seeds("0,2,7"), [0, 2, 7])
        self.assertEqual(parse_seeds(" 1-2 , 4 "), [1, 2, 4])
        self.assertEqual(parse_seeds("3,3,3"), [3])

    def test_aggregate_reports_means_wins_and_paired_gain(self):
        def payload(seed, adam_loss, sgd_loss):
            return {
                "seed": seed,
                "config_sha256": f"seed-{seed}",
                "paper": {},
                "metric": "test_loss",
                "results": [
                    {"name": "baseline", "config": {"optimizer": "sgd", "learning_rate": 0.15},
                     "test_accuracy": 0.90, "test_loss": sgd_loss, "epochs": 10},
                    {"name": "adam_reproduction", "config": {"optimizer": "adam", "learning_rate": 0.08},
                     "test_accuracy": 0.92, "test_loss": adam_loss, "epochs": 10},
                ],
            }

        summary = _aggregate(
            [payload(0, 0.20, 0.40), payload(1, 0.30, 0.50)],
            "test_loss",
            ROOT / "examples" / "classification.json",
            ["baseline"],
        )
        self.assertEqual(summary["seed_count"], 2)
        self.assertAlmostEqual(summary["trials"]["adam_reproduction"]["metric_mean"], 0.25)
        self.assertEqual(summary["trials"]["adam_reproduction"]["wins"], 2)
        self.assertEqual(summary["trials"]["adam_reproduction"]["win_rate"], 1.0)
        paired = summary["paired_improvement"]["baseline"]["adam_reproduction"]
        self.assertEqual(paired["better_in"], 2)
        self.assertAlmostEqual(paired["mean_improvement"], 0.20)


class NegativeControlTests(unittest.TestCase):
    def test_every_control_fragment_still_exists_in_the_source_it_names(self):
        """Controls must fail loudly instead of silently turning into no-ops.

        The fragment is checked in the file the control names, so moving an
        implementation between modules cannot quietly disarm a control.
        """
        for name, mutations in NEGATIVE_CONTROLS.items():
            with self.subTest(control=name):
                for mutation in mutations:
                    target = ROOT / mutation.get("file", "autoresearch/model.py")
                    self.assertTrue(target.exists(), f"{name}: missing {target}")
                    source = target.read_text(encoding="utf-8")
                    self.assertIn(mutation["old"], source, f"{name} in {target.name}")


if __name__ == "__main__":
    unittest.main()
