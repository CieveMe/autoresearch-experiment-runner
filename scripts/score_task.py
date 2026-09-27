#!/usr/bin/env python3
"""Score a submission against TASK.md and run the negative controls.

Two things are checked:

1. **Scoring contract** - `scripts/repro.py` is executed and the verified-check
   count from `expected/expected_metrics.json` is turned into a 0-100 score, so a
   partially working attempt gets partial credit instead of a binary verdict.
2. **Harness sensitivity (negative controls)** - the same scorer is run against
   deliberately mutated copies of the implementation. A task whose scorer passes
   a broken implementation is worthless, so every mutation must be *detected*.

Usage:
    python scripts/score_task.py            # score the current working tree
    python scripts/score_task.py --json     # machine-readable report
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.repro import SUITES  # noqa: E402
from scripts.verify_results import DEFAULT_EXPECTED, verify  # noqa: E402

def _ignore(directory: str, names: List[str]) -> set[str]:
    """Copy the repository without generated artifacts, but *with* the committed ones.

    ``runs/demo`` and ``runs/seed-sweep`` are regenerated per attempt; ``runs/demo-verified``
    is part of the contract (a unit test asserts the committed result still matches the
    expected numbers), so it must be present in the copy.
    """
    skip = {name for name in names if name in {".git", ".github", "__pycache__"} or name.endswith(".pyc")}
    if Path(directory).name == "runs":
        skip.update(name for name in names if not name.endswith("-verified"))
    return skip

# Each control replaces a fragment of the implementation. The expectation is that the
# reproduction harness *fails* afterwards; if it passes, the task is unfalsifiable.
# `file` is explicit because the update rules moved out of model.py into optimizers.py —
# a control that silently stops matching real source is worse than no control at all.
NEGATIVE_CONTROLS: Dict[str, List[Dict[str, str]]] = {
    "no-bias-correction": [
        {
            "file": "autoresearch/optimizers.py",
            "old": "corrected_first = first_moment[index] / (1.0 - beta1**step) if bias_correction else first_moment[index]",
            "new": "corrected_first = first_moment[index]",
        },
        {
            "file": "autoresearch/optimizers.py",
            "old": "corrected_second = second_moment[index] / (1.0 - beta2**step) if bias_correction else second_moment[index]",
            "new": "corrected_second = second_moment[index]",
        },
    ],
    "no-adaptive-scaling": [
        {
            "file": "autoresearch/optimizers.py",
            "old": "weights[index] -= learning_rate * corrected_first / (math.sqrt(corrected_second) + epsilon)",
            "new": "weights[index] -= learning_rate * corrected_first",
        },
    ],
    "ademamix-without-slow-ema": [
        {
            "file": "autoresearch/optimizers.py",
            "old": "update = (exp_avg_fast[index] / bias_correction1 + alpha * exp_avg_slow[index]) / denom",
            "new": "update = (exp_avg_fast[index] / bias_correction1) / denom",
        },
    ],
}


def _run_repro(directory: Path) -> int:
    result = subprocess.run(
        [sys.executable, "scripts/repro.py"],
        cwd=str(directory),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return result.returncode


def _score_directory(directory: Path, expected_path: Path = None) -> Dict[str, Any]:
    """Run every suite in the copy and aggregate the verified-check count.

    Aggregating over suites (not just the main one) is what lets a control that only
    breaks a newer experiment still be detected.
    """
    exit_code = _run_repro(directory)
    failures: List[str] = []
    passed = 0
    total = 0
    for name, suite in SUITES.items():
        results_path = directory / suite["output"] / "results.json"
        suite_expected = directory / suite["expected"]
        if not results_path.exists():
            failures.append(f"{name}: no results.json produced")
            continue
        suite_failures, checks = verify(results_path, suite_expected)
        total += len(checks)
        passed += len(checks) - len(suite_failures)
        failures.extend(f"{name}: {item}" for item in suite_failures)
    return {
        "exit_code": exit_code,
        "checks_passed": passed,
        "checks_total": total,
        "score": round(100.0 * passed / total, 1) if total else 0.0,
        "failures": failures,
    }


def _mutate(directory: Path, mutations: List[Dict[str, str]]) -> None:
    for mutation in mutations:
        target = directory / mutation.get("file", "autoresearch/model.py")
        text = target.read_text(encoding="utf-8")
        if mutation["old"] not in text:
            raise SystemExit(f"control fragment not found in {mutation.get('file', 'autoresearch/model.py')}: {mutation['old']}")
        target.write_text(text.replace(mutation["old"], mutation["new"]), encoding="utf-8")


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Score a submission and check harness sensitivity")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--skip-controls", action="store_true", help="only score the current tree")
    args = parser.parse_args(argv)

    report: Dict[str, Any] = {"schema": "autoresearch-lite/task-score@1", "submission": {}, "controls": {}}

    with tempfile.TemporaryDirectory() as tmp:
        submission = Path(tmp) / "submission"
        shutil.copytree(ROOT, submission, ignore=_ignore)
        report["submission"] = _score_directory(submission, DEFAULT_EXPECTED)

        if not args.skip_controls:
            for name, mutations in NEGATIVE_CONTROLS.items():
                target = Path(tmp) / name
                shutil.copytree(ROOT, target, ignore=_ignore)
                _mutate(target, mutations)
                outcome = _score_directory(target, DEFAULT_EXPECTED)
                outcome["detected"] = outcome["exit_code"] != 0 and outcome["score"] < 100.0
                report["controls"][name] = outcome

    report["controls_all_detected"] = (
        all(item["detected"] for item in report["controls"].values()) if report["controls"] else None
    )
    report["passed"] = bool(
        report["submission"]["exit_code"] == 0
        and report["submission"]["score"] == 100.0
        and report["controls_all_detected"] in (True, None)
    )

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        sub = report["submission"]
        print(f"submission score: {sub['score']}/100 ({sub['checks_passed']}/{sub['checks_total']} checks, exit {sub['exit_code']})")
        for failure in sub["failures"]:
            print(f"  FAIL {failure}")
        for name, item in report["controls"].items():
            verdict = "detected" if item["detected"] else "MISSED"
            print(f"control[{name}]: {verdict} (score {item['score']}/100, exit {item['exit_code']})")
        print()
        print("TASK RESULT: PASS" if report["passed"] else "TASK RESULT: FAIL")
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
