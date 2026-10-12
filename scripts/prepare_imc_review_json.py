#!/usr/bin/env python3
"""Convert full IMC staging output into a REVIEW-ONLY JSON file.

Strict gate: all 354 original problem pages represented, all statements
nonempty, unique official numbering. Do not register this in the public grid
without original-PDF fidelity review and classification.
"""
import argparse
import json
import pathlib
import re

EXPECTED = {
    **{y: 12 for y in range(1994, 2009)},
    **{y: 10 for y in range(2009, 2020)},
    **{y: 8 for y in range(2020, 2023)},
    **{y: 10 for y in range(2023, 2027)},
}
assert len(EXPECTED) == 33 and sum(EXPECTED.values()) == 354

def prepare(stage):
    if stage.get("competition") != "IMC":
        raise ValueError("Wrong competition")
    raw = stage.get("candidates")
    if not isinstance(raw, list) or len(raw) != 354:
        raise ValueError("Require exactly 354 candidate records")
    years = {y: [] for y in EXPECTED}
    for r in raw:
        year, number = r.get("year"), r.get("number")
        day, local = r.get("day"), r.get("day_local_number")
        if year not in EXPECTED or not isinstance(number, int):
            raise ValueError("Invalid year/problem identifier")
        if day not in (1, 2) or not isinstance(local, int):
            raise ValueError("Missing day/local number")
        expected_number = local + (EXPECTED[year] // 2 if day == 2 else 0)
        if number != expected_number:
            raise ValueError(f"Year {year} official problem numbering mismatch")
        statement = r.get("statement_candidate")
        if not isinstance(statement, str) or len(statement.strip()) < 30:
            raise ValueError(f"Unusable or empty candidate {year}/{number}")
        if re.search(r"solution\s*\(official\)", statement, flags=re.I):
            raise ValueError(f"Solution leakage {year}/{number}")
        if not r.get("source_url", "").startswith("https://studolymp.com/imc/problems/"):
            raise ValueError(f"Unexpected source URL {year}/{number}")
        years[year].append({
            "number": number,
            "day": day,
            "problem": statement.strip(),
            "latex_annotations_for_review": r.get("latex_annotations", []),
            "topics": [],
            "problem_dna": [],
            "source_url": r["source_url"],
            "statement_verified": False,
            "review_flags": r.get("review_flags", [])
        })
    result = []
    for year, entries in years.items():
        entries.sort(key=lambda p: p["number"])
        if [p["number"] for p in entries] != list(range(1, EXPECTED[year] + 1)):
            raise ValueError(f"Incomplete year {year}")
        result.append({"year": year, "problems": entries})
    return {
        "competition": "International Mathematics Competition for University Students",
        "short_name": "IMC",
        "status": "DRAFT_REQUIRES_OFFICIAL_PDF_VERIFICATION",
        "years": result,
        "problem_count": 354,
        "publication_eligible": False,
        "note": "Candidates only. No original-PDF source-fidelity review or topical classification yet; do not register in public bank."
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, type=pathlib.Path)
    ap.add_argument("--output", required=True, type=pathlib.Path)
    a = ap.parse_args()
    stage = json.loads(a.input.read_text(encoding="utf-8"))
    data = prepare(stage)
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Prepared review JSON with {len(data['years'])} complete years and {data['problem_count']} nonempty statements.")

if __name__ == "__main__":
    main()
