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
early=read('research/putnam/Putnam-1938-1964-native-secondary-review.json')
for y in early['years']:
 for p in y['problems']:
  uid=f"put.{y['year']}.{p.get('paper_id',0)}.{p['number']}"
  checks[uid]={'status':'statement_compared_against_secondary_source','checked_at':p['reviewed_on'],'source_url':p['comparison_source'],'source_problem_number':p['number'],'source_format':'Reworded secondary HTML archive by John Scholes','source_contains_solutions':False,'reviewed_statement':p['problem'],'statement_sha256':p['statement_sha256'],'review_method':p['review_method'],'transcription_source_url':p['source_url'],'source_variant_note':p.get('source_variant_note',''),'original_wording_verified':False}
  if p.get('source_issue_note'):notes[uid]={'text':p['source_issue_note'],'reviewed_statement':p['problem'],'statement_sha256':p['statement_sha256']}
output={'competition':old['competition'],'short_name':'Putnam','first_year':1938,'last_year':2025,'problem_count':1063,'statement_format':'english_text_latex','status':'PARTIALLY_SOURCE_VERIFIED_PUBLISHED_SERIES','publication_eligible':True,'publication_basis':'Oral permission reported by the project owner on 2026-10-12; publication of reviewed historical batches authorized.','source_verified_problem_count':240,'preexisting_source_review_pending_count':492,'historical_1938_1964_status':'331 edited native statements compared with a reworded secondary source; original examination wording remains unverified.', 'secondary_compared_problem_count':331,'years':early['years']+old['years']+recent['years']}
write('undergraduate/Putnam-problems.json',output)
write('metadata/putnam-statement-checks.json',{'schema_version':1,'collections':{'undergraduate/Putnam-problems.json':{'source_links':[{'url':'https://kskedlaya.org/putnam-archive/'},{'url':'https://www.scribd.com/document/629286756/Putnam-1965-1984'}],'verification_notes':'1965–1984: 240 source-reviewed native statements. Existing 1985–2025 statements retain their previous per-record source-review status. 1938–1964: 331 edited statements compared textually with the Scholes secondary archive, with unresolved variants labelled; original examination wording is unverified.','statement_checks':checks,'statement_notes':notes}}})
print('Prepared Putnam collection: 1063 records; 240 primary-source checks; 331 secondary comparisons.')
