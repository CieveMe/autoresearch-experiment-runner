# Threshold curves — where does the speed ranking hold?

Each suite is read from its committed loss curves; no experiment was re-run to produce this.
`epochs_to_target` is a function of the threshold, so a single number is a slice, not a fact.

| suite | fastest arm at the tight end | fastest at the loose end | ranking changes |
|---|---|---|---|
| `schedule-free` | `adamw_constant` | `adamw_constant` | 0 |
| `schedule-free-mlp` | `adamw_constant` | `schedule_free_adamw` | 1 |
