'use strict';
/* Offline, source-accurate word-usage contract.
 * Run node tests/wiki97/usage_guides.cjs (no packages).
 */
const assert=require('node:assert/strict');
const fs=require('node:fs'),vm=require('node:vm'),path=require('node:path');
const root=path.resolve(__dirname,'../..');
const window={};
vm.runInNewContext(fs.readFileSync(path.join(root,'web/wiki_usage.js'),'utf8'),{window});
const u=window.QaroshiUsage;
const mk=(qaroshi,pos='n',english='something',more={})=>({
  id:'Q-'+qaroshi,qaroshi,pos,english,domain:'test',components:'',note:'',...more
});
const words=[
  mk('mara','n','friend'),mk('mara-suri','n','friend book',{components:'mara + suri'}),
  mk('suri','n','book'),mk('goro','v','fly'),mk('lësha','adj','cute'),
  mk('ti','pron','you'),mk('sen','register','neutral'),
  mk('bëlaro','part','viewpoint'),mk('dasha','conj','even if'),
  mk('nëna','adv','now'),mk('gëwëmi','post','except for'),
  mk('dëna','det','this'),mk('he','qword','question'),
  mk('zha','register','enthusiasm'),mk('kima','n','water'),
];
const byWord=new Map(words.map(w=>[w.qaroshi,w]));
const data={
  affixes:[{form:'-m',category:'case',meaning:'object'},{form:'-te',category:'tense',meaning:'past'},
    {form:'-ri',category:'nominal',meaning:'plural'},{form:'-lë',category:'derivation',meaning:'affection'}],
  resonances:[{marker:'sen',name:'Still Voice',meaning:'neutral information'},
    {marker:'zha',name:'Bright Trill',meaning:'excitement'}],
  pronouns:[{form:'ti',english:'you (singular)'}],
  grammaticalParticles:[{form:'bëlaro',pos:'part',rule:'After resonance; report is not belief.'}],
  grammarFrames:[{lemma:'goro',frame:'V0',definition:'fly through the air',
    selection_note:'airborne motion, not permission',required_roles:['subject:flyer'],licensed_optional_roles:[]}],
};
const sentences=[
  {id:'P1',qaroshi:'sen mi mara-m tika-te.',english:'I protected a friend.'},
  {id:'P2',qaroshi:'sen mi mara-suri-m tika-te.',english:'I protected a friend book.'},
  {id:'P3',qaroshi:'zha mi mara-lë-ri-m tika-te.',english:'I protected dear friends.'},
  {id:'P4',qaroshi:'sen mi goro-te.',english:'I flew.'},
  {id:'P5',qaroshi:'sen mi suri-m tika-te.',english:'I protected a book.'},
  {id:'P6',qaroshi:'sen ti lësha.',english:'You are cute.'},
  {id:'P7',qaroshi:'sen mi mara-nonlexical tika-te.',english:'Noise is not a known inflection.'}
];
const index=u.sourceIndex(sentences,byWord,data.affixes);
assert.equal(index.get('mara').length,2,'mara-m and mara-lë-ri-m only');
assert.equal(index.get('mara-suri').length,1,'full compound root is indexed');
assert.equal(index.get('goro').length,1);
assert.equal(index.get('suri').length,1,'must not count inside compound mara-suri-m');
assert.equal(index.get('lësha').length,1);
assert.equal(u.resolveToken('mara-suri-m',byWord).headword,'mara-suri');
assert.equal(u.resolveToken('mara-lë-ri-m',byWord).headword,'mara');
assert.equal(u.resolveToken('mara-nonlexical',byWord),null);
assert.equal(u.resolveToken('mara-suri-goro',byWord),null);
assert.equal(u.highlight('sen mi mara-suri-m!', 'mara',byWord,data.affixes).includes('<mark'),false,
  'do not highlight a component within another lexical headword');
assert.equal(u.highlight('sen mi mara-m!', 'mara',byWord,data.affixes).includes('<mark'),true);
assert.equal(u.highlight('mara <script>!', 'mara',byWord,data.affixes).includes('<script>'),false,'escape HTML');
assert.equal(u.highlight('sen mi MArA-te!', 'mara',byWord,data.affixes).includes('<mark'),true);
for(const word of words){
  const p=u.profile(word,data);
  assert(p.label&&p.targeted&&p.placement&&p.chapter&&p.guide,'every class needs meaningful usage guidance: '+word.qaroshi);
  assert.equal(p.gloss,word.english,'never silently change source gloss');
  assert.equal(p.examplesAreAttested,false,'formulaic forms not attested sentences');
}
const noun=u.profile(words[0],data);
assert.equal(noun.forms.some(x=>x.text==='mara-m'),true);
assert.equal(noun.forms.some(x=>x.text==='mara-ri'),true);
assert.equal(noun.patterns.some(x=>x.pattern.includes('mara-m')),true);
const pron=u.profile(words.find(x=>x.pos==='pron'),data);
assert.equal(pron.forms.some(x=>x.text==='ti-na'),true);
assert.equal(pron.forms.some(x=>x.text==='ti-ri'),false,'cannot create plural pronouns from base');
const verb=u.profile(words.find(x=>x.qaroshi==='goro'),data);
assert.equal(verb.forms.some(x=>x.text==='goro-te'),true);
assert.equal(verb.frame.frame,'V0');assert.equal(verb.frame.selectionNote,'airborne motion, not permission');
const adj=u.profile(words.find(x=>x.pos==='adj'),data);
assert.equal(adj.patterns.some(x=>x.pattern.includes('lësha')),true);
const reg=u.profile(words.find(x=>x.qaroshi==='sen'),data);
assert.equal(reg.isResonance,true);
assert(reg.targeted.includes('Still Voice'));
assert.equal(reg.chapter,'02');
const particle=u.profile(words.find(x=>x.qaroshi==='bëlaro'),data);
assert.equal(particle.sourceRule,'After resonance; report is not belief.');
assert.equal(particle.chapter,'20');
assert(!u.profile(mk('goro','v','fly'),{}).frame,'no inherited frame without source');
console.log('PASS Wiki 9.7 morphology-aware exact corpus links, all word classes, safe template forms, source specificity and HTML escaping');
