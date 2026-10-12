#!/usr/bin/env python3
"""Fail-closed structural audit of 1975-1984 Putnam research-review files.

This script checks internal consistency, not original-paper fidelity or rights.
"""
import json
from pathlib import Path
import sys

FILES = [(1975, 1979), (1980, 1984)]
EXPECTED = [f"{section}{n}" for section in "AB" for n in range(1, 7)]

def audit():
    problems = []
    errors = []
    for first, last in FILES:
        path = Path(f"undergraduate/Putnam-{first}-{last}-raw-review.json")
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            errors.append(f"{path}: cannot load JSON: {exc}")
            continue
        if data.get("publication_eligible") is not False:
            errors.append(f"{path}: publication must remain blocked")
        if data.get("first_year") != first or data.get("last_year") != last:
            errors.append(f"{path}: bad year-range metadata")
        years = data.get("years", [])
        if [y.get("year") for y in years] != list(range(first, last + 1)):
            errors.append(f"{path}: missing or out-of-order years")
        if data.get("errors"):
            errors.append(f"{path}: unresolved collection errors")
        count = 0
        for year in years:
            yr = year.get("year")
            entries = year.get("problems", [])
            if [p.get("number") for p in entries] != EXPECTED:
                errors.append(f"{path} year {yr}: labels must be A1-A6, B1-B6 exactly")
            for p in entries:
                count += 1
                label = p.get("number", "?")
                ident = f"{yr}-{label}"
                problems.append(ident)
                statement = p.get("problem")
                if not isinstance(statement, str) or len(statement.strip()) < 35:
                    errors.append(f"{ident}: missing/short problem statement")
                if "solution" in p or "answer" in p:
                    errors.append(f"{ident}: answers/solutions must not be bundled")
                if not isinstance(p.get("topics"), list) or not isinstance(p.get("problem_dna"), list):
                    errors.append(f"{ident}: missing structured classification lists")
                if p.get("statement_verified") not in (True, False):
                    errors.append(f"{ident}: missing explicit verification boolean")
                if p.get("statement_verified") is True:
                    if p.get("review_flags"):
                        errors.append(f"{ident}: verified statement still carries review flags")
                    if not p.get("verification_source") or not p.get("verification_method"):
                        errors.append(f"{ident}: verified statement lacks evidence metadata")
                elif not p.get("review_flags"):
                    errors.append(f"{ident}: unverified statement must carry review flags")
                if not p.get("source_url"):
                    errors.append(f"{ident}: missing provenance URL")
        if count != 60 or data.get("problem_count") != count:
            errors.append(f"{path}: expected 60 records, metadata says {data.get('problem_count')}, saw {count}")
    if len(problems) != len(set(problems)):
        errors.append("duplicate year-and-problem identifiers across files")
    for issue in errors:
        print("FAIL:", issue, file=sys.stderr)
    print(f"Checked {len(problems)} research-only problem records; structural issues: {len(errors)}")
    print("NOTE: Structural pass does NOT certify mathematical fidelity, rights or publication.")
    return bool(errors)

if __name__ == "__main__":
    sys.exit(audit())
