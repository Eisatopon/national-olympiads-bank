#!/usr/bin/env python3
"""Stage IMC statements from collected source HTML; never publish unverified text.

Input: archive created by fetch_imc_sources.py.
Output: review-only JSON, one entry per captured original HTML page.

Requires beautifulsoup4. The text between the page title and the official
solution heading is only a CANDIDATE until manually checked against IMC PDFs.
"""
import argparse
import json
import pathlib
import re
from bs4 import BeautifulSoup, NavigableString, Tag

TITLE = re.compile(r"IMC\s+(\d{4})\s*[·\-]\s*Day\s+([12])\s*[·\-]\s*P(\d+)")
SOLUTION = re.compile(r"^\s*Solution\s*\(official\)\s*$", re.I)
IGNORE = {"script", "style", "noscript", "svg"}
MATH_TAGS = {"math"}

def render(node):
    if isinstance(node, NavigableString):
        return str(node)
    if not isinstance(node, Tag) or node.name in IGNORE:
        return ""
    if node.name == "annotation" and node.get("encoding") == "application/x-tex":
        return ""
    if node.name in MATH_TAGS or "katex" in node.get("class", []):
        annotations = node.select('annotation[encoding="application/x-tex"]')
        if annotations:
            return "$" + annotations[0].get_text(strip=True) + "$"
        # Do not pretend rendered glyphs are faithful LaTeX.
        return "[MATH_REQUIRES_REVIEW]"
    if node.name == "img":
        return "[FIGURE_REQUIRES_REVIEW]"
    return "".join(render(child) for child in node.children)

def extract(html, year, day, number):
    soup = BeautifulSoup(html, "html.parser")
    heading = soup.find("h1", string=lambda s: bool(s and TITLE.search(s)))
    if heading is None:
        raise ValueError("Matching problem title not found")
    match = TITLE.search(heading.get_text(" ", strip=True))
    if (int(match[1]), int(match[2]), int(match[3])) != (year, day, number):
        raise ValueError("Problem identity mismatch")
    # The content must be isolated structurally; never sweep the entire page,
    # because the official solution and related problems are also present.
    main = heading.find_parent("main")
    if main is None:
        raise ValueError("No <main> root available for isolation")
    solution = main.find(string=lambda s: bool(s and SOLUTION.fullmatch(s.strip())))
    if solution is None:
        raise ValueError("Official-solution boundary not detected")
    candidate_nodes = []
    for node in main.descendants:
        if node is heading:
            continue
        if node is solution:
            break
        if isinstance(node, Tag) and node.name in {"p", "li"}:
            if node.find_parent("a") or node.find_parent("button"):
                continue
            # Avoid duplicates: capture top-level textual blocks only.
            if node.find_parent(["p", "li"]) is not None:
                continue
            txt = render(node).strip()
            if txt:
                candidate_nodes.append(txt)
    candidate = "\n\n".join(candidate_nodes)
    flags = []
    if not candidate or len(candidate) < 30:
        flags.append("missing_or_short_statement")
    if "[MATH_REQUIRES_REVIEW]" in candidate:
        flags.append("math_not_recovered")
    if "[FIGURE_REQUIRES_REVIEW]" in candidate:
        flags.append("figure_requires_review")
    if "Solution (official)" in candidate:
        flags.append("solution_leakage")
    return candidate, flags

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--archive", required=True, type=pathlib.Path)
    parser.add_argument("--output", required=True, type=pathlib.Path)
    args = parser.parse_args()
    manifest = json.loads((args.archive / "manifest.json").read_text(encoding="utf-8"))
    records = []
    errors = []
    for item in manifest["sources"]:
        if item.get("source") != "studolymp_problem":
            continue
        year, day, number = item["year"], item["day"], item["number"]
        try:
            html = (args.archive / item["path"]).read_text(encoding="utf-8")
            statement, flags = extract(html, year, day, number)
        except (OSError, UnicodeError, ValueError) as exc:
            statement, flags = "", ["extraction_failed"]
            errors.append({"year": year, "day": day, "number": number, "error": str(exc)})
        records.append({
            "year": year, "day": day, "number": number,
            "statement_candidate": statement, "review_flags": flags,
            "source_url": item["resolved_url"], "source_sha256": item["sha256"],
            "statement_verified": False, "publication_eligible": False
        })
    records.sort(key=lambda r: (r["year"], r["day"], r["number"]))
    report = {
        "competition": "IMC",
        "status": "REVIEW_ONLY_NOT_FOR_PUBLICATION",
        "records": records, "errors": errors,
        "count": len(records),
        "clean_candidates": sum(1 for r in records if r["statement_candidate"] and not r["review_flags"]),
        "verified": 0,
        "note": "Every candidate requires comparison with the original IMC statement PDF."
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("IMC staged:", report["count"], "clean candidates:", report["clean_candidates"],
          "extraction errors:", len(errors))
    if errors or not records:
        raise SystemExit("Extraction incomplete; inspect review JSON and do not publish")

if __name__ == "__main__":
    main()
