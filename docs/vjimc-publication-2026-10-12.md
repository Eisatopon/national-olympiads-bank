# VJIMC native-text publication: 1991–2026

All **261 statements** from 33 held editions and 65 Category I/II papers now use English text and LaTeX. Native-text review was completed on 13 October 2026. No solutions are included. The 261 full-statement PNGs and the facsimile renderer have been removed; only the two diagram-only crops needed for 2026/I/3 and 2026/II/4 remain.

Every statement was manually transcribed and compared with the rendered official PDF. Source URLs, document SHA-256 hashes, pages, original statement-region coordinates, category identities and variant labels are preserved. Each native statement also has its own SHA-256 hash and an independent reviewed snapshot in `metadata/vjimc-statement-checks.json`. The snapshots drive the source-check badges and become stale if a published statement changes.

The source-papers collection was obtained in GitHub Actions run 38274003460, artifact 11758317060. All 60 original PDF hashes were checked again locally. The organiser's HTTPS certificate-chain exception remains recorded in the source metadata. It does not certify the transport as verified.

Category I/II remain distinct in loader IDs, visible filters, print sheets, related cards and AI prompts. Paper identities use `paper_id`, not invented competition days. The 4-M and 4-I alternatives are retained separately in both categories for 1997 and 1998. The official 1991 archive contains Category I only. Category I in 1995 and both categories in 1996 each have three problems. No placeholder editions are created for 2020, 2021 or 2023.

The two diagrams are lossless three-times-resolution crops of the official figure regions. The saved images were compared pixel-for-pixel with those regions. The surrounding statements and every formula remain native text. Diagram alt descriptions are English.

## Source editorial review

- **1993/I/2:** the introductory wording omits the matrix size; part 2 displays a 3-by-3 matrix. The original wording is retained and this omission is explicitly noted, without silently adding a hypothesis.
- **1993/II/1:** the original calls the generated ideal a “prime ideal”, although the described construction is a principal ideal. This terminology issue is explicitly noted and the original wording is retained.
- **2005/II/3:** the question paper prints the repeated factor `xy(1-y)(1-y)`. The official solutions document restates the question with `xy(1-x)(1-y)`. The corrected repeated statement is used, with an explicit source note. Its corrected formula was also visually checked in the historical compilation, page 153, SHA-256 `504d617e654ebb8e99bb89a380670a3936fb6f8e1c7600e33d9cb3a83a0bf62d`. Only the corrected question was imported.

Topic categories were reviewed using the existing four-category taxonomy. Technique lists remain empty until supported by a separate mathematical analysis. Source comparison certifies transcription fidelity; it does not independently prove every assertion in the historical papers.

Publication follows the project owner's explicit instruction and their reported oral permission to republish the contest problems.

## Verification

The native collection passed the existing bank regression checks, all 261 unique loader-ID checks, historical year/category/variant counts, statement snapshots and hashes, and critical-formula guards. MathJax successfully rendered **1,409 mathematical expressions**. Reproduce the original-source-byte and figure checks with:

```sh
python scripts/verify_vjimc_sources.py --pdf-dir /path/to/vjimc-pdfs
node tests/test_vjimc_publication.cjs
python scripts/build_runtime_metadata.py --check
```

The old facsimile builder was retired so it cannot overwrite the verified native text with damaged PDF extraction. The National, Regional, International and Tournament collection files are unchanged.
