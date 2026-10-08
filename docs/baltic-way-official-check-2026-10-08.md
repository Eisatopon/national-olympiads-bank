# Baltic Way — check against the official problem sheets (8 Oct 2026)

Source: the official English problem sheet of each year, `https://www.georgmohr.dk/bw/bwYYpb.pdf` (1991–2024).
Every stored statement for 1991–2024 (680 problems) was compared with the sheet, using both the PDF text layer and the rendered page image (the 2005 sheet has a broken font, so only the image was used). A `statement_checks` record was written for each of the 680 problems, including the sheet's SHA-256 and the page number.

## Corrections

**Mathematical errors**
- 1994 P3: the square roots were swapped. The stored text had `x√(1−x²)+y√(1−y²)`; the official text is `x√(1−y²)+y√(1−x²)`.
- 2005 P7: the condition was `n ≥ 2`; the official condition is `n > 2`.
- 2005 P2: the official condition is `0 ≤ α, β, γ < 90°`. The stored text said "acute", which excludes 0.
- 1991 P19: the AoPS paraphrase ("interiors have no common point, meet each other …") contradicted itself. It is replaced by the official wording.

**Official wording restored**
- 1991: all statements rewritten from the official sheet. In P3 the dollar signs are written out as "dollars" so they do not clash with the TeX delimiters.
- Also restored: 1995 P20, 1996 P6 ("not a prime"), 2005 P6 (`4·N²/K²`), 2005 P10 (`m = 30030 = 2·3·5·7·11·13`, "minimal integer n"), 2005 P14 (medians meet at `M`, `∠PMQ`), 2023 P11 (with the Remark) and 2023 P15 ("again", "respectively").

**Missing problems added, with figures cropped from the official sheets** (previously listed in KNOWN_GAPS)
- 1996 P2 (three half-circles): `images/bw_1996_p2_fig.png`
- 2008 P14 (4×4×4 cube from 4-cube blocks): `images/bw_2008_p14_fig.png`
- 2018 P9 (Olga and Sasha, hexagonal grid, rhomboid pattern): `images/bw_2018_p9_fig.png`

**Official figures added to existing statements**
- 2007 P7 (squiggle): `images/bw_2007_p7_fig.png`. This replaces a verbal description of the figure.
- 2018 P7 (torus): `images/bw_2018_p7_fig.png`
- 2021 P7 (hexagonal board): `images/bw_2021_p7_fig.png`
- 2017 P6 (jump rule): `images/bw_2017_p6_fig.png`
- 2017 P8 (normal and short knight moves): `images/bw_2017_p8_fig.png`

## Checked and left unchanged
Wherever the stored statement differed from the sheet only in spelling or wording but meant the same thing, it was kept as it is. Examples: British/American spelling, `2/AD = 1/BD + 1/CD` in 1998 P12, and the AoPS forms of 2023 P1–P5, P12–P14 and P16–P19. In 2023 P19 the exponent `2^{2^{2·2023}}` was confirmed on the page image.
The 2017 sheet's text layer is mixed with the solution booklet, so the 2017 statements were checked against the page image. For all other years, the numbers in each statement were also compared automatically with the text layer, and every mismatch was checked by hand (against the page image where the text layer was unclear). All of them turned out to be text-layer artefacts; for example, the 2010 layer lists Problem 9 out of order.

## Not checked
- 1990: no official sheet is available online.
- 2025: bw2025.lu.lv links an "English exam" file, but it is the 2013 Riga paper. These 20 problems remain AoPS-only and unverified.

A source check confirms that the stored text matches the official sheet. It does not certify that the problem is mathematically correct.
