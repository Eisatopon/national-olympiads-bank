const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const html = fs.readFileSync('index.html', 'utf8');
new vm.Script(html.slice(html.indexOf('<script>\n(() => {') + 8, html.lastIndexOf('</script>')));
const nodes = new Map();
const $ = id => { if (!nodes.has(id)) nodes.set(id, {value:'', checked:true, innerHTML:'', textContent:'', disabled:false}); return nodes.get(id); };
const storage = new Map();
const context = { $, STORAGE_KEY:'test', localStorage:{getItem:k=>storage.get(k)||null,setItem:(k,v)=>storage.set(k,v)}, selected:['uk1.2025.0.1','huo.2025.0.1'],
  esc:s=>String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/"/g,'&quot;'),
  window:{prompt:()=>'<Geometry>',confirm:()=>true}, URL, URLSearchParams, Date, Math,
  location:{href:'https://example.com/bank/?old=1',search:''}, CBY:{uk1:{},huo:{}},
  byUid:new Map([['uk1.2025.0.1',{}],['huo.2025.0.1',{}]]),
  hydrate:async uids=>uids,changeSelection:fn=>fn() };
vm.createContext(context);
vm.runInContext(html.slice(html.indexOf('const COLLECTIONS_KEY'), html.indexOf('/* ---------- Print ---------- */')), context);
vm.runInContext(html.slice(html.indexOf('function shareUrl()'), html.indexOf('function openShare()')), context);
vm.runInContext(html.slice(html.indexOf('function parseIncoming()'), html.indexOf('async function hydrate(')), context);
(async()=>{
  $('#examTitle').value='Γεωμετρία & Algebra'; $('#solutionSpace').value='80'; $('#showSource').checked=false;
  context.saveCollection();
  assert.equal(context.readCollections().length,1);
  assert.match($('#savedSets').innerHTML,/&lt;Geometry>/);
  const url = new URL(context.shareUrl());
  assert.equal(url.searchParams.get('title'),'Γεωμετρία & Algebra');
  assert.equal(url.searchParams.get('space'),'80'); assert.equal(url.searchParams.get('sources'),'0');
  context.location.search=url.search;
  assert.deepEqual(Array.from(context.parseIncoming()),context.selected);
  context.location.search='?set=unknown.2025.0.1,uk1.2025.0.1';
  assert.deepEqual(Array.from(context.parseIncoming()),['uk1.2025.0.1']);
  context.selected=['different']; $('#examTitle').value='Different';
  await context.openCollection();
  assert.deepEqual(Array.from(context.selected),['uk1.2025.0.1','huo.2025.0.1']);
  assert.equal($('#examTitle').value,'Γεωμετρία & Algebra');
  context.byUid.clear(); await context.openCollection();
  assert.match($('#collectionStatus').textContent,/2 problems are unavailable/);
  assert.equal(context.readCollections()[0].uids.length,2);
  context.localStorage.setItem=()=>{throw Error('Full')}; context.saveCollection();
  assert.match($('#collectionStatus').textContent,/Could not save/);
  context.localStorage.setItem=(k,v)=>storage.set(k,v);
  context.deleteCollection(); assert.equal(context.readCollections().length,0);
  assert.equal(context.selected.length,2);
  storage.set('test:collections','bad JSON'); assert.equal(context.readCollections().length,0);
  console.log('Collection checks passed: storage, exact ordered share IDs, title/options, unavailable records, storage errors and deletion.');
})().catch(e=>{console.error(e);process.exitCode=1});
