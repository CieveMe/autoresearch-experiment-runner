# Threshold curve — `activation expansion, hidden [32] with GELU: the four claim families`

Trainer: `mlp` · metric: epochs until the training loss reaches the row's threshold.
`never` means the arm did not reach that threshold inside the budget.

| threshold | adamw_cosine | adamw_constant | adam | adagrad | ademamix | schedule_free_adamw | fastest |
|---:|---:|---:|---:|---:|---:|---:|---|
| 0.1416 | 200 | never | never | never | never | never | adamw_cosine |
| 0.1417 | 155 | never | never | never | never | never | adamw_cosine |
| 0.1418 | 135 | never | never | never | never | never | adamw_cosine |
| 0.1419 | 121 | never | never | never | never | never | adamw_cosine |
| 0.1421 | 110 | never | never | never | never | never | adamw_cosine |
| 0.1422 | 98 | never | never | never | never | never | adamw_cosine |
| 0.1423 | 86 | never | never | never | never | never | adamw_cosine |
| 0.1424 | 76 | never | never | never | never | never | adamw_cosine |
| 0.1425 | 58 | never | never | never | never | never | adamw_cosine |
| 0.1427 | 56 | 189 | 189 | never | 184 | never | adamw_cosine |
| 0.1428 | 55 | 159 | 159 | never | 155 | never | adamw_cosine |
| 0.1429 | 54 | 119 | 119 | never | 116 | never | adamw_cosine |
| 0.1430 | 38 | 77 | 77 | 194 | 79 | 200 | adamw_cosine |

## Reading

The fastest arm is `adamw_cosine` at every threshold on this grid.

The suite's pinned threshold is **0.147** — read its row above, not just the headline number.
