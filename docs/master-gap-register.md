# Master Gap Register — National Olympiads Bank

**Established:** 11 October 2026. **Status:** living, curated audit; it is **not** a certification of complete global or historical coverage.

## Master files

- [Machine-readable register](master-gap-register.json) — stable IDs, country, collection, year, problem, category, priority, original-source verification requirement and open/closed status.
- [Reconciliation script](../scripts/reconcile_master_gaps.py) — checks each registered missing individual problem/paper against the actual current JSON, flagging possible stale entries.
- [Detailed tasks](pending-tasks.md) — editorial and sourcing history.
- [Source fidelity inventory](verification-progress.md) — separately measures statement-vs-source comparisons.
- [Original-figure recovery record](required-figure-recovery-2026-10-04.json).

```bash
python scripts/reconcile_master_gaps.py
python scripts/reconcile_master_gaps.py --strict
```

**Important limitations:** The checker does not infer that a test is complete simply because its year is present. It cannot establish mathematical correctness, whether an exam was actually held, whether all grades/days are covered or whether a figure accurately reproduces the original. A flagged item must be checked against readable primary evidence by an editor before it is marked closed. For broad historical or multi-year gaps, manual/year-specific review remains necessary. This register was curated from the current repository docs and therefore does not claim that other gaps cannot exist.

## Priorities (11 October 2026)

| Workstream | First actions |
| --- | --- |
| P1 single problems and essential figures | Argentina 1994/1; Brazil 1982/4 and 1984/6; Chile 1991/7 and 2005/1; Israel tile image |
| P1 unfinished Estonia | TST 1998, 1999, 2000, 2006; Grade 9–11 national finals (see [Issue 36](https://github.com/Eisatopon/national-olympiads-bank/issues/36)) |
| P1 complete yearly sequences | Cyprus, Albania, Italy, Belgium, Uruguay, Thailand, Australia, Kosovo |
| P1 new country archives | Nepal, Uzbekistan, Algeria; Turkmenistan and North Korea as source-discovery candidates |
| P2 historical research | USSR/Russia, Poland, Bulgaria, Czechoslovakia, Iran, China, India; distinguish held competitions from incomplete secondary listings |
| Continuous verification | Original source fidelity checks and diagram provenance, independently of topical review |

## Rules for closing records

1. Secure readable, identifiable original papers (or clearly labeled reliable secondary copies if originals are genuinely unavailable), with correct competition, year, round, grade and day.
2. Restore **complete** papers without solutions, hints or missing diagrams. Never invent formulas or geometric figures.
3. Match records against repository JSON and review exact statement transcription/translation, MathJax, figures, duplicate identifiers and topic data.
4. Only after an actual data commit and validation update the individual record `status` to `closed`, and retain the commit and evidence in a `resolution` field. A problem may also be classified `not_held`, `out_of_scope` or `unobtainable` with documented evidence, never silently discarded.
5. Before starting a new batch rerun reconciliation, read the latest `pending-tasks.md` and compare with actual current JSON. Historic October 3–7 catalogues are **snapshots**, not fresh missing-lists.

**Already repaired (do not relist):** Greece 2011/2 figure; Chile 2025/3 figure; Argentina 1996/1, 2007/4, 2008/1, 2010/5; Croatia senior nationals 1992–2026 have been stored; China national 2017–2026 are present. Serbia SMO 2025 was not held. Uruguay 2026 is scheduled after this audit, not a held missing paper. Cyprus calendar 2020 cannot automatically be considered missing when the corresponding season exam occurred in February 2021.

## Reconciliation, not false certification

A missing figure in a current problem, an original-paper quality issue and an absent complete paper are different kinds of work. They have distinct `type` values in the register. `historical_candidate` means the source/country/round/year still needs confirmation and is **not** an assertion that a complete paper existed. `new_country` means no verified collection is currently indexed; it does not certify that the proposed country publicly releases annual finals.

The repository's existing country grid and runtime app are **unchanged** by this documentation/control addition.
