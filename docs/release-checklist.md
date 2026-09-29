# Release checklist and DOI

Everything that can be prepared in the repository is done. The steps below need the repository
owner's accounts, so they are not automated.

> **Hard rule before every release: save the release body in the repository first.**
> Write the exact text you will publish to `docs/release-notes-vX.Y.Z.published.md` and commit it
> *before* creating the release. GitHub's release body is not part of the git history, so once a
> release is edited or deleted the only surviving copy is the one in this repository — we lost one
> already on 2026-09-28 and only had it back because a copy had been kept locally. The `published`
> suffix marks "what was actually posted" as distinct from `docs/release-notes-vX.Y.Z.md`
> ("what we prepared").

> **Hard rule 2: a release body must quote a `full`-tier run.** Before publishing, run
> `python scripts/repro.py --tier full` and `python scripts/score_task.py --tier full`, and paste
> their output (the suite count, the assertion count and the four negative controls) into the
> release body. The `core` tier exists only to save local iteration time: it skips the capacity
> suites, it always says so in its own output, and its numbers must never be presented as full
> coverage. CI enforces the same split - pull requests may run `core`, `main` and tags always run
> `full`.

> **Sequencing note (2026-09-28).** Tag `v0.1.0` already exists on GitHub and points at `0dd90e3`,
> which does **not** contain the convergence-speed experiment, `CHANGELOG.md` or `.zenodo.json`.
> Do not publish a release from that tag expecting the archival to include the negative result: push
> the pending commits and cut **v0.2.0** instead (below). Force-updating a published tag is possible
> but it is the worse habit, and a fresh release is the reliable trigger for the archival.

## 1. Before tagging

### Hard rules that outrank the steps below

1. **Save the release body verbatim into the repository before publishing it**
   (`docs/release-notes-vX.Y.Z.published.md`), because a release body deleted or edited on GitHub is
   gone from the git history.
2. **A release body quotes a full-tier run.** `python scripts/score_task.py --tier full`, with the tier
   label visible, so a core-tier number can never be read as full coverage.
   Quote the run **on the tag** when CI produced one — tag runs are never cancelled by the
   `concurrency` rule in `.github/workflows/repro.yml` — or, if the body is written before the tag exists,
   the full-tier run recorded in the repository (`runs/task-runs/`). **A branch run that a later push
   superseded may have been cancelled, and a cancelled run has no verdict, so it may not be quoted.**
3. **A published release body and a pushed tag are never edited.** Corrections go into the next
   version's body and into the section that carries the wrong statement; `docs/release-corrections-pending.md`
   is the queue. Reasons, in order: editing the body does not re-trigger archival, so GitHub and the
   archive would disagree; the archive is the tag's repository snapshot, so text in the tree at that tag
   is archived regardless; and silently repairing a published version destroys the evidence that this
   repository corrects itself in public.
4. **Any statistic a conclusion quotes has a generator, a definition and a test** before it is written
   into a table (`docs/defect-family.md` case 5).
5. **A check may not be deleted or skipped to make CI green, and a tolerance may not be widened without a
   measured basis.** If a pin fails only on another platform, the repair is to measure the spread
   (`scripts/perturbation_probe.py` measures it on one machine; a container run measures it across
   `libm` builds), scope the new tolerance to that one expectation, print it in the verifier's output, and
   state what sensitivity the widening costs. Case 7 in `docs/defect-family.md` is what happens when the
   tolerance is below the quantity's own reproducibility: the check measures which machine ran it.
6. **Keep the output of every gate run.** `make test-log` (or the same command piped into
   `runs/test-last.log`; on Windows, `... | Tee-Object -FilePath runs\test-last.log`) — `runs/` is ignored
   by git, so the log stays local. This is written down because it was learned the hard way: a full suite
   was run and committed **in the same command**, one run reported `errors=1`, and the output was never
   kept; two green runs afterwards then left nothing to diagnose from. "It has not recurred" is not "it did
   not happen", and a red run should leave a scene. One fact worth having when reading those logs:
   **`python -m unittest` calls an exception in a test body an *error* and an assertion failure a
   *failure*** (measured: the same raising test prints `FAILED (errors=1)`), while `pytest` reports both as
   `failed`. Which word you see therefore tells you which runner produced the output — and, in the
   unittest case, that something raised rather than asserted.
7. **Verify the CI's *later* steps too, not just the first one.** A job that fails at step 5 never runs
   steps 6–13, so a repo can be red for weeks with everyone assuming the failure is "the known one".
   Those steps may be **split into parallel jobs** to keep the wall clock down — they must not be removed,
   and their tier must not be lowered.
   **What that costs, measured on the v0.11.0 tag** (run `36539858168`, 6/6 jobs): the whole run took
   **1 h 06 m 59 s** and the scorer alone took **1 h 06 m 55 s** — 99.9% of it, because it reproduces the
   corpus five times (the submission plus four mutated copies). Everything else finished inside 34 minutes
   and ran in parallel; the threshold-curves job is nine seconds of work and only waits for the
   reproduction artifact. So "the CI takes about an hour" is a statement about the scorer, and any future
   attempt to shorten it has to argue about that job specifically rather than about the workflow.

```bash
python scripts/repro.py --tier full   # every suite, 0 failures, exit 0
python scripts/score_task.py --tier full   # 100/100 and every negative control detected
python -m unittest discover -s tests -v
git status --short               # must be clean
```

Confirm the released metadata is consistent: `pyproject.toml`, `autoresearch/__init__.py` and
`CITATION.cff` all carry **the version you are about to tag** (they are the fields a reader sees when
deciding what to cite — check them every time, because nothing in the test suite reads them), and
`.zenodo.json`'s description still matches `CHANGELOG.md`.

Push the two pending commits first (`ed0be38` = convergence-speed experiment, defect fixes and release
metadata; `77512b6` = milestone record):

```bash
git push github main
```

## 2. Tag and push (owner action — needs GitHub credentials)

```bash
git tag -a vX.Y.Z -m "AutoResearch Lite vX.Y.Z: <one line about what this version adds>"
git push github main
git push github vX.Y.Z
```

The tag must point at the commit whose CI run is green; check the Actions tab before announcing it.

### Publishing the release — and what the current script guarantees

The release is published by a script rather than by hand
(`scripts/papers/publish_github_release.py`, which lives in this project's automation and not in this
repository — so what is written here is the **contract**, and the script is one implementation of it):

1. resolve `git/ref/tags/<tag>` and dereference an annotated tag to its commit;
2. read `docs/release-notes-<tag>.published.md` **from that commit** (not from the working tree, not from
   the default branch);
3. create the release with exactly that text, taking the title from the commit subject.

**What that enforces mechanically: hard rule 1.** If the body is not in the repository at the tagged
commit, step 2 fails and no release is created — so "save the body before publishing it" stops being a
thing somebody has to remember. It also cannot create a second release for the same tag (GitHub rejects
the duplicate), and it prints `notes_chars` and `body_chars` from the two sides so the published body can
be compared against the file in one glance.

**What it does not enforce, and still needs a human:**

* **hard rule 2** — that the body quotes a full-tier run. The script copies text; it does not read it.
* **hard rule 3** — that a published body is never edited afterwards. The script never edits, but nothing
  stops an edit in the web UI; that is why the body is read from the *tag* and why the correction goes
  into the next version.
* One more consequence worth knowing: because publishing needs only the tag and the file, the release can
  be published before the tag's CI has finished. Quote the tag's run once it is green, and for a `full`
  claim (rule 2) quote a run that has a verdict — a cancelled or still-running one has none.

## 3. Zenodo (owner action — needs the Zenodo account)

1. Sign in to Zenodo with GitHub, open **Settings → GitHub**, and toggle the switch for
   `CieveMe/autoresearch-experiment-runner` to `ON`. Zenodo needs permission to read the repository
   list and to create webhooks; it does not get write access to code.
2. Create the GitHub release for the tag you just pushed: "Draft a new release" → pick the tag → paste
   the body from `docs/release-notes-vX.Y.Z.published.md` → publish. A **published release** (not a
   draft) is what triggers the archive; earlier releases are left exactly as they are. Zenodo archives
   the **tag's snapshot**, so the `.zenodo.json` it reads is the one in that commit — which is why a
   later change to the file cannot affect a release that is already queued.
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
