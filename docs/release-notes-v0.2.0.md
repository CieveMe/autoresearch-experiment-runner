# Release notes — v0.2.0

> **The body below is the text as it was actually published.** The verbatim body that was pasted
> into the GitHub release is kept next to it as `docs/release-notes-v0.2.0.published.md`, because a
> release body deleted on GitHub is gone for good and the repository is the only place that survives.

Paste this into the GitHub release form (target: `main` after `ed0be38` and `77512b6` are pushed;
tag `v0.2.0`).

## Title

`v0.2.0 — convergence-speed experiment (and the negative result)`

## Body

This release turns the paper's **actual headline claim** — *faster convergence* — into a measurable
experiment, and reports the answer even though it contradicts the paper.

### What is new

- **`epochs_to_target`**: the first epoch whose training loss reaches a target close to the converged
  floor, for Adam against SGD, heavy-ball momentum, AdaGrad and RMSProp at a matched 120-epoch budget.
- **A learning-rate sweep (24 trials)** so each optimizer family picks its learning rate by the same
  rule — comparing hand-picked rates would measure tuning luck, not the update rules. The sweep curves
  are committed, so the analysis can be re-scored against any other target.
- **A bias-correction ablation** (`bias_correction: false`), so the paper's correction term can be
  switched off and measured instead of argued about.
- **Per-epoch loss curves** in every result, plus `loss-curves.csv`.
- `python scripts/repro.py` now runs both suites in one command: **46 asserted checks**, and it prints
  `epochs_to_target` in its table.
- 17 unit tests (was 8), including one that fails when a new metric has no declared ranking direction.

### The result, stated plainly

AdaGrad reached the target first in **10/10 seeds** (mean **4.7** epochs vs Adam's **22.6**). SGD with
momentum also beat Adam 10/10 (16.7 epochs), RMSProp was the slowest adaptive method (42.0), and plain
SGD never reached the floor at any swept learning rate. Disabling Adam's bias correction reached the
target 10/10 **faster** (12.5 ± 4.6 epochs) with a marginally lower final loss.

So in this setup **Adam is not the fastest optimizer**, and the repository says so in
`REPRODUCTION.md` §5.4 instead of keeping the number that looked better. The fixed-budget experiment
from v0.1.0 (Adam has the lowest test loss at 80 epochs) and this time-to-target experiment answer
different questions, and neither is allowed to stand in for the other.

### Fixed

- `config_sha256` was newline-sensitive, so a Windows checkout hashed the same revision differently.
- `epochs_to_target` was missing from one copy of the "lower is better" metric list, which made the
  seed sweep report RMSProp as the per-seed winner instead of AdaGrad.

### Known limitations

Mechanism-level reproduction only (no MNIST/CIFAR-10/IMDB, no number from the paper's tables claimed);
full-batch gradients; no learning-rate schedules; one dataset family; ten seeds and no formal
significance test; and the learning-rate grid is not saturated — every adaptive family's best rate sits
at or beyond the largest value swept. All of this is listed in `REPRODUCTION.md` §7.

### Verify it yourself

```bash
python scripts/repro.py        # 46 checks, 0 failures, exit 0
python scripts/score_task.py   # 100/100, and both negative controls must be detected
```
