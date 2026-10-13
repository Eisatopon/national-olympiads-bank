"""Build the reviewed historical extension; retain recent records and their source status."""
import hashlib,json,re
from pathlib import Path
from putnam_tex_native import normalize_nested_text_math

ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads((ROOT/p).read_text())
def write(p,d):(ROOT/p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
codes={1965:'GCXCCGXC NXCG',1966:'AGXNXXGNXCGX',1967:'XCNXGAGAXNCX',1968:'XNCGAACAGXCX',1969:'AAGXXXNAXGXA',1970:'XGNXGXXXXXXG',1971:'NAGA NNAA XGXN',1972:'CAXGNXXXAAGA',1973:'GXNXXCAN NXAX',1974:'NGNCGNGXNXXC',1975:'NAXNXGAGAXXX',1976:'GANN GXXACGCN',1977:'AAAXNXXGAGAA',1978:'NAXAXCGXANAA',1979:'NXXCNXXXAXGA',1980:'GNXNXXXGXCXA',1981:'NCXGANXANANG',1982:'GXXXNXGXCNXG',1983:'NXNCNXGCXNXA',1984:'GXAGXNAGAXNG'}
EDITORIAL={
 (1978,'A5'):(r'\frac{\sin x_{i}}{x_{i}}<',r'\frac{\sin x_{i}}{x_{i}}\leq ', 'Editorial correction: the inequality is non-strict. The printed strict sign excludes the valid equality case when all x_i are equal. The corrected sign is explicit; it is not asserted as the original printed wording.'),
 (1978,'B3'):('for $ m>1 $',r'for $ m\geq1 $', 'Editorial correction: the recurrence applies for m>=1, so Q_3 and Q_4 are determined from the stated Q_1 and Q_2. The printed m>1 omits that initial step.'),
 (1979,'B6'):(r'r<\left|x_{1}\right|',r'r\leq\left|x_{1}\right|', 'Editorial correction: the inequality is non-strict. The printed strict sign fails already for n=1 and z_1=1. The corrected statement retains the generality of the original hypotheses.'),
}
names=dict(A='Algebra',G='Geometry',N='Number Theory',C='Combinatorics',X='Analysis')
old=read('research/putnam/Putnam-1965-1984-verified-review.json')
checks={};notes={}
for y in old['years']:
 code=codes[y['year']].replace(' ','');assert len(code)==12,(y['year'],code)
 for p,c in zip(y['problems'],code):
  p['category']=names[c];p['topics']=[names[c]];p['topic_review_method']='AI-assisted thematic review; primary topic assigned from the statement'
  key=(y['year'],p['number'])
  if key in EDITORIAL:
   before,after,note=EDITORIAL[key]
   assert before in p['problem'], f'Editorial source text changed: {key}'
   p['pre_editorial_statement_sha256']=hashlib.sha256(p['problem'].encode()).hexdigest()
   p['problem']=p['problem'].replace(before,after)
   p['source_issue_note']=note;p['original_wording_verified']=False
   p['source_issue_resolution']='Explicit mathematical correction of the recorded printed-source issue.'
  for f in p.get('figures',[]):p['problem']+='\n\nhttps://eisatopon.github.io/national-olympiads-bank/'+f['src']
  if p.get('figures'):p['figure_alt']=' '.join(f['alt'] for f in p['figures'])
  p['statement_sha256']=hashlib.sha256(p['problem'].encode()).hexdigest()
  uid=f"put.{y['year']}.0.{p['number']}"
  checks[uid]={'status':'statement_checked_against_source','checked_at':p['verified_on'],'source_url':p['verification_source'],'source_problem_number':p['number'],'source_format':'Printed MAA compilation, public scan' if p['source_contains_solutions'] else 'Examination PDF hosted by UCSD','source_contains_solutions':p['source_contains_solutions'],'reviewed_statement':p['problem'],'statement_sha256':p['statement_sha256'],'review_method':p['verification_method']}
  if 'original_wording_verified' in p:checks[uid]['original_wording_verified']=p['original_wording_verified']
  if 'verification_page' in p:checks[uid]['source_page']=p['verification_page']
  else:checks[uid]['source_pages']=p['verification_source_viewer_pages'];checks[uid]['printed_source_pages']=p['verification_source_printed_pages']
  if p.get('source_issue_note'):notes[uid]={'text':p['source_issue_note'],'reviewed_statement':p['problem'],'statement_sha256':p['statement_sha256']}
recent=read('research/putnam/Putnam-1985-2025-source-checked-review.json')
for y in recent['years']:
 for p in y['problems']:
  uid=f"put.{y['year']}.0.{p['number']}"
  checks[uid]={'status':'statement_checked_against_archive_tex','checked_at':p['verified_on'],'source_url':p['verification_source'],'source_problem_number':p['number'],'source_format':'Archive examination TeX transcription','source_contains_solutions':False,'reviewed_statement':p['problem'],'statement_sha256':p['statement_sha256'],'verification_basis':p['verification_basis'],'verification_tex_mirror':p['verification_tex_mirror'],'verification_pdf_source':p['verification_pdf_source'],'review_method':p['verification_method'],'original_wording_verified':False}
  if p.get('source_issue_note'):notes[uid]={'text':p['source_issue_note'],'reviewed_statement':p['problem'],'statement_sha256':p['statement_sha256']}
early=read('research/putnam/Putnam-1938-1964-native-secondary-review.json')
for y in early['years']:
 for p in y['problems']:
  uid=f"put.{y['year']}.{p.get('paper_id',0)}.{p['number']}"
  checks[uid]={'status':'statement_compared_against_secondary_source','checked_at':p['reviewed_on'],'source_url':p['comparison_source'],'source_problem_number':p['number'],'source_format':'Reworded secondary HTML archive by John Scholes','source_contains_solutions':False,'reviewed_statement':p['problem'],'statement_sha256':p['statement_sha256'],'review_method':p['review_method'],'transcription_source_url':p['source_url'],'source_variant_note':p.get('source_variant_note',''),'original_wording_verified':False}
  if p.get('source_issue_note'):notes[uid]={'text':p['source_issue_note'],'reviewed_statement':p['problem'],'statement_sha256':p['statement_sha256']}
output={'competition':old['competition'],'short_name':'Putnam','first_year':1938,'last_year':2025,'problem_count':1063,'statement_format':'english_text_latex','status':'PARTIALLY_SOURCE_VERIFIED_PUBLISHED_SERIES','publication_eligible':True,'publication_basis':'Oral permission reported by the project owner on 2026-10-12; publication of reviewed historical batches authorized.','source_verified_problem_count':732,'preexisting_source_review_pending_count':0,'archive_tex_checked_problem_count':492,'historical_1938_1964_status':'331 edited native statements compared with a reworded secondary source; original examination wording remains unverified.', 'secondary_compared_problem_count':331,'years':early['years']+old['years']+recent['years']}
write('undergraduate/Putnam-problems.json',output)
write('metadata/putnam-statement-checks.json',{'schema_version':1,'collections':{'undergraduate/Putnam-problems.json':{'source_links':[{'url':'https://kskedlaya.org/putnam-archive/'},{'url':'https://www.scribd.com/document/629286756/Putnam-1965-1984'}],'verification_notes':'1965–1984: 240 source-reviewed native statements. 1985–2025: all 492 cards checked against complete archive TeX transcriptions, with targeted PDF inspection; comparison with every original MAA scan is not asserted. 1938–1964: 331 edited statements compared textually with the Scholes secondary archive; the five recorded issues have explicit editorial resolutions or documented variants; original examination wording is unverified.','statement_checks':checks,'statement_notes':notes}}})
print('Prepared Putnam collection: 1063 records; 240 historical source checks; 492 archive TeX checks; 331 secondary comparisons.')
