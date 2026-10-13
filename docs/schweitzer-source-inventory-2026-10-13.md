# Miklós Schweitzer Memorial Competition — verified source inventory

Date: 2026-10-13. Scope: undergraduate expansion **source discovery**, not statement publication. No problems have been transcribed or certified by this inventory.

## Primary sources

- János Bolyai Mathematical Society, official competition and papers: https://www.bolyai.hu/versenyek-schweitzer-miklos-emlekverseny/
- University of Szeged (M. Maróti), historical PDF index: https://www.math.u-szeged.hu/tagok/mmaroti/schweitzer/index.html

The society's official page provides recent annual papers (including English-language 2024 and 2022 papers), and historical annual links for 2009–2020. The university index lists English editions for 2000–2004, 2007–2010, 2012–2020, and 2022, and additional Hungarian PDFs for multiple years; check exact years at the source page rather than inferring continuous coverage. Earlier competitions require primary publications or independent archive checking: *Contests in Higher Mathematics, Hungary 1949–1961* (1968), and *Contests in Higher Mathematics: Miklós Schweitzer Competitions, 1962–1991* (1995).

### 2026 classification warning

The society explicitly states that **there is no official competition or awards in 2026**. Instead it announced a mathematical problem-solving programme. Do not import it as a normal 2026 competition paper.

## Import gates (required before exposing a new Undergraduate grid row)

1. Acquire the original annual problem-only PDF (or visually isolate statements from a source with solutions).
2. Preserve all assumptions, notation and diagrams; translate Hungarian faithfully to English and verify against the visible PDF pages.
3. Complete an entire annual set, not isolated exercises. Flag every unavailable year explicitly; never fabricate continuous coverage.
4. Write `undergraduate/Schweitzer-problems.json` using the existing competition/year/problem schema.
5. Add full source and verification provenance to the metadata catalog; integrate the new row into the existing Undergraduate grid only when at least one full year has been verified.
6. Rebuild runtime metadata, run Python and Node validation, inspect rendered MathJax and figures, then publish and confirm GitHub Actions and Pages.

**Status as of 2026-10-13:** Official sources identified and inventoried. Source PDFs were not accessible to this work session for reliable line-by-line and diagram verification. Consequently no contest problems have been published and no new grid row has been added. This document deliberately does not assert completeness.


## Chronological source acquisition update (13 October 2026)

**Start year: 1949, not 2022.** The complete 2022 translation remains a separate staged draft and is not evidence of complete historical coverage.

- **1949–1961 primary edited book, digitized by the Library and Information Centre of the Hungarian Academy of Sciences**: https://real-eod.mtak.hu/14558/1/AkademiaiKiado_007070.pdf — *Contests in Higher Mathematics, Hungary, 1949–1961: In Memoriam Miklós Schweitzer* (Akadémiai Kiadó, 1968; English). This is the identified primary source for the first chronological batch. The PDF is approximately 79 MB and could not be downloaded in the current execution environment. Its individual formulas and problem counts have therefore **not** yet been verified.
- **1962–1991 follow-on volume**: https://link.springer.com/book/10.1007/978-1-4612-0733-7 — *Contests in Higher Mathematics: Miklós Schweitzer Competitions, 1962–1991* (1995), with a separate chapter *Problems of the Contests*, pp. 1–48.
- **1992 onward**: https://www.math.u-szeged.hu/tagok/mmaroti/schweitzer/index.html — annual original papers and English editions where available. This list is not evidence of uninterrupted coverage.

**Publication gate:** do not present any 1949–1961 questions as source-checked until the actual source PDF has been read and mathematical typesetting and diagrams compared against the pages. No year-to-year leap or placeholder collection is authorized.

## 1950 special handling — two rounds (verified from introductory historical volume)

The historical 1949–1961 volume explicitly states that the poor results of the first **1950** four-hour contest led to a separately announced **Second Round** with modified rules, still in 1950. For import, keep both as distinct sessions (`day: 1` and `day: 2`, with documented day/session meaning) under the same year; do not treat an independently found 9-question compilation as necessarily covering both rounds. Source: https://real-eod.mtak.hu/14558/1/AkademiaiKiado_007070.pdf, introductory historical text around printed page 8. Actual complete problem lists for both rounds are **not yet verified**. Do not publish a 1950 grid year until the original source pages have been checked visually.


## PRIMARY HISTORICAL VOLUME NOW ACCESSIBLE — 2026-10-13

The owner supplied the **complete legible 76 MB original English 1968 volume**, `AkademiaiKiado_007070.pdf` (268 PDF pages). Earlier assertions that the source cannot be opened are now **obsolete**. The original PDF has been opened and its chapter and historical totals directly inspected.

- Book, Chapter 1 **Problems of the contests**: printed pp. 11–32; **PDF pages 15–36** (22 pages); statements appear in chronological order. Chapter 2 begins PDF page 37.
- Chapter 2 **Results of the contests**: printed p. 33; **PDF page 37**. Authoritative full year counts:
  - 1949: 8
  - 1950/I: 10; 1950/II: 9 (**19 combined**, preserve rounds)
  - 1951: 17
  - 1952: 10
  - 1953: 10
  - 1954: 10
  - 1955: 10
  - 1956: 10
  - 1957: 10
  - 1958: 11
  - 1959: 10
  - 1960: 10
  - 1961: 10
  - **TOTAL: 145 numbered statements in 1949–1961**.

Statements continue across page boundaries. The source has been split locally into (a) a 22-page questions-only PDF, (b) per-year smaller PDFs that may overlap where years share a page, and (c) a machine-readable source index. Those locally generated files are not yet committed into this repository.

**IMPORTANT: Counts and page provenance are now checked from the primary volume; this does not automatically authenticate previously staged secondary-source statement transcriptions.** Re-compare 1949 and 1950 DRAFT JSON word-for-word/formula-for-formula against the visible 1968 pages, including a missing 1950/II problem 2 modulus restriction and precise expressions. Likewise, the 1951 source audit is superseded for source accessibility but does not constitute a completed full-text import. Do not publish until mathematical transcription QA, full-year checks and CI.
