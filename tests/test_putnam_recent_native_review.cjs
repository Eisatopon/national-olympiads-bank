const assert=require('node:assert/strict'),fs=require('node:fs'),crypto=require('node:crypto');
const read=p=>JSON.parse(fs.readFileSync(p,'utf8'));
const sha=t=>crypto.createHash('sha256').update(t).digest('hex');
const source=read('research/putnam/Putnam-1985-2025-statement-sources.json');
const checked=read('research/putnam/Putnam-1985-2025-source-checked-review.json');
const raw=read('undergraduate/Putnam-1985-2025-review.json');
const published=read('undergraduate/Putnam-problems.json');
const meta=read('metadata/putnam-statement-checks.json').collections['undergraduate/Putnam-problems.json'];
assert.equal(source.statement_count,492);assert.equal(source.solutions_imported,false);
assert.equal(source.source_files.length,82);assert.equal(source.additional_university_pdfs.length,26);
assert.equal(checked.problem_count,492);assert.equal(checked.original_examination_scan_comparison_complete,false);
assert.equal(checked.source_snapshot_sha256,sha(fs.readFileSync('research/putnam/Putnam-1985-2025-statement-sources.json')));
assert.deepEqual(checked.years.map(y=>y.year),Array.from({length:41},(_,i)=>1985+i));
const src=new Map(source.statements.map(p=>[`${p.year}.${p.number}`,p]));
let figures=0;
for(const y of checked.years){
 assert.deepEqual(y.problems.map(p=>p.number),['A','B'].flatMap(s=>[1,2,3,4,5,6].map(n=>s+n)));
 assert.deepEqual(published.years.find(z=>z.year===y.year),y);
 for(const p of y.problems){
  const id=`${y.year}.${p.number}`,uid=`put.${y.year}.0.${p.number}`;
  const s=src.get(id);assert.equal(sha(s.source_statement_tex),s.source_statement_sha256);
  assert.equal(p.source_input_statement_sha256,s.source_statement_sha256);
  assert.equal(p.statement_sha256,sha(p.problem));assert.equal(p.statement_verified,true);
  assert.equal(p.original_wording_verified,false);assert.ok(!p.solution);assert.deepEqual(p.review_flags,[]);
  assert.equal(meta.statement_checks[uid].status,'statement_checked_against_archive_tex');
  assert.equal(meta.statement_checks[uid].reviewed_statement,p.problem);
  const old=raw.years.find(z=>z.year===y.year).problems.find(z=>z.number===p.number);
  assert.equal(p.pre_review_statement_sha256,sha(old.problem));assert.equal(old.statement_verified,false);
  assert.equal(p.problem.split('$').length%2,1,id);
  const outside=p.problem.replace(/\$\$[\s\S]*?\$\$|\$[^$]*?\$/g,'');
  assert.ok(!/\\[A-Za-z]+/.test(outside),`${id}: unrendered TeX`);
  assert.ok(!/\[(?:Figure|Picture|Diagram).*?(?:omitted|requires|not included)/i.test(p.problem),id);
  for(const f of p.figures??[]){
   assert.equal(f.content,'diagram_only');assert.equal(f.sha256,sha(fs.readFileSync(f.src)));
   assert.ok(p.problem.includes(f.src));figures++;
  }
 }
}
assert.equal(figures,6);
const get=(y,n)=>checked.years.find(z=>z.year===y).problems.find(p=>p.number===n);
assert.ok(get(1992,'B6').problem.includes('at most $n^2$ matrices'));
assert.ok(get(1985,'A3').problem.includes('$$\n\\begin{aligned}'));
assert.ok(get(1985,'A6').problem.includes('\\Gamma(F(x)^n)'));
assert.ok(get(1990,'A6').problem.includes('let $|X|$ denote'));
assert.ok(get(1990,'B6').problem.includes('parallel to $K$'));
assert.ok(!get(1990,'B6').problem.includes('$K_1$'));
assert.ok(get(2007,'A6').problem.includes('each side of $P$'));
assert.ok(get(2013,'A6').problem.includes('0&2&-4&12&-4&2'));
assert.ok(get(2013,'A6').problem.includes('a\\backslash b&-2&-1&0&1&2'));
assert.ok(!get(2013,'A6').problem.includes('tabular'));
assert.ok(!get(2020,'A6').problem.includes('footnote'));
console.log('All 492 recent cards: complete source snapshots, faithful identity, native mathematics, restored conclusion, numeric table, six diagrams, and honest archive-check scope validated.');

const historicalGet=(y,n)=>published.years.find(z=>z.year===y).problems.find(p=>p.number===n);
assert.ok(historicalGet(1978,'A5').problem.includes('\\leq'));
assert.ok(historicalGet(1978,'B3').problem.includes('m\\geq1'));
assert.ok(historicalGet(1979,'B6').problem.includes('r\\leq'));
for(const [y,n] of [[1978,'A5'],[1978,'B3'],[1979,'B6']]){
 assert.equal(historicalGet(y,n).original_wording_verified,false);
 assert.ok(historicalGet(y,n).pre_editorial_statement_sha256);
}
