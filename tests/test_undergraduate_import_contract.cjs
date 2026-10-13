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
   assert.equal(problems.filter(p=>p.statement_verified).length,80,'SEEMOUS source-review count changed unexpectedly');
   const geometry2012 = problems.find(p=>p.year===2012&&p.number===2);
   assert.equal(geometry2012.statement_verified,true,'SEEMOUS 2012/2 source review incomplete');
   assert.equal(geometry2012.figure_asset,'images/seemous_2012_p2_fig.png');
   assert.ok(geometry2012.problem.endsWith('/images/seemous_2012_p2_fig.png'),'SEEMOUS 2012/2 missing source figure');
   assert.ok(geometry2012.figure_provenance.includes('cropped'),'Figure provenance must say it is a crop of the source');
   assert.ok(fs.existsSync(geometry2012.figure_asset),'Missing SEEMOUS 2012/2 figure');
   const p2021_4=problems.find(p=>p.year===2021&&p.number===4);
   assert.ok(p2021_4.problem.includes('|\\sin(\\pi x)|^x'),'SEEMOUS 2021/4 integrand exponent must match original');
   assert.ok(!p2021_4.problem.includes('\\sin(\\pi x)/x'),'SEEMOUS 2021/4 incorrect quotient prohibited');
   const p2025_2 = problems.find(p=>p.year===2025&&p.number===2);
   assert.ok(p2025_2.problem.includes('\\sqrt[n]{e^x-1-\\frac{x}{1!}'), '2025/2 must preserve original radical expression');
   assert.ok(!p2025_2.problem.includes('\\frac{e^x-1-'), '2025/2 spurious radical denominator reintroduced');

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
     }else if (p.year===2018){
       assert.equal(p.verification_source,'https://math.etti.tuiasi.ro/seemous2018/wp-content/uploads/2018/03/SEEMOUS-2018-Contest-Problems.pdf','Wrong original contest paper '+id);
       assert.ok(p.statement_verified&&p.verification_page===1&&p.review_flags.length===0,'Missing provenance '+id);
     }else if ([2007,2008,2009,2010,2011,2019].includes(p.year)) {
       assert.equal(p.statement_verified,true,'Compiled contest paper comparison missing '+id);
       assert.ok(p.verification_source === 'User-supplied Seemous-2007-2025.pdf' || (p.year===2009 && p.verification_source==='https://matematickitalent.mk/uploads/books/3nibFWGcTEi5Os97mSQ7sQ.pdf' || p.year===2010 && p.verification_source==='https://ssmr.ro/gazeta/gma/2010/gma1-2-2010-continut.pdf'),'Missing contest compilation provenance '+id);
       assert.ok(p.verification_page>0&&p.review_flags.length===0,'Incomplete reviewed page metadata '+id);
     }else if (p.year>=2012 && p.year<=2017){
       assert.equal(p.statement_verified,true,'SEEMOUS 2012-2017 source review missing '+id);
       assert.ok(p.verification_source && p.verification_page>=1 && p.review_flags.length===0,'Incomplete SEEMOUS 2012-2017 provenance '+id);
     }else if (p.year>=2020 && p.year<=2025){
       assert.equal(p.statement_verified,true,'SEEMOUS 2020-2025 source review missing '+id);
       assert.ok(p.verification_source&&p.verification_page>=1&&p.review_flags.length===0,'Source metadata incomplete '+id);
     }else{
       assert.equal(p.statement_verified,false,'Unverified original marked verified '+id);
       assert.ok(p.review_flags.includes('original_official_paper_statement_visual_comparison_pending'),'Missing pending review flag '+id);
       if (p.year===2012&&p.number===2) throw new Error('2012/2 diagram cannot remain pending');
     }
   }

   assert.equal(new Set(problems.map(p=>`${p.year}:${p.number}`)).size,80,'Duplicate SEEMOUS IDs');
   for(const p of problems){
     const id=`${p.year}:${p.number}`;
     assert.ok(p.problem.trim().length>=35,'Suspiciously short SEEMOUS statement '+id);
     assert.equal((p.problem.match(/\$/g)||[]).length%2,0,'Unbalanced inline TeX '+id);
     assert.ok(!/\[(MATH|FIGURE)_REQUIRES_REVIEW\]/.test(p.problem),'Unresolved problem placeholder '+id);
   }

 }else if(c.id==='put'){
   const imported=JSON.parse(fs.readFileSync(c.file,'utf8'));
   assert.equal(imported.problem_count,1063);
   assert.equal(imported.years.length,85);
   assert.equal(imported.years.flatMap(y=>y.problems).filter(p=>p.statement_verified).length,732);
   assert.ok(imported.years.filter(y=>y.year>=1965 && y.year<1985).every(y=>y.problems.every(p=>p.statement_verified&&p.category)));
 }else if(c.id==='vjimc'){
   const imported=JSON.parse(fs.readFileSync(c.file,'utf8'));
   assert.equal(imported.problem_count,261);
   assert.equal(imported.years.length,33);
   assert.ok(imported.years.every(y=>y.problems.every(p=>!p.statement_asset && p.paper && p.statement_verified && p.text_transcription_verified)));
 }else if(c.id==='smmc'){
   const imported=JSON.parse(fs.readFileSync(c.file,'utf8'));
   assert.equal(imported.problem_count,88);
   assert.equal(imported.years.length,9);
   assert.ok(imported.years.every(y=>y.problems.every(p=>p.statement_verified&&p.text_transcription_verified&&!p.statement_asset&&p.paper)));
 }else{
   assert.ok(!fs.existsSync(c.file),'Must not create a fake empty collection '+c.file);
 }
}
assert.ok(v.required_problem_fields.includes('problem'));
assert.ok(v.required_problem_fields.includes('topics'));
assert.ok(v.required_problem_fields.includes('problem_dna'));
assert.equal(v.state,'partial_import_vjimc_smmc_and_putnam_published');
console.log('Five full-text Undergraduate targets, correct historical starts and stable source metadata validated.');
