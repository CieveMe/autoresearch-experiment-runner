"""Where experiment data comes from.

The harness is offline by design, so only two sources exist: the deterministic synthetic
task used by the existing experiments, and a local CSV/JSON file. Anything that looks
like a URL is refused before it is opened — a reproducible experiment cannot depend on a
download that may return different bytes tomorrow.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

from .dataset import Point, make_dataset, split_dataset

REMOTE_PREFIXES = ("http://", "https://", "ftp://", "s3://", "gs://")


def _refuse_remote(path: str) -> None:
    if path.lower().startswith(REMOTE_PREFIXES):
        raise ValueError(
            f"remote datasets are not supported: {path!r}. Download the file yourself, verify its "
            "hash, and point the config at the local copy so the experiment stays reproducible."
        )


def load_rows(config: Dict[str, Any]) -> List[Point]:
    """Return the full dataset for a config (synthetic by default)."""
    source = str(config.get("source", "synthetic")).lower()
    if source == "synthetic":
        return make_dataset(
            size=int(config.get("size", 800)),
            seed=int(config.get("seed", 7)),
            noise=float(config.get("noise", 0.18)),
        )
    if source not in {"csv", "json"}:
        raise ValueError(f"unsupported dataset source: {source!r}")
    path_text = str(config.get("path", ""))
    if not path_text:
        raise ValueError(f"dataset source {source!r} requires a 'path'")
    _refuse_remote(path_text)
    path = Path(path_text)
    if not path.exists():
        raise ValueError(f"dataset file not found: {path}")
    if source == "json":
        rows = json.loads(path.read_text(encoding="utf-8"))
        return [([float(value) for value in row["features"]], int(row["label"])) for row in rows]
    points: List[Point] = []
    with path.open(newline="", encoding="utf-8") as handle:
        for raw in csv.DictReader(handle):
            features = [float(raw[key]) for key in sorted(key for key in raw if key.startswith("x"))]
            points.append((features, int(raw["label"])))
    return points


def train_test_split(rows: List[Point], config: Dict[str, Any]) -> Tuple[List[Point], List[Point]]:
    return split_dataset(rows, float(config.get("test_ratio", 0.25)))
