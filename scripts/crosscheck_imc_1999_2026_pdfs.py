#!/usr/bin/env python3
"""Cross-reference IMC 1999–2026 draft statements against official downloadable PDFs.

Heuristic report ONLY: words-in-official-document are not exact math fidelity,
particularly for scanned PDFs, integrals, matrices and diagrams. No writes
to the source JSON, no statement_verified changes, no publication.
"""
import concurrent.futures
import hashlib
import json
import pathlib
import re
import urllib.request
import urllib.parse
from collections import Counter
from html.parser import HTMLParser

import fitz

ROOT=pathlib.Path("staged/imc-1999-2026-pdf-crosscheck")
REVIEW=pathlib.Path("undergraduate/IMC-1994-2026-review.json")
YEARS=list(range(1999,2027))
class PDFLinks(HTMLParser):
    def __init__(self):
        super().__init__();self.items=[];self.href=None;self.label=[]
    def handle_starttag(self,tag,attrs):
        if tag=="a":
            self.href=dict(attrs).get("href","");self.label=[]
    def handle_data(self,data):
        if self.href is not None:self.label.append(data)
    def handle_endtag(self,tag):
        if tag=="a" and self.href is not None:
            self.items.append({"href":self.href,"label":" ".join(self.label).strip()})
            self.href=None;self.label=[]
def fetch(url):
    req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0 Eisatopon-IMC-quality-review/1.0"})
    with urllib.request.urlopen(req,timeout=35) as r:return r.read(14_000_001)
def words(s):
    return Counter(x for x in re.findall(r"[a-z]{4,}",s.lower()) if x not in {"then","with","that","this","such","where","which","from","given","show","prove","every","there","find","have","into","real","over","does","what","each","number","problem","value","values"})
def compare(probl,pdftext):
    # Lexical corroboration only, never original-formula certification.
    q=words(re.sub(r"\\[A-Za-z]+|[{}$]"," ",probl))
    t=words(pdftext)
    m=sum(min(count,t[word]) for word,count in q.items())
    denom=sum(q.values())
    return round(m/denom,3) if denom else None

def annual(y,drafts):
    out={"year":y,"official_year_url":f"https://www.imc-math.org.uk/?item=problems&year={y}","pdfs":[],"problems":[],"errors":[]}
    try:
        html=fetch(out["official_year_url"]).decode("utf8","replace")
        parser=PDFLinks();parser.feed(html)
        pdfs={}
        for item in parser.items:
            u=urllib.parse.urljoin(out["official_year_url"],item["href"])
            if not re.search(r"\.pdf(?:$|\?)",u,re.I) or "imc-math.org.uk" not in urllib.parse.urlsplit(u).hostname:continue
            if re.search(r"marking|solution",item["label"],re.I) and not re.search(r"problems and solutions",item["label"],re.I):continue
            pdfs.setdefault(u,item["label"])
        if not pdfs:raise ValueError("No official exam PDF links")
        texts=[]
        for url,label in sorted(pdfs.items()):
            try:
                raw=fetch(url)
                if not raw.startswith(b"%PDF"):raise ValueError("non-PDF response")
                doc=fitz.open(stream=raw,filetype="pdf")
                page_text=[page.get_text(sort=True) for page in doc]
                texts.append((url,"\n".join(page_text)))
                out["pdfs"].append({"url":url,"label":label,"pages":len(doc),"bytes":len(raw),"sha256":hashlib.sha256(raw).hexdigest(),"extractable_chars":sum(map(len,page_text))})
            except Exception as e:
                out["errors"].append(f"{url}: {type(e).__name__}: {e}")
        for p in drafts:
            candidates=[(url,compare(p["problem"],txt)) for url,txt in texts]
            best=max(candidates,key=lambda x:x[1] if x[1] is not None else -1) if candidates else (None,None)
            out["problems"].append({"number":p["number"],"best_pdf_url":best[0],"lexical_overlap":best[1],"source_document_correlated":best[1] is not None and best[1]>=0.35,"statement_verified":False,"review_required":"exact math and figures must be visually compared"})
        if len(out["problems"])!=len(drafts):out["errors"].append("Draft count mismatch")
    except Exception as e:
        out["errors"].append(f"annual: {type(e).__name__}: {e}")
    return out

def main():
    data=json.loads(REVIEW.read_text(encoding="utf8"))
    by_year={item["year"]:item["problems"] for item in data["years"]}
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
        results=list(pool.map(lambda y:annual(y,by_year[y]),YEARS))
    problems=sum(len(x["problems"]) for x in results)
    ok=sum(bool(x["pdfs"]) for x in results)
    high=sum(p["source_document_correlated"] for x in results for p in x["problems"])
    errors=sum(len(x["errors"]) for x in results)
    report={"status":"OFFICIAL_PDF_LEXICAL_CORROBORATION_ONLY_NOT_SOURCE_VERIFICATION",
            "year_range":"1999–2026","expected_statements":294,"checked_statements":problems,
            "years_with_downloadable_and_readable_pdfs":ok,
            "lexically_correlated_at_035_threshold":high,
            "source_fidelity_certifications_added":0,"errors":errors,"years":results,
            "warning":"Not a substitute for exact comparison of all mathematical notation, original figures and hypotheses. Cannot set statement_verified=True."}
    ROOT.mkdir(parents=True,exist_ok=True)
    (ROOT/"report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
    print(f"Official IMC PDFs read: {ok}/28 years; problem coverage {problems}/294; lexical corroborations {high}/{problems}; source errors {errors}")
    for x in results:
        score=sum(z["source_document_correlated"] for z in x["problems"])
        print(x["year"],len(x["problems"]),score,len(x["pdfs"]),"PDFs",x["errors"][:2],flush=True)
    if problems!=294 or ok!=28:raise SystemExit("Not all original official PDF documents could be sourced: review report")
if __name__=="__main__":main()
