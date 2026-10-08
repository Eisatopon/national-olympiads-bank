# National Olympiads Bank — instructions for Claude Code

Owner: Sokratis Romanidis (eisatopon.gr). **Reply to him in Greek**, directly, and do the work yourself (download, edit, verify, commit, push) instead of handing him manual steps.
Goal: the most complete bank in the world of NATIONAL math olympiad problems (national finals) and IMO TEAM SELECTION TESTS (TSTs), in English with LaTeX. Since 7 Oct 2026 it also holds REGIONAL competitions (Balkan MO, JBMO, …) and will hold INTERNATIONAL ones, each in its own section of the same grid.

Live site: GitHub Pages of `Eisatopon/national-olympiads-bank` (this repo). Push to `main` publishes it (1–2 min delay).

## Repo layout
- `index.html`: the whole app (HTML + CSS + JS in one file).
- `<Country>-<comp>-problems.json`: one file per row in the grid (the data).
- `images/`: figures, named `<prefix>_<year>_p<number>_fig.png`.
- `metadata/` — **audit files**, used by validators/tests, NOT downloaded by the site:
  - `collections.json`: per-collection source links, coverage notes, `missing_problem_numbers`, and per-problem `statement_checks` / `statement_notes` (each with a full `reviewed_statement` copy + `statement_sha256`).
  - `topic-overrides.json` + `topic-overrides-final575.json`: reviewed topics per uid (same full-copy scheme; final575 wins).
  - `problem-dna.json`: small pilot (13 records) of techniques; the site loads it directly.
- `metadata/runtime/` — **generated, what the site downloads** (`topics.json`, `collections.json`, `manifest.json`): same information with an 8-hex fingerprint `h` (FNV-1a 32 over UTF-16, `textHash()` in index.html) instead of the full statement copy. ~150 KB gzipped instead of ~2.1 MB. `manifest.json` holds the problem count per file and year: the grid, the totals and the "All problems" first page are drawn from it, and a collection file is downloaded only when its problems are shown (a cell, a year column, a search/topic filter, Connections). **Never edit by hand.** After ANY change to a problem text or to `metadata/*.json`, run `python scripts/build_runtime_metadata.py` and commit the result; CI fails (`--check`) if it is stale.
- `docs/`: audit reports and per-batch source records (`*-additions-*.json`, `source-gap-audit-*.md`, `verification-progress.md`). `docs/quarantine/` keeps the old corrupted China file.
- `sources/`, `pdfs/`: downloaded source documents and statement-only PDFs (`available-pdfs.html`, `thailand-pdfs.html` list them).
- `scripts/`: `validate_data.py`, `validate_topics.py`, `validate_dna.py`, `verification_progress.py`, `build_runtime_metadata.py`.
- `tests/`: node `*.cjs` tests (they `vm`-load slices of index.html by function name — keep function names/order stable) and python unittests.
- `.github/workflows/validate-data.yml`: runs all of the above on every push.
- `.dev/`: older working notes (`sources.json`, `extract-task.md`). Not used by the site.

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
1. **CSS colour var:** after the last `--xx: ...; --xx-ink: ...; --xx-tint: ...;` line, add `    --key: #col; --key-ink: #ink; --key-tint: #tint;`. Rows are no longer strictly in order; grep `--[a-z]*: #` and pick a colour that isn't used yet.
2. **CSS class:** after the last `.f-xx { --f: var(--xx); ... }` line, add `.f-key { --f: var(--key); --f-ink: var(--key-ink); --f-tint: var(--key-tint); }`.
3. **Continent:** add `REGION_OF.key = 'europe'|'asia'|'americas'|'africa'|'oceania';` just before `const regionOf = key =>`. Without it the row falls into "Other".
4. **Section:** national rows need nothing; a regional row gets `scope: 'regional'` and an international one `scope: 'international'` at the end of its COUNTRIES entry (e.g. `{ key: 'bmo', …, kind: 'years', scope: 'regional' }`). The page shows National · Regional · International buttons above the grid (only sections that have rows), each with the same grid; regional rows still get a `REGION_OF` continent. Regional/international rows are not countries: pass `-` as COUNTRY to add_row and do not bump the country count. TSTs stay national.
5. **COUNTRIES entry:** insert `    { key: 'key', name: 'Display Name', flag: '🇽🇽', file: 'File-problems.json', kind: 'years' },` just before `{ key: 'um', name: 'USA USAMO'`. Also add a `collections.json` entry for the new file (source links, coverage) — `validate_data.py` checks every collection is tracked. Use a name like "Serbia TST" for a second row of the same country.
6. **New country only:** bump the count in `<title>…Problems from N Countries…`, in `<b>N</b><span>countries</span>`, and add the country (alphabetical) to the `<meta name="description">` list.
7. **Years outside 1950–2026:** update `const FIRST = 1950, LAST = 2026;` and the two "1950–2026" strings.

8. **Bump `DATA_VERSION`** (one constant next to `BASE`) whenever data or metadata change. It must start with the date, `YYYYMMDD-...` (e.g. `20261007-moldova-tst`): the page shows it as "Updated 7 Oct 2026" under the totals. all fetches use `?v=DATA_VERSION` + `cache: 'no-cache'` so browsers never mix old and new files.

The grid is grouped by continent (countries sorted alphabetically); groups are collapsed by default and only one is open at a time. Problem totals are computed at runtime.

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
   Then run everything CI runs: `python scripts/validate_data.py`, `python scripts/validate_topics.py`, `python scripts/validate_dna.py`, `python -m unittest discover -s tests`, every `node tests/*.cjs`, then `python scripts/build_runtime_metadata.py` (and `--check`).
5. Edit `index.html` as above.
6. Test locally with `python -m http.server`, or `npx serve`. To make the page load local JSON, temporarily replace `const BASE = 'https://raw.githubusercontent.com/Eisatopon/national-olympiads-bank/main/'` with `'./'` in a copy and open that copy. Check the row shows the right years, the counts and that there are no console errors. **Never commit the BASE change.** In the cloud container, Playwright + Chromium are preinstalled (`npm root -g`/playwright) for a headless check.
7. `git add -A; git commit -m "Add <country/competition>"; git push`. Check that the GitHub Actions run is green. Then tell him in Greek, briefly, what was added (years, problem count, figures).

## Current state (6 Oct 2026)
68 countries, 102 rows (93 national + 7 regional + 2 international), 18,852 problems (16,700 national incl. 132 USA TSTST, 1,656 regional, 496 international). Grid starts in 1947. Statements only — no solutions are stored.
- **Europe:** Greece TST (key `gr`) + Greece Archimedes senior (key `gra`, 1994–2026 except 2012, 2015, 2021; 1996 from AoPS; Greek originals from Eisatopon/eisatopon-bank, whose 1995-96…2009-10 year labels are shifted by one), UK BMO1/BMO2/TST, Ireland (1988–2026, 2025–26 from the UCD IrMO compendium), Italy ITAMO (1986–2026; 1986–1996 from AoPS, unverified) + PreIMO TST (1993–2001 single-paper TST from AoPS, unverified; 2002–08, 2010–19, 2022), Turkey, Russia (1961–63, 1965–66, 1993–2026), USSR All-Union (key `su`, 1967–1987 senior form; see docs/ussr-all-union-2026-10-06.md), Poland (1950–2026 except 1952, 1965), Spain (1964–2026 except 1967, 1975, 1978), Austria, Czech-Slovak (1952–2026 except 1959, 1968, 1970, 1980), Serbia SMO (2007–2026 except 2025; see docs/serbia-2026-10-06.md) + TST (2003–06, 2009, 2012–13, 2016–19, 2021–26; 2003, 2009, 2025 from AoPS, unverified), Croatia (1997–2005 from AoPS, unverified; 2015–2026) + HMO, Norway, Netherlands (1962–2026 complete, from Dutch originals; 1975 holds two finals as day 1/day 2, none in 1974) + TST, Switzerland (2004 from AoPS) + TST, Germany BWM + MO (1962–2026; 1995 from AoPS with 6A/6B alternatives), Romania grade 10 (1995–2026 except 2020; 1995–2011 and 2015 from AoPS, unverified) + TST (AoPS 1979, 1981, 1988 and IMO-TST parts of 1989–1993; full AoPS years 1995, 1997, 1998, 2000, 2002–05, 2007, 2008, 2010, 2011, 2013–15, 2017, 2018, 2023, unverified; SSMR-published days only for 2012 test 1, 2016, 2019, 2021, 2022, 2025, 2026 baraj 1 P3–P4), Lithuania + TST, Slovenia (1997–2000 from AoPS, unverified), Estonia final + TST, Latvia, Portugal (1994–2025 except 2004, cat. B, from SPM originals), Denmark, Finland, Iceland (2010–2025 except 2018; no 2018 final on stae.is), France TST, Cyprus TST, Hungary Kürschák (1947–2025 except 1956, 1959, 1987; 1947–2016 from AoPS, unverified — see docs/kurschak-1947-2016-aops-2026-10-06.md) + OKTV, North Macedonia (2000, 2001, 2006, 2007, 2009, 2011–13, 2015–19 from AoPS, unverified; 2020–26), Ukraine grade 11 (1997–99, 2005, 2009, 2018, 2021, 2023, 2026 from AoPS, unverified; 2024–25) + TST (key `uat`, 1999, 2009–11, 2013, 2015–18 from AoPS, unverified), Bulgaria (1963–2026; TST key `bgt` 2003–08 from AoPS, unverified; missing 1962, 1965, 1974, 1975, 1978, 1992, 2010 — see docs/bulgaria-1963-2016-2026-10-06.md), Sweden SMT (1961–2025 complete, from Swedish originals), Belgium OMB MAXI final (2007, 2008, 2022–26), Bosnia and Herzegovina TST (key `ba`, 1996–2018 from AoPS, unverified), Belarus final grade 11 (key `by`, 1997, 1999–2011, 2015–2026 from AoPS, unverified), Moldova TST (key `md`, 2012, 2014–17, 2019–24 from AoPS, unverified; 1993–2011 skipped as misattributed), Albania grade 12 (key `al`, 2010–12, 2024, 2025 from AoPS, unverified), Kosovo grade 12 (key `xk`, 2009–13, 2016, 2017, 2019–26 from AoPS, unverified).
- **Asia:** China CMO (1986–2026, rebuilt 4 Oct 2026, 6 problems/year, clean) + TST (key `cnt`, 1986–2003, 2005–08, 2010–19, 2021–25 from AoPS, unverified; see docs/china-tst-aops-2026-10-07.md), Azerbaijan TST, Singapore (2021, 2026 from AoPS, unverified), India (1986–88 from AoPS) + TST (key `int`, TST days of 2001, 2005, 2006, 2011–19, 2023–26 from AoPS, unverified), Korea KMO (1994–97, 2005–08 from AoPS) / FKMO (1993, 1997–2008 from AoPS), Indonesia (2026 from AoPS, unverified), Vietnam + TST (key `vnt`, 1985, 1990–92, 1994–2026 from AoPS, unverified), Japan, Philippines, Hong Kong + TST, Iran TST (key `irt`, 2006–2022, 2024, 2026 from AoPS, unverified; see docs/iran-tst-aops-2026-10-07.md), Israel Gillis (key `il`, 2011, 2014–16, 2018, 2021, 2022, 2024, 2025 from AoPS, unverified; figure-dependent years omitted), Kazakhstan senior final (1999–2026; 1999–2010 from AoPS, unverified), Taiwan TMO (key `tw`, 1992–96, 1998–2000, 2002, 2006 from AoPS, unverified), Bangladesh BdMO national higher secondary (key `bd`, 2023–26 from AoPS, unverified), Thailand TMO (2004–26) + TST (2011–21) + TSTST (2021).
- **Africa:** South Africa SAMO senior final (key `za`, 1995–2026 from AoPS, unverified; official papers are sold).
- **Oceania:** Australia AMO (2016–20), New Zealand NZMO round 2 (2019–26).
- **Regional section:** Balkan MO (key `bmo`, 1984–2026 complete) and Junior Balkan MO (key `jbmo`, 1997–2026 complete), from AoPS, unverified — see docs/balkan-aops-2026-10-07.md. APMO (key `apmo`, continent asia, 1989–2026 complete, from AoPS c3226, unverified — see docs/apmo-aops-2026-10-07.md). Baltic Way (key `bw`, continent europe, 1990–2025, 20 problems/year, from AoPS c3231 and cross-checked against the official sheets at georgmohr.dk/bw; 1996 P2, 2008 P14, 2018 P9 omitted as figure-dependent and recorded in KNOWN_GAPS — see docs/baltic-way-aops-2026-10-07.md). MEMO (key `memo`, continent europe, 2007–2026, day 1 individual / day 2 team, from AoPS c3237, cross-checked with the official sheets on dev.skoljka.org/archive/memo/ — see docs/memo-aops-2026-10-08.md). Benelux MO (key `bx`, continent europe, 2009–2026 complete, 4 problems/year, transcribed from the official English papers on bxmo.org with source checks for all 72 statements; 2020 P2 figure cropped from the paper — see docs/benelux-bxmo-2026-10-08.md). Nordic MC (key `nmc`, continent europe, 1987–2026 complete, 4 problems/year, from the official NMC archive georgmohr.dk/nmcperm: 1987–2003 from the Lehtinen English collection, 2004–2026 from the English paper of each year; source checks for all 160; 1995 P1 figure — see docs/nordic-nmc-2026-10-08.md).
- **International section:** IMO (key `imo`, 1959–2026 complete, no IMO in 1980; continent group `world`), imported from the owner's repo Eisatopon/IMO-BANK (`data/imo_YYYY.json`, `\( \)` delimiters converted to `$`) — see docs/imo-2026-10-07.md. Rebuilt with the full official wording on 7 Oct 2026: 1959–1983 rewritten, 1996, 1997, 2025 and several wrong IMO-BANK problems replaced (cross-checked with AoPS c3222). EGMO (key `egmo`, 2012–2026 complete, from AoPS c3246, unverified — see docs/egmo-aops-2026-10-07.md). Next candidates: Iberoamerican, Centroamerican, Cono Sur, Pan-African, Silk Road (AoPS ids in AoPS folder c14).
- **Americas:** Argentina, Canada, Brazil, Mexico, Chile final (1989–2025, partial years flagged) + TST, Peru TST (key `pe`, 2009–2020, 2022, 2024 TST days from AoPS, unverified), Costa Rica final level III (key `cr`, 2013, 2015, 2020, 2022, 2023 from AoPS, unverified), Ecuador OMEC final (key `ec`, 2016, 2017, 2019–24 from AoPS, unverified), Uruguay final level V (2011–17), USA USAMO/TSTST/TST.

Review layers (all AI-assisted, kept separate): source-fidelity checks (`statement_checks`, ~1,700 records — see `docs/verification-progress.md`), editorial notes for source errors (`statement_notes`), thematic topics (all 11,041 reviewed), Problem DNA pilot (13). A changed statement automatically loses its checks/topics until re-reviewed (fingerprint mismatch).

Site features: continent grid (lazy loading via the manifest since 7 Oct 2026; the grid scrolls inside a box with a sticky year row, and a "Country, competition or year" box filters rows or jumps to a year column — Enter opens a single match or a year; the address bar keeps the current view as `?s=<section>&c=<key>&y=<year>&d=<day>&t=<topic>&q=<search>`, with a "Copy link to this view" button; `?set=` links still open a shared problem set), topic chips/filters, search, printable problem sets, named collections with share links, provenance notes per problem, "Connections" between problems, available-PDF pages.

Helper scripts on the owner's PC in `C:\Users\sokko\Documents\nob-work\tools\`: `pdf.py`, `validate.py`, `add_row.py` (predates the collections.json/DATA_VERSION steps — do those by hand), `localtest.ps1`, `figcrop.py`.

## Next tasks
1. **Open source gaps** (details: `docs/source-gap-audit-2026-10-03.md`): Chile figures (1989 P3, 1991 P6–7, 1995 two figures, 2025 P3), Chile 1991 only P3 stored, Chile 1998/2004/2005/2017 and 1999 P2 missing; Argentina missing 1994/1, 1996/1, 2007/4, 2008/1, 2010/5; Italy PreIMO 2009, 2020, 2021, 2023–26; Belgium 2009–21 (archive behind login); Uruguay after 2017; Thailand TST after 2021.
2. Older leftovers: Australia AMO after 2020, Croatia national before 2015, Serbia SMO 2025 and TST 2007–2011, 2014–2015, 2020, 2025 (no originals found on dms.rs or imomath.com/srb/zadaci).
3. **AoPS National catalogue audit** (owner-supplied, 4 Oct 2026): `docs/aops-national-catalogue-audit-2026-10-04.md`. Its top section lists, per existing row, the years AoPS has that the bank lacks, plus candidate new countries (Greece National, Iran, Israel, Taiwan, Belarus, South Africa, …). Check it before searching for any competition; keep its status block up to date when you add years.
4. **AoPS sources:** he now asks Claude to fetch them directly. The cloud shell cannot reach AoPS (Cloudflare challenge blocks curl and headless Chromium even with Full network access, checked 8 Oct 2026); official sites are reachable from the cloud with Full network access; use his Chrome (Claude in Chrome) on an artofproblemsolving.com tab and call `/m/community/ajax.php` with `a=fetch_category_data&category_id=<id>` (folder → collections → posts with `post_canonical`) or `a=fetch_topic&topic_id=<id>`. One JS call times out after 45 s, so run loops detached and poll; javascript_tool output truncates at ~1.5 KB, so write results into a `<pre>` and read them with `get_page_text`. Always cross-check AoPS against an original-language source when one exists. Candidates: Paraguay and Malaysia were checked and skipped (short-answer, junior level, many figures); Japan/Spain/Poland have no separate TST on AoPS. (Morocco TST 2017 was added and then removed at his request.)
5. Source-fidelity checks for the remaining ~9,300 records.

## Known pitfalls
- Some official PDFs mislabel things: wrong year in a header, a 2nd-round page inside a final, a primary-school paper filed as a TST. Always check the header against the year.
- Don't add problems from doubtful sources. The old eisatopon-next "Olympiad Bank" data is unreliable (summarised statements, wrong years).
- Keep commits small and verified. After pushing, check that the raw.githubusercontent URLs of new images return 200.
- Thematic topics are AI-assigned; grid/tiling problems are sometimes tagged Geometry rather than Combinatorics. Fix via the override files, not the classifier regexes alone.
- `metadata/topic-overrides.json` is ~6.6 MB: never load it from index.html; use the runtime files.
