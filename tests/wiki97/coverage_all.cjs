'use strict';
/* Traverse every canonical Wiki word against real embedded source metadata.
 * This is a software completeness check, NOT proof of semantic correctness or
 * independent speaker comprehension.
 */
const assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm'),path=require('node:path');
const root=path.resolve(__dirname,'../..');
const html=fs.readFileSync(path.join(root,'Qaroshi_Wiki.html'),'utf8');
const match=html.match(/<script type="application\/json" id="wiki-data">([\s\S]*?)<\/script>/);
assert(match,'standalone site must embed source metadata');
const data=JSON.parse(match[1]);
const w={};
vm.runInNewContext(fs.readFileSync(path.join(root,'web/wiki_usage.js'),'utf8'),{window:w});
const engine=w.QaroshiUsage;
assert.equal(data.words.length,30000);
assert.equal(data.phrases.length,4383);
assert.equal(data.resonances.length,16);
assert(data.grammaticalParticles.length>10);
assert(data.pronouns.length>=10);
assert.equal(data.grammarFrames.length,25);
const byWord=new Map(data.words.map(x=>[x.qaroshi.toLowerCase(),x]));
const source=engine.sourceIndex(data.phrases,byWord,data.affixes);
const editorial=engine.sourceIndex(data.semanticCases,byWord,data.affixes);
const classes={},withNotes=[],withRules=[],withForms=0,withTemplates=0;
let forms=0,templates=0,frames=0,registers=0;
for(const word of data.words){
  assert(word.qaroshi&&word.english&&word.pos&&word.id,'source entry incomplete');
  const u=engine.profile(word,data);
  assert.equal(u.gloss,word.english,'source English gloss must be preserved: '+word.qaroshi);
  assert(u.targeted.length>35,'missing word class or sense explanation: '+word.qaroshi);
  assert(u.placement.length>35,'missing grammatical usage explanation: '+word.qaroshi);
  assert(u.chapter&&u.guide,'must link to canonical grammar and instruction');
  assert.equal(u.examplesAreAttested,false,'schema patterns are not independently observed');
  assert.equal(u.meaningIsEditorialGloss,true,'the source gloss must remain explicitly editorial');
  assert(!u.forms.some(x=>x.text.includes('[')), 'forms are single tokens or negation illustration');
  classes[word.pos]=(classes[word.pos]||0)+1;
  if(word.note)withNotes.push(word.qaroshi);
  if(u.sourceRule)withRules.push(word.qaroshi);
  if(u.forms.length)forms++;
  if(u.patterns.length)templates++;
  if(u.frame)frames++;
  if(u.isResonance)registers++;
}
assert(forms>1000,'noun/verb morphology should be available for many entries');
assert(templates>1000,'explicit classroom patterns should cover common content classes');
assert(frames>=20,'reviewed source frames should render for canonical verbs');
assert.equal(registers,16,'all sentence-initial resonances need special teaching semantics');
let examples=0;
for(const [lemma,list] of source){
  assert(byWord.has(lemma));
  examples+=list.length;
  for(const x of list){
    assert(x.sentence.id&&x.sentence.english);
    assert.equal(engine.resolveToken(x.surface,byWord,new Set([
      ...data.affixes.map(a=>a.form),'-za'])).headword,lemma,
      'no substring-only or unrelated compound false positives');
    const marked=engine.highlight(x.sentence.qaroshi,lemma,byWord,data.affixes);
    assert(marked.includes('<mark class="lexical-highlight">'),'recorded occurrence is highlightable: '+lemma);
  }
}
assert(source.size>100,'several teaching words must have source examples');
assert(examples>100,'source corpus word uses must not be lost');
assert(editorial.size>0,'editorial candidates remain findable with the correct caveats');
const coverage={
  checked_words:data.words.length,
  by_class:classes,
  with_grammar_form_illustrations:forms,
  with_source_referenced_templates:templates,
  with_specific_particle_rule:withRules.length,
  with_reviewed_valency_frame:frames,
  resonance_guides:registers,
  headwords_with_exact_source_corpus_example:source.size,
  exact_source_corpus_headword_sentence_pairs:examples,
  headwords_with_editorial_case_candidate:editorial.size,
  headwords_without_exact_corpus_sentence:data.words.length-source.size,
  source_sentences:data.phrases.length,
  independent_human_semantic_comprehension_count:0
};
console.log('PASS Wiki 9.7 every canonical word has a source-bound meaning/usage explanation; no invented sentence evidence');
console.log(JSON.stringify(coverage,null,2));
