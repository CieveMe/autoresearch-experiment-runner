#!/usr/bin/env python3
"""Paired statistics over the committed ten-seed sweeps — analysis only, no re-runs.

Every paired comparison in this repository has so far been reported as a mean difference, a
standard deviation and a win count. That is a *description* of ten numbers, not a test, and the
win count on its own has already produced a wrong-looking verdict once: eight wins out of ten
with a mean difference of 9e-5 (three orders of magnitude below the per-seed spread).

This script adds the missing half. For each comparison it reports

* the paired differences themselves (wins / losses / ties, median, mean, spread),
* **effect sizes**: Cohen's d_z for paired data, the matched-pairs rank-biserial correlation, and
  the probability of superiority,
* **intervals**: a 95% t interval for the mean difference and a deterministic bootstrap percentile
  interval for the median difference,
* **exact distribution-free tests**: the sign test and the Wilcoxon signed-rank test, both computed
  by enumeration rather than by a normal approximation, because ten seeds is ten seeds,
* a Holm-Bonferroni adjustment across the whole family of comparisons printed in one run, so that
  a screen full of p-values cannot be read as if each one had been pre-registered on its own.

A hard rule is enforced in the wording as well as in the documentation: **a test that fails to
reject is reported as "no evidence at this budget", never as "no difference"**. With ten seeds the
power to detect anything but a large effect is low, and the two statements are not the same claim.
`scripts/score_task.py`'s fourth control is a mutation of the *method*; this rule is the equivalent
for the *sentence*.

Usage:
    python scripts/paired_stats.py                       # every committed seed sweep, baseline = first arm
    python scripts/paired_stats.py --reference adamw_cosine --suite norm-layernorm
    python scripts/paired_stats.py --json                # machine-readable
"""

from __future__ import annotations

import argparse
import json
import math
import random
import statistics
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.repro import SUITES  # noqa: E402

DEFAULT_SWEEP_ROOT = ROOT / "runs"
DEFAULT_OUTPUT = ROOT / "runs" / "paired-tests"

# 97.5th percentile of Student's t, indexed by degrees of freedom (abscissa 0.975).
_T975 = {
    1: 12.706, 2: 4.303, 3: 3.182, 4: 2.776, 5: 2.571, 6: 2.447, 7: 2.365, 8: 2.306,
    9: 2.262, 10: 2.228, 11: 2.201, 12: 2.179, 13: 2.160, 14: 2.145, 15: 2.131,
    16: 2.120, 17: 2.110, 18: 2.101, 19: 2.093, 20: 2.086, 21: 2.080, 22: 2.074,
    23: 2.069, 24: 2.064, 25: 2.060, 26: 2.056, 27: 2.052, 28: 2.048, 29: 2.045, 30: 2.042,
}

# 80th percentile of Student's t, for the power term of the minimal detectable effect.
_T80 = {
    1: 1.376, 2: 1.061, 3: 0.978, 4: 0.941, 5: 0.920, 6: 0.906, 7: 0.896, 8: 0.889,
    9: 0.883, 10: 0.879, 11: 0.876, 12: 0.873, 13: 0.870, 14: 0.868, 15: 0.866,
    16: 0.865, 17: 0.863, 18: 0.862, 19: 0.861, 20: 0.860, 21: 0.859, 22: 0.858,
    23: 0.858, 24: 0.857, 25: 0.856, 26: 0.856, 27: 0.855, 28: 0.855, 29: 0.854, 30: 0.854,
}

# Comparisons the repository's headline claims rest on, so the report leads with them rather than
# with a wall of tables. (suite, arm A, arm B); d = A - B, so a negative mean favours A.
HEADLINE_COMPARISONS: Tuple[Tuple[str, str, str], ...] = (
    ("schedule-free-mlp", "schedule_free_adamw", "adamw_cosine"),
    ("capacity-h32", "schedule_free_adamw", "adamw_cosine"),
    ("capacity-h64", "schedule_free_adamw", "adamw_cosine"),
    ("capacity-h16x16", "schedule_free_adamw", "adamw_cosine"),
    ("activation-relu", "schedule_free_adamw", "adamw_cosine"),
    ("activation-gelu", "schedule_free_adamw", "adamw_cosine"),
    ("norm-layernorm", "schedule_free_adamw", "adamw_cosine"),
    ("norm-batchnorm", "schedule_free_adamw", "adamw_cosine"),
    ("init-he", "schedule_free_adamw", "adamw_cosine"),
    ("init-plain", "schedule_free_adamw", "adamw_cosine"),
    ("ademamix-mlp", "ademamix_no_warmups", "adamw"),
    ("capacity-h64", "ademamix", "adamw_constant"),
    ("capacity-h16x16", "ademamix", "adamw_constant"),
    ("norm-layernorm", "ademamix", "adamw_constant"),
    ("optimizers", "adagrad", "adam"),
    ("optimizers-mlp", "adagrad", "adam"),
    ("optimizers", "adam", "baseline"),
)

# A p-value is only adjusted *within a family*, and the family has to be declared. Printing every
# comparison and then correcting across the whole printed set answers a question nobody asked: the
# claims were pre-registered one at a time, and a claim tested at ten capacities is still one claim.
# Both views are reported, and the report names the family each adjusted number belongs to.
CLAIM_FAMILIES: Dict[str, Tuple[Tuple[str, str, str], ...]] = {
    "schedule-free beats a tuned cosine (one claim, ten suites)": (
        ("schedule-free-mlp", "schedule_free_adamw", "adamw_cosine"),
        ("capacity-h32", "schedule_free_adamw", "adamw_cosine"),
        ("capacity-h64", "schedule_free_adamw", "adamw_cosine"),
        ("capacity-h16x16", "schedule_free_adamw", "adamw_cosine"),
        ("activation-relu", "schedule_free_adamw", "adamw_cosine"),
        ("activation-gelu", "schedule_free_adamw", "adamw_cosine"),
        ("norm-layernorm", "schedule_free_adamw", "adamw_cosine"),
        ("norm-batchnorm", "schedule_free_adamw", "adamw_cosine"),
        ("init-he", "schedule_free_adamw", "adamw_cosine"),
        ("init-plain", "schedule_free_adamw", "adamw_cosine"),
    ),
    "AdEMAMix shows no advantage over AdamW at matched settings (one claim, eleven suites)": (
        ("ademamix", "ademamix_tuned", "adamw"),
        ("ademamix-mlp", "ademamix_no_warmups", "adamw"),
        ("capacity-h32", "ademamix", "adamw_constant"),
        ("capacity-h64", "ademamix", "adamw_constant"),
        ("capacity-h16x16", "ademamix", "adamw_constant"),
        ("norm-layernorm", "ademamix", "adamw_constant"),
        ("norm-batchnorm", "ademamix", "adamw_constant"),
        ("init-he", "ademamix", "adamw_constant"),
        ("init-plain", "ademamix", "adamw_constant"),
        ("activation-relu", "ademamix", "adamw_constant"),
        ("activation-gelu", "ademamix", "adamw_constant"),
    ),
}


def _combinations(n: int, k: int) -> int:
    return math.comb(n, k)


def binomial_tail(n: int, k: int) -> float:
    """P(X >= k) for X ~ Binomial(n, 1/2), exactly."""
    if k <= 0:
        return 1.0
    if k > n:
        return 0.0
    return sum(_combinations(n, i) for i in range(k, n + 1)) / 2 ** n


def sign_test(differences: Sequence[float]) -> Dict[str, Any]:
    """Exact two-sided sign test. Zeros are dropped, as the test requires."""
    non_zero = [value for value in differences if value != 0]
    n = len(non_zero)
    if n == 0:
        return {"name": "sign", "n_used": 0, "positive": 0, "p_value": 1.0, "informative": False,
                "note": "every paired difference is exactly zero: the data carry no sign information"}
    positive = sum(1 for value in non_zero if value > 0)
    tail = binomial_tail(n, max(positive, n - positive))
    return {"name": "sign", "n_used": n, "positive": positive,
            "p_value": min(1.0, 2.0 * tail), "informative": True, "note": ""}


def _doubled_ranks(values: Sequence[float]) -> List[int]:
    """Ranks of |value| with average ranks for ties, multiplied by two so they stay integers.

    Doubling matters: average ranks for tied magnitudes are half-integers, and an exact test should
    not depend on a floating-point comparison when it can be decided with integers.
    """
    scaled = sorted((abs(value), index) for index, value in enumerate(values))
    ranks = [0] * len(values)
    position = 0
    while position < len(scaled):
        end = position
        while end + 1 < len(scaled) and scaled[end + 1][0] == scaled[position][0]:
            end += 1
        # positions are 1-based ranks: average of (position+1 .. end+1), doubled.
        average_doubled = (position + 1) + (end + 1)
        for index in range(position, end + 1):
            ranks[scaled[index][1]] = average_doubled
        position = end + 1
    return ranks


def wilcoxon_signed_rank(differences: Sequence[float], max_exact: int = 20) -> Dict[str, Any]:
    """Two-sided Wilcoxon signed-rank test. Exact by enumeration up to `max_exact` non-zero pairs.

    Average ranks are used for tied absolute differences. The exact null distribution is symmetric
    about T/2 because W- = T - W+, so the two-sided p-value is twice the lower tail of the observed
    W+ (clipped at 1).
    """
    non_zero = [value for value in differences if value != 0]
    n = len(non_zero)
    if n == 0:
        return {"name": "wilcoxon", "n_used": 0, "w_plus": 0.0, "p_value": 1.0, "exact": True,
                "informative": False, "note": "every paired difference is exactly zero"}
    doubled = _doubled_ranks(non_zero)
    w_plus_doubled = sum(rank for rank, value in zip(doubled, non_zero) if value > 0)
    total_doubled = 2 * (n * (n + 1) // 2)
    observed = min(w_plus_doubled, total_doubled - w_plus_doubled)
    if n <= max_exact:
        count = 0
        for mask in range(1 << n):
            statistic = sum(doubled[position] for position in range(n) if mask >> position & 1)
            if statistic <= observed:
                count += 1
        p_value = min(1.0, 2.0 * count / (1 << n))
        exact = True
    else:  # pragma: no cover - the repository's sweeps are all ten seeds
        mean = total_doubled / 2.0
        variance = n * (n + 1) * (2 * n + 1) / 6.0
        z = (abs(w_plus_doubled - mean) - 1.0) / math.sqrt(variance)
        p_value = min(1.0, 2.0 * (1.0 - 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))))
        exact = False
    return {"name": "wilcoxon", "n_used": n, "w_plus": w_plus_doubled / 2.0, "p_value": p_value,
            "exact": exact, "informative": True, "note": ""}


def bootstrap_interval(
    values: Sequence[float], statistic=statistics.median, resamples: int = 20000, seed: int = 20260928
) -> Tuple[float, float]:
    """Percentile bootstrap interval for a statistic of the paired differences.

    Deterministic: the resampling uses a fixed seed, so the published interval can be reproduced
    exactly instead of moving by a few 1e-5 on every run.
    """
    rng = random.Random(seed)
    count = len(values)
    estimates = []
    for _ in range(resamples):
        sample = [values[rng.randrange(count)] for _ in range(count)]
        estimates.append(statistic(sample))
    estimates.sort()
    low = estimates[int(0.025 * resamples)]
    high = estimates[min(resamples - 1, int(0.975 * resamples))]
    return low, high


def t_interval(values: Sequence[float], confidence: float = 0.95) -> Tuple[float, float, float]:
    """Mean and its two-sided t interval. Returns (mean, low, high)."""
    mean = statistics.mean(values)
    if len(values) < 2:
        return mean, float("nan"), float("nan")
    standard_error = statistics.stdev(values) / math.sqrt(len(values))
    critical = _T975.get(len(values) - 1, 1.96 if confidence == 0.95 else 2.576)
    return mean, mean - critical * standard_error, mean + critical * standard_error


def rank_biserial(differences: Sequence[float]) -> float:
    """Matched-pairs rank-biserial correlation from the Wilcoxon statistics."""
    non_zero = [value for value in differences if value != 0]
    if not non_zero:
        return 0.0
    ranks = _doubled_ranks(non_zero)
    positive = sum(rank for rank, value in zip(ranks, non_zero) if value > 0)
    negative = sum(rank for rank, value in zip(ranks, non_zero) if value < 0)
    return (positive - negative) / (positive + negative)


def effect_sizes(differences: Sequence[float]) -> Dict[str, float]:
    mean = statistics.mean(differences)
    spread = statistics.stdev(differences) if len(differences) > 1 else 0.0
    wins = sum(1 for value in differences if value < 0)
    ties = sum(1 for value in differences if value == 0)
    return {
        "cohens_dz": mean / spread if spread else 0.0,
        "rank_biserial": rank_biserial(differences),
        "probability_of_superiority": (wins + 0.5 * ties) / len(differences),
    }


def holm(p_values: Sequence[float]) -> List[float]:
    """Holm-Bonferroni adjusted p-values, returned in the original order."""
    order = sorted(range(len(p_values)), key=lambda index: p_values[index])
    count = len(p_values)
    adjusted = [0.0] * count
    running = 0.0
    for position, index in enumerate(order):
        scaled = min(1.0, (count - position) * p_values[index])
        running = max(running, scaled)
        adjusted[index] = running
    return adjusted


def minimal_detectable_effect(differences: Sequence[float], power: float = 0.8) -> float:
    """Smallest true paired difference this design can detect with the given power.

    Two-sided alpha = 0.05, normal-approximation formula
    ``(t_{1-a/2} + t_{power}) * sd / sqrt(n)``. This is the number that turns "the test did not
    reject" into something a reader can use: with ten paired seeds it comes out at roughly one
    per-seed standard deviation of the differences, so only a large effect is detectable and a
    null result bounds the effect rather than establishing its absence.
    """
    if len(differences) < 2:
        return float("nan")
    spread = statistics.stdev(differences)
    degrees = len(differences) - 1
    critical = _T975.get(degrees, 1.96)
    power_term = _T80.get(degrees, 0.85) if power == 0.8 else _T975.get(degrees, 1.96)
    return (critical + power_term) * spread / math.sqrt(len(differences))


def evidence_phrase(mean_low: float, mean_high: float, p_value: float, alpha: float = 0.05) -> str:
    """The sentence-level rule: a failed test is not evidence of equality.

    With ten seeds the power to detect anything but a large effect is low, so "the test did not
    reject" and "the two are the same" are different statements and only the first is supported.
    """
    if p_value <= alpha and (mean_low > 0 or mean_high < 0):
        direction = "worse" if mean_low > 0 else "better"
        return f"evidence of a difference (both tests agree; A is {direction} on this metric)"
    return "no evidence of a difference at this budget (not the same claim as no difference)"


def summarise(differences: Sequence[float], alpha: float = 0.05) -> Dict[str, Any]:
    """Everything above, for one paired comparison. `differences[i] = A_i - B_i`."""
    if not differences:
        raise ValueError("a paired comparison needs at least one seed")
    mean, mean_low, mean_high = t_interval(differences)
    median = statistics.median(differences)
    median_low, median_high = bootstrap_interval(differences)
    sign = sign_test(differences)
    wilcoxon = wilcoxon_signed_rank(differences)
    # The combined p-value is the more conservative of the two: a comparison is only called
    # significant when both distribution-free tests agree.
    combined = max(sign["p_value"], wilcoxon["p_value"])
    sizes = effect_sizes(differences)
    return {
        "n": len(differences),
        "wins": sum(1 for value in differences if value < 0),
        "losses": sum(1 for value in differences if value > 0),
        "ties": sum(1 for value in differences if value == 0),
        "mean": mean,
        "median": median,
        "stdev": statistics.stdev(differences) if len(differences) > 1 else 0.0,
        "mean_ci_low": mean_low,
        "mean_ci_high": mean_high,
        "median_ci_low": median_low,
        "median_ci_high": median_high,
        "min": min(differences),
        "max": max(differences),
        "sign_p": sign["p_value"],
        "wilcoxon_p": wilcoxon["p_value"],
        "wilcoxon_exact": wilcoxon["exact"],
        "combined_p": combined,
        "min_detectable_effect_80": minimal_detectable_effect(differences),
        "informative": sign["informative"] and wilcoxon["informative"],
        **sizes,
        "verdict": ("the two arms are identical in every seed, so there is nothing to test"
                    if not (sign["informative"] and wilcoxon["informative"])
                    else evidence_phrase(mean_low, mean_high, combined, alpha)),
    }


def load_sweep(directory: Path, metric: str) -> Tuple[List[int], Dict[str, List[float]]]:
    """Return (seeds, {arm: [value per seed]}) for one committed seed sweep."""
    seeds = sorted(
        int(path.name.split("-")[1])
        for path in directory.glob("seed-*")
        if path.is_dir() and path.name.split("-")[1].isdigit()
    )
    series: Dict[str, List[float]] = {}
    for seed in seeds:
        payload = json.loads((directory / f"seed-{seed}" / "results.json").read_text(encoding="utf-8"))
        for item in payload["results"]:
            series.setdefault(item["name"], []).append(item[metric])
    return seeds, series


def discover_sweeps(root: Path) -> Dict[str, Path]:
    """Map suite name -> seed-sweep directory for every suite that has one."""
    found: Dict[str, Path] = {}
    for name in list(SUITES) + ["main"]:
        candidate = root / f"seed-sweep-{name}" if name != "main" else root / "seed-sweep"
        if candidate.is_dir():
            found[name] = candidate
    return found


def build_report(root: Path, metric: str, only: Optional[Iterable[str]], reference: Optional[str],
                 alpha: float) -> Dict[str, Any]:
    sweeps = discover_sweeps(root)
    comparisons: List[Dict[str, Any]] = []
    skipped: List[Dict[str, Any]] = []
    series_cache: Dict[str, Tuple[List[int], Dict[str, List[float]]]] = {}

    def series_for(suite: str) -> Tuple[List[int], Dict[str, List[float]]]:
        if suite not in series_cache:
            series_cache[suite] = load_sweep(sweeps[suite], metric)
        return series_cache[suite]

    def compare(suite: str, arm: str, baseline: str) -> Optional[Dict[str, Any]]:
        _, series = series_for(suite)
        missing = [name for name in (arm, baseline)
                   if name not in series or any(value is None for value in series[name])]
        if missing:
            # `epochs_to_target` is None when an arm never reaches the target. Turning that into a
            # number needs a censoring convention (the repository ranks "never" last when it ranks at
            # all), and inventing one here would quietly change the test. These pairs are listed as
            # not tested instead.
            skipped.append({
                "suite": suite, "arm": arm, "reference": baseline,
                "reason": f"`{metric}` is not reached in every seed for: {', '.join(missing)}",
            })
            return None
        differences = [a - b for a, b in zip(series[arm], series[baseline])]
        return {"suite": suite, "metric": metric, "arm": arm, "reference": baseline,
                "seeds": len(differences), **summarise(differences, alpha)}

    for suite, directory in sorted(sweeps.items()):
        if only and suite not in set(only):
            continue
        _, series = series_for(suite)
        if not series:
            continue
        arms = list(series)
        family_reference = reference if reference and reference in series else None
        baseline = family_reference or arms[0]
        for arm in arms:
            if arm == baseline:
                continue
            item = compare(suite, arm, baseline)
            if item is not None:
                comparisons.append(item)
    adjusted = holm([item["combined_p"] for item in comparisons])
    for item, value in zip(comparisons, adjusted):
        item["holm_p"] = value
        item["significant_after_holm"] = value <= alpha
    unique_skips = {}
    for item in skipped:
        unique_skips[(item["suite"], item["arm"], item["reference"])] = item
    skipped = list(unique_skips.values())
    by_key = {(item["suite"], item["arm"], item["reference"]): item for item in comparisons}
    families: List[Dict[str, Any]] = []
    for claim, members in CLAIM_FAMILIES.items():
        present = []
        for suite, arm, base in members:
            if only and suite not in set(only):
                continue
            item = by_key.get((suite, arm, base))
            if item is None and suite in sweeps:
                item = compare(suite, arm, base)
            if item is not None:
                present.append(item)
        if not present:
            continue
        within = holm([item["combined_p"] for item in present])
        survivors = 0
        for item, value in zip(present, within):
            item["holm_within_family"] = value
            survivors += int(value <= alpha)
        families.append({
            "claim": claim,
            "members": len(present),
            "smallest_raw_p": min(item["combined_p"] for item in present),
            "smallest_adjusted_p": min(within),
            "survivors": survivors,
            "detail": [
                {"suite": item["suite"], "wins": item["wins"], "n": item["n"],
                 "median": item["median"], "median_ci_low": item["median_ci_low"],
                 "median_ci_high": item["median_ci_high"], "raw_p": item["combined_p"],
                 "adjusted_p": item["holm_within_family"], "verdict": item["verdict"]}
                for item in present
            ],
        })
    headline = [
        item for item in comparisons
        if (item["suite"], item["arm"], item["reference"]) in set(HEADLINE_COMPARISONS)
    ]
    return {
        "schema": "autoresearch-lite/paired-tests@1",
        "metric": metric,
        "alpha": alpha,
        "comparisons_tested": len(comparisons),
        "headline": headline,
        "claim_families": families,
        "skipped": skipped,
        "comparisons": comparisons,
    }


def _row(item: Dict[str, Any]) -> str:
    return (
        f"| `{item['suite']}` | {item['arm']} vs {item['reference']} | {item['wins']}/{item['n']} | "
        f"{item['median']:+.5f} [{item['median_ci_low']:+.5f}, {item['median_ci_high']:+.5f}] | "
        f"{item['mean']:+.5f} [{item['mean_ci_low']:+.5f}, {item['mean_ci_high']:+.5f}] | "
        f"{item['cohens_dz']:+.2f} | {item['min_detectable_effect_80']:.5f} | "
        f"{item['sign_p']:.4f} | {item['wilcoxon_p']:.4f} | "
        f"{item['holm_p']:.4f} | {item['verdict']} |"
    )


def render_markdown(report: Dict[str, Any]) -> str:
    lines = [
        "# Paired statistics over the committed ten-seed sweeps",
        "",
        f"Metric `{report['metric']}`, {report['comparisons_tested']} paired comparisons, "
        f"alpha = {report['alpha']}. Differences are `A - B`, so **negative favours A**.",
        "",
        "Every interval and p-value below comes from the committed per-seed files; no experiment was",
        "re-run to produce this. The sign test and the Wilcoxon signed-rank test are computed by",
        "enumeration (exact for ten pairs), the interval under the median is a deterministic percentile",
        "bootstrap, and the last p-value column is Holm-adjusted across the whole table, so a single",
        "p < 0.05 in a run of this many comparisons is not by itself a result.",
        "",
        "A failed test is written as **no evidence of a difference at this budget**. With ten seeds the",
        "power to detect anything but a large effect is low, and that sentence is deliberately not the",
        "same as \"no difference\".",
        "",
        "The **MDE** column is the smallest true difference this design could detect with 80% power at",
        "this spread — about one per-seed standard deviation of the paired differences. It is the number",
        "that makes a non-significant result readable: an interval that excludes effects larger than the",
        "MDE bounds the effect, it does not establish its absence.",
        "",
        "## The comparisons the headline claims rest on",
        "",
        "| suite | comparison | wins/n | median diff [95% boot] | mean diff [95% t] | d_z | MDE(80%) | sign p | wilcoxon p | holm p | verdict |",
        "|---|---|---:|---|---|---:|---:|---:|---:|---:|---|",
    ]
    for item in report["headline"]:
        lines.append(_row(item))
    lines += [
        "",
        "## Each claim inside the family it was actually tested in",
        "",
        "Correcting across every printed table answers a question nobody asked. These are the",
        "repository's two negative results, each treated as **one** claim tested repeatedly, with the",
        "correction applied over the repetitions only.",
        "",
        "| claim | suites in family | smallest raw p | smallest adjusted p | comparisons surviving |",
        "|---|---:|---:|---:|---:|",
    ]
    for family in report["claim_families"]:
        lines.append(
            f"| {family['claim']} | {family['members']} | {family['smallest_raw_p']:.4f} | "
            f"{family['smallest_adjusted_p']:.4f} | {family['survivors']}/{family['members']} |"
        )
    lines += ["", "Per suite, inside that family:", "",
              "| claim | suite | wins/n | median diff [95% boot] | raw p | adjusted p | verdict |",
              "|---|---|---:|---|---:|---:|---|"]
    for family in report["claim_families"]:
        for detail in family["detail"]:
            lines.append(
                f"| {family['claim'].split(' (')[0]} | `{detail['suite']}` | {detail['wins']}/{detail['n']} | "
                f"{detail['median']:+.5f} [{detail['median_ci_low']:+.5f}, {detail['median_ci_high']:+.5f}] | "
                f"{detail['raw_p']:.4f} | {detail['adjusted_p']:.4f} | {detail['verdict']} |"
            )
    if report["skipped"]:
        lines += ["", "## Not tested", "",
                  "| suite | comparison | reason |", "|---|---|---|"]
        for item in report["skipped"]:
            lines.append(f"| `{item['suite']}` | {item['arm']} vs {item['reference']} | {item['reason']} |")
    lines += [
        "",
        "## Every comparison (arm versus its suite's baseline)",
        "",
        "| suite | comparison | wins/n | median diff [95% boot] | mean diff [95% t] | d_z | MDE(80%) | sign p | wilcoxon p | holm p | verdict |",
        "|---|---|---:|---|---|---:|---:|---:|---:|---:|---|",
    ]
    for item in report["comparisons"]:
        lines.append(_row(item))
    lines.append("")
    return "\n".join(lines)


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Paired statistics over the committed seed sweeps")
    parser.add_argument("--root", type=Path, default=DEFAULT_SWEEP_ROOT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--metric", default="test_loss")
    parser.add_argument("--suite", action="append", default=[], help="limit to a suite name")
    parser.add_argument("--reference", default=None, help="arm to compare against (default: first arm)")
    parser.add_argument("--alpha", type=float, default=0.05)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    report = build_report(args.root, args.metric, args.suite or None, args.reference, args.alpha)
    markdown = render_markdown(report)
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "paired-tests.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (args.output / "paired-tests.md").write_text(markdown, encoding="utf-8")
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(markdown)
    print(f"\nwrote {args.output / 'paired-tests.md'} and paired-tests.json "
          f"({report['comparisons_tested']} comparisons)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
