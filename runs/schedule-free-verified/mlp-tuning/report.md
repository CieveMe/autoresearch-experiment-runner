# AutoResearch Lite 实验报告

- 任务：tuning sweep for the schedule-free comparison on the MLP trainer
- 论文：Schedule-Free Learning: Replacing Schedules with Iteration-Based Averages
- 论文标识：arXiv:2405.15682
- 假设：The logistic head is almost convex, which is the least favourable place to look for a schedule effect. This repeats the comparison on the two-layer MLP, with the cosine baseline tuned over both its learning rate and its minimum-learning-rate factor, and a constant learning rate included because that is what schedule-free replaces.
- 数据集：训练 600 条，测试 200 条
- 配置 SHA-256：`66c28062d5dbefbc67f3072fd2c757594cca018c128d19c74348887d25e48256`

## 最优方案

`schedule_free_adamw_lr0.03`：主指标 `test_loss` = **0.123931**，测试准确率 **93.50%**，测试损失 `0.12393149`。

## 对比结果

| 方案 | 测试准确率 | 测试损失 | 训练轮数 | 达标轮数 | 耗时(ms) |
|---|---:|---:|---:|---:|---:|
| schedule_free_adamw_lr0.03 | 93.50% | 0.12393149 | 200 | 未达标 | 2318.915 |
| adamw_cosine_lr0.03_min0.1 | 93.50% | 0.12400578 | 200 | 未达标 | 2350.719 |
| adamw_cosine_lr0.03_min0.0 | 93.50% | 0.12403573 | 199 | 未达标 | 2410.346 |
| adamw_constant_lr0.03 | 93.50% | 0.12423331 | 200 | 未达标 | 2337.142 |
| schedule_free_adamw_lr0.1 | 93.50% | 0.12451018 | 200 | 未达标 | 2248.981 |
| adamw_constant_lr0.3 | 93.00% | 0.12501296 | 200 | 未达标 | 2361.881 |
| sgd_cosine_lr1.0_min0.0 | 93.50% | 0.12501563 | 200 | 未达标 | 2293.216 |
| schedule_free_adamw_lr0.3 | 93.50% | 0.12506323 | 200 | 未达标 | 2283.409 |
| schedule_free_sgd_lr1.0 | 93.50% | 0.12530471 | 200 | 未达标 | 2288.798 |
| adamw_cosine_lr0.1_min0.0 | 93.50% | 0.12571879 | 200 | 未达标 | 2269.373 |
| adamw_cosine_lr0.1_min0.1 | 93.50% | 0.12574494 | 200 | 未达标 | 2402.848 |
| adamw_constant_lr0.1 | 93.50% | 0.12641344 | 200 | 未达标 | 2289.578 |
| adamw_cosine_lr0.3_min0.1 | 93.00% | 0.12699107 | 200 | 未达标 | 2305.713 |
| adamw_cosine_lr0.3_min0.0 | 93.00% | 0.12743962 | 200 | 未达标 | 2412.936 |
| schedule_free_sgd_lr0.3 | 93.50% | 0.13413602 | 200 | 未达标 | 2281.571 |
| sgd_cosine_lr0.3_min0.0 | 94.00% | 0.14656701 | 200 | 未达标 | 2249.443 |

## 复现命令

```bash
python scripts/repro.py          # 校验配置 → 运行实验 → 对照期望值 → 跑单测
make repro                       # 同上（Linux/macOS）
```

本报告由 `scripts/verify_results.py` 对照 `expected/expected_metrics.json` 逐项校验；
数值比对详见 `REPRODUCTION.md`。
