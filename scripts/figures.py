#!/usr/bin/env python3
"""Figures for the report, generated as SVG with no dependencies.

Two pictures carry the two claims of §5.16 and §5.11/§5.15 better than the tables do:

* `forest-*.svg` — the paired median difference with its bootstrap interval for every suite in each
  declared claim family, on one axis, so that "the effect is established at one suite" is visible
  rather than buried in a table row;
* `noise-vs-stability.svg` — the per-seed noise of a suite against how many different arms win at
  its pinned threshold. It was drawn to show the correlation §5.11 claimed; it shows instead that the
  correlation is not there, which is why §5.11 finding 7, §5.13's H5 and §5.15's N4 are withdrawn.

Everything is read from the committed per-seed files; no experiment is re-run. The SVGs are
deterministic (no timestamps), so a figure that changes means the data changed.

Usage:
    python scripts/figures.py            # writes runs/figures/
    make figures
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.paired_stats import CLAIM_FAMILIES, build_report, load_sweep  # noqa: E402

DEFAULT_OUTPUT = ROOT / "runs" / "figures"

INK = "#1f2933"
MUTED = "#7b8794"
ACCENT = "#b91c1c"
NEUTRAL = "#2f6f9f"
GRID = "#d9dee3"
FONT = "font-family=\"-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif\""


def _escape(text: str) -> str:
    return (text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def _header(width: int, height: int, title: str, subtitle: str) -> List[str]:
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-label="{_escape(title)}">',
        f'<rect width="{width}" height="{height}" fill="white"/>',
        f'<text x="24" y="30" {FONT} font-size="16" font-weight="600" fill="{INK}">{_escape(title)}</text>',
        f'<text x="24" y="50" {FONT} font-size="11" fill="{MUTED}">{_escape(subtitle)}</text>',
    ]


def forest_svg(suite_rows: Sequence[Dict[str, Any]], title: str, subtitle: str,
               width: int = 860) -> str:
    """One row per suite: median difference, bootstrap interval, and a marker if it survives."""
    row_height = 26
    top = 84
    left = 260
    right = width - 210
    height = top + row_height * len(suite_rows) + 56
    if not suite_rows:
        lines = _header(width, height, title, subtitle)
        lines.append(f'<text x="{left}" y="{top}" {FONT} font-size="11" fill="{MUTED}">'
                     f'no comparisons available</text>')
        lines.append("</svg>")
        return "\n".join(lines) + "\n"
    values = [value for row in suite_rows
              for value in (row["median"], row["median_ci_low"], row["median_ci_high"])]
    span = max(abs(min(values)), abs(max(values)), 1e-6)
    limit = span * 1.15

    def x_of(value: float) -> float:
        return left + (value + limit) / (2 * limit) * (right - left)

    lines = _header(width, height, title, subtitle)
    # zero line and axis
    zero = x_of(0.0)
    lines.append(f'<line x1="{zero:.1f}" y1="{top - 12}" x2="{zero:.1f}" y2="{height - 42}" '
                 f'stroke="{INK}" stroke-width="1"/>')
    for tick in (-1, -0.5, 0.5, 1):
        position = x_of(tick * limit)
        lines.append(f'<line x1="{position:.1f}" y1="{top - 6}" x2="{position:.1f}" y2="{height - 42}" '
                     f'stroke="{GRID}" stroke-width="1" stroke-dasharray="2 3"/>')
        lines.append(f'<text x="{position:.1f}" y="{height - 28}" {FONT} font-size="10" fill="{MUTED}" '
                     f'text-anchor="middle">{tick * limit:+.3f}</text>')
    lines.append(f'<text x="{zero:.1f}" y="{height - 28}" {FONT} font-size="10" fill="{INK}" '
                 f'text-anchor="middle">0</text>')
    for index, row in enumerate(suite_rows):
        y = top + index * row_height
        survives = row["adjusted_p"] <= 0.05
        colour = ACCENT if survives else NEUTRAL
        lines.append(f'<text x="{left - 12}" y="{y + 4}" {FONT} font-size="11" fill="{INK}" '
                     f'text-anchor="end">{_escape(row["suite"])} ({row["wins"]}/{row["n"]})</text>')
        low, high = x_of(row["median_ci_low"]), x_of(row["median_ci_high"])
        lines.append(f'<line x1="{low:.1f}" y1="{y:.1f}" x2="{high:.1f}" y2="{y:.1f}" '
                     f'stroke="{colour}" stroke-width="2"/>')
        for edge in (low, high):
            lines.append(f'<line x1="{edge:.1f}" y1="{y - 4:.1f}" x2="{edge:.1f}" y2="{y + 4:.1f}" '
                         f'stroke="{colour}" stroke-width="2"/>')
        lines.append(f'<circle cx="{x_of(row["median"]):.1f}" cy="{y:.1f}" r="3.5" fill="{colour}"/>')
        label = f'adjusted p = {row["adjusted_p"]:.3f}'
        lines.append(f'<text x="{right + 14}" y="{y + 4}" {FONT} font-size="10" '
                     f'fill="{ACCENT if survives else MUTED}">{label}</text>')
    lines.append(f'<text x="24" y="{height - 8}" {FONT} font-size="10" fill="{MUTED}">'
                 f'median paired difference in test loss (negative = first arm better; 0 = no '
                 f'difference), with the 95% bootstrap interval of the median</text>')
    lines.append("</svg>")
    return "\n".join(lines) + "\n"


def stability_table(root: Path) -> List[Dict[str, Any]]:
    """Per suite: the noise statistics and how many arms win at the pinned threshold.

    Every column is computed here, from the committed per-seed files, under a definition that is
    written next to it. That matters: the table in `REPRODUCTION.md` §5.13 was assembled by hand, and
    when this function was written its sigma column could not be reproduced — the values belong to
    different arms in different rows. See the correction in that section and case 5 in
    `docs/defect-family.md`.

    Definitions used here, all on `test_loss`:

    * `sigma_best` — per-seed stdev of the arm with the lowest **mean** test loss;
    * `sigma_modal` — mean of the per-seed stdevs of the arms that win at the pinned threshold most
      often (the tie set is averaged, which is stated because it is a choice);
    * `sigma_median` — median of the per-arm per-seed stdevs;
    * `winners` — number of distinct winner *sets* at the pinned `epochs_to_target` threshold over the
      ten seeds, where a tie counts as one set and is named.
    """
    rows: List[Dict[str, Any]] = []
    for directory in sorted(root.glob("seed-sweep*")):
        if not directory.is_dir():
            continue
        seeds, series = load_sweep(directory, "test_loss")
        if len(seeds) < 2:
            continue
        suite = directory.name.replace("seed-sweep-", "").replace("seed-sweep", "main")
        if any(value is None for values in series.values() for value in values):
            continue
        means = {arm: statistics.mean(values) for arm, values in series.items()}
        best = min(means, key=lambda arm: means[arm])
        sigma = statistics.stdev(series[best])
        winners: Dict[Tuple[str, ...], int] = {}
        reached_any = False
        for position in range(len(seeds)):
            reached = []
            for arm, values in series.items():
                epochs = _epochs_to_target(directory, position, arm)
                if epochs is not None:
                    reached.append((epochs, arm))
            if not reached:
                continue
            reached_any = True
            fastest = min(epoch for epoch, _ in reached)
            tied = tuple(sorted(arm for epoch, arm in reached if epoch == fastest))
            winners[tied] = winners.get(tied, 0) + 1
        if not reached_any:
            # No pinned target in this config, so there is no "winner at the pinned threshold" to
            # count. Plotting it at zero winners would invent a point.
            continue
        modal = max(winners, key=lambda key: winners[key])
        rows.append({
            "suite": suite,
            "best": best,
            "sigma": sigma,
            "sigma_best": sigma,
            "sigma_modal": statistics.mean(
                statistics.stdev(series[arm]) for arm in modal),
            "sigma_median": statistics.median(
                statistics.stdev(values) for values in series.values()),
            "winners": len(winners),
            "modal_winner": ", ".join(modal),
            "modal_winner_count": winners[modal],
        })
    return rows


_EPOCH_CACHE: Dict[Tuple[str, int], Dict[str, Optional[int]]] = {}


def _epochs_to_target(directory: Path, position: int, arm: str) -> Optional[int]:
    key = (str(directory), position)
    if key not in _EPOCH_CACHE:
        seed = sorted(
            int(path.name.split("-")[1]) for path in directory.glob("seed-*")
            if path.is_dir() and path.name.split("-")[1].isdigit()
        )[position]
        payload = json.loads((directory / f"seed-{seed}" / "results.json").read_text(encoding="utf-8"))
        _EPOCH_CACHE[key] = {item["name"]: item.get("epochs_to_target") for item in payload["results"]}
    return _EPOCH_CACHE[key].get(arm)


def stability_svg(rows: Sequence[Dict[str, Any]], width: int = 760) -> str:
    """Dot plot, one row per suite, ordered by noise.

    A scatter was the first attempt and it was unreadable: the y quantity (how many arms win) is a
    small integer, so most suites land on the same three lanes and their labels pile up. Ordering the
    suites by their own sigma and annotating the winner count on the right shows the same picture with
    no overlapping labels — and, as it turned out, no correlation either: the winner count does not
    rise with sigma, which is what withdrew the claim that used to live in §5.11 finding 7.
    without a single overlapping label.
    """
    ordered = sorted(rows, key=lambda row: (row["sigma"], row["suite"]))
    row_height = 26
    top = 96
    left = 210
    plot_right = width - 150
    height = top + row_height * len(ordered) + 78
    if not ordered:
        lines = _header(width, height, "Noise and ranking reproducibility, across every ten-seed suite",
                        "No suite with a pinned threshold was found")
        lines.append("</svg>")
        return "\n".join(lines) + "\n"
    sigmas = [row["sigma"] for row in ordered]
    low = min(sigmas) - 0.002
    high = max(sigmas) + 0.002

    def x_of(value: float) -> float:
        return left + (value - low) / (high - low) * (plot_right - left)

    lines = _header(
        width, height, "Noise and ranking reproducibility, across every ten-seed suite",
        "Per-seed test-loss stdev of the suite's best arm, against how many different arms win at its "
        "pinned threshold",
    )
    baseline = top + row_height * len(ordered) - row_height / 2 + 6
    for index in range(5):
        value = low + (high - low) * index / 4
        x = x_of(value)
        lines.append(f'<line x1="{x:.1f}" y1="{top - 16}" x2="{x:.1f}" y2="{baseline:.1f}" '
                     f'stroke="{GRID}" stroke-width="1" stroke-dasharray="2 3"/>')
        lines.append(f'<text x="{x:.1f}" y="{baseline + 22:.1f}" {FONT} font-size="10" fill="{MUTED}" '
                     f'text-anchor="middle">{value:.3f}</text>')
    lines.append(f'<text x="{(left + plot_right) / 2:.1f}" y="{height - 14}" {FONT} font-size="11" '
                 f'fill="{INK}" text-anchor="middle">per-seed test-loss standard deviation (sigma)</text>')
    for index, row in enumerate(ordered):
        y = top + index * row_height
        stable = row["winners"] == 1
        colour = ACCENT if stable else NEUTRAL
        lines.append(f'<text x="{left - 12}" y="{y + 4:.1f}" {FONT} font-size="11" fill="{INK}" '
                     f'text-anchor="end">{_escape(row["suite"])}</text>')
        lines.append(f'<line x1="{left - 6}" y1="{y:.1f}" x2="{x_of(row["sigma"]) - 6:.1f}" y2="{y:.1f}" '
                     f'stroke="{GRID}" stroke-width="1"/>')
        lines.append(f'<circle cx="{x_of(row["sigma"]):.1f}" cy="{y:.1f}" r="5" '
                     f'fill="{"white" if not stable else ACCENT}" stroke="{colour}" stroke-width="2"/>')
        lines.append(f'<text x="{plot_right + 14:.1f}" y="{y + 4:.1f}" {FONT} font-size="10" '
                     f'fill="{ACCENT if stable else MUTED}">{row["winners"]} winner'
                     f'{"" if row["winners"] == 1 else "s"}</text>')
    lines.append(f'<text x="24" y="{height - 46}" {FONT} font-size="10" fill="{MUTED}">'
                 f'Filled markers: one arm wins in all ten seeds. There is no monotone relationship: '
                 f'optimizers-mlp has the second-lowest noise and five winners, activation-relu sits '
                 f'higher and has one.</text>')
    lines.append("</svg>")
    return "\n".join(lines) + "\n"


CAPTIONS = """# Figure captions

Generated by `scripts/figures.py` from the committed per-seed files; no experiment is re-run, and the
SVGs are deterministic (a figure that changes means the data changed).

**forest-schedule-free.svg** — Paired median difference in test loss between Schedule-Free AdamW and the
tuned-cosine AdamW baseline, per suite, with the 95% bootstrap interval of the median. Differences are
`A - B`, so negative favours Schedule-Free. Red marks the one suite whose comparison survives a
Holm-Bonferroni correction inside this claim family (`capacity-h16x16`); the adjusted p-value is printed
on each row. The figure is the visual form of §5.16's finding that the direction of the median holds
across the matrix while the statistically established effect is the large one at the deepest capacity.

**forest-ademamix.svg** — The same construction for AdEMAMix against AdamW at matched settings, across
eleven suites. No interval clears zero after the family correction, and several sit on the wrong side of
zero, which is why the card states the claim as a bound ("no advantage detected") instead of an equality.

**noise-vs-stability.svg** — One row per ten-seed suite, ordered by the per-seed test-loss standard
deviation of its best arm (dot position on the x axis), annotated on the right with how many distinct
arms win at its pinned `epochs_to_target` threshold across the ten seeds. **There is no monotone
relationship**, and that is the point of the figure: `optimizers-mlp` has the second-lowest noise of the
corpus (0.02019) and five different winners, while the two activation suites sit at 0.0217 and have a
single winner in all ten seeds. The first version of this figure was a scatter with all six arms of each
suite labelled; it was unreadable because the winner count is a small integer, so most suites land on the
same three lanes. Ordering the suites by noise fixes the layout and, as it turned out, exposes that the
hand-assembled sigma column in §5.13 was not reproducible under its own label (see the correction there
and case 5 in `docs/defect-family.md`). `stability.csv` next to the figure carries all three noise
statistics and the winner counts, computed under stated definitions.

Suites whose config pins no target (`main`) are excluded: with no threshold there is no "winner at the
pinned threshold" to count, and plotting them at zero would invent a point.

The committed artifacts are SVG only, because they are text, deterministic and produced by the
repository's own dependency-free code. Raster previews for platforms that need them can be made locally
with `cairosvg`; they are ignored by git on purpose, because an artifact the repository cannot
regenerate is exactly what case 5 warns about.
"""


def forest_rows(report: Dict[str, Any], claim_prefix: str) -> List[Dict[str, Any]]:
    for family in report["claim_families"]:
        if family["claim"].startswith(claim_prefix):
            return list(reversed(family["detail"]))
    return []


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Generate the report figures as SVG")
    parser.add_argument("--root", type=Path, default=ROOT / "runs")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args(argv)

    report = build_report(args.root, "test_loss", None, None, 0.05)
    args.output.mkdir(parents=True, exist_ok=True)

    schedule_free = forest_rows(report, "schedule-free")
    ademamix = forest_rows(report, "AdEMAMix")
    (args.output / "forest-schedule-free.svg").write_text(
        forest_svg(schedule_free, "Schedule-Free AdamW vs a tuned cosine: paired differences",
                   "Ten-seed paired comparison per suite; negative favours Schedule-Free"),
        encoding="utf-8")
    (args.output / "forest-ademamix.svg").write_text(
        forest_svg(ademamix, "AdEMAMix vs AdamW at matched settings: paired differences",
                   "Ten-seed paired comparison per suite; negative favours AdEMAMix"),
        encoding="utf-8")
    (args.output / "noise-vs-stability.svg").write_text(
        stability_svg(stability_table(args.root)), encoding="utf-8")
    (args.output / "captions.md").write_text(CAPTIONS, encoding="utf-8")
    table = stability_table(args.root)
    header = ("suite,best_arm,sigma_best,sigma_modal,sigma_median,winners,modal_winner,"
              "modal_winner_count")
    lines = [header]
    for row in sorted(table, key=lambda item: item["sigma_best"]):
        lines.append(",".join([
            row["suite"], row["best"], f"{row['sigma_best']:.5f}", f"{row['sigma_modal']:.5f}",
            f"{row['sigma_median']:.5f}", str(row["winners"]), f'"{row["modal_winner"]}"',
            str(row["modal_winner_count"]),
        ]))
    (args.output / "stability.csv").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote 3 figures and captions.md to {args.output}")
    print(f"  schedule-free rows: {len(schedule_free)}, ademamix rows: {len(ademamix)}, "
          f"stability points: {len(stability_table(args.root))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
