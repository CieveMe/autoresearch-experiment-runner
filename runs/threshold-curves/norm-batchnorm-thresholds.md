# Threshold curve — `normalisation/initialisation robustness check, hidden [32], batchnorm on the hidden pre-activations (Xavier init): do the two negative results survive?`

Trainer: `mlp` · metric: epochs until the training loss reaches the row's threshold.
`never` means the arm did not reach that threshold inside the budget.

| threshold | adamw_cosine | adamw_constant | adam | adagrad | ademamix | schedule_free_adamw | fastest |
|---:|---:|---:|---:|---:|---:|---:|---|
| 0.1422 | never | never | never | never | 200 | never | ademamix |
| 0.1423 | never | 187 | 187 | never | 181 | never | ademamix |
| 0.1423 | never | 171 | 171 | never | 166 | never | ademamix |
| 0.1423 | never | 158 | 158 | never | 154 | never | ademamix |
| 0.1424 | never | 147 | 147 | never | 144 | never | ademamix |
| 0.1424 | never | 138 | 138 | never | 135 | never | ademamix |
| 0.1424 | never | 129 | 129 | never | 127 | never | ademamix |
| 0.1424 | never | 120 | 120 | never | 119 | never | ademamix |
| 0.1425 | 169 | 112 | 112 | never | 110 | never | ademamix |
| 0.1425 | 138 | 104 | 104 | never | 102 | never | ademamix |
| 0.1425 | 117 | 95 | 95 | never | 94 | never | ademamix |
| 0.1426 | 102 | 87 | 87 | never | 86 | 200 | ademamix |
| 0.1426 | 89 | 81 | 81 | 200 | 80 | 152 | ademamix |

## Reading

The fastest arm is `ademamix` at every threshold on this grid.

The suite's pinned threshold is **0.147** — read its row above, not just the headline number.
