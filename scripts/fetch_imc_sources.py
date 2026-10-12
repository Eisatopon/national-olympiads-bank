#!/usr/bin/env python3
"""Archive complete IMC annual statement pages with an auditable error manifest.

Only archives sources. It never claims problem transcription or publication.
"""
import argparse
import hashlib
import json
import pathlib
import time
import urllib.error
import urllib.request

FIRST, LAST = 1994, 2026
SOURCES = (
    ("official", "https://www.imc-math.org.uk/?item=problems&year={year}"),
    ("studolymp_statements", "https://studolymp.com/imc/{year}/problems"),
)

def fetch(url):
    request = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (compatible; Eisatopon-IMC-source-verification/1.0)",
        "Accept": "text/html,application/xhtml+xml",
    })
    with urllib.request.urlopen(request, timeout=40) as response:
        final_url = response.geturl()
        content_type = response.headers.get("Content-Type", "")
        raw = response.read(4_000_001)
    if len(raw) > 4_000_000 or len(raw) < 400:
        raise ValueError("Unexpected page size " + str(len(raw)))
    if "html" not in content_type.lower():
        raise ValueError("Expected HTML; got " + content_type)
    text = raw.decode("utf-8", errors="replace")
    if "studolymp.com" in url and not ("Problem 1" in text or "Problem 2" in text):
        raise ValueError("Annual statement page lacks expected problem headings")
    return final_url, raw

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=pathlib.Path)
    parser.add_argument("--years", type=int, nargs="+", default=list(range(FIRST, LAST + 1)))
    args = parser.parse_args()
    years = sorted(set(args.years))
    if not years or any(y < FIRST or y > LAST for y in years):
        parser.error("Years must be between 1994 and 2026")
    root = args.output
    root.mkdir(parents=True, exist_ok=True)
    records, errors = [], []
    for year in years:
        for name, template in SOURCES:
            url = template.format(year=year)
            try:
                final_url, body = fetch(url)
                dest = root / str(year) / (name + ".html")
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(body)
                record = {
                    "year": year, "source": name, "requested_url": url,
                    "resolved_url": final_url, "path": str(dest.relative_to(root)),
                    "bytes": len(body), "sha256": hashlib.sha256(body).hexdigest()
                }
                records.append(record)
                print(f"OK {year} {name}: {len(body)} bytes", flush=True)
            except (urllib.error.URLError, ValueError, TimeoutError, OSError) as exc:
                error = {"year": year, "source": name, "url": url, "error": str(exc)}
                errors.append(error)
                print(f"FAIL {year} {name}: {exc}", flush=True)
            time.sleep(0.2)
    manifest = {
        "competition": "IMC", "years_requested": years,
        "sources_expected": len(years) * len(SOURCES),
        "sources_fetched": len(records), "sources": records,
        "errors": errors, "status": "source_only_not_verified_or_imported",
        "publication_note": "Source pages are not a checked mathematical JSON archive."
    }
    (root / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"SUMMARY {len(records)}/{len(years)*len(SOURCES)} pages, {len(errors)} failures", flush=True)
    if errors:
        raise SystemExit("Incomplete IMC source archive; see failure list above and manifest.json")

if __name__ == "__main__":
    main()
