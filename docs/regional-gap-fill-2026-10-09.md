# Regional coverage repair — 9 October 2026

66 added/restored statements, six source figures, and two existing Cono Sur records/issues repaired. No new grid rows or layout changes.

| Collection | Added full years | Restored individual statements | Current coverage |
|---|---|---|---|
| Iberoamerican OIM | 2005, 2006, 2007 (18) | 1992 P2/P4, 1993 P6, 1994 P6, 1995 P2 (5) | 41 editions, 246 statements; 1985 and 1987–2026 |
| Cono Sur | 1991, 2007, 2015 (18) | None; the first edition was moved from 1988 to 1989 | 37 editions, 222 statements; 1989 and 1991–2026 |
| OMCC | 2007, 2024, 2025, 2026 (24) | 2017 P1 (1) | 28 editions, 168 statements; 1999–2026 |

No OIM was held in 1986. No Cono Sur was held in 1990. Coverage refers to the held editions, not every calendar-year cell. It does not certify mathematical correctness or independently verified solutions.

## Sources and exact locations

- OIM 2005: [UAN official day 1](https://oc.uan.edu.co/images/Olimpiadas/XXOIM/documentos/PruebaDia1XXOMCC2005.pdf) and [day 2](https://oc.uan.edu.co/images/Olimpiadas/XXOIM/documentos/PruebaDia2XXOMCC2005.pdf), PDF page 1 each. The filenames say OMCC, but both headers identify the XX Iberoamerican Olympiad, Cartagena, September 2005.
- OIM 2006: [OBM Eureka 25](https://www.obm.org.br/content/uploads/2017/01/Eureka_25.pdf), PDF pages 20–21. P2 uses [official OMM Avanzado 21](https://www.ommenlinea.org/wp-content/uploads/practica/folletos/Avanzado_21.pdf), PDF pages 29–30, because Eureka omits absolute-value bars. The Spanish booklet confirms both the bars in P2 and the signs `2a+1`, `2b−1` in P4.
- OIM 2007: [OBM Eureka 29](https://www.obm.org.br/content/uploads/2017/01/eureka_29.pdf), PDF pages 9–11. P4 is a 19×19 board and a (4,1) jump; its figure is included. P3 asks for a winning strategy for team B.
- OIM 1992 P2/P4, 1993 P6, 1994 P6 and 1995 P2: [Universidad de Jaén institutional archive](https://web.ujaen.es/eventos/omatematica/preparacion/competiciones.php?comp=4), respective year pages. These are clean Spanish statements with explicit LaTeX, resolving the lost interval inequality, recurrences, mutual set definition, index ranges and root indices. Source checks explicitly identify HTML, not original exam PDFs.
- Cono Sur 1991: [working OBM PDF](https://www.obm.org.br/content/uploads/2018/01/conesul91.pdf), pages 1–2. The archive's `.doc` link fails; `.pdf` exists. Its P4 board and toggle examples and P5 diagram are included.
- Cono Sur 2007: [OBM Eureka 27](https://www.obm.org.br/content/uploads/2017/01/eureka_27.pdf), P1–P6 on PDF pages 3, 4, 5, 6, 7–8 and 9.
- Cono Sur 2015: [OBM Eureka 39](https://www.obm.org.br/content/uploads/2017/01/eureka39.pdf), PDF pages 9–10. P6 asks for the existence of two friend subsets with at least 738 elements each; it does not assert that all friend subsets have that size.
- OMCC 2007: [official OMM Avanzado 22](https://www.ommenlinea.org/wp-content/uploads/practica/folletos/Avanzado_22.pdf), PDF pages 28–29 (printed 16–17). Introductorio 22 does not contain these examination statements.
- OMCC 2024: [host committee report, Revista Aleph](https://matematicasaleph.com/wp-content/uploads/2024/11/rma-v10-199-218-1.pdf), PDF pages 19–20 (printed 217–218). The exam pages are raster images and were read visually. Days 1 and 2 are dated October 14 and 15, 2024.
- OMCC 2025: [Universidad de Jaén institutional archive](https://web.ujaen.es/eventos/omatematica/preparacion/competiciones.php?comp=12&a=2025), days December 9–10, with both P3/P4 diagrams. The official Costa Rican host page could not be retrieved in this environment; these six checks clearly identify the institutional HTML source.
- OMCC 2017 P1: [Universidad de Jaén institutional archive](https://web.ujaen.es/eventos/omatematica/preparacion/competiciones.php?comp=12&a=2017), including the missing hexagonal triangular-grid figure. Previous Tzaloa/MURO sources lacked that figure.
- OMCC 2026: [official Durango day 1](https://omcc.ommenlinea.org/api/examen/file/wDRrEA/OMCC_2026_D1.pdf) and [day 2](https://omcc.ommenlinea.org/api/examen/file/MT0ofH/OMCC_2026_D2.pdf), PDF page 1 each, August 10–11, 2026.

Every new/restored record has its complete reviewed statement, SHA-256, date, source URL, document hash and figure hashes in `metadata/collections.json`. HTML checks use `source_page: 1` for their single document; this convention is stated in their scope. There are 12 institutional-archive checks (five older OIM statements, six OMCC 2025 statements, one OMCC 2017 statement). Other new checks use official olympiad publications/exam PDFs. All PDF statement pages and attached figures were inspected visually. Added/restored statements also received thematic review.

## Existing Cono Sur corrections

1. The first edition was incorrectly stored as **1988** because of the header in `conesul88.pdf`. The [official OMA first-edition page](https://www.oma.org.ar/enunciados/con1.htm) and [official 2026 host history](https://www.ompucp.org.pe/conosur2026/historia.html) both give **Uruguay 1989**. They identify the same six problems, including the unchanged request to calculate `f(1988)` in P3. The existing year block and all six check/topic identifiers were moved to 1989; no duplicated edition was added. The host history confirms no edition in 1990.
2. **2009 P5:** the [original Spanish OMA page](https://www.oma.org.ar/enunciados/con20.htm) simply says choose `k ∈ A` and then choose `k` entries of S. It has neither the erroneous OBM parenthesis `k = 1001` nor the previous editorial `k ≤ 1001`. The unsupported parenthesis was removed, and the source check was replaced by evidence from the Spanish original. This resolves the pending confirmation item.

## Figures

- `images/oim_2007_p4_fig.png` — cropped from Eureka 29 p10.
- `images/cono_1991_p4_fig.png` — source board and source toggle examples, combined from the two exam pages.
- `images/cono_1991_p5_fig.png` — cropped from the official PDF p2.
- `images/omcc_2017_p1_fig.png` — downloaded unchanged from Jaén problem image 2147.
- `images/omcc_2025_p3_fig.png` — downloaded unchanged from Jaén problem image 2782.
- `images/omcc_2025_p4_fig.png` — downloaded unchanged from Jaén problem image 2783.

## Validation

Data/provenance, topics and DNA validators; Python unit tests; all Node tests; runtime metadata regeneration and freshness check. Runtime manifest counts are OIM 246, Cono Sur 222 and OMCC 168. Whole bank: 19,491 stored records; 5,041 source checks; 14,450 still require source comparison. Source fidelity and coverage are distinct from solution certification.
