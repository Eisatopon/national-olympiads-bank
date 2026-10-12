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
let verified = 0;
for (const year of data.years) {
  assert.equal(year.problems.length, countByYear(year.year), 'Wrong annual count '+year.year);
  assert.deepEqual(year.problems.map(p=>p.number), Array.from({length:countByYear(year.year)},(_,i)=>i+1));
  for (const p of year.problems) {
    const id = year.year+':'+p.number;
    if (year.year >= 2004 && year.year <= 2008) {
      const expectedDay = p.number <= 6 ? 1 : 2;
      const officialCandidate = `https://www.imc-math.org.uk/imc${year.year}/day${expectedDay}_solutions.pdf`;
      assert.equal(p.official_pdf_candidate_url, officialCandidate, 'Misassigned IMC official PDF candidate '+id);
    }
    assert.ok(!ids.has(id), 'Duplicate '+id); ids.add(id);
    assert.ok(typeof p.problem === 'string' && p.problem.trim().length >= 30, 'Empty '+id);
    assert.ok(typeof p.statement_verified === 'boolean', 'Missing verification flag '+id);
    if (p.statement_verified) {
      verified++;
      assert.ok(typeof p.verification_source === 'string' && /^https:\/\//.test(p.verification_source), 'Missing original source '+id);
      assert.ok(typeof p.verification_method === 'string' && p.verification_method.trim(), 'Missing verification method '+id);
      assert.ok(Number.isInteger(p.verification_page) && p.verification_page > 0, 'Missing original PDF page '+id);
      assert.ok(/^\d{4}-\d{2}-\d{2}$/.test(p.verified_on || ''), 'Missing review date '+id);
      assert.ok(Array.isArray(p.review_flags) && p.review_flags.length === 0, 'Unresolved flags on verified record '+id);
    } else {
      assert.ok(Array.isArray(p.review_flags) && p.review_flags.length > 0, 'Unverified record requires review flags '+id);
    }
    assert.ok(Array.isArray(p.topics) && Array.isArray(p.problem_dna), 'Missing classification arrays '+id);
    assert.equal(p.day, p.number <= countByYear(year.year)/2 ? 1 : 2, 'Incorrect day '+id);
    const url = 'https://studolymp.com/imc/problems/imc-'+year.year+'-d'+p.day+'-p'+
      (p.day===1?p.number:p.number-countByYear(year.year)/2);
    assert.equal(p.source_url,url,'Wrong source URL '+id);
    assert.ok(!/\[(MATH|FIGURE)_REQUIRES_REVIEW\]/.test(p.problem),'Broken math or figure '+id);
    assert.ok(!/solution\s*\(official\)|show solution/i.test(p.problem),'Solution leaked '+id);
    assert.equal((p.problem.match(/\$/g)||[]).length%2,0,'Unbalanced inline math delimiters '+id);
    if (p.latex_annotations_for_review?.length) withLatex++;
    count++;
  }
}
assert.equal(count, 354);
assert.equal(withLatex, 350);
const html = fs.readFileSync('index.html','utf8');
assert.ok(html.includes("key: 'imc', name: 'IMC'"));
assert.ok(html.includes("file: 'undergraduate/IMC-1994-2026-review.json'"));
assert.ok(html.includes("if (key === 'imc') return {"));
assert.ok(html.includes("c.key === 'imc' ? 354"));
assert.ok(html.includes("loadCountry('imc')"));
assert.ok(html.includes("354 statements available in the year grid"));
console.log(`IMC review archive: 33 years, 354 sourced statements, 350 with LaTeX; ${verified} original-source-verified, ${count-verified} pending. Publication remains blocked.`);
