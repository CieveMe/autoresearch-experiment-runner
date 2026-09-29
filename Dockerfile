FROM python:3.12-slim

WORKDIR /app
# The image runs the repository's own suite (`scripts/repro.py` ends with `unittest discover`), so it
# must carry every file that suite reads. `runs/` is supplied at run time by compose; everything else is
# copied here, and `tests/test_harness.py::test_the_container_image_contains_everything_the_suite_reads`
# derives the required list from the test sources so a new file cannot be forgotten silently.
COPY autoresearch ./autoresearch
COPY examples ./examples
COPY expected ./expected
COPY tests ./tests
COPY scripts ./scripts
COPY README.md TODO.md pyproject.toml ./
# The build recipe is copied in as well, so the image can say which recipe produced it — and so the check
# that the image carries what the suite reads can run *inside* the image instead of being skipped there.
COPY Dockerfile ./Dockerfile

ENV PYTHONPATH=/app
CMD ["python", "scripts/repro.py"]
