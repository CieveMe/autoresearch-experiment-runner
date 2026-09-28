# Threshold curve — `Schedule-Free AdamW against a tuned cosine schedule on the MLP trainer`

Trainer: `mlp` · metric: epochs until the training loss reaches the row's threshold.
`never` means the arm did not reach that threshold inside the budget.

| threshold | adamw_cosine | adamw_constant | schedule_free_adamw | sgd_cosine | schedule_free_sgd | fastest |
|---:|---:|---:|---:|---:|---:|---|
| 0.1378 | never | 200 | never | never | never | adamw_constant |
| 0.1384 | never | 180 | never | never | never | adamw_constant |
| 0.1389 | never | 160 | never | never | never | adamw_constant |
| 0.1395 | never | 136 | never | never | never | adamw_constant |
| 0.1400 | 178 | 113 | never | never | never | adamw_constant |
| 0.1406 | 121 | 97 | never | never | never | adamw_constant |
| 0.1412 | 99 | 86 | never | never | never | adamw_constant |
| 0.1417 | 85 | 77 | 157 | never | never | adamw_constant |
| 0.1423 | 75 | 69 | 101 | never | never | adamw_constant |
| 0.1428 | 66 | 63 | 63 | never | never | tie: adamw_constant, schedule_free_adamw |
| 0.1434 | 58 | 56 | 40 | never | never | schedule_free_adamw |
| 0.1440 | 54 | 53 | 14 | never | 116 | schedule_free_adamw |
| 0.1445 | 44 | 44 | 13 | 198 | 105 | schedule_free_adamw |

## Reading

The fastest arm changes with the threshold:

- near **0.1428**: `adamw_constant` gives way to `tie: adamw_constant, schedule_free_adamw`
- near **0.1434**: `tie: adamw_constant, schedule_free_adamw` gives way to `schedule_free_adamw`

The suite's pinned threshold is **0.148** — read its row above, not just the headline number.
