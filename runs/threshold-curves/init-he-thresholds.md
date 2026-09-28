# Threshold curve — `normalisation/initialisation robustness check, hidden [32], He initialisation (no normalisation): do the two negative results survive?`

Trainer: `mlp` · metric: epochs until the training loss reaches the row's threshold.
`never` means the arm did not reach that threshold inside the budget.

| threshold | adamw_cosine | adamw_constant | adam | adagrad | ademamix | schedule_free_adamw | fastest |
|---:|---:|---:|---:|---:|---:|---:|---|
| 0.1310 | never | never | never | never | 199 | never | ademamix |
| 0.1317 | never | 197 | 197 | never | 187 | never | ademamix |
| 0.1324 | never | 179 | 179 | never | 176 | never | ademamix |
| 0.1331 | never | 162 | 162 | never | 168 | never | tie: adam, adamw_constant |
| 0.1338 | never | 149 | 149 | never | 143 | never | ademamix |
| 0.1345 | never | 136 | 136 | never | 131 | never | ademamix |
| 0.1353 | never | 124 | 124 | never | 119 | never | ademamix |
| 0.1360 | 167 | 111 | 111 | never | 108 | never | ademamix |
| 0.1367 | 126 | 99 | 99 | never | 96 | never | ademamix |
| 0.1374 | 103 | 87 | 87 | never | 85 | never | ademamix |
| 0.1381 | 86 | 77 | 77 | never | 75 | never | ademamix |
| 0.1388 | 74 | 68 | 68 | never | 68 | never | tie: adam, adamw_constant, ademamix |
| 0.1396 | 66 | 63 | 63 | 200 | 63 | 195 | tie: adam, adamw_constant, ademamix |

## Reading

The fastest arm changes with the threshold:

- near **0.1331**: `ademamix` gives way to `tie: adam, adamw_constant`
- near **0.1338**: `tie: adam, adamw_constant` gives way to `ademamix`
- near **0.1388**: `ademamix` gives way to `tie: adam, adamw_constant, ademamix`

The suite's pinned threshold is **0.147** — read its row above, not just the headline number.
