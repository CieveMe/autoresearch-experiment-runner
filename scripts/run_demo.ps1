$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$env:PYTHONPATH = $root
$config = Join-Path $root 'examples/classification.json'
$output = Join-Path $root 'runs/demo'
python -m autoresearch.cli validate-config --config $config
python -m autoresearch.cli run --config $config --output $output
Get-Content -LiteralPath (Join-Path $output 'report.md')
