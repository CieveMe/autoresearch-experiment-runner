import contextlib
import copy
import hashlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.html_report import main, render


class HtmlReportTests(unittest.TestCase):
    def setUp(self):
        self.payload = json.loads((ROOT / "runs/demo-verified/results.json").read_text(encoding="utf-8"))

    def page(self):
        return render(self.payload, "results.json", "abc")

    def test_offline_escaped_and_deterministic(self):
        self.payload["task"] = '<script>alert("x")</script>'
        self.payload["results"][0]["name"] = '<img src=x onerror="oops">'
        before = copy.deepcopy(self.payload)
        page = self.page()
        self.assertEqual(page, self.page())
        self.assertEqual(before, self.payload)
        self.assertIn("&lt;script&gt;", page)
        self.assertIn("&lt;img", page)
        self.assertNotIn("<script", page)
        self.assertNotIn("<img", page)
        self.assertNotIn('src="http', page)
        self.assertIn("Export does not verify expected", page)

    def test_metric_direction_ties_and_missing_target(self):
        a, b, c = [copy.deepcopy(self.payload["results"][0]) for _ in range(3)]
        for item, name, loss, accuracy in ((a, "AAA", .3, .9), (b, "BBB", .2, .8), (c, "CCC", .2, .95)):
            item.update(name=name, test_loss=loss, test_accuracy=accuracy)
        self.payload.update(results=[a, b, c], metric="test_loss")
        page = self.page()
        self.assertLess(page.index("<td>BBB</td>"), page.index("<td>CCC</td>"))
        self.assertLess(page.index("<td>CCC</td>"), page.index("<td>AAA</td>"))
        self.payload["metric"] = "test_accuracy"
        page = self.page()
        self.assertLess(page.index("<td>CCC</td>"), page.index("<td>AAA</td>"))
        self.assertLess(page.index("<td>AAA</td>"), page.index("<td>BBB</td>"))
        self.payload.update(metric="epochs_to_target", target_loss=.2)
        a["epochs_to_target"], b["epochs_to_target"], c["epochs_to_target"] = None, 5, 3
        page = self.page()
        self.assertLess(page.index("<td>CCC</td>"), page.index("<td>BBB</td>"))
        self.assertLess(page.index("<td>BBB</td>"), page.index("<td>AAA</td>"))
        self.assertIn("Not reached", page)
        self.payload["target_loss"] = None
        self.assertIn("Not configured", self.page())
        self.assertNotIn("Not reached", self.page())

    def test_curves_absent_flat_single_and_unequal(self):
        self.payload["results"] = self.payload["results"][:2]
        self.payload["results"][0]["loss_curve"] = [.5]
        self.payload["results"][1]["loss_curve"] = [.5, .5, .5]
        page = self.page()
        self.assertIn('points="60.000,280.000 420.000,280.000 780.000,280.000"', page)
        self.assertIn('<circle cx="60.000"', page)
        for item in self.payload["results"]:
            item["loss_curve"] = []
        self.assertIn("No training curves recorded", self.page())
        self.payload["results"][0]["loss_curve"] = [float("nan")]
        with self.assertRaisesRegex(ValueError, "finite"):
            self.page()

    def test_cli_keeps_source_and_binds_hash(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "results.json"
            source.write_text(json.dumps(self.payload, ensure_ascii=False), encoding="utf-8")
            before = source.read_bytes()
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(main(["--results", str(source)]), 0)
            self.assertEqual(source.read_bytes(), before)
            self.assertIn(hashlib.sha256(before).hexdigest(), source.with_name("report.html").read_text(encoding="utf-8"))
            with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as caught:
                main(["--results", str(source), "--output", str(source)])
            self.assertEqual(caught.exception.code, 1)
            self.assertEqual(source.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
