# AutoResearch Lite 实验报告

- 任务：capacity check, hidden [8,8]: does depth change the answers that width did not?
- 论文：Cross-paper capacity check (Adam 2014, AdEMAMix 2024, Schedule-Free 2024)
- 论文标识：internal-capacity-check
- 假设：Same capacity question as the [32] run, for a two-layer [8,8] network: do the directions survive a change of depth as well as width, and does the train-loss ranking continue to diverge from the test-loss ranking as capacity grows?
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`dd1fe09b9b043e414434101f48c02990836eac467bd58ac8566caf3b477c9d6e`

## 最优方案

`schedule_free_adamw`：主指标 `test_loss` = **0.124687**，测试准确率 **93.50%**，测试损失 `0.1246872`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| schedule_free_adamw | 93.50% | 0.1246872 | 200 | 20 | 5305.343 |
| adagrad | 93.50% | 0.12680418 | 200 | 26 | 5462.303 |
| adamw_cosine | 93.50% | 0.13495187 | 200 | 26 | 5346.014 |
| adamw_constant | 93.50% | 0.14107068 | 200 | 26 | 5898.186 |
| adam | 93.50% | 0.14107068 | 200 | 26 | 5561.125 |
| ademamix | 93.50% | 0.14184666 | 200 | 26 | 5343.732 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.147` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
