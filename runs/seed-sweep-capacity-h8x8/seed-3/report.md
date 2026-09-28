# AutoResearch Lite 实验报告

- 任务：capacity check, hidden [8,8]: does depth change the answers that width did not?
- 论文：Cross-paper capacity check (Adam 2014, AdEMAMix 2024, Schedule-Free 2024)
- 论文标识：internal-capacity-check
- 假设：Same capacity question as the [32] run, for a two-layer [8,8] network: do the directions survive a change of depth as well as width, and does the train-loss ranking continue to diverge from the test-loss ranking as capacity grows?
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`beba46d8a302cf3dd1f4d8d990d83e8e6cfae728262f1b585e3e4f3d717cede3`

## 最优方案

`adagrad`：主指标 `test_loss` = **0.130450**，测试准确率 **94.00%**，测试损失 `0.13045028`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| adagrad | 94.00% | 0.13045028 | 200 | 13 | 7560.707 |
| schedule_free_adamw | 95.00% | 0.14122537 | 200 | 7 | 7905.629 |
| adamw_cosine | 94.00% | 0.19414057 | 200 | 29 | 7741.179 |
| adamw_constant | 93.00% | 0.21421785 | 200 | 29 | 7647.746 |
| adam | 93.00% | 0.21421785 | 200 | 29 | 7558.018 |
| ademamix | 93.50% | 0.22545 | 200 | 29 | 7881.48 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.147` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
