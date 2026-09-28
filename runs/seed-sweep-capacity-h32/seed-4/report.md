# AutoResearch Lite 实验报告

- 任务：capacity check, hidden [32]: do the Adam / AdEMAMix / schedule-free conclusions survive a wider model?
- 论文：Cross-paper capacity check (Adam 2014, AdEMAMix 2024, Schedule-Free 2024)
- 论文标识：internal-capacity-check
- 假设：Every earlier conclusion was measured on an 8-unit hidden layer. With 32 units and every arm retuned for that model, do the same directions hold - Adam mid-pack on speed, AdEMAMix without an advantage, schedule-free losing to a tuned cosine - and does the final loss beat the speed metric as a quality signal?
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`a53ba5f98fa32272e62dfcd07da7ea0f9ce61eb943ce39229e63b3e19c0413b3`

## 最优方案

`adamw_cosine`：主指标 `test_loss` = **0.080923**，测试准确率 **97.00%**，测试损失 `0.08092261`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| adamw_cosine | 97.00% | 0.08092261 | 200 | 15 | 11225.3 |
| ademamix | 97.50% | 0.08161851 | 200 | 15 | 10642.852 |
| adamw_constant | 97.50% | 0.08164428 | 200 | 15 | 8845.012 |
| adam | 97.50% | 0.08164428 | 200 | 15 | 7692.468 |
| adagrad | 98.00% | 0.08323162 | 200 | 13 | 7563.414 |
| schedule_free_adamw | 95.50% | 0.08352051 | 200 | 4 | 10944.805 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.147` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
