# Corrections queued for the next release body

This file is the queue, not the record. A correction is **stated in the release body of the next
version** and simultaneously written into the section that carries the wrong statement; the published
release body itself is never edited, and a pushed tag is never moved.

## Why a published release is left alone

1. **Editing a published release body does not re-trigger archival** — Zenodo archives on
   `release/published`, so an edit changes what a reader sees on GitHub and changes nothing in the
   archived record. The two would then disagree, with the archive being the citable one.
2. **The archive is the tag's snapshot, not the release's text.** Zenodo archives the repository at the
   tag, so text that was already in `REPRODUCTION.md` at that tag is in the archived package whether or
   not the release body is later edited. Fixing the body would not remove it.
3. **Silently editing a published version destroys the only evidence that the repository corrects
   itself in public.** The corrections are the most persuasive part of this repository; the ordering
   rule "wrong text stays where it is, the correction goes forward" is what makes them credible.

The precedent is v0.5.0: its release notes quote a sentence about a threshold crossing that was later
shown to be produced by a tie-break bug. v0.5.0 was not touched; v0.6.0's body opens with the explicit
correction.

## Current status (2026-10-05): v0.12.0 is released; CI checkout repair is pending a new run

The dated deferral below is historical: the user subsequently approved publication and v0.12.0
was released at `aef012b`. Its DOI is `10.5281/zenodo.23055022`, and the README update landed at
`0d2ce81`. Do not re-release or move that tag because the historical deferral text remains here.

The next release body should cite the checkout-history repair and its eventual run verdict:
see `docs/ci-checkout-history.md`. Runs #72/#74 passed all 474 numerical checks but failed a
Git-dependent unit test because their shallow checkouts lacked historical release tags. The fix
supplies full history to the reproduction jobs; it does not change test coverage or tolerances.
Run #75 on `b8d8ff0` is the first repair run. Its final conclusion must be read before describing CI
as green. Old published bodies and tags remain intact.

## Historical deferral: prepared v0.12.0 (decided 2026-09-30, subsequently released)

An inventory of this file found the open items below, and `docs/release-notes-v0.12.0.published.md` — written
and committed on 2026-09-30 — carries every one of them. The decision is to **hold**, not to release:
nothing that has been published is wrong, so nobody is being misled while this waits, and publishing a
release is the owner's action. What makes waiting safe is that none of the items lives only in a
conversation; each is a section of this file or a paragraph of that body.

**Release on a trigger, not on a mood.** Any one of these ends the deferral:

| trigger | what it means in practice |
|---|---|
| **a claim-changing correction** | anything that makes a published statement wrong. This outranks the deferral completely: it is released on its own, with the correction first in the body |
| **the A3 preprint becomes public** | the owner wants the repository to cite it — one added line, the rest of the body unchanged |
| **a reviewer or a third party asks for something on this list** | the queue exists in order to be citable |
| **14 days pass (2026-10-14), or this file gains three more open sections** | whichever comes first. A queue with no deadline grows until it is wrong in several places at once, which is how the 78→79 rot started |

If the deadline passes and the release still waits, the reason is written here rather than remembered.

**Before the tag**, whichever trigger fires, re-run the checks the citation section names:

```bash
git diff --name-only v0.11.0..<commit>              # the list the body must state
git diff --name-only v0.11.0..<commit> -- expected/ # must print nothing
python scripts/test_log.py                          # runs/test-last.log
```

The prepared body names the commit it was written against, so a body that no longer matches the tree is
rewritten **before** the tag, never after it. The body is not edited once the release is published.

## Queue

### Citation checklist for the next release body (three items, none optional)

> **Status 2026-09-29:** all three are stated in `docs/release-notes-v0.11.0.published.md`, and the
> checklist stays here as the record of what was owed and where it was paid.

Written down because the next body has to carry all three and they live in different places; a reader of
the file should not have to reconstruct the list from the sections below.

| # | what the next body must state | where the material is |
|---|---|---|
| ① | **case 5** — §5.11 finding 7 and §5.13's H5 are withdrawn (the hand-assembled σ column), and the second half of §5.15's N4 with them; "no advantage detected" is stated as a bound | item 1 below; `docs/defect-family.md` case 5; §5.16 |
| ② | **case 6a and 6b** — the liveness failure (a 100/100 implementation that had moved the controls' mutation points into dead code) and the copy that was not the repository; including 6b's third copy, the container image that never carried `TODO.md` | `docs/defect-family.md` case 6; `runs/task-runs/README.md`; §5.17's closing passage |
| ③ | **case 7 + the CI change** — the pin whose tolerance was below its own reproducibility (with the measured spread and the basis for 0.005), and the CI work: the parallel jobs and the concurrency rule that cancels superseded branch runs | the CI entry below; §5.17; `runs/task-runs/FULL-TIER-ci-fix.md` |

And per hard rule 2: quote a **full-tier** run, preferably the one CI produced **on the tag** (tag runs are
never cancelled by the concurrency rule), otherwise the run recorded in `runs/task-runs/`.

**The tag's record is now complete, so the next body needs no qualifier.** CI run **36539858168**
(`refs/tags/v0.11.0`, commit `d72633f`, **6/6 jobs, run-level success**) is written out in
`runs/task-runs/FULL-TIER-v0.11.0-tag.md`: three full-tier reproductions — CPython 3.12 twice (once through
`make repro`), CPython 3.10, and the container image — each `474 checks, 0 failures`, plus the scorer's
verbatim `100.0/100 (tier=full (all suites)) (474/474 checks, exit 0)` with all four controls detected.
So the next release body may quote that line **directly**. The sentence "the run recorded in the
repository, not the run on this tag" was true of **v0.11.0's own body only**, because that body had to be
committed before its tag existed; it is not a standing caveat and must not be copied forward.

> **Corrected 2026-09-30: "no qualifier needed" was true for one moment and read as a standing rule.**
> It holds only while `main` equals the tag being quoted. Every *later* body is again written before *its
> own* tag exists (hard rule 1), so it must say which run it quotes — the previous tag's CI run, and/or
> the full-tier run recorded in `runs/task-runs/` — and it must state the diff between that run's commit
> and the commit the body is written against. Two commands decide whether quoting an older run's verdict
> is licensed: `git diff --name-only <tag>..<commit>` (the list the body has to state) and
> `git diff --name-only <tag>..<commit> -- expected/`, which must be **empty**. Measured while writing
> v0.12.0's body: 16 files differ from `v0.11.0` and the `expected/` diff is empty.

> **Status 2026-09-28:** both items below are stated in
> `docs/release-notes-v0.10.0.published.md` and are therefore no longer pending. They stay here as the
> record of what was owed and where it was paid, and the next entry will be added below them.

### 1. §5.13's σ column was not reproducible, and the correlation built on it is withdrawn

* **Where the wrong text is:** `REPRODUCTION.md` §5.13's H5 verdict and its "σ and the number of
  distinct winners move together" paragraph; §5.11 finding 7; the schedule-free paper card's reference
  to that rule. All three are corrected **in place** in the working tree already.
* **Published in:** v0.7.0 (the table and H5) and v0.9.0 (the N4 row that says "confirmed on the
  correlation", and the release body's N4 line).
* **What the next release body must say:** that the σ column was assembled by hand and is not
  reproducible under its own heading (five of ten rows carry a different arm's σ); that with every noise
  statistic recomputed from the committed files the relationship is not monotone
  (`optimizers-mlp` σ_best = 0.02019 with five distinct winners; the two activation suites at
  σ_best ≈ 0.0217 with one each); and that this is **case 5** in `docs/defect-family.md`, whose check is
  `tests/test_figures.py::test_the_noise_statistics_are_reproducible_and_disagree_with_the_old_table`.
* **Two rows of the v0.9.0 body are specifically wrong and must be named:** the N4 row's
  "refuted on the mechanism, **confirmed on the correlation**", and §5.13's H5 row as published in
  v0.7.0. Both halves of the σ claim are withdrawn, not just the boundary.
* **What survives:** the noise of a suite is measurable (`runs/figures/stability.csv`); it does not
  predict whether a fixed-threshold ranking reproduces on this corpus.

### 2. The H1 boundary precision (from the commit after the v0.8.0 tag)

* **Where:** `REPRODUCTION.md` §5.13's H1 row now states that what ends above `[64]` is AdaGrad's
  *lead*, not its usefulness (`[16,16]` still beats the tuned-cosine baseline in 9/10 seeds).
* **Published in:** v0.8.0's archived tree (the tag `b363b77` predates commit `8e27e30`).
* **What the next release body must say:** one sentence, naming the commit, as v0.9.0's body already
  does — keep it in the queue until the next body is written so it is not lost.

## Carried forward: to be stated in the next body (not corrections, but not silent either)

### Correction target: **the public repository's CI state** — six red runs, one tolerance too tight

* **Correction target:** not a release body. The thing that was wrong is the **state of
  `CieveMe/autoresearch-experiment-runner`'s public CI**, which had been failing on every run since
  `main` #33 (and on the `v0.10.0` tag run #32), on all three jobs. The repository's most valuable sentence
  is "every number is pinned and checked by one command"; a reader arriving at the repo saw red crosses
  first. `v0.10.0`'s tag and body stay untouched — that tag's CI run is red forever and that is honest.
* **What was wrong:** one expectation, `trial[schedule_free_adamw].test_loss` in `schedule-free-mlp`
  (and three more of the same arm in `norm-layernorm`, `init-he`, `capacity-h32`), was pinned with a
  1e-6 tolerance while the quantity itself is only reproducible to ≈1e-3 across platforms. The other 470
  assertions matched on both platforms. Measured: Linux 0.12526376 against the pinned 0.12506323
  (+2.0e-4), and a one-ULP nudge to `exp/sqrt/tanh/erf` on a single machine moves the same arm by up to
  9.8e-4 while every other arm moves by exactly 0 (`scripts/perturbation_probe.py`). Full measurements and
  the mechanism are in `REPRODUCTION.md` §5.17; the case is **case 7** in `docs/defect-family.md`.
* **The fix:** that one trial now carries a per-trial `loss_abs = 0.005` — five times the largest measured
  movement — while every other expectation in the same files keeps `1e-6`; the verifier prints the
  tolerance it used, and `tests/test_harness.py::test_a_trial_tolerance_widens_that_trial_and_nothing_else`
  pins the scope from both sides. No check was deleted or skipped. The residual cost is stated: a
  regression below 5e-3 in that arm's final loss is no longer caught by that expectation, and is still
  caught by its integer speed pin, its accuracy pin and the schedule-free negative control.
* **What the next release body must say:** one section — the CI went red for six runs because one pin's
  tolerance was below its own reproducibility; here is the measured spread and the basis for the new
  tolerance; the full-tier gate now passes, quoted in full; and `v0.10.0` is not touched.
  **The runs to quote are in `runs/task-runs/FULL-TIER-ci-fix.md`:** the Windows full scorer at `0f3ce2f`
  (`100.0/100 (tier=full (all suites)) (474/474 checks, exit 0)`, all four controls detected —
  `schedule-free-without-averaging` still at 92.8/100, i.e. the widened tolerance did not disarm it), the
  Linux container `repro --tier full` (`474 checks, 0 failures`, against 4 failures before the fix), and
  the fresh-clone `docker compose up --build` (`RESULT: PASS`, compose exit 0).
* **Also worth one line in that body:** the CI jobs had never reached their later steps (they stopped at
  the reproduction step on every run since #33), so the steps after it — the scorer, the sweeps, the
  threshold curves — were only ever exercised locally. The next body should say whether they ran green in
  the equivalent environment.
* **And one line about the workflow split.** Those later steps are now separate parallel jobs (`scorer`,
  `sweeps`, `thresholds`, alongside the `repro` matrix and `docker`), because as one job the wall clock was
  their sum — 1.5–2 hours on a two-core runner, which is how three pushes can look like a red queue.
  Nothing was removed and no tier was lowered: the same commands run at the same tier, `thresholds` keeps
  its dependency on `repro` by taking that job's artifacts instead of re-running suites, and lowering
  `main` to the core tier stays off the table because that is exactly the misreading hard rule 2 exists to
  prevent.
* **Plus one line about concurrency.** Superseded runs on a branch are now cancelled
  (`concurrency.cancel-in-progress` is true for pushes to non-tag refs and false for tags), so three quick
  commits no longer leave three long runs queued — which is how a green repository had looked red. The
  workflow states the rule that goes with it: **a cancelled run is not evidence and may not be cited
  outward**; what may be cited is a run on a tag, or the run quoted verbatim in the release body, and
  neither is ever cancelled. That keeps the concurrency setting inside hard rule 2 instead of next to it.

### Metadata hygiene: the version fields were stale at `0.2.0`

### A footnote on negative claims (to be stated in the next body, one line)

Recorded after v0.11.0 was tagged, so it belongs to the next version's body rather than to that one.
While checking a reference, a query returned nothing and the note written said "no registry has it". The
direct lookup had the record — OpenAlex resolves `10.2307/4615733` to Holm (1979), *Scandinavian Journal
of Statistics* **6:65–70** — and Crossref genuinely lacks that DOI (404), with the journal's whole 1979
volume unsurprisingly undeposited. The observation was true; the inference was not. Rule now written into
`docs/defect-family.md` as a footnote (no case number, as requested): **a negative claim is "I ran this
query and it returned this", never "it does not exist"** — the second form cannot be reproduced and turns
a limitation of the query into a fact about the world. The next body should state this in one line, since
the footnote is part of the tree.

### A second footnote: "which copy is in play" (also one line in the next body)

Recorded after v0.11.0, so it belongs to the next version's body as well. Three failures of one shape
turned up in a single afternoon, all of them about *which artefact was being read* rather than about the
experiment: a count typed into prose while the generator said otherwise; a script edited in its source tree
while a scheduled task ran a deployed copy; a handoff file written to disk while a different block reached
the other side. The shared repair is the family's own rule — **make the copy that is in play able to say so
itself** (quote the generator; hash-check the deployed copy; name the file on the first line of the
handoff). Written into `docs/defect-family.md` as a footnote without a case number, because these are
process failures of the project rather than defects of this repository. The next body states it in one
line.

### A third footnote: a number carries its unit and its convention (one line in the next body)

Recorded 2026-09-30, so it belongs to the next body. The same revision of one file was reported to two
sessions as `4,315` and as `7,233` — characters and bytes, **both correct** — and the one-character residue
afterwards was the file's final newline (`4,314`), while the line count carries the same ambiguity (99
elements when the blob is split on newlines, 98 lines of text). Nothing about the file was in dispute; the
missing piece was the convention. The rule written into `docs/defect-family.md` is therefore *name the
instrument **and its convention***, and `docs/release-checklist.md`'s hard rule 4 now reads
**generator, definition, unit, test**. The next body states it in one line, next to the other two
footnotes, because all three are one claim seen from three sides.

### The intermittent red, and the rule that a gate run leaves a log (one line in the next body)

Recorded 2026-09-30. `make test-log` (→ `scripts/test_log.py` → `runs/test-last.log`) now writes the
command, the runner, the start time, the platform and the interpreter version into the log it keeps, and a
test pins that header so the runner no longer has to be inferred from a word. It was added after a suite run
was made and committed **in the same command** and its output was never kept: the one red run of that
afternoon then left nothing to diagnose from, and two green runs afterwards could not bring it back. The
log paid for itself on its first use — it reproduced the cause immediately (a `.pytest_cache` the copy
tried to copy, `WinError 5`), which is a copy-filter bug, and it also produced the rule that a working tree
is a shared resource. The next body states this in one line.

### And one more line for the next body: the mirror image of 6b (a code defect, not a process one)

Recorded after v0.11.0. `scripts/score_task.py`'s copy filter kept the committed analysis inputs **by
prefix**, which also copied gitignored scratch files such as `runs/paired-tests-raw.txt` into every scored
tree — a copy that contains something the repository never published. It was introduced by the fix for 6b
itself (which added those names to the filter) and caught by the privacy-hygiene guard added later
(`tests/test_privacy_hygiene.py`). Unlike the two footnotes above, this is a defect of this repository's own
code, so it is filed **inside case 6b** rather than as a process footnote, with the rule *a copy must be
isomorphic to the published tree in both directions*. The next body states it in one line.

### Case 6b's guard now has four references, and one of them is the intent (one line in the next body)

Recorded 2026-09-30, so it belongs to the next version. The copy is now audited from four places, each
answering a different question: **git**'s tracked and ignored sets (nothing published is missing, nothing
unpublished is carried), a hand-written list of what the policy is *allowed* to leave out
(`INTENTIONAL_DROPS` — `.github/`, `runs/task-runs/`, `runs/threshold-curves/`), and the published `runs/`
files the test sources name. Writing the intent list down immediately found two families that were leaving
every copy **by side effect of a rule** rather than by decision — 73 tracked files in three families — and
the four hand-picked names stay written out because two of them are read behind `skipTest` guards, so
running the suite inside the copy reports a *skip* rather than a missing file. The next body states this in
one line as an **extension** of case 6b, not a correction: no published sentence claimed the copy was
already audited from these angles.

* **What was wrong:** `pyproject.toml`, `autoresearch/__init__.py`, `CITATION.cff` and the README's
  citation line all still described version `0.2.0`, eight releases after it. In `CITATION.cff` that
  field is what a human reads when deciding what they are citing, so it is not decoration; the README
  listed only v0.2.0's version DOI, which reads as if that were the current archive.
* **When it was fixed:** after v0.10.0 was published, in its own commit — deliberately **not** folded
  into the corrections release, and the `v0.10.0` tag was not touched.
* **What the next release body must say:** one "also carried" line naming the commit and the four files,
  so the change is visible rather than discovered in a diff.
  > **Named 2026-09-30:** the two commits are `0497634` (the version fields moved off the stale `0.2.0`)
  > and `74ca558` (the duplicated version numbers deleted rather than refreshed). v0.11.0's body described
  > the change and named neither, which is why the next body states both — four commits later, and the
  > delay is the argument for not letting a queue entry wait longer than it has to.
* **Still stale, and left alone on purpose:** `.zenodo.json`'s `notes` text still describes version
  `0.2.0` (it is read by Zenodo on deposit, and the Zenodo side is the project owner's half), and
  `docs/release-checklist.md`'s title still says "(v0.2.0)" while its body is version-agnostic.
  **Both were fixed in the follow-up commit below, version-agnostically rather than by bumping the
  numbers — see the next entry.**

### Metadata hygiene, second pass: remove the duplicated version numbers instead of updating them

* **What was wrong:** `.zenodo.json`'s `notes` still described version `0.2.0`, `docs/release-checklist.md`
  put `(v0.2.0)` in its title, and the checklist's own concrete steps hard-coded `v0.2.0` — including the
  line that tells the releaser to check that `pyproject.toml`, `autoresearch/__init__.py` and
  `CITATION.cff` all say `0.2.0`, which became wrong the moment those were bumped. That is the same
  shape as cases 5 and 6: one fact maintained in several places, so every copy rots on its own.
* **How it was fixed:** by deleting the duplication rather than refreshing it. `.zenodo.json` now says the
  record describes "the version tagged in the repository" and points at the concept DOI; the checklist
  title has no version; the steps use `vX.Y.Z`; and the metadata check says "the version you are about
  to tag", with a note that no test reads those fields, which is exactly why they have to be checked by
  hand every release. A dated note in the Zenodo section states that the archive is the **tag snapshot**,
  so a later edit to `.zenodo.json` cannot change a release that is already queued.
* **What the next release body must say:** one "also carried" line naming this commit and the files
  (`.zenodo.json`, `docs/release-checklist.md`).
* **Not touched:** the `v0.10.0` tag. The change is a commit on `main` after that tag, and the tagged
  snapshot keeps the file as it was.

### Correction target: **the `v0.10.0` release body** — §5.16's comparison count (78 → 79)

> Every entry in this file names the version whose body it corrects. This one is worth reading closely for
> that reason alone: it corrects the **release published immediately before it**, which was itself the
> corrections release for `v0.9.0`. A corrections release can need correcting — the rule does not change.
> The correction goes into the next body; `v0.10.0`'s body and tag are not touched, exactly as `v0.9.0`'s
> were not.

* **Correction target:** the **`v0.10.0` release body** (published 2026-09-28, release id `398224373`,
  body = `docs/release-notes-v0.10.0.published.md`), specifically its §5.16 summary line "across all 78
  comparisons nothing survives a family correction (smallest adjusted p = 0.15)". §5.16 in
  `REPRODUCTION.md` carried the same sentence and is already fixed in the tree.
* **What was wrong:** §5.16 and the v0.10.0 release body both say "across all 78 comparisons". The
  committed artifact `runs/paired-tests/paired-tests.json` says 79, because the corpus grew by one when
  the T-ADAM-01C ablation suite was registered after that prose was written. The claim is unaffected
  (nothing survives a family correction either way) and the smallest adjusted p is 0.1543, which the body
  rounded to 0.15 — but the count is a number, and it was quoted from memory rather than from the file.
* **When it was fixed:** in the tree now, with the note in §5.16 recording both numbers and why they
  differ.
* **What the next release body must say:** one line, and it must **name `v0.10.0` as the corrected
  version** — the count is 79 and the smallest adjusted p is 0.1543, so that body's "78" and "0.15" are
  superseded, with `make stats` (and the field paths in `docs/a3-data-pack.md`) as the authority.
* **Also to state, under the case 5/6 family note:** that the release checklist's own metadata line
  ("confirm the three files all say `0.2.0`") was already false the moment those files were bumped — the
  smallest example of the same disease, worth one sentence rather than a case of its own.

#### Follow-up, same entry: the count also lived in three more files, and the guard now enforces the rule

* **What the first pass missed:** after the queue entry above was written, a grep for the number found it
  still live in `README.md` (the outward-facing summary), `TODO.md`, `CHANGELOG.md` and a comment in
  `scripts/paired_stats.py` — the file that produces it. Four places, one of them corrected: the same
  disease as case 5, with the repair itself spreading only as far as somebody remembered to look. This is
  the third member of the family note in `docs/defect-family.md`.
* **How the live files were treated** (deliberately not "78 → 79", which would only postpone the rot):
  * `README.md` and `TODO.md` **no longer restate the count or the adjusted p**; they make the qualitative
    claim and point at `REPRODUCTION.md` §5.16 and the `make stats` artifact (field paths in
    `docs/a3-data-pack.md`);
  * `scripts/paired_stats.py`'s comment carries no numbers — the producer least of all;
  * `CHANGELOG.md` **keeps its text as a record of what was said at the time**, and is exempt from the
    guard by being named in it.
* **The rule is now mechanical**, because otherwise it depends on memory:
  `tests/test_paired_stats.py::test_live_documents_do_not_hard_code_the_corpus_size` (with companions that
  the artifact still owns the count and that the live documents still point at it). Writing it immediately
  failed case 6b's own guard — the artifact it reads was not yet copied into the scored tree — so
  `scripts/score_task.py`'s copy filter now also keeps `runs/paired-tests` and `runs/figures`.
* **What the next release body must say:** one line — the three live files now reference the artifact,
  `CHANGELOG.md` is kept as history on purpose, and a test enforces it from now on.

## Rules for the person writing the next body

1. Every item above gets an explicit line in the release body, with the section it corrects.
2. The corrected sections in the repository keep their wrong text visible (struck through or quoted)
   plus the correction next to it — never a silent rewrite.
3. If a correction changes a **claim**, the paper cards change too, because they are what a reader
   quotes.
4. If a correction invalidates a number a third party might have cited, say so in one sentence:
   "if you quoted X, the number is now Y".
