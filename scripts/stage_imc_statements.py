#!/usr/bin/env python3
"""Create review-only IMC candidate JSON from individual source pages.

No record is considered verified or eligible for publication. Math is flagged
for source comparison, and official solutions are excluded at a hard boundary.
"""
import argparse
import json
import pathlib
import re
from bs4 import BeautifulSoup, NavigableString, Tag

TITLE = re.compile(r"^IMC\s+(\d{4})\s*[·–-]\s*Day\s+([12])\s*[·–-]\s*P(\d+)$")
SOLUTION = re.compile(r"Solution\s*\(official\)", re.I)
EXPECTED = {
    **{y: 12 for y in range(1994, 2009)},
    **{y: 10 for y in range(2009, 2020)},
    **{y: 8 for y in range(2020, 2023)},
    **{y: 10 for y in range(2023, 2027)},
}

def extract(html, year, day, number):
    soup = BeautifulSoup(html, "html.parser")
    h1 = soup.find("h1")
    if not h1:
        raise ValueError("Missing h1 problem identity")
    title = h1.get_text(" ", strip=True)
    match = TITLE.fullmatch(title)
    if not match or tuple(map(int, match.groups())) != (year, day, number):
        raise ValueError("Problem title does not match archive identity: " + title[:90])
    container = h1.find_parent("main") or h1.find_parent("article")
    if not container:
        raise ValueError("Missing <main> or <article> content boundary")
    # Read the HTML after the problem title and stop exactly at the solution.
    # Not a guarantee of text fidelity; every record remains review-only.
    nodes = list(container.descendants)
    try:
        start = next(i for i, node in enumerate(nodes) if node is h1)
        end = next(i for i in range(start + 1, len(nodes))
                   if isinstance(nodes[i], NavigableString) and
                   SOLUTION.search(str(nodes[i])))
    except StopIteration:
        raise ValueError("Official solution boundary not found")
    source_text = " ".join(str(n).strip() for n in nodes[start+1:end]
                           if isinstance(n, NavigableString) and str(n).strip()
                           and n.find_parent(["script", "style", "noscript"]) is None)
    # The raw rendered webpage may contain repeated hidden KaTeX output.
    # This is NOT a safe ready-made mathematical statement.
    source_text = re.sub(r"\s+", " ", source_text).strip()
    if len(source_text) < 30:
        raise ValueError("Candidate text missing or too short")
    tex = []
    for node in nodes[start+1:end]:
        if isinstance(node, Tag) and node.name == "annotation" and node.get("encoding") == "application/x-tex":
            t = node.get_text(strip=True)
            if t:
                tex.append(t)
    return {"statement_candidate": source_text,
            "latex_annotations": tex,
            "review_flags": ["page_text_and_latex_require_source_fidelity_review"]}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--archive", type=pathlib.Path, required=True)
    ap.add_argument("--output", type=pathlib.Path, required=True)
    a = ap.parse_args()
    manifest = json.loads((a.archive / "manifest.json").read_text(encoding="utf-8"))
    entries = [x for x in manifest["sources"] if x["source"] == "studolymp_problem"]
    records, errors = [], []
    for item in entries:
        year, day, number = item["year"], item["day"], item["number"]
        try:
            html = (a.archive / item["path"]).read_text(encoding="utf-8")
            candidate = extract(html, year, day, number)
            records.append({
                "year": year, "day": day, "number": number, **candidate,
                "source_url": item["resolved_url"], "source_sha256": item["sha256"],
                "statement_verified": False, "publication_eligible": False
            })
        except (OSError, ValueError, UnicodeError) as exc:
            errors.append({"year": year, "day": day, "number": number, "error": str(exc)})
    records.sort(key=lambda r: (r["year"], r["number"]))
    expected = sum(EXPECTED[y] for y in manifest["years_requested"])
    keys = {(r["year"], r["number"]) for r in records}
    if len(keys) != len(records):
        errors.append({"error": "Duplicate problem IDs"})
    if len(records) != expected:
        errors.append({"error": "Incomplete statement extraction",
                       "expected": expected, "actual": len(records)})
    output = {
        "competition": "IMC", "status": "UNVERIFIED_REVIEW_ONLY",
        "expected": expected, "extracted": len(records),
        "candidates": records, "errors": errors,
        "publication_note": "Must compare each statement and LaTeX expression to original IMC PDFs before import."
    }
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"STAGED {len(records)}/{expected}; errors {len(errors)}", flush=True)
    for problem in errors:
        print("ERROR", problem, flush=True)
    if errors:
        raise SystemExit(1)

if __name__ == "__main__":
    main()
