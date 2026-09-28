# Threshold curve — `Schedule-Free AdamW against a tuned cosine schedule, at a matched budget`

Trainer: `logistic` · metric: epochs until the training loss reaches the row's threshold.
`never` means the arm did not reach that threshold inside the budget.

| threshold | adamw_cosine | adamw_constant | schedule_free_adamw | sgd_cosine | schedule_free_sgd | fastest |
|---:|---:|---:|---:|---:|---:|---|
| 0.1432 | never | 200 | never | never | never | adamw_constant |
| 0.1510 | 57 | 53 | 130 | never | never | adamw_constant |
| 0.1587 | 36 | 35 | 95 | never | never | adamw_constant |
| 0.1665 | 28 | 27 | 77 | never | never | adamw_constant |
| 0.1742 | 23 | 23 | 64 | never | never | tie: adamw_constant, adamw_cosine |
| 0.1820 | 20 | 20 | 55 | never | never | tie: adamw_constant, adamw_cosine |
| 0.1898 | 18 | 18 | 49 | never | never | tie: adamw_constant, adamw_cosine |
| 0.1975 | 16 | 16 | 43 | never | never | tie: adamw_constant, adamw_cosine |
| 0.2053 | 15 | 15 | 39 | never | never | tie: adamw_constant, adamw_cosine |
| 0.2130 | 13 | 13 | 35 | never | never | tie: adamw_constant, adamw_cosine |
| 0.2208 | 13 | 12 | 32 | never | 189 | adamw_constant |
| 0.2286 | 12 | 12 | 30 | never | 168 | tie: adamw_constant, adamw_cosine |
| 0.2363 | 11 | 11 | 27 | never | 151 | tie: adamw_constant, adamw_cosine |

## Reading

The fastest arm changes with the threshold:

- near **0.1742**: `adamw_constant` gives way to `tie: adamw_constant, adamw_cosine`
- near **0.2208**: `tie: adamw_constant, adamw_cosine` gives way to `adamw_constant`
- near **0.2286**: `adamw_constant` gives way to `tie: adamw_constant, adamw_cosine`

The suite's pinned threshold is **0.148** — read its row above, not just the headline number.
