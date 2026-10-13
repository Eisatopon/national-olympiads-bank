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
const putMeta=JSON.parse(fs.readFileSync('metadata/putnam-statement-checks.json','utf8')).collections;
Object.assign(ctx.collectionMetadata,putMeta);
ctx.CBY.put={file:'undergraduate/Putnam-problems.json'};
const rangeCheck=putMeta['undergraduate/Putnam-problems.json'].statement_checks['put.1965.0.A3'];
const rangeRecord={country:'put',year:1965,uid:'put.1965.0.A3',text:rangeCheck.reviewed_statement};
for(const print of [false,true]){
 const rendered=ctx.provenanceHtml(rangeRecord,print);
 assert.match(rendered,/Statement checked against source/);
 assert.match(rendered,/pages 15, 16/);
}
const savedPages=rangeCheck.source_pages;
rangeCheck.source_pages=[15,0];
assert.doesNotMatch(ctx.provenanceHtml(rangeRecord),/Statement checked against source/);
rangeCheck.source_pages=savedPages;
const secondaryCheck=putMeta['undergraduate/Putnam-problems.json'].statement_checks['put.1959.0.A1'];
const secondaryRecord={country:'put',year:1959,uid:'put.1959.0.A1',text:secondaryCheck.reviewed_statement};
for(const print of [false,true]){
 const rendered=ctx.provenanceHtml(secondaryRecord,print);
 assert.match(rendered,/Secondary-source comparison/);
 assert.doesNotMatch(rendered,/Statement checked against source|Exam source|page 1/);
 assert.doesNotMatch(ctx.provenanceHtml({...secondaryRecord,text:'Changed statement.'},print),/Secondary-source comparison/);
 const issueCheck=putMeta['undergraduate/Putnam-problems.json'].statement_checks['put.1959.0.B5'];
 assert.doesNotMatch(ctx.provenanceHtml({country:'put',year:1959,uid:'put.1959.0.B5',text:issueCheck.reviewed_statement},print),/Source issue — awaiting verification/);
}
const archiveCheck=putMeta['undergraduate/Putnam-problems.json'].statement_checks['put.1992.0.B6'];
const archiveRecord={country:'put',year:1992,uid:'put.1992.0.B6',text:archiveCheck.reviewed_statement};
for(const print of [false,true]){
 const rendered=ctx.provenanceHtml(archiveRecord,print);
 assert.match(rendered,/Statement checked against archive transcription/);
 assert.doesNotMatch(rendered,/Compared visually and textually|Exam source|page 1/);
 assert.doesNotMatch(ctx.provenanceHtml({...archiveRecord,text:'Changed statement.'},print),/Statement checked against archive transcription/);
}
const savedBasis=archiveCheck.verification_basis;archiveCheck.verification_basis='unsupported';
assert.doesNotMatch(ctx.provenanceHtml(archiveRecord),/Statement checked against archive transcription/);
archiveCheck.verification_basis=savedBasis;

const edited=putMeta['undergraduate/Putnam-problems.json'].statement_checks['put.1978.0.A5'];
for(const print of [false,true]){
 const text=ctx.provenanceHtml({country:'put',year:1978,uid:'put.1978.0.A5',text:edited.reviewed_statement},print);
 assert.match(text,/Edited statement — source correction recorded/);
 assert.doesNotMatch(text,/Source issue — awaiting verification|Compared visually and textually/);
}
