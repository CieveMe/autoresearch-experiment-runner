# AutoResearch Lite 实验报告

- 任务：capacity expansion, hidden [16,16]: the same four claim families
- 论文：Cross-paper capacity expansion (Adam 2014, AdEMAMix 2024, Schedule-Free 2024)
- 论文标识：internal-capacity-expansion
- 假设：Same six pre-registered hypotheses as the [64] run, for a deeper network. Overfitting is expected to dominate here, which is exactly what H4 predicts; the run tests whether the schedule-free architecture effect (H2) survives it.
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`d8060cfd6ce6eddf26fdd47532176b84fd28e1cc695a92e0b32650927dec9556`

## 最优方案

`schedule_free_adamw`：主指标 `test_loss` = **0.216638**，测试准确率 **92.50%**，测试损失 `0.21663818`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| schedule_free_adamw | 92.50% | 0.21663818 | 200 | 4 | 22146.819 |
| adagrad | 92.50% | 0.21957264 | 200 | 11 | 13597.353 |
| adamw_cosine | 91.50% | 0.27527534 | 200 | 4 | 13336.473 |
| ademamix | 91.50% | 0.34175118 | 200 | 4 | 22552.914 |
| adamw_constant | 90.50% | 0.36680311 | 200 | 4 | 12664.322 |
| adam | 90.50% | 0.36680311 | 200 | 4 | 13360.655 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.147` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
