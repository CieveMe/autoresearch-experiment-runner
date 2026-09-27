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
from typing import Any, Dict, List, Sequence

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.verify_results import DEFAULT_EXPECTED, verify  # noqa: E402


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
    lower_is_better = metric in {"test_loss", "train_loss", "duration_ms", "epochs"}
    rows = sorted(
        payload["results"],
        key=lambda item: ((1 if lower_is_better else -1) * item[metric], item["test_loss"]),
    )
    print(f"| trial | test_accuracy | test_loss | epochs | duration_ms |")
    print("|---|---:|---:|---:|---:|")
    for item in rows:
        marker = " *" if item["name"] == payload["best"]["name"] else ""
        print(
            f"| {item['name']}{marker} | {item['test_accuracy']:.2%} | "
            f"{item['test_loss']} | {item['epochs']} | {item['duration_ms']} |"
        )
    print(f"(* = best by `{metric}`)")


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Reproduce the AutoResearch Lite experiments")
    parser.add_argument("--config", type=Path, default=ROOT / "examples" / "classification.json")
    parser.add_argument("--output", type=Path, default=ROOT / "runs" / "demo")
    parser.add_argument("--expected", type=Path, default=DEFAULT_EXPECTED)
    parser.add_argument("--skip-tests", action="store_true", help="skip `python -m unittest`")
    parser.add_argument("--env-report", type=Path, default=None, help="where to write environment.json")
    args = parser.parse_args(argv)

    config_path = args.config if args.config.is_absolute() else (ROOT / args.config)
    output_dir = args.output if args.output.is_absolute() else (ROOT / args.output)
    expected_path = args.expected if args.expected.is_absolute() else (ROOT / args.expected)
    results_path = output_dir / "results.json"

    print("AutoResearch Lite - one-command reproduction")
    _header("environment")
    try:
        environment = _environment(config_path)
    except Exception as exc:  # pragma: no cover - defensive
        print(f"FAILED to read environment: {exc}")
        return 1
    for key, value in environment.items():
        print(f"{key}: {value}")
    env_report = args.env_report or (output_dir / "environment.json")
    env_report.parent.mkdir(parents=True, exist_ok=True)
    env_report.write_text(json.dumps(environment, indent=2) + "\n", encoding="utf-8")

    _header("step 1/4 validate config")
    if _run([sys.executable, "-m", "autoresearch.cli", "validate-config", "--config", str(config_path)]) != 0:
        print("FAILED: config validation")
        return 1

    _header("step 2/4 run experiments")
    if _run([
        sys.executable, "-m", "autoresearch.cli", "run",
        "--config", str(config_path), "--output", str(output_dir),
    ]) != 0:
        print("FAILED: experiment run")
        return 1

    _header("step 3/4 verify numbers against expectations")
    print(f"expected file: {expected_path.relative_to(ROOT) if expected_path.is_relative_to(ROOT) else expected_path}")
    failures, checks = verify(results_path, expected_path)
    for line in checks:
        print(line)
    _print_result_table(results_path)
    if failures:
        print()
        print(f"FAILED: {len(failures)} expectation(s) not met")
        return 1

    exit_code = 0
    if not args.skip_tests:
        _header("step 4/4 unit tests")
        if _run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"]) != 0:
            print("FAILED: unit tests")
            exit_code = 1
    else:
        _header("step 4/4 unit tests (skipped)")

    _header("summary")
    print(f"artifacts: {output_dir}")
    print(f"report:    {output_dir / 'report.md'}")
    print(f"verified:  {len(checks)} checks, {len(failures)} failures")
    print("RESULT: PASS" if exit_code == 0 else "RESULT: FAIL")
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
