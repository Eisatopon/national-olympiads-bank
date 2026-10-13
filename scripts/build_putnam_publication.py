"""Build the reviewed historical extension; retain recent records and their source status."""
import hashlib,json,re
from pathlib import Path
def normalize_nested_text_math(text):
    import re
    offset=0
    while True:
        match=re.search(r'\\(?:mbox|text)\s*\{',text[offset:])
        if not match:break
        start=offset+match.start();begin=offset+match.end();end=begin;depth=1
        while end<len(text) and depth:
            if text[end]=='{' and (end==0 or text[end-1]!='\\'):depth+=1
            if text[end]=='}' and (end==0 or text[end-1]!='\\'):depth-=1
            end+=1
        if depth:raise ValueError('Unbalanced text macro')
        body=text[begin:end-1]
        chunks=re.split(r'(?<!\\)\$',body)
        if len(chunks)>1:
            if len(chunks)%2==0:raise ValueError('Unbalanced nested text math')
            replacement=''.join((r'\text{'+c+'}' if i%2==0 else c) for i,c in enumerate(chunks) if c)
            text=text[:start]+replacement+text[end:];offset=start+len(replacement)
        else:offset=end
    return text

ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads((ROOT/p).read_text())
def write(p,d):(ROOT/p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
codes={1965:'GCXCCGXC NXCG',1966:'AGXNXXGNXCGX',1967:'XCNXGAGAXNCX',1968:'XNCGAACAGXCX',1969:'AAGXXXNAXGXA',1970:'XGNXGXXXXXXG',1971:'NAGA NNAA XGXN',1972:'CAXGNXXXAAGA',1973:'GXNXXCAN NXAX',1974:'NGNCGNGXNXXC',1975:'NAXNXGAGAXXX',1976:'GANN GXXACGCN',1977:'AAAXNXXGAGAA',1978:'NAXAXCGXANAA',1979:'NXXCNXXXAXGA',1980:'GNXNXXXGXCXA',1981:'NCXGANXANANG',1982:'GXXXNXGXCNXG',1983:'NXNCNXGCXNXA',1984:'GXAGXNAGAXNG'}
names=dict(A='Algebra',G='Geometry',N='Number Theory',C='Combinatorics',X='Analysis')
old=read('research/putnam/Putnam-1965-1984-verified-review.json')
checks={};notes={}
for y in old['years']:
 code=codes[y['year']].replace(' ','');assert len(code)==12,(y['year'],code)
 for p,c in zip(y['problems'],code):
  p['category']=names[c];p['topics']=[names[c]];p['topic_review_method']='AI-assisted thematic review; primary topic assigned from the statement'
  for f in p.get('figures',[]):p['problem']+='\n\nhttps://eisatopon.github.io/national-olympiads-bank/'+f['src']
  if p.get('figures'):p['figure_alt']=' '.join(f['alt'] for f in p['figures'])
  p['statement_sha256']=hashlib.sha256(p['problem'].encode()).hexdigest()
  uid=f"put.{y['year']}.0.{p['number']}"
  checks[uid]={'status':'statement_checked_against_source','checked_at':p['verified_on'],'source_url':p['verification_source'],'source_problem_number':p['number'],'source_format':'Printed MAA compilation, public scan' if p['source_contains_solutions'] else 'Examination PDF hosted by UCSD','source_contains_solutions':p['source_contains_solutions'],'reviewed_statement':p['problem'],'statement_sha256':p['statement_sha256'],'review_method':p['verification_method']}
  if 'verification_page' in p:checks[uid]['source_page']=p['verification_page']
  else:checks[uid]['source_pages']=p['verification_source_viewer_pages'];checks[uid]['printed_source_pages']=p['verification_source_printed_pages']
  if p.get('source_issue_note'):notes[uid]={'text':p['source_issue_note'],'reviewed_statement':p['problem'],'statement_sha256':p['statement_sha256']}
recent=read('undergraduate/Putnam-1985-2025-review.json')
for y in recent['years']:
 for p in y['problems']:
  repaired=normalize_nested_text_math(p['problem'])
  if repaired!=p['problem']:
   p['pre_render_repair_statement_sha256']=hashlib.sha256(p['problem'].encode()).hexdigest()
   p['native_rendering_repair']='Nested dollar math in text macros lifted into the surrounding math expression; hypotheses and formulas retained.'
   p['problem']=repaired
output={'competition':old['competition'],'short_name':'Putnam','first_year':1965,'last_year':2025,'problem_count':732,'statement_format':'english_text_latex','status':'PARTIALLY_SOURCE_VERIFIED_PUBLISHED_SERIES','publication_eligible':True,'publication_basis':'Oral permission reported by the project owner on 2026-10-12; publication of reviewed historical batches authorized.','source_verified_problem_count':240,'preexisting_source_review_pending_count':492,'historical_1938_1964_status':'Secondary-source statements recovered; mathematical comparison pending.','years':old['years']+recent['years']}
write('undergraduate/Putnam-problems.json',output)
write('metadata/putnam-statement-checks.json',{'schema_version':1,'collections':{'undergraduate/Putnam-problems.json':{'source_links':[{'url':'https://kskedlaya.org/putnam-archive/'},{'url':'https://www.scribd.com/document/629286756/Putnam-1965-1984'}],'verification_notes':'1965–1984: 240 source-reviewed native statements. Existing 1985–2025 statements retain their previous per-record source-review status. Historical 1938–1964 is not included yet.','statement_checks':checks,'statement_notes':notes}}})
p=ROOT/'index.html';s=p.read_text().replace("file: 'undergraduate/Putnam-1985-2025-review.json'","file: 'undergraduate/Putnam-problems.json'").replace("c.key === 'put' ? 492","c.key === 'put' ? 732");s=re.sub(r"if \(key === 'put'\) return \{[^\n]+", "if (key === 'put') return {"+','.join(f"'{y}':12" for y in range(1965,2026))+"};",s);p.write_text(s)
p=ROOT/'scripts/build_runtime_metadata.py';s=p.read_text().replace("src.update((load('vjimc-statement-checks.json') or {}).get('collections', {}))","src.update((load('vjimc-statement-checks.json') or {}).get('collections', {}))\n    src.update((load('putnam-statement-checks.json') or {}).get('collections', {}))").replace("ROOT / 'undergraduate/Simon-Marais-problems.json']","ROOT / 'undergraduate/Simon-Marais-problems.json', ROOT / 'undergraduate/Putnam-problems.json']");p.write_text(s)
p=ROOT/'tests/test_runtime_metadata.cjs';s=p.read_text().replace("...read('metadata/vjimc-statement-checks.json').collections}","...read('metadata/vjimc-statement-checks.json').collections, ...read('metadata/putnam-statement-checks.json').collections}");p.write_text(s)
p=ROOT/'tests/test_putnam_1985_1994.cjs';s=p.read_text().replace("file: 'undergraduate/Putnam-1985-2025-review.json'","file: 'undergraduate/Putnam-problems.json'").replace("c.key === 'put' ? 492","c.key === 'put' ? 732").replace('492 statements and Undergraduate grid registration','492 preserved recent statements and expanded Undergraduate grid registration');p.write_text(s)
contract=read('metadata/undergraduate-import-contract.json');c=next(c for c in contract['collections'] if c['id']=='put');c.update(file='undergraduate/Putnam-problems.json',publication_status='published_1965_2025_with_per_record_source_status',published_first_year=1965);contract['state']='partial_import_vjimc_smmc_and_putnam_published';contract['updated']='2026-10-13';write('metadata/undergraduate-import-contract.json',contract)
p=ROOT/'tests/test_undergraduate_import_contract.cjs';s=p.read_text().replace(" }else if(c.id==='vjimc'){"," }else if(c.id==='put'){\n   const imported=JSON.parse(fs.readFileSync(c.file,'utf8'));\n   assert.equal(imported.problem_count,732);\n   assert.equal(imported.years.length,61);\n   assert.equal(imported.years.flatMap(y=>y.problems).filter(p=>p.statement_verified).length,240);\n   assert.ok(imported.years.filter(y=>y.year<1985).every(y=>y.problems.every(p=>p.statement_verified&&p.category)));\n }else if(c.id==='vjimc'){").replace("v.state,'partial_import_vjimc_and_smmc_published'","v.state,'partial_import_vjimc_smmc_and_putnam_published'");p.write_text(s)
catalog=read('metadata/undergraduate-competitions.json');c=next(c for c in catalog['records'] if c['id']=='put');c.update(source_status='native_1965_2025_published_with_per_record_source_status',statements_imported=732,source_verified_statements=240,republication_permission='oral_permission_reported_by_project_owner_2026-10-12');catalog['updated']='2026-10-13';write('metadata/undergraduate-competitions.json',catalog)
history=read('metadata/putnam-historical-1938-2025.json')
for r in history['records']:
 r['publication_permission']='oral_permission_reported_by_project_owner_2026-10-12'
 if r['year']>=1965:r['statement_text_imported']=True;r['statement_by_statement_verified']=r['year']<1985;r['imported_file']='undergraduate/Putnam-problems.json'
write('metadata/putnam-historical-1938-2025.json',history)
p=ROOT/'tests/test_putnam_import.cjs';s=p.read_text().replace("assert.equal(r.statement_text_imported,false)","assert.equal(r.statement_text_imported,r.year>=1965)").replace("assert.equal(r.statement_by_statement_verified,false)","assert.equal(r.statement_by_statement_verified,r.year>=1965&&r.year<=1984)").replace("assert.equal(r.publication_permission,'not_established')","assert.equal(r.publication_permission,'oral_permission_reported_by_project_owner_2026-10-12')");p.write_text(s)
print('Prepared published Putnam collection: 732 records; 240 historical source checks.')
