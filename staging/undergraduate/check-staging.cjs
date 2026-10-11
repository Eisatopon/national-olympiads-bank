#!/usr/bin/env node
'use strict';
const fs=require('node:fs');const assert=require('node:assert/strict');
const base='staging/undergraduate/';
const cfg=JSON.parse(fs.readFileSync('metadata/undergraduate-import-contract.json','utf8'));
let total=0;
for(const target of cfg.collections){
 const file=base+target.id+'-coverage.json';
 const d=JSON.parse(fs.readFileSync(file,'utf8'));
 assert.equal(d.schema_version,1);
 assert.equal(d.collection_id,target.id);
 assert.equal(d.competition,target.competition);
 assert.equal(d.public_bank_integrated,false);
 assert.equal(d.full_text_available,false);
 assert.equal(d.events[0].year,target.first_year);
 assert.equal(d.events[d.events.length-1].year,target.last_archived_year);
 assert.deepEqual(d.required_fields,cfg.required_problem_fields);
 const expected=target.last_archived_year-target.first_year+1-(target.id==='put'?3:0);
 assert.equal(d.events.length,expected);
 const seen=new Set();
 for(const event of d.events){
  assert.ok(!seen.has(event.year),'Duplicate edition year '+event.year);
  seen.add(event.year);
  assert.ok(Array.isArray(event.sources));
  for(const s of event.sources){assert.match(s.url,/^https:\/\//);assert.ok(s.kind);}
  assert.equal(event.problem_records_imported,0,'Do not mislabel sources as complete problems');
  assert.equal(event.transcription_status,'not_transcribed');
  assert.equal(event.taxonomy_status,'not_started');
 }
 if(target.id==='put'){
  for(const missing of [1943,1944,1945])assert.ok(!seen.has(missing));
  assert.ok(d.events.find(e=>e.year===1958).edition_notes.includes('Two distinct'));
 }
 total+=d.events.length;
}
assert.equal(total,183);
console.log('Unpublished five-competition staging integrity passed:',total,'calendar-year slots (not verified statement records).');

let stagedStatementCount=0;
for(const target of cfg.collections){
 const draft=JSON.parse(fs.readFileSync(base+target.file,'utf8'));
 assert.equal(draft.collection_id,target.id);
 assert.equal(draft.publication_state,'unpublished_work_branch_only');
 assert.equal(draft.years.length,target.last_archived_year-target.first_year+1-(target.id==='put'?3:0));
 for(const year of draft.years){
   if(target.id==='put'&&year.year>=1985&&year.year<=2000){
     assert.equal(year.problems.length,12,'Must preserve all 12 Putnam source statements for '+year.year);
     assert.deepEqual(year.problems.map(p=>p.number),['A1','A2','A3','A4','A5','A6','B1','B2','B3','B4','B5','B6']);
     for(const problem of year.problems){
       assert.ok(problem.problem.length>=35);
       assert.deepEqual(problem.topics,[]);
       assert.deepEqual(problem.problem_dna,[]);
       assert.equal(problem.statement_verified,false);
       assert.ok(!Object.hasOwn(problem,'solution'));
       assert.ok(problem.source_url.startsWith('https://github.com/rpxgit/The-Putnam-Archive/'));
     }
   }else{
     if(target.id!=='put'&&(target.id==='imc'?[2023,2024,2025,2026].includes(year.year):year.year===({seemous:2024,vjimc:2025,smmc:2025})[target.id])){
       const expectedCount=target.id==='imc'?10:1;
       assert.equal(year.problems.length,expectedCount,'Must have all verified independently reworded records');
       for(const p of year.problems){
         assert.equal(p.statement_form,'independently_reworded_equivalent_not_verbatim');
         assert.equal(p.statement_verified,true);
         assert.ok(p.problem.length>=50);
         assert.ok(Array.isArray(p.topics)&&p.topics.length>0);
         assert.ok(Array.isArray(p.problem_dna)&&p.problem_dna.length>0);
         assert.ok(p.source_url.startsWith('https://'));
         assert.equal(p.taxonomy_status,'provisional');
         assert.ok(!Object.hasOwn(p,'solution'));
       }
       if(target.id==='imc'){
         assert.deepEqual(year.problems.map(p=>p.number),[1,2,3,4,5,6,7,8,9,10]);
         assert.deepEqual(year.problems.map(p=>p.day),[1,1,1,1,1,2,2,2,2,2]);
       }
     }else{
       assert.equal(year.problems.length,0,'Do not fabricate a year of problems');
     }
   }
   stagedStatementCount+=year.problems.length;
 }
}
assert.equal(stagedStatementCount,235);
console.log('All five standalone staged JSON files valid; 192 Putnam transcriptions and 23 independently worded source-checked mathematical statements; classification incomplete.');

const first=JSON.parse(fs.readFileSync(base+'put-1938-exam-index.json','utf8'));
assert.equal(first.year,1938);
assert.equal(first.total_numbered_questions,13);
assert.deepEqual(first.problem_index.map(p=>p.number),Array.from({length:13},(_,i)=>i+1));
assert.deepEqual(first.problem_index.filter(p=>p.session==='morning').map(p=>p.number),[1,2,3,4,5,6,7]);
assert.deepEqual(first.problem_index.filter(p=>p.session==='afternoon').map(p=>p.number),[8,9,10,11,12,13]);
assert.deepEqual(first.problem_index.filter(p=>p.alternatives).map(p=>p.number),[7,8]);
assert.ok(first.status.includes('NOT_IMPORTED'));
console.log('Putnam 1938 numbering/index source cross-reference validated; full-text statements remain unimported.');
