# AutoResearch Lite 实验报告

- 任务：capacity expansion, hidden [16,16]: the same four claim families
- 论文：Cross-paper capacity expansion (Adam 2014, AdEMAMix 2024, Schedule-Free 2024)
- 论文标识：internal-capacity-expansion
- 假设：Same six pre-registered hypotheses as the [64] run, for a deeper network. Overfitting is expected to dominate here, which is exactly what H4 predicts; the run tests whether the schedule-free architecture effect (H2) survives it.
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`5a836fe026f1fd76f2e0f50fe1802c5a61f06c51bdd887507fe06ff10671f231`

## 最优方案

`adagrad`：主指标 `test_loss` = **0.108253**，测试准确率 **94.50%**，测试损失 `0.10825328`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| adagrad | 94.50% | 0.10825328 | 200 | 10 | 16347.901 |
| schedule_free_adamw | 95.00% | 0.10932971 | 200 | 5 | 16201.107 |
| adamw_cosine | 95.50% | 0.1103921 | 200 | 8 | 15435.268 |
| adamw_constant | 93.00% | 0.13826122 | 200 | 8 | 16444.303 |
| adam | 93.00% | 0.13826122 | 200 | 8 | 16319.329 |
| ademamix | 93.00% | 0.14037281 | 200 | 8 | 16324.683 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.147` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
