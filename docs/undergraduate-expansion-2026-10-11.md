# Undergraduate expansion — implementation and source protocol
Date: 2026-10-11
Status: source discovery and integration specification; **zero undergraduate statements imported**.

## Goal
Add a fifth section, **Undergraduate**, alongside National, Regional, International and Tournaments. Keep the country's existing grid, color design, search, selection, printing and Ask AI flow unchanged. Do not relabel Putnam as International Olympiad or dilute the existing National scope.

## Priority full-exam collections

| Candidate | Proposed key | Proposed JSON | Years to audit | Sources |
| --- | --- | --- | --- | --- |
| William Lowell Putnam Mathematical Competition | put | Putnam-problems.json | Official recent archive 2018–2025; historical editions separately | https://maa.org/maa-putnam-archive/ |
| International Mathematics Competition for University Students | imc | IMC-problems.json | 1994–2026 | https://www.imc-math.org.uk/?item=problems |
| SEEMOUS | seem | SEEMOUS-problems.json | published proceedings by year, verify | https://www.seemous2025.com/ |
| Vojtěch Jarník International Mathematical Competition | vjimc | VJIMC-problems.json | verified editions only | https://vjimc.osu.cz/ |
| Simon Marais Mathematics Competition | smmc | SimonMarais-problems.json | verified complete A/B/C papers | https://www.simonmarais.org/ |
| Miklós Schweitzer Competition | schw | Schweitzer-problems.json | only complete exam series available with publication clearance | source discovery pending |

## Integrity gates
1. Check source-use and republication permissions, attribution and exam copyright before distributing full texts. Public access to a PDF is not by itself republication permission. Until confirmed, maintain links and metadata, not a full exam transcription.
2. Verify exact exam, year, session/day, complete problem count and mandatory graphics before any ingest. For Putnam, preserve A1–A6 and B1–B6 by storing `day:1` / `day:2` and `number:1..6` per session, or adopt one documented display convention without changing existing ids.
3. IMC: store Day 1 problems 1–5 and Day 2 problems 6–10, retaining both actual numbers and day labels. Individual years can have different formats: verify each rather than assuming ten.
4. For Simon Marais, A/B/C are **paper variants**, not chronological exam days. Do not merge their problem numbering into the same day without a distinct paper ID strategy and schema tests.
5. No solutions or implicit solution hints in problem statements. Keep original figure and mathematical notation. Cite source and page; classify full statements by mathematical topic and preserve source-review state accurately.
6. Update `index.html` list of country/competition rows with `scope: 'undergraduate'` only after the first genuinely verified, legally suitable complete collection exists; add `['undergraduate','Undergraduate']` to `TABS`. This app currently hides tabs with no collections.
7. Update `metadata/collections.json`, statement-level topic overrides, `docs/topic-review-progress.json` and regenerate all `metadata/runtime/*` via `python scripts/build_runtime_metadata.py`; run full data, topic, DNA, Node/Python test suite and Pages deployment checks. A JSON-only addition fails CI (demonstrated by Estonia 1997).
8. Preserve the existing grid and search behavior. Do not change the number of **countries** when adding university competitions unless the country counting semantics are deliberately reviewed.
9. Split historical completeness from source-fidelity verification: the presence of a year is not proof all exam rounds were collected.
10. Preserve no-paywall-bypass source retrieval and do not generate missing figures from guesses.

## Verified source discovery (not statement certification)
- MAA archive advertises Putnam problems and solutions links for recent years: https://maa.org/maa-putnam-archive/
- Official IMC site shows 2026 and annual archive from 1994 onwards with distinct day-1/day-2 question PDF links: https://www.imc-math.org.uk/?item=problems
- IMC example 2025 Day 1: https://imc-math.org.uk/imc2025/imc2025-day1-questions.pdf
- IMC example 2025 Day 2: https://www.imc-math.org.uk/imc2025/imc2025-day2-questions.pdf
- MAA example 2024 Putnam statement PDF: https://maa.org/wp-content/uploads/2026/02/2024-Putnam-Problems.pdf

## Next verified implementation unit
First obtain use/attribution permissions and original papers; then ingest **one complete Putnam edition and one complete IMC edition** including source IDs and all metadata. Run CI on a feature branch before merging to main, leaving the existing National grid intact.

This document is a prepared implementation protocol, not a claim that the Undergraduate tab or any Putnam/IMC statements are live.
