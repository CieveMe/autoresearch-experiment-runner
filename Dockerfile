FROM python:3.12-slim

WORKDIR /app
COPY autoresearch ./autoresearch
COPY examples ./examples
COPY expected ./expected
COPY tests ./tests
COPY scripts ./scripts
COPY README.md pyproject.toml ./

ENV PYTHONPATH=/app
CMD ["python", "scripts/repro.py"]
