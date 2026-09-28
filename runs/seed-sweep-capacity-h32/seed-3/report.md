# AutoResearch Lite 实验报告

- 任务：capacity check, hidden [32]: do the Adam / AdEMAMix / schedule-free conclusions survive a wider model?
- 论文：Cross-paper capacity check (Adam 2014, AdEMAMix 2024, Schedule-Free 2024)
- 论文标识：internal-capacity-check
- 假设：Every earlier conclusion was measured on an 8-unit hidden layer. With 32 units and every arm retuned for that model, do the same directions hold - Adam mid-pack on speed, AdEMAMix without an advantage, schedule-free losing to a tuned cosine - and does the final loss beat the speed metric as a quality signal?
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`a9e3713a1836b0ece4afc59f2d029e23779d3e63d52808daf3cf9c2c71e47c57`

## 最优方案

`adagrad`：主指标 `test_loss` = **0.126910**，测试准确率 **93.50%**，测试损失 `0.12691023`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| adagrad | 93.50% | 0.12691023 | 200 | 30 | 11871.587 |
| schedule_free_adamw | 93.50% | 0.13279064 | 200 | 7 | 8888.436 |
| adamw_cosine | 93.50% | 0.13814493 | 200 | 19 | 13081.558 |
| adamw_constant | 94.00% | 0.14109048 | 200 | 19 | 11868.474 |
| adam | 94.00% | 0.14109048 | 200 | 19 | 12865.602 |
| ademamix | 94.00% | 0.14156872 | 200 | 19 | 9259.201 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.147` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
