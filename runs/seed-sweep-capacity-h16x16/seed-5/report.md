# AutoResearch Lite 实验报告

- 任务：capacity expansion, hidden [16,16]: the same four claim families
- 论文：Cross-paper capacity expansion (Adam 2014, AdEMAMix 2024, Schedule-Free 2024)
- 论文标识：internal-capacity-expansion
- 假设：Same six pre-registered hypotheses as the [64] run, for a deeper network. Overfitting is expected to dominate here, which is exactly what H4 predicts; the run tests whether the schedule-free architecture effect (H2) survives it.
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`a9406ecabfbd74a9ee149ea8ee7c761e8136f9ec3d3aa4ed8b91dd98ec97ec41`

## 最优方案

`adagrad`：主指标 `test_loss` = **0.156859**，测试准确率 **94.50%**，测试损失 `0.15685924`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| adagrad | 94.50% | 0.15685924 | 200 | 15 | 16772.546 |
| schedule_free_adamw | 94.50% | 0.15757336 | 200 | 15 | 14720.752 |
| adamw_cosine | 94.50% | 0.18965774 | 200 | 21 | 17079.657 |
| adamw_constant | 93.50% | 0.22653092 | 200 | 21 | 17010.805 |
| adam | 93.50% | 0.22653092 | 200 | 21 | 16906.409 |
| ademamix | 93.50% | 0.22716234 | 200 | 21 | 16894.747 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.147` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
