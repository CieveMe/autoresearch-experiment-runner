# Threshold curve — `normalisation/initialisation robustness check, hidden [32], layernorm on the hidden pre-activations (Xavier init): do the two negative results survive?`

Trainer: `mlp` · metric: epochs until the training loss reaches the row's threshold.
`never` means the arm did not reach that threshold inside the budget.

| threshold | adamw_cosine | adamw_constant | adam | adagrad | ademamix | schedule_free_adamw | fastest |
|---:|---:|---:|---:|---:|---:|---:|---|
| 0.1384 | never | never | never | never | never | 200 | schedule_free_adamw |
| 0.1388 | never | never | never | never | never | 183 | schedule_free_adamw |
| 0.1391 | never | never | never | never | never | 167 | schedule_free_adamw |
| 0.1394 | never | never | never | never | never | 150 | schedule_free_adamw |
| 0.1397 | never | never | never | never | never | 134 | schedule_free_adamw |
| 0.1400 | never | never | never | never | never | 118 | schedule_free_adamw |
| 0.1403 | never | never | never | 194 | never | 104 | schedule_free_adamw |
| 0.1406 | never | never | never | 182 | never | 92 | schedule_free_adamw |
| 0.1409 | never | never | never | 177 | never | 82 | schedule_free_adamw |
| 0.1412 | never | never | never | 141 | never | 72 | schedule_free_adamw |
| 0.1415 | never | 184 | 184 | 131 | 183 | 64 | schedule_free_adamw |
| 0.1419 | never | 157 | 157 | 123 | 156 | 57 | schedule_free_adamw |
| 0.1422 | 200 | 134 | 134 | 115 | 132 | 51 | schedule_free_adamw |

## Reading

The fastest arm is `schedule_free_adamw` at every threshold on this grid.

The suite's pinned threshold is **0.147** — read its row above, not just the headline number.
