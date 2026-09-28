# AutoResearch Lite 实验报告

- 任务：capacity check, hidden [8,8]: does depth change the answers that width did not?
- 论文：Cross-paper capacity check (Adam 2014, AdEMAMix 2024, Schedule-Free 2024)
- 论文标识：internal-capacity-check
- 假设：Same capacity question as the [32] run, for a two-layer [8,8] network: do the directions survive a change of depth as well as width, and does the train-loss ranking continue to diverge from the test-loss ranking as capacity grows?
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`fec73ad77781490ed80eb629f426f264313b7c1a71024e1ce49228bc82839b10`

## 最优方案

`adagrad`：主指标 `test_loss` = **0.145853**，测试准确率 **92.00%**，测试损失 `0.14585275`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| adagrad | 92.00% | 0.14585275 | 200 | 13 | 7573.376 |
| schedule_free_adamw | 94.00% | 0.15222152 | 200 | 7 | 7647.928 |
| adamw_cosine | 92.50% | 0.20395142 | 200 | 19 | 5885.575 |
| adamw_constant | 91.50% | 0.24320158 | 200 | 19 | 8107.299 |
| adam | 91.50% | 0.24320158 | 200 | 19 | 7660.604 |
| ademamix | 91.00% | 0.24937939 | 200 | 19 | 7780.861 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.147` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
