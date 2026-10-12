#!/usr/bin/env python3
"""Fail-closed Putnam 1985–2025 review integrity / visual-dependency audit.

This checks structure and flags source-review needs; does not certify paper fidelity.
"""
import json
import re
import sys
from pathlib import Path

p=Path("undergraduate/Putnam-1985-2025-review.json")
d=json.loads(p.read_text(encoding="utf-8"))
errors=[]
warnings=[]
if d.get("publication_eligible") is not False:
    errors.append("Publication gate MUST remain closed")
if (d.get("first_year"),d.get("last_year")) != (1985,2025):
    errors.append("Incorrect time span")
ys=d.get("years",[])
if [y.get("year") for y in ys] != list(range(1985,2026)):
    errors.append("Missing, duplicated, or unordered contest years")
expected=[f"{s}{n}" for s in "AB" for n in range(1,7)]
seen=set()
for y in ys:
    year=y["year"]
    problems=y.get("problems",[])
    if [p.get("number") for p in problems] != expected:
        errors.append(f"{year}: incorrect A1-A6 B1-B6 labels")
    if not y.get("source_url"):
        errors.append(f"{year}: missing source URL")
    for x in problems:
        key=f"{year}-{x.get('number','?')}"
        if key in seen:
            errors.append(f"{key}: duplicate")
        seen.add(key)
        stmt=x.get("problem")
        if not isinstance(stmt,str) or len(stmt.strip())<35:
            errors.append(f"{key}: missing statement")
            continue
        if x.get("statement_verified") is not False:
            errors.append(f"{key}: unverified transcript must not be certified here")
        if not x.get("review_flags"):
            errors.append(f"{key}: missing review warning")
        if "solution" in x or "answer" in x:
            errors.append(f"{key}: unwanted solution data")
        if not isinstance(x.get("topics"),list) or not isinstance(x.get("problem_dna"),list):
            errors.append(f"{key}: missing category/DNA lists")
        if re.search(r"(?i)(?:figure|diagram|pictured|drawn below|illustrat|see (?:the )?picture)",stmt):
            warnings.append((key,"figure/diagram wording — inspect original sheet"))
        if re.search(r"(?<!\\)\\\\(?:begin\{(?:tabular|picture|tikzpicture)|includegraphics|epsfig)",stmt):
            warnings.append((key,"LaTeX embedded illustration/tabular — inspect rendering"))
        if stmt.count("$")%2:
            warnings.append((key,"odd dollar delimiter count; inspect formatting"))
if len(seen)!=492 or d.get("problem_count")!=492:
    errors.append(f"Expected exactly 492 problems; {len(seen)} unique")
print(f"Putnam 1985–2025: {len(ys)} years, {len(seen)} distinct records; structural errors: {len(errors)}")
print(f"Review hints: {len(warnings)} (heuristic; false positives possible)")
for ident,warning in warnings:
    print("REVIEW:",ident,warning)
for error in errors:
    print("FAIL:",error,file=sys.stderr)
print("This audit does not confer source fidelity or reproduction rights.")
sys.exit(bool(errors))
