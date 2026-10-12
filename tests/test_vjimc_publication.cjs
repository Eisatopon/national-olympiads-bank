const assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm'),crypto=require('node:crypto');
const html=fs.readFileSync('index.html','utf8');
const raw=JSON.parse(fs.readFileSync('undergraduate/Vojtech-Jarnik-problems.json','utf8'));
const held=Array.from({length:36},(_,i)=>1991+i).filter(y=>![2020,2021,2023].includes(y));
assert.deepEqual(raw.years.map(y=>y.year),held);
const counts={1991:4,1995:7,1996:6,1997:10,1998:10};
const paperIds=new Set(),assets=new Set();let total=0;
for(const y of raw.years){
 assert.equal(y.problems.length,counts[y.year]||8,`${y.year}: paper coverage`);
 const ids=new Set();
 for(const p of y.problems){
  const id=`${y.year}.${p.paper}.${p.number}`;assert.ok(!ids.has(id),id);ids.add(id);
  paperIds.add(`${y.year}.${p.paper}`);total++;
  assert.ok(['I','II'].includes(p.paper));assert.equal(p.paper_id,p.paper==='I'?1:2);
  assert.equal(p.paper_label,'Category '+p.paper);assert.ok(!('day' in p),'Category must not be encoded as a competition day');
  assert.ok(String(p.number).match(/^[1-4](?:-[MI])?$/));
  assert.ok(p.problem.trim().length>15);assert.doesNotMatch(p.problem,/\bSolution\b|\[MATH_REQUIRES_REVIEW\]/);
  assert.equal(p.statement_verified,true);assert.equal(p.text_transcription_verified,false);
  assert.match(p.verification_scope,/image/);assert.match(p.verification_source,/^https:\/\/(?:jarnik|vjimc)\.osu\.cz\/storage\/uploads\/j\d+problems[12]?\.pdf$/);
  assert.ok(p.verification_page>=1);assert.equal(p.source_crop_points.length,4);
  assert.match(p.source_document_sha256,/^[0-9a-f]{64}$/);
  const a=p.statement_asset;assert.match(a.src,/^assets\/statements\/vjimc\/\d{4}-(?:I|II)-p\d+[MI]?\.png$/);
  assert.ok(!assets.has(a.src));assets.add(a.src);assert.match(a.alt,/Αυθεντική εκφώνηση/);
  const data=fs.readFileSync(a.src);assert.equal(data.subarray(0,8).toString('hex'),'89504e470d0a1a0a');
  assert.equal(crypto.createHash('sha256').update(data).digest('hex'),a.sha256,`${id}: changed original crop`);
  assert.equal(data.readUInt32BE(16),a.width);assert.equal(data.readUInt32BE(20),a.height);
  assert.ok(a.width>700 && a.height>50);
 }
 if([1997,1998].includes(y.year))for(const paper of ['I','II'])for(const number of ['4-M','4-I'])assert.ok(y.problems.some(p=>p.paper===paper&&p.number===number));
}
assert.equal(total,261);assert.equal(paperIds.size,65);assert.equal(assets.size,261);
assert.deepEqual(raw.years[0].problems.map(p=>p.paper),['I','I','I','I']);
const ctx={URL,BASE:'./',topicOverrides:{},esc:s=>String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/"/g,'&quot;'),CBY:{vjimc:{name:'Vojtěch Jarník'}},location:{href:'https://eisatopon.github.io/national-olympiads-bank/'}};
vm.createContext(ctx);
vm.runInContext(html.slice(html.indexOf('function textHash('),html.indexOf('function loadCountry(')),ctx);
vm.runInContext(html.slice(html.indexOf('const IMG_RE ='),html.indexOf('/* ==========================================================\n   Φόρτωση')),ctx);
vm.runInContext(html.slice(html.indexOf('function aiPrompt('),html.indexOf('function aiUrl(')),ctx);
const list=ctx.normalizeYears({key:'vjimc'},raw);assert.equal(list.length,261);assert.equal(new Set(list.map(p=>p.uid)).size,261);
const p=list.find(p=>p.year===2026&&p.day===2&&p.num===4);
assert.equal(p.paperLabel,'Category II');assert.match(ctx.bodyHtml(p.text,p),/statement-original/);
assert.match(ctx.bodyHtml(p.text,p),/2026-II-p4\.png/);assert.doesNotMatch(ctx.bodyHtml(p.text,p),/\bProblem 4 Let/);
assert.doesNotMatch(ctx.bodyHtml('Safe text',{statementAsset:{src:'javascript:alert(1)'}}),/<img/);
const prompt=ctx.aiPrompt(p);assert.match(prompt,/Category II/);assert.match(prompt,/2026-II-p4\.png/);assert.match(prompt,/ask me to upload/);assert.doesNotMatch(prompt,/Day \/ Test/);
const manifest=JSON.parse(fs.readFileSync('metadata/runtime/manifest.json','utf8')).files['undergraduate/Vojtech-Jarnik-problems.json'];
assert.equal(manifest.total,261);assert.equal(Object.keys(manifest.years).length,33);
assert.match(html,/key: 'vjimc'.*scope: 'undergraduate'/);
console.log('VJIMC: 33 editions, 65 category papers, 261 original statement assets; alternatives, hashes, loader, category labels, safe image rendering and AI handoff verified.');
