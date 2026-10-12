#!/usr/bin/env python3
"""Download IMC source pages for independent offline transcription and checking.

This tool deliberately does NOT publish problems or infer mathematical text from
rendered HTML. It preserves the source files for a human-verifiable import.
Usage:
  python scripts/fetch_imc_sources.py --output /tmp/imc-source
  python scripts/fetch_imc_sources.py --output /tmp/imc-source --years 2025 2026
"""
import argparse
import hashlib
import re
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse
import json
import pathlib
import time
import urllib.error
import urllib.request

START, END = 1994, 2026
SOURCES = (
    ("official", "https://www.imc-math.org.uk/?item=problems&year={year}"),
    ("studolymp", "https://studolymp.com/imc/{year}"),
)

def fetch(url):
    req = urllib.request.Request(url, headers={
        "User-Agent": "Eisatopon-IMC-source-archiver/1.0 (educational source verification)",
        "Accept": "text/html",
    })
    with urllib.request.urlopen(req, timeout=35) as response:
        final_url = response.geturl()
        body = response.read(4_000_001)
        content_type = response.headers.get("Content-Type", "")
        if len(body) > 4_000_000:
            raise ValueError("Source HTML is unexpectedly large")
        if "html" not in content_type.lower() or len(body) < 400:
            raise ValueError("Expected a nonempty HTML source: " + content_type)
        return final_url, body

class ProblemLinkParser(HTMLParser):
    """Discover individual problem links from each annual Studolymp page."""
    def __init__(self, year):
        super().__init__()
        self.year = year
        self.links = set()

    def handle_starttag(self, tag, attrs):
        if tag != "a":
            return
        href = dict(attrs).get("href", "")
        full = urljoin("https://studolymp.com/", href)
        path = urlparse(full).path
        m = re.fullmatch(r"/imc/problems/imc-(\\d{4})-d([12])-p(\\d+)", path)
        if m and int(m.group(1)) == self.year and urlparse(full).hostname == "studolymp.com":
            self.links.add((int(m.group(2)), int(m.group(3)), full))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", required=True, type=pathlib.Path)
    ap.add_argument("--years", type=int, nargs="+", default=list(range(START, END + 1)))
    args = ap.parse_args()
    years = sorted(set(args.years))
    if not years or any(y < START or y > END for y in years):
        ap.error("Year outside official IMC archive range 1994–2026")
    root = args.output
    root.mkdir(parents=True, exist_ok=True)
    records = []
    errors = []
    discovered_problems = []
    for year in years:
        for label, template in SOURCES:
            url = template.format(year=year)
            try:
                final_url, content = fetch(url)
                file = root / str(year) / (label + ".html")
                file.parent.mkdir(parents=True, exist_ok=True)
                file.write_bytes(content)
                records.append({
                    "year": year, "source": label, "requested_url": url,
                    "resolved_url": final_url, "path": str(file.relative_to(root)),
                    "bytes": len(content), "sha256": hashlib.sha256(content).hexdigest()
                })
                print("OK", year, label, len(content))
                if label == "studolymp":
                    parser = ProblemLinkParser(year)
                    parser.feed(content.decode("utf-8", errors="replace"))
                    if not parser.links:
                        errors.append({"year": year, "source": label, "error": "No individual problem links found in yearly HTML"})
                    for day, number, problem_url in sorted(parser.links):
                        discovered_problems.append((year, day, number, problem_url))
            except (urllib.error.URLError, ValueError, TimeoutError, OSError) as exc:
                errors.append({"year": year, "source": label, "error": str(exc)})
                print("FAIL", year, label, exc)
            time.sleep(0.3)
    seen = set()
    for year, day, number, url in discovered_problems:
        key = (year, day, number)
        if key in seen:
            errors.append({"year": year, "day": day, "number": number, "error": "Duplicate problem id"})
            continue
        seen.add(key)
        try:
            final_url, content = fetch(url)
            path = root / str(year) / "problems" / ("day" + str(day) + "-p" + str(number) + ".html")
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
            records.append({
                "year": year, "day": day, "number": number, "source": "studolymp_problem",
                "requested_url": url, "resolved_url": final_url,
                "path": str(path.relative_to(root)), "bytes": len(content),
                "sha256": hashlib.sha256(content).hexdigest()
            })
            print("OK PROBLEM", year, day, number)
        except (urllib.error.URLError, ValueError, TimeoutError, OSError) as exc:
            errors.append({"year": year, "day": day, "number": number, "error": str(exc)})
            print("FAIL PROBLEM", year, day, number, exc)
        time.sleep(0.15)
    problem_counts = {str(y): sum(1 for k in seen if k[0] == y) for y in years}
    if years == list(range(START, END + 1)) and len(seen) != 354:
        errors.append({"error": "Problem inventory does not equal the archive's advertised 354",
                       "discovered": len(seen), "expected": 354})
    manifest = {
        "competition": "IMC", "years_requested": years,
        "sources_expected": len(years) * len(SOURCES),
        "sources_fetched": len(records),
        "problems_discovered": len(seen), "problem_counts_by_year": problem_counts,
        "sources": records, "errors": errors,
        "status": "source_only_not_verified_or_imported",
        "publication_note": "Never present this manifest as a completed problem import."
    }
    (root / "manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    if errors:
        raise SystemExit("Incomplete source download: " + str(len(errors)) + " failures")
    print("All discovered source pages downloaded. Statement verification is still required.")

if __name__ == "__main__":
    main()
