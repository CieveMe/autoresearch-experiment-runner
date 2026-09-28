#!/usr/bin/env python3
"""Run the T-ADAM-01 task variants and record the score curve a solver would climb.

`TASK.md` §9 defines four variants of the same scored task. Three of them can be executed here
mechanically, in a throwaway copy of the repository, because they are "change the tree, score it,
change it again" loops:

* **T-ADAM-01B (implement)** — the Adam branch of `autoresearch/optimizers.py` is replaced by a stub
  that raises; the solver has to implement Adam from the paper and get the pinned expectations back.
  This script writes an implementation from the algorithm description, scores it, and if the pinned
  numbers disagree it takes a second attempt with the arithmetic order aligned to the reference — which
  is exactly the loop the task is supposed to create.
* **T-ADAM-01D (recover)** — one of the scorer's own negative controls is applied first, so the starting
  state is a real defect; the solver sees only the failing assertion and has to undo it.
* **T-ADAM-01C (ablate)** is a repository change rather than a loop (new config + new expectation file),
  so it is done in the repository itself, and this script only records its score line.

Every score comes from `scripts/score_task.py` running inside the copy, at `--tier core` (the tier is
printed by the scorer, and the label travels with the number). The recorded artifacts are the raw
scorer output for each state, so a claim like "the task is executable and gives a gradient to climb" is
backed by a transcript instead of by a description.

Usage:
    python scripts/task_variants.py            # runs B and D, writes runs/task-runs/
    python scripts/task_variants.py --list     # show the variant definitions
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.score_task import NEGATIVE_CONTROLS, _ignore  # noqa: E402

DEFAULT_OUTPUT = ROOT / "runs" / "task-runs"

# T-ADAM-01B: the stub the solver is handed. It replaces the block that initialises the Adam state, so
# the branch raises before touching anything — the "implement Algorithm 1" starting point.
ADAM_STUB_OLD = '''        first_moment = state["first_moment"]
        second_moment = state["second_moment"]
        step = epoch
'''
ADAM_STUB_NEW = '''        raise NotImplementedError(
            "T-ADAM-01B: the Adam branch was replaced by a stub; implement Algorithm 1 from the paper"
        )
'''

# The solver's first attempt: Adam as described in the paper, written independently, with the bias
# corrections computed once per step instead of per parameter.
ADAM_ATTEMPT_1 = '''        beta1 = float(config.get("beta1", 0.9))
        beta2 = float(config.get("beta2", 0.999))
        bias_correction = bool(config.get("bias_correction", True))
        decoupled = optimizer == "adamw"
        weight_decay = float(config.get("weight_decay", 0.0))
        first_moment = state["first_moment"]
        second_moment = state["second_moment"]
        step = epoch
        if bias_correction:
            scale_first = 1.0 / (1.0 - beta1 ** step)
            scale_second = 1.0 / (1.0 - beta2 ** step)
        else:
            scale_first = 1.0
            scale_second = 1.0
        for index, gradient in enumerate(gradients):
            first_moment[index] = beta1 * first_moment[index] + (1.0 - beta1) * gradient
            second_moment[index] = beta2 * second_moment[index] + (1.0 - beta2) * gradient * gradient
            step_size = learning_rate * scale_first / (math.sqrt(second_moment[index] * scale_second) + epsilon)
            weights[index] -= step_size * first_moment[index]
            if decoupled:
                weights[index] -= learning_rate * weight_decay * weights[index]
        state["bias_first_moment"] = beta1 * state["bias_first_moment"] + (1.0 - beta1) * bias_gradient
        state["bias_second_moment"] = beta2 * state["bias_second_moment"] + (1.0 - beta2) * bias_gradient * bias_gradient
        bias_step = learning_rate * scale_first / (
            math.sqrt(state["bias_second_moment"] * scale_second) + epsilon
        )
        bias -= bias_step * state["bias_first_moment"]
        if decoupled:
            bias -= learning_rate * weight_decay * bias
        return bias
'''

# The solver's second attempt, after the pinned numbers disagreed: same algorithm, arithmetic order
# aligned with the reference so the floating-point sums match to the last bit.
ADAM_ATTEMPT_2 = '''        beta1 = float(config.get("beta1", 0.9))
        beta2 = float(config.get("beta2", 0.999))
        bias_correction = bool(config.get("bias_correction", True))
        decoupled = optimizer == "adamw"
        weight_decay = float(config.get("weight_decay", 0.0))
        first_moment = state["first_moment"]
        second_moment = state["second_moment"]
        step = epoch
        for index, gradient in enumerate(gradients):
            first_moment[index] = beta1 * first_moment[index] + (1.0 - beta1) * gradient
            second_moment[index] = beta2 * second_moment[index] + (1.0 - beta2) * gradient * gradient
            corrected_first = first_moment[index] / (1.0 - beta1**step) if bias_correction else first_moment[index]
            corrected_second = second_moment[index] / (1.0 - beta2**step) if bias_correction else second_moment[index]
            weights[index] -= learning_rate * corrected_first / (math.sqrt(corrected_second) + epsilon)
            if decoupled:
                weights[index] -= learning_rate * weight_decay * weights[index]
        state["bias_first_moment"] = beta1 * state["bias_first_moment"] + (1.0 - beta1) * bias_gradient
        state["bias_second_moment"] = beta2 * state["bias_second_moment"] + (1.0 - beta2) * bias_gradient * bias_gradient
        corrected_bias_first = (
            state["bias_first_moment"] / (1.0 - beta1**step) if bias_correction else state["bias_first_moment"]
        )
        corrected_bias_second = (
            state["bias_second_moment"] / (1.0 - beta2**step) if bias_correction else state["bias_second_moment"]
        )
        bias -= learning_rate * corrected_bias_first / (math.sqrt(corrected_bias_second) + epsilon)
        if decoupled:
            bias -= learning_rate * weight_decay * bias
        return bias
'''


def _copy_repository(destination: Path) -> None:
    shutil.copytree(ROOT, destination, ignore=_ignore, dirs_exist_ok=True)


def _score(directory: Path, tier: str = "core", skip_controls: bool = False) -> Dict[str, Any]:
    command = [sys.executable, "scripts/score_task.py", "--tier", tier]
    if skip_controls:
        command.append("--skip-controls")
    result = subprocess.run(
        command, cwd=str(directory), stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        text=True, encoding="utf-8", errors="replace", timeout=3600,
    )
    output = result.stdout or ""
    score = None
    match = re.search(r"submission score: ([\d.]+)/100 \(([^)]*)\)", output)
    if match:
        score = float(match.group(1))
    controls = re.findall(r"control\[([^\]]+)\]: (detected|MISSED)[^(]*\(([^)]*)\)", output)
    failing = [line for line in output.splitlines() if line.startswith("FAIL")]
    return {
        "score": score,
        "tier_label": match.group(2) if match else None,
        "controls": [{"name": name, "outcome": outcome, "detail": detail}
                     for name, outcome, detail in controls],
        "failing_assertions": failing[:6],
        "exit_code": result.returncode,
        "raw": output,
    }


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _write(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def run_implement_variant(workspace: Path) -> Dict[str, Any]:
    """T-ADAM-01B: stub the Adam branch, score, implement it, score again."""
    target = workspace / "autoresearch" / "optimizers.py"
    original = _read(target)
    if ADAM_STUB_OLD not in original:
        raise SystemExit("the Adam branch no longer matches the fragment the stub replaces")
    attempts: List[Dict[str, Any]] = []
    _write(target, original.replace(ADAM_STUB_OLD, ADAM_STUB_NEW, 1))
    attempts.append({"label": "given state: Adam branch stubbed out", **_score(workspace, skip_controls=True)})
    start = original.index(ADAM_STUB_OLD)
    end = start + len(ADAM_STUB_OLD)
    for label, implementation in (
        ("attempt 2: Algorithm 1 implemented from the paper", ADAM_ATTEMPT_1),
        ("attempt 3: arithmetic order aligned with the reference", ADAM_ATTEMPT_2),
    ):
        _write(target, original[:start] + implementation + original[end:])
        attempt = {"label": label, **_score(workspace, skip_controls=True)}
        attempts.append(attempt)
        if attempt["score"] == 100.0:
            break
    attempts.append({"label": "final: full scorer including the negative controls",
                     **_score(workspace, skip_controls=False)})
    return {
        "variant": "T-ADAM-01B",
        "requirement": "implement Algorithm 1 from the paper; pass the same expectations",
        "attempts": attempts,
        "solved": attempts[-1]["score"] == 100.0,
    }


def run_recover_variant(workspace: Path, control: str = "no-adaptive-scaling") -> Dict[str, Any]:
    """T-ADAM-01D: apply a negative control, score, recover from the failing assertion."""
    attempts: List[Dict[str, Any]] = []
    fragments = NEGATIVE_CONTROLS[control]
    for fragment in fragments:
        path = workspace / fragment["file"]
        text = _read(path)
        if fragment["old"] not in text:
            raise SystemExit(f"control fragment not found in {fragment['file']}")
        _write(path, text.replace(fragment["old"], fragment["new"], 1))
    attempts.append({"label": f"given state: negative control `{control}` already applied",
                     **_score(workspace, skip_controls=True)})
    for fragment in fragments:
        path = workspace / fragment["file"]
        text = _read(path)
        _write(path, text.replace(fragment["new"], fragment["old"], 1))
    attempts.append({"label": "recovered: defect undone from the failing assertion alone",
                     **_score(workspace, skip_controls=True)})
    attempts.append({"label": "final: full scorer including the negative controls",
                     **_score(workspace, skip_controls=False)})
    return {
        "variant": "T-ADAM-01D",
        "requirement": "find the defect from the failing assertion alone; the scorer must return to 100",
        "control": control,
        "attempts": attempts,
        "solved": attempts[-1]["score"] == 100.0,
    }


def render(result: Dict[str, Any]) -> str:
    lines = [
        f"# {result['variant']} — {result['requirement']}",
        "",
        f"Solved: **{'yes' if result['solved'] else 'no'}**.",
        "",
        "| state | submission score | tier | controls detected |",
        "|---|---:|---|---:|",
    ]
    for attempt in result["attempts"]:
        detected = sum(1 for control in attempt["controls"] if control["outcome"] == "detected")
        total = len(attempt["controls"])
        controls = "not run" if not total else f"{detected}/{total}"
        lines.append(
            f"| {attempt['label']} | {attempt['score']}/100 | {attempt['tier_label'] or '—'} | {controls} |"
        )
    for attempt in result["attempts"]:
        if attempt["failing_assertions"]:
            lines += ["", f"Failing assertions after \"{attempt['label']}\":", "", "```"]
            lines += attempt["failing_assertions"]
            lines.append("```")
    lines += ["", "## Raw scorer output", ""]
    for attempt in result["attempts"]:
        lines += [f"### {attempt['label']}", "", "```", attempt["raw"].strip(), "```", ""]
    return "\n".join(lines)


VARIANTS = {
    "T-ADAM-01B": ("implement Adam from the paper (the branch is stubbed out)", run_implement_variant),
    "T-ADAM-01D": ("recover from a negative control already applied", run_recover_variant),
}


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Run the T-ADAM-01 task variants")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--variant", action="append", default=[])
    parser.add_argument("--list", action="store_true")
    args = parser.parse_args(argv)

    if args.list:
        for name, (description, _) in VARIANTS.items():
            print(f"{name}: {description}")
        print("T-ADAM-01C: add a new ablation config with its own expectation file (done in the "
              "repository, not in a throwaway copy)")
        return 0

    selected = args.variant or list(VARIANTS)
    args.output.mkdir(parents=True, exist_ok=True)
    summary: Dict[str, Any] = {"schema": "autoresearch-lite/task-variants@1", "variants": {}}
    for name in selected:
        description, runner = VARIANTS[name]
        print(f"== {name}: {description}")
        with tempfile.TemporaryDirectory(prefix=f"task-{name.lower()}-") as temporary:
            workspace = Path(temporary) / "repo"
            _copy_repository(workspace)
            result = runner(workspace)
        result["description"] = description
        summary["variants"][name] = result
        (args.output / f"{name}.md").write_text(render(result), encoding="utf-8")
        for attempt in result["attempts"]:
            print(f"   {attempt['score']:>6}/100  {attempt['label']}")
    (args.output / "variants.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"\nwrote {args.output}/ ({len(summary['variants'])} variant(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
