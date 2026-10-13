"""Recover statement-only secondary sources and build a comparison queue, without certification."""
import concurrent.futures, hashlib, json, re, urllib.request
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin
ROOT=Path(__file__).resolve().parents[1]
BASE='https://prase.cz/kalva/putnam.html'
class Links(HTMLParser):
 def __init__(self):super().__init__();self.links=[]
 def handle_starttag(self,t,a):
  if t=='a':
   u=dict(a).get('href','')
   if re.fullmatch(r'putnam/putn\d\d[a]?\.html',u):self.links.append(urljoin(BASE,u))
class Cells(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=True);self.cells=[];self.current=None
 def handle_starttag(self,t,a):
  if t=='td':self.current=[]
  elif self.current is not None:
   if t=='sup':self.current.append('^{')
   elif t=='sub':self.current.append('_{')
   elif t in ('p','br'):self.current.append('\n')
 def handle_endtag(self,t):
  if t=='td' and self.current is not None:self.cells.append(''.join(self.current));self.current=None
  elif t in ('sup','sub') and self.current is not None:self.current.append('}')
 def handle_data(self,d):
  if self.current is not None:self.current.append(d)
def get(url):
 with urllib.request.urlopen(url,timeout=35) as response:return response.read()
index=get(BASE);links=Links();links.feed(index.decode('utf8','replace'))
urls=[]
for u in links.links:
 n=re.search(r'putn(\d\d)(a?)\.html',u);year=1900+int(n[1])
 if 1938<=year<=1964:urls.append((year,'Fall' if n[2] else 'Spring' if year==1958 else 'regular',u))
cache=ROOT/'.cache/putnam/scholes';cache.mkdir(parents=True,exist_ok=True)
def fetch(item):
 y,e,u=item;cached=cache/f'{y}-{e}.html';raw=cached.read_bytes() if cached.exists() else get(u);(cache/f'{y}-{e}.html').write_bytes(raw);parser=Cells();parser.feed(raw.decode('utf8','replace'))
 problems=[]
 for cell in parser.cells:
  cell=re.sub(r'[\t \r\f\v]+',' ',cell).strip();cell=re.sub(r'\n\s*\n+','\n',cell)
  m=re.match(r'^([AB]\d+)\.\s*(.+)',cell,re.S)
  if m:problems.append({'number':m[1],'source_statement_text':m[2].strip(),'source_url':u,'source_statement_sha256':hashlib.sha256(m[2].strip().encode()).hexdigest()})
 if not problems:raise ValueError(u)
 return {'year':y,'edition':e,'source_url':u,'source_document_sha256':hashlib.sha256(raw).hexdigest(),'problems':problems}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:editions=list(pool.map(fetch,urls))
original={}
for f in ['research/putnam/Putnam-1938-1949-raw-review.json','research/putnam/Putnam-1950-1974-raw-review.json','research/putnam/Putnam-1958-spring-fall-raw-review.json']:
 data=json.loads((ROOT/f).read_text())
 for y in data.get('editions',data.get('years',[])):
  if y['year']<=1964:
   for p in y['problems']:original[y['year'],y.get('edition','regular'),p['number']]=(f,p)
rows=[];source_keys=set()
for y in editions:
 for p in y['problems']:
  key=(y['year'],y['edition'],p['number']);source_keys.add(key)
  f,raw=original.get(key,('',{}));record={'year':key[0],'edition':key[1],'number':key[2],'source_url':y['source_url'],'existing_input':f,'existing_input_found':bool(raw),'statement_verified':False,'original_wording_verified':False,'status':'awaits_manual_mathematical_comparison'}
  if raw:
   nums=lambda s: sorted(re.findall(r'\d+',s))
   record['numeric_token_difference']=nums(re.sub(r'^\s*(?:[AB])?\d+[.]\s*','',raw['problem']))!=nums(p['source_statement_text'])
   record['raw_math_warning_patterns']=sorted(set(re.findall(r'\\(?:bullet|%)|\\(?:text|operatorname)\s*\{[^}]*\d[^}]*\}',raw['problem'])))
  rows.append(record)
output={'competition':'William Lowell Putnam Mathematical Competition','first_year':1938,'last_year':1964,'source_index':BASE,'source_version':'John Scholes reworded statements; original wording is not certified','source_author':'John Scholes','source_acquired_on':'2026-10-13','edition_count':len(editions),'numbered_statement_count':sum(len(y['problems']) for y in editions),'years_without_competition':[1943,1944,1945],'publication_eligible':False,'solutions_imported':False,'statement_format':'source_text_with_subscript_and_superscript_markers','editions':editions}
(ROOT/'research/putnam/Putnam-1938-1964-Scholes-source-review.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
audit={'schema_version':1,'scope':'Secondary-source coverage and comparison queue; not a fidelity certificate','records':rows,'existing_only_keys':[list(k) for k in sorted(set(original)-source_keys)],'secondary_only_keys':[list(k) for k in sorted(source_keys-set(original))],'numbered_statement_count':len(rows),'numeric_difference_count':sum(r.get('numeric_token_difference',False) for r in rows)}
(ROOT/'research/putnam/Putnam-1938-1964-secondary-comparison.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:output[k] for k in ['edition_count','numbered_statement_count']},indent=2));print('Existing only',audit['existing_only_keys']);print('Secondary only',audit['secondary_only_keys']);print('Numeric review queue',audit['numeric_difference_count'])
