# Threshold curves — where does the speed ranking hold?

Each suite is read from its committed loss curves; no experiment was re-run to produce this.
`epochs_to_target` is a function of the threshold, so a single number is a slice, not a fact.

| suite | fastest arm at the tight end | fastest at the loose end | ranking changes |
|---|---|---|---|
| `capacity-h32` | `ademamix` | `adam` | 1 |
| `capacity-h8x8` | `ademamix` | `adam` | 1 |
