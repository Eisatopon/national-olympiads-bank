"""Build the 492 source-checked cards from pinned full statement-only TeX snapshots."""
from pathlib import Path
import json,hashlib,re
from putnam_recent_corrections import prepare,NOTES
ROOT=Path(__file__).resolve().parents[1]
INPUT='research/putnam/Putnam-1985-2025-statement-sources.json'
SHA='31324b3b4ccf869f34e97da7da7caccc01ec3ce35d07991d178aafdcf642d829'
def digest(b):return hashlib.sha256(b).hexdigest()
def read(p):return json.loads((ROOT/p).read_text())
assert digest((ROOT/INPUT).read_bytes())==SHA,'Source snapshot changed; repeat source review.'
assert digest((ROOT/'undergraduate/Putnam-1985-2025-review.json').read_bytes())=='8c41689fc83d38083d133feb1abc71ba56dc5764c036fc3ebdcff4531ff78fd9', 'Prior input changed; repeat comparison'
source=read(INPUT);raw=read('undergraduate/Putnam-1985-2025-review.json')
byid={(p['year'],p['number']):p for p in source['statements']};assert len(byid)==492
files={(f['year'],f['file'].split('.')[-1]):f for f in source['source_files']}
figures={
 (1993,'A1'):('1993-A1.svg','The two regions between y=2x-3x cubed, y=c and the y-axis, reconstructed from the explicit description.','reconstructed'),
 (2003,'A5'):('2003-A5.png','A Dyck 5-path with returns of lengths three and one.','pdf_crop'),
 (2005,'A2'):('2005-A2.png','The illustrative rook tour through the fifteen points of a five-by-three grid.','pdf_crop'),
 (2011,'A1'):('2011-A1.svg','An illustrative growing spiral with directed steps east, north, west and south of increasing lengths.','reconstructed'),
 (2016,'A4'):('2016-A4.png','The two allowed tile shapes: an L-shaped tromino and a skew tetromino, with unit-square subdivisions.','pdf_crop'),
 (2024,'B2'):('2024-B2.png','Partner quadrilaterals ABCD and ABCE, with D and E reflected across the perpendicular bisector of AC.','pdf_crop'),
}
# These were independently inspected as complete source statements or source-critical diagrams/tables.
focused={(1985,'A6'),(1992,'B6'),(1993,'A1'),(2003,'A5'),(2005,'A2'),(2007,'A6'),(2013,'A6'),(2016,'A4'),(2024,'B2')}
years=[]
for y in raw['years']:
 yr=y['year'];out={'year':yr,'problems':[]}
 for original in y['problems']:
  n=original['number'];s=byid[(yr,n)];assert digest(s['source_statement_tex'].encode())==s['source_statement_sha256']
  text=prepare(yr,n,s['source_statement_tex']);tex=files[(yr,'tex')];pdf=files[(yr,'pdf')]
  p={'number':n,'problem':text,'statement_verified':True,'text_transcription_verified':True,'original_wording_verified':False,
   'verification_basis':'archive_tex_textual_comparison_with_focused_pdf_checks',
   'verification_source':tex['upstream_url'],'source_url':tex['upstream_url'],'verification_tex_mirror':tex['url'],
   'verification_tex_sha256':tex['sha256'],'verification_pdf_source':pdf['upstream_url'],'verification_pdf_mirror':pdf['url'],
   'verification_pdf_sha256':pdf['sha256'],'verification_method':'Fresh complete TeX statement extraction from the archive\u2019s declared verbatim examination transcriptions, compared against the prior cards; AI-assisted inspection of source differences, document-to-card conversion, formulas, diagrams and the numeric table. This is an archive-transcription check, not a claim of visual comparison with every original MAA examination scan.',
   'verified_on':'2026-10-13','source_contains_solutions':False,'review_flags':[],
   'source_input_statement_sha256':s['source_statement_sha256'],'pre_review_statement_sha256':digest(original['problem'].encode()),
   'topics':original.get('topics',[]),'problem_dna':original.get('problem_dna',[]),'statement_format':'english_text_latex',
   'focused_pdf_visual_review':(yr,n) in focused}
  if (yr,n) in NOTES:p['source_issue_note']=NOTES[(yr,n)]
  if yr<=2010:
   u=next(q for q in source['additional_university_pdfs'] if q['year']==yr)
   p['additional_university_source']=u['url'];p['additional_university_pdf_sha256']=u['sha256']
  if (yr,n) in figures:
   name,alt,kind=figures[(yr,n)];path='research/putnam/figures/'+name
   f={'src':path,'alt':alt,'content':'diagram_only','kind':kind,'sha256':digest((ROOT/path).read_bytes())}
   f['source_url']=p['additional_university_source'] if yr==2005 else pdf['url']
   f['source_page']=1
   if yr==2024:
    f['source_url']='https://raw.githubusercontent.com/raymonraymon/Putnam-Problems-and-solutions/main/2024-Putnam-Session-B-Solutions-1.pdf'
    f['source_page']=2;f['source_contains_solutions']=True
   f['provenance']='Reconstructed from the explicit statement definition' if kind=='reconstructed' else 'Diagram-only PDF crop inspected against the full question page; no solution content'
   p['figures']=[f];p['figure_alt']=alt;p['problem']+='\n\nhttps://eisatopon.github.io/national-olympiads-bank/'+path
  p['statement_sha256']=digest(p['problem'].encode());out['problems'].append(p)
 years.append(out)
output={'competition':raw['competition'],'first_year':1985,'last_year':2025,'problem_count':492,'solutions_imported':False,'publication_eligible':True,'status':'ARCHIVE_TEX_SOURCE_COMPARISON_COMPLETE','source_snapshot_sha256':SHA,'original_examination_scan_comparison_complete':False,'source_review_limit':'All 492 cards are checked against complete archive TeX transcriptions. PDF inspection focuses on source differences and visual dependencies. The 1938–1964 edited corpus remains explicitly secondary-source based.','years':years}
(ROOT/'research/putnam/Putnam-1985-2025-source-checked-review.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
print('Built 492 source-checked native cards from complete source snapshots; six diagram assets; original-scan review is not asserted.')
