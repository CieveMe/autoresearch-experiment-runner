# AutoResearch Lite - one-command reproduction.
# `make repro` is the entry point quoted in REPRODUCTION.md and TASK.md.
# On Windows without make, run: python scripts/repro.py
.PHONY: help repro run verify test docker clean

PYTHON ?= python3

help:
	@echo "make repro    - validate, run, verify expected numbers, run tests"
	@echo "make run      - run the experiments only"
	@echo "make verify   - compare runs/demo/results.json with expected/expected_metrics.json"
	@echo "make test     - run the unit tests"
	@echo "make docker   - the same reproduction inside Docker"
	@echo "make clean    - remove generated runs and caches"

repro:
	$(PYTHON) scripts/repro.py

run:
	$(PYTHON) -m autoresearch.cli run --config examples/classification.json --output runs/demo

verify:
	$(PYTHON) scripts/verify_results.py --results runs/demo/results.json

test:
	$(PYTHON) -m unittest discover -s tests -v

docker:
	docker compose up --build --exit-code-from repro

clean:
	$(PYTHON) -c "import shutil,pathlib;[shutil.rmtree(p, ignore_errors=True) for p in [pathlib.Path('runs/demo'), pathlib.Path('autoresearch/__pycache__'), pathlib.Path('tests/__pycache__')]]"
