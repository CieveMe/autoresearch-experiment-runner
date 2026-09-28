# Threshold curve — `optimizer convergence speed on a fixed synthetic task`

Trainer: `logistic` · metric: epochs until the training loss reaches the row's threshold.
`never` means the arm did not reach that threshold inside the budget.

| threshold | baseline | sgd_momentum | adagrad | rmsprop | adam | adam_no_bias_correction | fastest |
|---:|---:|---:|---:|---:|---:|---:|---|
| 0.1430 | never | never | never | never | never | 60 | adam_no_bias_correction |
| 0.1498 | never | 38 | 30 | 72 | 58 | 16 | adam_no_bias_correction |
| 0.1566 | never | 26 | 15 | 60 | 38 | 14 | adam_no_bias_correction |
| 0.1634 | never | 21 | 9 | 52 | 30 | 12 | adagrad |
| 0.1702 | never | 18 | 5 | 46 | 25 | 11 | adagrad |
| 0.1771 | never | 17 | 4 | 42 | 22 | 10 | adagrad |
| 0.1839 | never | 15 | 3 | 38 | 20 | 9 | adagrad |
| 0.1907 | never | 14 | 3 | 34 | 18 | 9 | adagrad |
| 0.1975 | never | 13 | 2 | 31 | 16 | 8 | adagrad |
| 0.2043 | never | 12 | 2 | 28 | 15 | 8 | adagrad |
| 0.2111 | never | 12 | 2 | 26 | 14 | 7 | adagrad |
| 0.2179 | never | 11 | 2 | 24 | 13 | 7 | adagrad |
| 0.2247 | 120 | 11 | 2 | 22 | 12 | 6 | adagrad |

## Reading

The fastest arm changes with the threshold:

- near **0.1634**: `adam_no_bias_correction` gives way to `adagrad`

The suite's pinned threshold is **0.16** — read its row above, not just the headline number.
