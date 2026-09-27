#!/usr/bin/env python3
"""Compare an experiment result file against the expected reproduction numbers.

Usage:
    python scripts/verify_results.py --results runs/demo/results.json
    python scripts/verify_results.py --results runs/demo/results.json --json

Exit code is 0 only when every checked number is inside tolerance.
Timing fields are ignored on purpose: wall-clock duration is not reproducible.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EXPECTED = ROOT / "expected" / "expected_metrics.json"

# Fields that legitimately differ between runs or machines.
VOLATILE_KEYS = frozenset({"duration_ms"})


def _load(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise SystemExit(f"missing file: {path}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"invalid JSON in {path}: {exc}")


def _close(actual: float, expected: float, abs_tol: float, rel_tol: float) -> bool:
    return abs(float(actual) - float(expected)) <= max(abs_tol, rel_tol * abs(float(expected)))


def verify(results_path: Path, expected_path: Path) -> Tuple[List[str], List[str]]:
    """Return (failures, checks). Empty failures means the reproduction matched."""
    actual = _load(results_path)
    expected = _load(expected_path)
    tolerance = expected.get("tolerance", {})
    accuracy_tol = float(tolerance.get("accuracy_abs", 0.005))
    loss_abs = float(tolerance.get("loss_abs", 1e-6))
    loss_rel = float(tolerance.get("loss_rel", 1e-6))

    failures: List[str] = []
    checks: List[str] = []

    def check(label: str, ok: bool, detail: str) -> None:
        checks.append(f"{'PASS' if ok else 'FAIL'}  {label}: {detail}")
        if not ok:
            failures.append(f"{label}: {detail}")

    check(
        "config_sha256",
        actual.get("config_sha256") == expected["config_sha256"],
        f"expected {expected['config_sha256'][:12]}..., got {str(actual.get('config_sha256'))[:12]}...",
    )
    check(
        "metric",
        actual.get("metric") == expected["metric"],
        f"expected {expected['metric']}, got {actual.get('metric')}",
    )
    check(
        "best.name",
        actual.get("best", {}).get("name") == expected["best"],
        f"expected {expected['best']}, got {actual.get('best', {}).get('name')}",
    )
    for split in ("train_size", "test_size"):
        if split in expected.get("dataset", {}):
            check(
                f"dataset.{split}",
                actual.get("dataset", {}).get(split) == expected["dataset"][split],
                f"expected {expected['dataset'][split]}, got {actual.get('dataset', {}).get(split)}",
            )

    by_name = {item.get("name"): item for item in actual.get("results", [])}
    for name, want in expected.get("trials", {}).items():
        got = by_name.get(name)
        if got is None:
            checks.append(f"FAIL  trial[{name}]: missing from results.json")
            failures.append(f"trial[{name}] missing")
            continue
        check(
            f"trial[{name}].test_accuracy",
            _close(got.get("test_accuracy", -1), want["test_accuracy"], accuracy_tol, 0.0),
            f"expected {want['test_accuracy']}, got {got.get('test_accuracy')}",
        )
        check(
            f"trial[{name}].test_loss",
            _close(got.get("test_loss", -1), want["test_loss"], loss_abs, loss_rel),
            f"expected {want['test_loss']}, got {got.get('test_loss')}",
        )
        if "epochs" in want:
            check(
                f"trial[{name}].epochs",
                got.get("epochs") == want["epochs"],
                f"expected {want['epochs']}, got {got.get('epochs')}",
            )
    return failures, checks


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Verify reproduction numbers against expectations")
    parser.add_argument("--results", type=Path, default=ROOT / "runs" / "demo" / "results.json")
    parser.add_argument("--expected", type=Path, default=DEFAULT_EXPECTED)
    parser.add_argument("--json", action="store_true", help="print a machine-readable summary")
    args = parser.parse_args(argv)

    failures, checks = verify(args.results, args.expected)
    if args.json:
        print(json.dumps({"passed": not failures, "failures": failures, "checks": checks}, indent=2))
    else:
        for line in checks:
            print(line)
        print()
        print(f"verified {len(checks)} checks, {len(failures)} failure(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
