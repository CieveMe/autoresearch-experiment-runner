import tempfile
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from autoresearch.runner import run


class RunnerTests(unittest.TestCase):
    def test_run_writes_reproducible_artifacts(self):
        config = ROOT / "examples" / "classification.json"
        with tempfile.TemporaryDirectory() as directory:
            first = run(config, Path(directory) / "first")
            second = run(config, Path(directory) / "second")
            self.assertEqual(first["best"]["name"], second["best"]["name"])
            self.assertEqual(first["best"]["test_accuracy"], second["best"]["test_accuracy"])
            self.assertEqual(first["best"]["name"], "adam_reproduction")
            self.assertTrue((Path(directory) / "first" / "report.md").exists())
            self.assertEqual(len(first["results"]), 4)
            self.assertGreaterEqual(first["best"]["test_accuracy"], 0.80)


if __name__ == "__main__":
    unittest.main()
