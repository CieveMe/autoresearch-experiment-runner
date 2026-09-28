# Crossing stability — `norm-batchnorm` (adamw_cosine vs schedule_free_adamw)

Crossings located in **1 of 10 seeds**, at 0.088121 on average (min 0.088121, max 0.088121, spread 0.0).

At the suite's pinned threshold (0.147), the faster arm per seed was:

| seed | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|---|
| faster | tie | adamw_cosine | tie | adamw_cosine | schedule_free_adamw | adamw_cosine | tie | adamw_cosine | tie | schedule_free_adamw |

**Not consistent**: the winner at the pinned threshold changes between seeds, so a single-seed statement about that threshold would not survive the sweep.

Per-seed crossing values:

| seed | crossing |
|---:|---|
| 0 | none |
| 1 | none |
| 2 | none |
| 3 | none |
| 4 | none |
| 5 | none |
| 6 | 0.088121 |
| 7 | none |
| 8 | none |
| 9 | none |
