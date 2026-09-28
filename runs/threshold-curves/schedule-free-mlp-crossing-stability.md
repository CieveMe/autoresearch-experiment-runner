# Crossing stability — `schedule-free-mlp` (adamw_constant vs schedule_free_adamw)

Crossings located in **10 of 10 seeds**, at 0.119163 on average (min 0.092327, max 0.142876, spread 0.050549).

At the suite's pinned threshold (0.148), the faster arm per seed was:

| seed | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|---|
| faster | adamw_constant | tie | adamw_constant | adamw_constant | adamw_constant | adamw_constant | adamw_constant | schedule_free_adamw | schedule_free_adamw | adamw_constant |

**Not consistent**: the winner at the pinned threshold changes between seeds, so a single-seed statement about that threshold would not survive the sweep.

Per-seed crossing values:

| seed | crossing |
|---:|---|
| 0 | 0.093688 |
| 1 | 0.116119 |
| 2 | 0.131358 |
| 3 | 0.136724 |
| 4 | 0.127317 |
| 5 | 0.136613 |
| 6 | 0.092327 |
| 7 | 0.142876 |
| 8 | 0.100099 |
| 9 | 0.114509 |
