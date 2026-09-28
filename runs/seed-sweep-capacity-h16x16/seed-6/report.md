# AutoResearch Lite 实验报告

- 任务：capacity expansion, hidden [16,16]: the same four claim families
- 论文：Cross-paper capacity expansion (Adam 2014, AdEMAMix 2024, Schedule-Free 2024)
- 论文标识：internal-capacity-expansion
- 假设：Same six pre-registered hypotheses as the [64] run, for a deeper network. Overfitting is expected to dominate here, which is exactly what H4 predicts; the run tests whether the schedule-free architecture effect (H2) survives it.
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`6aa63ebd9fe47b754d1d0d215efd0103cd5bf7beaed10200a892cfd1a514ccf4`

## 最优方案

`schedule_free_adamw`：主指标 `test_loss` = **0.158767**，测试准确率 **95.50%**，测试损失 `0.15876736`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| schedule_free_adamw | 95.50% | 0.15876736 | 200 | 3 | 12941.763 |
| adamw_cosine | 95.00% | 0.1629019 | 200 | 15 | 14265.359 |
| adagrad | 93.00% | 0.183584 | 200 | 8 | 12987.829 |
| adamw_constant | 94.00% | 0.22687265 | 200 | 15 | 12909.178 |
| adam | 94.00% | 0.22687265 | 200 | 15 | 13031.838 |
| ademamix | 94.00% | 0.23420125 | 200 | 15 | 12876.587 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.147` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
