# Reproducibility

## 环境

- Python 3.10 或更高版本
- 当前示例只依赖 Python 标准库
- 可选 Docker 环境，详见根目录 `Dockerfile`
- 已在 CPython 3.12.5 / Windows 11 x64 实测；CI 在 Linux 上覆盖 CPython 3.10 与 3.12

## 一条命令（推荐）

```bash
python scripts/repro.py        # 校验配置 → 运行实验 → 对照期望数值 → 跑单测，失败即非 0 退出
make repro                     # Linux/macOS
docker compose up --build      # 容器内同一套流程
python scripts/score_task.py   # 任务评分 + 负向控制
```

`scripts/repro.py` 会依次执行下面四步，并在第 3 步用 `expected/expected_metrics.json` 断言
17 项数值（损失、准确率、轮数、配置哈希），在第 4 步跑单元测试。期望值与容差见该文件；
`duration_ms` 不参与比对。

## 分步运行

```bash
python -m autoresearch.cli validate-config --config examples/classification.json
python -m autoresearch.cli run --config examples/classification.json --output runs/demo
python scripts/verify_results.py --results runs/demo/results.json
python -m unittest discover -s tests -v
```

Windows PowerShell：

```powershell
.\scripts\run_demo.ps1
```

## 多种子聚合

单个种子只能证明"可重复"，证明不了"结论可重复"。

```bash
python scripts/seed_sweep.py --seeds 0-9 --output runs/seed-sweep
```

输出每个种子的独立产物、`summary.json`（均值/标准差/最优次数/配对提升）与 `summary.md`。
已提交的聚合结果见 `runs/demo-verified/seed-sweep-summary.md`。

## 可复现约束

- 实验配置显式记录随机种子、数据规模、基线和对照方案。
- 运行器输出配置 SHA-256，便于确认结果对应的配置版本；该哈希**按归一化换行后的内容计算**，
  因此 Windows（`core.autocrlf=true`，检出为 CRLF）与 Linux 得到同一个哈希。
- 结果写入结构化 JSON，并生成 Markdown 报告。
- 提交实验结果时，应同时提交使用的配置和报告，不要只保留截图。
- 已提交的验证结果（`runs/demo-verified/`）由 `tests/test_harness.py` 反向断言：若重新生成得到的
  数值发生变化，单元测试会失败，避免"报告和代码悄悄漂移"。
