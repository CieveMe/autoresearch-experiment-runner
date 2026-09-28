# Threshold curves — where does the speed ranking hold?

Each suite is read from its committed loss curves; no experiment was re-run to produce this.
`epochs_to_target` is a function of the threshold, so a single number is a slice, not a fact.

| suite | fastest arm at the tight end | fastest at the loose end | ranking changes (strict) | tied thresholds |
|---|---|---|---:|---:|
| `capacity-h64` | `ademamix` | `tie: adam, adamw_constant, ademamix` | 0 | 2 |
| `capacity-h16x16` | `ademamix` | `tie: adam, adamw_constant, adamw_cosine, ademamix` | 0 | 5 |
