This release varies the last modelling choice that had never been varied — the hidden activation — and in
the middle of it found a defect in the harness itself. One pre-registered prediction came out as usefully
wrong, one was confirmed, and the defect is recorded as the fourth case of the same family.

### What is in it

- **ReLU and GELU hidden activations** (`hidden_activation` config key; `tanh` remains the default and its
  arithmetic is unchanged). GELU uses the exact erf formulation and its derivative, like the other two, is
  verified against finite differences.
- **The `[32]` capacity re-run with each of the three activations**, every arm retuned for its activation
  (18-trial sweeps), ten seeds, threshold curves — against three predictions committed in
  `docs/capacity-expansion-preregistration.md` before the runs.
- **Thirteen suites**: 345 asserted checks, 57 unit tests, four negative controls.

### Verdicts

| # | prediction | verdict | evidence |
|---|---|---|---|
| A1 | the schedule-free architecture effect does not depend on the activation | **confirmed** | schedule-free beats the tuned cosine on mean test loss and in 8/10 seeds under both ReLU and GELU; the effect now holds for tanh, ReLU and GELU |
| A2 | AdEMAMix's no-advantage verdict does not depend on the activation | **refuted, usefully** | against the tuned-cosine baseline it wins 9/10 (ReLU) and 7/10 (GELU); against AdamW **at the same learning rate** the difference is 4 × 10⁻⁵ and −1.7 × 10⁻⁴, i.e. still a tie. What moved is the baseline, not AdEMAMix |
| A3 | the metric trap does not depend on the activation | **confirmed** | under both activations the best training loss belongs to `adamw_cosine` and the best test loss to `adagrad`, with four of six arms moving at least two places |

**A2 is the result worth reading.** Under tanh, a cosine-scheduled AdamW was the strongest of the AdamW
variants, so "AdEMAMix has no advantage over the baseline" and "AdEMAMix has no advantage over AdamW" were
the same statement. Under ReLU and GELU the scheduled variant has the *lowest training loss and the worst
test loss* of the six arms, so AdEMAMix beats it — while remaining a tie against AdamW at the same rate.
The card's claim is now stated at that precision: **no advantage over AdamW at matched settings**, on both
model families and five capacities, with the α = 0 identity as the correctness check; against a scheduled
AdamW the outcome is activation-scoped. Which baseline is strong is itself a property of the
(optimizer, activation) pair, not of the optimizer.

### The fourth defect of the same family, found by a pinned number

While adding the activations, a patch re-indented the gradient-accumulation block into the loop that
computes the deltas. For a network with **two** hidden layers the accumulation then ran twice and doubled
every gradient; for one hidden layer it ran once and stayed correct — and the finite-difference test only
covered one hidden layer, so it passed. What caught it was a deep suite's pinned expectations failing on a
fresh run, followed by an independent transliteration of the pre-refactor arithmetic showing a factor of
exactly two (max |numerical − analytic| = 0.245 before the fix, 9.2 × 10⁻¹¹ after).

The check now varies depth as well as activation — `test_gradients_match_numerical_differences` runs `[3]`
and `[3, 3]` for tanh, ReLU and GELU — and `docs/defect-family.md` lists this as case 4 alongside the
inverted metric direction, the seed that reached only the data split, and the tie resolved alphabetically.
Four cases, four different mechanical checks, one shared lesson: the number can come from the tooling
rather than from the experiment.

**Blast radius, measured rather than assumed.** After the fix, the two activation suites (single hidden
layer) reproduced bit-identically, and the two-hidden-layer capacity suites returned to their previously
pinned values. So the defect affected only the two-hidden-layer runs, and it was introduced in this
release's own refactor rather than being present in any earlier published number.

### Protocol and coverage

Thirteen suites: the logistic-head family, MLP capacities `[8]`, `[32]`, `[8,8]`, `[64]`, `[16,16]`, and the
`[32]` capacity under ReLU and GELU; four method families (Adam-family baselines, AdaGrad, AdEMAMix
arXiv:2409.03137, Schedule-Free arXiv:2405.15682); 200 epochs, full batch, ten seeds per paired
comparison, thresholds pinned and drawn on every curve. `--tier core` skips the ten capacity and
activation suites for local iteration and always names them; CI runs `full` on `main` and on tags.

### Full-tier verification for this release

```
$ python scripts/repro.py --tier full
artifacts[activation-gelu]: runs/activation-gelu
verified:  345 checks, 0 failures
RESULT: PASS

$ python scripts/score_task.py --tier full
submission score: 100.0/100 (tier=full (all suites)) (345/345 checks, exit 0)
control[no-bias-correction]: detected (score 76.8/100, exit 1)
control[no-adaptive-scaling]: detected (score 79.1/100, exit 1)
control[ademamix-without-slow-ema]: detected (score 94.8/100, exit 1)
control[schedule-free-without-averaging]: detected (score 92.5/100, exit 1)
TASK RESULT: PASS
```
Thirteen suites, 345 asserted checks, 57 unit tests, four negative controls all detected, and the task
score 100.0/100 at the full tier.

### Known limitations

Mechanism-level reproduction throughout: no number from any paper's tables is claimed. One dataset family,
full-batch gradients, ten seeds. Both metrics are pinned and a claim names the one it is about — the
activation runs add a third scope label on top of threshold, model family and capacity: the pair
(optimizer, baseline) can change meaning with the activation. Normalisation layers and initialisation
schemes remain untested and are the next open question.

Archived on Zenodo; the concept DOI is 10.5281/zenodo.23003610 and each version has its own version DOI.
