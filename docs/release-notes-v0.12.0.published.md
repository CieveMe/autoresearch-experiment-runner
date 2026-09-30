> **Status at the time of writing (2026-09-30): prepared, not yet tagged.** This is the body that will be
> published **verbatim** with the `v0.12.0` tag. Hard rule 1 asks for the body to be in the repository
> before the release is published, so it is written and committed ahead of the tag on purpose. The version
> fields in this tree (`pyproject.toml`, `autoresearch/__init__.py`, `CITATION.cff`) now read `0.12.0`, and
> the README lists v0.12.0 as "归档中" because no version DOI exists until Zenodo archives the tag. Two
> consequences, both written down rather than assumed:
>
> 1. **The provenance paragraph below is date-dependent.** It names the commit this body was written
>    against and the diff between that commit and the `v0.11.0` tag. Re-run the two commands in the queue's
>    top section (`docs/release-corrections-pending.md`) before tagging; if those numbers moved, the body
>    is corrected **before** the tag, never after it.
> 2. **This file is not evidence that the version exists.** Its name asserts a release, and while no tag
>    exists the text has to carry this note; `tests/test_release_docs.py` enforces exactly that, in one
>    direction only, so publishing never requires editing the body afterwards.

This version carries **no correction to a published statement**, and it says so first because that is the
fact a reader needs in order to judge it. Everything below was already true in the tree; what was owed was
the statement itself. The three footnotes and the one extension have the same subject, which is why they
travel together: **a number is only as good as the record of what produced it.** The version also names the
two metadata commits that v0.11.0's body described without naming.

### 1. Where a number comes from — three footnotes, deliberately without case numbers

**A negative claim is a query, not a fact.** While checking a reference, a search returned nothing and what
got written down was "no registry has it". The direct lookup had the record: OpenAlex resolves
`10.2307/4615733` to Holm (1979), *A Simple Sequentially Rejective Multiple Test Procedure*,
**Scandinavian Journal of Statistics 6:65–70** — while Crossref genuinely has no record of that DOI (404)
and that journal's whole 1979 volume has zero deposits. The observation was true and the inference was not.
The rule now in `docs/defect-family.md`: **a negative claim is written as "I ran this query and it returned
this", never as "it does not exist"** — because the second form cannot be reproduced and turns a limitation
of the query into a fact about the world.

**Which copy is in play.** Three failures of one shape turned up in a single afternoon, all of them about
*which artefact was being read* rather than about the experiment: a count typed into a prose summary while
the generator said otherwise; a script edited in its source tree while a scheduled task ran a deployed
copy; a handoff file written to disk while a different block reached the other side. The shared repair is
the family's own rule — **make the copy that can be in play say so itself**: quote the generator, hash-check
the deployed copy, name the file on the first line of the handoff. In this repository that has a fourth
member, which is the one case 6b was about.

**A number carries its unit and its convention.** The same revision of one file was reported to two
sessions as `4,315` and as `7,233`. Both were correct: one counted characters, the other bytes. The residue
after that was a single character (`4,314` — the same blob without its final newline), and the line count
carries the same ambiguity (99 elements when the blob is split on newlines, 98 lines of text). Nothing about
the file was ever in dispute, and two messages were spent settling a missing convention. So
`docs/release-checklist.md`'s hard rule 4 now reads **generator, definition, unit, test**: a size without
its unit is the same defect as a number without its generator, and it is settled the same way, by naming
the instrument.

### 2. Case 6b, extended: the copy is now audited from four places

Case 6b is "a copy that is not the repository". The guard applied to the scored copy now compares it against
four different references, each answering a question the others cannot:

* **git's tracked and ignored sets** — every published file the policy keeps must be present, and no file
  git ignores may be present. This found `runs/ablation-verified/` on its first run: four files that were
  in every copy and had never been committed.
* **the intent list** (`INTENTIONAL_DROPS` in `tests/test_harness.py`) — the policy may leave tracked files
  out only if what it leaves out is a subset of a short list that a person can read and justify:
  `.github/`, `runs/task-runs/`, `runs/threshold-curves/`. Writing that list down found two of the three
  families were leaving every copy **by side effect of the `runs/` rule** rather than by decision — 73
  tracked files, one of them the committed `*-curves.svg` family that the copy filter's own comment used to
  cite as an example of something the filter must not drop. The decision is now written where the filter
  cannot compute it.
* **the published `runs/` files the test sources name** (derived, not listed) — this is the only reference
  that can see a *new* name: a test that starts reading a file inside a family the policy drops on purpose.
* **four pinned names**, kept written out because two of them are read behind `skipTest` guards
  (`tests/test_figures.py` and `VerifyTests` in `tests/test_harness.py`): when such a file is missing, the
  suite inside the copy reports a **skip**, not a failure — and a skip is not a report.

Two things belong to this section rather than beside it. The **mirror member** of 6b: the copy filter kept
the committed analysis inputs by *prefix*, which also carried gitignored scratch such as
`runs/paired-tests-raw.txt` into every scored tree — a copy containing something the repository never
published. It was introduced by 6b's own fix and caught by the privacy-hygiene guard added later, and it is
filed inside case 6b because it is this repository's code rather than a process note. And the **copy filter
no longer copies tool caches**: a `.pytest_cache` held open by a concurrently running tool made `copytree`
raise `WinError 5`, which turned a green suite intermittently red until the gate log caught it with a
traceback. Both directions of isomorphism now have their own assertion, because one assertion and one
assumption is how the first half of this section started.

### 3. Also carried in this version

* **The two metadata commits, now named.** `0497634` moved the version fields off the stale `0.2.0`
  (`pyproject.toml`, `autoresearch/__init__.py`, `CITATION.cff`, and the README's citation line), and
  `74ca558` deleted the duplicated version numbers instead of refreshing them (`.zenodo.json`,
  `docs/release-checklist.md`). v0.11.0's body described this change and named neither commit; they are
  named here because a change a reader has to find in a diff is a change that did not get reported.
* **A gate run now leaves a log.** `make test-log` runs the suite through `scripts/test_log.py`, which
  writes `runs/test-last.log` with a header naming the command, the runner, the start time, the platform
  and the interpreter, and a test pins that header. This exists because a suite run was once made and
  committed in the same command, the output was never kept, and the one red run of that afternoon left
  nothing behind to diagnose. The log then paid for itself on first use by reproducing the cause.
* **The CI split is verified end to end, on a tag.** The `thresholds` job takes the `repro` job's artifacts
  through `needs:`, and that dependency was exercised by CI rather than by argument: on the v0.11.0 tag run
  it started only after the reproduction artifact landed and finished in **nine seconds**. The scorer job
  in the same run took **1 h 06 m 55 s** of a **1 h 06 m 59 s** wall clock — 99.9% — which is the measured
  form of the statement the split was built around.

### Full-tier verification for this release

```
$ python scripts/score_task.py --tier full
submission score: 100.0/100 (tier=full (all suites)) (474/474 checks, exit 0)
control[no-bias-correction]: detected (score 74.9/100, exit 1)
control[no-adaptive-scaling]: detected (score 77.0/100, exit 1)
control[ademamix-without-slow-ema]: detected (score 94.9/100, exit 1)
control[schedule-free-without-averaging]: detected (score 92.8/100, exit 1)

TASK RESULT: PASS
```

**Provenance, stated plainly.** A release body is committed before its tag exists, which is what hard
rule 1 requires, so this body quotes the most complete record that exists at the time of writing: the CI
run **on the v0.11.0 tag** (`36539858168`, `refs/tags/v0.11.0`, commit `d72633f`, six jobs, run-level
success — a tag run cannot be cancelled by the concurrency rule), recorded verbatim in
`runs/task-runs/FULL-TIER-v0.11.0-tag.md`. Between that commit and the commit this body is written
against, **16 files differ** — tests, documentation, the gate-log script, the scorer's copy filter, and one
newly tracked archive under `runs/` — and `git diff --name-only v0.11.0..<commit> -- expected/` is **empty**,
so no pinned number and no tolerance moved. This release's own tag run is produced by CI after the tag;
this body is not edited afterwards.

### Known limitations

Mechanism-level reproduction throughout; no number from any paper's table is claimed. One dataset family,
full-batch gradients, ten seeds, and §5.16 mostly *bounds* what ten seeds can see (the minimal detectable
effect is ≈ 0.99 σ_d). One arm's final loss is pinned only to ≈1e-3 because that is what it reproduces to
across platforms (§5.17). The copy guard's derived read list is taken from literals in the test sources, so
it is a lower bound on what the suite reads rather than a proof: a path assembled at runtime would not
appear in it, and the behavioural check — the suite running green inside the copy — remains the check that
covers those. The six scope axes are frozen; further axes only on a reviewer's request. The version
fields the checklist names — `pyproject.toml`, `autoresearch/__init__.py`, `CITATION.cff` and the README's
citation line — are checked by hand against the tag being created, because no test reads them, which is
exactly why the checklist spells the check out.

Archived on Zenodo; the concept DOI is 10.5281/zenodo.23003610 and each version has its own version DOI.
