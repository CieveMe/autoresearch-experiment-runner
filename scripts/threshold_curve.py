#!/usr/bin/env python3
"""Turn single-point `epochs_to_target` numbers into curves over the target itself.

The speed metric is a function of the threshold it is measured at, and two models can give
opposite answers at one threshold and the same answer at another. A single number hides
that; this script reads the committed loss curves and reports, for a grid of thresholds,
which arm is fastest and which never arrives — plus an SVG so the crossing point is visible.

Usage:
    python scripts/threshold_curve.py --suite schedule-free --suite schedule-free-mlp
    python scripts/threshold_curve.py --results runs/demo/results.json --output runs/thresholds

Outputs per suite, in the output directory: `<suite>-thresholds.csv`, `<suite>-thresholds.md`
and `<suite>-curves.svg`. Nothing here re-trains anything, so it is cheap and deterministic.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from autoresearch.metrics import epochs_to_target  # noqa: E402
from scripts.repro import SUITES  # noqa: E402

COLORS = ["#1f77b4", "#d62728", "#2ca02c", "#9467bd", "#ff7f0e", "#8c564b", "#17becf", "#e377c2"]


def load_results(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def threshold_grid(payload: Dict[str, Any], steps: int) -> List[float]:
    """From the best converged floor to the worst arm's own floor, evenly spaced.

    Those two ends bracket the region where the threshold is informative: at the tight end
    only the arm that converges deepest can arrive at all, and beyond the loose end every
    arm arrives within a few epochs and the metric is measuring the first step.
    """
    curves = [row["loss_curve"] for row in payload["results"] if row.get("loss_curve")]
    if not curves:
        raise ValueError(f"{payload['task']}: no loss curves in results.json")
    best_floor = min(min(curve) for curve in curves)
    loose = max(curve[-1] for curve in curves)
    tight = best_floor
    if loose <= tight:
        loose = tight * 1.05
    return [tight + (loose - tight) * index / (steps - 1) for index in range(steps)]


def table(payload: Dict[str, Any], thresholds: Sequence[float]) -> Dict[str, List[Optional[int]]]:
    out: Dict[str, List[Optional[int]]] = {}
    for row in payload["results"]:
        curve = row.get("loss_curve") or []
        out[row["name"]] = [epochs_to_target(curve, value) for value in thresholds]
    return out


def markdown(payload: Dict[str, Any], thresholds: Sequence[float], curves: Dict[str, List[Optional[int]]]) -> str:
    names = list(curves)
    lines = [
        f"# Threshold curve — `{payload['task']}`",
        "",
        f"Trainer: `{payload.get('trainer', 'logistic')}` · metric: epochs until the training loss reaches the row's threshold.",
        "`never` means the arm did not reach that threshold inside the budget.",
        "",
        "| threshold | " + " | ".join(names) + " | fastest |",
        "|---:|" + "---:|" * len(names) + "---|",
    ]
    for index, value in enumerate(thresholds):
        row = [curves[name][index] for name in names]
        reached = [(epoch, name) for epoch, name in zip(row, names) if epoch is not None]
        fastest = min(reached)[1] if reached else "never reached"
        cells = " | ".join("never" if epoch is None else str(epoch) for epoch in row)
        lines.append(f"| {value:.4f} | {cells} | {fastest} |")
    lines.append("")
    # where does the ranking change?
    winners: List[str] = []
    for index in range(len(thresholds)):
        reached = [
            (curves[name][index], name) for name in names if curves[name][index] is not None
        ]
        winners.append(min(reached)[1] if reached else "none")
    changes = [
        (thresholds[index], winners[index - 1], winners[index])
        for index in range(1, len(winners))
        if winners[index] != winners[index - 1]
    ]
    nominal = payload.get("target_loss")
    lines.append("## Reading")
    lines.append("")
    if changes:
        lines.append("The fastest arm changes with the threshold:")
        lines.append("")
        for value, before, after in changes:
            lines.append(f"- near **{value:.4f}**: `{before}` gives way to `{after}`")
    else:
        lines.append(f"The fastest arm is `{winners[0]}` at every threshold on this grid.")
    if nominal is not None:
        lines.append("")
        lines.append(f"The suite's pinned threshold is **{nominal}** — read its row above, not just the headline number.")
    lines.append("")
    return "\n".join(lines)


def svg(payload: Dict[str, Any], thresholds: Sequence[float], curves: Dict[str, List[Optional[int]]]) -> str:
    """Hand-rolled SVG (no dependencies): x = epochs, y = threshold, one line per arm."""
    width, height = 900, 420
    left, right, top, bottom = 150, 30, 40, 50
    plot_w = width - left - right
    plot_h = height - top - bottom
    max_epochs = max(
        (epoch for row in curves.values() for epoch in row if epoch is not None), default=1
    )
    lo, hi = min(thresholds), max(thresholds)

    def x_of(epoch: int) -> float:
        return left + plot_w * (epoch / max_epochs)

    def y_of(value: float) -> float:
        return top + plot_h * (1.0 - (value - lo) / (hi - lo))

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" font-family="system-ui, sans-serif" font-size="12">',
        f'<rect width="{width}" height="{height}" fill="white"/>',
        f'<text x="{left}" y="22" font-size="14">{payload["task"]} — epochs to reach each threshold</text>',
        f'<line x1="{left}" y1="{top + plot_h}" x2="{left + plot_w}" y2="{top + plot_h}" stroke="#333"/>',
        f'<line x1="{left}" y1="{top}" x2="{left}" y2="{top + plot_h}" stroke="#333"/>',
    ]
    for step in range(0, 6):
        value = lo + (hi - lo) * step / 5
        y = y_of(value)
        parts.append(f'<line x1="{left}" y1="{y:.1f}" x2="{left + plot_w}" y2="{y:.1f}" stroke="#eee"/>')
        parts.append(f'<text x="{left - 8}" y="{y + 4:.1f}" text-anchor="end">{value:.3f}</text>')
    for step in range(0, 6):
        epoch = round(max_epochs * step / 5)
        x = x_of(epoch)
        parts.append(f'<line x1="{x:.1f}" y1="{top + plot_h}" x2="{x:.1f}" y2="{top + plot_h + 5}" stroke="#333"/>')
        parts.append(f'<text x="{x:.1f}" y="{top + plot_h + 20}" text-anchor="middle">{epoch}</text>')
    parts.append(f'<text x="{left + plot_w / 2:.0f}" y="{height - 8}" text-anchor="middle">epochs to reach the threshold</text>')
    nominal = payload.get("target_loss")
    if nominal is not None and lo <= nominal <= hi:
        y = y_of(nominal)
        parts.append(f'<line x1="{left}" y1="{y:.1f}" x2="{left + plot_w}" y2="{y:.1f}" stroke="#999" stroke-dasharray="6 4"/>')
        parts.append(f'<text x="{left + plot_w - 4}" y="{y - 4:.1f}" text-anchor="end" fill="#666">pinned target {nominal}</text>')
    for index, (name, row) in enumerate(curves.items()):
        color = COLORS[index % len(COLORS)]
        points = [
            (x_of(epoch), y_of(thresholds[position]))
            for position, epoch in enumerate(row)
            if epoch is not None
        ]
        if len(points) >= 2:
            path = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
            parts.append(f'<polyline points="{path}" fill="none" stroke="{color}" stroke-width="2"/>')
        for x, y in points:
            parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2" fill="{color}"/>')
        legend_y = top + 6 + index * 18
        parts.append(f'<line x1="14" y1="{legend_y}" x2="34" y2="{legend_y}" stroke="{color}" stroke-width="3"/>')
        parts.append(f'<text x="40" y="{legend_y + 4}">{name}</text>')
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def write_suite(payload: Dict[str, Any], name: str, output: Path, steps: int) -> Dict[str, Any]:
    thresholds = threshold_grid(payload, steps)
    curves = table(payload, thresholds)
    output.mkdir(parents=True, exist_ok=True)
    (output / f"{name}-thresholds.md").write_text(markdown(payload, thresholds, curves), encoding="utf-8")
    (output / f"{name}-curves.svg").write_text(svg(payload, thresholds, curves), encoding="utf-8")
    with (output / f"{name}-thresholds.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["threshold", *curves.keys()])
        for index, value in enumerate(thresholds):
            writer.writerow([f"{value:.6f}", *["" if curves[arm][index] is None else curves[arm][index] for arm in curves]])
    return {"suite": name, "thresholds": thresholds, "curves": curves, "task": payload["task"]}


def summary(results: List[Dict[str, Any]]) -> str:
    lines = [
        "# Threshold curves — where does the speed ranking hold?",
        "",
        "Each suite is read from its committed loss curves; no experiment was re-run to produce this.",
        "`epochs_to_target` is a function of the threshold, so a single number is a slice, not a fact.",
        "",
        "| suite | fastest arm at the tight end | fastest at the loose end | ranking changes |",
        "|---|---|---|---|",
    ]
    for item in results:
        curves, thresholds = item["curves"], item["thresholds"]
        winners: List[str] = []
        for index in range(len(thresholds)):
            reached = [(row[index], name) for name, row in curves.items() if row[index] is not None]
            winners.append(min(reached)[1] if reached else "none")
        changes = sum(1 for index in range(1, len(winners)) if winners[index] != winners[index - 1])
        lines.append(
            f"| `{item['suite']}` | `{winners[0]}` | `{winners[-1]}` | {changes} |"
        )
    lines.append("")
    return "\n".join(lines)


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Curves of epochs-to-target over thresholds")
    parser.add_argument("--suite", action="append", default=[], help="suite name from scripts/repro.py")
    parser.add_argument("--results", action="append", default=[], type=Path, help="explicit results.json")
    parser.add_argument("--output", type=Path, default=ROOT / "runs" / "threshold-curves")
    parser.add_argument("--steps", type=int, default=13, help="number of thresholds on the grid")
    args = parser.parse_args(argv)

    output = args.output if args.output.is_absolute() else (ROOT / args.output)
    items: List[Dict[str, Any]] = []
    for name in args.suite:
        if name not in SUITES:
            raise SystemExit(f"unknown suite: {name} (available: {', '.join(SUITES)})")
        path = ROOT / SUITES[name]["output"] / "results.json"
        if not path.exists():
            raise SystemExit(f"missing {path}; run `python scripts/repro.py --suite {name}` first")
        items.append(write_suite(load_results(path), name, output, args.steps))
    for path in args.results:
        resolved = path if path.is_absolute() else (ROOT / path)
        items.append(write_suite(load_results(resolved), resolved.parent.name, output, args.steps))
    if not items:
        raise SystemExit("nothing to do: pass --suite and/or --results")

    (output / "SUMMARY.md").write_text(summary(items), encoding="utf-8")
    for item in items:
        print(f"{item['suite']:<22} thresholds {item['thresholds'][0]:.4f}..{item['thresholds'][-1]:.4f}")
    print(f"summary: {output / 'SUMMARY.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
