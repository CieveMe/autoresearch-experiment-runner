#!/usr/bin/env bash
set -euo pipefail
export PYTHONPATH="$(cd "$(dirname "$0")/.." && pwd)"
python3 -m autoresearch.cli validate-config --config examples/classification.json
python3 -m autoresearch.cli run --config examples/classification.json --output runs/demo
cat runs/demo/report.md
