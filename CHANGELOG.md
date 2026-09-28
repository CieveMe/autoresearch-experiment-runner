# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and this project uses
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- **Trainer adapter** (`autoresearch/trainers/`): the original model moved, unchanged, into
  `trainers/logistic.py`; a second, dependency-free `trainers/mlp.py` (two-layer tanh, deterministic
  initialisation) proves the adapter is real, and `trainers/registry.py` selects by config key.
  `autoresearch/model.py` is now a compatibility shim.
- **Optimizer registry** (`autoresearch/optimizers.py`): every update rule in one place, written
  against a plain parameter vector so both trainers share it. Adds `adamw` (decoupled weight decay)
  and `ademamix`.
- **Schedules** (`autoresearch/schedules.py`): constant (default, exactly 1.0 so existing arithmetic is
  untouched), cosine, warmup+cosine, and AdEMAMix's α / β3 warmups.
- **Data sources** (`autoresearch/datasets.py`): synthetic (default) plus local CSV/JSON; URLs are
  refused before they are opened.
- **AdEMAMix (arXiv:2409.03137) suite**: `examples/ademamix.json` + `examples/ademamix-sweep.json` +
  `expected/expected_ademamix.json` + `docs/papers/ademamix-2024.md`. Result: the paper's
  faster-than-AdamW claim **is not reproduced** at this scale (identical epochs-to-target in 10/10
  seeds; the paper's own warmup scheme scaled to this budget is 4.5× slower).
- Thirteen more unit tests (30 total), including an MLP gradient check against finite differences and
  the α = 0 identity with AdamW.
- **The self-scepticism re-run**: both suites were repeated with the MLP trainer, with every family
  retuned for that model (`examples/optimizers-mlp.json`, `examples/ademamix-mlp.json` plus their
  sweeps). The logistic-head conclusions survive: Adam is mid-pack on time-to-target on both models
  (MLP: 20.3 epochs against AdaGrad 6.2 and momentum 7.0) and the paper's warmup scheme is the worst
  arm on both (MLP mean test loss 0.14269 / 0.15261 against AdamW's 0.13218).
- `examples/optimizers-mlp-sweep.json` (24 trials) and `examples/ademamix-mlp-sweep.json` (17 trials),
  committed with their curves, so the MLP rates can be re-derived rather than trusted.

### Changed

- `scripts/repro.py` runs **five** suites (121 asserted checks, ~18 s); `scripts/score_task.py`
  aggregates over all suites and its negative controls now name the file they mutate.

### Added (schedule-free follow-up, same release)

- **Schedule-Free AdamW / SGD** (`autoresearch/optimizers.py`, transliterated from
  `facebookresearch/schedule_free`, Apache-2.0) with the averaged-sequence evaluation point wired
  through `optimizers.eval_params()`; `examples/schedule-free.json` compares it against a **tuned**
  cosine baseline (21-trial sweep over learning rate × min-LR factor) and a constant-rate baseline, at
  a 200-epoch budget. Result: "at worst matches" is roughly right, "out-performs" is not — schedule-free
  is 0.3% behind the tuned cosine and loses all ten seeds, while a constant rate beats both.
- `tests/test_schedule_free.py`: the port is cross-checked step by step against a literal
  re-implementation of the reference rule, plus warmup, determinism and eval-point checks (39 tests
  total).
- `docs/papers/schedule-free-2024.md`.

### Added (threshold curves, same release)

- **`scripts/threshold_curve.py`** turns every single-point `epochs_to_target` number into a curve:
  a 13-point threshold grid per suite, with the fastest arm, the arms that never arrive, and the
  threshold where the ranking changes, plus an SVG that marks the suite's pinned threshold. Outputs are
  committed under `runs/threshold-curves/` and read from the committed loss curves, so no experiment is
  re-run to produce them.
- The result is a scope correction rather than a new claim: **four of six suites have a
  threshold-dependent winner**, three of them at their pinned threshold, while `schedule-free` (logistic)
  is stable at all thirteen thresholds and `ademamix` (logistic) oscillates five times inside a
  0.0014-wide band (i.e. its two arms are tied there and "fastest" is noise). Six more unit tests (45
  total).

### Added (capacity check, same release)

- **Two more capacities**, `[32]` and a two-layer `[8,8]`, with every arm retuned for the model it runs
  on (`examples/capacity-h32.json` / `capacity-h8x8.json` plus 21-trial sweeps) and ten seeds each.
  Results: **AdEMAMix's "no advantage" is stable at every capacity and on both model families** (1/10
  seeds better than the AdamW baseline in both new runs); the **schedule-free flip is an architecture
  effect, not a capacity effect** (it beats the tuned cosine at all three MLP capacities and loses on
  the logistic head); **AdaGrad wins on final test loss once the model has room to overfit** (9/10 and
  10/10 seeds better than the cosine baseline); and train-loss versus test-loss rankings diverge as
  capacity grows, so both are pinned. Nine suites / 229 asserted checks.

### Added (crossing stability, same release)

- **Per-seed crossing analysis** (`scripts/threshold_curve.py --seeds-dir ... --compare A:B`): locates the
  threshold where the strict winner between two arms flips, in every seed of a seed sweep, and reports
  whether the arm that is faster at the suite's pinned threshold is the same every time. Outputs in
  `runs/threshold-curves/*-crossing-stability.md` and `CROSSINGS.md`.
- **Result, and it is a scope correction again**: "a crossing exists" is not "the crossing is stable".
  The logistic `optimizers` pair crosses in 10/10 seeds but the position moves across a 0.0456 band —
  while `adagrad` is faster at the pinned threshold in every seed, which is the usable statement. The
  `schedule-free-mlp` pair crosses in 10/10 seeds but **the winner at the pinned threshold changes
  between seeds**, so that card's seed-7 speed sentence is now labelled single-seed. Two pairs
  (`capacity-h32`, `capacity-h8x8`) turn out to have **tie bands rather than crossings**.
- **Fixed, third defect of the same family**: the analysis resolved ties with `min()` over
  `(epoch, name)` tuples — alphabetically — in two places, which manufactured the "crossing" reported
  for `capacity-h32`. Ties are now reported as `tie: a, b`, the crossing detector skips tied thresholds,
  and tests pin both behaviours. Nine more tests (55 total).
- **`REPRODUCTION.md` §5.12 — which metric ranks the methods**: both final-quality numbers are pinned, the
  top-1 flips between training and test loss exactly at the two larger capacities, rank churn grows with
  capacity (0 → 2 → 3 → 4 → 5 arms moving at least two places), and `epochs_to_target` is measured on the
  training curve, so "faster" and "better" must stay separate claims.
- **`docs/defect-family.md`** — the three defects of the "number came from the tooling" family as a named
  section: the inverted metric direction, the seed that reached only the data split, and the tie resolved
  alphabetically, each with the check that caught it and the test file that guards it.
- **`docs/release-notes-v0.6.0.published.md`** corrects, in the open, the sentence v0.5.0 published about
  the `[32]` suite's crossing at 0.1417.

### Added (capacity expansion, next release)

- **Pre-registered capacity expansion** (`docs/capacity-expansion-preregistration.md`, committed before the
  runs): six falsifiable hypotheses with the protocol, the decision rules and what would refute each,
  covering AdaGrad's strengthening, the schedule-free architecture effect, AdEMAMix's no-advantage
  verdict, the train/test divergence, the §5.11 noise-correlation claim and Adam's speed standing.
- **Two more capacities**, `[64]` and a two-layer `[16,16]`, with 17-trial tuning sweeps per capacity
  committed before the headline runs, ten seeds each, and threshold curves as standard. Overfitting
  becomes dominant at `[16,16]`: the arm with the lowest training loss (AdEMAMix, 0.09444) has the worst
  test loss (0.18107), while schedule-free reaches the best test loss (0.11778).

### Added (activation expansion, same release)

- **ReLU and GELU hidden activations** in the MLP trainer (`hidden_activation` config key; exact erf GELU,
  its derivative checked against finite differences like the other two). `tanh` remains the default and
  its arithmetic is unchanged: every existing MLP suite still verifies bit for bit.
- **A fourth defect of the "the number came from the tooling" family, found while adding the activations.**
  The patch re-indented the gradient-accumulation block into the delta loop, which doubled every gradient
  for a network with two hidden layers and left one hidden layer correct; the finite-difference check only
  covered one hidden layer, so it passed. What caught it was a deep suite's pinned expectations failing on
  a fresh run (max |numerical − analytic| = 0.245 before the fix, 9.2 × 10⁻¹¹ after). The check now runs
  `[3]` and `[3, 3]` for tanh, ReLU and GELU. Recorded as case 4 in `docs/defect-family.md`.
- **The `[32]` capacity re-run with ReLU and with GELU**, every arm retuned (18-trial sweeps), ten seeds,
  threshold curves, against three pre-registered predictions. A1 confirmed (schedule-free beats the tuned
  cosine under both activations, 8/10 seeds each), A3 confirmed (the training/test ranking trap appears
  under both), and **A2 refuted in an informative way**: AdEMAMix is a tie against AdamW at the same rate
  but wins against a cosine-scheduled AdamW under ReLU/GELU — because under those activations the
  scheduled baseline is the weakest arm, not AdEMAMix being good.
- **Selectable hidden normalisation and weight initialisation** (`hidden_norm`: none/layernorm/batchnorm,
  `init_scheme`: xavier/he/plain). `none` and `xavier` are the defaults and the original arithmetic, so
  every earlier pinned number still verifies bit for bit. The forward pass became batch-shaped and the
  backward chain layer-major, because normalisation is where rows stop being independent; the
  finite-difference check now varies normalisation as well as activation and depth (18 checks).
- **The normalisation/initialisation robustness check** (pre-registered N1-N4 in
  `docs/normalization-init-preregistration.md`, committed before the runs): four variants at the `[32]`
  reference capacity on the reference tuning grid, ten seeds, threshold curves. **N1 is refuted as a
  general claim** — schedule-free's edge over the tuned cosine is stronger under He init (9/10 seeds),
  a tie under batchnorm and plain init (5/10 each, mean gap below 0.001) and reverses under layernorm
  (the cosine wins 7/10); both arms moved, so it is not the §5.14 pattern. **N2's direction holds in 3 of
  4**, while its pre-registered win-count criterion fails (8/10 "wins" with a mean difference of 9e-5 —
  a win count without a magnitude is not evidence, the third arrival of that lesson). **N3 confirmed.**
  **N4 is refuted on mechanism**: no variant lowered the best arm's σ below the reference's 0.0210, so
  "normalisation reduces the noise floor" is wrong — while the σ/reproducibility correlation of §5.11
  held again. §5.15 records that this is the **last experimental axis**; the scope table now has six.
- **`scripts/paired_stats.py`**: exact paired tests over every committed sweep (sign test and Wilcoxon
  signed-rank by enumeration), effect sizes (d_z, matched-pairs rank-biserial, probability of
  superiority), a 95% t interval for the mean difference and a deterministic bootstrap interval for the
  median, the minimal detectable effect at 80% power, and a Holm-Bonferroni adjustment within a
  **declared family** rather than across everything printed. `make stats` regenerates
  `runs/paired-tests/`. The wording rule is enforced in code and tested: a test that fails to reject is
  reported as *no evidence of a difference at this budget*, never as "no difference".
- **What the tests changed about the claims** (§5.16). Across all 78 comparisons nothing survives a
  family correction (smallest adjusted p = 0.15); inside their declared families, the schedule-free
  result is statistically established at exactly one suite (`capacity-h16x16`, 10/10 seeds, adjusted
  p = 0.0195, 1/10) and the AdEMAMix family has none (0/11). The second negative result is therefore
  restated as a **bound** — "no advantage detected, and here is the smallest effect this design could
  have seen" — because a test that fails to reject cannot confirm a null. No pinned number moved and no
  run was repeated.
- **`scripts/figures.py`** (dependency-free SVG): a forest plot per claim family (median paired
  difference with its bootstrap interval, the surviving comparison marked) and a dot plot of
  noise against ranking reproducibility, plus `runs/figures/stability.csv` carrying three noise
  statistics and the winner counts under stated definitions. `make figures` regenerates them; the
  figures are deterministic and `tests/test_figures.py` checks the geometry as well as the content.
- **Correction: §5.13's σ column was not reproducible and the correlation built on it is withdrawn.**
  Drawing the stability figure required recomputing "per-seed test-loss σ of the best arm" for every
  suite, and five of the ten published rows disagreed: the hand-assembled column carries different
  arms' σ in different rows (0.0646 for `capacity-h8x8` is `adamw_constant`; the best arm is `adagrad`
  at 0.02271). Recomputed under one stated definition the relationship is not monotone —
  `optimizers-mlp` has the second-lowest noise in the corpus (0.02019) and five different winners, while
  the two activation suites sit at 0.0217 with one winner each. §5.11 finding 7, §5.13's H5 and §5.15's
  N4 are corrected in place, recorded as **case 5** in `docs/defect-family.md`, and must be stated as a
  correction in the next release body (`v0.9.0` is published and is not rewritten).
- **The schedule-free comparison on the MLP** (`examples/schedule-free-mlp.json`, 15-trial sweep):
  the direction **flips** — schedule-free AdamW beats the tuned cosine in 9/10 seeds here, whereas it
  lost 10/10 on the logistic head — while the constant learning rate still wins on both models (9/10).
  The weak claim ("at worst matches") survives both runs; the strong claim does not. Seven suites /
  171 asserted checks.

### Fixed

- Trial configs did not inherit the experiment's `seed`, so a "10-seed" MLP run varied the data split
  while initialising from identical weights. `TRIAL_INHERITED_KEYS` now includes `seed`; the logistic
  trainer never read it, so the earlier pinned numbers are unaffected and still verify.

## [0.2.0] — 2026-09-28

The release that turns the paper's actual headline claim — *faster convergence* — into a measurable
experiment, and reports the result even though it contradicts the paper.

### Added

- **Convergence-speed experiment** (`examples/optimizers.json`): `epochs_to_target` (the first epoch
  whose training loss reaches a target near the converged floor) for Adam against SGD, heavy-ball
  momentum, AdaGrad and RMSProp, all at a matched 120-epoch budget.
- **Learning-rate sweep** (`examples/optimizers-sweep.json`, 24 trials): each optimizer family picks
  its learning rate by the same rule (lowest final training loss, ties to the smaller rate), so the
  comparison does not measure tuning luck. Curves are committed, so any other target can be re-scored.
- **Bias-correction ablation**: `bias_correction: false` on Adam, so the paper's correction term can
  be switched off and measured.
- **Per-epoch loss curves** in every result, exported to `loss-curves.csv`.
- **Release metadata**: `CHANGELOG.md`, `.zenodo.json`, `docs/release-checklist.md`.
- Five more unit tests (17 total) covering the new optimizers, target reaching and metric direction.

### Changed

- `scripts/repro.py` now runs **both** experiment suites in one command (46 asserted checks) and takes
  `--suite main|optimizers|all`; its table prints `epochs_to_target`.
- `scripts/seed_sweep.py` handles "never reached the target" (`null`) in means, ranking and paired
  comparisons instead of crashing or silently dropping the trial.

### Fixed

- `config_sha256` was computed from raw bytes, so a Windows checkout (`core.autocrlf=true`) reported a
  different hash for the same revision. The hash now normalizes line endings, with a regression test.
- `epochs_to_target` was missing from one copy of the "lower is better" metric list, which inverted the
  seed-sweep ranking (RMSProp was reported as the per-seed winner instead of AdaGrad). The set now has
  a single definition plus a test that fails when a new metric has no declared direction.

### Result reported by this release

AdaGrad reached the target first in **10/10 seeds** (mean 4.7 epochs vs Adam's 22.6); SGD with momentum
beat Adam 10/10 as well; RMSProp was the slowest adaptive method; plain SGD never reached the floor at
any swept rate. Disabling Adam's bias correction reached the target 10/10 faster (12.5 ± 4.6 epochs)
with a marginally lower final loss. Full analysis, caveats and the raw curves are in
`REPRODUCTION.md` §5.4 and `runs/optimizers-verified/`.

### Known limitations

- Mechanism-level, not benchmark-level: the paper's MNIST / CIFAR-10 / IMDB experiments are **not**
  reproduced and no number from the paper's tables is claimed.
- Full-batch gradients, no learning-rate schedules, one dataset family, ten seeds, no formal
  significance test, and a learning-rate grid that is not saturated (every adaptive family's best rate
  sits at or beyond the largest swept value).
- The convergence-speed ranking depends on the chosen target (0.16); both the tight and a looser
  target regime are committed so the analysis can be redone.

## [0.1.0] — 2026-09-28

First public release (tag `v0.1.0`, commit `0dd90e3`). Every number in this repository is regenerated
and asserted by one command (`python scripts/repro.py`), and the assertion harness is itself checked
against deliberately broken implementations.

### Added

- **Adam mechanism reproduction** (`examples/classification.json`): the first/second moment estimates
  and bias correction from Algorithm 1 of arXiv:1412.6980, implemented in dependency-free Python and
  compared against fixed-learning-rate SGD under a fixed seed and epoch budget.
- **One-command entry point** (`scripts/repro.py`): environment report, config validation, run,
  expected-number verification, unit tests; non-zero exit on any mismatch.
  `make repro` and `docker compose up --build` run the same path.
- **Expected-number contract**: `expected/expected_metrics.json` (17 assertions) and
  `expected/expected_optimizers.json` (28 assertions) pin every reported number with explicit
  tolerances; `scripts/verify_results.py` enforces them.
- **Multi-seed aggregation** (`scripts/seed_sweep.py`): means, standard deviations, per-seed win
  counts and paired per-seed improvements, so no claim rests on a single run.
- **Task contract** (`TASK.md` / `TASK.zh.md`): objective, command surface, K1–K7 acceptance criteria,
  0–100 partial-credit scoring, failure modes with detection, retry protocol, four task variants.
- **Falsifiability checks** (`scripts/score_task.py`): scores a submission and runs negative controls
  (drop bias correction; drop adaptive scaling) that must be detected.
- **Reproduction report** (`REPRODUCTION.md`): what is and is not reproduced, deviations from the
  paper, limitations, and the negative result in the convergence-speed experiment.
- CI on Python 3.10/3.12 plus a container job, `Dockerfile`, `compose.yaml`, `Makefile`, MIT licence,
  `CITATION.cff` and 8 unit tests.
