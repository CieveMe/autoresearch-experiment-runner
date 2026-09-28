# Threshold curves — where does the speed ranking hold?

Each suite is read from its committed loss curves; no experiment was re-run to produce this.
`epochs_to_target` is a function of the threshold, so a single number is a slice, not a fact.

| suite | fastest arm at the tight end | fastest at the loose end | ranking changes (strict) | tied thresholds |
|---|---|---|---:|---:|
| `optimizers` | `adam_no_bias_correction` | `adagrad` | 1 | 0 |
| `optimizers-mlp` | `adam` | `sgd_momentum` | 1 | 0 |
| `schedule-free-mlp` | `adamw_constant` | `schedule_free_adamw` | 1 | 1 |
| `capacity-h32` | `ademamix` | `tie: adam, adamw_constant, ademamix` | 0 | 4 |
| `capacity-h8x8` | `ademamix` | `tie: adam, adamw_constant, adamw_cosine, ademamix` | 0 | 8 |
