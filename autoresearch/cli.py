from __future__ import annotations

import argparse
from pathlib import Path

from .runner import _read_json, _validate, run


def main() -> int:
    parser = argparse.ArgumentParser(description="Run reproducible paper-inspired experiments")
    subparsers = parser.add_subparsers(dest="command", required=True)
    run_parser = subparsers.add_parser("run", help="run baseline and experiment variants")
    run_parser.add_argument("--config", type=Path, required=True)
    run_parser.add_argument("--output", type=Path, required=True)
    validate_parser = subparsers.add_parser("validate-config", help="validate an experiment config")
    validate_parser.add_argument("--config", type=Path, required=True)
    args = parser.parse_args()
    if args.command == "validate-config":
        _validate(_read_json(args.config))
        print(f"valid config: {args.config}")
        return 0
    payload = run(args.config, args.output)
    print(f"best={payload['best']['name']} test_accuracy={payload['best']['test_accuracy']:.4f}")
    print(f"report={args.output / 'report.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
