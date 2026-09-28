# Threshold curve — `AdEMAMix convergence speed against AdamW and momentum on a fixed synthetic task`

Trainer: `logistic` · metric: epochs until the training loss reaches the row's threshold.
`never` means the arm did not reach that threshold inside the budget.

| threshold | adamw | ademamix_tuned | ademamix_paper_warmups | ademamix_no_slow_ema | sgd_momentum | fastest |
|---:|---:|---:|---:|---:|---:|---|
| 0.1430 | never | 92 | never | never | never | ademamix_tuned |
| 0.1432 | 52 | 51 | never | 52 | never | ademamix_tuned |
| 0.1434 | 44 | 43 | never | 44 | never | ademamix_tuned |
| 0.1435 | 42 | 42 | never | 42 | never | adamw |
| 0.1437 | 36 | 35 | never | 36 | never | ademamix_tuned |
| 0.1439 | 35 | 35 | never | 35 | never | adamw |
| 0.1440 | 34 | 34 | never | 34 | never | adamw |
| 0.1442 | 34 | 34 | never | 34 | never | adamw |
| 0.1444 | 33 | 33 | never | 33 | never | adamw |
| 0.1446 | 33 | 33 | never | 33 | 120 | adamw |
| 0.1447 | 33 | 32 | never | 33 | 111 | ademamix_tuned |
| 0.1449 | 32 | 32 | never | 32 | 104 | adamw |
| 0.1451 | 32 | 32 | 120 | 32 | 98 | adamw |

## Reading

The fastest arm changes with the threshold:

- near **0.1435**: `ademamix_tuned` gives way to `adamw`
- near **0.1437**: `adamw` gives way to `ademamix_tuned`
- near **0.1439**: `ademamix_tuned` gives way to `adamw`
- near **0.1447**: `adamw` gives way to `ademamix_tuned`
- near **0.1449**: `ademamix_tuned` gives way to `adamw`

The suite's pinned threshold is **0.148** — read its row above, not just the headline number.
