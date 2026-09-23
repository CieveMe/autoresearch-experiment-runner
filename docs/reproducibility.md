# Reproducibility

## 环境

- Python 3.10 或更高版本
- 当前示例只依赖 Python 标准库
- 可选 Docker 环境，详见根目录 `Dockerfile`

## 运行

```bash
python -m autoresearch.cli validate-config --config examples/classification.json
python -m autoresearch.cli run --config examples/classification.json --output runs/demo
python -m unittest discover -s tests -v
```

Windows PowerShell：

```powershell
.\scripts\run_demo.ps1
```

## 可复现约束

- 实验配置显式记录随机种子、数据规模、基线和对照方案。
- 运行器输出配置 SHA-256，便于确认结果对应的配置版本。
- 结果写入结构化 JSON，并生成 Markdown 报告。
- 提交实验结果时，应同时提交使用的配置和报告，不要只保留截图。
