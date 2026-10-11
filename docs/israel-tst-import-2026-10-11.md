# Israel TST import — 11 October 2026

Added **74 statements in 24 complete displayed tests**, in the new Asia/National row `ilt`, `Israel-tst-problems.json`. The owner explicitly accepted complete individual examinations even where other tests of the same annual season remain missing. This supersedes the earlier decision to withhold every examination until a complete annual season is recovered. Israel is not declared complete.

All seven secondary AoPS compilation PDFs were inspected visually in the browser, **19 pages in total**, with enlarged checks for ambiguous formulae. The statements are independently worded English mathematical restatements retaining the conditions and questions; no solutions were imported. The original Israeli exam sheets remain unretrieved. Every statement has a visible secondary-source qualification and its original test/problem identity; none earns an original-source verification badge. Numbering is continuous within each stored year, while `day` preserves the source test label. The exact mapping and dates are in `israel-tst-additions-2026-10-11.json`.

| Source year | Collection | Included test labels | Statements | Unresolved / withheld |
|---|---:|---|---:|---|
| 2016 | 422600 | 2 | 4 | Test 1 withheld: coin donations are bounded by three without a rule specifying subsequent donation choices. Official index also lists four camp packets; this is not a full-season certificate. |
| 2021 | 3053795 | 1, 2, 4, 6, 8 | 16 | Labels 3, 5, 7 absent. Tests 1 and 2 were held in November 2020; source school-year heading retained. |
| 2022 | 3048611 | 2, 7, 9 | 9 | Labels 1, 3–6, 8 absent; source explicitly omits tests consisting of IMO Shortlist problems. |
| 2023 | 3316615 | 1, 2, 5, 7 | 12 | Test 3 withheld as a whole: P1 refers to six tiles but the image is absent from the compiled PDF. Labels 4, 6 absent; explicit IMO Shortlist omission. |
| 2024 | 3525428 | 1, 2, 3, 6, 8 | 15 | Labels 4, 5, 7 absent; explicit IMO Shortlist omission. Test 3 P2 has the disclosed single-vertex clarification below. |
| 2025 | 4081821 | 2, 4 | 6 | Tests 1, 7, 8 each contain only two entries; full original-paper counts not established, so each whole test withheld. Labels 3, 5, 6 absent. |
| 2026 | 4633248 | 1, 4, 5, 7 | 12 | Test 2 P3 prints AC, AD rather than a nondegenerate pair: F becomes D and circle BDF is undefined. Test 9 P3 requires a0 at n=2 without defining it. Both whole tests withheld; labels 3, 6, 8 absent. |

An absent label is a gap in the recovered compilation, not proof that a particular exam was held or that the highest printed label was the last exam. Other years remain unretrieved. Original camp archive leads remain in `israel-tst-audit-2026-10-11.md`.

## Formula review and editorial qualifications

- 2021 Test 1 P1: first sum has 2019 alternating terms; second ends in +1/5781. Test 2 P3: the three counts are floors of n²/25, n²/19, n²/14. Test 8 P3 includes the entire sum of four norms squared.
- 2022 Test 7 P2: **S > 3n**, not 3^n; R < 2^(2^n). This was confirmed at 100% zoom against the rendered page. Both annulus boundaries are included.
- 2024 Test 8 P1: the product is of floor(n/k), with **no exponent k**; the conclusion is infinitely many m with a_(m+1) < a_m.
- 2024 Test 3 P2: the printed N is positive, but its neighbour average is undefined for N=1. The stored condition is the equivalent degree-multiplied inequality d_v(w_v+1) >= sum of neighbouring weights. For N>1 it is exactly equivalent; for a single vertex it is vacuous. This minimal extension is explicitly disclosed per statement, without an exact-source badge.
- 2026 Test 4 P2: iterations explicitly have to be well-defined in the printed domain >1. No value for Delta(1) has been invented. Exact-period question and prime-power/multiplicativity definitions retained.
- No missing geometric/tile image was reconstructed by guessing. The direct AoPS discussion containing the 2023 tile problem reached a Cloudflare human-verification challenge; the challenge was not solved or bypassed. The Bariz search-indexed mirror identifies the problem but did not provide a readable image.

## Correction to the preceding audit

The preceding source-only audit claimed that two rendered pages had been inspected. Its web screenshot results were text placeholders, which do not establish visual inspection. That claim is withdrawn. The visual review reported here comes from actual browser-rendered images of all 19 pages, with enlarged follow-ups where needed.

## Validation and inventory

All 74 added statements received full-statement topic reviews. The data, topic and DNA validators, Python unittests, all Node CJS checks, generated runtime freshness, and whitespace checks are required before publication. Inventory after import: **20,736 statements, 116 rows (99 national), 72 countries**. Original-source checks remain **5,954**, with **14,782** pending. Cyprus and Estonia remain next in the agreed country order; Israel's precise unresolved items remain documented.
