'use strict';
const assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm'),path=require('node:path');
const root=path.resolve(__dirname,'../..');
const window={QaroshiUsage:{resolveToken:(token,words)=>{
 const form=token.toLowerCase();return words.has(form)?{headword:form,suffixes:[]}:null;
}};
vm.runInNewContext(fs.readFileSync(path.join(root,'web/wiki_standard10.js'),'utf8'),{window});
const datum={
 words:[{id:'Q1',qaroshi:'mara',english:'friend',pos:'n'},{id:'Q2',qaroshi:'goro',english:'fly',pos:'v'}],
 affixes:[],
 standard10:{
  profiles:{mara:{profile_id:'LXP001',definition:'A trusted peer',
    restriction:'Not every stranger',contrast:'Different from family',
    qaroshi_example:'sen mi mara-m nashi.',english_example:'I cherish a friend.',
    meaning_status:'editorial, independent review pending',reviewer_status:'awaiting reader'}},
  senses:{mara:[{sense_id:'LS1',label:'close friend',definition:'Trusted and enduring peer',
    construction:'mara-m',source_status:'standard editorial sense description'}]},
  priorities:{mara:{rank:12,corpus_mentions:42,source_reference_ids:'S123',
    gloss_interpretation:'English indexing gloss only',lexical_treatment:'editorial review inventory',
    speaker_attestation:'none asserted',source:'data/source.csv'}},
  draft_cards:{mara:{sense_id:'SC1',selected_reference_gloss:'friend',
    candidate_qaroshi:'<img src=x onerror=alert(1)>',
    candidate_english:'Not approved',source:'candidate.csv'}},
  dialogues:[{id:'original11/hello',title:'An introduction',context:'Two speakers',domain:'original',
    turns:[{speaker:'A',qaroshi:'sen mi mara-m tika.',english:'I see a friend.',
      literal_english:'I see the friend.',status:'editorial'}]}],
  controlled_drills:[{id:'TR10-0001',english:'I see.',qaroshi:'sen mi tika.',backtranslated_english:'I see.',
    warning:'Not native approved'}],
  manifest:{canonical_words:30000,core_individually_authored_profiles:1,
    previous_editorial_sense_descriptions:1,unreviewed_gloss_selection_and_example_cards:1,
    editorial_conversations:1,conversation_turns:1,machine_roundtrip_drills:1}
 }
};
const ui=window.Qaroshi10.create(datum);
assert.equal(ui.counts.dialogues,1);
assert.equal(ui.counts.drills,1);
assert.equal(ui.counts.coreProfiles,1);
assert.equal(ui.counts.curatedEntries,1);
assert.equal(ui.counts.proposals,1);
const html=ui.sensesHTML(datum.words[0]);
for(const expected of ['Trusted and enduring peer','mara-m','Not every stranger','LXP001','LS1',
  'UNREVIEWED','independently unverified','English dictionary gloss','independently unverified','SC1']){
 if(!html.toLowerCase().includes(expected.toLowerCase()))throw Error('Missing source status '+expected);
}
assert.equal(html.includes('<img'),false,'untrusted candidate must be HTML-escaped');
assert(html.includes('&lt;img'),'candidate content is safely escaped');
const missing=ui.sensesHTML(datum.words[1]);
assert(missing.includes('No separately reviewed sense definition'));
assert(!missing.includes('Trusted and enduring peer'),'definitions must not bleed to other headwords');
assert.equal(missing.includes('UNREVIEWED'),false);
console.log('PASS Standard 10 source editorial senses, 800-core priority evidence, distinct proposals and safe HTML escaping');
