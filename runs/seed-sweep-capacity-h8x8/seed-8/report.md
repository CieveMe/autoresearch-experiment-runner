# AutoResearch Lite 实验报告

- 任务：capacity check, hidden [8,8]: does depth change the answers that width did not?
- 论文：Cross-paper capacity check (Adam 2014, AdEMAMix 2024, Schedule-Free 2024)
- 论文标识：internal-capacity-check
- 假设：Same capacity question as the [32] run, for a two-layer [8,8] network: do the directions survive a change of depth as well as width, and does the train-loss ranking continue to diverge from the test-loss ranking as capacity grows?
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`c612a0b8f44aa1864ec08dbfc775c9f6e41eb65ea534e237c57e4f401e56e65c`

## 最优方案

`adagrad`：主指标 `test_loss` = **0.164330**，测试准确率 **93.50%**，测试损失 `0.16433016`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| adagrad | 93.50% | 0.16433016 | 200 | 14 | 5429.784 |
| adamw_cosine | 92.00% | 0.24595399 | 200 | 4 | 5315.036 |
| schedule_free_adamw | 91.50% | 0.25220781 | 200 | 4 | 5595.445 |
| adamw_constant | 92.00% | 0.27989469 | 200 | 4 | 5770.858 |
| adam | 92.00% | 0.27989469 | 200 | 4 | 6124.544 |
| ademamix | 92.00% | 0.28849731 | 200 | 4 | 5439.349 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.147` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
