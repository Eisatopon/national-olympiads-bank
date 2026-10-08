# MEMO — check against the official problem sheets (8 Oct 2026)

Sources:
- Official English sheets (individual and team) from the Školjka archive: https://dev.skoljka.org/archive/memo/. These cover 2009–2011, 2013, 2015, 2016 and 2018–2025.
- 2017: the official "Contest problems with solutions" booklet, from https://skmo.sk/dokument.php?id=3907.

Every stored statement for these years (172 problems) was compared with the sheet in three passes:
- **Words:** an automatic word-level diff.
- **Numbers:** a comparison of the numbers in each problem.
- **Symbols:** a comparison of the letters inside the formulas.

Every mismatch was then checked by hand. A `statement_checks` record was written for each of the 172 problems, including the sheet's SHA-256 and the page.

## Changes (34 statements)

**Official wording restored (32).** The AoPS paraphrases were replaced by the sheet text:
- 2013: T-2
- 2016: I-1, I-2, I-3, T-1, T-2, T-4, T-5, T-6, T-7, T-8
- 2019: I-1, I-2
- 2022: I-1, I-4, T-3, T-4, T-7, T-8
- 2023: I-1, I-2, I-3, I-4, T-1, T-2, T-3, T-6
- 2024: I-1, I-2, I-4
- 2025: I-1, T-8

Substantive fixes among these:
- 2022 T-7 and 2023 T-1(b): the AoPS text wrote $\mathbb{N}$ without saying it means the positive integers. The official text defines the domain.
- 2024 I-2: the AoPS text added "rectangular" and "independent of the choice of the polygon", which are not in the official text.
- Restored the official remarks that AoPS had dropped:
  - definitions of gcd/lcm, chord, bishop attack, adjacency, $A$-excircle, $\mathbb{N}_0$, and iterated functions;
  - the examples in 2022 T-3 and T-8.

**Official figures added (2).**
- 2018 I-2: the two staircases. Before this, they were only described in words.
- 2025 T-3: the snake example in a $4\times4$ grid.

The figures are in `images/memo_2018_p2_fig.png` and `images/memo_2025_p7_fig.png`.

## Checked and left unchanged
The remaining 138 statements agree with the sheets. They differ, if at all, only in British vs American spelling or trivial wording, for example $2^2$ written for $4$ in 2020 T-4.

The 2015 T-4 example figure was not added. The problem text is complete without it.

## Not checked
2007, 2008, 2012, 2014 and 2026: no official English sheet was found online. The archived 2012 (imosuisse.ch) and 2014 (memo2014.de) PDFs could not be retrieved from the Wayback Machine. These 60 problems remain AoPS-only and unverified.

A source check confirms that the stored text matches the official sheet. It does not certify that the problem is mathematically correct.
