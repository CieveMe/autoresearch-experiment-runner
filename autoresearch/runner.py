from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path
from typing import Any, Dict, List

from .dataset import make_dataset, split_dataset
from .model import epochs_to_target, evaluate, train

# Metrics where a smaller value is better. Defined once: duplicating this set
# across the runner, the seed sweep and the one-command entry already produced a
# real bug (a sweep reported RMSProp as the per-seed winner because the new
# metric was missing from one copy of the list).
LOWER_IS_BETTER_METRICS = frozenset(
    {"test_loss", "train_loss", "duration_ms", "epochs", "epochs_to_target"}
)


def is_lower_is_better(metric: str) -> bool:
    return metric in LOWER_IS_BETTER_METRICS


def _read_json(path: Path) -> Dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON config: {exc}") from exc


def config_sha256(path: Path) -> str:
    """Hash a config file with newlines normalized to LF.

    Hashing raw bytes makes the reported config hash depend on the checkout
    platform: Git on Windows (``core.autocrlf=true``) rewrites LF to CRLF, so
    the same revision produced two different hashes. Normalizing newlines keeps
    the identity of a revision stable across Windows, Linux and Docker.
    """
    payload = path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha256(payload).hexdigest()


def _validate(config: Dict[str, Any]) -> None:
    required = {"task", "dataset", "baseline", "experiments"}
    missing = sorted(required - set(config))
    if missing:
        raise ValueError(f"missing config fields: {', '.join(missing)}")
    if not isinstance(config["experiments"], list) or not config["experiments"]:
        raise ValueError("experiments must be a non-empty list")
    for item in config["experiments"]:
        if "name" not in item:
            raise ValueError("every experiment needs a name")


def run(config_path: Path, output_dir: Path) -> Dict[str, Any]:
    config = _read_json(config_path)
    _validate(config)
    dataset_config = config["dataset"]
    all_rows = make_dataset(
        size=int(dataset_config.get("size", 800)),
        seed=int(config.get("seed", 7)),
        noise=float(dataset_config.get("noise", 0.18)),
    )
    train_rows, test_rows = split_dataset(all_rows, float(dataset_config.get("test_ratio", 0.25)))
    trials = [{"name": "baseline", **config["baseline"]}, *config["experiments"]]
    target_loss = config.get("target_loss")
    results: List[Dict[str, Any]] = []
    for trial in trials:
        started = time.perf_counter()
        weights, bias, epochs, train_loss, loss_curve = train(train_rows, trial)
        train_metrics = evaluate(train_rows, weights, bias, float(trial.get("weight_decay", 0.0)))
        test_metrics = evaluate(test_rows, weights, bias, float(trial.get("weight_decay", 0.0)))
        results.append({
            "name": trial["name"],
            "config": trial,
            "train_accuracy": round(train_metrics["accuracy"], 6),
            "test_accuracy": round(test_metrics["accuracy"], 6),
            "train_loss": round(train_loss, 8),
            "test_loss": round(test_metrics["loss"], 8),
            "epochs": epochs,
            "epochs_to_target": (
                epochs_to_target(loss_curve, float(target_loss)) if target_loss is not None else None
            ),
            "loss_curve": [round(value, 8) for value in loss_curve],
            "duration_ms": round((time.perf_counter() - started) * 1000, 3),
        })
    metric = str(config.get("metric", "test_accuracy"))
    lower_is_better = is_lower_is_better(metric)
    ranked = sorted(results, key=lambda item: rank_key(item, metric, lower_is_better))
    best = ranked[0]
    payload = {
        "task": config["task"],
        "paper": config.get("paper", {}),
        "hypothesis": config.get("hypothesis", ""),
        "metric": config.get("metric", "test_accuracy"),
        "config_sha256": config_sha256(config_path),
        "dataset": {"train_size": len(train_rows), "test_size": len(test_rows), **dataset_config},
        "target_loss": target_loss,
        "best": best,
        "results": results,
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "results.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    (output_dir / "report.md").write_text(_report(payload), encoding="utf-8")
    _write_loss_curves(results, output_dir)
    return payload


def rank_key(item: Dict[str, Any], metric: str, lower_is_better: bool) -> tuple:
    """Rank without crashing on "never reached the target" (``None``) entries."""
    value = item.get(metric)
    if value is None:
        value = float("inf") if lower_is_better else float("-inf")
    return ((1 if lower_is_better else -1) * value, item["test_loss"])


def _write_loss_curves(results: List[Dict[str, Any]], output_dir: Path) -> None:
    """Export per-epoch curves as CSV so a convergence claim can be plotted."""
    curves = [(item["name"], item.get("loss_curve") or []) for item in results]
    if not any(curve for _, curve in curves):
        return
    width = max(len(curve) for _, curve in curves)
    lines = [",".join(["epoch", *[name for name, _ in curves]])]
    for index in range(width):
        row = [str(index + 1)]
        row.extend(f"{curve[index]:.8f}" if index < len(curve) else "" for _, curve in curves)
        lines.append(",".join(row))
    (output_dir / "loss-curves.csv").write_text("\n".join(lines) + "\n", encoding="utf-8")


def _report(payload: Dict[str, Any]) -> str:
    lines = [
        f"# AutoResearch Lite 实验报告\n",
        f"- 任务：{payload['task']}",
        f"- 论文：{payload.get('paper', {}).get('title', '未指定')}",
        f"- 论文标识：{payload.get('paper', {}).get('identifier', '未指定')}",
        f"- 假设：{payload['hypothesis']}",
        f"- 数据集：训练 {payload['dataset']['train_size']} 条，测试 {payload['dataset']['test_size']} 条",
        f"- 配置 SHA-256：`{payload['config_sha256']}`\n",
        f"## 最优方案\n",
        f"`{payload['best']['name']}`：主指标 `{payload['metric']}` = "
        f"**{_format_metric(payload['best'].get(payload['metric']))}**，"
        f"测试准确率 **{payload['best']['test_accuracy']:.2%}**，测试损失 `{payload['best']['test_loss']}`。\n",
        "## 对比结果\n",
        "| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    lower_is_better = is_lower_is_better(payload["metric"])
    for item in sorted(payload["results"], key=lambda value: rank_key(value, payload["metric"], lower_is_better)):
        lines.append(
            f"| {item['name']} | {item['test_accuracy']:.2%} | {item['test_loss']} | {item['epochs']} | "
            f"{_format_metric(item.get('epochs_to_target'))} | {item['duration_ms']} |"
        )
    lines.extend([
        "",
        "## 复现命令",
        "",
        "```bash",
        "python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测",
        "make repro                       # 同上（Linux/macOS）",
        "```",
        "",
        "本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；",
        "数值比对详见 `REPRODUCTION.md`。",
        "",
    ])
    if payload.get("target_loss") is not None:
        lines.extend([
            "达标轮数 = 训练损失首次小于或等于 "
            f"`{payload['target_loss']}` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。",
            "",
        ])
    return "\n".join(lines)


def _format_metric(value: Any) -> str:
    if value is None:
        return "未达标"
    if isinstance(value, float):
        return f"{value:.6f}"
    return str(value)
