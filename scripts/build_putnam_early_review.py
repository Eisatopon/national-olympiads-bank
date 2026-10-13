"""Build native edited statements with transparent secondary-source comparison records."""
import json,hashlib,re
from pathlib import Path
from putnam_early_corrections import prepare,REVIEWED,CATEGORIES,NOTES,VARIANTS
ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads((ROOT/p).read_text())
def write(p,d):(ROOT/p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
INPUT_SHA256={'Putnam-1938-1949-raw-review.json': '9f3e31abfe69fcf52f07987cfa0a5fd27d5dc88bea8f33470cc25432a02d350b', 'Putnam-1950-1974-raw-review.json': '4077713018839eb4cf1bb489ff8abac08ff684239246a36fa646e83d9bf198e7', 'Putnam-1958-spring-fall-raw-review.json': 'bd9f30fced6d3774530943bee6d33b25e16b03bfc2be335ae59a7cde41eb2a25', 'Putnam-1938-1964-Scholes-source-review.json': '542c8598d50d029162e0cc39c64be004b088881769db8be101272cb68ca26557'}
for name,digest in INPUT_SHA256.items():
 assert hashlib.sha256((ROOT/'research/putnam'/name).read_bytes()).hexdigest()==digest, f'Input changed: {name}; re-review is required'
raw={}
inputs=['Putnam-1938-1949-raw-review.json','Putnam-1950-1974-raw-review.json','Putnam-1958-spring-fall-raw-review.json']
for name in inputs:
 d=read('research/putnam/'+name)
 for y in d.get('years',d.get('editions',[])):
  if y['year']>1964:continue
  for p in y['problems']:raw[(y['year'],y.get('edition','regular'),p['number'])]=p
source=read('research/putnam/Putnam-1938-1964-Scholes-source-review.json')
assert set(raw)==REVIEWED and len(raw)==331
names=dict(A='Algebra',G='Geometry',N='Number Theory',C='Combinatorics',X='Analysis')
years={};records=[]
for e in source['editions']:
 y=e['year'];edition=e['edition'];code=CATEGORIES.get((y,edition),CATEGORIES.get(y)).replace(' ','')
 assert len(code)==len(e['problems']),(y,edition)
 years.setdefault(y,{'year':y,'problems':[]})
 for sp,c in zip(e['problems'],code):
  n=sp['number'];key=(y,edition,n);r=raw[key];text=prepare(y,n,r['problem'],edition)
  text=re.sub(r'\s*\\quad\s*\\quad\s*',' ',text)
  p={'number':n,'problem':text,'category':names[c],'topics':[names[c]],'problem_dna':[],
   'source_url':r['source_url'],'statement_verified':False,'original_wording_verified':False,
   'secondary_comparison_completed':True,'comparison_source':e['source_url'],
   'comparison_source_document_sha256':e['source_document_sha256'],
   'comparison_source_statement_sha256':sp['source_statement_sha256'],
   'review_method':'AI-assisted record-by-record textual and mathematical comparison of a longer dataset transcription with John Scholes\u2019 explicitly reworded secondary archive. Original examination wording has not been verified.',
   'reviewed_on':'2026-10-13','statement_format':'english_text_latex',
   'review_flags':['original_examination_wording_not_verified'],
   'topic_review_method':'AI-assisted thematic review; primary topic assigned from the statement'}
  if y==1958:p.update(paper_id=1 if edition=='Spring' else 2,paper_label=f'{edition} examination',edition=edition)
  for field,m in [('source_issue_note',NOTES),('source_variant_note',VARIANTS)]:
   val=m.get(key,m.get((y,n)))
   if val:p[field]=val
  if p.get('source_issue_note','').startswith(('Unresolved','Incomplete')):p['review_flags'].append('source_issue_awaiting_original_verification')
  if y==1947 and n=='A3':
   f={'src':'research/putnam/figures/1947-A3.svg','alt':'Reconstructed configuration: three triangle vertices, an interior fourth vertex, and all six joining segments.','content':'diagram_only','provenance':'Editorial reconstruction from the explicit Scholes configuration; not a crop of an original examination.'}
   f['sha256']=hashlib.sha256((ROOT/f['src']).read_bytes()).hexdigest()
   p['figures']=[f];p['figure_alt']=f['alt']
   p['problem']+='\n\nhttps://eisatopon.github.io/national-olympiads-bank/'+f['src']
  p['statement_sha256']=hashlib.sha256(p['problem'].encode()).hexdigest()
  p['pre_review_statement_sha256']=hashlib.sha256(r['problem'].encode()).hexdigest()
  years[y]['problems'].append(p);records.append(key)
assert set(records)==REVIEWED
out={'competition':source['competition'],'first_year':1938,'last_year':1964,'problem_count':331,'edition_count':25,'years_without_competition':[1943,1944,1945],
 'status':'SECONDARY_COMPARISON_COMPLETE_ORIGINAL_WORDING_UNVERIFIED','publication_eligible':True,'solutions_imported':False,
 'statement_format':'english_text_latex','source_basis':'Edited longer dataset transcriptions compared individually with John Scholes\u2019 reworded secondary archive; source variants and editorial changes are recorded, without claiming original-examination fidelity.',
 'source_inputs_sha256':{n:hashlib.sha256((ROOT/'research/putnam'/n).read_bytes()).hexdigest() for n in inputs},
 'years':list(years.values())}
write('research/putnam/Putnam-1938-1964-native-secondary-review.json',out)
print('Prepared 331 native statements, 25 editions, 24 held calendar years; original-wording verification remains false.')
