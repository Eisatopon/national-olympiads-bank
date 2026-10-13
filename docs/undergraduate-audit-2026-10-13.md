# Undergraduate section — completeness and source-check audit (13 Oct 2026)

| Row | Stored | Coverage | Source checks (badges) |
|---|---|---|---|
| Putnam | 1,063 | 1938–2025 complete; no competition 1943–1945 | 1,063 (331 of 1938–1964 compared with the reworded Scholes archive, flagged "original wording not verified") |
| IMC | 354 | 1994–2026 complete | **354 (new)** |
| Vojtěch Jarník | 261 | 1991–2026 complete; no edition 2020, 2021, 2023 | 261 |
| Simon Marais | 88 | 2017–2025 complete | 88 |
| SEEMOUS | 80 | 2007–2026 complete | **20 (2018, 2020, 2022, 2024, 2026)** |
| Miklós Schweitzer | 475 | 1949–1961, 1987, 1995, 1997–2025 | 475 |

## IMC
- All 63 official organiser PDFs (imc-math.org.uk) downloaded; every statement re-compared word by word with the PDF text layer (ligature-tolerant); all discrepancies inspected.
- **136 statements carried a proposer credit** ("(Proposed by …, University)", or a bare name/affiliation line in 2020) copied from the solution sheets; the official question papers do not contain it. Moved to a separate `proposer` field.
- 13 displayed formulas written as inline `$\tag{n} …$` (and two `align*` blocks) converted to proper display math; one `&amp;` fixed; 2010 P6 "(5 points)" removed (not on the source).
- Remaining text differences are only spelling/hyphenation (non-negative/nonnegative) or PDF glyph defects (2014 sheets drop the letter "c").
- Source checks: `metadata/imc-statement-checks.json` (URL, page, PDF SHA-256, statement SHA-256).

## SEEMOUS
- 13 Oct 2026, organizers' wording for the remaining 64 statements: the NKUA course file `Seemous-2007-2025.pdf` (https://eclass.uoa.gr/modules/document/file.php/MATH206/%CE%98%CE%AD%CE%BC%CE%B1%CF%84%CE%B1%20SEEMOUS/Seemous-2007-2025.pdf, sha256 f4e4997c…, 75 pages; the same file the owner supplied) is a merge of the organizer documents of each year (problem sheets or problems-with-solutions; 2019 sheet from Devin on p. 34; 2021 English paper on p. 40). Every statement of 2007–2017, 2019, 2021, 2023, 2025 was re-transcribed from the page images, replacing the condensed paraphrases; secondary compilation, so no badges. 2018 comes from the official paper on the Iasi host (math.etti.tuiasi.ro/seemous2018, reachable only through the browser) with source checks. 2012 P2: the source figure is cropped from p. 16 (replaces the schematic SVG reconstruction). Notes: 2017 P2 b) editorial correction (the sheet omits the factor ε that its own solution uses); 2014 P2 source ambiguity (recurrence printed for n ≥ 2). 2021 P1 follows the English paper ("strictly increasing"), not the Gazeta report. The mathematica.gr SEEMOUS tag (owner's link) holds only forum retypings and the SSMR Gazeta reports are in Romanian, so neither was used as wording source.
- 2020, 2022, 2024, 2026 (2022 from the organiser site poincare.matf.bg.ac.rs/~kmiljan/SEEMOUS): the stored texts were condensed paraphrases; replaced by the official wording of the contest papers, formula by formula, with source checks (`metadata/seemous-statement-checks.json`).
- Other years come from secondary compilations (SSMR Gazeta reprints, a University of Patras course archive, matematickitalent.mk, Scribd, a user-supplied compilation) and stay without original-source badges. The MASSEE 2007–2014 collection is no longer on massee-org.eu and the Internet Archive is not reachable from the cloud session.

## Open items
- SEEMOUS: the official papers of 2007–2017, 2019, 2021, 2023, 2025 are still not online at their hosts (the 2025 host seemous.site is blocked from the cloud). Their texts now follow the organizers' wording (see below) but have no original-source badge.
- Done 13 Oct 2026: literal TeX quotes ``…'' in 21 older statements (Sweden, Portugal, Putnam, Brazil, Netherlands, Spain) replaced by typographic quotes; Putnam checks and topic records updated (previous text kept as superseded snapshots).
