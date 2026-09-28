This is a **corrections release**. It carries two corrections to claims that previous versions
published, together with the analysis work that found them: exact paired tests over every committed
sweep, the figures that exposed the error, and a scored task run end to end. No experiment was re-run to
produce it, and no pinned number moved.

### Corrections (the reason this version exists)

**Correction 1 — §5.13's σ column was not reproducible, and §5.11's finding 7 is withdrawn.**
v0.7.0 published a table whose column was headed "test-loss σ of the best arm" and a claim resting on it:
that a suite's per-seed noise predicts whether its fixed-threshold ranking reproduces across ten seeds.
Drawing the noise/stability figure required recomputing that column from the committed files, and five of
the ten rows disagreed. The published values belong to *different arms in different rows* — 0.0646 for
`capacity-h8x8` is `adamw_constant`'s σ while the suite's best arm is `adagrad` at 0.02271, and 0.0381 for
`capacity-h16x16` is `adagrad`'s while the best arm is `schedule-free` at 0.03697. There is no definition
under which the column is correct. Recomputed under one stated definition the relationship is not
monotone: `optimizers-mlp` has the second-lowest noise in the corpus (0.02019) and **five** different
winners, while the two activation suites sit at 0.0217 with **one** each. So §5.11 finding 7 and §5.13's
H5 are withdrawn, and what survives is: *the noise of a suite is measurable, and on this corpus it does
not predict whether its fixed-threshold ranking reproduces.* The audited table is
`runs/figures/stability.csv`, emitted by `scripts/figures.py` and pinned by
`tests/test_figures.py::test_the_noise_statistics_are_reproducible_and_disagree_with_the_old_table`.

**Correction 2 — the second half of §5.15's N4 was wrong too.** The v0.9.0 body stated N4 as
"refuted on the mechanism, **confirmed on the correlation**". That verb rested on the same column, so it
is withdrawn with it: within that batch no variant produced a single fixed-threshold winner (plain init
had two), and the `[32]` activation suites — same capacity, higher σ — had one each. N4 is refuted in both
halves; what survives is the refutation of its mechanism and the negative result about the statistic
itself.

Both corrections are **case 5** in `docs/defect-family.md`, and both are recorded in place: the wrong text
stays where it is, struck through or quoted, with the correction next to it. The sections that carry it
are §5.11 finding 7, §5.13's H5 row and its "two columns are the point" paragraph, §5.15's N4 row and
finding 5, and the schedule-free paper card.

**Also carried forward from the queue, both already fixed in the tree:** the H1 boundary precision from
the commit after the v0.8.0 tag (`8e27e30`: what ends above `[64]` is AdaGrad's *lead*, not its
usefulness), and the two internal wordings corrected for case 4 (the CHANGELOG's claim about the
gradient check, and §8's "three defects"). `docs/release-corrections-pending.md` records the queue and the
rule: a published release body and a pushed tag are never edited, because editing the body does not
re-trigger archival, the archive is the tag's repository snapshot, and silently repairing a published
version destroys the evidence that this repository corrects itself in public.

### What else is in this release

- **`scripts/paired_stats.py`** — exact paired tests over every committed sweep (sign test and Wilcoxon
  signed-rank by enumeration), effect sizes (d_z, matched-pairs rank-biserial, probability of
  superiority), a 95% t interval for the mean difference, a deterministic bootstrap interval for the
  median, the minimal detectable effect at 80% power, and Holm-Bonferroni adjustment **within a declared
  family**. Wording is enforced in code: a test that fails to reject is reported as *no evidence of a
  difference at this budget*, never as "no difference", and a closed-set test forbids a bypass. Headline
  results (§5.16): across all 78 comparisons nothing survives a family correction (smallest adjusted
  p = 0.15); the schedule-free result is statistically established at exactly one suite
  (`capacity-h16x16`, 10/10 seeds, median −0.02692 [−0.04536, −0.01102], d_z = −1.20, adjusted
  p = 0.0195); the AdEMAMix family has none (0/11), so that negative result is restated as a **bound** —
  no advantage detected, with the smallest effect this design could see quoted next to it.
- **`scripts/figures.py`** — a forest plot per claim family and a noise/stability dot plot, as
  dependency-free deterministic SVG, with `runs/figures/stability.csv` carrying three noise statistics
  under stated definitions. Committed artifacts are SVG and CSV only: raster previews depend on
  `cairosvg`, which is not part of this repository's tooling, and an artifact the repository cannot
  regenerate is what case 5 warns about.
- **The defect family has six members** (`docs/defect-family.md`). Case 5 is the hand-assembled column.
  Case 6 is new and different in kind — *the checker stopped checking* — with two members found by running
  the task rather than by reading it: **6a**, four controls reported as detected while an implementation
  that scored 100/100 had moved every fragment they mutate into dead code; **6b**, a perfect submission
  reported as `exit 1` with two controls missed because the scored copy dropped the committed per-seed
  sweeps. Both fixes are guards that demonstrate their own liveness:
  `test_every_control_fragment_changes_the_numbers_it_mutates` and
  `test_the_scored_copy_can_run_the_repositorys_own_tests`.
- **The T-ADAM-01 variants, run end to end** (`runs/task-runs/`): 01B (Adam branch stubbed out)
  0.0 → 100.0/100, 01D (a negative control applied) 82.1 → 100.0/100, and 01C, a pre-registered
  first-moment ablation whose prediction came out **half wrong** (β1 = 0 is slower to the target and
  worse at the floor, 0/10 seeds either way; paired p = 0.0020). The ablation is now part of the
  contract (`make repro-ablation`).
- **The per-seed sweeps are committed** (7.4 MB, `runs/seed-sweep-*`). They are the input of the analysis
  and of the figures, and leaving them out — as this repository did until now — meant a fresh clone could
  not run its own tests and every scored copy reported a verdict about the copy.

### Full-tier verification for this release

```
$ python scripts/score_task.py --tier full
submission score: 100.0/100 (tier=full (all suites)) (474/474 checks, exit 0)
control[no-bias-correction]: detected (score 74.9/100, exit 1)
control[no-adaptive-scaling]: detected (score 77.0/100, exit 1)
control[ademamix-without-slow-ema]: detected (score 94.9/100, exit 1)
control[schedule-free-without-averaging]: detected (score 92.4/100, exit 1)

TASK RESULT: PASS
```

**Provenance, because the run and the tag are not the same commit** (the full version is in
`runs/task-runs/FULL-TIER.md`):

```
run at 3dabd96 → 100.0/100 (tier=full (all suites)) (474/474 checks, exit 0)
tag v0.10.0 = the commit carrying this file (`git rev-parse v0.10.0^{commit}`)
git diff --name-only 3dabd96..v0.10.0 =
  .gitignore, CHANGELOG.md, docs/defect-family.md, docs/release-corrections-pending.md,
  docs/release-notes-v0.10.0.published.md, expected/expected_ablation_adam_no_first_moment.json,
  runs/task-runs/{FULL-TIER.md,README.md,T-ADAM-01C.md}, tests/test_harness.py

expected/…ablation…json: the `notes` array gained one string; no numeric and no tolerance field changed,
so the 474 assertions and the four control scores are unaffected.
unit tests in the run's tree: 87 → 88 (the two case-6 guards). Tests, not asserted checks.
```

No re-run was done, and that is deliberate: a re-run would be evidence obtainable by reading a diff, and
the discipline this repository follows is to write the provenance down precisely rather than to cover it
with fresh compute. Had any numeric or tolerance field moved in `expected/`, a re-run would have been the
only honest option.

### Known limitations

Mechanism-level reproduction throughout; no number from any paper's table is claimed. One dataset family,
full-batch gradients, ten seeds, no formal significance test beyond §5.16 (which mostly *bounds* what ten
seeds can see: the minimal detectable effect is ≈ 0.99 σ_d, so most comparisons are "no evidence at this
budget"). The six scope axes are frozen; further axes only on a reviewer's request. The version metadata
in `pyproject.toml`, `autoresearch/__init__.py` and `CITATION.cff` still reads `0.2.0` — stale since that
release, unrelated to this tag, and left alone here rather than silently changed in a corrections release.

Archived on Zenodo; the concept DOI is 10.5281/zenodo.23003610 and each version has its own version DOI.
