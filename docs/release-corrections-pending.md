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

## Queue

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

### Metadata hygiene: the version fields were stale at `0.2.0`

* **What was wrong:** `pyproject.toml`, `autoresearch/__init__.py`, `CITATION.cff` and the README's
  citation line all still described version `0.2.0`, eight releases after it. In `CITATION.cff` that
  field is what a human reads when deciding what they are citing, so it is not decoration; the README
  listed only v0.2.0's version DOI, which reads as if that were the current archive.
* **When it was fixed:** after v0.10.0 was published, in its own commit — deliberately **not** folded
  into the corrections release, and the `v0.10.0` tag was not touched.
* **What the next release body must say:** one "also carried" line naming the commit and the four files,
  so the change is visible rather than discovered in a diff.
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

## Rules for the person writing the next body

1. Every item above gets an explicit line in the release body, with the section it corrects.
2. The corrected sections in the repository keep their wrong text visible (struck through or quoted)
   plus the correction next to it — never a silent rewrite.
3. If a correction changes a **claim**, the paper cards change too, because they are what a reader
   quotes.
4. If a correction invalidates a number a third party might have cited, say so in one sentence:
   "if you quoted X, the number is now Y".
