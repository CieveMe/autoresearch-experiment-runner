# AutoResearch Lite 实验报告

- 任务：capacity expansion, hidden [16,16]: the same four claim families
- 论文：Cross-paper capacity expansion (Adam 2014, AdEMAMix 2024, Schedule-Free 2024)
- 论文标识：internal-capacity-expansion
- 假设：Same six pre-registered hypotheses as the [64] run, for a deeper network. Overfitting is expected to dominate here, which is exactly what H4 predicts; the run tests whether the schedule-free architecture effect (H2) survives it.
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`f7e895a451eb54e0bbb99fc07efe2cc826e2fcb494ae90d220a5148b3fb4dfa8`

## 最优方案

`adagrad`：主指标 `test_loss` = **0.104154**，测试准确率 **95.50%**，测试损失 `0.10415434`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| adagrad | 95.50% | 0.10415434 | 200 | 13 | 16763.584 |
| schedule_free_adamw | 91.00% | 0.13710241 | 200 | 4 | 16717.697 |
| adamw_cosine | 92.50% | 0.14850653 | 200 | 15 | 16088.04 |
| adamw_constant | 93.50% | 0.21983288 | 200 | 15 | 16568.716 |
| adam | 93.50% | 0.21983288 | 200 | 15 | 16697.389 |
| ademamix | 92.50% | 0.24444579 | 200 | 15 | 17177.34 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.147` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
