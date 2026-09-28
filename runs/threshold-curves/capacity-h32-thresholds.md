# Threshold curve — `capacity check, hidden [32]: do the Adam / AdEMAMix / schedule-free conclusions survive a wider model?`

Trainer: `mlp` · metric: epochs until the training loss reaches the row's threshold.
`never` means the arm did not reach that threshold inside the budget.

| threshold | adamw_cosine | adamw_constant | adam | adagrad | ademamix | schedule_free_adamw | fastest |
|---:|---:|---:|---:|---:|---:|---:|---|
| 0.1376 | never | never | never | never | 200 | never | ademamix |
| 0.1380 | never | 196 | 196 | never | 188 | never | ademamix |
| 0.1385 | never | 182 | 182 | never | 175 | never | ademamix |
| 0.1389 | never | 167 | 167 | never | 162 | never | ademamix |
| 0.1394 | never | 153 | 153 | never | 148 | never | ademamix |
| 0.1399 | never | 138 | 138 | never | 135 | never | ademamix |
| 0.1403 | never | 124 | 124 | never | 122 | never | ademamix |
| 0.1408 | 165 | 111 | 111 | never | 109 | never | ademamix |
| 0.1412 | 123 | 98 | 98 | never | 97 | never | ademamix |
| 0.1417 | 99 | 87 | 87 | never | 87 | never | adam |
| 0.1421 | 83 | 76 | 76 | never | 76 | 173 | adam |
| 0.1426 | 71 | 68 | 68 | never | 68 | 147 | adam |
| 0.1430 | 63 | 61 | 61 | 200 | 61 | 102 | adam |

## Reading

The fastest arm changes with the threshold:

- near **0.1417**: `ademamix` gives way to `adam`

The suite's pinned threshold is **0.147** — read its row above, not just the headline number.
