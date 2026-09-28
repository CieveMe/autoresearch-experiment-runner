# AutoResearch Lite - one-command reproduction.
# `make repro` is the entry point quoted in REPRODUCTION.md and TASK.md.
# On Windows without make, run: python scripts/repro.py
.PHONY: help repro repro-main repro-optimizers repro-ademamix repro-mlp repro-schedule-free repro-schedule-free-mlp repro-capacity repro-normalization run verify test sweep thresholds stats figures score docker clean

PYTHON ?= python3

help:
	@echo "make repro    - validate, run, verify expected numbers, run tests"
	@echo "make repro-main       - only the Adam mechanism suite"
	@echo "make repro-optimizers - only the optimizer convergence-speed suite"
	@echo "make repro-ablation   - only the T-ADAM-01C first-moment ablation"
	@echo "make repro-ademamix   - only the AdEMAMix (2024) suite"
	@echo "make repro-mlp        - the two MLP suites (does the ranking survive a bigger model?)"
	@echo "make repro-schedule-free - the schedule-free suite (tuned cosine baseline)"
	@echo "make repro-schedule-free-mlp - the same comparison on the MLP trainer"
	@echo "make repro-capacity   - the [32] and [8,8] capacity checks"
	@echo "make repro-normalization - the layernorm/batchnorm/He/plain robustness checks"
	@echo "make run      - run the experiments only"
	@echo "make verify   - compare runs/demo/results.json with expected/expected_metrics.json"
	@echo "make test     - run the unit tests"
	@echo "make sweep    - 10-seed sweep for the main suite and the optimizer suite"
	@echo "make thresholds - epochs-to-target curves over the threshold grid (Markdown + CSV + SVG)"
	@echo "make stats    - exact paired tests, effect sizes and intervals over the committed seed sweeps"
	@echo "make figures  - the forest plots and the noise/stability dot plot (SVG + stability.csv)"
	@echo "make score    - task score + negative controls"
	@echo "make docker   - the same reproduction inside Docker"
	@echo "make clean    - remove generated runs and caches"

repro:
	$(PYTHON) scripts/repro.py

repro-main:
	$(PYTHON) scripts/repro.py --suite main

repro-optimizers:
	$(PYTHON) scripts/repro.py --suite optimizers

repro-ablation:
	$(PYTHON) scripts/repro.py --suite ablation-adam-no-first-moment

repro-ademamix:
	$(PYTHON) scripts/repro.py --suite ademamix

repro-mlp:
	$(PYTHON) scripts/repro.py --suite optimizers-mlp
	$(PYTHON) scripts/repro.py --suite ademamix-mlp

repro-schedule-free:
	$(PYTHON) scripts/repro.py --suite schedule-free

repro-schedule-free-mlp:
	$(PYTHON) scripts/repro.py --suite schedule-free-mlp

repro-capacity:
	$(PYTHON) scripts/repro.py --suite capacity-h32
	$(PYTHON) scripts/repro.py --suite capacity-h8x8
	$(PYTHON) scripts/repro.py --suite capacity-h64
	$(PYTHON) scripts/repro.py --suite capacity-h16x16
	$(PYTHON) scripts/repro.py --suite activation-relu
	$(PYTHON) scripts/repro.py --suite activation-gelu

repro-normalization:
	$(PYTHON) scripts/repro.py --suite norm-layernorm
	$(PYTHON) scripts/repro.py --suite norm-batchnorm
	$(PYTHON) scripts/repro.py --suite init-he
	$(PYTHON) scripts/repro.py --suite init-plain

run:
	$(PYTHON) -m autoresearch.cli run --config examples/classification.json --output runs/demo

verify:
	$(PYTHON) scripts/verify_results.py --results runs/demo/results.json
	$(PYTHON) scripts/verify_results.py --results runs/optimizers/results.json --expected expected/expected_optimizers.json
	$(PYTHON) scripts/verify_results.py --results runs/ablation-adam-no-first-moment/results.json --expected expected/expected_ablation_adam_no_first_moment.json
	$(PYTHON) scripts/verify_results.py --results runs/ademamix/results.json --expected expected/expected_ademamix.json
	$(PYTHON) scripts/verify_results.py --results runs/optimizers-mlp/results.json --expected expected/expected_optimizers_mlp.json
	$(PYTHON) scripts/verify_results.py --results runs/ademamix-mlp/results.json --expected expected/expected_ademamix_mlp.json
	$(PYTHON) scripts/verify_results.py --results runs/schedule-free/results.json --expected expected/expected_schedule_free.json
	$(PYTHON) scripts/verify_results.py --results runs/schedule-free-mlp/results.json --expected expected/expected_schedule_free_mlp.json
	$(PYTHON) scripts/verify_results.py --results runs/capacity-h32/results.json --expected expected/expected_capacity_h32.json
	$(PYTHON) scripts/verify_results.py --results runs/capacity-h8x8/results.json --expected expected/expected_capacity_h8x8.json
	$(PYTHON) scripts/verify_results.py --results runs/capacity-h64/results.json --expected expected/expected_capacity_h64.json
	$(PYTHON) scripts/verify_results.py --results runs/capacity-h16x16/results.json --expected expected/expected_capacity_h16x16.json
	$(PYTHON) scripts/verify_results.py --results runs/activation-relu/results.json --expected expected/expected_activation_relu.json
	$(PYTHON) scripts/verify_results.py --results runs/activation-gelu/results.json --expected expected/expected_activation_gelu.json
	$(PYTHON) scripts/verify_results.py --results runs/norm-layernorm/results.json --expected expected/expected_norm_layernorm.json
	$(PYTHON) scripts/verify_results.py --results runs/norm-batchnorm/results.json --expected expected/expected_norm_batchnorm.json
	$(PYTHON) scripts/verify_results.py --results runs/init-he/results.json --expected expected/expected_init_he.json
	$(PYTHON) scripts/verify_results.py --results runs/init-plain/results.json --expected expected/expected_init_plain.json

test:
	$(PYTHON) -m unittest discover -s tests -v

sweep:
	$(PYTHON) scripts/seed_sweep.py --seeds 0-9 --output runs/seed-sweep
	$(PYTHON) scripts/seed_sweep.py --config examples/optimizers.json --seeds 0-9 --output runs/seed-sweep-optimizers
	$(PYTHON) scripts/seed_sweep.py --config examples/ademamix.json --seeds 0-9 --output runs/seed-sweep-ademamix --reference adamw,sgd_momentum
	$(PYTHON) -m autoresearch.cli run --config examples/ademamix-sweep.json --output runs/ademamix-tuning
	$(PYTHON) scripts/seed_sweep.py --config examples/optimizers-mlp.json --seeds 0-9 --output runs/seed-sweep-optimizers-mlp --reference adam,sgd_momentum
	$(PYTHON) scripts/seed_sweep.py --config examples/ademamix-mlp.json --seeds 0-9 --output runs/seed-sweep-ademamix-mlp --reference adamw,sgd_momentum
	$(PYTHON) -m autoresearch.cli run --config examples/optimizers-mlp-sweep.json --output runs/optimizers-mlp-tuning
	$(PYTHON) -m autoresearch.cli run --config examples/ademamix-mlp-sweep.json --output runs/ademamix-mlp-tuning
	$(PYTHON) scripts/seed_sweep.py --config examples/schedule-free.json --seeds 0-9 --output runs/seed-sweep-schedule-free --reference adamw_cosine,schedule_free_adamw
	$(PYTHON) -m autoresearch.cli run --config examples/schedule-free-sweep.json --output runs/schedule-free-tuning
	$(PYTHON) scripts/seed_sweep.py --config examples/schedule-free-mlp.json --seeds 0-9 --output runs/seed-sweep-schedule-free-mlp --reference adamw_cosine,schedule_free_adamw
	$(PYTHON) -m autoresearch.cli run --config examples/schedule-free-mlp-sweep.json --output runs/schedule-free-mlp-tuning

thresholds:
	$(PYTHON) scripts/threshold_curve.py --suite optimizers --suite optimizers-mlp --suite schedule-free --suite schedule-free-mlp --suite ademamix --suite ademamix-mlp --suite capacity-h32 --suite capacity-h8x8 --suite capacity-h64 --suite capacity-h16x16 --suite activation-relu --suite activation-gelu --suite norm-layernorm --suite norm-batchnorm --suite init-he --suite init-plain

score:
	$(PYTHON) scripts/score_task.py

stats:
	$(PYTHON) scripts/paired_stats.py

figures:
	$(PYTHON) scripts/figures.py

docker:
	docker compose up --build --exit-code-from repro

clean:
	$(PYTHON) -c "import shutil,pathlib;[shutil.rmtree(p, ignore_errors=True) for p in [pathlib.Path('runs/demo'), pathlib.Path('autoresearch/__pycache__'), pathlib.Path('tests/__pycache__')]]"
