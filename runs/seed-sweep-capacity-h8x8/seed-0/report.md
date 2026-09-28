# AutoResearch Lite 实验报告

- 任务：capacity check, hidden [8,8]: does depth change the answers that width did not?
- 论文：Cross-paper capacity check (Adam 2014, AdEMAMix 2024, Schedule-Free 2024)
- 论文标识：internal-capacity-check
- 假设：Same capacity question as the [32] run, for a two-layer [8,8] network: do the directions survive a change of depth as well as width, and does the train-loss ranking continue to diverge from the test-loss ranking as capacity grows?
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`073e27862d702762cc10bbf47c72cede8d4cd1e2ceb2e1d4dde78a521a05b872`

## 最优方案

`adamw_constant`：主指标 `test_loss` = **0.094957**，测试准确率 **96.50%**，测试损失 `0.09495689`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| adamw_constant | 96.50% | 0.09495689 | 200 | 5 | 7558.037 |
| adam | 96.50% | 0.09495689 | 200 | 5 | 5883.311 |
| ademamix | 96.00% | 0.09957575 | 200 | 5 | 5436.511 |
| adagrad | 95.50% | 0.10615257 | 200 | 6 | 6362.469 |
| adamw_cosine | 95.00% | 0.11290656 | 200 | 5 | 6896.318 |
| schedule_free_adamw | 94.00% | 0.11778492 | 200 | 4 | 6761.023 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.147` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
