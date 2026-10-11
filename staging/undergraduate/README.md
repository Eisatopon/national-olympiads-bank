# Undergraduate staging — not published to the bank

Branch: `work/undergraduate-five-collections-unpublished-20261011`

This branch holds **five independent year/source coverage files** for the eventual five searchable problem collections:

| Collection | Start | Last indexed year |
| --- | ---: | ---: |
| IMC | 1994 | 2026 |
| Putnam | 1938 | 2025 |
| SEEMOUS | 2007 | 2026 |
| Vojtěch Jarník | 1991 | 2026 |
| Simon Marais | 2017 | 2025 |

These are **research inventories**, **not imported question statements**, **not completed examination text files**, and **not classified problem records**. `problem_records_imported: 0` is deliberate and must not be changed until actual source-verified problem objects have been added. Do not infer completion from a year's existence in the inventory.

Each eventual individual problem must follow `metadata/undergraduate-import-contract.json`: complete verified statement in LaTeX, exact year and competition number, correct day/session/paper/category, taxonomy topics, Problem DNA, figures when necessary, traceable primary source, and documented publication basis. No solutions, invented problem numbers, or missing-diagram omissions. Early Putnam contests require historically correct structure; 1943–45 absent, 1958 has two events. Coverage-year entries for competitions other than Putnam do **not** confirm that each contest took place in every year; they identify the user-requested search span.

To check the five coverage inventories:

```sh
node staging/undergraduate/check-staging.cjs
```

## Separation from public bank

This work is stored only on an unpublished feature branch. It is **not merged into `main`**, is **not wired into `index.html`**, `COUNTRIES`, the runtime manifest or the published problem count, and does not alter any public grid. **Because the repository is public, GitHub branch files are still publicly readable at their direct URLs**, even though they are not exposed in the bank UI.

To complete this task, verified lawful-to-publish original statements must be gathered, transcribed and mathematically checked, classified and then persisted as real problem JSON. Do not change the status to complete until that work is finished.
