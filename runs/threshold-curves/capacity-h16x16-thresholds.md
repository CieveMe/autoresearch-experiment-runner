# Threshold curve — `capacity expansion, hidden [16,16]: the same four claim families`

Trainer: `mlp` · metric: epochs until the training loss reaches the row's threshold.
`never` means the arm did not reach that threshold inside the budget.

| threshold | adamw_cosine | adamw_constant | adam | adagrad | ademamix | schedule_free_adamw | fastest |
|---:|---:|---:|---:|---:|---:|---:|---|
| 0.0944 | never | never | never | never | 200 | never | ademamix |
| 0.0981 | never | 189 | 189 | never | 189 | never | tie: adam, adamw_constant, ademamix |
| 0.1017 | never | 180 | 180 | never | 177 | never | ademamix |
| 0.1054 | never | 167 | 167 | never | 164 | never | ademamix |
| 0.1090 | never | 154 | 154 | never | 154 | never | tie: adam, adamw_constant, ademamix |
| 0.1127 | never | 138 | 138 | never | 135 | never | ademamix |
| 0.1163 | never | 121 | 121 | never | 118 | never | ademamix |
| 0.1200 | 130 | 104 | 104 | never | 102 | never | ademamix |
| 0.1236 | 98 | 87 | 87 | never | 86 | never | ademamix |
| 0.1273 | 75 | 71 | 71 | never | 70 | never | ademamix |
| 0.1309 | 56 | 54 | 54 | never | 54 | never | tie: adam, adamw_constant, ademamix |
| 0.1346 | 46 | 45 | 45 | never | 45 | 143 | tie: adam, adamw_constant, ademamix |
| 0.1382 | 40 | 40 | 40 | 194 | 40 | 86 | tie: adam, adamw_constant, adamw_cosine, ademamix |

## Reading

The fastest arm changes with the threshold:

- near **0.0981**: `ademamix` gives way to `tie: adam, adamw_constant, ademamix`
- near **0.1017**: `tie: adam, adamw_constant, ademamix` gives way to `ademamix`
- near **0.1090**: `ademamix` gives way to `tie: adam, adamw_constant, ademamix`
- near **0.1127**: `tie: adam, adamw_constant, ademamix` gives way to `ademamix`
- near **0.1309**: `ademamix` gives way to `tie: adam, adamw_constant, ademamix`
- near **0.1382**: `tie: adam, adamw_constant, ademamix` gives way to `tie: adam, adamw_constant, adamw_cosine, ademamix`

The suite's pinned threshold is **0.147** — read its row above, not just the headline number.
