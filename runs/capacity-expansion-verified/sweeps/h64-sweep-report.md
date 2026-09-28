# AutoResearch Lite 实验报告

- 任务：capacity expansion, hidden [64]: tuning sweep (pre-registered in docs/capacity-expansion-preregistration.md)
- 论文：Cross-paper capacity expansion (Adam 2014, AdEMAMix 2024, Schedule-Free 2024)
- 论文标识：internal-capacity-expansion
- 假设：H1: AdaGrad keeps strengthening. H2: the schedule-free architecture effect continues. H3: AdEMAMix still has no advantage. Tuning must be redone for this capacity; the rule is unchanged.
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`69e7e0fe5b6122280a7d626c64db6a0d2ffd515ced3599043a30bac322426a6a`

## 最优方案

`schedule_free_adamw_lr0.03`：主指标 `test_loss` = **0.122422**，测试准确率 **93.50%**，测试损失 `0.12242197`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| schedule_free_adamw_lr0.03 | 93.50% | 0.12242197 | 200 | 未达标 | 20634.749 |
| adamw_cosine_lr0.03 | 93.50% | 0.12250315 | 200 | 未达标 | 20312.927 |
| adagrad_lr0.1 | 93.50% | 0.12250428 | 200 | 未达标 | 19829.255 |
| adamw_constant_lr0.03 | 93.50% | 0.12254424 | 200 | 未达标 | 20360.631 |
| adam_lr0.03 | 93.50% | 0.12254424 | 200 | 未达标 | 19349.676 |
| ademamix_lr0.03 | 93.50% | 0.12257457 | 200 | 未达标 | 20149.065 |
| adagrad_lr0.3 | 93.50% | 0.12268389 | 200 | 未达标 | 19938.835 |
| schedule_free_adamw_lr0.1 | 93.50% | 0.12282786 | 200 | 未达标 | 21536.057 |
| schedule_free_adamw_lr0.3 | 93.50% | 0.12391022 | 200 | 未达标 | 16408.602 |
| adamw_cosine_lr0.1 | 93.50% | 0.12481536 | 200 | 未达标 | 19447.151 |
| adamw_constant_lr0.1 | 93.50% | 0.12510317 | 200 | 未达标 | 19678.458 |
| adam_lr0.1 | 93.50% | 0.12510317 | 200 | 未达标 | 19394.035 |
| ademamix_lr0.1 | 93.50% | 0.12536205 | 200 | 未达标 | 20012.07 |
| adamw_cosine_lr0.3 | 93.00% | 0.12726768 | 200 | 未达标 | 20091.617 |
| ademamix_lr0.3 | 92.50% | 0.12832685 | 200 | 未达标 | 20044.237 |
| adamw_constant_lr0.3 | 92.50% | 0.12845077 | 200 | 未达标 | 20869.606 |
| adam_lr0.3 | 92.50% | 0.12845077 | 200 | 未达标 | 20196.209 |
| adagrad_lr1.0 | 92.50% | 0.16870662 | 200 | 未达标 | 20336.67 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。
