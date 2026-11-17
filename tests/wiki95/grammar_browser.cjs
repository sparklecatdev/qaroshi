/* Real source-licensed browser grammar tests, no npm dependencies.
 * Run node tests/wiki95/grammar_browser.cjs.
 */
'use strict';
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const path=require('node:path'),root=path.resolve(__dirname,'../..');
const spec=JSON.parse(fs.readFileSync(path.join(root,'data/standard_9_3/grammar_licenses.json'),'utf8'));
const frames=JSON.parse(fs.readFileSync(path.join(root,'data/semantics/valency_frames.json'),'utf8'));
const browser={};vm.runInNewContext(fs.readFileSync(path.join(root,'web/grammar_live.js'),'utf8'),{window:browser});
const grammar=browser.QaroshiGrammar.createGrammar(spec,frames);
assert.equal(frames.length,25);
let checks=0,roundtrips=0;
const same=(a,b)=>assert.equal(JSON.stringify(a),JSON.stringify(b));
const event=(verb,offset=0)=>{
  const choose=role=>grammar.candidateNouns(verb,role)[offset%Math.max(1,grammar.candidateNouns(verb,role).length)]?.form||null;
  return grammar.atom({actor:choose('subject'),verb,patient:choose('patient'),
    recipient:choose('recipient'),tense:'te'});
};
const round=(s)=>{
  const q=grammar.render(s),p=grammar.parse(q);
  assert.equal(grammar.render(p),q);
  same(grammar.meaning(s),grammar.meaning(p));
  roundtrips++;return q;
};
for(const verb of Object.keys(spec.verb_overrides)){
  for(const person of [0,1,2]){
    const a=event(verb,person);
    for(const tense of ['','te','yu'])
      for(const modal of ['','ki','ho','du'])
        for(const neg of [false,true]){
          const atom=grammar.atom({...a,tense,modal,negated:neg});
          for(const mood of ['statement','polar']){
            const s={proposition:atom,resonance:mood==='polar'?'hë':'sen',mood,attribution:'',evidential:''};
            round(s);checks++;
          }
        }
  }
}
const A=event('tika'),B=event('këmë');
for(const relation of ['after','before','when','if','counterfactual']){
  for(const att of ['','reported_to_speaker','unknown_whether']){
    const s={proposition:{type:'link',relation,first:A,second:B},
      resonance:'sen',mood:'statement',attribution:att,evidential:''};
    const q=round(s);
    const meaning=grammar.meaning(s);
    assert.equal(meaning.relation,relation);
    if(att)assert.equal(meaning.matrix_event_asserted,false);
    if(relation==='counterfactual')assert(q.includes(' qinë'));
    checks++;
  }
}
for(const resonance of spec.allowed_resonances)round({proposition:A,resonance,mood:'polar',attribution:'',evidential:''});
assert.equal(grammar.render({proposition:grammar.atom({actor:'mi',verb:'pëli',patient:'kima',recipient:'mara',tense:'te'}),
  resonance:'sen',mood:'statement',attribution:'',evidential:''}), 'sen mi mara-tu kima-m pëli-te.');
const invalid=[
  'sen mi mara-tu kima-m pëli-ki-te.','sen mi kima-m pëli-te.',
  'sen mi kima-m mara-tu pëli-te.','sen kima ti-m tika-te.',
  'sen mi kima-m shëma-te.','sen mi mara-m tika-te-te.',
  'sen mi mara-m tika-li-te.',
  'sen mi mara-m tika-te do yano mi-tu shiri-te ye.',
  'sen mi mara-m tika-yu-te.','sen mi mara-m mara-m tika-te.',
  'sen mi mara-m nope-te.','mi mara-m tika-te.'
];
for(const q of invalid){assert.throws(()=>grammar.parse(q),undefined,'Should reject '+q);checks++;}
assert.throws(()=>grammar.render({resonance:'sen',mood:'statement',
  proposition:grammar.atom({actor:'mi',verb:'pëli',patient:'mara',recipient:'kima'})}));
assert.equal(grammar.parse('hë mi mara-m tika-te.').mood,'statement');checks++;
assert.equal(grammar.parse('sen mi mara-m tika-te he?').mood,'polar');checks++;
assert.equal(grammar.parse('hë mi mara-m tika-te he?').mood,'polar');checks++;
for(const extra of [
  grammar.atom({actor:'mi',verb:'gura',goal:'naro',source:'naro',location:'naro',tense:'te'}),
  grammar.atom({actor:'mara',verb:'rawo',comitative:'ti',location:'naro',tense:'yu'}),
])round({resonance:'sen',mood:'statement',proposition:extra,attribution:'',evidential:''});
assert(roundtrips>=3500,roundtrips);
console.log('PASS',roundtrips,'browser parser/composer roundtrips,',checks,'assertion groups');
