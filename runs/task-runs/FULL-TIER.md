# Full-tier score for the task-contract claim

`docs/release-checklist.md` hard rule 2: a release body quotes a **full**-tier run, and so does any
outward-facing claim that the task contract is executable. This is that run.

```
$ python scripts/score_task.py --tier full
submission score: 100.0/100 (tier=full (all suites)) (474/474 checks, exit 0)
control[no-bias-correction]: detected (score 74.9/100, exit 1)
control[no-adaptive-scaling]: detected (score 77.0/100, exit 1)
control[ademamix-without-slow-ema]: detected (score 94.9/100, exit 1)
control[schedule-free-without-averaging]: detected (score 92.4/100, exit 1)

TASK RESULT: PASS
```

## Provenance

| field | value |
|---|---|
| commit | `3dabd96` (pushed to `github/main` before this run started) |
| tier | `full` — 18 suites, capacity/activation/normalisation suites included, nothing skipped |
| asserted checks | 474 (461 + 13 from the T-ADAM-01C ablation suite) |
| unit tests in the same tree | 87 |
| negative controls | 4 of 4 detected; the scores above are the mutated trees', not the submission's |
| command | `python scripts/score_task.py --tier full` |

The tier is printed inside the score line on purpose: a `core` run always names the suites it did not
run, so a partial number can never be read as full coverage. The per-variant runs in
[`README.md`](README.md) are core-tier by design (they exist to show the score curve), and the core-tier
line is quoted there as process evidence only.

## What this does and does not support

* **Supports:** the repository is a scored task in which a working submission reaches 100/100 at the full
  tier with a clean exit code, and in which four separate mutations of the implementation are still
  detected. That is the "the task contract is executable" claim.
* **Does not support:** anything about what a language-model agent would score. The T-ADAM-01 runs in
  this directory were performed by scripts, not by an agent, and `TASK.md` §9 remains the definition of
  those variants.
