#!/usr/bin/env python3
"""Fail-closed import of historical Putnam research artifacts into research/putnam.

Never copy to the published bank. Primary-paper verification is separate.
"""
import json
from pathlib import Path

SPECS = [
    ("Putnam-1938-1949-raw-review.json", 115),
    ("Putnam-1950-1974-raw-review.json", 308),
    ("Putnam-1958-spring-fall-raw-review.json", 28),
]
IN = Path("staged")
OUT = Path("research/putnam")
seen = set()
total = 0

for name, count in SPECS:
    src = IN / name
    a = json.loads(src.read_text(encoding="utf-8"))
    assert a["publication_eligible"] is False, name
    assert a["problem_count"] == count, (name, a.get("problem_count"))
    groups = a["editions"] if "editions" in a else a["years"]
    assert groups and not a.get("errors"), name
    actual = 0
    for group in groups:
        edition = group.get("edition", "regular")
        for p in group["problems"]:
            actual += 1
            ident = (group["year"], edition, p["number"])
            assert ident not in seen, f"Duplicate historical entry: {ident}"
            seen.add(ident)
            assert p["statement_verified"] is False, ident
            assert p.get("review_flags"), ident
            assert isinstance(p.get("problem"), str) and len(p["problem"].strip()) >= 30, ident
            assert p.get("source_url") and p.get("source_id"), ident
            assert "solution" not in p and "answer" not in p, ident
    assert actual == count, (name, actual)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(json.dumps(a, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    total += actual

assert total == 451, total
print(f"PASS: imported {total} unique source-linked research records, all unverified and nonpublishing")
