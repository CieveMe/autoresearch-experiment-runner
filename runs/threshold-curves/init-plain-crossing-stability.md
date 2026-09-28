# Crossing stability — `init-plain` (adamw_cosine vs schedule_free_adamw)

Crossings located in **6 of 10 seeds**, at 0.127508 on average (min 0.113659, max 0.136458, spread 0.022799).

At the suite's pinned threshold (0.147), the faster arm per seed was:

| seed | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|---|
| faster | adamw_cosine | adamw_cosine | adamw_cosine | adamw_cosine | adamw_cosine | adamw_cosine | adamw_cosine | adamw_cosine | adamw_cosine | adamw_cosine |

**Consistent**: `adamw_cosine` is faster at the pinned threshold in every seed.

Per-seed crossing values:

| seed | crossing |
|---:|---|
| 0 | none |
| 1 | 0.11619 |
| 2 | 0.133535 |
| 3 | 0.135515 |
| 4 | 0.129689 |
| 5 | 0.136458 |
| 6 | none |
| 7 | none |
| 8 | none |
| 9 | 0.113659 |
