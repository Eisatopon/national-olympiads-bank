# All-Russian MO — official source check (15 Oct 2026)

Collection `Russia-aro-problems.json` (key `ru`). All 289 previously stored statements compared visually (rendered pages, formulas included) with official Russian sources; 1964 added. Per-problem records: `docs/russia-official-check-2026-10-15.json`.

Result: 285 unchanged, 4 corrected, 5 added → 294 statements, 294 source checks.

## Sources
- 1961–1966: Russian original of Vasil'ev & Egorov, *Задачи всесоюзных математических олимпиад* (Nauka 1988), compiled by jury members — https://math.ru/lib/files/djvu/olimp/vsesojuznye.djvu, book pp. 21–34. Top-form row of the grade tables (grade 10 in 1961–62, grade 11 in 1963–65, grades 10–11 in 1966).
- 1993–2005: *Всероссийские олимпиады школьников по математике 1993–2006* (MCCME 2007), final stage, grade 11 — https://math.ru/lib/files/pdf/olimp/Vseross.pdf, pp. 56–97; 2005 also olympiads.mccme.ru/vmo/31/zadachi.htm.
- 2006–2026: official final papers at https://olympiads.mccme.ru/vmo/ (statement sheets; 2021–2022 and 2024 from the organisers' booklets, statements only taken).

## Corrections
- 2021 P7: condition is $|m-n|>20^{21}$ (stored: 2021).
- 2025 P6: each player makes $10^{10}$ moves (stored: 1010).
- 1965 P4: the question asks for the number of bad **non-negative** integers (otherwise the answer is trivially infinite).
- 1966 P4: rewritten from the original — $\alpha,\beta$ are the angles through which the aeroplane moved as seen from $A$ and $B$; acute hypothesis restored; unsupported "along the line AB" removed; book Fig. 5 added (`images/ru_1966_p4_fig.png`).

## Added
- 1964 (5 statements, grade 11: book problems 54, 55, 52, 53, 44). The English version's grade table lists one problem twice; the Russian table does not. 1964 P5 carries a note: the book writes "n integers $a_1,\dots,a_{2k+1}$" and then uses $a_n$, read as $n=2k+1$.
- Source problem labels with letters (e.g. "6b") are recorded as `source_problem_label`; `source_problem_number` keeps the numeric part.

## Gaps
- 1967–1991: All-Union olympiad (USSR row `su`).
- 1992: no All-Russian final (the final stage was first held in 1993, Anapa).
- 2020: final cancelled.
