# Undergraduate section — completeness and source-check audit (13 Oct 2026)

| Row | Stored | Coverage | Source checks (badges) |
|---|---|---|---|
| Putnam | 1,063 | 1938–2025 complete; no competition 1943–1945 | 1,063 (331 of 1938–1964 compared with the reworded Scholes archive, flagged "original wording not verified") |
| IMC | 354 | 1994–2026 complete | **354 (new)** |
| Vojtěch Jarník | 261 | 1991–2026 complete; no edition 2020, 2021, 2023 | 261 |
| Simon Marais | 88 | 2017–2025 complete | 88 |
| SEEMOUS | 80 | 2007–2026 complete | **12 (new: 2020, 2024, 2026)** |
| Miklós Schweitzer | 475 | 1949–1961, 1987, 1995, 1997–2025 | 475 |

## IMC
- All 63 official organiser PDFs (imc-math.org.uk) downloaded; every statement re-compared word by word with the PDF text layer (ligature-tolerant); all discrepancies inspected.
- **136 statements carried a proposer credit** ("(Proposed by …, University)", or a bare name/affiliation line in 2020) copied from the solution sheets; the official question papers do not contain it. Moved to a separate `proposer` field.
- 13 displayed formulas written as inline `$\tag{n} …$` (and two `align*` blocks) converted to proper display math; one `&amp;` fixed; 2010 P6 "(5 points)" removed (not on the source).
- Remaining text differences are only spelling/hyphenation (non-negative/nonnegative) or PDF glyph defects (2014 sheets drop the letter "c").
- Source checks: `metadata/imc-statement-checks.json` (URL, page, PDF SHA-256, statement SHA-256).

## SEEMOUS
- 2020, 2024, 2026: the stored texts were condensed paraphrases; replaced by the official wording of the contest papers, formula by formula, with source checks (`metadata/seemous-statement-checks.json`).
- Other years come from secondary compilations (SSMR Gazeta reprints, a University of Patras course archive, matematickitalent.mk, Scribd, a user-supplied compilation) and stay without original-source badges. The MASSEE 2007–2014 collection is no longer on massee-org.eu and the Internet Archive is not reachable from the cloud session.

## Open items
- SEEMOUS 2007–2019, 2021–2023, 2025: find the official papers (organiser sites, MASSEE newsletters) and re-transcribe; the stored texts may be paraphrased like 2020/2024/2026 were.
- Literal TeX quotes ``…'' in prose (shown as backticks on the site) remain in 38 older statements: Sweden 12, Portugal 12, Putnam 6, Brazil 3, Netherlands 3, Spain 2. Fixing them changes the statement fingerprints, so the source checks and topic records must be updated together.
