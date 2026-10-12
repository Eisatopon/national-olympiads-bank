#!/usr/bin/env python3
"""Probe the organiser's numbered question PDFs for VJIMC; never mark unreviewed text verified."""
import json, subprocess, tempfile, urllib.request
from pathlib import Path
manifest=json.loads(Path('metadata/vojtech-jarnik-editions-source-manifest.json').read_text())
results=[]
extracted=[]
for edition in manifest['editions']:
    n=edition['edition']
    year=edition['year']
    url=f'https://vjimc.osu.cz/storage/uploads/j{n:02d}problems.pdf'
    record={'year':year,'edition':n,'url':url,'status':'unavailable_or_unreadable','categories_found':[],'visual_review_required':True}
    try:
        with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 (research source review)'}),timeout=15) as r:
            raw=r.read(10000000)
        if not raw.startswith(b'%PDF'): raise ValueError('not_pdf')
        with tempfile.TemporaryDirectory() as td:
            pdf=Path(td)/'source.pdf';pdf.write_bytes(raw)
            p=subprocess.run(['pdftotext','-layout',str(pdf),'-'],capture_output=True,text=True,timeout=15)
            if p.returncode: raise ValueError('pdftotext_error')
            t=p.stdout
        # Save unedited extracted paper text as a REVIEW CANDIDATE only.
        # Problem boundaries and mathematical formulae still require visual PDF inspection.
        extracted.append({'year':year,'edition':n,'source_url':url,
                          'original_pdf_text':t,'statement_verified':False,
                          'publication_eligible':False,
                          'review_flags':['pdf_text_extraction_only_visual_review_pending']})
        cats=[c for c in ['I','II'] if ('Category '+c+'\n') in t or ('Category '+c+' ') in t]
        record.update(status='pdf_text_extracted',categories_found=cats,raw_bytes=len(raw),text_chars=len(t),
          pdf_problem_word_occurrences=t.lower().count('problem'))
    except Exception as e:
        record['error']=str(e)[:160]
    results.append(record)
Path('out').mkdir(exist_ok=True)
Path('out/vjimc-source-discovery.json').write_text(json.dumps({'competition':'VJIMC','edition_count':len(results),'results':results},ensure_ascii=False,indent=2)+'\\n')
Path('out/vjimc-original-pdf-text-review.json').write_text(
    json.dumps({'competition':'VJIMC','research_only':True,'documents':extracted},
               ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('VJIMC papers obtained:',sum(x['status']=='pdf_text_extracted' for x in results),'/',len(results))
for x in results: print(x['year'],x['edition'],x['status'],x['categories_found'])
