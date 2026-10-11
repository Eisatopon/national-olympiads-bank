#!/usr/bin/env node
'use strict';
// Quality gate for independently supplied, approved-for-publication Putnam exam transcriptions.
// Does NOT download or reproduce copyrighted problems.
const fs=require('node:fs');
const assert=require('node:assert/strict');
const path=require('node:path');
const registryPath=path.resolve('metadata/undergraduate-official-papers.json');
function verify(input, sources) {
  assert.equal(input.competition,'William Lowell Putnam Mathematical Competition');
  assert.ok(Array.isArray(input.years)&&input.years.length>0,'At least one exam year required');
  const seenYears=new Set();
  for(const exam of input.years){
    assert.ok(Number.isInteger(exam.year)&&exam.year>=1938,'Year required');
    assert.ok(!seenYears.has(exam.year),'Duplicate exam year '+exam.year);
    seenYears.add(exam.year);
    const source=sources.find(x=>x.competition_id==='put'&&x.year===exam.year);
    assert.ok(source&&source.questions_pdf&&source.questions_pdf.startsWith('https://maa.org/'),'Missing official MAA original for '+exam.year);
    assert.ok(Array.isArray(exam.problems)&&exam.problems.length===12,'Must have all 12 problems: '+exam.year);
    const ids=new Set();
    for(const p of exam.problems){
      assert.ok(/^[AB][1-6]$/.test(p.number),'Invalid Putnam problem identifier');
      assert.ok(!ids.has(p.number),'Repeated problem '+p.number);
      ids.add(p.number);
      assert.equal(typeof p.problem,'string');
      assert.ok(p.problem.trim().length>=30,'Empty, placeholder or incomplete text: '+p.number);
      assert.ok(!/^(source|pdf|todo|tbd|see (the )?(link|pdf|original)|pending)/i.test(p.problem.trim()),'Source-only placeholder: '+p.number);
      assert.ok(!Object.prototype.hasOwnProperty.call(p,'solution'),'Solutions not allowed');
    }
    for(const session of ['A','B'])for(let n=1;n<=6;n++)assert.ok(ids.has(session+n),'Missing '+session+n);
    assert.equal(exam.primary_source_url,source.questions_pdf,'Must cite exact official original');
    assert.equal(exam.statement_reviewed_against_original,true,'Requires recorded statement-level review');
    assert.equal(exam.publication_authorized,true,'Requires documented legal publication clearance');
    assert.equal(typeof exam.authorization_reference,'string');
    assert.ok(exam.authorization_reference.trim().length>4,'Missing permission evidence');
  }
  return {years:input.years.length,problems:input.years.length*12};
}
if(require.main===module){
  try{
    const filepath=process.argv[2];
    assert.ok(filepath,'Usage: node scripts/verify_putnam_import.cjs path/to/Putnam-problems.json');
    const source=JSON.parse(fs.readFileSync(registryPath,'utf8')).competitions;
    const result=verify(JSON.parse(fs.readFileSync(filepath,'utf8')),source);
    console.log('Putnam publication quality gate PASSED:',JSON.stringify(result));
  }catch(err){console.error('Putnam import BLOCKED:',err.message);process.exitCode=1;}
}
module.exports={verify};
