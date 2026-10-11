const assert=require('node:assert/strict');
const fs=require('node:fs');
const v=JSON.parse(fs.readFileSync('metadata/undergraduate-import-contract.json','utf8'));
assert.equal(v.schema_version,1);
assert.equal(v.section,'undergraduate');
assert.deepEqual(v.collections.map(c=>[c.id,c.first_year]),[['imc',1994],['put',1938],['seemous',2007],['vjimc',1991],['smmc',2017]]);
assert.equal(new Set(v.collections.map(c=>c.file)).size,5);
const catalog=JSON.parse(fs.readFileSync('metadata/undergraduate-competitions.json','utf8'));
assert.deepEqual(v.collections.map(c=>c.id),catalog.records.map(c=>c.id).sort((a,b)=>['imc','put','seemous','vjimc','smmc'].indexOf(a)-['imc','put','seemous','vjimc','smmc'].indexOf(b)));
for(const c of v.collections){
 assert.ok(c.file.endsWith('-problems.json'));
 assert.ok(c.first_year<=c.last_archived_year);
 assert.ok(fs.existsSync(c.source_registry));
 assert.ok(!fs.existsSync(c.file),'Must not create a fake empty collection '+c.file);
}
assert.ok(v.required_problem_fields.includes('problem'));
assert.ok(v.required_problem_fields.includes('topics'));
assert.ok(v.required_problem_fields.includes('problem_dna'));
assert.equal(v.state,'specification_only_no_statement_import');
console.log('Five full-text Undergraduate targets, correct historical starts and stable source metadata validated.');
