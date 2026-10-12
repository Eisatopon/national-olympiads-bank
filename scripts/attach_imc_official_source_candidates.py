#!/usr/bin/env python3
"""Attach provenance hints, not unearned verifications, to all IMC 1999–2026 statements."""
import json
from pathlib import Path

report=json.loads(Path("staged/imc-1999-2026-pdf-crosscheck/report.json").read_text(encoding="utf8"))
path=Path("undergraduate/IMC-1994-2026-review.json")
data=json.loads(path.read_text(encoding="utf8"))
assert report["expected_statements"]==294
assert report["checked_statements"]==294
assert report["source_fidelity_certifications_added"]==0
assert report["years_with_downloadable_and_readable_pdfs"]==28
by_year={int(y["year"]):y for y in data["years"]}
issues=[]
seen=set()
for yr in report["years"]:
    year=int(yr["year"])
    assert 1999<=year<=2026
    assert not yr["errors"],(year,yr["errors"])
    problems={p["number"]:p for p in by_year[year]["problems"]}
    for entry in yr["problems"]:
        p=problems[int(entry["number"])]
        key=(year,p["number"])
        assert key not in seen
        seen.add(key)
        assert p["statement_verified"] is False,key
        pdf=entry["best_pdf_url"]
        assert pdf and pdf.startswith("https://") and "imc-math.org.uk" in pdf,key
        p["official_pdf_candidate_url"]=pdf
        p["official_pdf_lexical_overlap"]=entry["lexical_overlap"]
        p["official_pdf_crosscheck_method"]="automated lexical screening only; exact mathematics and figures require visual review"
        flags=set(p.get("review_flags",[]))
        flags.add("original_official_pdf_exact_statement_review_pending")
        if not entry["source_document_correlated"]:
            flags.add("low_lexical_overlap_priority_review")
            issues.append(f"{year}-{p['number']} overlap={entry['lexical_overlap']}")
        p["review_flags"]=sorted(flags)
assert len(seen)==294,len(seen)
assert data["publication_eligible"] is False
path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
Path("research/imc").mkdir(parents=True,exist_ok=True)
Path("research/imc/official-1999-2026-crosscheck.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
print(f"Recorded organizer PDF provenance for {len(seen)} IMC statements, 0 incorrectly certified; {len(issues)} require priority visual review")
for issue in issues:print("FLAG",issue)
