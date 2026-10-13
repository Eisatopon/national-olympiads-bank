// Miklós Schweitzer 1949-1961: full annual sets from the 1968 English volume, with exact source checks.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const crypto = require('node:crypto');
const vm = require('node:vm');
const read = path => JSON.parse(fs.readFileSync(path, 'utf8'));
const file = 'undergraduate/Schweitzer-problems.json';
const data = read(file);
const meta = read('metadata/schweitzer-statement-checks.json').collections[file];
const html = fs.readFileSync('index.html', 'utf8');
const hash = s => crypto.createHash('sha256').update(s).digest('hex');
const SRC = 'https://real-eod.mtak.hu/14558/1/AkademiaiKiado_007070.pdf';
// Year totals printed in Chapter 2 of the book (1950 had two rounds).
const expected = {1949: 8, 1950: 19, 1951: 17, 1952: 10, 1953: 10, 1954: 10, 1955: 10, 1956: 10, 1957: 10, 1958: 11, 1959: 10, 1960: 10, 1961: 10};
assert.deepEqual(data.years.map(y => y.year), Object.keys(expected).map(Number));
assert.equal(data.problem_count, 145);
let n = 0;
for (const y of data.years) {
  assert.equal(y.problems.length, expected[y.year], `${y.year}: count`);
  const rounds = y.year === 1950 ? [1, 2] : [undefined];
  for (const d of rounds) {
    const list = y.problems.filter(p => p.day === d);
    assert.deepEqual(list.map(p => p.number), list.map((_, i) => i + 1), `${y.year}/${d}: numbering`);
    if (y.year === 1950) assert.equal(list.length, d === 1 ? 10 : 9);
  }
  for (const p of y.problems) {
    const uid = `schw.${y.year}.${p.day || 0}.${p.number}`;
    if (y.year === 1950) assert.equal(p.paper_label, p.day === 1 ? 'First round' : 'Second round');
    else assert.ok(!('day' in p) && !('paper_label' in p), uid);
    assert.equal(hash(p.problem), p.statement_sha256, uid);
    assert.equal((p.problem.match(/\$/g) || []).length % 2, 0, uid);
    assert.doesNotMatch(p.problem, /¶|\\tag|\\cancel|[\x00-\x08\x0b\x0c\x0e-\x1f]/, uid);
    assert.ok(p.problem.length >= 40, uid);
    assert.deepEqual(p.topics, [p.category]);
    assert.ok(['Algebra', 'Geometry', 'Combinatorics', 'Number Theory', 'Analysis'].includes(p.category), uid);
    assert.ok(!('solution' in p), uid);
    const c = meta.statement_checks[uid];
    assert.ok(c, uid);
    assert.equal(c.reviewed_statement, p.problem, uid);
    assert.equal(c.statement_sha256, p.statement_sha256, uid);
    assert.equal(c.source_url, SRC);
    const pages = c.source_page ? [c.source_page] : c.source_pages;
    assert.deepEqual(pages, p.verification_pages, uid);
    assert.ok(pages.every(pg => pg >= 15 && pg <= 36), uid);
    assert.equal(c.source_problem_number, p.number);
    assert.equal(c.review_method, 'AI-assisted visual and textual comparison');
    n++;
  }
}
assert.equal(Object.keys(meta.statement_checks).length, 145);
// The one disclosed misprint correction is not presented as original wording.
assert.deepEqual(Object.keys(meta.statement_notes), ['schw.1950.2.3']);
assert.equal(meta.statement_checks['schw.1950.2.3'].original_wording_verified, false);
const get = (y, n, d) => data.years.find(b => b.year === y).problems.find(p => p.number === n && p.day === d);
// Formulas that the book's OCR layer loses or garbles.
assert.ok(get(1950, 2, 2).problem.includes('q \\equiv 1 \\pmod 4'));
assert.ok(get(1950, 3, 2).problem.includes('n_0 = n_0(\\varepsilon)') && get(1950, 3, 2).problem.includes('f_\\nu(x_1\', x_2\', \\ldots, x_n\') \\leqq \\varepsilon'));
assert.ok(get(1951, 3).problem.includes('f(x) = 4x - 4x^2'));
assert.ok(get(1952, 4).problem.includes('\\overline{f(x)}=\\sum_{i=0}^{n}a_ix^{p^i}'));
assert.ok(get(1956, 8).problem.includes('\\right)^{\\frac12-\\varepsilon}'));
assert.ok(get(1960, 6).problem.includes('n_k^{\\frac{1}{2^k}}'));
assert.ok(get(1955, 4).problem.includes('p^\\alpha = q^\\beta + r^\\alpha'));
assert.match(html, /key: 'schw'.*file: 'undergraduate\/Schweitzer-problems\.json'.*scope: 'undergraduate'/);
const ctx = {};
vm.createContext(ctx);
vm.runInContext(html.slice(html.indexOf('function textHash('), html.indexOf('function loadCountry(')), ctx);
const normalized = ctx.normalizeYears({key: 'schw'}, data);
assert.equal(new Set(normalized.map(p => p.uid)).size, 145);
assert.equal(normalized.filter(p => p.year === 1950 && p.paperLabel === 'Second round').length, 9);
const manifest = read('metadata/runtime/manifest.json').files[file];
assert.equal(manifest.total, 145);
console.log(`Schweitzer 1949-1961: ${n} statements, 14 papers, year totals match the 1968 volume, source checks and runtime manifest consistent.`);
