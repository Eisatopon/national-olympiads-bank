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
 if(c.id==='seemous'){
   const imported='undergraduate/SEEMOUS-2007-2010-problems.json';
   assert.ok(fs.existsSync(imported),'SEEMOUS imported archive is missing');
   const data=JSON.parse(fs.readFileSync(imported,'utf8'));
   assert.ok(data.competition && Array.isArray(data.years));
   assert.deepEqual(data.years.map(y=>y.year),Array.from({length:20},(_,i)=>2007+i));
   assert.ok(data.years.every(y=>y.problems.length===4&&y.problems.every((p,i)=>p.number===i+1&&typeof p.problem==='string'&&p.problem.trim())));
   // SEEMOUS was incrementally imported through 2026 despite its historical filename.
   // Guard all imported full statements against accidental truncation and broken TeX.
   const problems=data.years.flatMap(y=>y.problems.map(p=>({year:y.year,...p})));
   assert.equal(problems.length,80,'SEEMOUS 2007-2026 must contain 80 problems');
   assert.equal(problems.filter(p=>p.statement_verified).length,8,'SEEMOUS original-source review count changed unexpectedly');
   for(const p of problems){
     const id=`${p.year}:${p.number}`;
     if (p.year===2024 || p.year===2026){
       const official = p.year===2024
         ? 'https://math.etti.tuiasi.ro/seemous2024/wp-content/SEEMOUS_2024_Contest_Problems.pdf'
         : 'https://cdn.b3web.xyz/web/cms/optimizedSEEMOUS_2026_Contest.pdf1772877068.pdf';
       assert.equal(p.statement_verified,true,'Original paper check missing '+id);
       assert.equal(p.verification_source,official,'Wrong original contest paper '+id);
       assert.equal(p.verification_page,1,'Wrong original contest page '+id);
       assert.ok(p.verification_method && p.verified_on && p.review_flags.length===0,'Missing provenance '+id);
     }else{
       assert.equal(p.statement_verified,false,'Unverified original marked verified '+id);
       assert.ok(p.review_flags.includes('original_official_paper_statement_visual_comparison_pending'),'Missing pending review flag '+id);
     }
   }

   assert.equal(new Set(problems.map(p=>`${p.year}:${p.number}`)).size,80,'Duplicate SEEMOUS IDs');
   for(const p of problems){
     const id=`${p.year}:${p.number}`;
     assert.ok(p.problem.trim().length>=35,'Suspiciously short SEEMOUS statement '+id);
     assert.equal((p.problem.match(/\$/g)||[]).length%2,0,'Unbalanced inline TeX '+id);
     assert.ok(!/\[(MATH|FIGURE)_REQUIRES_REVIEW\]/.test(p.problem),'Unresolved problem placeholder '+id);
   }

 }else{
   assert.ok(!fs.existsSync(c.file),'Must not create a fake empty collection '+c.file);
 }
}
assert.ok(v.required_problem_fields.includes('problem'));
assert.ok(v.required_problem_fields.includes('topics'));
assert.ok(v.required_problem_fields.includes('problem_dna'));
assert.equal(v.state,'specification_only_no_statement_import');
console.log('Five full-text Undergraduate targets, correct historical starts and stable source metadata validated.');
