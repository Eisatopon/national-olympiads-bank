const assert=require('node:assert/strict');
const {verify}=require('../scripts/verify_putnam_import.cjs');
const fs=require('node:fs');
const sources=JSON.parse(fs.readFileSync('metadata/undergraduate-official-papers.json','utf8')).competitions;
const source=sources.find(x=>x.competition_id==='put'&&x.year===2025);
const fulltext='Let a, b and c be positive integers with a+b+c=100 and determine all values satisfying the stated conditions.';
const base=()=>({competition:'William Lowell Putnam Mathematical Competition',years:[{year:2025,primary_source_url:source.questions_pdf,statement_reviewed_against_original:true,publication_authorized:true,authorization_reference:'Written approval on file',problems:['A','B'].flatMap(session=>Array.from({length:6},(_,i)=>({number:session+(i+1),problem:fulltext})))}]});
assert.deepEqual(verify(base(),sources),{years:1,problems:12});
const missing=base();missing.years[0].problems.pop();assert.throws(()=>verify(missing,sources),/12 problems/);
const duplicate=base();duplicate.years[0].problems[11].number='A1';assert.throws(()=>verify(duplicate,sources),/Repeated/);
const placeholder=base();placeholder.years[0].problems[0].problem='See the original PDF';assert.throws(()=>verify(placeholder,sources),/placeholder|incomplete/);
const unreviewed=base();unreviewed.years[0].statement_reviewed_against_original=false;assert.throws(()=>verify(unreviewed,sources),/review/);
const unauthorized=base();unauthorized.years[0].publication_authorized=false;assert.throws(()=>verify(unauthorized,sources),/clearance/);
const badlink=base();badlink.years[0].primary_source_url='https://example.com';assert.throws(()=>verify(badlink,sources),/official original/);
console.log('Putnam full-text import integrity tests passed.');

const history=JSON.parse(fs.readFileSync('metadata/putnam-historical-1938-2025.json','utf8'));
assert.equal(history.schema_version,1);
assert.equal(history.coverage.edition_records,86);
assert.equal(history.records.length,86);
assert.equal(history.coverage.last_past_exam_year,2025);
assert.ok(history.records.every(x=>x.year<=2025),'2026 exam has not occurred yet');
assert.equal(new Set(history.records.map(r=>r.year+':'+r.edition)).size,86);
const validYears=new Set(history.records.map(r=>r.year));
assert.equal(validYears.size,85);
for(const year of [1943,1944,1945])assert.ok(!validYears.has(year),'Putnam not held in '+year);
for(const year of [1938,1942,1946,1957,1959,1984,1985,2020,2025])assert.ok(validYears.has(year));
assert.deepEqual(history.records.filter(r=>r.year===1958).map(r=>r.edition),['spring','autumn']);
const recent=history.records.filter(r=>r.year>=1985);
assert.equal(recent.length,41);
for(const r of recent){
  assert.equal(r.exam_pdf,'https://kskedlaya.org/putnam-archive/'+r.year+'.pdf');
  assert.equal(r.exam_tex,'https://kskedlaya.org/putnam-archive/'+r.year+'.tex');
}
const early=history.records.filter(r=>r.year<1985);
assert.equal(early.length,45);
for(const r of early){
 assert.equal(r.exam_pdf,undefined,'Do not fabricate an early PDF source for '+r.year);
 assert.ok(['1938–1964','1965–1984'].includes(r.compilation_period));
}
for(const r of history.records){
 assert.equal(r.statement_text_imported,true);
 assert.equal(r.statement_by_statement_verified,r.year>=1965&&r.year<=1984);
 assert.equal(r.publication_permission,'oral_permission_reported_by_project_owner_2026-10-12');
}
assert.equal(history.records.find(r=>r.year===2020).event_status,'unofficial_rescheduled_2021-02-20');
const wronglyModern=base();wronglyModern.years[0].year=1938;
assert.throws(()=>verify(wronglyModern,sources),/Standard A1–B6 validation/);
console.log('Putnam historical coverage: 86 editions and zero invented historical originals.');
