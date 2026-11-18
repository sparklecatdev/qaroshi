/* Source-only verb composition: exact lexical identity, escaping and UI markers. */
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const code=fs.readFileSync('web/wiki_source_frames.js','utf8');
const context={window:{}};vm.runInNewContext(code,context);
const sample=Array.from({length:97},(_,i)=>({
  source_id:'V87-'+String(i+1).padStart(3,'0'),
  lemma:'testverb'+String.fromCharCode(97+Math.floor(i/26))+String.fromCharCode(97+i%26),patient:'testnoun',gloss:'test gloss',
  domain:'test',source_example_id:'S00123',
  source_sentence:'sen mi testnoun-m testverb'+String.fromCharCode(97+Math.floor(i/26))+String.fromCharCode(97+i%26)+'.',
  source_english:'Test wording',
  semantic_boundary:'Do not infer other objects',
  review_status:'bounded_source_exemplar_not_general_frame',
  human_attested:false,
}));
const app=context.window.QaroshiSourceFrames.create(sample);
assert.equal(app.count,97);
assert.equal(app.compose('testverbaa'),sample[0].source_sentence);
assert.equal(app.compose('testverbaa',{tense:'te',negative:true,question:true,resonance:'hë'}),
  'hë mi testnoun-m nu testverbaa-te he?');
for(const invalid of [
  ()=>app.compose('not-in-source'),
  ()=>app.compose('testverbaa',{tense:'ki'}),
  ()=>app.compose('testverbaa',{resonance:'unrecognized'}),
])assert.throws(invalid);
assert.match(app.renderCard(sample[0],{}),/Original controlled example/);
assert.match(app.renderCard(sample[0],{tense:'yu'}),/EDITORIAL SYNTHETIC FORM/);
const injected={...sample[0],gloss:'<img src=x onerror=alert(1)>'};
const html=app.renderCard(injected,{});
assert(!html.includes('<img src='));
assert(html.includes('&lt;img'));
assert.throws(()=>context.window.QaroshiSourceFrames.create(sample.slice(1)));
console.log('sourceframe UI: exact source validation, safe composition, provenance and escaping passed');
