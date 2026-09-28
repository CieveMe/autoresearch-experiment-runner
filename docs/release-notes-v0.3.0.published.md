This release makes the harness able to take on real papers, runs a 2024 paper through it, and then
turns the same scepticism on its own earlier results. Two of the three headline claims below are
negative results, reported because the experiments were built to be able to falsify them.

### What is new

- **Trainer adapter.** The original model moved, unchanged, into `autoresearch/trainers/logistic.py`;
  a dependency-free two-layer tanh MLP was added at `autoresearch/trainers/mlp.py`; `trainers/registry.py`
  selects by config key. The update rules now live in one place (`autoresearch/optimizers.py`, which
  gains `adamw` and `ademamix`), schedules and data sources are their own modules
  (`autoresearch/schedules.py`, `autoresearch/datasets.py`, the latter refusing remote URLs), and
  `autoresearch/model.py` is a compatibility shim. The "replace the model to take on another paper"
  claim in the README is now true, and the 46 assertions that existed before the refactor still pass
  unchanged.
- **A 2024 paper, AdEMAMix (arXiv:2409.03137), end to end**: config, a 20-trial tuning sweep, pinned
  expectations, a 10-seed paired comparison, a paper card (`docs/papers/ademamix-2024.md`) and a
  negative control that mutates the slow-EMA term.
- **The self-scepticism run.** Both earlier suites were repeated on the MLP trainer, with every
  optimizer family retuned for that model, to test whether the earlier conclusions were an artefact of
  a two-parameter, almost-convex model.
- 30 unit tests (was 17), including a numerical gradient check for the MLP and a check that switching
  AdEMAMix's slow EMA off reproduces AdamW.

### Results, stated plainly

| question | answer |
|---|---|
| Does AdEMAMix converge faster than AdamW? | **Not reproduced.** On the logistic task it reaches the target in the *same* epoch as AdamW in 10/10 seeds; on the MLP it matches AdamW again while AdamW's own baselines (AdaGrad, momentum) are 3× faster. |
| Does AdEMAMix reach a better optimum at this budget? | **Not on the logistic head, and not on the MLP either once ten seeds are used** (mean test loss 0.13249 without warmups vs AdamW's 0.13218). Its no-warmup variant is indistinguishable from AdamW on both. |
| Is the paper's warmup scheme useful here? | **No — it is the worst arm on both trainers** (MLP mean test loss 0.14269 with 45-step ramps, 0.15261 with 120-step ramps, against AdamW's 0.13218). The ramps are sized for a 256k-step run; at 120 epochs they never finish. |
| Is Adam the fastest optimizer? | **No, on either model.** MLP ten-seed averages: AdaGrad 6.2 epochs, momentum 7.0, Adam 20.3, RMSProp 33.3, SGD 36.1. Adam does have the lowest final loss, which is a different claim and is reported separately. |

The most useful artefact of the release is a trap it documents: on seed 7 the pinned MLP numbers
favour an AdEMAMix variant that is the **second worst of five over ten seeds**. The pinned file
(`expected/expected_ademamix_mlp.json`) now carries that warning, and `REPRODUCTION.md` §5.6 says
plainly that pinned numbers are a regression baseline, not evidence; the verdict always comes from the
seed sweep.

### Fixed

- The MLP applied `tanh` to its output layer as well, which made the analytic gradient about 1% off —
  found by a finite-difference check, not by reading the code. The output layer is now linear with a
  single sigmoid.
- Trial configs did not inherit the experiment's `seed`, so a "10-seed" MLP run varied the data split
  while initialising every run from the same weights. `TRIAL_INHERITED_KEYS` now includes `seed`; the
  logistic trainer never read it, so the earlier numbers are unaffected and still verify. A regression
  test now asserts the contract for every suite.
- Two MLP learning rates (AdaGrad, RMSProp) had been carried over from before that fix and were
  re-derived from the fresh sweep, so the tuning rule applies to every arm.
- The cosine schedule started at 0.978 instead of 1.0 on the first step.

### Known limitations

Mechanism-level reproduction only: no MNIST/CIFAR-10/IMDB, no number from any paper's tables is claimed.
Full-batch gradients, one dataset family, one hidden-layer size, ten seeds and no formal significance
test; test-loss standard deviation around 0.023 means ten seeds separate "0.13 from 0.15" but not
"0.13218 from 0.13249". The learning-rate grids are not saturated for every family.

### Verify it yourself

```bash
python scripts/repro.py        # five suites, 121 asserted checks, exit 0
python scripts/score_task.py   # 100/100, and all three negative controls must be detected
python -m unittest discover -s tests -v
```

Archived on Zenodo; the concept DOI is 10.5281/zenodo.23003610 and each version gets its own version
DOI.
