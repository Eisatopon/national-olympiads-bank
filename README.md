# National Olympiads Problem Bank

A collection of national mathematical olympiad and team selection test statements, with an English interface and MathJax rendering.

## Current application

`index.html` is the standalone application. It loads one `<Country>-<competition>-problems.json` per collection from this repository. Features include country/year and keyword search, problem-set selection and reordering, local saving, printing with mathematical notation, and URL/QR sharing.

The older Olympiad Bank in `Eisatopon/eisatopon-next` is a separate application and dataset; an automated integration is not yet implemented.

## Data integrity

China is temporarily excluded from search and problem sets because its archive contains corrupted statements and duplicate identifiers. The original JSON is retained for reconstruction. Counts in the application cover available collections, not the quarantined archive.

Argentina has documented numbering gaps in 1994, 1996, 2007, 2008 and 2010. Original numbers are preserved; these years should not be treated as complete.

Passing validation confirms structural checks, not mathematical correctness or verification against an official source. Source research is in `.dev/sources.json`; per-problem source verification progress is tracked in `docs/verification-progress.md`.

## Schema

```json
{"competition":"Competition name","years":[{"year":2025,"problems":[{"number":1,"problem":"Prove $x=x$."}]}]}
```

Years are ascending and unique. Numbers are positive integers in official order. Optional `day` identifies an exam day or paper and must be positive. Optional `category` is used by the topic filter. The USA TSTST archive retains its legacy schema, handled by a separate loader.

Most statements do not yet have topic or difficulty metadata. The application does not provide a difficulty filter. Figures currently appear as image URLs in statement text.

## Validation

Run from the repository root:

```bash
python -m unittest discover -s tests
node tests/test_loader.cjs
python scripts/validate_data.py
```

GitHub Actions runs these checks on pushes and pull requests. The validator checks JSON structure, collection registration, unique years and identifiers, numbering, nonempty statements, dollar delimiter parity, control characters and local figure existence. Known Argentina gaps are explicit exceptions; changes to their numbering fail validation. China is reported as quarantined and must remain marked as such in the application until repaired.

The loader also rejects duplicate identifiers before storing any records from a collection, preventing an incorrect statement from being selected or printed under a reused identifier.

## Local preview

Serve the repository using `python -m http.server`. The committed application loads published data from `main`. To inspect local data changes, replace `BASE` with `./` in a temporary copy; do not commit that preview-only change.

## Source transparency

`metadata/collections.json` records source research links separately from problem statements. Every collection has an explicit verification state. The initial links were carried over from `.dev/sources.json` through a manually selected competition-to-file mapping; they have not been certified as the source of an individual statement. The UI labels them as research links and does not claim source verification. Collections without recorded links say so explicitly.

Known missing Argentina problem numbers are shown in problem cards and on printed sets when source notes are enabled. Metadata failures leave statements available with a warning. Source verification records the exact paper, page, review method and reviewed text before displaying a checked claim.

## Statement comparison: first batch

165 statements were visually and textually compared with published exam PDFs on 2026-10-02: all 85 stored USA TST statements (2012–2026, no stored 2022 cycle), 40 Australia AMO statements (2016–2020), and 40 New Zealand NZMO Round Two statements (2019–2026). USA sources are Evan Chen's archive and the public USA TST archive; Australia and New Zealand sources are the organizers' PDFs. These are source-copy fidelity checks performed with AI assistance, not a human certification or an independent review of solutions. No material statement discrepancies were found in this batch.

Individual `statement_checks` records include the exact reviewed statement, its SHA-256, source PDF checksum, URL, page, original problem number, review method and date. The UI displays the checked status only when the current statement exactly matches the reviewed snapshot; CI rejects stale text and changed reviewed figures using SHA-256 checksums. A collection-wide unverified status does not override these granular checks or certify its remaining years.

The year denotes the selection cycle, which can begin in December of the previous year. The 2012 source PDF has an inconsistent IMO-edition header; its exam dates are recorded in the review notes without changing the bank's year labels.

Generate the full 64-collection inventory with `python scripts/verification_progress.py`. The inventory counts stored records and explicitly separates checked and pending records, including the quarantined China data.

## Personal collections and classroom printouts

Save multiple named collections on the current browser/device, reopen them or delete a saved copy without clearing the current set. Sharing preserves ordered problem IDs, the title, source visibility and solution-space settings. Opening a shared link loads that exact set instead of merging it into the recipient's previous selection. Existing shared links still work, including competitions with longer identifiers. Collections stay local; keep a share link as a portable copy.

Printouts offer no solution space, 4 cm or 8 cm per problem. Printing waits for typesetting and figure loading, keeps ordinary problem blocks together and constrains figure size. Very long problems may span pages.

## Thematic browsing

Topic filters work across countries and years, using Geometry, Number Theory, Combinatorics and Algebra. Existing editorial categories take precedence. Statements without a recorded category receive conservative keyword-based suggestions; a problem can belong to multiple topics. Ambiguous cases remain Unclassified. These browsing labels are not a reviewed mathematical classification and do not change source statements.

## Mathematical connections and Problem DNA

Every problem offers mathematical connections through concepts in its statement. Related results require at least two shared concepts or a shared reviewed technique, exclude the source itself and identical statement copies, and prefer another competition when scores tie. Suggestions explain the matching concepts or techniques; concept overlap does not establish an equivalent solution.

The initial Problem DNA pilot contains 13 records in `metadata/problem-dna.json`, each with an ordered technique sequence, exact statement snapshot/hash, concise mathematical solution derivation, review date/method and a relative practice level (1–3). Analysis is AI-assisted, not human certification. Techniques are hidden behind a reveal control to avoid immediate spoilers. Earlier practice and next challenges use levels only within this reviewed pilot; no difficulty is inferred from official problem numbers. This small pilot starts the longer-term 100–200 problem curation plan.

The UI drops DNA when the statement changes, and `scripts/validate_dna.py` rejects stale or incomplete records in CI. Connections and concept browsing continue if DNA metadata is unavailable. Source statements and original identities are unchanged.

## Thematic corrections (2 October 2026)

151 previously unclassified statements now have explicit full-statement topic reviews in `metadata/topic-overrides.json`, including mixed-topic cases. Existing recorded categories take precedence, then exact-text reviewed overrides, then the fallback classifier. The fallback now handles plural geometry terms, solid geometry, polynomial notation, mathematical inequality symbols, recurrences and common integer/combinatorial structures. Regression tests include real omitted geometry and algebra problems across several countries. These changes repair the earlier incomplete keyword classifier; they do not certify a reviewed classification for every bank record. CI rejects stale thematic snapshots.

## Focused thematic audit (2 October 2026)

A subsequent full-statement audit covers 224 active records in three risk groups: Geometry + Number Theory, Geometry + Algebra, and Geometry-only statements mentioning cubes. All 12 referenced figures were visually inspected. Topic sets changed for 168 records; some changes add a substantive subject rather than remove an error. There are now 374 distinct statement-reviewed overrides, including the previous batch and one overlapping record.

`docs/topic-audit-2026-10-02.json` records each decision, rationale, statement hash, prior labels, reviewed labels, inspected figures and two source-follow-up items. This audit does **not** claim review of all 9,458 active records: 9,234 were outside this audit. It reviews thematic content of stored statements, not correctness of solutions or fidelity to original sources. CI checks audit/override consistency and exact statement snapshots.

## Remaining unclassified statements and Greece TST review

All 253 statements still labelled Unclassified after the focused audit have now been read and assigned explicit, individually justified topics. All five referenced figures were visually inspected. The infinite-series and definite-integral problems use the additional Analysis category, which the existing dynamic topic filters support. `docs/topic-audit-unclassified-2026-10-02.json` records the review and source evidence.

All 72 stored Greece TST statements were then reviewed. Eleven topic sets changed; 56 records were newly reviewed, with 16 overlapping earlier batches. Polynomial-ring divisibility is Algebra; colour-only complete-graph problems and lattice path counts do not acquire Geometry merely from their drawing. `docs/topic-audit-greece-2026-10-02.json` records individual reasoning and five source-follow-up items in the stored Greek statements.

One CHKMO 2015 problem had ambiguous plural wording inherited from its official compilation. Visual comparison of the official question and solution confirms that the **sum** of the radicals must be a positive integer. Its final phrase is clarified accordingly; the formula is unchanged. The source URLs and PDF page references are preserved in the review metadata. The earlier Indonesia 2011 and Vietnam 1971 source concerns remain open: no suitable official source was obtained, and those statements were not changed.

All 132 stored BMO1 statements (2005–2026) have also been read. Forty-two topic sets changed, and 116 records were newly reviewed. Circular arrangements, lattice paths and colouring problems receive Combinatorics when their mathematical content requires it. `docs/topic-audit-bmo1-2026-10-02.json` records this complete collection review. Rationales are required for changed and mixed classifications; clear unchanged single-topic cases retain an exact statement snapshot, hash, date and category. Earlier rationales are preserved.

All 88 stored BMO2 statements (2005–2026) have also been read. Twenty-seven topic sets changed, with 84 newly reviewed records. The cyclic movement game is Combinatorics and Number Theory, while genuine lattice-distance problems retain Geometry alongside their arithmetic or placement constraints. `docs/topic-audit-bmo2-2026-10-02.json` records this full collection review.

There are now **883 distinct statement-reviewed records** out of 9,458 active records; **8,575 remain outside full-statement thematic review**. All previously Unclassified active statements have explicit reviews in this branch. This does not certify the remaining automatic labels. `docs/topic-review-progress.json` preserves non-additive, distinct coverage. The reviewed corrections were published at the owner's request on 2 October 2026 after successful validation. The broader thematic review remains incomplete.
