FROM python:3.12-slim

WORKDIR /app
COPY autoresearch ./autoresearch
COPY examples ./examples
COPY tests ./tests
COPY scripts ./scripts
COPY README.md pyproject.toml ./

ENV PYTHONPATH=/app
CMD ["python", "-m", "autoresearch.cli", "run", "--config", "examples/classification.json", "--output", "runs/demo"]
