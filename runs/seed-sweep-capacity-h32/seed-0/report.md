# AutoResearch Lite 实验报告

- 任务：capacity check, hidden [32]: do the Adam / AdEMAMix / schedule-free conclusions survive a wider model?
- 论文：Cross-paper capacity check (Adam 2014, AdEMAMix 2024, Schedule-Free 2024)
- 论文标识：internal-capacity-check
- 假设：Every earlier conclusion was measured on an 8-unit hidden layer. With 32 units and every arm retuned for that model, do the same directions hold - Adam mid-pack on speed, AdEMAMix without an advantage, schedule-free losing to a tuned cosine - and does the final loss beat the speed metric as a quality signal?
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`d972058d147a0273c1647e385e5bd5f939d6ae585f5282f33d4213314e9ded7e`

## 最优方案

`adagrad`：主指标 `test_loss` = **0.105206**，测试准确率 **95.50%**，测试损失 `0.10520563`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| adagrad | 95.50% | 0.10520563 | 200 | 11 | 7719.336 |
| schedule_free_adamw | 95.50% | 0.11454946 | 200 | 3 | 7874.854 |
| adamw_cosine | 93.00% | 0.13583484 | 200 | 3 | 7486.08 |
| adamw_constant | 92.50% | 0.16447161 | 200 | 3 | 8104.036 |
| adam | 92.50% | 0.16447161 | 200 | 3 | 7665.197 |
| ademamix | 92.50% | 0.16689536 | 200 | 3 | 8006.869 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.147` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
