This release varies the last two modelling choices that had never been varied — how the hidden
pre-activations are normalised and how the weights are initialised — as a **robustness check of the two
negative results**, not as a new question. Four pre-registered hypotheses were tested; one general claim
had to be narrowed, one pre-registered criterion failed in a way that is worth more than the hypothesis
it was testing, and one mechanism was refuted while the correlation it was meant to explain held again.
With this axis the scope table is complete, and it is frozen here.

### What is in it

- **Selectable hidden normalisation and initialisation** — `hidden_norm: none|layernorm|batchnorm` and
  `init_scheme: xavier|he|plain`. `none` and `xavier` are the defaults and the original arithmetic: the
  full tier still reproduces every earlier pinned number **bit for bit**, which is the evidence that the
  refactor changed nothing already published.
- **Four new suites** at the `[32]` reference capacity (layernorm, batchnorm, He, plain), each retuned on
  the reference's own tuning grid so the comparison is controlled, ten seeds, threshold curves, against
  the four hypotheses committed in `docs/normalization-init-preregistration.md` before the runs.
- **Seventeen suites**: 461 asserted checks, 60 unit tests, four negative controls.

### Verdicts

| # | prediction | verdict | evidence |
|---|---|---|---|
| N1 | the schedule-free architecture effect survives both change families | **refuted (scope correction)** | it is *stronger* under He init (better than the tuned cosine in 9/10 seeds, +0.00566), a tie under batchnorm (+0.00094, 5/10) and plain init (+0.00052, 5/10), and it **reverses under layernorm** — the tuned cosine wins 7/10 and by 0.00374 on the mean. Both arms moved (schedule-free 0.13214 → 0.13625, baseline 0.13587 → 0.13251), so this is not the A2 pattern |
| N2 | AdEMAMix's no-advantage verdict survives both change families | **direction holds in 3 of 4; the pre-registered win-count criterion is refuted** | worse than AdamW at the same rate under batchnorm (+0.00006), He (+0.00238) and plain (+0.00195), marginally better under layernorm (−0.00009). But it "wins" 8/10 seeds under layernorm while the mean gap is 9 × 10⁻⁵ — see below |
| N3 | the metric trap (§5.12) survives | **confirmed** | on ten-seed means the best arm by training loss differs from the best by test loss in 4/4 variants, with 3/5/5/6 of six arms moving at least two places. On the pinned single runs it appears in 2/4 — both counts are reported, and the pre-registered criterion is recorded as under-specified between the two statistics |
| N4 | a variant lowers the per-seed noise, and its fixed-threshold winner then becomes stable | **refuted on the mechanism, confirmed on the correlation** | σ of the best arm: reference 0.0210, layernorm 0.0237, batchnorm 0.0306, He 0.0277, plain 0.0216 — **nothing lowered it**. The only variant whose fixed-threshold winner is consistent across ten seeds is the low-σ one: plain init, 2 distinct winners, against 3 for the reference, 3 for layernorm, 5 for batchnorm and 3 for He |

### The result worth reading: a win count without a magnitude is not evidence

N2 was written as "at most 2/10 seeds better". Under layernorm AdEMAMix is better in **8 of 10 seeds**
— while the mean difference is 0.00009, three orders of magnitude below the per-seed spread of either
arm (σ ≈ 0.025). A consistent sign and a nil effect. The criterion, as written, cannot tell those apart,
and the honest reading is that the criterion failed rather than that the method improved.

That is the **third arrival of the same lesson** in this repository — A2 in v0.8.0 was a baseline that
moved rather than a method that improved, and H5 in v0.7.0 was a noise boundary guessed in the wrong
place — and it is now a reporting rule in the pre-registration file rather than a footnote in a card.
In the same batch, §5.10's finding that **AdaGrad wins on final test loss once the model has room to
overfit** had to be scoped: under a plain fixed initialisation AdaGrad beats the tuned cosine in only
1 of 10 seeds, so that result belongs to the default normalisation and initialisation, not to capacity
alone.

### Correction notes (nothing already published is rewritten)

- **`v0.8.0` tag is untouched.** One documentation commit landed after it (`8e27e30`), stating H1's
  boundary precisely: what ends above `[64]` is AdaGrad's *lead*, not its usefulness — at `[16,16]` it
  still beats the tuned-cosine baseline in 9/10 seeds (+0.02563 on mean test loss). It belongs to this
  version, not to the archived v0.8.0.
- **Two internal wordings were wrong and are corrected in the body text, not silently dropped.**
  `CHANGELOG.md` first said the finite-difference check had caught the fourth defect; it had not — the
  check covered a single hidden layer and passed, and it was a deep suite's pinned number that failed.
  `REPRODUCTION.md` §8 described the family as "three defects"; it has four. Both are recorded in
  §5.10's correction note alongside the capacity suites that found it, and in `docs/defect-family.md`
  case 4.

### Protocol and coverage

Seventeen suites: the logistic-head family, MLP capacities `[8]`, `[32]`, `[8,8]`, `[64]`, `[16,16]`,
the `[32]` capacity under ReLU and GELU, and the `[32]` capacity under layernorm, batchnorm, He and plain
initialisation; four method families (Adam-family baselines, AdaGrad, AdEMAMix arXiv:2409.03137,
Schedule-Free arXiv:2405.15682); 200 epochs, full batch, ten seeds per paired comparison, thresholds
pinned and drawn on every curve. Normalisation here has no affine parameter and no running statistics —
the statistics are recomputed on whichever batch is evaluated — and that scope is stated wherever the
numbers are quoted. `--tier core` skips the fourteen capacity/activation/normalisation suites for local
iteration and always names them; CI runs `full` on `main` and on tags.

### Full-tier verification for this release

```
$ python scripts/repro.py --tier full
artifacts[init-plain]: runs/init-plain
verified:  461 checks, 0 failures
RESULT: PASS

$ python scripts/score_task.py --tier full
submission score: 100.0/100 (tier=full (all suites)) (461/461 checks, exit 0)
control[no-bias-correction]: detected (score 75.3/100, exit 1)
control[no-adaptive-scaling]: detected (score 77.2/100, exit 1)
control[ademamix-without-slow-ema]: detected (score 94.8/100, exit 1)
control[schedule-free-without-averaging]: detected (score 92.2/100, exit 1)
TASK RESULT: PASS
```
Seventeen suites, 461 asserted checks, 60 unit tests, four negative controls all detected, and the task
score 100.0/100 at the full tier.

### Known limitations

Mechanism-level reproduction throughout: no number from any paper's tables is claimed. One dataset
family, full-batch gradients, ten seeds, no formal significance test. Both metrics are pinned and a claim
named the one it is about. The activation and normalisation results add two scope labels on top of
threshold, model family, capacity and metric: which baseline is strong can change with the activation,
and which arm is best can change with the normalisation and initialisation. **This is the last
experimental axis**: the scope table has six, and further axes are added only if a reviewer asks for one.

Archived on Zenodo; the concept DOI is 10.5281/zenodo.23003610 and each version has its own version DOI.
