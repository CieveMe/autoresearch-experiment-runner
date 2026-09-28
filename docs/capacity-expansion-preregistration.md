# Pre-registration: capacity expansion to `[64]` and `[16,16]`

Written **before** any of the new runs exist, so that the result can be cited as a prediction that was
confirmed or refuted rather than as a finding that was obvious afterwards. Date: 2026-09-29. Status of
the runs at the time of writing: none executed.

## Why expand capacity again

The capacity check in `REPRODUCTION.md` §5.10 produced three capacity-dependent results at `[32]` and
`[8,8]`: AdaGrad became the best arm on final test loss, the top-1 changed between training and test
loss, and AdEMAMix's no-advantage verdict stayed stable. It also produced a new methodological claim in
§5.11 — *the reproducibility of a fixed-threshold speed ranking varies with the model family's noise
level, and that noise is measurable* — based on three MLP suites being unstable while the logistic ones
were not. Both need a boundary test at capacities further from `[8]`.

## Protocol (fixed in advance, identical to the existing suites)

| item | value |
|---|---|
| Capacities | `[64]` (wider) and `[16,16]` (deeper); `[8]`, `[32]`, `[8,8]` already exist |
| Trainer | `mlp`, tanh hidden layers, deterministic init from the experiment seed |
| Budget | 200 epochs, full batch, one dataset family (800 rows, 2 features, noise 0.18) |
| Tuning | 21-trial sweep per capacity; rule unchanged: lowest final **training** loss, ties to the smaller value |
| Headline arms | `adamw_cosine` (tuned, baseline), `adamw_constant`, `adam`, `adagrad`, `ademamix`, `schedule_free_adamw` |
| Metric | `test_loss` pinned, `epochs_to_target` at 0.147 pinned alongside |
| Seeds | 10 per suite, paired per seed |
| Standard extras | threshold curves and the per-seed crossing-stability analysis |

## Hypotheses (with what would refute each)

**H1 — AdaGrad's advantage continues and strengthens.** At `[32]` AdaGrad was the best arm on mean test
loss with 9/10 per-seed wins; at `[8,8]` it won 7/10 and beat the cosine baseline in 10/10. Prediction:
it is best or tied-best on mean test loss at both new capacities, with at least 7/10 per-seed wins.
*Refuted if* it drops below 7/10 at either capacity, or if another arm beats it on mean test loss.

**H2 — The schedule-free architecture effect continues.** Schedule-free beats the tuned cosine on mean
test loss at `[8]` (9/10 seeds), `[32]` (8/10) and `[8,8]` (8/10). Prediction: it beats the tuned cosine
at both new capacities. *Refuted if* the tuned cosine wins at either capacity, in which case the effect
narrows to a range of capacities rather than the model family.

**H3 — AdEMAMix still has no advantage.** Prediction: it is better than the AdamW baseline in at most
2/10 seeds at each new capacity, and worse on mean test loss. *Refuted if* it wins ≥5/10 — which would
turn the repository's most robust negative result into a capacity-scoped one, reported as such.

**H4 — The train-versus-test divergence continues to grow.** At `[8]`/`[32]`/`[8,8]` the number of arms
moving at least two places between the training-loss and test-loss rankings was 2/4/5 (excluding the
logistic suites). Prediction: ≥4 arms move at least two places at each new capacity, and the top-1 arm
differs between the two metrics at least one of the two capacities. *Refuted if* the churn falls back
towards the small-capacity values.

**H5 — The §5.11 noise-correlation claim holds.** Ranking reproducibility at a fixed threshold was
stable on the logistic head (test-loss stdev ≈ 0.02) and unstable on all three MLP suites (stdev ≈
0.02–0.06). Prediction: the fixed-threshold winner at each new capacity is unstable **if** that suite's
per-seed test-loss standard deviation is ≥0.03, and stable if it is below. *Refuted if* a suite with high
stdev has a stable winner, or a low-stdev suite does not. This is a claim about the correlation between a
measurable quantity and reproducibility, and it is the one hypothesis here that can be wrong in either
direction.

**H6 — Adam is still not the fastest.** Prediction: at the pinned threshold Adam is not the best arm in a
majority of seeds at either capacity. *Refuted if* it wins a majority at either capacity, which would
turn "mid-pack on speed" into a capacity-scoped claim.

## Reporting rules, fixed before the results

1. Every hypothesis above is reported as **confirmed**, **refuted** or **boundary** (the effect holds in
   one capacity and not the other), with the numbers that decide it.
2. A refutation is written as a **scope correction, not a retraction**: earlier conclusions are labelled
   with the range where they were measured, and no earlier section is quietly rewritten.
3. The two metrics stay pinned and a claim names the one it is about; `epochs_to_target` is measured on
   the training curve, so "faster to converge" is never substituted for "better final loss".
4. Anything that contradicts a published statement gets an explicit correction note in the next release
   body, as `docs/defect-family.md` and §5.11 already do.
