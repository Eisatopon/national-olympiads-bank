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
  console.log('Loader checks passed: duplicates blocked atomically, quarantine avoids fetch, topic preserved.');
})().catch(e => { console.error(e); process.exitCode = 1; });
