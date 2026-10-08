# Iberoamerican Mathematical Olympiad (OIM), 1985–2026 (8 Oct 2026)

New regional row, key `oim`, file `Iberoamerican-oim-problems.json`, continent group *americas*.
There are 223 problems in 38 years: 1985, 1987–2004 and 2008–2026. Each year has 6 problems: day 1 is P1–P3 and day 2 is P4–P6.

## Sources
AoPS is unreachable from the build environment. Every statement was therefore translated into English from an official-language text published by an olympiad organisation:

| Years | Source |
|---|---|
| 1985, 1987–1997 | Olimpíada Matemática Argentina, `oma.org.ar/enunciados/ibe1.htm` … `ibe12.htm` (Spanish). Checked against the archived official OEI pages (`oei.es/oim/ioim.htm` …). Formula images were read from the GIFs, and symbol-font glyphs were decoded (`³` = ≥, `£` = ≤, `¹` = ≠). |
| 1998–2003, 2008, 2011, 2012, 2014, 2016–2026 | Portuguese papers published by the OBM (`obm.org.br`, Provas e gabaritos). The 2026 paper is a scan and was read from the page images. |
| 2004 | Official OEI papers `xixd1.PDF` and `xixd2.PDF` (archived). |
| 2009, 2010, 2013, 2015 | *Revista Tzaloa* of the Olimpiada Mexicana de Matemáticas (issues 1/2010, 1/2011, 1/2014 and 1/2016). |

A `statement_checks` record was written for all 223 statements. Each record holds the source URL, the page, the document SHA-256 and the figure hashes.

## Gaps
- **1986**: there was no OIM that year. The II OIM was held in January 1987.
- **2005–2007**: no official text has been found online yet. OEI stops at 2004 and the OBM archive has no paper for these years. These years can be added later from AoPS once the text can be pasted in.
- **Omitted problems** (listed in `KNOWN_GAPS` and in `missing_problem_numbers`). Every surviving text of these problems is corrupt, so they were left out instead of being guessed:
  - 1992 P2: the inequality defining the intervals is lost ("formed by all x = 1").
  - 1992 P4: the recurrences are missing, and the text runs into the statement of 1991 P4.
  - 1993 P6: self-contradictory ("B is the set of all numbers that are 'cuates' of all elements of B").
  - 1994 P6: the index condition is corrupt (`0 ≤ s , i`).
  - 1995 P2: the exponents are ambiguous.

## Source slips corrected (also noted in the scope of each check)
- 1985 P6: the formula image reads `1/CE`. It should be `1/CF`, the cevian through C.
- 1989 P1: the source prints `k²` in the second equation. Corrected to `y²`.
- 1990 P1: the index variable clashes with `n`. Renamed to `j`.
- 1993 P1: the source defines `y_{i+1} = x_{i+1} − x_i`. Restated as `y_i = x_{i+1} − x_i`.
- 1997 P3: the symbol-font glyph decodes to `n ≤ 2`. Corrected to `n ≥ 2`.
- 2000 P1: the OBM paper lost the symbol in `n > 3`. Restored from OEI.

## Figures
- `images/oim_1992_p6_fig.png`: from the OMA page.
- `images/oim_1996_p5_fig.png`: from the OMA page.
- `images/oim_2009_p1_fig.png`: from Tzaloa.
- `images/oim_2025_p2_fig.png`: from the OBM paper.

A source check confirms that the stored translation matches the official text. It does not certify that the problem is mathematically correct.
