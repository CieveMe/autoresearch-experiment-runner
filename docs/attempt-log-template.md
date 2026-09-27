# Attempt log

Copy this file to `runs/attempts.md` (local, not committed) and append one row per attempt, so that
the retry history of a task attempt is auditable without polluting the artifact. Protocol: `TASK.md`
§8.

| # | command | exit | score | first failing assertion | change made |
|---:|---|---:|---:|---|---|
|   |  |  |  |  |  |

## Current status of the task variants

No agent attempts against `T-ADAM-01A/01B/01C/01D` have been recorded yet. What *has* been run and
verified is the reference state plus the two negative controls (`REPRODUCTION.md` §9):

| state | score | exit | outcome |
|---|---:|---:|---|
| reference implementation (this repository) | 100.0 / 100 | 0 | pass, 17/17 assertions |
| control `no-bias-correction` | 82.4 / 100 | 1 | detected (as required) |
| control `no-adaptive-scaling` | 82.4 / 100 | 1 | detected (as required) |

Reproduce the table with:

```bash
python scripts/score_task.py --json
```
