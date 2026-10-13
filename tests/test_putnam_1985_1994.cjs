const assert = require('node:assert/strict');
const fs = require('node:fs');
const data = JSON.parse(fs.readFileSync('undergraduate/Putnam-1985-1994-review.json','utf8'));
assert.equal(data.short_name,'Putnam');
assert.equal(data.status,'DRAFT_REQUIRES_OFFICIAL_PDF_VERIFICATION');
assert.equal(data.publication_eligible,false);
assert.equal(data.problem_count,120);
assert.deepEqual(data.years.map(y=>y.year),Array.from({length:10},(_,i)=>1985+i));
let total=0;
for (const year of data.years) {
  assert.equal(year.problems.length,12,'Wrong problem count '+year.year);
  assert.deepEqual(year.problems.map(p=>p.number), ['A1','A2','A3','A4','A5','A6','B1','B2','B3','B4','B5','B6']);
  assert.ok(year.source_url.endsWith('/'+year.year+'.tex'));
  for (const p of year.problems) {
    assert.ok(p.problem.length>=30,'Missing text '+year.year+' '+p.number);
    assert.ok(!Object.hasOwn(p,'solution'),'Solutions not permitted');
    assert.equal(p.statement_verified,false);
    assert.ok(Array.isArray(p.topics)&&Array.isArray(p.problem_dna));
    assert.equal((p.problem.match(/\$/g)||[]).length%2,0,'Unpaired math delimiter: '+year.year+' '+p.number);
    total++;
  }
}
assert.equal(total,120);
const merged=JSON.parse(fs.readFileSync('undergraduate/Putnam-1985-2004-review.json','utf8'));
assert.deepEqual(merged.years.map(y=>y.year),Array.from({length:20},(_,i)=>1985+i));
assert.equal(merged.problem_count,240);
for(let i=0;i<10;i++) assert.deepEqual(merged.years[i],data.years[i]);
for(let i=10;i<20;i++) {
  const y=merged.years[i];
  assert.equal(y.problems.length,12);
  assert.deepEqual(y.problems.map(p=>p.number),['A1','A2','A3','A4','A5','A6','B1','B2','B3','B4','B5','B6']);
  for(const p of y.problems) {
    assert.ok(p.problem.length>=30);
    assert.ok(!Object.hasOwn(p,'solution'));
    assert.equal(p.statement_verified,false);
    assert.equal((p.problem.match(/\$/g)||[]).length%2,0);
  }
}
assert.ok(merged.years.find(y=>y.year===2003).problems.find(p=>p.number==='A5').review_flags.includes('source_diagram_requires_reproduction'));
const three=JSON.parse(fs.readFileSync('undergraduate/Putnam-1985-2014-review.json','utf8'));
assert.equal(three.problem_count,360);
assert.deepEqual(three.years.map(y=>y.year),Array.from({length:30},(_,i)=>1985+i));
for(let i=0;i<20;i++) assert.deepEqual(three.years[i],merged.years[i]);
for(let i=20;i<30;i++){
 const y=three.years[i];
 assert.equal(y.problems.length,12);
 assert.deepEqual(y.problems.map(p=>p.number),['A1','A2','A3','A4','A5','A6','B1','B2','B3','B4','B5','B6']);
 for(const p of y.problems){
  assert.ok(p.problem.length>=30);
  assert.equal(p.statement_verified,false);
  assert.ok(!Object.hasOwn(p,'solution'));
  assert.equal((p.problem.match(/\$/g)||[]).length%2,0);
 }
}
assert.ok(three.years.find(y=>y.year===2013).problems.find(p=>p.number==='A6').review_flags.includes('latex_tabular_requires_browser_render_review'));
const four=JSON.parse(fs.readFileSync('undergraduate/Putnam-1985-2024-review.json','utf8'));
assert.equal(four.problem_count,480);
assert.deepEqual(four.years.map(y=>y.year),Array.from({length:40},(_,i)=>1985+i));
for(let i=0;i<30;i++) assert.deepEqual(four.years[i],three.years[i]);
for(let i=30;i<40;i++){
 const year=four.years[i];
 assert.equal(year.problems.length,12);
 assert.deepEqual(year.problems.map(p=>p.number),['A1','A2','A3','A4','A5','A6','B1','B2','B3','B4','B5','B6']);
 for(const p of year.problems){
  assert.ok(p.problem.length>=30);
  assert.equal(p.statement_verified,false);
  assert.ok(!Object.hasOwn(p,'solution'));
  assert.equal((p.problem.match(/\$/g)||[]).length%2,0);
 }
}
assert.ok(four.years.find(y=>y.year===2016).problems.find(p=>p.number==='A4').review_flags.includes('source_diagram_requires_reproduction'));
const through2025=JSON.parse(fs.readFileSync('undergraduate/Putnam-1985-2025-review.json','utf8'));
assert.equal(through2025.problem_count,492);
assert.deepEqual(through2025.years.map(y=>y.year),Array.from({length:41},(_,i)=>1985+i));
for(let i=0;i<40;i++) assert.deepEqual(through2025.years[i],four.years[i]);
const newest=through2025.years[40];
assert.deepEqual(newest.problems.map(p=>p.number),['A1','A2','A3','A4','A5','A6','B1','B2','B3','B4','B5','B6']);
assert.ok(newest.problems.every(p=>p.problem.trim().length>=30&&!Object.hasOwn(p,'solution')&&p.statement_verified===false&&(p.problem.match(/\$/g)||[]).length%2===0));
const html = fs.readFileSync('index.html','utf8');
assert.ok(html.includes("key: 'put', name: 'Putnam'"));
assert.ok(html.includes("file: 'undergraduate/Putnam-problems.json'"));
assert.ok(html.includes("if (key === 'put') return {"));
assert.ok(html.includes("c.key === 'put' ? 1063"));
assert.ok(html.includes("loadCountry('put')"));
console.log('Putnam 1985-2025: 492 preserved recent statements and expanded Undergraduate grid registration validated.');
