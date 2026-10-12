import fitz,re,json,hashlib
from pathlib import Path
from PIL import Image,ImageChops,ImageOps,ImageDraw
ROOT=Path(__file__).resolve().parents[1]
import argparse
parser=argparse.ArgumentParser(description='Build exact original VJIMC statement images from source-discovery artifact.')
parser.add_argument('--sources',type=Path,required=True,help='Extracted artifact containing vjimc-pdfs and vjimc-original-pdf-text-review.json')
SRC=parser.parse_args().sources
docs=json.loads((SRC/'vjimc-original-pdf-text-review.json').read_text())['documents']
assets=ROOT/'assets/statements/vjimc';assets.mkdir(parents=True,exist_ok=True)
years={};audit=[];tiles=[]
for doc in docs:
 pdfpath=SRC/'vjimc-pdfs'/doc['file_name'];sha=hashlib.sha256(pdfpath.read_bytes()).hexdigest();assert sha==doc['pdf_sha256']
 pdf=fitz.open(pdfpath)
 for page_index,page in enumerate(pdf):
  text=page.get_text();catmatch=re.search(r'Category\s+(II|I)\b',text)
  if not catmatch:continue
  cat=catmatch.group(1);lines=[l for b in page.get_text('dict')['blocks'] for l in b.get('lines',[])]
  heads=[];footer=[]
  for line in lines:
   t=''.join(s['text'] for s in line['spans']);m=re.match(r'^Problem\s*(\d+)(?:-([MI]))?\b',t)
   if m:heads.append((int(m[1]),m[2],line['bbox'][1],t))
   if re.match(r'^\s*\d{1,2}-[A-Za-z]{3}-\d{4}',t):footer.append(line['bbox'][1])
  assert heads,(doc['year'],cat)
  for i,(number,variant,y0,heading) in enumerate(heads):
   end=heads[i+1][2]-2 if i+1<len(heads) else min([y for y in footer if y>y0] or [page.rect.height-20])-2
   rect=fitz.Rect(0,max(0,y0-3),page.rect.width,end)
   pix=page.get_pixmap(matrix=fitz.Matrix(3,3),clip=rect,alpha=False)
   image=Image.frombytes('RGB',[pix.width,pix.height],pix.samples)
   ink=ImageChops.difference(image,Image.new('RGB',image.size,'white')).getbbox();assert ink
   trimmed=image.crop(ink);out=ImageOps.expand(trimmed,border=18,fill='white')
   suffix=str(number)+(variant or '');filename=f"{doc['year']}-{cat}-p{suffix}.png";path=assets/filename;out.save(path,optimize=True)
   # Confirm exact source-render pixels: padding aside, the published body is unchanged.
   check=Image.open(path).convert('RGB').crop((18,18,18+trimmed.width,18+trimmed.height))
   assert ImageChops.difference(check,trimmed).getbbox() is None
   raw=page.get_text(clip=rect)
   raw=re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]','',raw)
   raw=' '.join(raw.split());assert 'Solution' not in raw
   record={'number':f'{number}-{variant}' if variant else number,'paper':cat,'paper_id':1 if cat=='I' else 2,'paper_label':'Category '+cat,'problem':raw,'statement_asset':{'src':str(path.relative_to(ROOT)),'alt':f"Αυθεντική εκφώνηση του προβλήματος {number}{'-'+variant if variant else ''}, Κατηγορία {cat}, του διαγωνισμού Vojtěch Jarník {doc['year']}, με τους μαθηματικούς τύπους του επίσημου φύλλου.",'width':out.width,'height':out.height,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()},'statement_format':'official_paper_facsimile','statement_verified':True,'verification_scope':'Exact original statement image; searchable PDF text is not a certified mathematical transcription','text_transcription_verified':False,'verification_method':'Lossless 3x rendering of official PDF statement region; saved pixels compared exactly to source render; source heading and paper identity retained','verification_source':doc['source_url'],'verification_page':page_index+1,'source_url':doc['source_url'],'source_document_sha256':sha,'source_crop_points':list(rect),'source_variant':variant,'https_certificate_verified':doc['https_certificate_verified'],'verified_on':'2026-10-12','review_flags':[]}
   if re.search(r'\b(?:matrix|matrices|determinants?|eigenvalues?|eigenvectors?)\b',raw,re.I) and not re.search(r'\b(?:primes?|divides?|divisib\w*|modulo)\b',raw,re.I):record['category']='Algebra'
   if doc['year']==2026 and cat=='I' and number==3:record['category']='Geometry'
   years.setdefault(doc['year'],[]).append(record);audit.append({'year':doc['year'],'paper':cat,'number':record['number'],'asset':str(path.relative_to(ROOT)),'bbox':list(rect)})
   # 4 statement crops per sheet, readable at full resolution.
   tile=Image.new('RGB',(1550,1100),'#f1f3f5');label=f"{doc['year']} Category {cat} — Problem {record['number']}";ImageDraw.Draw(tile).text((20,10),label,fill='black')
   thumb=out.copy();thumb.thumbnail((1510,1030));tile.paste(thumb,(20,45));tiles.append(tile)
for y,ps in years.items():
 ids=[(p['paper'],str(p['number'])) for p in ps];assert len(ids)==len(set(ids));ps.sort(key=lambda p:(p['paper_id'],int(str(p['number']).split('-')[0]),0 if str(p['number']).endswith('-M') else 1))
assert len(years)==33 and sum(map(len,years.values()))==261
assert not {2020,2021,2023}&years.keys()
collection={'competition':'Vojtěch Jarník International Mathematical Competition','statement_format':'official_paper_facsimile','publication_basis':'Project owner reports oral permission to publish; publication explicitly requested 2026-10-12','held_years':sorted(years),'years_without_competition':[2020,2021,2023],'paper_count':65,'problem_count':261,'count_note':'1997 and 1998 have separate Problem 4-M and 4-I alternatives in each category; all four additional variants are retained. 1991 has only the Category I paper in the official archive.','years':[{'year':y,'problems':years[y]} for y in sorted(years)]}
(ROOT/'undergraduate/Vojtech-Jarnik-problems.json').write_text(json.dumps(collection,ensure_ascii=False,indent=2)+'\n')
qa=ROOT/'.cache/vjimc-qa';qa.mkdir(parents=True,exist_ok=True)
for start in range(0,len(tiles),4):
 sheet=Image.new('RGB',(3100,2200),'white')
 for j,t in enumerate(tiles[start:start+4]):sheet.paste(t,((j%2)*1550,(j//2)*1100))
 sheet.save(qa/f'sheet-{start//4+1:02}.jpg',quality=90)
(qa/'crop-audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2))
print('Published assets prepared:',len(audit),'years:',len(years),'asset MB:',round(sum(p.stat().st_size for p in assets.glob('*.png'))/1e6,2),'QA sheets:',(len(tiles)+3)//4)
