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
