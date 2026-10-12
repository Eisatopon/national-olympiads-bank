#!/usr/bin/env python3
"""Quality gate for imported historical Putnam 1938-1974 research archive.

Structural checks and heuristics only; no primary-source fidelity certification.
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path("research/putnam")
SPECS = [
 ("Putnam-1938-1949-raw-review.json",115),
 ("Putnam-1950-1974-raw-review.json",308),
 ("Putnam-1958-spring-fall-raw-review.json",28),
]
issues=[]
all_ids=[]
counts={}
for name,expected_count in SPECS:
    path=ROOT/name
    if not path.exists():
        issues.append(f"{name}: missing archive")
        continue
    try:
        data=json.loads(path.read_text(encoding="utf-8"))
    except (OSError,ValueError) as e:
        issues.append(f"{name}: invalid JSON: {e}")
        continue
    if data.get("publication_eligible") is not False:
        issues.append(f"{name}: unsafe publication flag")
    groups=data.get("editions",data.get("years",[]))
    count=sum(len(g.get("problems",[])) for g in groups)
    counts[name]=count
    if count!=expected_count or data.get("problem_count")!=expected_count:
        issues.append(f"{name}: expected {expected_count}; found {count}")
    for group in groups:
        year=group["year"]
        edition=group.get("edition","regular")
        labels=[]
        for p in group.get("problems",[]):
            label=p.get("number")
            labels.append(label)
            key=f"{year}/{edition}/{label}"
            all_ids.append(key)
            if p.get("statement_verified") is not False:
                issues.append(f"{key}: original verification must not be presumed")
            if not p.get("review_flags"):
                issues.append(f"{key}: missing warning flags")
            if not p.get("source_url") or not p.get("source_id"):
                issues.append(f"{key}: source trace missing")
            if not isinstance(p.get("problem"),str) or len(p["problem"].strip())<30:
                issues.append(f"{key}: empty/short statement")
            if "solution" in p or "answer" in p:
                issues.append(f"{key}: solution/answer included")
        if len(labels)!=len(set(labels)):
            issues.append(f"{year}/{edition}: repeated problem labels")
        if any(not re.fullmatch(r"[A-Z][1-9][0-9]*",str(x)) for x in labels):
            issues.append(f"{year}/{edition}: malformed label")
if len(all_ids)!=len(set(all_ids)):
    issues.append("Duplicate identifier across files")
if len(all_ids)!=451:
    issues.append(f"Total {len(all_ids)}, expected 451")
print("ARCHIVE COUNTS:",counts)
print(f"STRUCTURAL ISSUES: {len(issues)}")
for issue in issues[:100]:
    print("FAIL:",issue,file=sys.stderr)
print("No record is made publication-eligible or source-verified by this test.")
sys.exit(bool(issues))
