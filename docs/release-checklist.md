# Release checklist (v0.2.0) and DOI

Everything that can be prepared in the repository is done. The steps below need the repository
owner's accounts, so they are not automated.

> **Hard rule before every release: save the release body in the repository first.**
> Write the exact text you will publish to `docs/release-notes-vX.Y.Z.published.md` and commit it
> *before* creating the release. GitHub's release body is not part of the git history, so once a
> release is edited or deleted the only surviving copy is the one in this repository — we lost one
> already on 2026-09-28 and only had it back because a copy had been kept locally. The `published`
> suffix marks "what was actually posted" as distinct from `docs/release-notes-vX.Y.Z.md`
> ("what we prepared").

> **Sequencing note (2026-09-28).** Tag `v0.1.0` already exists on GitHub and points at `0dd90e3`,
> which does **not** contain the convergence-speed experiment, `CHANGELOG.md` or `.zenodo.json`.
> Do not publish a release from that tag expecting the archival to include the negative result: push
> the pending commits and cut **v0.2.0** instead (below). Force-updating a published tag is possible
> but it is the worse habit, and a fresh release is the reliable trigger for the archival.

## 1. Before tagging

```bash
python scripts/repro.py          # both suites: 46 checks, 0 failures, exit 0
python scripts/score_task.py     # 100/100 and both negative controls detected
python -m unittest discover -s tests -v
git status --short               # must be clean
```

Confirm the released metadata is consistent (`pyproject.toml`, `autoresearch/__init__.py`,
`CITATION.cff` all say `0.2.0`, and `.zenodo.json` carries the same description as `CHANGELOG.md`).

Push the two pending commits first (`ed0be38` = convergence-speed experiment, defect fixes and release
metadata; `77512b6` = milestone record):

```bash
git push github main
```

## 2. Tag and push (owner action — needs GitHub credentials)

```bash
git tag -a v0.2.0 -m "AutoResearch Lite v0.2.0: convergence-speed experiment and its negative result"
git push github main
git push github v0.2.0
```

The tag must point at the commit whose CI run is green; check the Actions tab before announcing it.

## 3. Zenodo (owner action — needs the Zenodo account)

1. Sign in to Zenodo with GitHub, open **Settings → GitHub**, and toggle the switch for
   `CieveMe/autoresearch-experiment-runner` to `ON`. Zenodo needs permission to read the repository
   list and to create webhooks; it does not get write access to code.
2. Create the GitHub release for tag `v0.2.0`: "Draft a new release" → pick the tag → paste the body
   from `docs/release-notes-v0.2.0.md` → publish. A **published release** (not a draft) is what
   triggers the archive. The existing `v0.1.0` release can stay exactly as it is.
3. Zenodo archives the release and mints a DOI within a few minutes. The record's metadata comes from
   `.zenodo.json` in the released commit.
4. Copy the DOI and add the badge to `README.md`:

   ```markdown
   [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)
   ```

   Also add the DOI to `CITATION.cff` (`doi:` field, and `date-released` if it changed).

## 4. After the DOI exists

- Re-run `python scripts/repro.py` and commit any regenerated artifact, so the released numbers and the
  committed numbers stay identical.
- If a later release is made, Zenodo mints a new version DOI and keeps the concept DOI stable; cite the
  concept DOI when referring to "the software" and the version DOI for a pinned reproduction.

## What the DOI does **not** claim

A DOI records that this artifact is citable and immutable; it is not peer review and it does not make
the reproduction benchmark-level. `REPRODUCTION.md` states exactly which claims are and are not
supported, and that section must be kept up to date with any new experiment.
