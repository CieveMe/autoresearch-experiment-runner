# AutoResearch Lite 实验报告

- 任务：capacity expansion, hidden [16,16]: the same four claim families
- 论文：Cross-paper capacity expansion (Adam 2014, AdEMAMix 2024, Schedule-Free 2024)
- 论文标识：internal-capacity-expansion
- 假设：Same six pre-registered hypotheses as the [64] run, for a deeper network. Overfitting is expected to dominate here, which is exactly what H4 predicts; the run tests whether the schedule-free architecture effect (H2) survives it.
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`285656ca5f35909258822078f8430bb4f90e5bfe813739d1678b5100dc3bf382`

## 最优方案

`schedule_free_adamw`：主指标 `test_loss` = **0.082619**，测试准确率 **97.00%**，测试损失 `0.08261873`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| schedule_free_adamw | 97.00% | 0.08261873 | 200 | 10 | 16930.796 |
| adagrad | 97.00% | 0.10185254 | 200 | 29 | 16678.892 |
| adamw_cosine | 96.00% | 0.11107414 | 200 | 26 | 16764.112 |
| ademamix | 96.50% | 0.12027642 | 200 | 26 | 16433.445 |
| adamw_constant | 96.50% | 0.1248198 | 200 | 26 | 16449.934 |
| adam | 96.50% | 0.1248198 | 200 | 26 | 17511.061 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.147` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
