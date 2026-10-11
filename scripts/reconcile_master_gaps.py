#!/usr/bin/env python3
"""Reconcile the curated gap register against CURRENT repository data.

Run: python scripts/reconcile_master_gaps.py
Use --strict to exit nonzero when a recorded missing paper now exists.
Never automatically close a gap: a year alone does not prove completeness.
"""
import argparse
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTER = ROOT / "docs/master-gap-register.json"


def reconcile():
    doc = json.loads(REGISTER.read_text(encoding="utf-8"))
    records = doc["items"]
    ids = [r["id"] for r in records]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate Master Gap IDs")
    found = []
    missing_files = []
    for r in records:
        path = r.get("collection")
        if not path:
            continue
        fullpath = ROOT / path
        if not fullpath.is_file():
            missing_files.append((r["id"], path))
            continue
        obj = json.loads(fullpath.read_text(encoding="utf-8"))
        years = obj.get("years", [])
        year = r.get("year")
        if year is None:
            continue
        corresponding = [y for y in years if str(y.get("year")) == str(year)]
        if not corresponding:
            continue
        num = r.get("number")
        matching = (
            any(str(p.get("number")) == str(num) for y in corresponding for p in y.get("problems", []))
            if num is not None else True
        )
        if matching and r.get("type") in ("paper", "problem"):
            found.append((r["id"], path, year, num))
    return records, found, missing_files


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict", action="store_true", help="Fail if unresolved missing-paper/problem records are now present")
    args = parser.parse_args()
    records, found, missing_files = reconcile()
    counts = Counter(r["type"] for r in records)
    print(f"Master gaps: {len(records)} | open: {sum(r['status']=='open' for r in records)}")
    print("By type:", ", ".join(f"{k}={v}" for k, v in sorted(counts.items())))
    for id_, path, year, num in found:
        print(f"REVIEW FOR CLOSURE: {id_}: {path} year={year} problem={num}; verify full original before closing")
    for id_, path in missing_files:
        print(f"MISSING COLLECTION PATH: {id_}: {path}")
    print(f"Possible stale gaps: {len(found)}; missing referenced collection files: {len(missing_files)}")
    return 1 if args.strict and (found or missing_files) else 0


if __name__ == "__main__":
    raise SystemExit(main())
