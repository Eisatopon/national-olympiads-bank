const fs = require('node:fs');
const assert = require('node:assert/strict');

const path = 'undergraduate/IMC-1994-2026-review.json';
const data = JSON.parse(fs.readFileSync(path, 'utf8'));
const countByYear = y => y <= 2008 ? 12 : y <= 2019 ? 10 : y <= 2022 ? 8 : 10;
assert.equal(data.short_name, 'IMC');
assert.equal(data.status, 'DRAFT_REQUIRES_OFFICIAL_PDF_VERIFICATION');
assert.equal(data.publication_eligible, false);
assert.equal(data.problem_count, 354);
assert.deepEqual(data.years.map(y => y.year), Array.from({length:33}, (_,i) => 1994+i));
const ids = new Set();
let count = 0;
let withLatex = 0;
for (const year of data.years) {
  assert.equal(year.problems.length, countByYear(year.year), 'Wrong annual count '+year.year);
  assert.deepEqual(year.problems.map(p=>p.number), Array.from({length:countByYear(year.year)},(_,i)=>i+1));
  for (const p of year.problems) {
    const id = year.year+':'+p.number;
    assert.ok(!ids.has(id), 'Duplicate '+id); ids.add(id);
    assert.ok(typeof p.problem === 'string' && p.problem.trim().length >= 30, 'Empty '+id);
    assert.equal(p.statement_verified, false, 'Unverified statement must not be certified: '+id);
    assert.ok(Array.isArray(p.review_flags) && p.review_flags.length > 0, 'Review required '+id);
    assert.ok(Array.isArray(p.topics) && Array.isArray(p.problem_dna), 'Missing classification arrays '+id);
    assert.equal(p.day, p.number <= countByYear(year.year)/2 ? 1 : 2, 'Incorrect day '+id);
    const url = 'https://studolymp.com/imc/problems/imc-'+year.year+'-d'+p.day+'-p'+
      (p.day===1?p.number:p.number-countByYear(year.year)/2);
    assert.equal(p.source_url,url,'Wrong source URL '+id);
    assert.ok(!/\\[(MATH|FIGURE)_REQUIRES_REVIEW\\]/.test(p.problem),'Broken math or figure '+id);
    assert.ok(!/solution\\s*\\(official\\)|show solution/i.test(p.problem),'Solution leaked '+id);
    assert.equal((p.problem.match(/\\$/g)||[]).length%2,0,'Unbalanced inline math delimiters '+id);
    if (p.latex_annotations_for_review?.length) withLatex++;
    count++;
  }
}
assert.equal(count, 354);
assert.equal(withLatex, 350);
const html = fs.readFileSync('index.html','utf8');
assert.match(html, /key: 'imc'.*file: 'undergraduate\\/IMC-1994-2026-review\\.json'.*scope: 'undergraduate'/);
assert.match(html, /if \\(key === 'imc'\\) return \\{/);
assert.match(html, /c\\.key === 'imc' \\? 354/);
assert.match(html, /loadCountry\\('imc'\\)/);
assert.match(html, /354 statements available in the year grid/);
console.log('IMC review archive: 33 years, 354 distinct nonempty sourced statements, 350 with LaTeX; all remain unverified.');
