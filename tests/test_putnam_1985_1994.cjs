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
const html = fs.readFileSync('index.html','utf8');
assert.ok(html.includes("key: 'put', name: 'Putnam'"));
assert.ok(html.includes("file: 'undergraduate/Putnam-1985-1994-review.json'"));
assert.ok(html.includes("if (key === 'put') return {"));
assert.ok(html.includes("c.key === 'put' ? 120"));
assert.ok(html.includes("loadCountry('put')"));
console.log('Putnam 1985-1994: complete 120 statements and Undergraduate grid registration validated.');
