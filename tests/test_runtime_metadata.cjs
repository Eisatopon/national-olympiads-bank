// The browser uses slim metadata (fingerprints instead of full statement copies).
// Check that it is current and that it gives exactly the same answers as the audit files.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const html = fs.readFileSync('index.html', 'utf8');
const ctx = {URL, CBY:{}, esc:s=>String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/"/g,'&quot;')};
vm.createContext(ctx);
vm.runInContext(html.slice(html.indexOf('function textHash('), html.indexOf('function normalizeYears(')), ctx);
vm.runInContext(html.slice(html.indexOf('function safeSourceUrl('), html.indexOf('/* ---------- Mathematical connections')), ctx);

const read = f => JSON.parse(fs.readFileSync(f, 'utf8'));
const full = {...read('metadata/topic-overrides.json').records, ...read('metadata/topic-overrides-final575.json').records};
const slim = read('metadata/runtime/topics.json').records;
let n = 0;
for (const [uid, rec] of Object.entries(full)) {
  if (!rec.reviewed_statement || !rec.topics?.length) continue;
  assert.ok(slim[uid], `${uid}: missing from runtime topics`);
  assert.equal(slim[uid][1], ctx.textHash(rec.reviewed_statement), `${uid}: fingerprint differs between Python and browser`);
  assert.deepEqual(slim[uid][0], rec.topics, `${uid}: topics differ`);
  n++;
}
assert.equal(Object.keys(slim).length, n);
// An edited statement must lose its reviewed topics.
ctx.topicOverrides = {'x.1': {topics: ['Geometry'], h: ctx.textHash('Original.')}};
vm.runInContext('topicOverrides = this.topicOverrides', ctx);
assert.deepEqual(Array.from(ctx.topicFields('Original.', null, 'x.1').topics), ['Geometry']);
assert.notDeepEqual(Array.from(ctx.topicFields('Edited.', null, 'x.1').topics), ['Geometry']);

// Provenance rendered from slim metadata must match the full audit metadata, statement by statement.
const fullMeta = read('metadata/collections.json').collections;
const slimMeta = read('metadata/runtime/collections.json').collections;
let checked = 0;
for (const [file, meta] of Object.entries(fullMeta)) {
  const uids = new Set([...Object.keys(meta.statement_checks || {}), ...Object.keys(meta.statement_notes || {})]);
  for (const uid of uids) {
    const key = uid.split('.')[0];
    ctx.CBY[key] = {file};
    const text = (meta.statement_checks?.[uid] || meta.statement_notes?.[uid]).reviewed_statement;
    const p = {uid, country: key, year: +uid.split('.')[1], text};
    for (const print of [false, true]) {
      ctx.collectionMetadata = fullMeta; vm.runInContext('collectionMetadata = this.collectionMetadata', ctx);
      const a = ctx.provenanceHtml(p, print);
      ctx.collectionMetadata = slimMeta; vm.runInContext('collectionMetadata = this.collectionMetadata', ctx);
      const b = ctx.provenanceHtml(p, print);
      assert.equal(b, a, `${uid}: provenance differs with runtime metadata`);
    }
    checked++;
  }
}
// The manifest (counts per file and year) must match what the browser derives from the full files,
// because the grid and the totals are drawn from it before any collection is downloaded.
const manifest = read('metadata/runtime/manifest.json').files;
vm.runInContext(html.slice(html.indexOf('function normalizeYears('), html.indexOf('function loadCountry(')), ctx);
const entries = [...html.matchAll(/\{\s*key:\s*'(\w+)',\s*name:\s*'[^']*',\s*flag:\s*'[^']*',\s*file:\s*'([^']+)',\s*kind:\s*'(\w+)'/g)];
assert.ok(entries.length > 50, 'COUNTRIES entries not found');
let files = 0;
for (const [, key, file, kind] of entries) {
  const raw = read(file);
  const list = kind === 'usa' ? ctx.normalizeUsa({key}, raw) : ctx.normalizeYears({key}, raw);
  const years = {};
  list.forEach(p => { years[p.year] = (years[p.year] || 0) + 1; });
  assert.ok(manifest[file], `${file}: missing from the manifest`);
  assert.deepEqual(Object.fromEntries(Object.entries(manifest[file].years).map(([y, c]) => [y, c])), Object.fromEntries(Object.entries(years).map(([y, c]) => [String(y), c])), `${file}: manifest counts differ`);
  assert.equal(manifest[file].total, list.length, `${file}: manifest total differs`);
  files++;
}
console.log(`Runtime metadata checks passed: ${n} topic fingerprints, ${checked} provenance records identical, ${files} manifest entries match.`);
