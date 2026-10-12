#!/usr/bin/env python3
"""Collect Putnam 1938-1949 raw *statements* into a research-only JSON.

Discover exact historical problem identifiers from upstream Git tree. Never
invent twelve problems per year or synthesize non-contest years 1943-1945.
No solutions are copied. This is NOT original-source fidelity verification.
"""
import json
import pathlib
import re
import urllib.request
import urllib.error

OWNER_REPO = "YurenHao0426/PutnamGAP"
TREE_URL = f"https://api.github.com/repos/{OWNER_REPO}/git/trees/main?recursive=1"
RAW = f"https://raw.githubusercontent.com/{OWNER_REPO}/main/"
YEARS = [*range(1938, 1943), *range(1946, 1950)]
PATTERN = re.compile(r"^dataset/(19(?:3[89]|4[0-9]))-([A-Z])-(\d+)\.json$")

def get(url):
    req = urllib.request.Request(url, headers={
        "User-Agent": "Eisatopon-archival-review/1.0",
        "Accept": "application/vnd.github+json",
    })
    with urllib.request.urlopen(req, timeout=70) as resp:
        return json.load(resp)

def main():
    tree = get(TREE_URL)
    if tree.get("truncated"):
        raise SystemExit("FAIL: upstream file tree truncated; discovery incomplete")
    groups = {y: [] for y in YEARS}
    for entry in tree.get("tree", []):
        m = PATTERN.fullmatch(entry.get("path", ""))
        if m and int(m.group(1)) in groups and entry.get("type") == "blob":
            year, section, number = int(m.group(1)), m.group(2), int(m.group(3))
            groups[year].append((section, number, entry["path"]))
    if any(not groups[y] for y in YEARS):
        raise SystemExit("FAIL: at least one historical contest year has no source records")
    years = []
    for year in YEARS:
        records = []
        seen = set()
        for section, number, path in sorted(groups[year], key=lambda x: (x[0], x[1])):
            label = f"{section}{number}"
            if label in seen:
                raise SystemExit(f"FAIL: duplicate historical label {year}-{label}")
            seen.add(label)
            source = get(RAW + path)
            expected_id = f"{year}-{section}-{number}"
            if source.get("index") != expected_id:
                raise SystemExit(f"FAIL: identity mismatch: {expected_id}")
            statement = source.get("question")
            if not isinstance(statement, str) or len(statement.strip()) < 30:
                raise SystemExit(f"FAIL: absent/short statement: {expected_id}")
            records.append({
                "number": label,
                "problem": statement.strip(),
                "topics": [],
                "problem_dna": [],
                "source_id": expected_id,
                "source_url": f"https://github.com/{OWNER_REPO}/blob/main/{path}",
                "statement_verified": False,
                "review_flags": [
                    "OCR_math_symbols_must_be_checked",
                    "requires_authoritative_original_page_comparison",
                ],
            })
        years.append({"year": year, "problems": records})
        print(f"{year}: {len(records)} source-linked raw problems")
    total = sum(len(y["problems"]) for y in years)
    payload = {
        "competition": "William Lowell Putnam Mathematical Competition",
        "short_name": "Putnam",
        "first_year": 1938,
        "last_year": 1949,
        "non_contest_years": [1943, 1944, 1945],
        "status": "RAW_TRANSCRIPT_REQUIRES_ORIGINAL_PDF_FIDELITY_REVIEW",
        "publication_eligible": False,
        "problem_count": total,
        "source_dataset": f"https://github.com/{OWNER_REPO}",
        "authoritative_print_reference": "Gleason, Greenwood & Kelly, The William Lowell Putnam Mathematical Competition: Problems and Solutions, 1938-1964 (MAA)",
        "rights_note": "Availability of source does not confer republication permission; clarify with MAA.",
        "note": "Research-only statements from PutnamGAP. OCR may alter mathematics. Never automatically certify or publish.",
        "years": years,
        "errors": [],
    }
    out = pathlib.Path("staged/Putnam-1938-1949-raw-review.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"STAGED ONLY: {total} raw problem candidates, {len(years)} contest years, no solutions, no certification")

if __name__ == "__main__":
    main()
