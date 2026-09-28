This release gives every conclusion in this repository an explicit scope, and it corrects one sentence
that v0.5.0 published. It contains no new training runs: everything here is analysis of the committed
loss curves, which is why the whole release took minutes rather than hours.

### Correction to v0.5.0

v0.5.0's release body says that in the `[32]` capacity suite "the lead passes to `adam` at 0.1417". **That
statement was produced by a bug in the analysis code and is wrong.** The three leading arms (`adam`,
`adamw_constant`, `ademamix`) reach every threshold from 0.1417 upward on *exactly the same epoch*:
they are tied, and the code was resolving ties with `min()` over `(epoch, name)` — i.e. in alphabetical
order — in two places. The corrected reading is in `REPRODUCTION.md` §5.10 finding 6 and §5.11: `ademamix`
is strictly faster below ~0.1417, and above it the leading arms are tied. v0.5.0 is published and
stays as it is; this note is the correction, and the defect is documented with the check that now
catches it in `docs/defect-family.md`.

### What is in it

- **Crossing stability across seeds** (`scripts/threshold_curve.py --seeds-dir ... --compare A:B`): the
  threshold where the strict winner between two arms flips, located in every seed of a seed sweep, plus
  whether the arm that is faster at the suite's pinned threshold is the same every time. Outputs in
  `runs/threshold-curves/`.
- **Which metric ranks the methods** (`REPRODUCTION.md` §5.12): both final-quality numbers are pinned and
  the report says which claim belongs to which.
- **The defect family as a named section** (`docs/defect-family.md`): three ways a reported number came
  from the tooling rather than from the experiment, each with the check that caught it and the test file
  that now guards it.

### Protocol this release covers

Nine suites: one logistic-head family and three MLP capacities (`[8]`, `[32]`, two-layer `[8,8]`), each
with every arm retuned for the model it runs on (21-trial sweeps committed alongside). Budget: **200
epochs**, full batch, ten seeds for every paired comparison, target thresholds pinned per suite and
marked on every curve. Four 2024-era method families are covered: Adam-family baselines, AdaGrad,
RMSProp, AdEMAMix (arXiv:2409.03137) and Schedule-Free (arXiv:2405.15682).

### Crossing stability across seeds (seed sweep, 10 seeds per suite)

| suite | pair | crossings | mean position | spread | winner at the pinned threshold |
|---|---|---:|---:|---:|---|
| `optimizers` (logistic) | adam_no_bias_correction vs adagrad | 10/10 | 0.1370 | 0.0456 | **stable: `adagrad`** |
| `optimizers-mlp` | adam vs sgd_momentum | 7/10 | 0.1167 | 0.0530 | **unstable** |
| `schedule-free` (logistic) | schedule_free_adamw vs adamw_cosine | 0/10 | — | — | **stable: `adamw_cosine`** |
| `schedule-free-mlp` | adamw_constant vs schedule_free_adamw | 10/10 | 0.1192 | 0.0505 | **unstable** |
| `ademamix` (logistic) | ademamix_tuned vs adamw | 1/10 | 0.1296 | — | **stable: tie** |
| `ademamix-mlp` | ademamix_warmup_45 vs adamw | 2/10 | 0.1329 | 0.0026 | **unstable** |
| `capacity-h32` | ademamix vs adam | 0/10 | — | — | **stable: tie** |
| `capacity-h8x8` | ademamix vs adam | 5/10 | 0.0947 | 0.0528 | **stable: tie** |

Two conclusions. First, **"a crossing exists" is not "the crossing is stable"**: `optimizers` crosses in
every seed but the crossing moves across a 0.0456-wide band, so the usable statement is the one about the
pinned threshold, where `adagrad` is faster in 10/10 seeds. Second, **every suite whose fixed-threshold
speed ranking is unstable is an MLP suite** (`optimizers-mlp`, `schedule-free-mlp`, `ademamix-mlp`); on
the two-parameter logistic head those rankings reproduce across seeds. The same split shows up in the
test-loss standard deviations, which are roughly twice as large on the MLP suites.

One consequence, stated plainly because it narrows an earlier claim: for `schedule-free-mlp` the seed-7
sentence "schedule-free reaches the target in 11 epochs against the constant rate's 23" is **a
single-seed statement**. The suite's *test-loss* result — schedule-free beats the tuned cosine in 9/10
seeds — is a different measurement and is **not** affected. The paper card keeps both sentences side by
side so that the scope correction is not mistaken for a retraction.

### Which metric ranks the methods (seed 7, both numbers pinned)

| suite | top arm by training loss | top arm by test loss | arms moving ≥2 places |
|---|---|---|---:|
| `optimizers` (logistic) | adam_no_bias_correction | adam_no_bias_correction | 2 |
| `optimizers-mlp` | adam | adam | 1 |
| `schedule-free` (logistic) | adamw_constant | adamw_constant | 0 |
| `schedule-free-mlp` | adamw_constant | adamw_constant | 2 |
| `ademamix` (logistic) | ademamix_tuned | ademamix_tuned | 0 |
| `ademamix-mlp` | ademamix_warmup_45 | ademamix_warmup_45 | 3 |
| **`capacity-h32`** | **ademamix** | **adagrad** | 4 |
| **`capacity-h8x8`** | **ademamix** | **schedule_free_adamw** | 5 |

The top-1 flips exactly at the two larger capacities, and rank churn grows with capacity (0 → 2 → 3 → 4 →
5 arms moving at least two places). `epochs_to_target` is measured on the *training* curve, so
"faster to converge" and "better final test loss" must be reported as the two different claims they are
— at `[8,8]` the fastest-converging arms are also the worst generalisers.

### The defect family (named section, not an appendix)

Three defects were found in this repository, all of the same kind — a reported number produced by the
harness rather than by the experiment — and each was caught by a *different* mechanical check:

| case | what the number was | what it should have been | check | test file |
|---|---|---|---|---|
| 1 | a ranking in the wrong direction | a ranking in the declared direction | `test_every_metric_the_runner_can_rank_has_a_known_direction` | `tests/test_metric_direction.py` |
| 2 | ten runs, one initialisation | ten runs, ten seeds | `test_a_multi_seed_sweep_produces_distinct_seeds_not_a_fixed_value` | `tests/test_seed_contract.py` |
| 3 | a leader produced by alphabetical order | a tie | `test_identical_curves_have_no_crossing` | `tests/test_threshold_curve.py` |

None of the three would have been caught by looking harder at the results; all three produced tables that
looked reasonable. `docs/defect-family.md` records each case with its symptom, cause, fix, the check that
catches it and the generalisation for a new experiment.

### Tiers: full coverage on main and on tags

`scripts/repro.py --tier core` skips the two capacity suites for local iteration and **always says so**
(`tier=core; NOT run: capacity-h32, capacity-h8x8`); the default is `full`, and CI runs `full` on `main`
and on tags while pull requests may run `core`. The release body below quotes a full-tier run, as
`docs/release-checklist.md` now requires.

### Full-tier verification for this release

```
$ python scripts/repro.py --tier full
artifacts[capacity-h8x8]: runs/capacity-h8x8
verified:  229 checks, 0 failures
RESULT: PASS

$ python scripts/score_task.py --tier full
submission score: 100.0/100 (tier=full (all suites)) (229/229 checks, exit 0)
control[no-bias-correction]: detected (score 81.2/100, exit 1)
control[no-adaptive-scaling]: detected (score 81.2/100, exit 1)
control[ademamix-without-slow-ema]: detected (score 94.3/100, exit 1)
control[schedule-free-without-averaging]: detected (score 93.0/100, exit 1)
TASK RESULT: PASS
```

### Known limitations

Mechanism-level reproduction throughout: no number from any paper's tables is claimed. Full-batch
gradients, one dataset family, four model configurations and ten seeds with test-loss standard deviations
of 0.02–0.06 — enough to separate 0.13 from 0.19, not enough to resolve a 0.0003 difference. Crossing
positions are located on each seed's own grid, so their means sit below the converged floors whenever a
curve overfits (its tightest reachable point is an early minimum). Capacity expansion to `[64]` and
deeper nets is explicitly left to the next release.

Archived on Zenodo; the concept DOI is 10.5281/zenodo.23003610 and each version has its own version DOI.
