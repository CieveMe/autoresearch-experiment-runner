# Full-tier gate on the v0.11.0 tag (the preferred citation)

`docs/release-checklist.md` hard rule 2 asks a release body to quote a full-tier run, and prefers the run
**on the tag** — tag runs are never cancelled by the `concurrency` rule, so their verdict cannot be taken
away by a later push. This file records that run.

| field | value |
|---|---|
| run | [#45](https://github.com/CieveMe/autoresearch-experiment-runner/actions/runs/45), workflow `repro` |
| run id | `36539858168` (the HTML page shows run number 45) |
| trigger | `push` on `refs/tags/v0.11.0` |
| commit | `d72633f` (the commit `v0.11.0` points at) |
| result | **all six jobs green**; the run itself is `completed / success` |
| the scorer job | `score the task and its negative controls (python 3.12)`, job `109312424917` — finished green, output quoted below |

## What it cost, measured rather than estimated

Read from the API's `started_at` / `completed_at` fields, so this replaces the "≈1 h" that was an estimate
before:

| job | duration | window (UTC) |
|---|---:|---|
| run wall-clock | **1 h 06 m 59 s** | 07:58:44 → 09:05:43 |
| `score the task and its negative controls` | **1 h 06 m 55 s** | 07:58:47 → 09:05:42 |
| `reproduce (python 3.12)` | 33 m 56 s | 07:58:46 → 08:32:42 |
| `reproduce (python 3.10)` | 18 m 31 s | 07:58:46 → 08:17:17 |
| `reproduce (docker)` | 18 m 22 s | 07:58:47 → 08:17:09 |
| `regenerate the sweeps and tuning curves` | 13 m 47 s | 07:58:46 → 08:12:33 |
| `regenerate the threshold curves` | 9 s | 08:32:45 → 08:32:54 |

**The scorer is 99.9% of the wall clock**, which is the measured form of the statement the workflow split
was built around: the parallel jobs removed the *sum*, and what remains is one job that reproduces the
corpus five times. The threshold-curves job is nine seconds of work that starts only when the
reproduction artifact lands — that is the `needs: repro` dependency doing exactly what it was written to
do, and it is worth knowing that its own runtime is negligible next to the wait.

## What the tag run verified, quoted from the job logs

Every line below is copied from the run's job logs. Those logs are **not readable anonymously** (the API
answers 403 to an unauthenticated request), so they were read with the repository owner's credential; the
quotes are verbatim and the job ids are given so anyone with access can check them.

**`reproduce (python 3.12)`** — job `109312424998`, started 07:58Z:

```
tier=full (all suites)
verified:  474 checks, 0 failures
RESULT: PASS
```

…and the same block again later in the same job, because `make repro` runs a second full reproduction to
verify the documented one-command entry point. Both passed. `Ran 93 tests` in each.

**`reproduce (python 3.10)`** — job `109312424888`:

```
Ran 93 tests in 48.718s
tier=full (all suites)
verified:  474 checks, 0 failures
RESULT: PASS
```

**`reproduce (docker)`** — job `109312424603`, from inside the container:

```
repro-1  | Ran 93 tests in 37.693s
repro-1  | tier=full (all suites)
repro-1  | verified:  474 checks, 0 failures
repro-1  | RESULT: PASS
```

So the tag carries **three independent full-tier reproductions on three runtimes** — CPython 3.10, CPython
3.12, and the dependency-free container image — each reporting 474 asserted checks with no failures and 93
unit tests green. The suite count is 18; nothing was skipped, and the tier label says so in every line.

The other two jobs — `regenerate the sweeps and tuning curves` and `regenerate the threshold curves` —
completed successfully as well; they regenerate artifacts rather than verify numbers, so their verdict is
the job conclusion rather than a line of output.

## The `scorer` job

`score the task and its negative controls (python 3.12)` runs `scripts/score_task.py --tier full`, which
reproduces the corpus five times (the submission plus four mutated copies) and is therefore the longest
job. It finished green, and this is its output, verbatim:

```
submission score: 100.0/100 (tier=full (all suites)) (474/474 checks, exit 0)
control[no-bias-correction]: detected (score 75.3/100, exit 1)
control[no-adaptive-scaling]: detected (score 77.0/100, exit 1)
control[ademamix-without-slow-ema]: detected (score 94.9/100, exit 1)
control[schedule-free-without-averaging]: detected (score 92.4/100, exit 1)
TASK RESULT: PASS
```

**This is the line a release body should quote**, and it is the one the next version's body can use
without any qualifier: it comes from the tag, it is a `full`-tier run, the tier label is in the line, and
no later push can cancel it. The equivalent line in the v0.11.0 body — the Windows run at `0f3ce2f`,
same score with controls `74.9 / 77.0 / 94.9 / 92.8` — was on a *branch*, which is exactly why that body
had to label it "the run recorded in the repository, not the run on this tag".
