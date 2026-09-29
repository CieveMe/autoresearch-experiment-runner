#!/usr/bin/env python3
"""How much does one ULP of `libm` move each arm? A local stand-in for a second platform.

The pinned expectations are compared with a tolerance of 1e-6, and on Linux one arm — `schedule_free_adamw`
— missed it by up to 2.0e-4 while every other arm in every suite reproduced to the last printed decimal.
That is not "CI magic": it is what happens when a trajectory has a positive divergence rate, so the
last-bit differences between two `libm` builds (Windows MSVCRT vs glibc) are amplified over the run.

This probe measures that amplification without needing a second machine. It runs the arms of a suite
twice — once normally, once with `math.exp`/`sqrt`/`tanh`/`erf` each nudged one ULP upward — and reports
how far the final test loss moves. One ULP is the smallest difference a different libm can introduce, so
the numbers here are a lower bound on the cross-platform spread, and they are what the tolerance fix in
`expected/*.json` is justified with.

Usage:
    python scripts/perturbation_probe.py --suite schedule-free-mlp --suite capacity-h32
    python scripts/perturbation_probe.py --suite norm-layernorm --json
"""

from __future__ import annotations

import argparse
import json
import math
import statistics
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.repro import SUITES  # noqa: E402

_ORIGINALS = {name: getattr(math, name) for name in ("exp", "sqrt", "tanh", "erf")}


def _install_perturbation() -> None:
    for name, original in _ORIGINALS.items():
        setattr(math, name, lambda value, _original=original: math.nextafter(_original(value), math.inf))


def _remove_perturbation() -> None:
    for name, original in _ORIGINALS.items():
        setattr(math, name, original)


def _run_suite(suite: str) -> Dict[str, Any]:
    """Run one suite in a throwaway output directory and return its curves."""
    from autoresearch.runner import run as run_experiment

    suite_config = SUITES[suite]
    config_path = ROOT / suite_config["config"]
    with tempfile.TemporaryDirectory(prefix="perturbation-probe-") as temporary:
        output = Path(temporary) / "run"
        payload = run_experiment(config_path, output)
    return payload


def probe_suite(suite: str) -> Dict[str, Any]:
    clean = _run_suite(suite)
    _install_perturbation()
    try:
        perturbed = _run_suite(suite)
    finally:
        _remove_perturbation()
    clean_arms = {item["name"]: item for item in clean["results"]}
    rows = []
    for item in perturbed["results"]:
        name = item["name"]
        reference = clean_arms[name]
        curves = zip(reference.get("loss_curve") or [], item.get("loss_curve") or [])
        per_epoch = [abs(a - b) for a, b in curves]
        first = next((index + 1 for index, value in enumerate(per_epoch) if value > 1e-9), None)
        rows.append({
            "arm": name,
            "delta_test_loss": item["test_loss"] - reference["test_loss"],
            "delta_epochs": item["epochs"] - reference["epochs"],
            "max_curve_delta": max(per_epoch) if per_epoch else 0.0,
            "first_visible_epoch": first,
            "within_pinned_tolerance": abs(item["test_loss"] - reference["test_loss"]) <= 1e-6,
        })
    rows.sort(key=lambda row: -abs(row["delta_test_loss"]))
    return {"suite": suite, "metric": clean["metric"], "arms": rows}


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Measure one-ULP sensitivity per arm")
    parser.add_argument("--suite", action="append", default=[],
                        help="suite name from scripts/repro.py (default: the ones with schedule-free arms)")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    suites = args.suite or ["schedule-free", "schedule-free-mlp", "capacity-h32", "norm-layernorm"]
    report: List[Dict[str, Any]] = []
    for suite in suites:
        result = probe_suite(suite)
        report.append(result)
        print(f"== {suite}")
        print(f"   {'arm':<22} {'delta test_loss':>16} {'max curve delta':>16} {'first visible':>14} {'within 1e-6':>12}")
        for row in result["arms"]:
            print(f"   {row['arm']:<22} {row['delta_test_loss']:>+16.3e} {row['max_curve_delta']:>16.3e} "
                  f"{str(row['first_visible_epoch']):>14} {str(row['within_pinned_tolerance']):>12}")
    worst = max((abs(row["delta_test_loss"]) for suite in report for row in suite["arms"]), default=0.0)
    print(f"\nlargest movement from one ULP across all probed arms: {worst:.3e}")
    if args.json:
        print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
