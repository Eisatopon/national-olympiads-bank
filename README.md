# National Olympiads Problem Bank

A collection of national mathematical olympiad and team selection test statements, with an English interface and MathJax rendering.

## Current application

`index.html` is the standalone application. It loads one `<Country>-<competition>-problems.json` per collection from this repository. Features include country/year and keyword search, problem-set selection and reordering, local saving, printing with mathematical notation, and URL/QR sharing.

The older Olympiad Bank in `Eisatopon/eisatopon-next` is a separate application and dataset; an automated integration is not yet implemented.

## Data integrity

China is temporarily excluded from search and problem sets because its archive contains corrupted statements and duplicate identifiers. The original JSON is retained for reconstruction. Counts in the application cover available collections, not the quarantined archive.

Argentina has documented numbering gaps in 1994, 1996, 2007, 2008 and 2010. Original numbers are preserved; these years should not be treated as complete.

Passing validation confirms structural checks, not mathematical correctness or verification against an official source. Source research is in `.dev/sources.json`; per-problem source verification remains future work.

## Schema

```json
{"competition":"Competition name","years":[{"year":2025,"problems":[{"number":1,"problem":"Prove $x=x$."}]}]}
```

Years are ascending and unique. Numbers are positive integers in official order. Optional `day` identifies an exam day or paper and must be positive. Optional `category` is used by the topic filter. The USA TSTST archive retains its legacy schema, handled by a separate loader.

Most statements do not yet have topic or difficulty metadata. The application does not provide a difficulty filter. Figures currently appear as image URLs in statement text.

## Validation

Run from the repository root:

```bash
python -m unittest discover -s tests
node tests/test_loader.cjs
python scripts/validate_data.py
```

GitHub Actions runs these checks on pushes and pull requests. The validator checks JSON structure, collection registration, unique years and identifiers, numbering, nonempty statements, dollar delimiter parity, control characters and local figure existence. Known Argentina gaps are explicit exceptions; changes to their numbering fail validation. China is reported as quarantined and must remain marked as such in the application until repaired.

The loader also rejects duplicate identifiers before storing any records from a collection, preventing an incorrect statement from being selected or printed under a reused identifier.

## Local preview

Serve the repository using `python -m http.server`. The committed application loads published data from `main`. To inspect local data changes, replace `BASE` with `./` in a temporary copy; do not commit that preview-only change.
