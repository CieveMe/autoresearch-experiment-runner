# AutoResearch Lite 实验报告

- 任务：capacity expansion, hidden [16,16]: the same four claim families
- 论文：Cross-paper capacity expansion (Adam 2014, AdEMAMix 2024, Schedule-Free 2024)
- 论文标识：internal-capacity-expansion
- 假设：Same six pre-registered hypotheses as the [64] run, for a deeper network. Overfitting is expected to dominate here, which is exactly what H4 predicts; the run tests whether the schedule-free architecture effect (H2) survives it.
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`ba14e6aabfbeff99c7049d3dfe5af8555e3c4dd72bf9c52f5a307d2a49b8faf9`

## 最优方案

`adagrad`：主指标 `test_loss` = **0.147189**，测试准确率 **93.00%**，测试损失 `0.14718877`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| adagrad | 93.00% | 0.14718877 | 200 | 39 | 16967.358 |
| schedule_free_adamw | 92.00% | 0.15472854 | 200 | 12 | 16303.554 |
| adamw_cosine | 93.50% | 0.23574155 | 200 | 17 | 16852.621 |
| adamw_constant | 92.00% | 0.27507543 | 200 | 17 | 16850.955 |
| adam | 92.00% | 0.27507543 | 200 | 17 | 17172.874 |
| ademamix | 90.50% | 0.28167824 | 200 | 17 | 16217.893 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.147` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
