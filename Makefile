# AutoResearch Lite - one-command reproduction.
# `make repro` is the entry point quoted in REPRODUCTION.md and TASK.md.
# On Windows without make, run: python scripts/repro.py
.PHONY: help repro repro-main repro-optimizers run verify test sweep score docker clean

PYTHON ?= python3

help:
	@echo "make repro    - validate, run, verify expected numbers, run tests"
	@echo "make repro-main       - only the Adam mechanism suite"
	@echo "make repro-optimizers - only the optimizer convergence-speed suite"
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

run:
	$(PYTHON) -m autoresearch.cli run --config examples/classification.json --output runs/demo

verify:
	$(PYTHON) scripts/verify_results.py --results runs/demo/results.json
	$(PYTHON) scripts/verify_results.py --results runs/optimizers/results.json --expected expected/expected_optimizers.json

test:
	$(PYTHON) -m unittest discover -s tests -v

sweep:
	$(PYTHON) scripts/seed_sweep.py --seeds 0-9 --output runs/seed-sweep
	$(PYTHON) scripts/seed_sweep.py --config examples/optimizers.json --seeds 0-9 --output runs/seed-sweep-optimizers

score:
	$(PYTHON) scripts/score_task.py

docker:
	docker compose up --build --exit-code-from repro

clean:
	$(PYTHON) -c "import shutil,pathlib;[shutil.rmtree(p, ignore_errors=True) for p in [pathlib.Path('runs/demo'), pathlib.Path('autoresearch/__pycache__'), pathlib.Path('tests/__pycache__')]]"
