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
for (const day of imc2026.days) assert.ok(html.includes(day.questions_pdf), day.questions_pdf);
const officialIMC = papers.competitions.filter(x => x.competition_id === 'imc' && x.original_exams_verified).sort((a,b) => a.year-b.year);
assert.deepEqual(officialIMC.map(x => x.year), [2020, 2021, 2022, 2023, 2024, 2025, 2026]);
const editionSpecs = {
  2020: {dates:['2020-07-26','2020-07-27'], dayNumbers:[[1,2,3,4],[5,6,7,8]]},
  2021: {dates:['2021-08-03','2021-08-04'], dayNumbers:[[1,2,3,4],[5,6,7,8]]},
  2022: {dates:['2022-08-03','2022-08-04'], dayNumbers:[[1,2,3,4],[5,6,7,8]]},
  2023: {dates:['2023-08-02','2023-08-03'], dayNumbers:[[1,2,3,4,5],[6,7,8,9,10]]},
  2024: {dates:['2024-08-07','2024-08-08'], dayNumbers:[[1,2,3,4,5],[6,7,8,9,10]]},
  2025: {dates:['2025-07-30','2025-07-31'], dayNumbers:[[1,2,3,4,5],[6,7,8,9,10]]},
  2026: {dates:['2026-07-29','2026-07-30'], dayNumbers:[[1,2,3,4,5],[6,7,8,9,10]]}
};
for (const edition of officialIMC) {
  const spec = editionSpecs[edition.year];
  assert.deepEqual(edition.days.map(d => d.date), spec.dates, edition.year);
  assert.deepEqual(edition.days.map(d => d.numbers), spec.dayNumbers, edition.year);
  assert.equal(new Set(edition.days.flatMap(d => d.numbers)).size,
    edition.days.reduce((n,d) => n + d.numbers.length,0), 'No duplicate paper numbers');
  for (const day of edition.days) {
    assert.equal(day.page_count, 1);
    assert.ok(['verified_original','verified_original_visual_review'].includes(day.pdf_read), edition.year);
    assert.ok(html.includes(day.questions_pdf), day.questions_pdf);
  }
  assert.equal(edition.statement_text_imported, false);
  assert.equal(edition.source_rights, 'permission_not_documented');
}
assert.equal(papers.competitions.filter(x => x.original_exams_verified).length, 7);
const putnam = papers.competitions.filter(x => x.competition_id === 'put');
assert.equal(putnam.length, 8);
assert.deepEqual(putnam.map(x => x.year).sort((a,b) => a-b), [2018,2019,2020,2021,2022,2023,2024,2025]);
for (const edition of putnam) {
  assert.equal(edition.original_exams_verified, false, 'Link resolution is not a source-fidelity review');
  assert.equal(edition.source_link_status, 'exact_official_archive_pdf_link_resolved');
  assert.ok(edition.questions_pdf.startsWith('https://maa.org/wp-content/uploads/'));
  assert.equal(edition.pdf_pages, 2);
  assert.equal(edition.statement_text_imported, false);
}
for (const y of [2024, 2025]) assert.ok(html.includes(putnam.find(x => x.year === y).questions_pdf));
console.log('Undergraduate taxonomy and official paper index checks passed.');
