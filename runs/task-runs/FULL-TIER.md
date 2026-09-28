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

The run and the tag are not the same commit, so the difference is written out in full rather than
summarised. A summary like "docs and tests only" would be wrong for the same reason a stale pin is
wrong: `expected/` is a verification input.

```
run at 3dabd96 → submission score: 100.0/100 (tier=full (all suites)) (474/474 checks, exit 0)

tag v0.10.0 = the commit carrying this file  (`git rev-parse v0.10.0^{commit}`)
git diff --name-only 3dabd96..v0.10.0 =
  .gitignore
  CHANGELOG.md
  docs/defect-family.md
  docs/release-corrections-pending.md
  docs/release-notes-v0.10.0.published.md
  expected/expected_ablation_adam_no_first_moment.json
  runs/task-runs/FULL-TIER.md
  runs/task-runs/README.md
  runs/task-runs/T-ADAM-01C.md
  tests/test_harness.py

expected/expected_ablation_adam_no_first_moment.json: the `notes` array gained one string and nothing
else — no numeric and no tolerance field changed, so the ablation's checks and the other 461 are the
same inputs they were. `.gitignore` gained an ignore rule. The rest is prose and tests.

unit tests in the run's tree: 87 → 88 (the two new guards for case 6a and 6b), which is a count of
tests, not of asserted checks: the 474 pinned assertions and the four control scores are unaffected.
```

| field | value |
|---|---|
| run commit | `3dabd96` (pushed to `github/main` before the run started) |
| tag | `v0.10.0` (see the diff above; verified by `git diff --name-only 3dabd96..v0.10.0`) |
| tier | `full` — 18 suites, capacity/activation/normalisation suites included, nothing skipped |
| asserted checks | 474 (461 + 13 from the T-ADAM-01C ablation suite) |
| negative controls | 4 of 4 detected; the scores above are the mutated trees', not the submission's |
| command | `python scripts/score_task.py --tier full` |

Why there is no re-run: a re-run would be evidence that could have been obtained by reading a diff, and
the rule this repository follows is to write the provenance down precisely instead of covering it with
fresh compute. If any numeric or tolerance field had moved in `expected/`, the re-run would have been
the only honest option.

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
