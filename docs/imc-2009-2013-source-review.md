# IMC 2009–2013 — source-fidelity review (2026-10-12)

Scope: 50 problems, ten organizer-hosted original Day 1 / Day 2 solution documents. Each problem statement is compared with its displayed mathematical notation on the original PDF page and marked with `verification_source`, `verification_page`, `verification_method`, and `verified_on` in `undergraduate/IMC-1994-2026-review.json`. This is an AI-assisted source-copy fidelity review, not human certification of mathematical correctness, solutions, or copyright status.

## Exact original PDFs

- 2009: `https://www.imc-math.org.uk/imc2009/imc2009-day{1,2}-solutions.pdf`
- 2010: `https://www.imc-math.org.uk/imc2010/imc2010-day{1,2}-solutions.pdf`
- 2011: `https://www.imc-math.org.uk/imc2011/imc2011-day{1,2}-solutions.pdf`
- 2012: `https://www.imc-math.org.uk/imc2012/IMC2012-day{1,2}-solutions.pdf`
- 2013: `https://www.imc-math.org.uk/imc2013/IMC2013-day{1,2}-solutions.pdf`

## Source-specific editorial notes

1. The organizer's **2013 Day 1** PDF displays the header “IMC 2012, ... July 28, 2012,” while the problems are the 2013 collection and its Day 2 PDF explicitly states 2013. This is an apparent original document heading carry-over, not evidence that the statements are from 2012. No archive year was changed.
2. In the organizer's **2012 Day 1 problem 1**, the sample claims `p(4)=5` but the displayed enumeration omits the singleton partition `4`; preserve the source's example rather than silently inventing a different statement. A separate editorial clarification may be offered outside the reproduced original.
3. **2010 problem 7** had originally been linked to Day 1 in the automated candidate metadata, but the actual statement is Day 2 problem 2. The candidate and verified source have both been corrected to the official Day 2 file.
4. Source-fidelity checks do not prove correctness of supplied organizer solutions. No solutions are included in the bank.

## Validation

The full five-year set has 10 statements per year (50 total). The repository regression test `tests/test_imc_review.cjs` enforces correct official PDF naming and day selection for every statement in 2009–2013. The original IMC bank-wide publication gate remains closed until its outstanding editions are reviewed; a successfully completed GitHub Actions run has not yet been independently confirmed.
