# AutoResearch Lite 实验报告

- 任务：capacity expansion, hidden [16,16]: the same four claim families
- 论文：Cross-paper capacity expansion (Adam 2014, AdEMAMix 2024, Schedule-Free 2024)
- 论文标识：internal-capacity-expansion
- 假设：Same six pre-registered hypotheses as the [64] run, for a deeper network. Overfitting is expected to dominate here, which is exactly what H4 predicts; the run tests whether the schedule-free architecture effect (H2) survives it.
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`8c0a5ba5fcdd5e95728cb2f4d419505781a954ae970ae4ca4eb276b8398ee270`

## 最优方案

`schedule_free_adamw`：主指标 `test_loss` = **0.161237**，测试准确率 **93.00%**，测试损失 `0.16123713`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| schedule_free_adamw | 93.00% | 0.16123713 | 200 | 7 | 16612.286 |
| adagrad | 92.00% | 0.16638154 | 200 | 9 | 16736.834 |
| adamw_cosine | 92.50% | 0.19882382 | 200 | 13 | 17344.689 |
| adamw_constant | 93.00% | 0.25217278 | 200 | 13 | 18779.513 |
| adam | 93.00% | 0.25217278 | 200 | 13 | 16396.829 |
| ademamix | 92.50% | 0.2542055 | 200 | 13 | 17166.131 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.147` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
