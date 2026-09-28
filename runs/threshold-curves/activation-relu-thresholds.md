# Threshold curve — `activation expansion, hidden [32] with ReLU: the four claim families`

Trainer: `mlp` · metric: epochs until the training loss reaches the row's threshold.
`never` means the arm did not reach that threshold inside the budget.

| threshold | adamw_cosine | adamw_constant | adam | adagrad | ademamix | schedule_free_adamw | fastest |
|---:|---:|---:|---:|---:|---:|---:|---|
| 0.1406 | 200 | never | never | never | never | never | adamw_cosine |
| 0.1408 | 145 | never | never | never | never | never | adamw_cosine |
| 0.1409 | 118 | never | never | never | never | never | adamw_cosine |
| 0.1411 | 100 | never | never | never | never | never | adamw_cosine |
| 0.1413 | 88 | never | never | never | never | never | adamw_cosine |
| 0.1415 | 80 | never | never | never | never | never | adamw_cosine |
| 0.1417 | 76 | never | never | never | never | never | adamw_cosine |
| 0.1419 | 68 | 192 | 192 | never | 189 | never | adamw_cosine |
| 0.1421 | 61 | 162 | 162 | never | 159 | never | adamw_cosine |
| 0.1423 | 58 | 135 | 135 | never | 132 | never | adamw_cosine |
| 0.1425 | 41 | 109 | 109 | never | 106 | never | adamw_cosine |
| 0.1427 | 39 | 80 | 80 | never | 81 | never | adamw_cosine |
| 0.1429 | 38 | 71 | 71 | 138 | 72 | 200 | adamw_cosine |

## Reading

The fastest arm is `adamw_cosine` at every threshold on this grid.

The suite's pinned threshold is **0.147** — read its row above, not just the headline number.
