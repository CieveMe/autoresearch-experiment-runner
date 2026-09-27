#!/usr/bin/env bash
set -euo pipefail
export PYTHONPATH="$(cd "$(dirname "$0")/.." && pwd)"
cd "$(dirname "$0")/.."

# Thin wrapper kept for compatibility: scripts/repro.py is the real entry point,
# it also verifies the expected numbers and runs the unit tests.
exec python3 scripts/repro.py "$@"
