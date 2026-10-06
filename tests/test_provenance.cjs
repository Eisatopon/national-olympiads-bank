const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const html = fs.readFileSync('index.html', 'utf8');
const metadata = JSON.parse(fs.readFileSync('metadata/collections.json', 'utf8')).collections;
const ctx = {URL, collectionMetadata:metadata, CBY:{ca:{file:'Canada-cmo-problems.json'}},
  esc:s=>String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/"/g,'&quot;')};
vm.createContext(ctx);
vm.runInContext(html.slice(html.indexOf('function textHash('),html.indexOf('function classifyStatement(')),ctx);
vm.runInContext(html.slice(html.indexOf('function safeSourceUrl('),html.indexOf('/* ---------- Mathematical connections')),ctx);
const uid='ca.1969.0.1';
const text=metadata['Canada-cmo-problems.json'].statement_checks[uid].reviewed_statement;
const record={uid,country:'ca',year:1969,text};
for(const print of [false,true]) {
  const rendered=ctx.provenanceHtml(record,print);
  assert.match(rendered,/Editorial clarification/);
  assert.match(rendered,/0\/0/);
  const changed=ctx.provenanceHtml({...record,text:'A different problem.'},print);
  assert.doesNotMatch(changed,/Editorial clarification|Statement checked against source/);
}
const note=metadata['Canada-cmo-problems.json'].statement_notes[uid];
note.text='<img src=x onerror=alert(1)>';
assert.match(ctx.provenanceHtml(record),/&lt;img/);
assert.doesNotMatch(ctx.provenanceHtml(record),/<img src=x/);
const checked=ctx.provenanceHtml({country:'ca',year:2026,uid:'ca.2026.0.1',text:metadata['Canada-cmo-problems.json'].statement_checks['ca.2026.0.1'].reviewed_statement});
assert.match(checked,/not the solution or independent mathematical correctness/);
ctx.CBY.tht={file:'Thailand-tst-problems.json'};
const defective=metadata['Thailand-tst-problems.json'].statement_checks['tht.2012.9.25'];
for(const print of [false,true]) {
  const rendered=ctx.provenanceHtml({country:'tht',year:2012,uid:'tht.2012.9.25',text:defective.reviewed_statement},print);
  assert.match(rendered,/Source issue — awaiting verification/);
  assert.doesNotMatch(rendered,/Statement checked against source/);
  assert.match(rendered,/do not use/);
}
console.log('Provenance checks passed: editorial notes in screen/print, stale evidence hidden, HTML escaped, source scope explicit.');
