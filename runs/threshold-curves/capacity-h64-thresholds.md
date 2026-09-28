# Threshold curve — `capacity expansion, hidden [64]: the same four claim families`

Trainer: `mlp` · metric: epochs until the training loss reaches the row's threshold.
`never` means the arm did not reach that threshold inside the budget.

| threshold | adamw_cosine | adamw_constant | adam | adagrad | ademamix | schedule_free_adamw | fastest |
|---:|---:|---:|---:|---:|---:|---:|---|
| 0.1358 | never | never | never | never | 200 | never | ademamix |
| 0.1364 | never | never | never | never | 192 | never | ademamix |
| 0.1369 | never | 192 | 192 | never | 183 | never | ademamix |
| 0.1375 | never | 181 | 181 | never | 173 | never | ademamix |
| 0.1381 | never | 169 | 169 | never | 161 | never | ademamix |
| 0.1387 | never | 155 | 155 | never | 149 | never | ademamix |
| 0.1393 | never | 140 | 140 | never | 135 | never | ademamix |
| 0.1398 | never | 124 | 124 | never | 120 | never | ademamix |
| 0.1404 | 157 | 108 | 108 | never | 105 | never | ademamix |
| 0.1410 | 113 | 92 | 92 | never | 91 | never | ademamix |
| 0.1416 | 87 | 80 | 80 | never | 80 | never | tie: adam, adamw_constant, ademamix |
| 0.1421 | 73 | 65 | 65 | never | 64 | 152 | ademamix |
| 0.1427 | 63 | 61 | 61 | 200 | 61 | 72 | tie: adam, adamw_constant, ademamix |

## Reading

The fastest arm changes with the threshold:

- near **0.1416**: `ademamix` gives way to `tie: adam, adamw_constant, ademamix`
- near **0.1421**: `tie: adam, adamw_constant, ademamix` gives way to `ademamix`
- near **0.1427**: `ademamix` gives way to `tie: adam, adamw_constant, ademamix`

The suite's pinned threshold is **0.147** — read its row above, not just the headline number.
