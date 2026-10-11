# Undergraduate staging — not published to the bank

Branch: `work/undergraduate-five-collections-unpublished-20261011`

This branch holds **five independent year/source coverage files** for the eventual five searchable problem collections:

| Collection | Start | Last indexed year |
| --- | ---: | ---: |
| IMC | 1994 | 2026 |
| Putnam | 1938 | 2025 |
| SEEMOUS | 2007 | 2026 |
| Vojtěch Jarník | 1991 | 2026 |
| Simon Marais | 2017 | 2025 |

These are **research inventories**, **not imported question statements**, **not completed examination text files**, and **not classified problem records**. `problem_records_imported: 0` is deliberate and must not be changed until actual source-verified problem objects have been added. Do not infer completion from a year's existence in the inventory.

Each eventual individual problem must follow `metadata/undergraduate-import-contract.json`: complete verified statement in LaTeX, exact year and competition number, correct day/session/paper/category, taxonomy topics, Problem DNA, figures when necessary, traceable primary source, and documented publication basis. No solutions, invented problem numbers, or missing-diagram omissions. Early Putnam contests require historically correct structure; 1943–45 absent, 1958 has two events. Coverage-year entries for competitions other than Putnam do **not** confirm that each contest took place in every year; they identify the user-requested search span.

To check the five coverage inventories:

```sh
node staging/undergraduate/check-staging.cjs
```

## Separation from public bank

This work is stored only on an unpublished feature branch. It is **not merged into `main`**, is **not wired into `index.html`**, `COUNTRIES`, the runtime manifest or the published problem count, and does not alter any public grid. **Because the repository is public, GitHub branch files are still publicly readable at their direct URLs**, even though they are not exposed in the bank UI.

To complete this task, verified lawful-to-publish original statements must be gathered, transcribed and mathematically checked, classified and then persisted as real problem JSON. Do not change the status to complete until that work is finished.

## Five separate structured problem JSON drafts

The following files now exist **on this work branch only**:

- `IMC-university-problems.json`
- `Putnam-problems.json`
- `SEEMOUS-problems.json`
- `Vojtech-Jarnik-problems.json`
- `Simon-Marais-problems.json`

They contain the requested historical-year slots and known original source references. **Putnam 1985–2000 now contains 192 source-transcribed A1–B6 statement texts.** Their source LaTeX is preserved, but independent mathematical fidelity review, MathJax/HTML normalization, topical tags and Problem DNA are still pending; these problems are not approved for bank publication. Four short independently reworded, mathematically equivalent sample tasks are now saved in IMC 2026 P1, SEEMOUS 2024 P2, VJIMC 2025 Category I P1, and SMMC 2025 A1. They are **not verbatim copies** or complete examination series; topic and Problem DNA classifications are provisional. Every other problem list remains empty. They must **not** be described as completed question banks. Only actual verified full statement records may populate them; mathematical topics, DNA tags and graph links must be checked per question. These draft files are not wired into the live application, and GitHub public repository branch links are visible to others who know the URL.

## Putnam 1985–2000 archival provenance and reproduction notice

The 192 Putnam statement records in the unpublished `Putnam-problems.json` were taken from statement-only, unofficial LaTeX files held by `rpxgit/The-Putnam-Archive` (year and URL cited on each entry). The copyright notice in the MAA book *The William Lowell Putnam Mathematical Competition 1985–2000: Problems, Solutions, and Commentary* (2002) expressly permits reproduction for educational/scientific purposes without fees or permission, except services charging for delivery of documents, and requires the following credit:

> First published in The William Lowell Putnam Mathematical Competition 1985–2000: Problems, Solutions, and Commentary, © 2002 by the Mathematical Association of America.

This notice applies to that book and period, not automatically to other years or competitions. Current GitHub files are publicly readable although this branch is **not merged** into `main`. These transcripts are **source-extracted, not independently verified against MAA originals** and retain plain LaTeX constructs that may require normalization for the live bank.

Historical years before 1985 and contest texts after 2000, plus the other four contests, remain **untranscribed** in these JSON drafts.

## 1938 original exam verification (2026-10-11)

The original **first Putnam examination (1938-04-16)** has been located in Joseph A. Gallian's independent historical article, Appendix I: https://www.d.umn.edu/~jgallian/putnam13.pdf . A separate file `put-1938-exam-index.json` records all **13** numbered problems, original morning/afternoon split (morning 1–7, afternoon 8–13), and a/b alternative questions **7 and 8**, with provisional subject notes. The index summaries are **not full exam transcriptions**; the 1938 `problems` array in `Putnam-problems.json` is still empty and its verification status states that explicitly. Never impose A1–B6 on this first examination.

## Four first non-Putnam sample statements (2026-10-11)

The four other competition JSONs each contain **one** source-checked **independently reworded** mathematical question with its original year, exact identifier, mathematical LaTeX, source URL, topic and controlled-vocabulary Problem DNA tag. These are expressly marked `statement_form: independently_reworded_equivalent_not_verbatim` and `taxonomy_status: provisional`. They are not presented as full sets or official text copies. Source references: IMC official 2026 problem 1; SEEMOUS official 2024 problem 2; VJIMC official 2025 Category I problem 1; Simon Marais official 2025 A1.

**Incomplete:** 33 years of IMC, 20 SEEMOUS, 36 VJIMC and 9 SMMC years are not fully populated. Earlier progress is insufficient for user's request for all exam statements. Do not merge this branch into the public bank.

## IMC 2026 complete two-day mathematical restatement set

The 2026 IMC exam now contains **10 separately authored, mathematically equivalent statement records**, numbered 1–5 for Day 1 and 6–10 for Day 2, with exact official source page per problem. Each record has LaTeX, topic tags, controlled-vocabulary Problem DNA, and `statement_form: independently_reworded_equivalent_not_verbatim`. The categorization is **provisional**. All **other** IMC years remain untranscribed and the entire work branch remains unpublished to the live bank. This is not a license to copy other organisers' original texts.
