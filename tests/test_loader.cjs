const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const html = fs.readFileSync('index.html', 'utf8');
const code = html.slice(html.indexOf('function normalizeYears('), html.indexOf('function loadAll('));
const context = {
  BASE: './', cache: new Map(), inflight: new Map(), failed: new Map(), byUid: new Map(),
  CBY: { ok: {key:'ok',file:'ok.json'}, bad:{key:'bad',file:'bad.json'}, cn:{key:'cn',file:'cn.json',quarantined:true} },
  onCountrySettled() {}, fetch: async () => { throw Error('unexpected fetch'); }
};
vm.createContext(context); vm.runInContext(code, context);
(async () => {
  let calls = 0;
  context.fetch = async () => { calls++; return {ok:true,text:async()=>JSON.stringify({years:[{year:2025,problems:[{number:1,problem:'First',category:'Algebra'},{number:1,problem:'Second'}]}]})}; };
  await assert.rejects(context.loadCountry('bad'), /Duplicate problem identifiers/);
  assert.equal(context.byUid.size, 0);
  assert.equal(context.cache.has('bad'), false);
  await assert.rejects(context.loadCountry('cn'), /under review/);
  assert.equal(calls, 1);
  context.fetch = async () => ({ok:true,text:async()=>JSON.stringify({years:[{year:2025,problems:[{number:1,problem:'First',category:'Algebra'}]}]})});
  await context.loadCountry('ok');
  assert.equal(context.byUid.get('ok.2025.0.1').text, 'First');
  assert.equal(context.byUid.get('ok.2025.0.1').topic, 'Algebra');
  const provenanceCode = html.slice(html.indexOf('function safeSourceUrl('), html.indexOf('function problemHtml('));
  context.esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  context.URL = URL;
  context.collectionMetadata = {'ok.json': {missing_problem_numbers: {'2025':[4]}, source_links: [{url:'javascript:alert(1)'},{url:'https://example.com/archive'}]}};
  vm.runInContext(provenanceCode, context);
  const note = context.provenanceHtml({country:'ok',year:2025});
  assert.match(note, /missing problem 4/);
  assert.match(note, /https:\/\/example.com\/archive/);
  assert.doesNotMatch(note, /javascript:/);
  assert.doesNotMatch(note, /Not yet verified/);
  assert.doesNotMatch(context.provenanceHtml({country:'ok',year:2025}, true), /Not yet verified/);
  const record = {uid:'ok.2025.0.1',country:'ok',year:2025,text:'First'};
  context.collectionMetadata['ok.json'].statement_checks = {'ok.2025.0.1': {status:'statement_checked_against_source', reviewed_statement:'First',source_url:'https://example.com/exam.pdf',source_page:1,source_problem_number:1,checked_at:'2026-10-02'}};
  assert.match(context.provenanceHtml(record), /Statement checked against source/);
  assert.match(context.provenanceHtml(record, true), /page 1, problem 1/);
  assert.match(context.provenanceHtml({...record,text:'Changed'}), /Sources and notes/);
  assert.match(context.provenanceHtml({...record,uid:'ok.2025.0.2'}), /Sources and notes/);
  context.collectionMetadata['ok.json'].statement_checks[record.uid].source_url='javascript:alert(1)';
  assert.match(context.provenanceHtml(record), /Sources and notes/);
  assert.equal(context.provenanceHtml({...record,year:2024}, true), '');
  context.collectionMetadata = {};
  assert.equal(context.provenanceHtml(record), '');
  assert.equal(context.provenanceHtml(record, true), '');
  console.log('Loader checks passed: duplicates blocked atomically, quarantine avoids fetch, topic preserved.');
})().catch(e => { console.error(e); process.exitCode = 1; });
