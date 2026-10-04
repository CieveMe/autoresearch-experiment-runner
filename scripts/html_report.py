"""Export an existing per-run results.json to a self-contained offline report."""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import math
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from autoresearch.runner import is_lower_is_better, rank_key


def escape(value: Any) -> str:
    return html.escape(str(value), quote=True)


def number(value: Any) -> str:
    return "—" if value is None else escape(value)


def curves_svg(results: list[dict[str, Any]]) -> str:
    curves = [(item["name"], item.get("loss_curve") or []) for item in results]
    curves = [(name, curve) for name, curve in curves if curve]
    if not curves:
        return "<p>No training curves recorded.</p>"
    values = [float(value) for _, curve in curves for value in curve]
    if not all(math.isfinite(value) for value in values):
        raise ValueError("training curves must contain finite numbers")
    lo, hi = min(values), max(values)
    span = hi - lo or 1.0
    epochs = max(len(curve) for _, curve in curves)
    colors = ("#235789", "#b34a31", "#427d47", "#7a4e9b", "#946b12", "#497e88")
    parts = ['<svg viewBox="0 0 800 330" role="img" aria-label="Training loss by epoch">',
             '<title>Training loss by epoch; each curve ends at its recorded epoch</title>',
             '<path d="M60 20 V280 H780" fill="none" stroke="#777"/>',
             f'<text x="5" y="28">{hi:.4g}</text>',
             f'<text x="5" y="280">{lo:.4g}</text>',
             '<text x="60" y="305">1</text>',
             f'<text x="740" y="305">{epochs}</text>',
             '<text x="350" y="325">Epoch / training loss</text>']
    legend = []
    for index, (name, curve) in enumerate(curves):
        color = colors[index % len(colors)]
        points = " ".join(f"{60 + 720 * i / max(1, epochs - 1):.3f},"
                          f"{280 - 260 * (float(value) - lo) / span:.3f}"
                          for i, value in enumerate(curve))
        parts.append(f'<polyline points="{points}" fill="none" stroke="{color}" '
                     f'stroke-width="2"><title>{escape(name)}</title></polyline>')
        # A one-epoch curve needs a visible point as well as a polyline.
        x, y = points.split()[0].split(",")
        parts.append(f'<circle cx="{x}" cy="{y}" r="3" fill="{color}"/>')
        legend.append(f'<li style="color:{color}">{escape(name)}</li>')
    return "".join(parts) + '</svg><ul class="legend">' + "".join(legend) + "</ul>"


def render(payload: dict[str, Any], source_name: str, source_sha256: str) -> str:
    results = payload["results"]
    if not isinstance(results, list) or not results:
        raise ValueError("results must be a non-empty list")
    metric = payload["metric"]
    lower = is_lower_is_better(metric)
    ranked = sorted(results, key=lambda item: rank_key(item, metric, lower))
    target = payload.get("target_loss")
    rows = []
    for item in ranked:
        reached = ("Not configured" if target is None else
                   "Not reached" if item.get("epochs_to_target") is None else
                   number(item["epochs_to_target"]))
        rows.append("<tr>" + "".join(f"<td>{value}</td>" for value in (
            escape(item["name"]), number(item.get(metric)),
            number(item.get("train_loss")), number(item.get("test_loss")),
            number(item.get("test_accuracy")), number(item.get("epochs")),
            reached, number(item.get("duration_ms")))) + "</tr>")
    metadata = {key: payload.get(key) for key in
                ("task", "trainer", "paper", "hypothesis", "dataset", "config_sha256", "target_loss")}
    configurations = [{"name": item["name"], "config": item.get("config", {})} for item in results]
    return f'''<!doctype html>
<html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>AutoResearch — {escape(payload['task'])}</title>
<style>
body{{margin:0;background:#f5f3ee;color:#252b31;font:16px/1.6 system-ui,sans-serif}}
main{{max-width:1100px;margin:auto;padding:40px 24px}}h1{{line-height:1.2}}
section{{background:white;border:1px solid #d6d4ce;padding:24px;margin:24px 0}}
.scroll{{overflow:auto}}table{{width:100%;border-collapse:collapse;font-variant-numeric:tabular-nums}}
th,td{{padding:10px;text-align:right;border-bottom:1px solid #deded8;white-space:nowrap}}
th:first-child,td:first-child{{text-align:left}}th{{background:#f1f2ee}}
pre{{white-space:pre-wrap;overflow-wrap:anywhere;font-size:13px}}code{{overflow-wrap:anywhere}}
svg{{width:100%;height:auto}}svg text{{font:13px system-ui,sans-serif}}
.legend{{display:flex;flex-wrap:wrap;gap:8px 30px}}.note{{color:#535b60}}
@media print{{body{{background:white}}main{{padding:0}}section{{break-inside:avoid}}}}
</style><main>
<p>AutoResearch Lite · Offline experiment report</p><h1>{escape(payload['task'])}</h1>
<p>{escape(payload.get('hypothesis', ''))}</p>
<section><h2>Run identity and scope</h2>
<p>Source: <code>{escape(source_name)}</code><br>Source SHA-256: <code>{escape(source_sha256)}</code><br>
Configuration SHA-256: <code>{escape(payload.get('config_sha256', 'Not recorded'))}</code></p>
<p>Ranking metric: <strong>{escape(metric)}</strong> ({'lower' if lower else 'higher'} is better).
Recorded best arm: <strong>{escape(payload['best']['name'])}</strong>.</p>
<p class="note">This is one recorded run, not a multi-seed significance test. Table order uses the
runner's test-loss tie-breaker; ties do not establish superiority. Export does not verify expected
values. Duration is observed wall time, not a deterministic performance guarantee.</p>
<details><summary>Experiment metadata</summary><pre>{escape(json.dumps(metadata, ensure_ascii=False, indent=2))}</pre></details></section>
<section><h2>Trial results</h2><p>Accuracy is a fraction. Target epoch is the first training loss
at or below {number(target) if target is not None else 'the threshold (not configured for this run)'}.</p>
<div class="scroll"><table><thead><tr><th>Trial</th><th>{escape(metric)}</th><th>Train loss</th>
<th>Test loss</th><th>Test accuracy</th><th>Epochs</th><th>Target epoch</th><th>Duration (ms)</th>
</tr></thead><tbody>{''.join(rows)}</tbody></table></div></section>
<section><h2>Training curves</h2>{curves_svg(results)}</section>
<section><details><summary>Trial configurations and seeds</summary>
<pre>{escape(json.dumps(configurations, ensure_ascii=False, indent=2))}</pre></details></section>
</main></html>
'''


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    output = args.output or args.results.with_name("report.html")
    try:
        if output.resolve() == args.results.resolve():
            raise ValueError("output must not overwrite results input")
        source = args.results.read_bytes()
        document = render(json.loads(source), args.results.name, hashlib.sha256(source).hexdigest())
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(document, encoding="utf-8")
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.exit(1, f"HTML export failed: {exc}\n")
    print(f"report={output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
