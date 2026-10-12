#!/usr/bin/env python3
"""Inventory official VJIMC statement PDFs; never invent or auto-publish problems.

Usage:
    python scripts/vjimc_collect.py --output docs/vjimc-official-manifest.json
    python scripts/vjimc_collect.py --download --output docs/vjimc-official-manifest.json
Run from a network-enabled machine. Downloads are confined to a gitignored
working directory by default; each URL must be obtained from organizer HTML.
"""
import argparse
import hashlib
import html.parser
import json
import pathlib
import re
import urllib.parse
import urllib.request
from datetime import date

ARCHIVE = "https://jarnik.osu.cz/problems"
CURRENT = "https://vjimc.osu.cz/j32results"
BASE = "https://jarnik.osu.cz"
ABSENT = {2020, 2021, 2023}
YEARS = [y for y in range(1991, 2027) if y not in ABSENT]
USER_AGENT = "Eisatopon-Research/1.0 (+official source inventory)"


def get(url):
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=35) as response:
        return response.read(), response.geturl()


class Anchors(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.href = None
        self.label = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self.href = dict(attrs).get("href")
            self.label = []

    def handle_data(self, value):
        if self.href is not None:
            self.label.append(value)

    def handle_endtag(self, tag):
        if tag == "a" and self.href is not None:
            self.links.append((self.href, " ".join(" ".join(self.label).split())))
            self.href = None
            self.label = []


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--output", default="docs/vjimc-official-manifest.json")
    p.add_argument("--download", action="store_true")
    p.add_argument("--download-dir", default=".cache/vjimc-sources")
    args = p.parse_args()
    raw, final_url = get(ARCHIVE)
    parser = Anchors()
    parser.feed(raw.decode("utf-8", errors="replace"))
    links = []
    for href, label in parser.links:
        url = urllib.parse.urljoin(final_url, href)
        parts = urllib.parse.urlsplit(url)
        if parts.hostname not in {"jarnik.osu.cz", "vjimc.osu.cz"}:
            continue
        name = pathlib.PurePosixPath(parts.path).name
        if not re.fullmatch(r"j\d{1,2}problems[12]?\.pdf", name, re.IGNORECASE):
            continue
        m = re.fullmatch(r"j(\d{1,2})problems([12]?)\.pdf", name, re.IGNORECASE)
        edition = int(m.group(1))
        year = 1990 + edition if edition <= 29 else {30: 2022, 31: 2024, 32: 2025, 33: 2026}.get(edition)
        if year is None or year not in YEARS:
            continue
        item = {"year": year, "edition": edition, "url": url, "anchor_label": label,
                "category": {"1": "I", "2": "II"}.get(m.group(2), "requires_manual_check"),
                "pdf_sha256": None, "status": "source_discovered_not_verified"}
        if args.download:
            try:
                data, resolved_url = get(url)
                if not data.startswith(b"%PDF-"):
                    raise ValueError("Not a PDF")
                dest = pathlib.Path(args.download_dir)
                dest.mkdir(parents=True, exist_ok=True)
                filename = f"{year}-{name}"
                (dest / filename).write_bytes(data)
                item.update(pdf_sha256=hashlib.sha256(data).hexdigest(),
                            local_path=str(dest / filename),
                            resolved_url=resolved_url,
                            status="pdf_downloaded_statement_review_pending")
            except Exception as ex:
                item["download_error"] = str(ex)
        links.append(item)

    result = {"competition": "Vojtěch Jarník International Mathematical Competition",
              "archive": ARCHIVE, "generated_date": date.today().isoformat(),
              "held_years": YEARS, "years_without_competition": sorted(ABSENT),
              "files": sorted(links, key=lambda x: (x["year"], x["category"], x["url"])),
              "caution": "Inventory only. PDFs and statements require individual source checks; no solutions."}
    out = pathlib.Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{len(links)} linked PDF sources discovered; {len(YEARS)} held years. Output: {out}")
    missing = sorted(set(YEARS) - {a["year"] for a in links})
    if missing:
        print("Years without recognized source links:", missing)
    return 0 if links else 1


if __name__ == "__main__":
    raise SystemExit(main())
