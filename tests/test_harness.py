import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from autoresearch.runner import config_sha256
from scripts.score_task import NEGATIVE_CONTROLS, _ignore as scored_copy_ignore
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

    def _verify_with_shifted_loss(self, expected_name: str, results_path: Path, arm: str, shift: float):
        payload = json.loads(results_path.read_text(encoding="utf-8"))
        for item in payload["results"]:
            if item["name"] == arm:
                item["test_loss"] = round(item["test_loss"] + shift, 8)
        with tempfile.TemporaryDirectory() as directory:
            tampered = Path(directory) / "results.json"
            tampered.write_text(json.dumps(payload), encoding="utf-8")
            return verify(tampered, ROOT / "expected" / expected_name)

    def test_a_trial_tolerance_widens_that_trial_and_nothing_else(self):
        """Case 7's repair has to be scoped: one arm, measured basis, everything else still tight.

        The schedule-free AdamW arm amplifies last-bit libm differences, so its `test_loss` carries a
        wider tolerance. This test pins the scope from both sides: a shift inside the widened band is
        accepted for that arm, a shift outside it is rejected, and a shift 10x smaller is still rejected
        for a *different* arm in the same file.
        """
        results = ROOT / "runs" / "schedule-free-mlp" / "results.json"
        if not results.exists():
            results = ROOT / "runs" / "schedule-free-verified" / "mlp" / "results.json"
        if not results.exists():
            self.skipTest("no schedule-free MLP results in this working tree")

        _, checks = self._verify_with_shifted_loss(
            "expected_schedule_free_mlp.json", results, "schedule_free_adamw", 0.001)
        self.assertTrue(any("tolerance 0.005" in line for line in checks),
                        "the widened tolerance must be visible in the check output")

        failures, _ = self._verify_with_shifted_loss(
            "expected_schedule_free_mlp.json", results, "schedule_free_adamw", 0.02)
        self.assertTrue(any("schedule_free_adamw" in failure for failure in failures),
                        "a shift well outside the measured band must still fail")

        failures, _ = self._verify_with_shifted_loss(
            "expected_schedule_free_mlp.json", results, "adamw_cosine", 1e-5)
        self.assertTrue(any("adamw_cosine" in failure for failure in failures),
                        "another arm in the same file must keep the 1e-6 tolerance")

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

    def test_every_control_fragment_changes_the_numbers_it_mutates(self):
        """Presence is not enough: the fragment has to be in the code that runs.

        Case 6a. A rewrite that leaves the original branch behind as dead code satisfies every fragment
        check while the code that actually executes is untouched — the controls then report that a broken
        implementation passed, and the harness has lost its teeth. This happened for real while running
        the T-ADAM-01B variant, so the guard is behavioural: mutate a throwaway copy, run one tiny
        experiment with the optimizer the mutation targets, and require the loss to move.
        """
        self._check_control_liveness()

    def test_the_scored_copy_can_run_the_repositorys_own_tests(self):
        """Case 6b: the copy the scorer builds must be isomorphic enough to run the real suite.

        The scorer copies the repository before mutating it. When that copy dropped the committed
        per-seed sweeps, the analysis tests failed inside every scored tree, a perfect submission
        reported ``exit 1``, and two controls came back *missed* — a verdict about the copy rather than
        about the submission. The guard is the property itself: build the copy the way `score_task.py`
        builds it and require the repository's own suite to pass inside it.
        """
        if os.environ.get("AUTORESEARCH_COPY_CHECK"):
            self.skipTest("already running inside a scored copy")
        with tempfile.TemporaryDirectory() as temporary:
            copy = Path(temporary) / "scored"
            shutil.copytree(ROOT, copy, ignore=scored_copy_ignore)
            environment = dict(os.environ, AUTORESEARCH_COPY_CHECK="1")
            result = subprocess.run(
                [sys.executable, "-m", "unittest", "discover", "-s", "tests"],
                cwd=str(copy), env=environment, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, encoding="utf-8", errors="replace",
            )
            self.assertEqual(result.returncode, 0,
                             "the scored copy cannot run the repository's own tests:\n"
                             + result.stdout[-2000:])

    def test_the_container_image_contains_everything_the_suite_reads(self):
        """Case 6b's second copy: the image that runs `repro.py` must carry what the suite reads.

        `scripts/repro.py` ends with `unittest discover`, so the container image is a third place where
        the repository's own suite runs — and it failed there for a whole CI run because `TODO.md`, which
        the live-document guard reads, was never copied into the image. The required list is derived from
        the test sources rather than written by hand, so a test that starts reading a new file fails here
        instead of in the CI docker job, where the traceback is the only symptom.
        """
        dockerfile = (ROOT / "Dockerfile").read_text(encoding="utf-8")
        required = self._top_level_entries_the_suite_touches()
        missing = self._missing_from_image(dockerfile, required)
        self.assertEqual(missing, [], f"the Dockerfile does not copy: {missing}")
        # Negative control for this guard: without TODO.md it must say so. A check that cannot fail is
        # the thing this family exists to prevent (case 6a).
        crippled = "\n".join(line for line in dockerfile.splitlines() if "TODO.md" not in line)
        self.assertIn("TODO.md", self._missing_from_image(crippled, required))

    @staticmethod
    def _image_copy_sources(dockerfile: str):
        copied = set()
        for line in dockerfile.splitlines():
            tokens = line.split()
            if tokens and tokens[0].upper() == "COPY" and len(tokens) >= 3:
                copied.update(tokens[1:-1])
        return copied

    def _top_level_entries_the_suite_touches(self):
        """Top-level repository entries the test sources name, whether via a path join or a literal."""
        entries = {path.name for path in ROOT.iterdir()}
        sources = "\n".join(path.read_text(encoding="utf-8")
                            for path in sorted((ROOT / "tests").glob("test_*.py")))
        referenced = {name for name in entries
                      if re.search(rf'["\']({re.escape(name)})["\']', sources)}
        referenced.update(name for name in re.findall(r'ROOT\s*/\s*"([^"/]+)"', sources)
                          if name in entries)
        # `runs/` is supplied by the compose mount; the build recipe itself and the ignore files are not
        # things the suite reads from inside the image.
        for excluded in ("runs", "Dockerfile", ".dockerignore", ".gitignore", "compose.yaml"):
            referenced.discard(excluded)
        return sorted(referenced)

    def _missing_from_image(self, dockerfile: str, required):
        copied = self._image_copy_sources(dockerfile)
        return [name for name in required if name not in copied]

    def _check_control_liveness(self):
        """Presence is not enough: the fragment has to be in the code that runs.

        A rewrite that leaves the original branch behind as dead code satisfies every fragment check
        while the code that actually executes is untouched — the controls then report that a broken
        implementation passed, and the harness has lost its teeth. This happened for real while running
        the T-ADAM-01B variant, so the guard is behavioural: mutate a throwaway copy, run one tiny
        experiment with the optimizer the mutation targets, and require the loss to move.
        """
        exercise = {
            "no-bias-correction": "adam",
            "no-adaptive-scaling": "adam",
            "ademamix-without-slow-ema": "ademamix",
            "schedule-free-without-averaging": "schedule_free_adamw",
        }
        for name, optimizer in exercise.items():
            with self.subTest(control=name):
                with tempfile.TemporaryDirectory() as temporary:
                    probe = Path(temporary) / "repo"
                    shutil.copytree(ROOT / "autoresearch", probe / "autoresearch")
                    config = {
                        "task": f"liveness probe for {name}",
                        "trainer": "logistic",
                        "metric": "test_loss",
                        "seed": 7,
                        "dataset": {"size": 200, "test_ratio": 0.25, "noise": 0.18},
                        "baseline": {"name": "probe", "optimizer": "sgd",
                                     "learning_rate": 0.1, "epochs": 6},
                        "experiments": [{"name": "arm", "optimizer": optimizer, "alpha": 2.0,
                                         "beta3": 0.9999, "learning_rate": 0.1, "epochs": 6}],
                    }
                    config_path = probe / "probe.json"
                    config_path.write_text(json.dumps(config), encoding="utf-8")
                    before = _run_probe(probe, config_path)
                    for fragment in NEGATIVE_CONTROLS[name]:
                        target = probe / fragment["file"]
                        text = target.read_text(encoding="utf-8")
                        self.assertIn(fragment["old"], text, f"{name} in {target.name}")
                        target.write_text(text.replace(fragment["old"], fragment["new"]), encoding="utf-8")
                    after = _run_probe(probe, config_path, "mutated")
                    self.assertNotAlmostEqual(
                        before, after, places=9,
                        msg=f"control `{name}` did not change the numbers it mutates: the fragment is "
                            f"present but not live",
                    )


def _run_probe(probe: Path, config_path: Path, tag: str = "clean") -> float:
    """Run one tiny experiment in the probe copy and return its final test loss."""
    result = subprocess.run(
        [sys.executable, "-m", "autoresearch.cli", "run", "--config", str(config_path),
         "--output", f"runs/{tag}"],
        cwd=str(probe), stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        text=True, encoding="utf-8", errors="replace",
    )
    if result.returncode != 0:
        raise AssertionError(f"probe run failed: {result.stdout[-400:]}")
    payload = json.loads((probe / "runs" / tag / "results.json").read_text(encoding="utf-8"))
    return next(item["test_loss"] for item in payload["results"] if item["name"] == "arm")


if __name__ == "__main__":
    unittest.main()
