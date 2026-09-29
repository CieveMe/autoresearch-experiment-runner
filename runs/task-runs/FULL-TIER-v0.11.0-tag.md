# Full-tier gate on the v0.11.0 tag (the preferred citation)

`docs/release-checklist.md` hard rule 2 asks a release body to quote a full-tier run, and prefers the run
**on the tag** — tag runs are never cancelled by the `concurrency` rule, so their verdict cannot be taken
away by a later push. This file records that run.

| field | value |
|---|---|
| run | [#45](https://github.com/CieveMe/autoresearch-experiment-runner/actions/runs/45), workflow `repro` |
| trigger | `push` on `refs/tags/v0.11.0` |
| commit | `d72633f` (the commit `v0.11.0` points at) |
| result | **five of six jobs green, and the three jobs that reproduce the corpus all report 474/474** |
| the sixth job | `score the task and its negative controls (python 3.12)` — still running when this file was written; its line is appended below when it lands |

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
job. At the time of writing it was still running; when it completes, its score line and the four control
verdicts belong here.

Until then, the equivalent line already in the repository is the one quoted in the v0.11.0 body — the
Windows run at `0f3ce2f`, `100.0/100 (tier=full (all suites)) (474/474 checks, exit 0)` with all four
controls detected (`runs/task-runs/FULL-TIER-ci-fix.md`). That run was on a branch, which is exactly why
this file exists: the tag run is the one a later push cannot cancel.
