const fs=require('fs'),vm=require('vm'),assert=require('node:assert/strict');
const html=fs.readFileSync('index.html','utf8');
const metadata=JSON.parse(fs.readFileSync('metadata/topic-overrides.json','utf8'));
const ctx={topicOverrides:metadata.records};vm.createContext(ctx);
vm.runInContext(html.slice(html.indexOf('function classifyStatement('),html.indexOf('function normalizeYears(')),ctx);
for(const [uid,r] of Object.entries(metadata.records)) assert.deepEqual(Array.from(ctx.topicFields(r.reviewed_statement,null,uid).topics),r.topics,uid);
// Check that real source records (including existing categories) actually use the reviews.
const sourceRecords=new Map();
for(const m of html.matchAll(/key: '([^']+)'[^\n]*file: '([^']+)'[^\n]*/g)) {
  if(m[0].includes('quarantined: true')) continue;
  const data=JSON.parse(fs.readFileSync(m[2],'utf8'));
  if(!Array.isArray(data.years)) continue;
  for(const y of data.years) for(const p of y.problems) {
    const uid=`${m[1]}.${y.year}.${p.day||0}.${p.number}`;
    sourceRecords.set(uid,p);
    if(metadata.records[uid]) assert.deepEqual(Array.from(ctx.topicFields(p.problem,p.category,uid).topics),metadata.records[uid].topics,uid);
  }
}
const batch=JSON.parse(fs.readFileSync('docs/topic-audit-unclassified-2026-10-02.json','utf8'));
assert.equal(Object.keys(batch.reviews).length,253);
for(const uid of Object.keys(batch.reviews)) assert.ok(!ctx.topicFields(sourceRecords.get(uid).problem,null,uid).topics.includes('Unclassified'),uid);
const greek=JSON.parse(fs.readFileSync('docs/topic-audit-greece-2026-10-02.json','utf8'));
assert.deepEqual(Object.keys(greek.reviews).sort(),Array.from(sourceRecords.keys()).filter(uid=>uid.startsWith('gr.')).sort());
const bmo=JSON.parse(fs.readFileSync('docs/topic-audit-bmo1-2026-10-02.json','utf8'));
assert.equal(Object.keys(bmo.reviews).length,132);
const bmo2=JSON.parse(fs.readFileSync('docs/topic-audit-bmo2-2026-10-02.json','utf8'));
assert.equal(Object.keys(bmo2.reviews).length,88);
assert.deepEqual(Object.keys(bmo2.reviews).sort(),Array.from(sourceRecords.keys()).filter(uid=>uid.startsWith('uk2.')).sort());
for(const [uid,expected] of [['uk2.2018.0.2',['Combinatorics','Number Theory']],['uk2.2019.0.2',['Combinatorics','Geometry','Number Theory']],['uk2.2017.0.4',['Combinatorics']]]) {
  assert.deepEqual(Array.from(ctx.topicFields(sourceRecords.get(uid).problem,null,uid).topics),expected,uid);
}
assert.deepEqual(Object.keys(bmo.reviews).sort(),Array.from(sourceRecords.keys()).filter(uid=>uid.startsWith('uk1.')).sort());
for(const [uid,expected] of [['uk1.2021.0.3',['Combinatorics','Geometry']],['uk1.2024.0.5',['Combinatorics']]]) {
  assert.deepEqual(Array.from(ctx.topicFields(sourceRecords.get(uid).problem,null,uid).topics),expected,uid);
}
assert.deepEqual(Array.from(ctx.topicFields(sourceRecords.get('ee.1999.0.2').problem,null,'ee.1999.0.2').topics),['Analysis']);
const actual=(file,year,number,day=0)=>{const d=JSON.parse(fs.readFileSync(file));return d.years.find(b=>b.year===year).problems.find(p=>p.number===number&&(p.day||0)===day).problem};
for(const [file,year,day,number,expected] of [
 ['Germany-mo-problems.json',2006,1,2,'Geometry'],
 ['Germany-mo-problems.json',2025,2,5,'Geometry'],
 ['Poland-pmo-problems.json',1997,1,3,'Geometry'],
 ['Portugal-opm-problems.json',2012,2,5,'Geometry'],
 ['Hungary-oktv-problems.json',2018,0,1,'Geometry'],
 ['Brazil-obm-problems.json',1982,0,5,'Geometry'],
 ['NewZealand-nzmo-problems.json',2020,0,1,'Algebra'],
 ['Australia-amo-problems.json',2020,1,4,'Algebra'],
 ['Russia-aro-problems.json',2018,1,2,'Algebra'],
 ['Russia-aro-problems.json',2006,1,1,'Algebra'],
 ['Greece-tst-problems.json',2013,1,3,'Algebra'],
 ['HongKong-tst-problems.json',2011,2,8,'Algebra']
]) assert.ok(ctx.classifyStatement(actual(file,year,number,day)).includes(expected),`${file} ${year}/${number} missing ${expected}`);
const record=metadata.records['au.2017.2.5'];
assert.equal(ctx.topicFields(record.reviewed_statement,null,'au.2017.2.5').topic,'Algebra');
assert.deepEqual(Array.from(ctx.topicFields('Find all primes p.',null,'au.2017.2.5').topics),['Number Theory']);
assert.equal(ctx.topicFields(record.reviewed_statement,'Geometry','au.2017.2.5').topic,'Geometry');
assert.ok(!ctx.classifyStatement('Find integers x,y with x^2+y^2=1.').includes('Geometry'));
assert.ok(!ctx.classifyStatement('A regular 14-gon has marked vertices.').includes('Number Theory'));
console.log(`Thematic checks passed: ${Object.keys(metadata.records).length} reviewed records, actual geometry/algebra omissions, stale overrides and category precedence.`);

const thousand=JSON.parse(fs.readFileSync('docs/topic-audit-batch1000-2026-10-02.json'));
assert.equal(Object.keys(thousand.reviews).length,1000);
assert.equal(thousand.new_distinct_reviews,1000);
for(const prefix of ['ukt.','nl.','nlt.','ch.']) for(const uid of sourceRecords.keys()) if(uid.startsWith(prefix)) assert.ok(metadata.records[uid],uid);
for(const [uid,expected] of [['ukt.2011.1.2',['Combinatorics']],['ch.2012.2.8',['Combinatorics']],['nl.2010.0.3',['Geometry','Number Theory']],['nlt.2018.1.2',['Geometry']]]) assert.deepEqual(Array.from(ctx.topicFields(sourceRecords.get(uid).problem,null,uid).topics),expected,uid);
