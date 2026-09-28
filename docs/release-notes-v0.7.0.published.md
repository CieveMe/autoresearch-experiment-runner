This release expands the capacity check to `[64]` and a two-layer `[16,16]`, and it does so under a
pre-registration: the six hypotheses, the protocol and the decision rules were written into
`docs/capacity-expansion-preregistration.md` and committed **before** the runs existed. Two predictions
were confirmed strongly, three were confirmed, one came out as a boundary and one was partially refuted —
which is the point of writing them down first.

### What is in it

- **Two more capacities**: `[64]` (wider) and `[16,16]` (deeper), each with a 17-trial tuning sweep
  committed before the headline run, six arms, **ten seeds**, threshold curves and the per-seed crossing
  analysis. Protocol unchanged: 200 epochs, full batch, target 0.147 pinned beside test loss.
- **`REPRODUCTION.md` §5.13** records the verdict per hypothesis with the numbers that decide it, and the
  per-suite table behind the noise claim.
- **`REPRODUCTION.md` §5.11 finding 7** now states the methodological claim as its own sentence: the
  reproducibility of a fixed-threshold ranking tracks the model family's noise level, and that noise is
  measurable before deciding whether to quote a winner.

### Verdicts against the pre-registration

| # | hypothesis | verdict | evidence |
|---|---|---|---|
| H1 | AdaGrad keeps strengthening | **boundary** | best arm with 8/10 wins at `[64]`; at `[16,16]` schedule-free overtakes it and its wins fall to 4/10 — the strengthening holds up to `[64]`, not beyond |
| H2 | the schedule-free architecture effect continues | **confirmed** | beats the tuned cosine on mean test loss at both new capacities (9/10 and 10/10 seeds); the effect now holds at five MLP capacities |
| H3 | AdEMAMix still has no advantage | **confirmed** | 1/10 and 0/10 seeds better than the AdamW baseline and worse on mean test loss; five capacities and both model families agree |
| H4 | train/test divergence keeps growing | **confirmed** | the top-1 differs between the two metrics at both capacities (ademamix → adagrad; ademamix → schedule-free) and five of six arms move at least two places |
| H5 | reproducibility tracks noise, boundary at σ ≈ 0.03 | **partially refuted** | direction holds (the three highest-σ suites are all unstable), boundary was too generous: instability appears by σ ≈ 0.021 |
| H6 | Adam is still not the fastest | **confirmed** | at the pinned threshold Adam needs 39 epochs at `[64]` (adaGrad 6, schedule-free 14) and 34 at `[16,16]` (schedule-free 20) |

Ten-seed test-loss means at the two new capacities:

| arm | `[64]` | `[16,16]` |
|---|---:|---:|
| adagrad | **0.12570 ± 0.02109** (8/10 wins) | 0.15048 ± 0.03812 (4/10) |
| schedule-free AdamW | 0.12904 ± 0.02323 (1/10) | **0.14634 ± 0.03697** (6/10) |
| adamw + tuned cosine | 0.13808 | 0.17611 |
| adamw constant / adam | 0.14480 | 0.22111 |
| ademamix | 0.14568 | 0.22439 |

### What the two new capacities teach

**H5 was the hypothesis worth pre-registering.** Its direction held — the only suites whose fixed-threshold
winner was identical in all ten seeds are the two whose per-seed test-loss standard deviation is lowest
(σ ≈ 0.020), and every suite at σ ≥ 0.021 produced two to four different winners — but the boundary
guessed for it was wrong. The pre-registered number (σ ≈ 0.03) is not the boundary; the observed one is
about **0.021**. The usable statement is therefore narrower and measurable: *check the sweep's noise
before quoting a fixed-threshold ranking; reproduce only what sits at the low end of the noise range.*

**H1 turned out to be capacity-scoped.** AdaGrad's rise with capacity was one of the more striking results
of the previous release; at `[16,16]` schedule-free takes the top spot on test loss and AdaGrad's per-seed
wins drop to 4/10. It is reported as a scope correction — "strengthening up to `[64]`" — not as a
retraction, and AdaGrad remains 9/10 better than the tuned cosine baseline at that capacity.

**H3 got stronger for the fifth time.** AdEMAMix has no advantage at any capacity tested, on either model
family, in ten-seed paired comparisons. At `[16,16]` it is also the sharpest illustration of the metric
trap in §5.12: it reaches the lowest **training** loss of any arm (0.0944) and has the worst **test** loss
(0.2211 mean), while the best test arm (schedule-free, 0.1463) is third on training loss. "Faster to
converge" and "better in the end" are different claims and this release keeps them apart everywhere.

### Protocol and coverage

Eleven suites: the logistic-head family plus MLP capacities `[8]`, `[32]`, `[8,8]`, `[64]`, `[16,16]`; four
method families (Adam-family baselines, AdaGrad, AdEMAMix arXiv:2409.03137, Schedule-Free
arXiv:2405.15682); 200 epochs, full batch, ten seeds per paired comparison, thresholds pinned and drawn on
every curve. `--tier core` skips the five capacity suites for local iteration and always says so; CI runs
`full` on `main` and on tags, and this body quotes a full-tier run as `docs/release-checklist.md`
requires.

### Full-tier verification for this release

```
$ python scripts/repro.py --tier full
artifacts[capacity-h16x16]: runs/capacity-h16x16
verified:  287 checks, 0 failures
RESULT: PASS

$ python scripts/score_task.py --tier full
submission score: 100.0/100 (tier=full (all suites)) (287/287 checks, exit 0)
control[no-bias-correction]: detected (score 79.1/100, exit 1)
control[no-adaptive-scaling]: detected (score 79.4/100, exit 1)
control[ademamix-without-slow-ema]: detected (score 94.4/100, exit 1)
control[schedule-free-without-averaging]: detected (score 92.7/100, exit 1)
TASK RESULT: PASS
```
Eleven suites, 287 asserted checks, four negative controls all detected, and the task score 100.0/100 at
the full tier.

### Known limitations

Mechanism-level reproduction throughout: no number from any paper's tables is claimed. One dataset family,
full-batch gradients and ten seeds; the newest capacities overfit heavily (`[16,16]` training losses reach
0.09 while test losses exceed 0.22), so they probe the metric question more than they probe the methods.
Activation functions other than tanh, and capacities beyond `[64]`, are left to the next release.

Archived on Zenodo; the concept DOI is 10.5281/zenodo.23003610 and each version has its own version DOI.
