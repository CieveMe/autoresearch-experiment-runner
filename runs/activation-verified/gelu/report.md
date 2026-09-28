# AutoResearch Lite 实验报告

- 任务：activation expansion, hidden [32] with GELU: the four claim families
- 论文：Activation expansion (Adam 2014, AdEMAMix 2024, Schedule-Free 2024)
- 论文标识：internal-activation-expansion
- 假设：Same pre-registered A1-A3 as the ReLU run, with GELU instead of tanh: the schedule-free architecture effect, AdEMAMix's no-advantage verdict and the metric trap should survive the change of activation.
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`d5e45d7d66df60263aae5d5132c7aa54a93ad15f4e90ac89823521cef90ca965`

## 最优方案

`adagrad`：主指标 `test_loss` = **0.122565**，测试准确率 **93.50%**，测试损失 `0.12256457`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| adagrad | 93.50% | 0.12256457 | 200 | 33 | 10233.145 |
| schedule_free_adamw | 93.50% | 0.12273812 | 200 | 49 | 10373.409 |
| adamw_constant | 93.50% | 0.12305048 | 200 | 25 | 10484.745 |
| adam | 93.50% | 0.12305048 | 200 | 25 | 10398.279 |
| ademamix | 93.50% | 0.12317559 | 200 | 25 | 10478.372 |
| adamw_cosine | 93.50% | 0.12437396 | 200 | 8 | 10285.578 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。

达标轮数 = 训练损失首次小于或等于 `0.147` 的轮次；「未达标」表示在给定轮数预算内没有达到该阈值。
