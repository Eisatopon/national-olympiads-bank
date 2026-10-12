#!/usr/bin/env python3
"""Stage historical Putnam 1980–1984 problem candidates from UCSD PDFs.

Never promote PDF text extraction to verified mathematical statements:
old embedded fonts corrupt roots, exponents, integral signs, inequalities.
"""
import argparse
import hashlib
import json
import re
import subprocess
import urllib.request
from pathlib import Path

YEARS=range(1980,1985)
PDF_URL="https://math.ucsd.edu/~pfitz/downloads/putnam/putnam{year}.pdf"
HEADING=re.compile(r"(?m)^\s*([AB])\s*[-–]?\s*([1-6])\s*\.\s*")
ORDER=[f"{s}{i}" for s in "AB" for i in range(1,7)]

def process(year,folder):
    url=PDF_URL.format(year=year)
    req=urllib.request.Request(url,headers={"User-Agent":"Eisatopon mathematical archives (source verification)"})
    with urllib.request.urlopen(req,timeout=45) as r:
        binary=r.read(4_000_001)
    if not binary.startswith(b"%PDF-") or len(binary)>4_000_000:
        raise ValueError("Invalid/oversize exam PDF")
    pdf=folder/f"{year}.pdf";pdf.write_bytes(binary)
    textfile=folder/f"{year}.txt"
    subprocess.run(["pdftotext","-layout","-enc","UTF-8",str(pdf),str(textfile)],check=True,timeout=45)
    raw=textfile.read_text(encoding="utf-8")
    matches=list(HEADING.finditer(raw))
    extracted=[]
    for i,m in enumerate(matches):
        key=m.group(1)+m.group(2)
        piece=raw[m.end():matches[i+1].start() if i+1<len(matches) else len(raw)].strip()
        piece=re.sub(r"(?m)^\s*(FORTY\S*.*|WILLIAM LOWELL PUTNAM MATHEMATICAL COMPETITION|Saturday, .* Examination [AB])\s*$","",piece).strip()
        extracted.append({"number":key,"candidate_raw_pdf_text":piece,
                          "statement_verified":False,"publication_eligible":False,
                          "review_flags":["mathematical_pdf_font_encoding_corruption","compare_every_equation_against_original_pdf_page"]})
    found=[item["number"] for item in extracted]
    expected_ok=found==ORDER
    if not expected_ok:
        raise ValueError(f"Expected all A1–B6 in order, saw {found}")
    if any(len(p["candidate_raw_pdf_text"])<25 for p in extracted):
        raise ValueError("One or more empty/short candidates")
    return {"year":year,"source_pdf_url":url,"source_sha256":hashlib.sha256(binary).hexdigest(),
            "status":"UNVERIFIED_RAW_PDF_TEXT_DO_NOT_PUBLISH","problems":extracted}

def main():
    arg=argparse.ArgumentParser()
    arg.add_argument("--output",type=Path,default=Path("putnam-1980-1984-review"))
    opts=arg.parse_args()
    folder=opts.output;folder.mkdir(parents=True,exist_ok=True)
    years=[];errors=[]
    for year in YEARS:
        try:
            result=process(year,folder)
            years.append(result)
            print(f"OK {year}: {len(result['problems'])} numbered raw candidates",flush=True)
        except Exception as err:
            errors.append({"year":year,"error":str(err)})
            print(f"FAIL {year}: {err}",flush=True)
    report={"competition":"Putnam","scope":"1980–1984","status":"UNVERIFIED_DO_NOT_PUBLISH",
            "years":years,"raw_candidate_count":sum(len(y["problems"]) for y in years),
            "errors":errors,
            "warning":"Mathematical symbols in this PDF text are demonstrably damaged; these are only comparison notes, not publishable statements."}
    (folder/"candidates.json").write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    if errors or len(years)!=5 or report["raw_candidate_count"]!=60:
        raise SystemExit("Incomplete or damaged source acquisition; inspect artifact")

if __name__=="__main__":
    main()
