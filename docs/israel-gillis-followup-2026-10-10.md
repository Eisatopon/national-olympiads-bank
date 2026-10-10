# Israel Gillis follow-up — 10 October 2026

Published change: **54 additional statements in six complete stored sets**, plus **11 source figure crops** (four historical and seven in existing modern sets). Gillis now has **275 statements in 40 sets**. No grid layout changes; statements only.

| Added year | Count | Source |
|---|---:|---|
| 1983 | 9 | Weizmann-hosted Hebrew historical compilation |
| 1984 | 10 | same |
| 1985 | 10 | same |
| 1986 | 9 | same |
| 1988 | 8 | same |
| 1995 | 8 | IMO Compendium Group English collection, IsrMO95.pdf |

Historical sources are secondary published collections, not original sheets. All 54 were compared with rendered pages, but **none gets an original-paper badge**. Source URLs and document hashes are in `israel-gillis-followup-additions-2026-10-10.json`.

## Existing stored years checked

All 55 statements in 2011, 2014–2016, 2018, 2022, 2024 and 2025 were visually compared with the Weizmann original papers/publications. **53 receive source checks**. The other two contain explicit domain clarifications: 2014 P6 needs n >= 2, and 2018 P3 excludes the all-zero denominator.

Corrections and clarifications:

- 2018 P2: remove the extra restrictions d != 0 and q not in {0,1,-1}, which are absent from the official definitions.
- 2022 P2: k,m may be zero; only the six numbers used as denominators must be nonzero.
- 2025 P6: restore positive real variables. The corrected second numerator bc+ab+1 is confirmed in the official solutions publication's restatement on page 5. The standalone question sheet prints bc+ca+1, a typographical error. A visible provenance note explains the chosen corrected publication; no solution is copied.
- 2016 P6: clarify that perpendicular feet lie on the lines containing the diagonals; they need not lie on the segments for an arbitrary plane point X.
- 2022 P3: restore the source colour figure so the question identifies which three of the five strips are orange.

Modern source figures added: 2016 P2/P6; 2018 P6; 2022 P3/P5; 2024 P3; 2025 P2. Historical figures: 1983 P9; 1985 P1; 1986 P7; 1988 P7. Figure files and source documents are fingerprinted in provenance records where applicable.

## Historical editorial notes

These records have no original-source badges. Their notes are visible through the app's provenance feature.

- 1983 P5: the area-only escape guarantee needs a no-holes hypothesis. The English version explicitly assumes an open simply connected forest. The printed historical wording omits this; a thin region containing any entire finite prescribed path would otherwise be a counterexample.
- 1983 P9: the distinct circle chain lies in the upper semicircle, as in the source diagram; the construction must not return to an earlier circle.
- 1984 P2: explicitly require positive irrational c. The identity is not valid for arbitrary negative irrational c with ordinary finite-sum conventions.
- 1984 P3: intersections must exist; the conclusion depends on X,A,B,C,D, and is independent only of H,K.
- 1984 P6: a != 0, required by x/a^2.
- 1985 P2: omit the printed inequality hint, retaining only the challenge.
- 1986 P7: clarify the exterior supporting plane and the rays from A in the geometric construction.
- 1988 P4: exclude rotations for which the defining chord lines do not exist or intersect.

## Remaining Gillis gaps and concrete blockers

| Period/year | Evidence and blocker |
|---|---|
| 1968–1970 | No complete usable dated sheets recovered. |
| 1971–1982 | The 118-page Weizmann book was recovered. Its preface says 1971–1982, whereas the archive link labels 1972–1982. It groups problems by topic, not dated exam sets; inspected problem pages give no year labels. Do not invent dated full papers from this book. |
| 1987 | Recovered compilation lists P1–P11. P9 and P11 repeat the same inequality; P8 and P10 are closely related variants. The genuine exam count cannot be certified from this flawed list. No incomplete or guessed set imported. |
| 1989 | All seven entries recovered; P6 is ambiguous about the selected s sets, the global odd-membership condition, and intersection-sum indexing. A faithful unambiguous full set is not established. |
| 2004–2005 | Archive rows have no question link. English filename candidates at IMOmath returned 404; full papers remain unretrieved. |
| 2021 | Existing seven statements retained. No original question sheet in the archive table; this year is not source-checked. |

The standalone 2025 paper's calendar header says 27.11.2023 but its school-year title and the problems refer to 5785/2024. Keep the collection's existing ending-school-year convention; do not silently move the set to 2024 or 2023.

## Israel TST investigation

The [official selection-process page](https://www.weizmann.ac.il/math/IMT/%D7%AA%D7%94%D7%9C%D7%99%D7%9A-%D7%94%D7%9E%D7%99%D7%95%D7%A0%D7%99%D7%9D) explicitly says that delegations are selected using camp selection contests. **Camp examinations must not all be dismissed as mere training**. Conversely, topical worksheets and junior-group papers must not be inserted as senior IMO TSTs.

The official [resources page](https://www.weizmann.ac.il/math/IMT/%D7%9B%D7%9C%D7%9C%D7%99) links to taharut.org. The official year pages 5781, 5782 and 5786 were inspected. The 5782 page lists autumn, winter, spring, summer and September exam packets. In this environment, all six taharut.org year-index requests 5781–5786 returned HTTP 502. The directly linked winter and spring PDFs also failed through web retrieval:

- `https://taharut.org/imo/I5782/Mevhans_5782_2_Winter.pdf`
- `https://taharut.org/imo/I5782/Mevhans_5782_3_Pesakh_cens.pdf`

AoPS leads found: 2016 c422600; 2021 c3053795; 2022 c3048611; 2023 c3316615; 2024 c3525428. Direct printable downloads returned HTTP 403; no anti-bot bypass attempted. Search snippets for **2022 and 2023 explicitly say that tests consisting of IMO-shortlist problems are omitted**, so these cannot certify complete annual TST series. No partial TST row was added.

## Validation

Full data/topic/DNA validators, 11 Python unit tests, all seven Node test files, and generated-runtime checks passed. All 11 new figure crops were visually inspected, including labels and source colour assignments. Source comparison is separate from independent mathematical solution verification. The remaining gaps above mean **Israel is not historically complete**.
