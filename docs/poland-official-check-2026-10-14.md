# Polish MO final round — official source check (14 Oct 2026)

Collection: `Poland-pmo-problems.json` (key `pl`), final round (zawody stopnia III), 1950–2026.
Per-problem record: `docs/poland-official-check-2026-10-14.json`.

## Sources (all official, Polish)
- 1950: scanned report of the Main Committee, *Pierwsza Olimpiada Matematyczna — Sprawozdanie Komitetu Głównego* (PTM, 1951), pp. 119–132 (`om1_3r.pdf`, attached to archom node 194).
- 1951–1995: Polish Mathematical Society olympiad archive, archom.ptm.org.pl (one node per problem, III etap pages).
- 1996–2026: official problem sheets of the Main Committee, om.sem.edu.pl/static/app_main/problems/omNN_3.pdf (1999 from `om50_3r.pdf`, problems with solutions; solutions ignored); archom used as a second source up to 2009.

Review method: AI-assisted visual and textual comparison of the English statement with the Polish original; not an independent mathematical or human certification.

## Result
- 455 stored statements (was 444): 378 verified unchanged, 66 corrected to faithful translations, 11 added.
- Added: 1952 complete (6), 1965 P1–P5. 1965 P6: the official archive node 1386 (XVI OM, III etap, Zadanie 6) has an empty body and no attachment holds the paper; recorded in `missing_problem_numbers`.
- 2020: no final round (COVID-19) — confirmed by the committee record `om.sem.edu.pl/static/app_main/previous_olympiad/71/71OM.json` ("brak finału").
- 448 source checks; 7 statements carry an *Editorial correction* note (misprint in the archive resolved from the archive's own solution) and therefore no exact-source check: 1967 P4, 1969 P3, 1975 P5, 1975 P6, 1976 P2, 1989 P6, 1995 P5. 14 further notes record archive OCR/LaTeX slips (Source ambiguity / Source note) where the stored reading follows the official solution.

## Real errors fixed (previous AoPS-derived text)
1950 P5 (implication, not iff); 1959 P1 (any numbers, not non-negative), P3 (path not restricted to the surface); 1967 P3 (mutual acquaintance); 1968 P4 (natural numbers), P6 (exactly k neighbours); 1970 P2 (natural terms); 1971 P2 (finitely many directions), P4 (strict min(x,y) > n), P6 (infimum distance); 1972 P1 (n > 2), P4 (equivalence), P6 (digit sum tends to infinity);
1973 P5, P6; 1975 P3 (wrong, generalised problem; second question restored); 1976 P4; 1977 P4 (spurious b > 0); 1978 P1, P5; 1979 P5, P6; 1980 P1; 1981 P1 (in space, not in a plane); 1982 P4; 1984 P1, P5 (discs of diameter 1); 1985 P2, 1986 P4 (strict vs non-strict); 1987 P2 (circle of length 1), P3; 1988 P1; 1990 P2, P4; 1991 P3; 1993 P2, P3; 1994 P4 (range and “third vessel”); 1995 P3, P6;
1998 P6 (all vertices with integer coordinates); 1999 P2–P6 (AoPS paraphrase; P5 is about integers, P6 had a different hypothesis and conclusion); 2017 P2 (wording).
Scoring remarks removed from 2021 P6 and 2024 P5. Other corrections restore official notation, part labels or remarks.

## Open points
- 1965 P6 not recoverable from the official archive.
- 1981 P3: the archive prints $\alpha^{n-1}\le x$ (adopted; Source ambiguity note); a printed booklet would settle it.
- 2003: the sheet for day 2 carries a copy-paste header of the second round; archom and `om54_3r.pdf` confirm P4–P6 belong to the final.
