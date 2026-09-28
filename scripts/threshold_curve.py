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
        fastest = _winner_label(reached)
        cells = " | ".join("never" if epoch is None else str(epoch) for epoch in row)
        lines.append(f"| {value:.4f} | {cells} | {fastest} |")
    lines.append("")
    # where does the ranking change?
    winners: List[str] = []
    for index in range(len(thresholds)):
        reached = [
            (curves[name][index], name) for name in names if curves[name][index] is not None
        ]
        winners.append(_winner_label(reached))
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


def _strict_winner(reached: Sequence) -> Optional[str]:
    """The single fastest arm, or None when the fastest epoch is shared.

    Ties are common here (two arms can reach a threshold on exactly the same epoch), and
    resolving them alphabetically would invent a ranking out of a sort order. Callers must
    treat None as "tied", not as "unknown".
    """
    if not reached:
        return None
    best = min(epoch for epoch, _ in reached)
    tied = [name for epoch, name in reached if epoch == best]
    return tied[0] if len(tied) == 1 else None


def _winner_label(reached: Sequence) -> str:
    if not reached:
        return "never reached"
    best = min(epoch for epoch, _ in reached)
    tied = sorted(name for epoch, name in reached if epoch == best)
    if len(tied) == 1:
        return tied[0]
    return "tie: " + ", ".join(tied)


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


def crossing_threshold(
    payload: Dict[str, Any], first: str, second: str, steps: int = 40
) -> Optional[float]:
    """The threshold where the *strict* winner between two arms flips (None if it never does).

    Found on a fine grid over the region that is informative for this seed, so that "there is a
    crossing" becomes "the crossing is at T", which is the statement a conclusion can carry.
    Thresholds where the two arms tie are skipped rather than broken by name: a tied band is not
    evidence of a crossing, and letting a sort order decide it is how a fake ranking gets made.
    """
    curves = {row["name"]: row.get("loss_curve") or [] for row in payload["results"]}
    if first not in curves or second not in curves or not curves[first] or not curves[second]:
        return None
    grid = threshold_grid(payload, steps)
    last_strict_winner = None
    last_strict_threshold = None
    for index, value in enumerate(grid):
        first_epoch = epochs_to_target(curves[first], value)
        second_epoch = epochs_to_target(curves[second], value)
        if first_epoch is None and second_epoch is None:
            continue
        if first_epoch is None:
            winner = second
        elif second_epoch is None:
            winner = first
        else:
            winner = first if first_epoch < second_epoch else (second if second_epoch < first_epoch else None)
        if winner is None:
            continue
        if last_strict_winner is not None and winner != last_strict_winner:
            return round((value + last_strict_threshold) / 2.0, 6)
        last_strict_winner = winner
        last_strict_threshold = value
    return None


def tied_band(
    payload: Dict[str, Any], first: str, second: str, steps: int = 40
) -> Optional[float]:
    """Width of the threshold band where the two arms reach the target on the same epoch."""
    curves = {row["name"]: row.get("loss_curve") or [] for row in payload["results"]}
    if first not in curves or second not in curves:
        return None
    grid = threshold_grid(payload, steps)
    tied = 0
    for value in grid:
        first_epoch = epochs_to_target(curves[first], value)
        second_epoch = epochs_to_target(curves[second], value)
        if first_epoch is None or second_epoch is None:
            continue
        if first_epoch == second_epoch:
            tied += 1
    if not grid:
        return None
    return round((grid[-1] - grid[0]) * tied / len(grid), 6)


def crossing_stability(
    seed_payloads: Sequence[Dict[str, Any]],
    first: str,
    second: str,
    pinned: Optional[float],
    steps: int = 40,
) -> Dict[str, Any]:
    """How stable is the crossing, and is the pinned threshold on the same side every time?"""
    crossings = [crossing_threshold(payload, first, second, steps) for payload in seed_payloads]
    found = [value for value in crossings if value is not None]
    pinned_winner: List[str] = []
    if pinned is not None:
        for payload in seed_payloads:
            curves = {row["name"]: row.get("loss_curve") or [] for row in payload["results"]}
            first_epoch = epochs_to_target(curves[first], pinned)
            second_epoch = epochs_to_target(curves[second], pinned)
            if first_epoch is None and second_epoch is None:
                pinned_winner.append("neither")
            elif first_epoch is None:
                pinned_winner.append(second)
            elif second_epoch is None:
                pinned_winner.append(first)
            elif first_epoch == second_epoch:
                pinned_winner.append("tie")
            else:
                pinned_winner.append(first if first_epoch <= second_epoch else second)
    return {
        "pair": [first, second],
        "seeds": len(seed_payloads),
        "crossings_found": len(found),
        "crossing_mean": round(sum(found) / len(found), 6) if found else None,
        "crossing_min": min(found) if found else None,
        "crossing_max": max(found) if found else None,
        "crossing_spread": round(max(found) - min(found), 6) if found else None,
        "crossing_values": crossings,
        "pinned_threshold": pinned,
        "pinned_winners": pinned_winner,
        "pinned_consistent": len(set(pinned_winner)) == 1 if pinned_winner else None,
        "pinned_winner": pinned_winner[0] if pinned_winner and len(set(pinned_winner)) == 1 else None,
    }


def stability_markdown(suite: str, result: Dict[str, Any]) -> str:
    first, second = result["pair"]
    lines = [
        f"# Crossing stability — `{suite}` ({first} vs {second})",
        "",
        f"Crossings located in **{result['crossings_found']} of {result['seeds']} seeds**"
        + (
            f", at {result['crossing_mean']} on average "
            f"(min {result['crossing_min']}, max {result['crossing_max']}, spread {result['crossing_spread']})."
            if result["crossings_found"]
            else " — no seed showed the two arms swapping the lead on this grid."
        ),
        "",
    ]
    if result["pinned_threshold"] is not None:
        lines += [
            f"At the suite's pinned threshold ({result['pinned_threshold']}), the faster arm per seed was:",
            "",
            "| seed | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |",
            "|---|---|---|---|---|---|---|---|---|---|---|",
            "| faster | " + " | ".join(result["pinned_winners"]) + " |",
            "",
            f"**{'Consistent' if result['pinned_consistent'] else 'Not consistent'}**: "
            + (
                f"`{result['pinned_winner']}` is faster at the pinned threshold in every seed."
                if result["pinned_consistent"]
                else "the winner at the pinned threshold changes between seeds, so a single-seed "
                "statement about that threshold would not survive the sweep."
            ),
            "",
        ]
    lines += [
        "Per-seed crossing values:",
        "",
        "| seed | crossing |",
        "|---:|---|",
    ]
    for seed, value in enumerate(result["crossing_values"]):
        lines.append(f"| {seed} | {'none' if value is None else value} |")
    lines.append("")
    return "\n".join(lines)


def summary(results: List[Dict[str, Any]]) -> str:
    lines = [
        "# Threshold curves — where does the speed ranking hold?",
        "",
        "Each suite is read from its committed loss curves; no experiment was re-run to produce this.",
        "`epochs_to_target` is a function of the threshold, so a single number is a slice, not a fact.",
        "",
        "| suite | fastest arm at the tight end | fastest at the loose end | ranking changes (strict) | tied thresholds |",
        "|---|---|---|---:|---:|",
    ]
    for item in results:
        curves, thresholds = item["curves"], item["thresholds"]
        winners: List[str] = []
        for index in range(len(thresholds)):
            reached = [(row[index], name) for name, row in curves.items() if row[index] is not None]
            winners.append(_winner_label(reached))
        # Count only changes between *strict* winners; a tie is neither a winner nor a change.
        strict = [winner for winner in winners if winner not in ("never reached",) and not winner.startswith("tie:")]
        changes = sum(1 for index in range(1, len(strict)) if strict[index] != strict[index - 1])
        ties = sum(1 for winner in winners if winner.startswith("tie:"))
        lines.append(
            f"| `{item['suite']}` | `{winners[0]}` | `{winners[-1]}` | {changes} | {ties} |"
        )
    lines.append("")
    return "\n".join(lines)


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Curves of epochs-to-target over thresholds")
    parser.add_argument("--suite", action="append", default=[], help="suite name from scripts/repro.py")
    parser.add_argument("--results", action="append", default=[], type=Path, help="explicit results.json")
    parser.add_argument("--output", type=Path, default=ROOT / "runs" / "threshold-curves")
    parser.add_argument("--steps", type=int, default=13, help="number of thresholds on the grid")
    parser.add_argument("--seeds-dir", action="append", default=[], type=Path,
                        help="a seed-sweep directory (runs/seed-sweep-<suite>): also report how stable "
                             "the crossing between two arms is across those seeds. Repeat once per "
                             "--suite, in the same order.")
    parser.add_argument("--compare", action="append", default=[],
                        help="two arm names, colon separated (e.g. adamw_constant:schedule_free_adamw), "
                             "once per --suite in the same order")
    parser.add_argument("--pinned", type=float, default=None,
                        help="threshold to test for consistency across seeds (default: the suite's target_loss)")
    args = parser.parse_args(argv)

    output = args.output if args.output.is_absolute() else (ROOT / args.output)
    if args.seeds_dir and len(args.seeds_dir) != len(args.suite):
        raise SystemExit("--seeds-dir must be given once per --suite, in the same order")
    if args.compare and len(args.compare) != len(args.suite):
        raise SystemExit("--compare must be given once per --suite, in the same order")
    items: List[Dict[str, Any]] = []
    stability: List[Dict[str, Any]] = []
    for position, name in enumerate(args.suite):
        if name not in SUITES:
            raise SystemExit(f"unknown suite: {name} (available: {', '.join(SUITES)})")
        path = ROOT / SUITES[name]["output"] / "results.json"
        if not path.exists():
            raise SystemExit(f"missing {path}; run `python scripts/repro.py --suite {name}` first")
        payload = load_results(path)
        items.append(write_suite(payload, name, output, args.steps))
        if args.seeds_dir and args.compare:
            raw_dir = args.seeds_dir[position]
            seeds_dir = raw_dir if raw_dir.is_absolute() else (ROOT / raw_dir)
            seed_payloads = [
                load_results(seed_dir / "results.json")
                for seed_dir in sorted(seeds_dir.glob("seed-*"), key=lambda item: int(item.name.split("-")[1]))
            ]
            first, _, second = args.compare[position].partition(":")
            if not first or not second:
                raise SystemExit("--compare expects two names separated by ':'")
            result = crossing_stability(
                seed_payloads, first, second,
                args.pinned if args.pinned is not None else payload.get("target_loss"),
                steps=40,
            )
            (output / f"{name}-crossing-stability.md").write_text(
                stability_markdown(name, result), encoding="utf-8"
            )
            stability.append({"suite": name, **result})
            print(
                f"{name:<22} crossings in {result['crossings_found']}/{result['seeds']} seeds, "
                f"mean {result['crossing_mean']}, pinned winner consistent: {result['pinned_consistent']}"
            )
    for path in args.results:
        resolved = path if path.is_absolute() else (ROOT / path)
        items.append(write_suite(load_results(resolved), resolved.parent.name, output, args.steps))
    if not items:
        raise SystemExit("nothing to do: pass --suite and/or --results")

    (output / "SUMMARY.md").write_text(summary(items), encoding="utf-8")
    for item in items:
        print(f"{item['suite']:<22} thresholds {item['thresholds'][0]:.4f}..{item['thresholds'][-1]:.4f}")
    print(f"summary: {output / 'SUMMARY.md'}")
    if stability:
        (output / "CROSSINGS.md").write_text(
            "# Crossing stability across seeds\n\n"
            + "\n".join(
                f"- `{item['suite']}` ({item['pair'][0]} vs {item['pair'][1]}): crossing in "
                f"{item['crossings_found']}/{item['seeds']} seeds, mean {item['crossing_mean']}, "
                f"spread {item['crossing_spread']}; pinned-threshold winner consistent: "
                f"{item['pinned_consistent']} ({item['pinned_winner']})"
                for item in stability
            )
            + "\n",
            encoding="utf-8",
        )
        print(f"crossings: {output / 'CROSSINGS.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
