# Schweitzer 1950: primary-source reconciliation checkpoint

Original primary source: *Contests in Higher Mathematics: Hungary 1949–1961* (1968), printed pages 12–15 (PDF pages 16–19). Original results table printed p. 33 confirms two distinct rounds with 10 and 9 problems.

Existing file: `docs/schweitzer/Schweitzer-1950-secondary-DRAFT.json`; all 19 entries are present, sequentially 1–19 with round index in `day`. **This file is STILL DRAFT, not the publishable source-reviewed collection.**

## Definite corrections from the primary scan
- 1950/II #2 (global #12): constraint `q ≡ 1 (mod 4)` restored in commit `3b81061`.
- 1950/I #7 (global #7): source prints the interval as `[k,k+1]`, not `[k,k+1)`; adjusted in commit `7e753f3`.
- 1950/I #10 (global #10): maintain the ambiguous original language about the osculating circles and endpoints as a faithful English restatement; do not present an invented interpretation as source fact.
- The original book's notation for 1950/II #3 is unusually dense; recheck all indices, summation signs and inequalities against printed page 14 before changing verification status.
- The original 1950/I #6 determinant equation and 1950/II #8 probability expression also require full mathematical visual comparison.

## Status
The authoritative original pages and round counts are now available, and individual verified corrections have been made to the staged draft. This document does **not** mark the whole set 19/19 as fully checked. Finish a formula-by-formula comparison, then create the source-reviewed JSON and run the bank's validators. No new public Undergraduate row was introduced by this audit.
