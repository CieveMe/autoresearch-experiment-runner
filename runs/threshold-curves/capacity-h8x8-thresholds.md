# Threshold curve — `capacity check, hidden [8,8]: does depth change the answers that width did not?`

Trainer: `mlp` · metric: epochs until the training loss reaches the row's threshold.
`never` means the arm did not reach that threshold inside the budget.

| threshold | adamw_cosine | adamw_constant | adam | adagrad | ademamix | schedule_free_adamw | fastest |
|---:|---:|---:|---:|---:|---:|---:|---|
| 0.1330 | never | never | never | never | 200 | never | ademamix |
| 0.1339 | never | 161 | 161 | never | 152 | never | ademamix |
| 0.1348 | never | 118 | 118 | never | 113 | never | ademamix |
| 0.1356 | 103 | 88 | 88 | never | 86 | never | ademamix |
| 0.1365 | 72 | 68 | 68 | never | 67 | never | ademamix |
| 0.1374 | 52 | 51 | 51 | never | 51 | 186 | tie: adam, adamw_constant, ademamix |
| 0.1383 | 42 | 42 | 42 | never | 42 | 168 | tie: adam, adamw_constant, adamw_cosine, ademamix |
| 0.1392 | 41 | 40 | 40 | never | 40 | 150 | tie: adam, adamw_constant, ademamix |
| 0.1400 | 33 | 33 | 33 | never | 33 | 134 | tie: adam, adamw_constant, adamw_cosine, ademamix |
| 0.1409 | 30 | 30 | 30 | never | 30 | 120 | tie: adam, adamw_constant, adamw_cosine, ademamix |
| 0.1418 | 29 | 29 | 29 | never | 29 | 105 | tie: adam, adamw_constant, adamw_cosine, ademamix |
| 0.1427 | 29 | 29 | 29 | never | 29 | 86 | tie: adam, adamw_constant, adamw_cosine, ademamix |
| 0.1436 | 28 | 28 | 28 | 200 | 28 | 48 | tie: adam, adamw_constant, adamw_cosine, ademamix |

## Reading

The fastest arm changes with the threshold:

- near **0.1374**: `ademamix` gives way to `tie: adam, adamw_constant, ademamix`
- near **0.1383**: `tie: adam, adamw_constant, ademamix` gives way to `tie: adam, adamw_constant, adamw_cosine, ademamix`
- near **0.1392**: `tie: adam, adamw_constant, adamw_cosine, ademamix` gives way to `tie: adam, adamw_constant, ademamix`
- near **0.1400**: `tie: adam, adamw_constant, ademamix` gives way to `tie: adam, adamw_constant, adamw_cosine, ademamix`

The suite's pinned threshold is **0.147** — read its row above, not just the headline number.
