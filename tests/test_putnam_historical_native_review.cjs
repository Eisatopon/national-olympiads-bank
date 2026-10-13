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
