#!/usr/bin/env python3
"""Collect indexed VJIMC organizer source PDFs, preserving unreviewed status."""
import json, re, subprocess, tempfile, urllib.request, urllib.error, urllib.parse, ssl, hashlib
from pathlib import Path

manifest=json.loads(Path('metadata/vojtech-jarnik-editions-source-manifest.json').read_text())
results=[]
extracted=[]
for ed in manifest['editions']:
    n=ed['edition']; year=ed['year']
    prefix=f'j{n:02d}'
    attempts=[]
    found=[]
    # Categories are separate in much of the organizer's archive; a generic older
    # PDF may contain a single category. Never infer category solely from suffix.
    for suffix in ('problems1.pdf','problems2.pdf','problems.pdf'):
        result=None
        for host in ('https://jarnik.osu.cz','https://vjimc.osu.cz'):
            url=f'{host}/storage/uploads/{prefix}{suffix}'
            try:
                req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
                transport_verified = True
                try:
                    with urllib.request.urlopen(req,timeout=8) as h:
                        data=h.read(10000000)
                except urllib.error.URLError as ex:
                    if not isinstance(ex.reason, ssl.SSLCertVerificationError):
                        raise
                    # Public organizer papers only, no credentials or publication.
                    # Keep the transport exception explicit for source review.
                    transport_verified = False
                    context = ssl._create_unverified_context()
                    with urllib.request.urlopen(req,timeout=8,context=context) as h:
                        if urllib.parse.urlparse(h.geturl()).hostname not in ("jarnik.osu.cz", "vjimc.osu.cz"):
                            raise ValueError("unexpected_redirect_host")
                        data=h.read(10000000)
                if not data.startswith(b'%PDF'): raise ValueError('not_pdf')
                pdf_dir=Path('out/vjimc-pdfs');pdf_dir.mkdir(parents=True,exist_ok=True)
                (pdf_dir/(prefix+suffix)).write_bytes(data)
                with tempfile.TemporaryDirectory() as tmp:
                    fp=Path(tmp)/'exam.pdf';fp.write_bytes(data)
                    proc=subprocess.run(['pdftotext','-layout',str(fp),'-'],text=True,capture_output=True,timeout=12)
                    if proc.returncode: raise ValueError('pdftotext_failed')
                    body=proc.stdout
                if len(body.strip())<70: raise ValueError('extraction_too_short')
                match=re.search(r'Category\s+(II|I)\b',body,re.I)
                result={'year':year,'edition':n,'source_url':url,'category_observed':match.group(1).upper() if match else None,
                        'file_name':prefix+suffix,'original_pdf_text':body,
                        'statement_verified':False,'publication_eligible':False,
                        'https_certificate_verified':transport_verified,
                        'pdf_sha256':hashlib.sha256(data).hexdigest(),
                        'review_flags':['pdf_text_extraction_only_visual_source_check_pending']}
                found.append({'url':url,'category_observed':result['category_observed'],'text_chars':len(body),'https_certificate_verified':transport_verified})
                extracted.append(result)
                break
            except Exception as e:
                attempts.append({'url':url,'error':str(e)[:150]})
    results.append({'year':year,'edition':n,'found':found,'attempts':attempts,
                    'source_status':'source_pdf_extracted_for_review' if found else 'source_pdf_unavailable'})
Path('out').mkdir(exist_ok=True)
Path('out/vjimc-source-discovery.json').write_text(json.dumps({'competition':'VJIMC','edition_count':len(results),'results':results},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
Path('out/vjimc-original-pdf-text-review.json').write_text(json.dumps({'competition':'VJIMC','research_only':True,'documents':extracted},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('VJIMC source PDFs obtained:',len(extracted),'from',sum(bool(x['found']) for x in results),'editions')
for x in results: print(x['year'],x['edition'],x['source_status'],[(k['file_name'] if 'file_name' in k else k['category_observed']) for k in x['found']])
if not extracted: raise SystemExit('SOURCE_DISCOVERY_INCOMPLETE: no organizer PDFs downloadable; manual alternative required')
