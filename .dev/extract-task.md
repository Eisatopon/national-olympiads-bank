# Task: turn one downloaded olympiad archive into bank JSON (English, LaTeX)

You get: a competition, a source folder under a scratch folder (PDFs downloaded from the official site; there may be extra files such as solutions, reports, other grades, other languages, and a _page.html listing page), and an output path.

Goal: for every year available, extract the COMPLETE problem statements of the specified competition/paper and write ONE JSON file:
{"competition": "<name given to you>", "years": [ {"year": 2019, "problems": [ {"day": 1, "number": 1, "problem": "..."}, ... ]}, ... ]}
- years sorted ascending; problems in official order; "number" = official problem number within the year (if the year has several papers/tests with their own numbering 1..k, number them continuously 1..N across the year and put the paper index in "day": test/paper 1 -> day 1, test 2 -> day 2, ...; say in the report what each day means).
- "day": for two-day finals use 1/2 as officially split; for one-paper contests omit "day" entirely for all problems of that competition.
- Write with Python json.dump(obj, f, ensure_ascii=False, indent=2).

How to read sources:
- Prefer an English version of a year if one exists (e.g. files with _en/english/Problems); else translate faithfully from the original language.
- Read PDFs page by page and ALWAYS verify formulas against the rendered page (Claude Code can read PDF pages visually; on Windows you can also install poppler for pdftotext/pdftoppm). Text extraction garbles fractions, exponents, ≥/≤, angles, sums. If a file is scanned (no text), read it from images.
- If a file contains statements + solutions, take only the statements. If it contains several grades/categories, take only the one specified.
- Skip non-problem files (reports "verslag", results, rankings).

Style (like official English olympiad statements):
- Faithful, complete, precise. No summaries, hints, solutions, author credits or point values. Keep notes/remarks and parts (a), (b).
- All math in LaTeX: inline $...$, displayed $$...$$ inside the string. Standard MathJax only (no \cancel, no macros, no \emph, no markdown). Use \angle, \le, \ge, \dots, \cdot, \frac, \sqrt, \binom, \lfloor..., \gcd, \operatorname{lcm}.
- Keep names of people.

Figures: only when a problem STATEMENT includes a picture needed to understand it: crop it from a 250-dpi render into images/<prefix>_<year>_p<number>_fig.png (tight, ~10px white margin, no statement text), check it with Read, and append to the problem text "\n\nhttps://raw.githubusercontent.com/Eisatopon/national-olympiads-bank/main/images/<prefix>_<year>_p<number>_fig.png". <prefix> is given to you.

Validate before finishing: json.load works; every year has problems numbered 1..N without gaps; every problem string has an even number of $; no empty problems; no leftover Polish/German/etc. words.

Report briefly (max 15 lines): years included, problems count, what "day" means, years skipped and why, doubts (quote exact spot), figures made.
