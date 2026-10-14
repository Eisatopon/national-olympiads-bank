# Estonia: final round and IMO TST checked against the official archive (14 Oct 2026)

Sources (University of Tartu olympiad archive, all downloaded and fingerprinted):
- Estonian papers: final round `https://math.olympiaadid.ut.ee/arhiiv/loppv/` (lpYYest.pdf 1993–2009, lpYYYY.pdf 2007–2026, Grade 12 paper) and selection contest `https://math.olympiaadid.ut.ee/arhiiv/valik/` (vvYYest.pdf 1993–2011, vvYYYY.pdf 2006–2025, additional round tvvYYYY.pdf 2015–2025).
- Official English booklets "Estonian Math Competitions" `https://math.olympiaadid.ut.ee/eng/archive/probYYZZ.pdf` (1992/93–2024/25): all selection-contest problems from 2001 on (and 1996), selected final-round problems.

Method: every stored statement was compared with the page image of the official paper. The official English booklet wording is used wherever the booklet prints the problem; otherwise the Estonian paper was translated faithfully. Per-problem ledger (identity, old identity, action, source file, page, printed number, change): `docs/estonia-official-check-2026-10-14.json`.

## Final round, Grade 12 (key `ee`)
1993–2026, 5 problems every year, 170 statements, all complete (no additions needed).
- 124 now carry the official booklet wording; 46 are translations of the Estonian paper (years without a booklet: 1995, 1997, 1998, 2000, 2026, and problems the booklet omits).
- Real errors fixed: 1996 P2 (only the last term is divided by x), 2013 P5 (both students know the tasks), 2018 P5 ("either solution"), 2023 P4 (the chairman decides), 2024 P1 (snail shells, not tea cups), 2024 P5 (coprime to the number two positions away), 2026 P3 ("nice", not "proud").
- Definition notes printed on the Estonian paper but omitted by the booklet are kept as a "Note." paragraph (2015 P4, 2020 P2, P3, 2023 P1, P2, 2024 P5; 1999 P3).
- Notes: 1993 P3 source ambiguity; editorial corrections of booklet misprints in 1994 P2, 2001 P3, 2014 P1, 2020 P4 (no source-check badge).

## IMO team selection contest (key `eet`)
1993–2025 complete, 264 statements (was 171): two days of three problems each year; from 2015 also the additional selection round (täiendav valikvõistlus) as days 3–4 (12 problems/year).
- Added 93: whole years 1993, 1994, 1995, 1998, 1999, 2000 and 2006 (translated from the Estonian papers; the early booklets do not contain the selection contest), and the missing problems of 2018–2025 (51; the stored data held only the booklet's selected problems).
- Day/number structure corrected: 1996–1997 had no day; 2015–2017 were two days instead of four; 2018–2025 had no day and wrong numbering.
- Errors fixed: 1997 P3 (seated along the wall of a circular hall), P4, P5 (rectangles erected outwards), P6 (k vs n); 2016 P9 (less than √n).
- Notes: 2002 P1, 2016 P10, 2025 P1 source ambiguity (booklet vs Estonian paper, kept as printed); editorial corrections in 1998 P6, 2015 P4, P6, P9, 2016 P4 (no badge).
- Three new figures cropped from the papers: `estoniatst_1994_p1_fig.png`, `estoniatst_1998_p6_fig.png`, `estoniatst_2006_p3_fig.png`.
- Not yet available: the 2026 selection contest papers are not published in the archive.

## Source checks
425 of the 434 statements carry source checks (`metadata/collections.json`); the 9 with editorial corrections carry notes instead. Topic records: 93 new reviews; changed statements keep their earlier reviews as superseded snapshots; moved identities were relabelled in the historical topic-audit files (same review, same statement hash).
