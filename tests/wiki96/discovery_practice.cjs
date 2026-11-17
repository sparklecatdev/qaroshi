'use strict';
/* Pure Node parity checks for the Wiki 9.6 ranking and offline practice code. */
const assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm'),path=require('node:path');
const ROOT=path.resolve(__dirname,'../..'),window={};
for(const name of ['wiki_discovery.js','wiki_practice.js'])
  vm.runInNewContext(fs.readFileSync(path.join(ROOT,'web',name),'utf8'),{window});
const sample=[
  {id:'Q1',qaroshi:'kima',english:'water',domain:'nature',pos:'n',components:'',note:''},
  {id:'Q2',qaroshi:'kima-shima',english:'water book',domain:'nature',pos:'n',components:'kima + shima',note:''},
  {id:'Q3',qaroshi:'shima',english:'book',domain:'writing',pos:'n',components:'',note:''},
  {id:'Q4',qaroshi:'pëli',english:'give water',domain:'social',pos:'v',components:'',note:''},
  {id:'Q5',qaroshi:'kirë',english:'water',domain:'nature',pos:'n',components:'',note:'related by English gloss only'},
  {id:'Q6',qaroshi:'kimasuru',english:'water source',domain:'nature',pos:'n',components:'',note:''},
  {id:'Q7',qaroshi:'raro',english:'door',domain:'everyday',pos:'n',components:'',note:''},
];
const d=window.QaroshiDiscovery.createIndex(sample);
assert.equal(d.size,7);
assert.equal(d.find('kima').results[0].qaroshi,'kima');
assert.equal(d.find('water').results[0].qaroshi,'kima');
assert.equal(d.find('WATER').results[0].qaroshi,'kima');
assert.equal(d.find('peli').results[0].qaroshi,'pëli');
assert.equal(d.find('water book').results[0].qaroshi,'kima-shima');
assert.equal(d.find('water book').total,1);
assert.equal(d.find('water',{domain:'nature'}).results.every(x=>x.domain==='nature'),true);
assert.equal(d.find('water',{pos:'v'}).results[0].qaroshi,'pëli');
assert.equal(d.find('quartz').total,0);
assert.equal(d.find('kima',{limit:1}).results.length,1);
assert.equal(d.find('').total,7);
assert.equal(d.find('source water').results[0].qaroshi,'kimasuru');
const graph=d.related('kima');
assert.equal(graph.compoundTotal,1);
assert.equal(graph.compounds[0].qaroshi,'kima-shima');
assert.equal(graph.parts.length,0);
assert.equal(graph.sameGloss.length,1);
assert.equal(graph.sameGloss[0].qaroshi,'kirë');
assert.equal(graph.unsupportedAntonyms,true);
assert.equal(d.related('kima-shima').parts.length,2);
assert.equal(d.related('kima-shima').parts[0].entry.qaroshi,'kima');
assert.equal(d.related('kima-shima').parts[1].entry.qaroshi,'shima');
assert.equal(d.related('absent').compounds.length,0);
assert.equal(d.related('absent').unsupportedAntonyms,true);
const p=window.QaroshiPractice;
const first=p.createDeck(sample,{word:'kima',limit:4,seed:123});
assert.equal(first[0].qaroshi,'kima');
assert.equal(first.length,4);
assert.equal(new Set(first.map(x=>x.qaroshi)).size,4);
assert.equal(JSON.stringify(p.createDeck(sample,{limit:5,seed:3})),JSON.stringify(p.createDeck(sample,{limit:5,seed:3})));
assert.equal(p.createDeck(sample,{limit:5,seed:4}).length,5);
assert.equal(p.createDeck(sample,{domain:'nature',limit:10}).every(x=>x.domain==='nature'),true);
assert.equal(p.createDeck(sample,{domain:'nothing'}).length,0);
assert.equal(p.createDeck(sample,{limit:0}).length,0);
console.log('PASS Wiki 9.6 dictionary ranking, exact component graphs, non-synonym labeling, deterministic offline cards');
