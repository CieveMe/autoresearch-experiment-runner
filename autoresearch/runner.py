from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path
from typing import Any, Dict, List

from .dataset import make_dataset, split_dataset
from .model import evaluate, train


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
    results: List[Dict[str, Any]] = []
    for trial in trials:
        started = time.perf_counter()
        weights, bias, epochs, train_loss = train(train_rows, trial)
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
            "duration_ms": round((time.perf_counter() - started) * 1000, 3),
        })
    metric = str(config.get("metric", "test_accuracy"))
    lower_is_better = metric in {"test_loss", "train_loss", "duration_ms", "epochs"}
    ranked = sorted(
        results,
        key=lambda item: ((1 if lower_is_better else -1) * item[metric], item["test_loss"]),
    )
    best = ranked[0]
    payload = {
        "task": config["task"],
        "paper": config.get("paper", {}),
        "hypothesis": config.get("hypothesis", ""),
        "metric": config.get("metric", "test_accuracy"),
        "config_sha256": config_sha256(config_path),
        "dataset": {"train_size": len(train_rows), "test_size": len(test_rows), **dataset_config},
        "best": best,
        "results": results,
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "results.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    (output_dir / "report.md").write_text(_report(payload), encoding="utf-8")
    return payload


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
        f"`{payload['best']['name']}`：主指标 `{payload['metric']}` = **{payload['best'][payload['metric']]}**，测试准确率 **{payload['best']['test_accuracy']:.2%}**，测试损失 `{payload['best']['test_loss']}`。\n",
        "## 对比结果\n",
        "| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 耗时(ms) |",
        "|---|---:|---:|---:|---:|",
    ]
    lower_is_better = payload["metric"] in {"test_loss", "train_loss", "duration_ms", "epochs"}
    for item in sorted(payload["results"], key=lambda value: ((1 if lower_is_better else -1) * value[payload["metric"]], value["test_loss"])):
        lines.append(f"| {item['name']} | {item['test_accuracy']:.2%} | {item['test_loss']} | {item['epochs']} | {item['duration_ms']} |")
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
    return "\n".join(lines)
