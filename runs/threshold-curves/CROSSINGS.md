# Crossing stability across seeds

- `optimizers` (adam_no_bias_correction vs adagrad): crossing in 10/10 seeds, mean 0.136984, spread 0.045616; pinned-threshold winner consistent: True (adagrad)
- `optimizers-mlp` (adam vs sgd_momentum): crossing in 7/10 seeds, mean 0.116718, spread 0.052965; pinned-threshold winner consistent: False (None)
- `schedule-free-mlp` (adamw_constant vs schedule_free_adamw): crossing in 10/10 seeds, mean 0.119163, spread 0.050549; pinned-threshold winner consistent: False (None)
- `capacity-h32` (ademamix vs adam): crossing in 0/10 seeds, mean None, spread None; pinned-threshold winner consistent: True (tie)
- `capacity-h8x8` (ademamix vs adam): crossing in 5/10 seeds, mean 0.094733, spread 0.052847; pinned-threshold winner consistent: True (tie)
