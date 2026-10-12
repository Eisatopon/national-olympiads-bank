#!/usr/bin/env python3
"""Stage sixty 1975-1979 PutnamGAP statement candidates, no solutions."""
import argparse
import json
import pathlib
import re
import time
import urllib.request

SOURCE="https://raw.githubusercontent.com/YurenHao0426/PutnamGAP/main/dataset"
EXPECTED=[f"{s}{i}" for s in "AB" for i in range(1,7)]

def download(url):
    req=urllib.request.Request(url,headers={"User-Agent":"Eisatopon-archival-audit/1.0","Accept":"application/json"})
    last=None
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req,timeout=40) as response:
                return json.load(response)
        except Exception as err:
            last=err
            if attempt<3: time.sleep(2*(attempt+1))
    raise RuntimeError(f"Cannot retrieve {url}: {last}")

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",type=pathlib.Path,default=pathlib.Path("undergraduate/Putnam-1975-1979-raw-review.json"))
    args=parser.parse_args()
    years=[]
    errors=[]
    for year in range(1975,1980):
        problems=[]
        for label in EXPECTED:
            source_id=f"{year}-{label[0]}-{label[1]}"
            url=f"{SOURCE}/{source_id}.json"
            try:
                record=download(url)
                assert record.get("index")==source_id, f"Problem identity mismatch: {source_id}"
                statement=record.get("question")
                assert isinstance(statement,str) and len(statement.strip())>=35, f"Missing statement: {source_id}"
                assert not re.search(r"^\s*(?:solution|answer)\s*:",statement,re.I), f"Unexpected solution field: {source_id}"
                problems.append({
                    "number":label,"problem":statement.strip(),"topics":[],"problem_dna":[],
                    "statement_verified":False,"source_id":source_id,
                    "source_url":f"https://github.com/YurenHao0426/PutnamGAP/blob/main/dataset/{source_id}.json",
                    "review_flags":["OCR_may_corrupt_mathematical_symbols","requires_original_MAA_paper_visual_comparison"]
                })
            except Exception as exc:
                errors.append({"year":year,"number":label,"error":str(exc)})
        print(f"{year}: {len(problems)}/12 statement candidates",flush=True)
        years.append({"year":year,
                      "historical_MAA_collection_url":"https://old.maa.org/node/109706",
                      "problems":problems})
    total=sum(len(y["problems"]) for y in years)
    payload={
        "competition":"William Lowell Putnam Mathematical Competition",
        "short_name":"Putnam","first_year":1975,"last_year":1979,
        "status":"RAW_TRANSCRIPT_REQUIRES_ORIGINAL_PDF_FIDELITY_REVIEW",
        "publication_eligible":False,"problem_count":total,
        "source_dataset":"PutnamGAP by Hao, Wan and Zhai; originals reproduced from MAA books",
        "rights_note":"Owner reports oral permission from MAA colleagues; authority and scope not independently verified.",
        "note":"OCR-derived research transcriptions may have damaged formulas and must be checked.",
        "years":years,"errors":errors,
    }
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
    if errors or total!=60 or any([p["number"] for p in y["problems"]]!=EXPECTED for y in years):
        raise SystemExit(f"INCOMPLETE: {total}/60, errors={len(errors)}")
    print("COMPLETE: 60/60 Putnam review records, 1975–1979",flush=True)

if __name__=="__main__":
    main()
