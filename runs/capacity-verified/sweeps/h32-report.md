# AutoResearch Lite 实验报告

- 任务：capacity check, hidden [32]: tuning sweep for the three claims
- 论文：Cross-paper capacity check (Adam 2014, AdEMAMix 2024, Schedule-Free 2024)
- 论文标识：internal-capacity-check
- 假设：The conclusions about Adam, AdEMAMix and schedule-free were all measured on an 8-unit hidden layer. Re-tuning every arm for a 32-unit layer and for a two-layer [8,8] net tests whether the ranking is a property of the methods or of the model size.
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`0c271ca25059092e0e4b9c20d9e8c8c3c1dd134235e9d9db89ad601cab4f87b2`

## 最优方案

`schedule_free_adamw_lr0.03`：主指标 `test_loss` = **0.122581**，测试准确率 **93.50%**，测试损失 `0.12258075`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| schedule_free_adamw_lr0.03 | 93.50% | 0.12258075 | 200 | 未达标 | 11263.333 |
| adagrad_lr0.1 | 93.50% | 0.12286263 | 200 | 未达标 | 11969.017 |
| adamw_cosine_lr0.03 | 93.50% | 0.12297071 | 200 | 未达标 | 7492.596 |
| adagrad_lr0.3 | 93.50% | 0.12343128 | 200 | 未达标 | 11638.364 |
| sgd_momentum_lr0.3 | 93.50% | 0.12358416 | 200 | 未达标 | 11263.767 |
| adamw_constant_lr0.03 | 93.50% | 0.12385445 | 200 | 未达标 | 7765.098 |
| adam_lr0.03 | 93.50% | 0.12385445 | 200 | 未达标 | 7607.486 |
| ademamix_lr0.03 | 93.50% | 0.12395296 | 200 | 未达标 | 11650.825 |
| schedule_free_adamw_lr0.1 | 93.50% | 0.12446549 | 200 | 未达标 | 11644.439 |
| schedule_free_adamw_lr0.3 | 93.50% | 0.12452343 | 200 | 未达标 | 11841.205 |
| sgd_momentum_lr0.6 | 93.50% | 0.12486892 | 200 | 未达标 | 13127.882 |
| adamw_cosine_lr0.1 | 93.50% | 0.12554742 | 200 | 未达标 | 7523.265 |
| sgd_momentum_lr1.0 | 93.50% | 0.1259798 | 200 | 未达标 | 9165.535 |
| adamw_constant_lr0.1 | 93.50% | 0.12618672 | 200 | 未达标 | 7819.998 |
| adam_lr0.1 | 93.50% | 0.12618672 | 200 | 未达标 | 7523.378 |
| ademamix_lr0.1 | 93.50% | 0.12650536 | 200 | 未达标 | 11603.442 |
| adamw_constant_lr0.3 | 92.50% | 0.12921253 | 200 | 未达标 | 8018.23 |
| adam_lr0.3 | 92.50% | 0.12921253 | 200 | 未达标 | 10611.469 |
| ademamix_lr0.3 | 92.50% | 0.12931594 | 200 | 未达标 | 11324.749 |
| adamw_cosine_lr0.3 | 93.00% | 0.12962289 | 200 | 未达标 | 7820.475 |
| adagrad_lr1.0 | 92.50% | 0.13108277 | 200 | 未达标 | 12202.465 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。
