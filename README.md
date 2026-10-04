# National Olympiads Problem Bank

A collection of national mathematical olympiad and team selection test statements, with an English interface and MathJax rendering.

## Current application

`index.html` is the standalone application. It loads one `<Country>-<competition>-problems.json` per collection from this repository. Features include country/year and keyword search, problem-set selection and reordering, local saving, printing with mathematical notation, and URL/QR sharing.

The older Olympiad Bank in `Eisatopon/eisatopon-next` is a separate application and dataset; an automated integration is not yet implemented.

## Data integrity

China now indexes 168 statements in 28 six-problem papers: 1987–1993, 1995–1996 and 1998–2016. The remaining historical gaps are 1994 and 1997. Uploaded AoPS papers are visually checked, with source errors, restored conditions and unresolved variants recorded in metadata. This does not certify every statement against an official original. The corrupted original archive remains in `docs/quarantine/China-olympiad-problems-pre-rebuild.json` and is never loaded by the application.

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

GitHub Actions runs these checks on pushes and pull requests. The validator checks JSON structure, collection registration, unique years and identifiers, numbering, nonempty statements, dollar delimiter parity, control characters and local figure existence. Known Argentina gaps are explicit exceptions; changes to their numbering fail validation. Damaged historical China records remain outside the active collection; the rebuilt China data receives the same strict validation as other collections.

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

The next batch covers 1,000 previously unreviewed statements across UK TST, Netherlands final/TST and Swiss final/selection. It changes 258 topic sets, includes inspection of all 26 referenced figures, and completes thematic coverage of the first four collections. Three wording concerns are recorded separately for official-source follow-up; the source statements are unchanged. See `docs/topic-audit-batch1000-2026-10-02.json`.

The second 1,000-statement batch changes 311 topic sets and inspects all 17 referenced figures, including both alternatives in multi-version German records. It completes Swiss selection, Germany BWM/MO, Hong Kong final/TST and Romania final/TST thematic coverage, and reviews another 63 Lithuania final statements. Five stored-wording concerns are recorded for official-source follow-up. See `docs/topic-audit-batch1000-2-2026-10-02.json`.

The third 1,000-statement batch changes 294 topic sets and inspects all 78 referenced figures. It completes Lithuania final/TST, Slovenia, Latvia, Estonia TST, Portugal, Denmark, Finland, Iceland and Hungary Kurschak thematic coverage, and reviews another eight Australia AMO statements. Two stored-wording concerns are recorded for official-source follow-up. See `docs/topic-audit-batch1000-3-2026-10-02.json`.

The fourth 1,000-statement batch changes 274 topic sets and inspects all 24 referenced figures. It completes Australia AMO, New Zealand, North Macedonia, Ukraine, Bulgaria, Kazakhstan, Hungary OKTV, Cyprus TST, France TST, Estonia final, Norway Abel and Croatia national thematic coverage, and adds 88 Croatia HMO reviews. Five stored-wording concerns are recorded for official-source follow-up without changing source statements. Identical statements retain consistent topic sets, including the magic triangulation problem appearing in Cyprus and Croatia. See `docs/topic-audit-batch1000-4-2026-10-02.json`.

The fifth 1,000-statement batch changes 293 topic sets and inspects all 26 referenced figures. It completes Croatia HMO, Austria, Czech-Slovak, Serbia national, Serbia TST, Poland, Spain and Italy thematic coverage, and adds 22 Azerbaijan TST reviews. Six stored-wording concerns are recorded for official-source follow-up without changing source statements. Exact duplicate statements have no topic-set conflicts with earlier reviews. See `docs/topic-audit-batch1000-5-2026-10-02.json`.

The sixth 1,000-statement batch changes 301 topic sets and inspects all five referenced figures. It completes Azerbaijan TST, Singapore, India, Korea KMO/FKMO, Indonesia and Japan thematic coverage, and adds ten Philippines reviews. Six stored-wording or missing-diagram concerns are recorded for official-source follow-up without changing source statements. Exact duplicate statements have no topic-set conflicts with earlier reviews. See `docs/topic-audit-batch1000-6-2026-10-03.json`.

The seventh 1,000-statement batch changes 277 topic sets and inspects all 15 referenced figures. It completes Philippines, Ireland, Canada and Brazil thematic coverage, and adds 28 Mexico reviews (42 of 238 stored statements reviewed cumulatively). Ten stored-wording or missing-diagram concerns are recorded for official-source follow-up without changing source statements. Exact duplicate statements have no topic-set conflicts with earlier reviews. See `docs/topic-audit-batch1000-7-2026-10-03.json`.

The eighth 1,000-statement batch changes 265 topic sets and inspects all 11 referenced figures. It completes Mexico, Argentina, Vietnam and Turkey thematic coverage, and adds 168 Russia reviews (189 of 264 stored statements reviewed cumulatively). 38 stored-wording or missing-diagram concerns are recorded for original-source follow-up without changing source statements. Exact duplicate statements have no topic-set conflicts with earlier reviews. See `docs/topic-audit-batch1000-8-2026-10-03.json`.

There are now **8,883 distinct statement-reviewed records** out of 9,458 active records; **575 remain outside full-statement thematic review**. All previously Unclassified active statements have explicit reviews in this branch. This does not certify the remaining automatic labels. `docs/topic-review-progress.json` preserves non-additive, distinct coverage. The reviewed corrections were published at the owner's request on 2 and 3 October 2026 after successful validation. The broader thematic review remains incomplete.

## Sweden national finals (3 October 2026)

Sweden SMT adds all six final problems for each calendar year 2006–2024: 114 English translations from 19 official Swedish papers, with three original statement figures. Every statement has individual visual/textual source-comparison evidence and an explicit thematic review. No solutions or hints were imported. Calendar-year labels follow the exam dates rather than the archive's later school-year labels. The bank now has 50 countries and 65 collections, with 9,572 active records. Historical thematic audit counts remain snapshots of the bank at their review dates.

## Belgium senior finals (3 October 2026)

Belgium OMB MAXI adds all four senior final questions, with every subpart, for 2022–2026: 20 English translations from official French papers, with four required statement figures. Every statement has source-comparison evidence and thematic review metadata. Lower categories and all solutions in the 2022–2024 compilation were excluded. With Sweden and Belgium, the bank has 51 countries, 66 collections and 9,592 active records; 399 records have source-comparison evidence.

### Italy PreIMO TST (2010–2019)

Added 60 English statements from the official Italian archive, six per year. Day 1 contains A1–A3; day 2 contains B1–B3, with continuous annual numbering 1–6. All formulas and subparts were compared with the rendered original TST pages. Each record includes source evidence and thematic review. No training exercises, solutions or hints imported. The active bank now contains 9,652 problems across 67 collections and 51 countries.

### Thailand papers and TMO statements

Added 20 searchable English LaTeX statements from the user-supplied TMO 2021 and 2023 PDFs, five problems per day. All formulas were visually compared with the supplied pages; notably TMO 2021 Problem 3 is $a^a bc+b^b ca+c^c ab$. Source evidence and thematic review accompany every indexed statement. The active bank now contains 9,672 problems across 68 collections and 52 countries.

The [Thailand PDF archive](thailand-pdfs.html), linked from the main bank, contains 33 complete statement documents: TMO 2004–2024, TST 2011–2021, and TSTST 2021. Official Thai originals cover TMO 2020, 2022 and 2024; the other documents are English. The 2021 TST and TSTST documents combine the English statement pages from the original papers. An explicit hint on page 8 of TST 2014 was removed; no statements or definition notes were removed. Original and published document fingerprints are recorded in `docs/thailand-pdf-archive.json`.

PDF documents other than TMO 2021 and 2023 are not individually indexed and are not counted as additional searchable problems. Historical source ambiguities (TMO 2004, TST 2011/2013) and a date typo (TMO 2007) are explicitly marked. This is complete coverage of the retrieved papers, not a claim of all Thai contest history. TMO 2025–2026 and selection papers outside the recorded ranges remain unretrieved; the 2026 event programme contains no exam paper and is excluded. Training camps, practice sets, solutions and hints are excluded.

### Uruguay senior national final (2011–2017)

Added all 28 Level V final statements, four per year, as complete English LaTeX records with source evidence and thematic metadata. Every source statement page and formula was visually reviewed; a Pascal-triangle illustration is cropped from the 2017 source. No solutions or hints are included. The original domain in 2016 Problem 3 is explicitly corrected from “positive integer” to n ≥ 2, with the discrepancy displayed on screen and in print. The 2012 Problem 4 quantifier is normalised to the variable n used in its inequality. Coverage outside 2011–2017 is not claimed.

Seven original source documents remain available from the provenance details: four PDFs and three Word documents (2012–2014). Their original hashes and the review-render hashes are recorded in `docs/uruguay-source-documents-2026-10-03.json`. The same discreet “Original PDF” link is added to the supplied Thailand 2021/2023 problem provenance. The active bank now contains 9,700 problems across 69 indexed collections and 53 countries.

### Chile senior team selection tests

Added all 46 senior statements from the 12 published selection papers: Ibero 2013–2015, shared IMO/Ibero 2016, IMO 2022–2026 and Ibero 2023–2025. The shared 2016 paper appears once. All subparts, formulas and four original figures were visually checked and translated to full English LaTeX. No solutions or hints are included. The explicitly junior-only problem 1 in Ibero 2024 and IMO 2025 is omitted. Bank numbering is continuous per year, with original numbers in provenance; day 1/2 denotes IMO/Ibero in 2023–2025 and day is omitted otherwise. Gaps outside the listed papers remain explicit.

Twelve linked downloads contain statements only: eleven original papers and one raster-only statement extract from the 2026 source, whose interspersed solutions are excluded. Source domain omissions in Ibero 2013/2023 and explicit clarifications in IMO 2024/Ibero 2025 appear on screen and in print. The source term “crecientes” in Ibero 2025 Problem 1 is translated as nondecreasing. The original 2026 source link is labelled as including solutions. Evidence and file hashes are recorded in `docs/chile-source-documents-2026-10-03.json`. Active total: 9,746 problems, 70 collections and 54 countries.

### Gap filling — 3 October 2026

The Thai TMO row now indexes all 294 recorded problems from the retrieved 2004–2024 papers, including the early short-answer sections (274 additional records). The 2020 geometry diagram is cropped from the original official paper. One 2004 statement has an incomplete source condition and remains explicitly flagged; further source conventions are recorded as editorial notes.

A separate Thailand TST row indexes 189 problems from all retrieved 2011–2015 papers. Original within-paper numbering is recorded in provenance while bank numbering is continuous within each year. The 2014 hint and scoring instructions are excluded. Source ambiguities and explicit editorial corrections appear on the affected records; these records are not certified as mathematically correct. TST 2016–2021 and TSTST indexing remains in progress.

The six problems of the official Swedish final dated 22 November 2025 extend the SMT row to 2006–2025 (120 problems). No solutions or hints are included in these additions. Active total: 10,215 problems across 71 collections and 54 countries. Earlier totals above are historical snapshots.

The next Thai TST pass adds all 71 recorded problems from the 2016–2017 papers (260 TST records total). The unconfirmed change from “infinitely many” to “finitely many” in TST 2012 Day 9 Problem 1 has been reverted to the literal source; the defective assertion is explicitly flagged and is not usable as a verified exercise. Records with unresolved source omissions or ambiguities now display “Source issue — awaiting verification” in screen and print provenance. Active total: 10,286. No claim of complete gap closure is made.

### Thai TST 2018–2021 and TSTST 2021 gap fill

Added 100 complete TST statements: 2018 (28), 2019 (27), 2020 (24), 2021 (21). A separate TSTST row adds all 12 problems from four 2021 papers. Every source statement page and formula was visually compared. Continuous annual numbering; day denotes paper index. Source Day 0–6 in TST 2021 maps to bank day 1–7; the original PDF labels remain available. TST 2020 combines four two-day tests, indexed as papers 1–8 with original within-test problem numbers in provenance.

The retrieved Thai archive is now fully indexed: 294 TMO, 360 TST, 12 TSTST problems. Printed source omissions and ambiguities are retained and explicitly flagged, rather than silently repaired. No solutions or hints. Active total: 10,398 across 72 collections and 54 countries. This does not close newer or older Thai years, unresolved source issues, or other-country gaps.

### Chile senior final — verified source batch

Added 44 complete statements for 2014–2016, 2018 and 2020–2023, including seven original statement figures. Downloads contain only senior statements; all printed solutions and the 2022 complementary training problem are excluded. The unspecified tangent choices in 2018 Problem 6 are explicitly flagged. The mislabeled 2024 national-round file and inconsistent 2019 header have not been silently imported as finals. Earlier Chile years remain under review. Active total: 10,442 across 73 collections and 54 countries.

### Chile earlier finals and source-label corroboration

Added 111 complete statements for 1990, 1992, 1994, 1996–1997, 2000–2003, 2006–2012, 2019 and 2024, with 10 original diagrams and 18 statement-only PDFs. Chile Final now has 155 records in 26 years. Matching AoPS collections corroborate the 2019 year and 2024 senior-final classification; the official source condition k > 2 is retained. Printed source defects are visible notes. Missing original figures or missing statements prevent faithful completion of 1989, 1991, 1995 and 1999; 1993/2013 remain under review. Active total: 10,553; no claim that all bank gaps are closed.

### Italian PreIMO earlier selection tests

Added all 49 TST statements for 2002–2008 and 2022, including original 2004 cube diagrams, complete statements continued onto later pages, and eight statement-only source PDFs. The 2022 official paper has seven statements (four on day 1, three on day 2); none is discarded to force a six-problem format. Italy PreIMO now contains 109 records across 18 years. Other years are still under source research. Active total: 10,602.

### Belgian OMB older senior finals

Added all eight MAXI final statements for 2007/2008 from public official attachments. Original statement diagram and two statement-only PDFs included; 2007 solutions and junior categories physically excluded. Belgium now has 28 records in seven years. The central historical final archive requires sign-in; missing years remain explicitly open.
