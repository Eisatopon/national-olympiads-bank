#!/usr/bin/env python3
"""Fetch the 41 primary TeX problem sheets (1985–2025) for Putnam review.

This is a source-acquisition tool. It neither ingests solutions nor creates
published problems. Preserve each TeX byte-for-byte for mathematical checking.
"""
import argparse
import hashlib
import json
from pathlib import Path
import urllib.request
import urllib.error

FIRST, LAST = 1985, 2025

def fetch(year):
    url = f"https://kskedlaya.org/putnam-archive/{year}.tex"
    request = urllib.request.Request(url, headers={
        "User-Agent": "Eisatopon-Putnam-review/1.0 (educational source audit)",
        "Accept": "application/x-tex,text/plain,*/*",
    })
    with urllib.request.urlopen(request, timeout=40) as response:
        final = response.geturl()
        data = response.read(1_500_001)
    if len(data) < 250 or len(data) > 1_500_000:
        raise ValueError("Unexpected TeX source size")
    source = data.decode("utf-8", errors="replace")
    if not any(x in source for x in (r"\begin{document}", r"\input", r"\problem", r"\item")):
        raise ValueError("Source lacks recognizable LaTeX document/problem structure")
    return final, data

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--output", required=True, type=Path)
    p.add_argument("--years", nargs="+", type=int, default=list(range(FIRST, LAST+1)))
    opts = p.parse_args()
    years = sorted(set(opts.years))
    if not years or years[0] < FIRST or years[-1] > LAST:
        p.error("The TeX source archive supports 1985–2025 only")
    opts.output.mkdir(parents=True, exist_ok=True)
    sources, errors = [], []
    for year in years:
        url = f"https://kskedlaya.org/putnam-archive/{year}.tex"
        try:
            final, body = fetch(year)
            rel = f"{year}.tex"
            (opts.output / rel).write_bytes(body)
            sources.append({
                "year": year, "kind": "problem_sheet_tex", "url": final,
                "file": rel, "sha256": hashlib.sha256(body).hexdigest(), "bytes": len(body)
            })
            print(f"OK {year}: {len(body)} bytes", flush=True)
        except (OSError, ValueError, UnicodeError, urllib.error.URLError) as exc:
            errors.append({"year": year, "url": url, "error": str(exc)})
            print(f"FAIL {year}: {exc}", flush=True)
    report = {
        "competition": "Putnam", "range": "1985–2025",
        "years_requested": years, "downloaded": len(sources),
        "sources": sources, "errors": errors,
        "status": "SOURCE_FILES_ONLY_NOT_TRANSCRIBED",
        "rights_note": "Project owner reports oral permission from MAA colleagues; authority and scope not independently documented.",
        "warning": "Not a problem JSON import; early 1938–1984 papers require different original sources."
    }
    (opts.output / "manifest.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    if errors or len(sources) != len(years):
        raise SystemExit("Some Putnam TeX sources could not be fetched; see manifest")
    print(f"COMPLETE: {len(sources)} original Putnam TeX problem sheets acquired.", flush=True)

if __name__ == "__main__":
    main()
