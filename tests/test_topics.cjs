const fs=require('fs'),vm=require('vm'),assert=require('node:assert/strict');
const html=fs.readFileSync('index.html','utf8');
const metadata=JSON.parse(fs.readFileSync('metadata/topic-overrides.json','utf8'));
const ctx={topicOverrides:metadata.records};vm.createContext(ctx);
vm.runInContext(html.slice(html.indexOf('function classifyStatement('),html.indexOf('function normalizeYears(')),ctx);
for(const [uid,r] of Object.entries(metadata.records)) assert.deepEqual(Array.from(ctx.topicFields(r.reviewed_statement,null,uid).topics),r.topics,uid);
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
