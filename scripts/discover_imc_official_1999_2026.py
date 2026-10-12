#!/usr/bin/env python3
"""Auditable source discovery for all as-yet-unchecked IMC years 1999–2026.

Source acquisition is NOT full statement verification. Never automatically
set statement_verified=true from HTML/PDF text extraction or OCR similarity.
"""
import concurrent.futures
import datetime
import hashlib
import json
import pathlib
import re
import urllib.request
from html.parser import HTMLParser
from urllib.parse import urljoin

YEARS=list(range(1999,2027))
EXPECTED={**{y:12 for y in range(1999,2009)},**{y:10 for y in range(2009,2020)},**{y:8 for y in range(2020,2023)},**{y:10 for y in range(2023,2027)}}
OUT=pathlib.Path("staged/imc-official-1999-2026")
HEADERS={"User-Agent":"Mozilla/5.0 Eisatopon-IMC-source-review/1.0"}
class A(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links=[]
    def handle_starttag(self,tag,attrs):
        if tag=="a":
            d=dict(attrs)
            self.links.append((d.get("href",""),""))
def get(url):
    req=urllib.request.Request(url,headers=HEADERS)
    with urllib.request.urlopen(req,timeout=24) as response:
        body=response.read(5_000_001)
        ctype=response.headers.get("Content-Type","")
        final=response.geturl()
    if len(body)>5_000_000 or not body:
        raise ValueError("empty or excessively large source")
    return body,ctype,final
def check_year(year):
    url=f"https://www.imc-math.org.uk/?item=problems&year={year}"
    record={"year":year,"expected_statements":EXPECTED[year],"official_url":url,"official_page_readable":False,"official_pdf_links":[],"warnings":[]}
    try:
        body,typ,final=get(url)
        if "html" not in typ.lower():raise ValueError("non-HTML annual page")
        record["official_page_readable"]=True
        record["sha256"]=hashlib.sha256(body).hexdigest()
        record["resolved_url"]=final
        html=body.decode("utf-8","replace")
        (OUT/str(year)).mkdir(parents=True,exist_ok=True)
        (OUT/str(year)/"official.html").write_bytes(body)
        parser=A();parser.feed(html)
        links=[]
        for href,_ in parser.links:
            full=urljoin(final,href)
            if re.search(r"\.pdf(?:\?|$)",full,re.I) and ("imc-math.org.uk" in full):
                links.append(full)
        record["official_pdf_links"]=sorted(set(links))
        if not links:
            record["warnings"].append("Official page has no directly linked PDFs; may use per-problem HTML pages")
        if f"{year}" not in html:
            record["warnings"].append("Annual page does not visibly contain target year")
    except Exception as e:
        record["warnings"].append(f"Official source request failed: {type(e).__name__}: {e}")
    return record

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        entries=sorted(pool.map(check_year,YEARS),key=lambda r:r["year"])
    manifest={
        "created_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "status":"SOURCE_DISCOVERY_ONLY_NOT_VERIFICATION",
        "publication_eligible":False,
        "years":entries,
        "expected_problem_count":sum(EXPECTED.values()),
        "verified_statement_count_added":0,
        "method":"Fetch official year archive HTML and record source links, sha256, and access failures. Do not certify statements.",
        "permission_status":"Owner reports explicit oral permission to publish problems; exact scope, identity of grantor and any restrictions not independently recorded."
    }
    (OUT/"manifest.json").write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+"\n",encoding="utf8")
    good=sum(x["official_page_readable"] for x in entries)
    print(f"IMC 1999–2026 official source pages accessed: {good}/{len(entries)}")
    print(f"Research statements awaiting original-document visual comparison: {sum(EXPECTED.values())}")
    for x in entries:
        print(x["year"],"OK" if x["official_page_readable"] else "FAIL","PDF links",len(x["official_pdf_links"]),"; ".join(x["warnings"])[:200],flush=True)
    if good != len(entries): raise SystemExit("Some official year pages inaccessible; source acquisition incomplete")
if __name__=="__main__":main()
