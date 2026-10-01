# National Olympiads Bank — instructions for Claude Code

Owner: Sokratis Romanidis (eisatopon.gr). **Reply to him in Greek**, directly, and do the work yourself (download, edit, verify, commit, push) instead of handing him manual steps.
Goal: the most complete bank in the world of NATIONAL math olympiad problems (national finals) and IMO TEAM SELECTION TESTS (TSTs), in English with LaTeX.

Live site: GitHub Pages of `Eisatopon/national-olympiads-bank` (this repo). Push to `main` publishes it (1–2 min delay).

## Repo layout
- `index.html`: the whole app (HTML + CSS + JS in one file).
- `<Country>-<comp>-problems.json`: one file per row in the grid.
- `images/`: figures, named `<prefix>_<year>_p<number>_fig.png`.
- `.dev/`: working notes. These are not used by the site.
  - `sources.json`: research on official archives per country.
  - `extract-task.md`: rules for turning PDFs into JSON.
  - `get-batch3.ps1`: the batch-3 download (already processed).

## JSON schema (per file)
```json
{"competition": "Full English name", "years": [
  {"year": 2024, "problems": [ {"day": 1, "number": 1, "problem": "LaTeX text ..."} ]}
]}
```
- Years ascending. `number` is 1..N with no gaps within a year.
- `day` = exam day, or test index for TSTs. Omit it entirely for one-paper contests.
- Problem text: faithful English, inline math `$...$`, display math `$$...$$`. Only standard MathJax: no `\cancel`, no macros, no markdown. The count of `$` must be even.
- Figures: put the URL on its own line at the end of the problem text, `\n\nhttps://raw.githubusercontent.com/Eisatopon/national-olympiads-bank/main/images/<name>.png`, and the file goes in `images/`.
- Exception: `Usa-tstst-problems.json` uses an older different schema, with kind `'usa'` in COUNTRIES. Don't change it unless asked.

## Adding a row to index.html (all of these, each exactly once)
1. **CSS colour var:** after the last `--xx: ...; --xx-ink: ...; --xx-tint: ...;` line, add `    --key: #col; --key-ink: #ink; --key-tint: #tint;`. The current last one is `--huo`. Pick a colour that isn't used yet.
2. **CSS class:** after the last `.f-xx { --f: var(--xx); ... }` line, add `.f-key { --f: var(--key); --f-ink: var(--key-ink); --f-tint: var(--key-tint); }`.
3. **Continent:** add `REGION_OF.key = 'europe'|'asia'|'americas'|'africa'|'oceania';` just before `const regionOf = key =>`. Without it the row falls into "Other".
4. **COUNTRIES entry:** insert `    { key: 'key', name: 'Display Name', flag: '🇽🇽', file: 'File-problems.json', kind: 'years' },` just before `{ key: 'um', name: 'USA USAMO'`. Use a name like "Serbia TST" for a second row of the same country.
5. **New country only:** bump the count in `<title>…Problems from N Countries…`, in `<b>N</b><span>countries</span>`, and add the country (alphabetical) to the `<meta name="description">` list.
6. **Years outside 1962–2026:** update `const FIRST = 1962, LAST = 2026;` and the two "1962–2026" strings.

The grid is grouped by continent; groups are collapsed by default and only one is open at a time. Problem totals are computed at runtime.

## Workflow for a new competition
1. Find official sources: check `.dev/sources.json` first, then search the web. Use official sites only; AoPS is fine only if the user downloads the files himself.
2. Download every year into a scratch folder outside the repo, e.g. `C:\Users\sokko\Documents\nob-work\<comp>\`.
3. Extract statements following `.dev/extract-task.md`:
   - Read the PDF pages visually and check every formula against the page image; text extraction garbles fractions, exponents, ≤/≥ and angles.
   - Take statements only (no solutions), and only the senior category.
   - Translate faithfully if the source isn't in English.
4. Validate the JSON:
   - it loads;
   - numbering runs 1..N in every year;
   - every problem has an even count of `$`;
   - every figure URL points to an existing file in `images/`;
   - no leftover foreign words;
   - no "see figure" without a figure.
5. Edit `index.html` as above.
6. Test locally with `python -m http.server`, or `npx serve`. To make the page load local JSON, temporarily replace `const BASE = 'https://raw.githubusercontent.com/Eisatopon/national-olympiads-bank/main/'` with `'./'` in a copy and open that copy. Check the row shows the right years, the counts and that there are no console errors. **Never commit the BASE change.**
7. `git add -A; git commit -m "Add <country/competition>"; git push`. Then tell him in Greek, briefly, what was added (years, problem count, figures).

## Current state (Oct 2026)
49 countries, ~9,660 problems (plus USA TSTST), 64 rows. The rows are:
- **Europe:** Greece TST, UK BMO1/BMO2/TST, Ireland, Italy, Turkey, Russia, Poland, Spain, Austria, Czech-Slovak, Serbia + TST, Croatia + HMO, Norway, Netherlands + TST, Switzerland + TST, Germany BWM + MO (1962–94 and 1996–2026; no 1995 in the official archive), Romania + TST, Lithuania + TST, Slovenia, Estonia final gr. 12 (1993–2026), Latvia, Estonia TST, Portugal, Denmark, Finland, Iceland, France TST, Cyprus TST, Hungary Kürschák (2014, 2017–24) + OKTV III final (2006–26), North Macedonia (2020–26), Ukraine final gr. 11 (2024–25), Bulgaria national round (2017–21).
- **Asia:** China (1987–2016), Azerbaijan TST, Singapore, India, Korea KMO/FKMO, Indonesia, Vietnam, Japan, Philippines, Hong Kong + TST, Kazakhstan final gr. 11 (2022 only).
- **Oceania:** Australia AMO (2016–20), New Zealand NZMO round 2 (2019–26).
- **Americas:** Argentina, Canada, Brazil, Mexico, USA USAMO/TSTST/TST.

Last added colour var is `--huo`. Helper scripts in `C:\Users\sokko\Documents\nob-work\tools\`: `pdf.py` (text/render), `validate.py`, `add_row.py` (does all index.html edits; check the description position for countries alphabetically before Croatia), `localtest.ps1` (headless Chrome against local JSON), `figcrop.py`.

## Next tasks (in order)
1. **Batch 3 is done** (Oct 2026). Leftovers: Kazakhstan other years (daryn.kz/ro/<year>/tasks/ only has 2022), Kürschák 2025 (not yet posted on bolyai.hu), Australia AMO after 2020 (not on amt.edu.au past papers), Bulgaria after 2021 (matematika.bg; needs `curl -A "Mozilla/5.0"`, a full browser UA gets 403).
2. **Gaps (Oct 2026 pass done):** added Russia 1993–2005 (from Agakhanov et al., math.ru/lib/files/pdf/olimp/Vseross.pdf; Russia 2020 had no final), Serbia SMO 2008, Croatia 2015, Italy 2026, Estonia final, Hungary OKTV, Kürschák 2014/2017. Still open:
   - **China file is corrupted** (`China-olympiad-problems.json`: years descending, 2016 has 81 mixed entries, ~150 problems with AoPS-PDF garbage like `$\leq$`, duplicated 2010/2011). Came from AoPS PDFs. Needs a rebuild; ask him for a source (no official one exists). China after 2016: same problem.
   - Validator warnings in older files: Argentina numbering gaps (1994, 1996, 2007, 2008, …), Greece TST and Azerbaijan/Singapore years not sorted, Greece 2013 numbering, a few "non-English letters" (mostly names with diacritics, probably fine).
   - Italy before 1997, Croatia national before 2015, Serbia SMO 2015/2020/2021/2025 and TST 2008–2015: not on the official sites.
   - Kürschák 2009–2016: in KöMaL February issues, but komal.hu/lap/YYYY-02/YYfebr.pdf only exists for 2015 and 2018; 1900–2008 not reachable.
3. **AoPS-only (ask him first):** Iran, Taiwan, Thailand, Israel; TSTs of China, Vietnam, India, Japan, Italy, Spain, Poland, Brazil, Mexico, Canada, Bulgaria, Ukraine. AoPS PDFs: https://artofproblemsolving.com/downloads/printable_post_collections/<collection id> — they need him logged in, and may come out blank.

## Known pitfalls
- Some official PDFs mislabel things: wrong year in a header, a 2nd-round page inside a final, a primary-school paper filed as a TST. Always check the header against the year.
- Don't add problems from doubtful sources. The old eisatopon-next "Olympiad Bank" data is unreliable (summarised statements, wrong years).
- Keep commits small and verified. After pushing, check that the raw.githubusercontent URLs of new images return 200.
