# Threshold curve — `AdEMAMix on the two-layer MLP: speed versus final quality`

Trainer: `mlp` · metric: epochs until the training loss reaches the row's threshold.
`never` means the arm did not reach that threshold inside the budget.

| threshold | adamw | ademamix_no_warmups | ademamix_warmup_45 | ademamix_warmup_120 | sgd_momentum | fastest |
|---:|---:|---:|---:|---:|---:|---|
| 0.1380 | never | never | 120 | never | never | ademamix_warmup_45 |
| 0.1383 | never | never | 115 | never | never | ademamix_warmup_45 |
| 0.1385 | never | never | 111 | never | never | ademamix_warmup_45 |
| 0.1387 | never | never | 108 | never | never | ademamix_warmup_45 |
| 0.1390 | never | never | 105 | never | never | ademamix_warmup_45 |
| 0.1392 | never | never | 102 | never | never | ademamix_warmup_45 |
| 0.1394 | never | never | 100 | never | never | ademamix_warmup_45 |
| 0.1397 | never | never | 98 | never | never | ademamix_warmup_45 |
| 0.1399 | 118 | 114 | 96 | never | never | ademamix_warmup_45 |
| 0.1401 | 110 | 107 | 94 | never | never | ademamix_warmup_45 |
| 0.1404 | 103 | 101 | 92 | 104 | never | ademamix_warmup_45 |
| 0.1406 | 97 | 96 | 90 | 101 | never | ademamix_warmup_45 |
| 0.1408 | 92 | 91 | 88 | 98 | 117 | ademamix_warmup_45 |

## Reading

The fastest arm is `ademamix_warmup_45` at every threshold on this grid.

The suite's pinned threshold is **0.143** — read its row above, not just the headline number.
