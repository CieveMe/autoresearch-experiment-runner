#!/usr/bin/env python3
"""One-command, cross-platform reproduction entry point.

    python scripts/repro.py

It performs, in order:

1. environment report (interpreter, platform, config revision),
2. config validation,
3. the experiment run (baseline + adam + control variants),
4. verification of the produced numbers against ``expected/expected_metrics.json``,
5. the unit test suite.

Exit code 0 means: the artifacts were produced and every checked number is
inside tolerance. Any other outcome is a failure with a non-zero exit code,
so this script is safe to use as a CI gate, a reviewer check and an agent
scoring harness.
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.verify_results import DEFAULT_EXPECTED, verify  # noqa: E402
from autoresearch.runner import is_lower_is_better, rank_key  # noqa: E402

# Each suite is one experiment config plus the numbers it is expected to produce.
SUITES: Dict[str, Dict[str, str]] = {
    "main": {
        "config": "examples/classification.json",
        "output": "runs/demo",
        "expected": "expected/expected_metrics.json",
        "label": "Adam mechanism reproduction (fixed epoch budget)",
    },
    "optimizers": {
        "config": "examples/optimizers.json",
        "output": "runs/optimizers",
        "expected": "expected/expected_optimizers.json",
        "label": "optimizer convergence speed (tuned rates, tight target)",
    },
    "ademamix": {
        "config": "examples/ademamix.json",
        "output": "runs/ademamix",
        "expected": "expected/expected_ademamix.json",
        "label": "AdEMAMix (2024) against AdamW on time-to-target",
    },
    "optimizers-mlp": {
        "config": "examples/optimizers-mlp.json",
        "output": "runs/optimizers-mlp",
        "expected": "expected/expected_optimizers_mlp.json",
        "label": "optimizer family on the MLP trainer (does the ranking survive a bigger model?)",
    },
    "ademamix-mlp": {
        "config": "examples/ademamix-mlp.json",
        "output": "runs/ademamix-mlp",
        "expected": "expected/expected_ademamix_mlp.json",
        "label": "AdEMAMix on the MLP trainer (speed versus final quality)",
    },
    "schedule-free": {
        "config": "examples/schedule-free.json",
        "output": "runs/schedule-free",
        "expected": "expected/expected_schedule_free.json",
        "label": "Schedule-Free AdamW against a tuned cosine schedule (2024)",
    },
    "schedule-free-mlp": {
        "config": "examples/schedule-free-mlp.json",
        "output": "runs/schedule-free-mlp",
        "expected": "expected/expected_schedule_free_mlp.json",
        "label": "Schedule-Free AdamW against a tuned cosine schedule on the MLP",
    },
    "capacity-h32": {
        "config": "examples/capacity-h32.json",
        "output": "runs/capacity-h32",
        "expected": "expected/expected_capacity_h32.json",
        "label": "capacity check: do the three claim families survive 32 hidden units?",
        "tier": "capacity",
    },
    "capacity-h8x8": {
        "config": "examples/capacity-h8x8.json",
        "output": "runs/capacity-h8x8",
        "expected": "expected/expected_capacity_h8x8.json",
        "label": "capacity check: do they survive a second hidden layer?",
        "tier": "capacity",
    },
}

# Tiers exist to save local iteration time, never to hide coverage. Every report line that
# shows a score carries the tier and the suites it skipped, and CI runs the full tier on
# main and on tags (see .github/workflows/repro.yml and docs/release-checklist.md).
TIERS = ("core", "full")


def suites_for_tier(tier: str) -> List[str]:
    if tier == "full":
        return list(SUITES)
    if tier == "core":
        return [name for name, suite in SUITES.items() if suite.get("tier", "core") == "core"]
    raise ValueError(f"unknown tier: {tier} (available: {', '.join(TIERS)})")


def tier_label(tier: str, names: Sequence[str]) -> str:
    """A label that can never be mistaken for full coverage."""
    skipped = [name for name in SUITES if name not in names]
    if not skipped:
        return "tier=full (all suites)"
    return f"tier={tier}; NOT run: {', '.join(skipped)}"


def _header(title: str) -> None:
    print()
    print(f"=== {title} ===")


def _run(cmd: Sequence[str], quiet: bool = False) -> int:
    env = dict(os.environ)
    env["PYTHONPATH"] = str(ROOT)
    env.setdefault("PYTHONHASHSEED", "0")
    env.setdefault("PYTHONIOENCODING", "utf-8")
    print("$ " + " ".join(cmd))
    result = subprocess.run(
        list(cmd),
        cwd=str(ROOT),
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    output = (result.stdout or "").strip()
    if output and not quiet:
        print(output)
    return result.returncode


def _environment(config_path: Path) -> Dict[str, Any]:
    import autoresearch

    from autoresearch.runner import config_sha256

    info: Dict[str, Any] = {
        "python": sys.version.split()[0],
        "implementation": platform.python_implementation(),
        "platform": platform.platform(),
        "machine": platform.machine(),
        "autoresearch_lite": autoresearch.__version__,
        "config": str(config_path.relative_to(ROOT)),
        "config_sha256": config_sha256(config_path),
    }
    return info


def _print_result_table(results_path: Path) -> None:
    payload = json.loads(results_path.read_text(encoding="utf-8"))
    metric = payload["metric"]
    lower_is_better = is_lower_is_better(metric)
    rows = sorted(payload["results"], key=lambda item: rank_key(item, metric, lower_is_better))
    print("| trial | test_accuracy | test_loss | epochs | epochs_to_target | duration_ms |")
    print("|---|---:|---:|---:|---:|---:|")
    for item in rows:
        marker = " *" if item["name"] == payload["best"]["name"] else ""
        to_target = item.get("epochs_to_target")
        to_target = "not reached" if to_target is None else to_target
        print(
            f"| {item['name']}{marker} | {item['test_accuracy']:.2%} | "
            f"{item['test_loss']} | {item['epochs']} | {to_target} | {item['duration_ms']} |"
        )
    print(f"(* = best by `{metric}`)")


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Reproduce the AutoResearch Lite experiments")
    parser.add_argument("--suite", choices=["all", *SUITES.keys()], default="all",
                        help="which experiment suite(s) to run (default: all)")
    parser.add_argument("--tier", choices=list(TIERS), default="full",
                        help="`full` runs every suite; `core` skips the capacity suites to save "
                             "local iteration time. The summary always names the tier and what "
                             "was skipped, and CI runs full on main and tags.")
    parser.add_argument("--config", type=Path, default=None,
                        help="run a single ad-hoc config instead of the named suites")
    parser.add_argument("--output", type=Path, default=ROOT / "runs" / "ad-hoc")
    parser.add_argument("--expected", type=Path, default=DEFAULT_EXPECTED)
    parser.add_argument("--skip-tests", action="store_true", help="skip `python -m unittest`")
    args = parser.parse_args(argv)

    print("AutoResearch Lite - one-command reproduction")

    if args.config is not None:
        config_path = args.config if args.config.is_absolute() else (ROOT / args.config)
        output_dir = args.output if args.output.is_absolute() else (ROOT / args.output)
        expected_path = args.expected if args.expected.is_absolute() else (ROOT / args.expected)
        suites = [("ad-hoc", {"config": str(config_path), "output": str(output_dir),
                              "expected": str(expected_path), "label": "ad-hoc config"})]
    else:
        if args.suite == "all":
            names = suites_for_tier(args.tier)
        else:
            names = [args.suite]
        suites = [(name, SUITES[name]) for name in names]

    exit_code = 0
    verified_total = 0
    failures_total: List[str] = []

    for name, suite in suites:
        config_path = ROOT / suite["config"]
        output_dir = ROOT / suite["output"]
        expected_path = ROOT / suite["expected"]
        results_path = output_dir / "results.json"

        _header(f"suite `{name}` — {suite['label']}")
        print(f"config:   {suite['config']}")
        print(f"expected: {suite['expected']}")
        try:
            environment = _environment(config_path)
        except Exception as exc:  # pragma: no cover - defensive
            print(f"FAILED to read environment: {exc}")
            return 1
        for key, value in environment.items():
            print(f"  {key}: {value}")
        output_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / "environment.json").write_text(json.dumps(environment, indent=2) + "\n", encoding="utf-8")

        if _run([sys.executable, "-m", "autoresearch.cli", "validate-config", "--config", str(config_path)]) != 0:
            print("FAILED: config validation")
            return 1
        if _run([
            sys.executable, "-m", "autoresearch.cli", "run",
            "--config", str(config_path), "--output", str(output_dir),
        ]) != 0:
            print("FAILED: experiment run")
            return 1

        failures, checks = verify(results_path, expected_path)
        for line in checks:
            print(line)
        _print_result_table(results_path)
        verified_total += len(checks)
        if failures:
            failures_total.extend(failures)
            exit_code = 1
            print(f"FAILED: {len(failures)} expectation(s) not met in suite `{name}`")

    if not args.skip_tests:
        _header("unit tests")
        if _run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"]) != 0:
            print("FAILED: unit tests")
            exit_code = 1
    else:
        _header("unit tests (skipped)")

    _header("summary")
    print(tier_label(args.tier, [name for name, _ in suites]))
    for name, suite in suites:
        print(f"artifacts[{name}]: {suite['output']}")
    print(f"verified:  {verified_total} checks, {len(failures_total)} failures")
    print("RESULT: PASS" if exit_code == 0 else "RESULT: FAIL")
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
