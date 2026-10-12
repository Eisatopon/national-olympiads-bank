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
  assert.equal(r.statements_imported, r.id === 'vjimc' ? 261 : r.id === 'smmc' ? 88 : 0);
  assert.equal(r.republication_permission, r.id === 'vjimc' ? 'oral_permission_reported_by_project_owner_2026-10-12' : r.id === 'smmc' ? 'publication_requested_by_project_owner_2026-10-12_no_licence_inferred' : 'not_established');
  assert.ok(r.paper_structure && r.source_status);
}
assert.match(html, /\['undergraduate', 'Undergraduate'\]/);
assert.doesNotMatch(html, /id="undergraduateSources"|class="undergraduate-card"/);
assert.match(html, /key: 'seemous'.*scope: 'undergraduate'/);
const seemous = JSON.parse(fs.readFileSync('undergraduate/SEEMOUS-2007-2010-problems.json', 'utf8'));
assert.deepEqual(seemous.years.map(y => y.year), Array.from({length:20}, (_,i) => 2007 + i));
assert.ok(seemous.years.every(y => y.problems.length === 4));
assert.ok(seemous.years.every(y => y.problems.every((p,i) => p.number === i + 1 && typeof p.problem === 'string' && p.problem.trim())));
assert.match(html, /c\.key === 'seemous' \? 80/);
const papers = JSON.parse(fs.readFileSync('metadata/undergraduate-official-papers.json', 'utf8'));
assert.equal(papers.schema_version, 1);
assert.equal(papers.competitions.length, 41);
assert.equal(new Set(papers.competitions.map(x => x.competition_id + ':' + x.year)).size, 41);
for (const paper of papers.competitions) {
  assert.ok(['imc','put'].includes(paper.competition_id));
  assert.equal(paper.source_rights, paper.competition_id === 'imc' ? 'oral_permission_reported_by_project_owner_2026-10-12_not_independently_verified' : 'permission_not_documented');
  assert.equal(paper.statement_text_imported, false);
  assert.ok(paper.year_page.startsWith('https://'));
}
const imc2026 = papers.competitions.find(x => x.competition_id === 'imc' && x.year === 2026);
assert.equal(imc2026.original_exams_verified, true);
assert.deepEqual(imc2026.days.map(x => x.numbers), [[1,2,3,4,5],[6,7,8,9,10]]);
assert.deepEqual(imc2026.days.map(x => x.date), ['2026-07-29','2026-07-30']);
const officialIMC = papers.competitions.filter(x => x.competition_id === 'imc' && x.original_exams_verified).sort((a,b) => a.year-b.year);
assert.deepEqual(officialIMC.map(x => x.year), [2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026]);
const editionSpecs = {
  2017: {dates:['2017-08-02','2017-08-03'], dayNumbers:[[1,2,3,4,5],[6,7,8,9,10]]},
  2018: {dates:['2018-07-24','2018-07-25'], dayNumbers:[[1,2,3,4,5],[6,7,8,9,10]]},
  2019: {dates:['2019-07-30','2019-07-31'], dayNumbers:[[1,2,3,4,5],[6,7,8,9,10]]},
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
  }
  assert.equal(edition.statement_text_imported, false);
  assert.equal(edition.source_rights, 'oral_permission_reported_by_project_owner_2026-10-12_not_independently_verified');
}
assert.equal(papers.competitions.filter(x => x.original_exams_verified).length, 10);
const historical = papers.competitions.filter(x => x.competition_id === 'imc' && x.year >= 1994 && x.year <= 2016).sort((a,b) => a.year - b.year);
assert.deepEqual(historical.map(x => x.year), Array.from({length:23}, (_,i) => 1994 + i));
assert.equal(papers.historical_archive_review.year_pages_verified, 23);
assert.equal(papers.historical_archive_review.original_full_year_papers_certified, 0);
const combined1990s = new Set([1994,1995,1996]);
for (const edition of historical) {
  assert.equal(edition.archive_year_page_verified, true, edition.year);
  assert.equal(edition.original_exams_verified, false, edition.year);
  assert.equal(edition.statement_text_imported, false, edition.year);
  assert.equal(edition.source_rights, 'oral_permission_reported_by_project_owner_2026-10-12_not_independently_verified', edition.year);
  assert.ok(edition.year_page.endsWith('year=' + edition.year));
  
  if (combined1990s.has(edition.year)) {
    assert.equal(edition.verified_primary_pdf.format, 'combined_problems_and_solutions_both_days');
    
  }
}
assert.equal(historical.filter(x => x.verified_primary_pdf).length, 7);
assert.equal(papers.historical_archive_review.full_year_official_document_link_sets_verified, 23);
assert.equal(papers.historical_archive_review.original_pdf_links_verified, 43);
const links = new Set();
for (const edition of historical) {
  const docs = edition.official_original_documents;
  assert.equal(edition.official_original_document_links_confirmed, true, edition.year);
  assert.equal(docs.length, edition.year <= 1996 ? 1 : 2, edition.year);
  assert.deepEqual(docs.map(d => d.paper), edition.year <= 1996 ? ['combined'] : ['day_1', 'day_2'], edition.year);
  for (const d of docs) {
    assert.match(d.official_url, /^https:\/\/www\.imc-math\.org\.uk\/imc\d{4}\//);
    assert.ok(d.official_url.includes('/imc' + edition.year + '/'));
    
    assert.ok(!links.has(d.official_url), 'Duplicate original document link');
    links.add(d.official_url);
  }
  assert.equal(edition.original_exams_verified, false);
  assert.equal(edition.statement_text_imported, false);
}
assert.equal(links.size, 43);


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

console.log('Undergraduate taxonomy and official paper index checks passed.');
