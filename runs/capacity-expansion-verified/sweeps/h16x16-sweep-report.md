# AutoResearch Lite 实验报告

- 任务：capacity expansion, hidden [16,16]: tuning sweep (pre-registered in docs/capacity-expansion-preregistration.md)
- 论文：Cross-paper capacity expansion (Adam 2014, AdEMAMix 2024, Schedule-Free 2024)
- 论文标识：internal-capacity-expansion
- 假设：Same six pre-registered hypotheses as the [64] run, for a deeper network: H1 AdaGrad keeps strengthening, H2 the schedule-free architecture effect continues, H3 AdEMAMix still has no advantage, H4 train/test divergence grows, H5 the noise-correlation claim holds, H6 Adam is still not the fastest.
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`f386112664e5f67b45bbcbb36e4635d0416954312f04b9aa2e799d3c728e168b`

## 最优方案

`ademamix_lr0.1`：主指标 `test_loss` = **0.115887**，测试准确率 **94.50%**，测试损失 `0.11588701`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| ademamix_lr0.1 | 94.50% | 0.11588701 | 200 | 未达标 | 17802.021 |
| adamw_constant_lr0.1 | 94.00% | 0.11666266 | 200 | 未达标 | 15412.776 |
| adam_lr0.1 | 94.00% | 0.11666266 | 200 | 未达标 | 22737.557 |
| schedule_free_adamw_lr0.3 | 94.00% | 0.11777748 | 200 | 未达标 | 24656.256 |
| adamw_cosine_lr0.1 | 93.50% | 0.11928815 | 200 | 未达标 | 12851.627 |
| adagrad_lr0.1 | 93.50% | 0.12350784 | 200 | 未达标 | 22785.196 |
| schedule_free_adamw_lr0.03 | 93.50% | 0.12599536 | 200 | 未达标 | 17212.337 |
| schedule_free_adamw_lr0.1 | 93.00% | 0.12605526 | 200 | 未达标 | 23729.159 |
| adamw_constant_lr0.03 | 93.50% | 0.12685491 | 200 | 未达标 | 13011.769 |
| adam_lr0.03 | 93.50% | 0.12685491 | 200 | 未达标 | 15600.158 |
| ademamix_lr0.03 | 93.50% | 0.12700116 | 200 | 未达标 | 17646.409 |
| adamw_cosine_lr0.03 | 93.50% | 0.12702205 | 200 | 未达标 | 13053.974 |
| adagrad_lr0.3 | 92.50% | 0.12883614 | 200 | 未达标 | 21685.305 |
| adagrad_lr1.0 | 93.00% | 0.14288459 | 200 | 未达标 | 22079.626 |
| adamw_cosine_lr0.3 | 94.00% | 0.14315398 | 200 | 未达标 | 13303.107 |
| adamw_constant_lr0.3 | 94.00% | 0.17496292 | 200 | 未达标 | 15223.361 |
| adam_lr0.3 | 94.00% | 0.17496292 | 200 | 未达标 | 22662.678 |
| ademamix_lr0.3 | 93.00% | 0.18106628 | 200 | 未达标 | 16931.517 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。
