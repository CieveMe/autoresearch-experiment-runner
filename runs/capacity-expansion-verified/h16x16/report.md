# AutoResearch Lite 实验报告

- 任务：capacity expansion, hidden [16,16]: the same four claim families
- 论文：Cross-paper capacity expansion (Adam 2014, AdEMAMix 2024, Schedule-Free 2024)
- 论文标识：internal-capacity-expansion
- 假设：Same six pre-registered hypotheses as the [64] run, for a deeper network. Overfitting is expected to dominate here, which is exactly what H4 predicts; the run tests whether the schedule-free architecture effect (H2) survives it.
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`c1fa52ce7ab0acb6e47343c4657974452af36a4fdb4a0a7af036964411720644`

## 最优方案

`schedule_free_adamw`：主指标 `test_loss` = **0.117777**，测试准确率 **94.00%**，测试损失 `0.11777748`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| schedule_free_adamw | 94.00% | 0.11777748 | 200 | 20 | 16310.517 |
| adagrad | 93.00% | 0.14288459 | 200 | 60 | 16366.672 |
| adamw_cosine | 94.00% | 0.14315398 | 200 | 34 | 14863.845 |
| adamw_constant | 94.00% | 0.17496292 | 200 | 34 | 16465.726 |
| adam | 94.00% | 0.17496292 | 200 | 34 | 15556.639 |
| ademamix | 93.00% | 0.18106628 | 200 | 34 | 16158.743 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.147` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
