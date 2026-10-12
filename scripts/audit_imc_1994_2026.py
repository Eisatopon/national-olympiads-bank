#!/usr/bin/env python3
"""Fail-closed structural audit of the 1994–2026 IMC research review file.

This does NOT establish fidelity of formulas, diagrams or permission to publish.
"""
import json
import re
import sys
from pathlib import Path

path=Path("undergraduate/IMC-1994-2026-review.json")
data=json.loads(path.read_text(encoding="utf-8"))
errors=[]
expected_counts={**{y:12 for y in range(1994,2009)},
                 **{y:10 for y in range(2009,2020)},
                 **{y:8 for y in range(2020,2023)},
                 **{y:10 for y in range(2023,2027)}}
eligible = data.get("publication_eligible")
if eligible is not True:
    errors.append("Editorial publication gate must reflect completed 354-source review")
if data.get("status") != "EDITORIAL_SOURCE_REVIEW_COMPLETE":
    errors.append("IMC editorial source review must be marked complete")
years=data.get("years",[])
if [y.get("year") for y in years]!=list(range(1994,2027)):
    errors.append("IMC years not consecutive or unordered")
total=0
for year in years:
    y=year["year"]
    records=year.get("problems",[])
    expected=expected_counts.get(y)
    total+=len(records)
    if expected is None or len(records)!=expected:
        errors.append(f"{y}: expected {expected}, found {len(records)}")
    labels=[p.get("number") for p in records]
    if labels!=list(range(1,expected+1)) if expected else True:
        errors.append(f"{y}: expected problem labels 1 through {expected}")
    for p in records:
        ident=f"{y}-{p.get('number')}"
        n=p.get("number")
        expected_day=1 if n is not None and n <= expected//2 else 2
        if p.get("day")!=expected_day:
            errors.append(f"{ident}: incorrect exam day")
        if not isinstance(p.get("problem"),str) or len(p["problem"].strip())<25:
            errors.append(f"{ident}: missing/short statement")
        if p.get("statement_verified") is True:
            if not p.get("verification_source") or not p.get("verification_method") or not p.get("verification_page"):
                errors.append(f"{ident}: verified statement lacks source, method or original page")
            if p.get("review_flags"):
                errors.append(f"{ident}: verified statement still has unresolved review flags")
        elif p.get("statement_verified") is False:
            if not p.get("review_flags"):
                errors.append(f"{ident}: unverified record lacks review flags")
        else:
            errors.append(f"{ident}: invalid verification boolean")
        if not p.get("source_url"):
            errors.append(f"{ident}: source not traceable")
        if not isinstance(p.get("topics"),list) or not isinstance(p.get("problem_dna"),list):
            errors.append(f"{ident}: missing categorization arrays")
        if "solution" in p or "answer" in p:
            errors.append(f"{ident}: solutions/answers should not be included")
if total!=354 or data.get("problem_count")!=354:
    errors.append(f"Incorrect total: {total}")
print(f"IMC audit: {len(years)} years, {total} statements; structural issues {len(errors)}")
for e in errors: print("FAIL:",e,file=sys.stderr)
print("Verified metadata and editorial gate consistency checked; source fidelity and legal permission not independently certified by audit.")
sys.exit(bool(errors))
