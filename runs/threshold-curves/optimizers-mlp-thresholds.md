# Threshold curve — `optimizer convergence speed on the two-layer MLP trainer`

Trainer: `mlp` · metric: epochs until the training loss reaches the row's threshold.
`never` means the arm did not reach that threshold inside the budget.

| threshold | sgd | sgd_momentum | adagrad | rmsprop | adam | fastest |
|---:|---:|---:|---:|---:|---:|---|
| 0.1362 | never | never | never | never | 120 | adam |
| 0.1369 | never | never | never | never | 85 | adam |
| 0.1375 | never | never | never | never | 67 | adam |
| 0.1382 | never | never | never | never | 63 | adam |
| 0.1389 | never | never | never | never | 54 | adam |
| 0.1396 | never | never | never | never | 47 | adam |
| 0.1402 | never | never | never | never | 46 | adam |
| 0.1409 | never | 109 | never | never | 44 | adam |
| 0.1416 | never | 66 | never | never | 43 | adam |
| 0.1422 | never | 41 | never | never | 43 | sgd_momentum |
| 0.1429 | never | 30 | 113 | never | 40 | sgd_momentum |
| 0.1436 | never | 30 | 68 | never | 39 | sgd_momentum |
| 0.1443 | 107 | 29 | 40 | 120 | 39 | sgd_momentum |

## Reading

The fastest arm changes with the threshold:

- near **0.1422**: `adam` gives way to `sgd_momentum`

The suite's pinned threshold is **0.147** — read its row above, not just the headline number.
