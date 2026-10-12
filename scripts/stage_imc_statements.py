#!/usr/bin/env python3
"""Extract unverified IMC problem candidates from archived ANNUAL pages.

This is deliberately fail-closed: a missing or ambiguous boundary is reported
rather than silently guessed. Nothing produced here is ready for publication.
"""
import argparse
import json
import pathlib
import re
from bs4 import BeautifulSoup, NavigableString, Tag

DAY = re.compile(r"^Day\s*([12])$", re.I)
PROBLEM = re.compile(r"^Problem\s+(\d+)$", re.I)
STOP = re.compile(r"^(?:Day\s*[12]|Problem\s+\d+|Solutions?|Statistics)$", re.I)
# Based on the actual edition structures, not a uniform assumption.
EXPECTED_COUNTS = {
    **{y: 12 for y in range(1994, 2009)},
    **{y: 10 for y in range(2009, 2020)},
    **{y: 8 for y in range(2020, 2023)},
    **{y: 10 for y in range(2023, 2027)},
}
assert len(EXPECTED_COUNTS) == 33 and sum(EXPECTED_COUNTS.values()) == 354

def rendered_math(node):
    annotations = node.select('annotation[encoding="application/x-tex"]')
    if annotations:
        tex = annotations[0].get_text(strip=True)
        if tex:
            return "$" + tex + "$"
    return "[MATH_REQUIRES_REVIEW]"

def render(node):
    if isinstance(node, NavigableString):
        return str(node)
    if not isinstance(node, Tag) or node.name in {"script", "style", "noscript"}:
        return ""
    classes = node.get("class", [])
    if node.name == "math" or "katex" in classes or "MathJax" in classes:
        return rendered_math(node)
    if node.name == "img":
        return "[FIGURE_REQUIRES_REVIEW]"
    if node.name == "button":
        return ""
    if node.name == "br":
        return "\n"
    return "".join(render(child) for child in node.children)

def clean(s):
    return re.sub(r"[ \t]+", " ", s).strip()

def extract(html, year):
    soup = BeautifulSoup(html, "html.parser")
    content = soup.select_one("main") or soup.select_one("article")
    if content is None:
        raise ValueError("Neither <main> nor <article> detected")
    # Heading conventions are deliberately strict to prevent collecting
    # site navigation, solutions, or duplicate rendered MathJax glyphs.
    headings = [h for h in content.find_all(re.compile(r"^h[1-6]$"))
                if DAY.fullmatch(h.get_text(" ", strip=True))
                or PROBLEM.fullmatch(h.get_text(" ", strip=True))]
    if not headings:
        raise ValueError("No recognized Day/Problem headings")
    records, day = [], None
    for idx, heading in enumerate(headings):
        title = heading.get_text(" ", strip=True)
        d = DAY.fullmatch(title)
        if d:
            day = int(d[1])
            continue
        p = PROBLEM.fullmatch(title)
        if not p:
            continue
        if day is None:
            raise ValueError("Problem heading found without preceding Day heading")
        # Only accept sibling-contained problem text. Layout variants must be
        # investigated separately rather than silently creating corrupt JSON.
        chunks = []
        cursor = heading.next_sibling
        while cursor is not None:
            if isinstance(cursor, Tag) and re.fullmatch(r"h[1-6]", cursor.name or ""):
                break
            if isinstance(cursor, Tag) and STOP.fullmatch(cursor.get_text(" ", strip=True)):
                break
            if isinstance(cursor, NavigableString):
                if cursor.strip():
                    chunks.append(str(cursor).strip())
            elif isinstance(cursor, Tag):
                chunks.append(render(cursor))
            cursor = cursor.next_sibling
        statement = clean("\n".join(chunks))
        flags = []
        if len(statement) < 30:
            flags.append("empty_or_too_short")
        if "[MATH_REQUIRES_REVIEW]" in statement:
            flags.append("math_requires_review")
        if "[FIGURE_REQUIRES_REVIEW]" in statement:
            flags.append("figure_requires_review")
        if re.search(r"(?i)official solution|show solution", statement):
            flags.append("possible_solution_leak")
        records.append({
            "year": year, "day": day, "number": int(p[1]),
            "statement_candidate": statement,
            "review_flags": flags, "statement_verified": False,
            "publication_eligible": False
        })
    keys = [(x["day"], x["number"]) for x in records]
    if len(keys) != len(set(keys)):
        raise ValueError("Duplicate year/day/problem")
    if not records:
        raise ValueError("No problems extracted")
    return records

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--archive", required=True, type=pathlib.Path)
    parser.add_argument("--output", required=True, type=pathlib.Path)
    args = parser.parse_args()
    manifest = json.loads((args.archive / "manifest.json").read_text(encoding="utf-8"))
    records, failures = [], []
    for source in manifest["sources"]:
        if source["source"] != "studolymp_statements":
            continue
        year = source["year"]
        try:
            raw = (args.archive / source["path"]).read_text(encoding="utf-8")
            extracted = extract(raw, year)
            expected = EXPECTED_COUNTS[year]
            if len(extracted) != expected:
                raise ValueError(f"Year {year}: extracted {len(extracted)} problems, expected {expected}")
            if sorted(x["number"] for x in extracted) != list(range(1, expected + 1)):
                raise ValueError(f"Year {year}: missing or duplicated official problem numbers")
            for item in extracted:
                item["source_url"] = source["resolved_url"]
                item["source_sha256"] = source["sha256"]
            records.extend(extracted)
            print("STAGED", year, len(extracted), flush=True)
        except (ValueError, OSError, UnicodeError) as exc:
            failures.append({"year": year, "error": str(exc)})
            print("FAIL", year, str(exc), flush=True)
    records.sort(key=lambda r: (r["year"], r["day"], r["number"]))
    output = {
        "status": "UNVERIFIED_CANDIDATES_NOT_FOR_PUBLICATION",
        "years_expected": manifest["years_requested"],
        "years_staged": sorted({r["year"] for r in records}),
        "problem_candidates": len(records),
        "expected_count": sum(EXPECTED_COUNTS[y] for y in manifest["years_requested"]),
        "counts_by_year": {
            str(y): sum(r["year"] == y for r in records)
            for y in manifest["years_requested"]
        },
        "candidates": records,
        "failures": failures,
        "note": "Do not publish: all equations, full text, authorship and numbering need comparison to original official papers."
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if (failures or len(output["years_staged"]) != len(manifest["years_requested"])
            or len(records) != output["expected_count"]):
        raise SystemExit("Statement staging incomplete; inspect report artifact")

if __name__ == "__main__":
    main()
