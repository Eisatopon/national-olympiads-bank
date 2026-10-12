#!/usr/bin/env python3
"""Archive IMC official annual pages and individual Studolymp problem pages.

Never publishes statements. Failure is explicit, with a manifest artifact.
"""
import argparse
import hashlib
from html.parser import HTMLParser
import json
import pathlib
import re
import time
import urllib.error
import urllib.request
from urllib.parse import urljoin, urlsplit

FIRST, LAST = 1994, 2026
EXPECTED = {
    **{y: 12 for y in range(1994, 2009)},
    **{y: 10 for y in range(2009, 2020)},
    **{y: 8 for y in range(2020, 2023)},
    **{y: 10 for y in range(2023, 2027)},
}
assert len(EXPECTED) == 33 and sum(EXPECTED.values()) == 354
PATTERN = re.compile(r"^/imc/problems/imc-(\d{4})-d([12])-p(\d+)/?$")

class Links(HTMLParser):
    def __init__(self, year):
        super().__init__()
        self.year = year
        self.problems = {}

    def handle_starttag(self, tag, attrs):
        if tag != "a":
            return
        href = dict(attrs).get("href", "")
        url = urljoin("https://studolymp.com/", href)
        parsed = urlsplit(url)
        m = PATTERN.fullmatch(parsed.path)
        if parsed.hostname not in ("studolymp.com", "www.studolymp.com") or not m:
            return
        year, day, number = map(int, m.groups())
        if year == self.year:
            key = (day, number)
            if key in self.problems and self.problems[key] != url:
                raise ValueError("Conflicting links for problem " + str(key))
            self.problems[key] = url

def fetch(url):
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (compatible; Eisatopon-IMC-archive/1.0)",
        "Accept": "text/html,application/xhtml+xml",
    })
    with urllib.request.urlopen(req, timeout=30) as r:
        final_url = r.geturl()
        content_type = r.headers.get("Content-Type", "")
        raw = r.read(4_000_001)
    if not (400 <= len(raw) <= 4_000_000) or "html" not in content_type.lower():
        raise ValueError("Invalid HTML body or size, type=" + content_type)
    return final_url, raw

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", type=pathlib.Path, required=True)
    ap.add_argument("--years", type=int, nargs="+", default=list(range(FIRST, LAST + 1)))
    a = ap.parse_args()
    years = sorted(set(a.years))
    if not years or min(years) < FIRST or max(years) > LAST:
        ap.error("Years must be in the range 1994–2026")
    a.output.mkdir(parents=True, exist_ok=True)
    records, errors = [], []

    def save(year, label, url, relpath, day=None, number=None):
        try:
            final, body = fetch(url)
            path = a.output / relpath
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(body)
            item = {"year": year, "source": label, "requested_url": url,
                    "resolved_url": final, "path": str(relpath),
                    "bytes": len(body), "sha256": hashlib.sha256(body).hexdigest()}
            if day is not None:
                item.update(day=day, number=number)
            records.append(item)
            print(f"OK {year} {label} {number or ''} {len(body)} bytes", flush=True)
            return body
        except (OSError, urllib.error.URLError, ValueError, TimeoutError) as e:
            errors.append({"year": year, "source": label, "url": url, "error": str(e)})
            print(f"FAIL {year} {label}: {e}", flush=True)
            return None

    for year in years:
        official = "https://www.imc-math.org.uk/?item=problems&year=" + str(year)
        save(year, "official", official, pathlib.Path(str(year)) / "official.html")
        year_url = f"https://studolymp.com/imc/{year}"
        body = save(year, "studolymp_index", year_url, pathlib.Path(str(year)) / "index.html")
        if body is None:
            continue
        try:
            parser = Links(year)
            parser.feed(body.decode("utf-8", errors="replace"))
            got = sorted(parser.problems)
            if len(got) != EXPECTED[year]:
                raise ValueError(f"Found {len(got)} problems, expected {EXPECTED[year]}")
            if [n for _, n in got] != list(range(1, EXPECTED[year] + 1)):
                raise ValueError("Official problem numbers incomplete or duplicated")
            if any(d not in (1, 2) for d, _ in got):
                raise ValueError("Unknown day identifier")
        except ValueError as e:
            errors.append({"year": year, "source": "problem_inventory", "error": str(e)})
            print(f"FAIL inventory {year}: {e}", flush=True)
            continue
        for (day, number), url in sorted(parser.problems.items()):
            rel = pathlib.Path(str(year)) / "problems" / f"d{day}-p{number}.html"
            save(year, "studolymp_problem", url, rel, day, number)
            time.sleep(0.07)
        time.sleep(0.15)
    downloaded = [r for r in records if r["source"] == "studolymp_problem"]
    full_range = years == list(range(FIRST, LAST+1))
    if len(downloaded) != sum(EXPECTED[y] for y in years):
        errors.append({"source": "count", "expected": sum(EXPECTED[y] for y in years),
                       "actual": len(downloaded)})
    manifest = {
        "competition": "IMC", "years_requested": years,
        "expected_problem_pages": sum(EXPECTED[y] for y in years),
        "downloaded_problem_pages": len(downloaded),
        "sources": records, "errors": errors,
        "status": "RAW_SOURCE_PAGES_ONLY_NOT_VERIFIED"
    }
    (a.output / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"SUMMARY problem pages {len(downloaded)}/{manifest['expected_problem_pages']}; errors {len(errors)}", flush=True)
    if errors:
        raise SystemExit(1)

if __name__ == "__main__":
    main()
