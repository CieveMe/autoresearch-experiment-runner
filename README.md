# AutoResearch Lite MVP

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23003610.svg)](https://doi.org/10.5281/zenodo.23003610)

> GitHub repository: `https://github.com/CieveMe/autoresearch-experiment-runner`  
> 已归档到 Zenodo：v0.2.0 → <https://doi.org/10.5281/zenodo.23003626>（全版本概念 DOI：`10.5281/zenodo.23003610`，v0.1.0 → `10.5281/zenodo.23003611`）  
> 当前版本定位：论文复现与工程能力作品集 MVP。

一个离线、可复现的“论文想法 → 实验任务 → 多方案运行 → 指标评估 → 自动选优 → 报告生成”最小闭环。

这个 MVP 用纯 Python 实现**可替换的训练器**，并以 Adam 论文为例完成优化器机制复现。接入新论文时改的是
`autoresearch/trainers/`（现有 `logistic` 与 `mlp` 两个实现）与 `autoresearch/optimizers.py`（更新规则集中在一处），
`autoresearch/model.py` 只是保持旧导入路径可用的兼容层。实验配置、期望数值与判据都可复用。

## 工程能力

- JSON 实验配置：记录假设、数据规模、随机种子、基线和对照方案。
- 可复现实验：固定随机种子、配置 SHA-256、结构化 `results.json`。
- 自动评估：比较测试准确率、测试损失、训练轮数和耗时，自动生成 Markdown 报告。
- 论文复现：以 Adam 为例，将论文中的矩估计和偏差修正映射为可运行实现，并与 SGD baseline 做对照。
- 环境可迁移：标准库实现，支持 Python 3.10+，提供 Dockerfile 和 Linux Shell 入口。
- 可验证：一条命令跑完"校验配置 → 运行实验 → 对照期望数值（17 项断言，含容差）→ 单元测试"，数值不符即非 0 退出，可直接当 CI 门禁。
- 结论可统计：同一配置跨 10 个种子重跑并做配对比较（不靠单次运行下结论）。
- 判据可证伪：`scripts/score_task.py` 会把实现改坏后的提交判为失败（负向控制必须被识别）。

## 快速运行

```bash
python -m autoresearch.cli validate-config --config examples/classification.json
python -m autoresearch.cli run --config examples/classification.json --output runs/demo
cat runs/demo/report.md
python -m unittest discover -s tests -v
```

Windows PowerShell 可将 `cat` 换成 `Get-Content`。

Windows 也可以直接运行 `scripts/run_demo.ps1`。

## 一键复现与验证（推荐入口）

```bash
python scripts/repro.py        # 任意平台：环境报告 → 校验配置 → 运行 → 对照期望数值 → 单测
make repro                     # Linux/macOS 等价入口
docker compose up --build      # 容器内跑同一套流程，产物写到 ./runs
```

`scripts/repro.py` 的第三步会用 `expected/expected_metrics.json` 逐项断言 17 个数值（各方案的测试损失、准确率、训练轮数、配置 SHA-256），
容差写在同一个文件里；`duration_ms` 不参与比对，因为它本来就不可复现。任何一步失败都会以非 0 退出码结束。

想验证"结论是否可重复"（而不只是"这一次能不能跑"）：

```bash
python scripts/seed_sweep.py --seeds 0-9      # 10 个种子 + 配对提升，输出 summary.json / summary.md
python scripts/score_task.py                  # 任务评分（0-100 部分得分）+ 两个负向控制
```

已提交的验证产物在 `runs/demo-verified/`，由单元测试反向断言：如果重新生成得到的数值变了，测试会失败。
数值来源、与论文的差异、以及"哪些结论不成立"的完整说明见 [`REPRODUCTION.md`](REPRODUCTION.md)；
把复现转成"可反复尝试、可评分"的实验任务的规范见 [`TASK.md`](TASK.md)（中文版 [`TASK.zh.md`](TASK.zh.md)）。

### 三个实验，三个不同的问题

| 实验 | 问题 | 10 个种子的结果 |
|---|---|---|
| `examples/classification.json` | 固定 80 轮时，谁的测试损失更低 | Adam 最低（10/10 种子），配对提升 0.07670 ± 0.00554 |
| `examples/optimizers.json` | 达到接近收敛下限的目标损失，谁用的轮数更少 | **AdaGrad 最快**：平均 **4.7 轮**（10/10 种子），带动量 SGD 16.7 轮，**Adam 22.6 轮**，RMSProp 42.0 轮，朴素 SGD **从未达标** |
| `examples/ademamix.json` | **2024 年论文 AdEMAMix** 是否比 AdamW 更快达标 | **没有更快**：AdEMAMix 与 AdamW **同为 23 轮**（10/10 种子逐种子相同，配对差 0.0），最终测试损失仅好 0.4%；按论文自己的 warmup 缩放到 120 轮预算则慢 4.5 倍（105 轮）。实现正确性检查：把慢 EMA 关掉（α=0）会精确回到 AdamW |
| `examples/optimizers-mlp.json` | 换成**两层 MLP** 后，"Adam 速度居中"是否还成立 | **成立**：AdaGrad 6.2 轮、动量 7.0 轮、**Adam 20.3 轮**（10 种子）；Adam 仍拿到最低最终损失。⇒ 之前的结论不是"两参数模型"的产物 |
| `examples/ademamix-mlp.json` | 换模型后，AdEMAMix 的好处是否出现 | **速度仍无优势，论文 warmup 仍然更差**：10 种子平均测试损失 AdamW 0.13218、AdEMAMix（无 warmup）0.13249、warmup=45 0.14269、warmup=120 0.15261 |
| `examples/schedule-free.json` | **2024 论文 Schedule-Free** 是否能打平"调过的 cosine"计划 | **"打平"勉强成立、"超过"不成立**：10 种子平均测试损失 调过 cosine 0.12610 vs Schedule-Free 0.12642（**10/10 种子败**），达标轮数 80 vs 154；而**常数学习率**（0.12448）比两者都好 |

第二个实验给每个优化器家族（SGD / 带动量 SGD / AdaGrad / RMSProp / Adam）都用同一套学习率扫描
（`examples/optimizers-sweep.json`，24 组）选出自己的学习率，避免"用手选学习率比较调参运气"；
还带一个偏差修正消融（关掉后 Adam 反而 10/10 更快达标，快 12.5 ± 4.6 轮）。

**结论是：论文里"Adam 收敛更快"这一条在本设置下不成立。** 仓库把它写在
[`REPRODUCTION.md`](REPRODUCTION.md) 第 5.4 节，而不是只留下好看的那个数字——这也是"论文复现 +
智能体实验任务"真正值得做的部分：任务必须能证伪自己的假设。注意两个实验回答的是**不同问题**
（固定轮数下的损失水平 vs 达到目标的轮数），不能互相替代引用；未测量的部分（学习率网格未饱和、
目标阈值人工选定、仍是全批量凸任务）列在第 7 节。

## Docker

```bash
docker build -t autoresearch-lite .
docker run --rm -v "$PWD/runs:/app/runs" autoresearch-lite
```

## 论文复现流程

当前示例完整走通：论文元信息 → 研究假设 → baseline → 论文方法实现 → 固定数据和随机种子 → 指标对比 → 复现边界说明。具体记录见 `docs/papers/adam-2014.md`。

## 下一步接入真实论文

1. 将论文的研究问题写成 `hypothesis`，把评测指标写入 `metric`。
2. 在 `autoresearch/trainers/` 增加该论文方法的训练器（或在 `optimizers.py` 增加更新规则）。
3. 在 JSON 中增加 baseline、ablation 和超参数变体。
4. 为数据集、评测指标和失败案例补充测试。
5. 把实验报告、配置和结果一起提交，保留配置哈希以支持复盘。

## 这个 MVP 演示了什么

- **论文机制 → 可运行实现**：把 Adam 的一阶/二阶矩估计与偏差修正映射为纯 Python 训练器，并与固定学习率的 SGD baseline 做对照实验。
- **实验可配置**：研究假设、数据规模、随机种子、基线与对照方案统一写在 JSON 里，并记录配置的 SHA-256 指纹以便复盘。
- **自动评估与报告**：多方案训练 → 指标对比与排序 → 结构化 `results.json` + Markdown 报告。
- **可验证**：配置校验、确定性运行、结果产物测试（`python -m unittest discover -s tests -v`）。
- **环境可迁移**：Python 3.10+ 标准库实现，附 `Dockerfile` 与 Linux / Windows 运行脚本，可在离线环境从零构建。

## 参考文档

- 复现报告（英文，含与论文的差异与局限）：`REPRODUCTION.md`
- 实验任务规范（目标、判据、评分、失败模式、重试协议）：`TASK.md`、`TASK.zh.md`
- 工程过程与设计取舍：`docs/process/initial-design.md`、`docs/engineering-plan.md`
- 复现边界与可复现性约束：`docs/reproducibility.md`
- 论文复现记录：`docs/papers/adam-2014.md`、`docs/papers/adam-2014-result.md`
- 阶段记录与后续计划：`MILESTONES.md`、`TODO.md`

## 局限

当前示例是二分类任务上的标准库实现，用于演示"论文 → 实验任务 → 评估 → 报告"的闭环，**不构成对 Adam 原论文的完整复现**（数据规模、硬件与原始实验设置不同）。复现边界与差异说明见 `docs/reproducibility.md`。

## Roadmap — 接入真实论文

当前只用 Adam (2014) 验证了"论文机制 → 可运行实现"这条链路。下一步是把它接到**更近期的论文**上，让复现本身成为可验证、可复用的实验任务：

1. 把论文的研究问题写成 `hypothesis`，把评测指标写入 `metric`。
2. 在 `autoresearch/trainers/` 增加该论文方法的训练器（或在 `optimizers.py` 增加更新规则）。
3. 在 JSON 配置里补齐 baseline、ablation 与超参数变体。
4. 为数据集、评测指标和失败案例补充测试。
5. 把实验报告、配置与结构化结果一起提交，并保留配置哈希以支持复盘。

选择标准：优先能**在同一台机器上离线复现**、且**原始论文给出了可对齐的数字**的工作；不接受无法在两三天内跑出可比结果的选题。

## License

MIT，见 `LICENSE`。
