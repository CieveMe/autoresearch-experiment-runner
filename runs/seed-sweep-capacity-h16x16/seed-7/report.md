# AutoResearch Lite 实验报告

- 任务：capacity expansion, hidden [16,16]: the same four claim families
- 论文：Cross-paper capacity expansion (Adam 2014, AdEMAMix 2024, Schedule-Free 2024)
- 论文标识：internal-capacity-expansion
- 假设：Same six pre-registered hypotheses as the [64] run, for a deeper network. Overfitting is expected to dominate here, which is exactly what H4 predicts; the run tests whether the schedule-free architecture effect (H2) survives it.
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`f3b53a15b0ff20a5818924d74fdcb3e4202e02a554ad98615e6f46ba1418a485`

## 最优方案

`schedule_free_adamw`：主指标 `test_loss` = **0.117777**，测试准确率 **94.00%**，测试损失 `0.11777748`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| schedule_free_adamw | 94.00% | 0.11777748 | 200 | 20 | 14476.799 |
| adagrad | 93.00% | 0.14288459 | 200 | 60 | 12646.504 |
| adamw_cosine | 94.00% | 0.14315398 | 200 | 34 | 12944.119 |
| adamw_constant | 94.00% | 0.17496292 | 200 | 34 | 12870.273 |
| adam | 94.00% | 0.17496292 | 200 | 34 | 13152.595 |
| ademamix | 93.00% | 0.18106628 | 200 | 34 | 12805.796 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.147` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
