# AutoResearch Lite 实验报告

- 任务：capacity check, hidden [32]: do the Adam / AdEMAMix / schedule-free conclusions survive a wider model?
- 论文：Cross-paper capacity check (Adam 2014, AdEMAMix 2024, Schedule-Free 2024)
- 论文标识：internal-capacity-check
- 假设：Every earlier conclusion was measured on an 8-unit hidden layer. With 32 units and every arm retuned for that model, do the same directions hold - Adam mid-pack on speed, AdEMAMix without an advantage, schedule-free losing to a tuned cosine - and does the final loss beat the speed metric as a quality signal?
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`6eb6078786c34cdab16705d86497ab8e5a4cf95c6bed6cef8479cd46aa5ff09c`

## 最优方案

`adagrad`：主指标 `test_loss` = **0.121874**，测试准确率 **95.00%**，测试损失 `0.12187405`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| adagrad | 95.00% | 0.12187405 | 200 | 13 | 7845.617 |
| adamw_cosine | 95.00% | 0.12541635 | 200 | 4 | 7923.86 |
| schedule_free_adamw | 95.00% | 0.12716805 | 200 | 4 | 8321.604 |
| ademamix | 96.00% | 0.12879786 | 200 | 4 | 8149.289 |
| adamw_constant | 96.00% | 0.1290106 | 200 | 4 | 7996.552 |
| adam | 96.00% | 0.1290106 | 200 | 4 | 7814.446 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.147` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
