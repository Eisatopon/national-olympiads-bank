# Vojtěch Jarník International Mathematical Competition — ingestion register

Status: **source inventory only; problem statements not yet imported or certified**.

## Official historical series

- Competition: Vojtěch Jarník International Mathematical Competition (VJIMC), Ostrava.
- First competition: 1991; 33rd competition: 2026.
- 2020, 2021, 2023: **no edition**. Do not create year records or placeholder problems.
- Each held edition requires separately sourced **Category I** and **Category II** problem papers. The earliest editions must be checked for whether both categories actually existed; never infer missing Category II papers.
- 2022: 30th edition (2 April).
- 2024: 31st edition (13 April).
- 2025: 32nd edition (1 May).
- 2026: 33rd edition.

## Source of truth

Official historical problem archive: https://jarnik.osu.cz/problems
Official current competition website: https://vjimc.osu.cz/
Official categories/rules: https://vjimc.osu.cz/rules

## Required ingestion gate

1. Retrieve each original Category I/II exam paper via the official historical archive; record exact source URL, year, category and paper.
2. Extract **complete problem statements only**, preserving formulas, quantifiers, diagrams, and official numbering; exclude solutions and hints.
3. Compare the rendered LaTeX to the source **for every problem**, including any required diagrams. Missing or unreadable diagrams block publication of the affected statement.
4. Encode in the repository's established JSON schema, with the year plus a stable category discriminator for the two separate papers; check compatibility with the actual loader before registration.
5. Reject blank, invented, duplicate or unverifiable statements; audit yearly paper counts against originals rather than assuming a fixed number.
6. Run Python/Node checks and GitHub Actions before publication; distinguish automated structural validation from source verification.

## Publication status

This register certifies **only the calendar/edition exclusions and research entry point**. It does NOT assert that any VJIMC statements were imported, tested, or published.
