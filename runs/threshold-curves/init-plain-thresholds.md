# Threshold curve — `normalisation/initialisation robustness check, hidden [32], plain fixed-0.05 initialisation (no normalisation): do the two negative results survive?`

Trainer: `mlp` · metric: epochs until the training loss reaches the row's threshold.
`never` means the arm did not reach that threshold inside the budget.

| threshold | adamw_cosine | adamw_constant | adam | adagrad | ademamix | schedule_free_adamw | fastest |
|---:|---:|---:|---:|---:|---:|---:|---|
| 0.1405 | never | never | never | never | 200 | never | ademamix |
| 0.1407 | never | 196 | 196 | never | 191 | never | ademamix |
| 0.1409 | never | 186 | 186 | never | 183 | never | ademamix |
| 0.1411 | never | 176 | 176 | 134 | 174 | never | adagrad |
| 0.1413 | never | 168 | 168 | 95 | 167 | never | adagrad |
| 0.1416 | never | 160 | 160 | 91 | 159 | never | adagrad |
| 0.1418 | never | 153 | 153 | 43 | 153 | never | adagrad |
| 0.1420 | never | 146 | 146 | 39 | 146 | never | adagrad |
| 0.1422 | never | 140 | 140 | 37 | 141 | never | adagrad |
| 0.1424 | never | 134 | 134 | 35 | 135 | never | adagrad |
| 0.1426 | never | 129 | 129 | 34 | 130 | 174 | adagrad |
| 0.1428 | never | 124 | 124 | 33 | 125 | 121 | adagrad |
| 0.1430 | 200 | 119 | 119 | 31 | 120 | 72 | adagrad |

## Reading

The fastest arm changes with the threshold:

- near **0.1411**: `ademamix` gives way to `adagrad`

The suite's pinned threshold is **0.147** — read its row above, not just the headline number.
