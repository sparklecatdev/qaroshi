#!/usr/bin/env node
/* Reproducible lexical-content review queue: prioritize missing, source-checked
 * example coverage and underspecified senses, never invent missing evidence.
 */
'use strict';
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const root=path.resolve(__dirname,'../..'),args=process.argv.slice(2);
const out=path.resolve(root,args[args.indexOf('--out')+1]||'data/standard10/generated');
const html=fs.readFileSync(path.join(root,'Qaroshi_Wiki.html'),'utf8');
const m=html.match(/<script type="application\/json" id="wiki-data">([\s\S]*?)<\/script>/);
if(!m)throw Error('Build offline Wiki first');
const data=JSON.parse(m[1]);
const global={};vm.runInNewContext(fs.readFileSync(path.join(root,'web/wiki_usage.js'),'utf8'),{window:global});
const words=new Map(data.words.map(w=>[w.qaroshi.toLowerCase(),w]));
const source=global.QaroshiUsage.sourceIndex(data.phrases,words,data.affixes);
const turns=data.standard10.dialogues.flatMap(d=>d.turns);
const connected=global.QaroshiUsage.sourceIndex(turns,words,data.affixes);
const originalTurns=data.standard10.dialogues.filter(d=>d.id.startsWith('original11/')).flatMap(d=>d.turns);
const recombinedTurns=data.standard10.dialogues.filter(d=>d.id.startsWith('source18/')).flatMap(d=>d.turns);
const originalSceneIndex=global.QaroshiUsage.sourceIndex(originalTurns,words,data.affixes);
const recombinedSceneIndex=global.QaroshiUsage.sourceIndex(recombinedTurns,words,data.affixes);
const anyDocumentedIndex=new Set([...source.keys(),...originalSceneIndex.keys(),...recombinedSceneIndex.keys()]);

const s=data.standard10;
const candidate=data.words.map(w=>{
 const rootWord=!w.components,pr=s.priorities[w.qaroshi],prof=s.profiles[w.qaroshi],senses=s.senses[w.qaroshi]||[];
 const count=source.get(w.qaroshi.toLowerCase())?.length||0;
 const dialogues=connected.get(w.qaroshi.toLowerCase())?.length||0;
 const draft=s.draft_cards[w.qaroshi];
 const missingDefinition=!prof&&!senses.length;
 const needs=[];
 if(!count)needs.push('No exact original 4,383-sentence corpus use');
 if(missingDefinition)needs.push('No individually authored or inherited sense definition');
 if(draft)needs.push('5,000-card editorial candidate awaits semantic/selection review');
 if(w.english.includes(';'))needs.push('Multiple source English gloss segments need scope check');
 return {
  id:w.id,lemma:w.qaroshi,pos:w.pos,canonical_english_gloss:w.english,
  domain:w.domain,word_kind:rootWord?'independent source entry':'recorded compound',
  exact_original_corpus_example_count:count,
  connected_editorial_dialogue_turn_count:dialogues,
  core_priority_rank:pr?.rank||'',
  has_individually_authored_definition:!!prof,
  inherited_curated_sense_count:senses.length,
  has_unreviewed_candidate:!!draft,
  review_needed:needs.join('; '),
  editorial_status:'Source/example evidence only: no independent human attestation',
  weight:(pr?200000-pr.rank*100:0)+(!count?10000:0)+(!missingDefinition?0:5500)+(rootWord?500:0)+dialogues*15,
 };
}).filter(x=>x.review_needed);
candidate.sort((a,b)=>b.weight-a.weight||a.id.localeCompare(b.id));
fs.mkdirSync(out,{recursive:true});
const rows=candidate.slice(0,1000);
const fields=Object.keys(rows[0]).filter(x=>x!=='weight');
const csvCell=x=>'"'+String(x??'').replaceAll('"','""')+'"';
fs.writeFileSync(path.join(out,'priority_1000_editorial_review_queue.csv'),
 [fields.join(','),...rows.map(x=>fields.map(k=>csvCell(x[k])).join(','))].join('\n')+'\n','utf8');
const summary={
 source_dictionary_entries:data.words.length,
 original_bilingual_teaching_sentences:data.phrases.length,
 headwords_with_exact_original_corpus_use:source.size,
 headwords_without_original_corpus_use:data.words.length-source.size,
 lexemes_with_connected_editorial_turn_use:connected.size,
 headwords_in_individually_scripted_editorial_scenes:originalSceneIndex.size,
 headwords_in_recombined_reference_scenes:recombinedSceneIndex.size,
 headwords_with_any_original_sentence_or_editorial_scene: anyDocumentedIndex.size,
 headwords_without_any_recorded_sentence_or_editorial_scene: data.words.length-anyDocumentedIndex.size,
 source_evidence_separation: 'Original parallel corpus, independently scripted editorial scenes, and recombined reference paths are three distinct evidence classes, none spontaneous fluent-speaker attestation.',

 editorial_conversation_turns:turns.length,
 original_source_priority_index: Object.keys(s.priorities).length,
 queued_for_review:rows.length,
 reviewers_recorded:0,
 automatic_proficiency_certification:false,
 note:'This report organizes existing materials. Missing editorial examples and semantic sense boundaries need editorial and independent human validation, not synthetic automatic ratification.'
};
fs.writeFileSync(path.join(out,'coverage_gap_report.json'),JSON.stringify(summary,null,2)+'\n','utf8');
console.log(JSON.stringify(summary,null,2));
