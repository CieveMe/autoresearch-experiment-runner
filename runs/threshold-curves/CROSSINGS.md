# Crossing stability across seeds

- `schedule-free` (schedule_free_adamw vs adamw_cosine): crossing in 0/10 seeds, mean None, spread None; pinned-threshold winner consistent: True (adamw_cosine)
- `ademamix` (ademamix_tuned vs adamw): crossing in 1/10 seeds, mean 0.129625, spread 0.0; pinned-threshold winner consistent: True (tie)
- `ademamix-mlp` (ademamix_warmup_45 vs adamw): crossing in 2/10 seeds, mean 0.132939, spread 0.002614; pinned-threshold winner consistent: False (None)
