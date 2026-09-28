# Pre-registration: normalisation and initialisation as a robustness check

Written **before** any of the new runs exist, so that the result can be cited as a prediction that was
confirmed or refuted rather than as a finding that was obvious afterwards. Date: 2026-09-28. Status of
the runs at the time of writing: none executed.

## Scope, fixed in advance: this is a robustness check, not a new topic

The repository's two negative results are:

* **the schedule-free architecture effect** — on the MLP trainer, Schedule-Free AdamW beats a tuned
  cosine-scheduled AdamW on mean test loss (`REPRODUCTION.md` §5.7, §5.8, §5.10, §5.13, §5.14);
* **AdEMAMix's no-advantage verdict** — at matched settings AdEMAMix does not beat AdamW on this task
  (§5.5, §5.10, §5.13, §5.14).

Every one of those measurements was taken with the same two modelling choices: Xavier/Glorot
initialisation and no normalisation of the hidden pre-activations. This batch varies exactly those two
choices and asks **whether the two negative results depend on them**. It does not open a new question,
and no new optimizer, dataset or metric is introduced.

The activation expansion (§5.14) showed why the framing matters: its one refutation (A2) was not
"AdEMAMix got better", it was "the *baseline* got worse under the new activation". The same distinction
is a **reporting rule** here (see below), not a hypothesis.

## Protocol (identical to the capacity and activation expansions)

| item | value |
|---|---|
| Reference | `capacity-h32`: `[32]`, tanh, no normalisation, Xavier init — already pinned and re-verified bit for bit under the new code |
| Variants | `layernorm`, `batchnorm` (normalisation, Xavier init) and `he`, `plain` (initialisation, no normalisation) |
| Trainer | `mlp`, `[32]` hidden units, deterministic init from the experiment seed |
| Budget | 200 epochs, full batch, one dataset family (800 rows, 2 features, noise 0.18) |
| Tuning | 18-trial sweep per variant; rule unchanged: lowest final **training** loss, ties to the smaller value |
| Headline arms | `adamw_cosine` (tuned, baseline), `adamw_constant`, `adam`, `adagrad`, `ademamix`, `schedule_free_adamw` |
| Metrics | `test_loss` pinned, `epochs_to_target` at 0.147 pinned alongside |
| Seeds | 10 per suite, paired per seed |
| Standard extras | threshold curves and the per-seed crossing-stability analysis |

Definitions, so the numbers are reproducible rather than named:

* **layernorm** standardises each row's hidden pre-activations across the units of that layer;
  **batchnorm** standardises each unit's pre-activations across the batch. Both use the biased variance
  and ε = 1e-5, and neither has an affine parameter or running statistics — the statistics are
  recomputed on whichever batch is evaluated. This is the *scale-and-centre* question only, and it is
  labelled as such wherever the result is quoted.
* **Xavier** is the existing limit `sqrt(6/(fan_in+fan_out))` and remains the default; **He** is
  `sqrt(6/fan_in)`; **plain** is a fixed 0.05, which is what a hand-written trainer starts with.

## Hypotheses (with what would refute each)

**N1 — the schedule-free architecture effect survives both change families.** Prediction: under each of
the four variants, Schedule-Free AdamW beats the tuned-cosine baseline on mean test loss.
*Refuted if* the tuned cosine wins under any variant, in which case the effect is labelled
normalisation- or initialisation-scoped rather than named as a property of the model family.

**N2 — AdEMAMix's no-advantage verdict survives both change families.** Prediction: under each of the
four variants it is better than the AdamW baseline in at most 2/10 seeds and worse on mean test loss.
*Refuted if* it reaches ≥5/10 under any variant, which would turn the repository's most robust negative
result into a scoped one.

**N3 — the metric trap (§5.12) survives.** Prediction: in at least 3 of the 4 variants the best arm by
training loss is not the best arm by test loss. *Refuted if* the two metrics agree at the top in three or
more variants, which would mean the trap is an artefact of the unnormalised/unscaled regime.

**N4 — a controlled test of the §5.11 noise claim.** §5.11/§5.13 found that a fixed-threshold ranking
reproduced across ten seeds only in the lowest-σ suites (σ ≈ 0.020), while σ ≥ 0.021 produced two to four
different winners. Normalisation is the first change in this repository that is expected to *reduce* the
per-seed test-loss standard deviation of the same model at the same capacity. Prediction: at least one
normalisation variant has a lower σ than the `[32]` reference (0.0210), **and** if σ drops, the
fixed-threshold winner in that variant becomes stable across the ten seeds. *Refuted if* a variant lowers
σ but keeps an unstable winner, or if no variant lowers σ at all. This is the one hypothesis here that can
be wrong in either direction, and it is the reason the batch is worth running: it is the only way to vary
the noise of a fixed model deliberately.

## Reporting rules, fixed before the results

1. Every hypothesis is reported as **confirmed**, **refuted** or **boundary**, with the numbers that
   decide it.
2. **A flip is attributed to the arm that moved.** If a conclusion changes under a variant, the report
   compares that variant's own arms with the reference's own arms and states which one changed, the way
   §5.14 did for A2. "The method got better/worse" is only written when that arm's own numbers moved.
3. **Effect magnitudes are reported as they come out**, not rescaled into a verdict. A result whose
   direction holds but whose size changes by an order of magnitude is written as a scope correction
   ("holds in direction, range unchanged/scoped"), never as a retraction and never as "confirmed".
4. **This is the last experimental axis.** The scope table in `REPRODUCTION.md` has six axes —
   threshold, model family, capacity, metric, activation, normalisation/initialisation. After this batch
   the axis list is frozen; further axes are added only if a reviewer asks for one.
5. The two metrics stay pinned and a claim names the one it is about. `epochs_to_target` is measured on
   the training curve, so "faster to converge" is never substituted for "better final loss".
