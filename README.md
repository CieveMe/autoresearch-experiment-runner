# AutoResearch Lite MVP

> GitHub repository: `https://github.com/CieveMe/autoresearch-experiment-runner`  
> 当前版本定位：论文复现与工程能力作品集 MVP。

一个离线、可复现的“论文想法 → 实验任务 → 多方案运行 → 指标评估 → 自动选优 → 报告生成”最小闭环。

这个 MVP 用纯 Python 实现一个可替换的二分类训练器，并以 Adam 论文为例完成优化器机制复现；后续只需替换 `autoresearch/model.py`，即可接入其他论文代码、PyTorch 模型或 LLM 评测任务。

## 工程能力

- JSON 实验配置：记录假设、数据规模、随机种子、基线和对照方案。
- 可复现实验：固定随机种子、配置 SHA-256、结构化 `results.json`。
- 自动评估：比较测试准确率、测试损失、训练轮数和耗时，自动生成 Markdown 报告。
- 论文复现：以 Adam 为例，将论文中的矩估计和偏差修正映射为可运行实现，并与 SGD baseline 做对照。
- 环境可迁移：标准库实现，支持 Python 3.10+，提供 Dockerfile 和 Linux Shell 入口。
- 可验证：包含配置校验、确定性运行和结果产物测试。

## 快速运行

```bash
python -m autoresearch.cli validate-config --config examples/classification.json
python -m autoresearch.cli run --config examples/classification.json --output runs/demo
cat runs/demo/report.md
python -m unittest discover -s tests -v
```

Windows PowerShell 可将 `cat` 换成 `Get-Content`。

Windows 也可以直接运行 `scripts/run_demo.ps1`。

## Docker

```bash
docker build -t autoresearch-lite .
docker run --rm -v "$PWD/runs:/app/runs" autoresearch-lite
```

## 论文复现流程

当前示例完整走通：论文元信息 → 研究假设 → baseline → 论文方法实现 → 固定数据和随机种子 → 指标对比 → 复现边界说明。具体记录见 `docs/papers/adam-2014.md`。

## 下一步接入真实论文

1. 将论文的研究问题写成 `hypothesis`，把评测指标写入 `metric`。
2. 在 `model.py` 实现论文方法的训练或推理适配器。
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

- 工程过程与设计取舍：`docs/process/initial-design.md`、`docs/engineering-plan.md`
- 复现边界与可复现性约束：`docs/reproducibility.md`
- 论文复现记录：`docs/papers/adam-2014.md`、`docs/papers/adam-2014-result.md`
- 阶段记录与后续计划：`MILESTONES.md`、`TODO.md`

## 局限

当前示例是二分类任务上的标准库实现，用于演示"论文 → 实验任务 → 评估 → 报告"的闭环，**不构成对 Adam 原论文的完整复现**（数据规模、硬件与原始实验设置不同）。复现边界与差异说明见 `docs/reproducibility.md`。

## License

MIT，见 `LICENSE`。
