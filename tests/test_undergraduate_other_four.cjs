const assert=require('node:assert/strict');
const fs=require('node:fs');
const registry=JSON.parse(fs.readFileSync('metadata/undergraduate-other-four-sources.json','utf8'));
assert.equal(registry.schema_version,1);
assert.equal(registry.records.length,16);
assert.deepEqual(new Set(registry.records.map(r=>r.competition_id)),new Set(['smmc','vjimc','seemous','imc']));
const smmc=registry.records.filter(r=>r.competition_id==='smmc');
assert.equal(smmc.length,9);
assert.deepEqual(smmc.map(r=>r.year),[2017,2018,2019,2020,2021,2022,2023,2024,2025]);
for(const entry of smmc){
 assert.match(entry.source_page,/^https:\/\/www\.simonmarais\.org\/\d{4}1?\.html$/);
 assert.equal(entry.statement_imported,false);
}
const pdfs=smmc.find(r=>r.year===2025).question_pdfs;
assert.deepEqual(Object.keys(pdfs),['A','B','C']);
for(const url of Object.values(pdfs))assert.match(url,/^https:\/\/www\.simonmarais\.org\/uploads\/.*\.pdf$/);
const jarnik=registry.records.filter(r=>r.competition_id==='vjimc');
assert.deepEqual(jarnik.map(r=>r.year),[2024,2025,2026]);
for(const entry of jarnik)assert.deepEqual(entry.category_ids,['I','II']);
const seemous=registry.records.filter(r=>r.competition_id==='seemous');
assert.ok(seemous.find(x=>x.year===2024).question_pdf.includes('SEEMOUS_2024_Contest_Problems.pdf'));
assert.ok(seemous.find(x=>x.year===2026).source_page.includes('cms.org.cy'));
assert.ok(seemous.find(x=>x.year_range==='2007–2025').source_kind.includes('collection'));
assert.equal(registry.records.filter(x=>x.competition_id==='imc').length,1);
assert.ok(registry.records.every(x=>x.statement_imported===(x.competition_id==='vjimc')));
console.log('All four university competition source registries verified for structure and paper identity.');
