# Milestones

本文件用于记录真实开发阶段，每个阶段的起止 SHA 一律取自真实 Git 历史。

## 记录规则

每个 milestone 需要说明：

1. 目标与背景
2. 实现要点
3. 对外可观察变化
4. 如何验证
5. 区间说明及起止完整 commit SHA

## 当前状态

当前共 3 个真实阶段：M1 初始工程版本、M2 可验证复现 + 任务契约、M3（进行中）。每个区间的
起止 SHA 都可在 `git log` 中核对；本文件不补造任何提交历史。

### M1 — 初始工程版本与最小实验闭环

- Commit range: `d04d760`..`5e6d226`
- 目标与背景：把"论文复现"从散落的脚本收敛成一个可离线运行的实验闭环：配置驱动、固定种子、
  结构化结果与 Markdown 报告。
- 实现要点：`autoresearch/{dataset,model,runner,cli}.py`（纯标准库）、`examples/classification.json`、
  `tests/test_runner.py`、Dockerfile、Linux/Windows 运行脚本。
- 对外可观察变化：新增 `python -m autoresearch.cli run` 子命令，产出 `results.json` + `report.md`。
- 如何验证：`python -m unittest discover -s tests -v`（1 项测试，覆盖确定性运行与产物存在）。
- 区间说明：`d04d760` 为本仓库起点（此前无提交）；`5e6d226` 追加工程证据清单文档。

### M2 — 可验证复现、多种子结论与智能体任务契约

- Commit range: `5e6d226`..`8f1dcdf`
- 目标与背景：单个种子只能证明"可重复"，证明不了"结论可重复"；而"可验证"必须能
  被机器判定为通过或失败。
- 实现要点：`scripts/repro.py`（一键：环境 → 校验 → 运行 → 对照期望值 → 单测）；
  `expected/expected_metrics.json` + `scripts/verify_results.py`（17 项断言与容差）；
  `scripts/seed_sweep.py`（10 种子配对比较）；`scripts/score_task.py`（0–100 部分得分 + 两个
  负向控制）；`REPRODUCTION.md`、`TASK.md`/`TASK.zh.md`；CI（Python 3.10/3.12 + 容器）；
  单测从 1 项增加到 8 项。
- 对外可观察变化：一条命令即可复跑并断言数值；论文结论从"单次演示"变成"10 种子上 10/10 方向
  一致，配对提升 0.07670 ± 0.00554"；任务验收标准自带负向控制（改坏的实现必须被判失败）。
- 如何验证：`python scripts/repro.py`（17/17，退出码 0）、`python -m unittest discover -s tests`
  （8 项通过）、`python scripts/score_task.py`（提交 100/100，两个控制各 82.4/100 且被识别）。
- 区间说明：起点 `5e6d226` 的复现已能运行但**无法自我验证**（`repro.py`、期望数值文件、多种子
  聚合、负向控制都不存在，且配置哈希在 Windows 检出下会漂移）；终点 `8f1dcdf` 上述检查全部通过。

### M3 — 收敛速度实验（负结果）、真实缺陷修复与 0.1.0 发布元数据

- Commit range: `8f1dcdf`..`ed0be38`
- 目标与背景：M2 只测了"固定轮数下谁的损失更低"，而论文的主张是"更快收敛"。这一阶段把该主张变成
  可检验对象，并且**允许它不成立**。
- 实现要点：`autoresearch/model.py` 增加 SGD+momentum / AdaGrad / RMSProp 与 `bias_correction`
  开关，`train()` 返回逐轮损失曲线；新增 `epochs_to_target` 指标与 `examples/optimizers.json`、
  `examples/optimizers-sweep.json`（24 组学习率扫描）、`expected/expected_optimizers.json`；
  `scripts/repro.py` 改为一次跑两个套件（46 项断言）；`scripts/seed_sweep.py` 支持"未达标 = None"
  的排序与配对统计；`CHANGELOG.md`、`.zenodo.json`、`docs/release-checklist.md`；单测 8 → 17 项。
- 对外可观察变化：报告新增 5.4 节并给出**负结果**——AdaGrad 在 10/10 种子上最先达标（平均 4.7 轮 vs
  Adam 22.6 轮），带动量 SGD 也 10/10 快于 Adam，朴素 SGD 在任何扫描学习率下都未达标；关闭偏差修正
  后 Adam 反而 10/10 更快（快 12.5 ± 4.6 轮）。同时修掉两个真实缺陷：配置哈希的平台相关性，以及
  "越小越好"指标集合存在重复定义导致种子扫描把 RMSProp 误报为逐种子获胜者。
- 如何验证：`python scripts/repro.py`（46/46，退出码 0）、`python -m unittest discover -s tests`
  （17 项通过）、`python scripts/score_task.py`（100/100，两个负向控制各 82.4/100 且被识别）、
  `python scripts/seed_sweep.py --config examples/optimizers.json --seeds 0-9`。
- 区间说明：起点 `8f1dcdf` 时模型只支持 `sgd`/`adam`，没有逐轮曲线、没有达标轮数指标，因此**无法**
  检验"更快收敛"；终点 `ed0be38` 该项可跑、可断言、结论为负且已如实写进报告。该区间内还包含
  文档面向读者的清理与一次合并提交（由并行的求职项目工作流完成，见 `37422be`、`0dd90e3`）。

### M4 —（进行中）

- Start: `ed0be38`
- 内容：稀疏梯度场景（论文声称的优势场景之一）；PyTorch 适配器接入真实论文；
  多目标阈值的"达标轮数 vs 阈值"曲线；配对显著性检验（p 值/置信区间）；
  学习率网格向大值延伸并加密（当前各家族最优都在网格边缘）；
  `TASK.md` 第 9 节三个任务变体（T-ADAM-01B/01C/01D）的首轮实测记录。
- End: 待后续真实提交完成后回填。

## 记录模板（后续阶段）

```text
### M1 - 实验配置与最小运行闭环
- Commit range: <start SHA>.. <end SHA>
- 目标与背景：
- 实现要点：
- 对外变化：
- 验证方式：
- 区间说明：起始提交如何失败，结束提交如何通过。
```

后续阶段应在真实开发完成后按 M1、M2、M3……顺序追加，并保证后一个阶段依赖前一个阶段建立的接口、数据结构或配置。
