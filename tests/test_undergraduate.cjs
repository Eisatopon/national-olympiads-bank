const fs = require('node:fs');
const assert = require('node:assert/strict');
const data = JSON.parse(fs.readFileSync('metadata/undergraduate-competitions.json', 'utf8'));
const html = fs.readFileSync('index.html', 'utf8');
assert.equal(data.schema_version, 1);
assert.equal(data.section, 'undergraduate');
assert.deepEqual(data.records.map(r => r.id), ['put', 'imc', 'seemous', 'vjimc', 'smmc']);
assert.equal(new Set(data.records.map(r => r.id)).size, data.records.length);
for (const r of data.records) {
  assert.ok(r.name && r.audience && r.geography && r.scope.includes('university'), r.id);
  assert.equal(r.statements_imported, 0, 'No rights-cleared contest statements imported');
  assert.equal(r.republication_permission, 'not_established');
  assert.ok(r.paper_structure && r.source_status);
}
assert.match(html, /\['undergraduate', 'Undergraduate'\]/);
assert.match(html, /id="undergraduateSources"/);
assert.match(html, /four 90-minute sessions/);
assert.match(html, /A, B and C are distinct paper variants/);
assert.ok(!/scope:\s*'undergraduate'/.test(html), 'Source cards must not be represented as exam problems');
const papers = JSON.parse(fs.readFileSync('metadata/undergraduate-official-papers.json', 'utf8'));
assert.equal(papers.schema_version, 1);
assert.equal(papers.competitions.length, 41);
assert.equal(new Set(papers.competitions.map(x => x.competition_id + ':' + x.year)).size, 41);
for (const paper of papers.competitions) {
  assert.ok(['imc','put'].includes(paper.competition_id));
  assert.equal(paper.source_rights, 'permission_not_documented');
  assert.equal(paper.statement_text_imported, false);
  assert.ok(paper.year_page.startsWith('https://'));
}
const imc2026 = papers.competitions.find(x => x.competition_id === 'imc' && x.year === 2026);
assert.equal(imc2026.original_exams_verified, true);
assert.deepEqual(imc2026.days.map(x => x.numbers), [[1,2,3,4,5],[6,7,8,9,10]]);
assert.deepEqual(imc2026.days.map(x => x.date), ['2026-07-29','2026-07-30']);
for (const day of imc2026.days) assert.match(html, new RegExp(day.questions_pdf.replace(/[.*+?^${}()|[\]\\]/g, '\\console.log('Undergraduate taxonomy and source-only UI validation passed.');')));
assert.equal(papers.competitions.filter(x => x.original_exams_verified).length, 1);
console.log('Undergraduate taxonomy and official paper index checks passed.');
