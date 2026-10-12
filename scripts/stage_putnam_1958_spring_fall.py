#!/usr/bin/env python3
"""Stage distinct Spring/Fall Putnam 1958 source statements for review only."""
import json
import pathlib
import urllib.request

SOURCE = "https://raw.githubusercontent.com/YurenHao0426/PutnamGAP/main/dataset"
OUT = pathlib.Path("staged/Putnam-1958-spring-fall-raw-review.json")

def retrieve(url):
    request = urllib.request.Request(url, headers={"User-Agent": "Eisatopon-archival-review/1.0"})
    with urllib.request.urlopen(request, timeout=45) as response:
        return json.load(response)

def main():
    editions=[]
    for edition, prefix in (("Spring","1958"), ("Fall","1958-2")):
        records=[]
        for section in "AB":
            for number in range(1,8):
                label=f"{section}{number}"
                source_id=f"{prefix}-{section}-{number}"
                path=f"{source_id}.json"
                item=retrieve(f"{SOURCE}/{path}")
                statement=item.get("question")
                if item.get("index") != source_id or not isinstance(statement,str) or len(statement.strip()) < 30:
                    raise RuntimeError(f"Missing or invalid source record: {source_id}")
                records.append({
                    "number":label,"problem":statement.strip(),
                    "source_id":source_id,
                    "source_url":f"https://github.com/YurenHao0426/PutnamGAP/blob/main/dataset/{path}",
                    "topics":[],"problem_dna":[],
                    "statement_verified":False,
                    "review_flags":["OCR_math_symbols_must_be_checked","requires_authoritative_original_page_comparison"]
                })
        assert len(records)==14
        editions.append({"year":1958,"edition":edition,"source_prefix":prefix,"problems":records})
        print(f"1958 {edition}: {len(records)}/14 source-linked research records",flush=True)
    assert len({p["source_id"] for e in editions for p in e["problems"]})==28
    payload={
        "competition":"William Lowell Putnam Mathematical Competition",
        "short_name":"Putnam",
        "year":1958,
        "status":"RAW_TRANSCRIPT_REQUIRES_ORIGINAL_PDF_FIDELITY_REVIEW",
        "publication_eligible":False,
        "problem_count":28,
        "source_dataset":"https://github.com/YurenHao0426/PutnamGAP",
        "rights_note":"Source access does not grant public reproduction rights.",
        "note":"Spring and Fall 1958 are separate competitions; unverified OCR research candidates only.",
        "editions":editions,"errors":[]
    }
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
    print("STAGED ONLY: 28/28 source-linked 1958 records, two distinct editions",flush=True)

if __name__=="__main__":
    main()
