const assert=require('node:assert/strict');
const fs=require('node:fs');
const manifest=JSON.parse(fs.readFileSync('metadata/vojtech-jarnik-editions-source-manifest.json','utf8'));
const years=[...Array.from({length:29},(_,i)=>1991+i),2022,2024,2025,2026];
assert.deepEqual(manifest.editions.map(e=>e.year),years,'Historical years must come from official edition record');
assert.deepEqual(manifest.editions.map(e=>e.edition),Array.from({length:33},(_,i)=>i+1));
assert.equal(manifest.editions.at(-1).edition,33);
const y1991=JSON.parse(fs.readFileSync('undergraduate/Vojtech-Jarnik-1991-source-review.json','utf8'));
assert.equal(y1991.year,1991);
assert.equal(y1991.category_I_complete,true);
assert.equal(y1991.category_II_original_not_found,true);
assert.equal(y1991.public_full_competition_eligible,false);
assert.deepEqual(y1991.problems.map(p=>p.number),[1,2,3,4]);
assert.ok(y1991.problems.every(p=>p.category==='I'&&p.source_page===1&&p.source_verified===true));
assert.ok(y1991.problems.every(p=>(p.problem.match(/\$/g)||[]).length%2===0));
for(const year of [1992,1993]){
 const j=JSON.parse(fs.readFileSync('undergraduate/Vojtech-Jarnik-'+year+'-source-review.json','utf8'));
 assert.equal(j.year,year);
 assert.equal(j.problems.length,4);
 assert.deepEqual(j.problems.map(p=>p.number),[1,2,3,4]);
 assert.ok(j.problems.every(p=>p.category==='II'&&p.source_verified===false&&p.review_flags.includes('visual_comparison_of_original_pdf_required')));
 assert.equal(j.public_full_competition_eligible,false);
 for(const p of j.problems) assert.equal((p.problem.match(/\$/g)||[]).length%2,0,'Unbalanced math '+year+'/'+p.number);
}
console.log('VJIMC historical editions and 1991 original Category I source staging verified.');
