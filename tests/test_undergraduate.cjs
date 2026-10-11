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
console.log('Undergraduate taxonomy and source-only UI validation passed.');
