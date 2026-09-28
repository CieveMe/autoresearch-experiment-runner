# Crossing stability across seeds

- `norm-layernorm` (adamw_cosine vs schedule_free_adamw): crossing in 1/10 seeds, mean 0.087745, spread 0.0; pinned-threshold winner consistent: False (None)
- `norm-batchnorm` (adamw_cosine vs schedule_free_adamw): crossing in 1/10 seeds, mean 0.088121, spread 0.0; pinned-threshold winner consistent: False (None)
- `init-he` (adamw_cosine vs schedule_free_adamw): crossing in 0/10 seeds, mean None, spread None; pinned-threshold winner consistent: False (None)
- `init-plain` (adamw_cosine vs schedule_free_adamw): crossing in 6/10 seeds, mean 0.127508, spread 0.022799; pinned-threshold winner consistent: True (adamw_cosine)
