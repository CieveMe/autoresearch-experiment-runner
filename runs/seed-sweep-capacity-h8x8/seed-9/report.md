# AutoResearch Lite 实验报告

- 任务：capacity check, hidden [8,8]: does depth change the answers that width did not?
- 论文：Cross-paper capacity check (Adam 2014, AdEMAMix 2024, Schedule-Free 2024)
- 论文标识：internal-capacity-check
- 假设：Same capacity question as the [32] run, for a two-layer [8,8] network: do the directions survive a change of depth as well as width, and does the train-loss ranking continue to diverge from the test-loss ranking as capacity grows?
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`5762e5854a0c7d64c45eb00b74e614021d6040b01e80f68981a196479ab54afd`

## 最优方案

`adagrad`：主指标 `test_loss` = **0.150128**，测试准确率 **93.50%**，测试损失 `0.1501277`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| adagrad | 93.50% | 0.1501277 | 200 | 8 | 6131.339 |
| schedule_free_adamw | 92.50% | 0.15873 | 200 | 4 | 9284.453 |
| adamw_cosine | 92.00% | 0.20634378 | 200 | 3 | 5254.877 |
| ademamix | 91.00% | 0.24295102 | 200 | 3 | 8411.051 |
| adamw_constant | 91.50% | 0.24453105 | 200 | 3 | 6489.149 |
| adam | 91.50% | 0.24453105 | 200 | 3 | 6473.546 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.147` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
