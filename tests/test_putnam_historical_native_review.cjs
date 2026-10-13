const assert = require('node:assert/strict');
const fs = require('node:fs');
const crypto = require('node:crypto');
const file = 'research/putnam/Putnam-1965-1984-verified-review.json';
const data = JSON.parse(fs.readFileSync(file, 'utf8'));
const sha = text => crypto.createHash('sha256').update(text).digest('hex');
const records = data.years.flatMap(y => y.problems.map(p => ({year:y.year,...p})));
assert.equal(records.length, 240);
assert.equal(data.publication_eligible, false);
assert.equal(data.solutions_imported, false);
assert.deepEqual(data.years.map(y=>y.year), Array.from({length:20},(_,i)=>1965+i));
for (const y of data.years) assert.deepEqual(y.problems.map(p=>p.number), ['A','B'].flatMap(s=>Array.from({length:6},(_,i)=>s+(i+1))));
for (const p of records) {
  assert.equal(p.statement_verified, true);
  assert.equal(p.statement_sha256, sha(p.problem));
  assert.ok(p.verification_source.startsWith('https://'));
  assert.ok(!/[\u0370-\u03ff]/.test(p.problem));
  assert.ok(!p.solution);
  assert.ok(!/\\[()[\]]/.test(p.problem));
  const withoutMath=p.problem.replace(/\$\$[\s\S]*?\$\$|\$[^$]*?\$/g,'');
  assert.ok(!/\\(?:text|begin|frac|sum|sqrt)\b/.test(withoutMath), `${p.year}/${p.number}: math outside delimiters`);
  for (const f of p.figures??[]) {
    assert.equal(f.content, 'diagram_only');
    assert.equal(f.sha256,sha(fs.readFileSync(f.src)));
  }
}
const get=(y,n)=>records.find(p=>p.year===y&&p.number===n).problem;
assert.ok(get(1965,'A3').includes('a_{n^{2}}'));
assert.ok(get(1971,'B6').includes('\\left|\\sum'));
assert.ok(get(1972,'A1').includes('\\binom n{r+3}'));
assert.ok(get(1975,'A3').includes('x^{c}+y^{c}+z^{c}=1'));
assert.ok(get(1975,'B1').includes('(5,4)'));
assert.ok(get(1982,'B5').includes('$u_{n+1}$'));
assert.equal(records.filter(p=>p.source_issue_note).length,3);
assert.equal(records.flatMap(p=>p.figures??[]).length,3);
assert.equal(records.flatMap(p=>p.figures??[]).reduce((n,f)=>n+f.diagram_count,0),4);
console.log('Putnam historical checkpoint: 240 statements, source hashes, corrected formulas and four diagram crops verified.');
const published=JSON.parse(fs.readFileSync('undergraduate/Putnam-problems.json','utf8'));
const recent=JSON.parse(fs.readFileSync('undergraduate/Putnam-1985-2025-review.json','utf8'));
assert.equal(published.problem_count,732);
const recentPublished=published.years.filter(y=>y.year>=1985);
assert.deepEqual(recentPublished.map(y=>y.year),recent.years.map(y=>y.year));
let renderingRepairs=0;
for(let i=0;i<recent.years.length;i++)for(let j=0;j<12;j++){
 const original=recent.years[i].problems[j], current=recentPublished[i].problems[j];
 const {problem,pre_render_repair_statement_sha256,native_rendering_repair,...rest}=current;
 const {problem:oldProblem,...oldRest}=original;
 assert.deepEqual(rest,oldRest);
 if(native_rendering_repair){
  assert.equal(pre_render_repair_statement_sha256,sha(oldProblem));
  assert.notEqual(problem,oldProblem);
  assert.ok(!/\\(?:mbox|text)\s*\{[^}]*\$/.test(problem));
  renderingRepairs++;
 }else assert.equal(problem,oldProblem);
}
assert.equal(renderingRepairs,12);
const historical=published.years.filter(y=>y.year<1985).flatMap(y=>y.problems);
assert.equal(historical.length,240);
const categories=new Set(['Algebra','Geometry','Number Theory','Combinatorics','Analysis']);
for(const p of historical){
  assert.equal(p.statement_sha256,sha(p.problem));
  assert.ok(categories.has(p.category));
  assert.deepEqual(p.topics,[p.category]);
  for(const f of p.figures??[])assert.ok(p.problem.includes('https://eisatopon.github.io/national-olympiads-bank/'+f.src));
}
const checks=JSON.parse(fs.readFileSync('metadata/putnam-statement-checks.json','utf8')).collections['undergraduate/Putnam-problems.json'].statement_checks;
assert.equal(Object.keys(checks).length,240);
for(const y of published.years.filter(y=>y.year<1985))for(const p of y.problems){
  assert.equal(checks[`put.${y.year}.0.${p.number}`].reviewed_statement,p.problem);
}
const secondary=JSON.parse(fs.readFileSync('research/putnam/Putnam-1938-1964-Scholes-source-review.json','utf8'));
const queue=JSON.parse(fs.readFileSync('research/putnam/Putnam-1938-1964-secondary-comparison.json','utf8'));
assert.equal(secondary.edition_count,25);
assert.equal(secondary.numbered_statement_count,331);
assert.ok(secondary.editions.every(y=>y.year>=1938&&y.year<=1964));
assert.deepEqual(secondary.editions.filter(y=>y.year===1958).map(y=>y.edition),['Spring','Fall']);
assert.equal(secondary.publication_eligible,false);
assert.equal(queue.records.length,331);
assert.deepEqual(queue.existing_only_keys,[]);
assert.deepEqual(queue.secondary_only_keys,[]);
assert.ok(queue.records.every(r=>r.statement_verified===false&&r.original_wording_verified===false));
console.log('Public extension: 240 checked historical records, 492 recent records with twelve rendering-only repairs; 331 early secondary-source identities matched.');
