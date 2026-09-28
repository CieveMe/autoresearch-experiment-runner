# Threshold curves — where does the speed ranking hold?

Each suite is read from its committed loss curves; no experiment was re-run to produce this.
`epochs_to_target` is a function of the threshold, so a single number is a slice, not a fact.

| suite | fastest arm at the tight end | fastest at the loose end | ranking changes (strict) | tied thresholds |
|---|---|---|---:|---:|
| `schedule-free` | `adamw_constant` | `tie: adamw_constant, adamw_cosine` | 0 | 8 |
| `ademamix` | `ademamix_tuned` | `tie: adamw, ademamix_no_slow_ema, ademamix_tuned` | 0 | 8 |
| `ademamix-mlp` | `ademamix_warmup_45` | `ademamix_warmup_45` | 0 | 0 |
