#!/usr/bin/env python3
"""Re-run one experiment config across several seeds and aggregate the outcome.

A single seed can only show that a run is repeatable. A seed sweep shows whether
the *conclusion* is repeatable, which is what a reproduction claim needs.

Usage:
    python scripts/seed_sweep.py --config examples/classification.json --seeds 0-9
    python scripts/seed_sweep.py --seeds 0,1,2,7 --output runs/seed-sweep

Outputs, inside the output directory:
    seed-<n>/results.json, seed-<n>/report.md   per-seed artifacts (config copies included)
    summary.json                                machine-readable aggregate
    summary.md                                  table for the reproduction report
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from pathlib import Path
from typing import Any, Dict, List, Sequence

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from autoresearch.runner import config_sha256, is_lower_is_better, rank_key, run  # noqa: E402

INF = float("inf")


def _metric_or_inf(value):
    """``None`` means "never reached the target", which must rank last."""
    return INF if value is None else value


def parse_seeds(spec: str) -> List[int]:
    """Accept ``0-9``, ``0,1,2`` or a mixture such as ``0-2,7,9``."""
    seeds: List[int] = []
    for chunk in spec.replace(" ", "").split(","):
        if not chunk:
            continue
        if "-" in chunk:
            start_text, _, end_text = chunk.partition("-")
            start, end = int(start_text), int(end_text)
            if end < start:
                raise ValueError(f"invalid seed range: {chunk}")
            seeds.extend(range(start, end + 1))
        else:
            seeds.append(int(chunk))
    if not seeds:
        raise ValueError("no seeds given")
    return sorted(set(seeds))


def _aggregate(
    payloads: Sequence[Dict[str, Any]],
    metric: str,
    config_path: Path,
    references: Sequence[str] = ("baseline",),
) -> Dict[str, Any]:
    lower_is_better = is_lower_is_better(metric)
    names: List[str] = []
    for payload in payloads:
        for item in payload["results"]:
            if item["name"] not in names:
                names.append(item["name"])

    trials: Dict[str, Any] = {}
    for name in names:
        rows = [next(item for item in payload["results"] if item["name"] == name) for payload in payloads]
        raw_metrics = [row[metric] for row in rows]
        metrics = [value for value in raw_metrics if value is not None]
        accuracies = [row["test_accuracy"] for row in rows]
        trials[name] = {
            "optimizer": rows[0]["config"].get("optimizer"),
            "learning_rate": rows[0]["config"].get("learning_rate"),
            "weight_decay": rows[0]["config"].get("weight_decay", 0.0),
            "epochs": rows[0]["config"].get("epochs"),
            "reached_in": len(metrics),
            "metric_mean": round(statistics.fmean(metrics), 8) if metrics else None,
            "metric_stdev": round(statistics.stdev(metrics), 8) if len(metrics) > 1 else 0.0,
            "metric_min": min(metrics) if metrics else None,
            "metric_max": max(metrics) if metrics else None,
            "test_accuracy_mean": round(statistics.fmean(accuracies), 6),
            "test_accuracy_stdev": round(statistics.stdev(accuracies), 6) if len(accuracies) > 1 else 0.0,
            "wins": 0,
        }

    for payload in payloads:
        ranked = sorted(
            payload["results"],
            key=lambda item: rank_key(item, metric, lower_is_better),
        )
        trials[ranked[0]["name"]]["wins"] += 1

    seed_count = len(payloads)
    for name, summary in trials.items():
        summary["win_rate"] = round(summary["wins"] / seed_count, 4) if seed_count else 0.0

    # Seeds are paired: the same seed drives every trial, so the per-seed
    # difference is a stronger signal than comparing means with overlapping
    # spreads. Positive difference always means "better than the reference".
    paired: Dict[str, Any] = {}
    sign = 1.0 if lower_is_better else -1.0
    for reference in references:
        if reference not in trials:
            continue
        reference_metric = [
            next(row[metric] for row in payload["results"] if row["name"] == reference) for payload in payloads
        ]
        per_trial: Dict[str, Any] = {}
        for name in names:
            if name == reference:
                continue
            diffs = []
            incomparable = 0
            for index, payload in enumerate(payloads):
                value = next(row[metric] for row in payload["results"] if row["name"] == name)
                baseline_value = reference_metric[index]
                if value is None or baseline_value is None:
                    incomparable += 1
                    continue
                diffs.append(sign * (baseline_value - value))
            per_trial[name] = {
                "better_in": sum(1 for value in diffs if value > 0),
                "worse_in": sum(1 for value in diffs if value < 0),
                "incomparable": incomparable,
                "mean_improvement": round(statistics.fmean(diffs), 8) if diffs else None,
                "stdev_improvement": round(statistics.stdev(diffs), 8) if len(diffs) > 1 else 0.0,
                "min_improvement": min(diffs) if diffs else None,
                "max_improvement": max(diffs) if diffs else None,
            }
        paired[reference] = per_trial

    return {
        "schema": "autoresearch-lite/seed-sweep@1",
        "metric": metric,
        "seeds": [payload["seed"] for payload in payloads],
        "seed_count": seed_count,
        "base_config": str(config_path.relative_to(ROOT)) if config_path.is_relative_to(ROOT) else str(config_path),
        "base_config_sha256": config_sha256(config_path),
        "seed_config_sha256": {
            f"seed-{payload['seed']}": payload["config_sha256"] for payload in payloads
        },
        "paper": payloads[0].get("paper", {}),
        "trials": trials,
        "paired_improvement": paired,
    }


def _markdown(summary: Dict[str, Any]) -> str:
    metric = summary["metric"]
    lines = [
        f"# Seed sweep summary ({summary['seed_count']} seeds: {summary['seeds']})",
        "",
        f"- metric: `{metric}` (lower is better)",
        f"- base config: `{summary['base_config']}` (SHA-256 `{summary['base_config_sha256']}`)",
        "- per-seed config copies are written next to each run and hashed in `summary.json`",
        "",
        f"| trial | {metric} mean | {metric} stdev | min | max | reached | test_accuracy mean | wins | win rate |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    ordered = sorted(summary["trials"].items(), key=lambda pair: _metric_or_inf(pair[1]["metric_mean"]))
    for name, row in ordered:
        lines.append(
            f"| {name} | {row['metric_mean']} | {row['metric_stdev']} | {row['metric_min']} | "
            f"{row['metric_max']} | {row.get('reached_in', summary['seed_count'])}/{summary['seed_count']} | "
            f"{row['test_accuracy_mean']:.2%} | {row['wins']}/{summary['seed_count']} | "
            f"{row['win_rate']:.0%} |"
        )
    for reference, per_trial in (summary.get("paired_improvement") or {}).items():
        lines.extend([
            "",
            f"Paired per-seed improvement over `{reference}` (positive = better `{metric}`):",
            "",
            "| trial | better in | worse in | incomparable | mean improvement | stdev | min | max |",
            "|---|---:|---:|---:|---:|---:|---:|---:|",
        ])
        for name, row in sorted(
            per_trial.items(),
            key=lambda pair: (
                pair[1]["mean_improvement"] is None,
                -_metric_or_inf(pair[1]["mean_improvement"]),
            ),
        ):
            lines.append(
                f"| {name} | {row['better_in']}/{summary['seed_count']} | {row['worse_in']} | "
                f"{row['incomparable']} | {row['mean_improvement']} | {row['stdev_improvement']} | "
                f"{row['min_improvement']} | {row['max_improvement']} |"
            )
    lines.append("")
    return "\n".join(lines)


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Aggregate one config across several seeds")
    parser.add_argument("--config", type=Path, default=ROOT / "examples" / "classification.json")
    parser.add_argument("--seeds", default="0-9", help="seed list, e.g. 0-9 or 0,1,2,7")
    parser.add_argument("--output", type=Path, default=ROOT / "runs" / "seed-sweep")
    parser.add_argument("--metric", default=None, help="override the metric from the config")
    parser.add_argument(
        "--reference",
        default="baseline,sgd_control",
        help="comma-separated trial names used for paired per-seed comparisons",
    )
    args = parser.parse_args(argv)

    config_path = args.config if args.config.is_absolute() else (ROOT / args.config)
    output_dir = args.output if args.output.is_absolute() else (ROOT / args.output)
    seeds = parse_seeds(args.seeds)
    base_config = json.loads(config_path.read_text(encoding="utf-8"))
    metric = args.metric or str(base_config.get("metric", "test_accuracy"))

    payloads: List[Dict[str, Any]] = []
    for seed in seeds:
        seed_config = dict(base_config)
        seed_config["seed"] = seed
        seed_dir = output_dir / f"seed-{seed}"
        seed_dir.mkdir(parents=True, exist_ok=True)
        seed_config_path = seed_dir / "config.json"
        seed_config_path.write_text(json.dumps(seed_config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        payload = run(seed_config_path, seed_dir)
        payload["seed"] = seed
        payloads.append(payload)
        print(
            f"seed {seed:>3}: best={payload['best']['name']:<18} "
            f"{metric}={payload['best'][metric]}"
        )

    references = [item.strip() for item in args.reference.split(",") if item.strip()]
    summary = _aggregate(payloads, metric, config_path, references)
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (output_dir / "summary.md").write_text(_markdown(summary), encoding="utf-8")
    print()
    print(_markdown(summary))
    print(f"summary: {output_dir / 'summary.md'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
