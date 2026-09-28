# AutoResearch Lite - one-command reproduction.
# `make repro` is the entry point quoted in REPRODUCTION.md and TASK.md.
# On Windows without make, run: python scripts/repro.py
.PHONY: help repro repro-main repro-optimizers repro-ademamix repro-mlp repro-schedule-free run verify test sweep score docker clean

PYTHON ?= python3

help:
	@echo "make repro    - validate, run, verify expected numbers, run tests"
	@echo "make repro-main       - only the Adam mechanism suite"
	@echo "make repro-optimizers - only the optimizer convergence-speed suite"
	@echo "make repro-ademamix   - only the AdEMAMix (2024) suite"
	@echo "make repro-mlp        - the two MLP suites (does the ranking survive a bigger model?)"
	@echo "make repro-schedule-free - the schedule-free suite (tuned cosine baseline)"
	@echo "make run      - run the experiments only"
	@echo "make verify   - compare runs/demo/results.json with expected/expected_metrics.json"
	@echo "make test     - run the unit tests"
	@echo "make sweep    - 10-seed sweep for the main suite and the optimizer suite"
	@echo "make score    - task score + negative controls"
	@echo "make docker   - the same reproduction inside Docker"
	@echo "make clean    - remove generated runs and caches"

repro:
	$(PYTHON) scripts/repro.py

repro-main:
	$(PYTHON) scripts/repro.py --suite main

repro-optimizers:
	$(PYTHON) scripts/repro.py --suite optimizers

repro-ademamix:
	$(PYTHON) scripts/repro.py --suite ademamix

repro-mlp:
	$(PYTHON) scripts/repro.py --suite optimizers-mlp
	$(PYTHON) scripts/repro.py --suite ademamix-mlp

repro-schedule-free:
	$(PYTHON) scripts/repro.py --suite schedule-free

run:
	$(PYTHON) -m autoresearch.cli run --config examples/classification.json --output runs/demo

verify:
	$(PYTHON) scripts/verify_results.py --results runs/demo/results.json
	$(PYTHON) scripts/verify_results.py --results runs/optimizers/results.json --expected expected/expected_optimizers.json
	$(PYTHON) scripts/verify_results.py --results runs/ademamix/results.json --expected expected/expected_ademamix.json
	$(PYTHON) scripts/verify_results.py --results runs/optimizers-mlp/results.json --expected expected/expected_optimizers_mlp.json
	$(PYTHON) scripts/verify_results.py --results runs/ademamix-mlp/results.json --expected expected/expected_ademamix_mlp.json
	$(PYTHON) scripts/verify_results.py --results runs/schedule-free/results.json --expected expected/expected_schedule_free.json

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

score:
	$(PYTHON) scripts/score_task.py

docker:
	docker compose up --build --exit-code-from repro

clean:
	$(PYTHON) -c "import shutil,pathlib;[shutil.rmtree(p, ignore_errors=True) for p in [pathlib.Path('runs/demo'), pathlib.Path('autoresearch/__pycache__'), pathlib.Path('tests/__pycache__')]]"
