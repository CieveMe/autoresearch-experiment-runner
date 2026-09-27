$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$env:PYTHONPATH = $root

# Thin wrapper kept for compatibility: scripts/repro.py is the real entry point,
# it also verifies the expected numbers and runs the unit tests.
python (Join-Path $root 'scripts/repro.py')
exit $LASTEXITCODE
