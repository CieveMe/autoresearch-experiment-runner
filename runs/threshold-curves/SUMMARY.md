# Threshold curves — where does the speed ranking hold?

Each suite is read from its committed loss curves; no experiment was re-run to produce this.
`epochs_to_target` is a function of the threshold, so a single number is a slice, not a fact.

| suite | fastest arm at the tight end | fastest at the loose end | ranking changes (strict) | tied thresholds |
|---|---|---|---:|---:|
| `norm-layernorm` | `schedule_free_adamw` | `schedule_free_adamw` | 0 | 0 |
| `norm-batchnorm` | `ademamix` | `ademamix` | 0 | 0 |
| `init-he` | `ademamix` | `tie: adam, adamw_constant, ademamix` | 0 | 3 |
| `init-plain` | `ademamix` | `adagrad` | 1 | 0 |
