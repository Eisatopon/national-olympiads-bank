# Israel Grossman — official archive import, 10 October 2026

Added **162 English statements in 23 complete high-school papers, 2004–2026**, as a separate Israel Grossman row (`ilg`). No examination day field: each year is one paper. Nine statement diagrams accompany the collection: eight official PDF crops at 250 dpi and one faithful vector redraw of the 2025 P2 example with English labels. Junior papers and printed hints, answers and solutions are excluded. The 2020 and 2021 papers each have nine multiple-choice questions; all ten choices per question are retained.

The existing grid behaviour is retained. A country is not added: Israel already has a Gillis row.

## Primary sources and archive repair

- Current Technion archive: https://noam-math.technion.ac.il/questions-and-results-grossman/
- Older Technion archive: https://noam-math.net.technion.ac.il/grossman/
- Official competition description: https://noam-math.technion.ac.il/grossman/

All 50 unique PDF targets from the current archive were inventoried: 47 retrieved and three failed targets. The old official archive supplies the correct 2008 and 2011 papers, the 2006 official publication with full problem restatements, and the 2023 question paper. Current 2023 question links incorrectly target a winners report. Original questions-only publications from the old archive were preferred for 2020 and 2021. The import ledger records the selected source URL, original PDF SHA-256, statement SHA-256, page, problem number and figure evidence per record.

The 2005 archive label follows the Hebrew school-year ending year: its cover gives **9 December 2004**. The distinct 2004 archive paper is dated **17 May 2004**. The 2008 cover gives **2 March 2008**, despite a misleading embedded document name. The 2025 publication has a date placeholder and mentions 2026 guests in P2; its assignment is supported by the official 5785 archive row and the official 5785 winners notice, rather than by that problem's number. The 2026 senior paper is dated **4 September 2026**.

| Years | Problems per paper |
|---|---:|
| 2004–2008 | 7 |
| 2009–2010 | 6 |
| 2011–2015 | 7 |
| 2016 | 6 |
| 2017–2019 | 7 |
| 2020–2021 | 9 |
| 2022–2026 | 7 |

## Source fidelity and visible notes

Every statement page was inspected visually against the English transcription; formulas were not accepted solely from extracted text. The second pass repaired draft translation errors before publication, including the tenfold lap time and obtuse angles in 2004, and distinct initial raven locations in 2008. The 2023 P5 recurrence is the printed fraction `a_n(a_n-1)/2`, not the garbled extracted expression.

**154 records have exact-source comparisons. Eight records remain without exact-source badges**, with their qualifications visible beside the statement:

| Problem | Qualification |
|---|---|
| 2008/7 | Unbound `x` in the first condition restored to the quantified variable `a`; editorial correction, not an official erratum. |
| 2009/4 | Hebrew containment counts explicitly translated as “at least”; cardinality interpretation disclosed. |
| 2009/6 | Nonempty clubs required in both parts; the source only states this explicitly in part (b). |
| 2010/3 | Zero-degree angles permitted to cover collinear point sets. |
| 2013/6 | Source leaves region-boundary and line-orientation conventions unspecified; wording retained and ambiguity disclosed. |
| 2021/8 | Domain `n >= 3` made explicit. The source leaves the comparison of answer expressions for small `n` versus a uniform/asymptotic comparison unspecified; this ambiguity remains disclosed. |
| 2025/5 | Shorter-arc distance made explicit; metric missing from the statement's wording. |
| 2026/4 | Confirmation of the correct ranking counted as success; candidate elimination applies to a disagreement response. |

2011/6 follows the authors' **official corrected restatement on page 3**, replacing `10^20 - 1` by `10^20 - 9`. This record has an exact-source check against the corrected restatement and a visible note explaining the correction.

These are AI-assisted source-fidelity checks, not independent mathematical solution verification. In particular, retaining a complete published paper does not resolve an ambiguity that remains in its original wording.

## Remaining historical coverage

The accessible old and current Technion exam archives start at the 2004 school-year paper. The competition itself dates back to 1960. Targeted English and Hebrew searches did not recover dated complete pre-2004 high-school papers in this pass. **Pre-2004 remains open**, rather than being declared complete or populated with isolated problems. This Grossman addition does not close the separate Gillis historical gaps or the unretrieved complete Israel IMO-TST seasons.

Cyprus and Estonia remain next in the owner's agreed country order after the remaining Israel source work.

## Validation

Passed: bank data validation (115 collections), thematic review validation (20,656 records), Problem DNA validation, all 11 Python unittests, all seven Node suites, generated runtime freshness and git diff whitespace checks. No original-source badge is inferred merely from downloading a PDF.
