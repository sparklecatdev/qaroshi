#!/usr/bin/env python3
"""Generate an evidence-based root-learning map, not a claim of universal inferrability.

Lexical roots are not deduced from sound.  This decomposes ONLY dictionary-marked
compounds using the entry's explicitly recorded modifier + head components.
"""
from __future__ import annotations
from pathlib import Path
from collections import Counter,defaultdict
import csv,json,hashlib
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'data/v16';OUT.mkdir(exist_ok=True,parents=True)
with (ROOT/'data/lexicon.csv').open(encoding='utf8',newline='') as f:lex=list(csv.DictReader(f))
D={x['qaroshi']:x for x in lex};comp=[x for x in lex if x['type']=='compound']

def parts(word):
 row=D[word]
 if row['type']!='compound':return []
 return [v.strip() for v in row['components'].split('+') if v.strip()]

def leaves(word,stack=()):
 if word in stack:raise ValueError('cyclic compound: '+str(stack+(word,)))
 if D[word]['type']!='compound':return [word]
 a=parts(word)
 if len(a)!=2 or ''.join(a)!=word or not all(x in D for x in a):raise ValueError('compound mapping invalid '+word)
 return leaves(a[0],stack+(word,))+leaves(a[1],stack+(word,))

leaf_freq=Counter();immediate_freq=Counter();nested=0
for c in comp:
 a=parts(c['qaroshi']);nested+=sum(D[x]['type']=='compound' for x in a)>0
 for p in a:immediate_freq[p]+=1
 for r in set(leaves(c['qaroshi'])):leaf_freq[r]+=1
rank=[r for r,n in leaf_freq.most_common()]
root_ranks={r:i+1 for i,r in enumerate(rank)}
all_bases=set(rank)
assert len(lex)==30000 and len(comp)==13379
rows=[]
for c in comp:
 q=c['qaroshi'];a=parts(q);base=leaves(q);needed=sorted(set(base));maxrank=max(root_ranks[v] for v in needed)
 rows.append({'id':c['id'],'compound':q,'english':c['english'],'modifier':a[0], 'modifier_english':D[a[0]]['english'], 'head':a[1], 'head_english':D[a[1]]['english'], 'ultimate_base_roots':' + '.join(base),'base_count':len(needed),'learning_threshold':maxrank,'status':'Transparent modifier-head FORM; actual contextual sense may be narrower or lexicalized.', 'editorial_review':''})
with (OUT/'compound_decomposition_13379.csv').open('w',encoding='utf8',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
root_rows=[]
for rank_no,q in enumerate(rank,1):
 r=D[q];related=[x['compound'] for x in rows if q in x['ultimate_base_roots'].split(' + ')]
 root_rows.append({'rank':rank_no,'root':q,'english':r['english'],'ipa':r['ipa'],'pos':r['pos'],'domain':r['domain'],'type':r['type'], 'immediate_compound_mentions':immediate_freq[q], 'compounds_using_base_root':leaf_freq[q], 'first_6_compounds':' | '.join(related[:6]), 'status':'Existing dictionary word; root meaning must be learned or independently derived, not read from phonetics.'})
with (OUT/'productive_root_learning_ladder.csv').open('w',encoding='utf8',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(root_rows[0]));w.writeheader();w.writerows(root_rows)
thresholds=(25,50,100,200,350,500,750,1000,1250,1500,len(rank))
coverage=[{'unique_base_roots_learned':n,'unlocked_compounds':sum(x['learning_threshold']<=n for x in rows),'fraction_compounds':round(sum(x['learning_threshold']<=n for x in rows)/len(comp),5)} for n in thresholds]
summary={'lexicon_entries':len(lex),'compound_entries':len(comp),'headword_labeled_entries':sum(x['type']=='headword' for x in lex),'function_word_entries':sum(x['type']=='function word' for x in lex),'distinct_immediate_components':len(immediate_freq),'unique_ultimate_base_components':len(all_bases),'headword_bases_in_compounds':sum(D[q]['type']=='headword' for q in all_bases),'nested_compounds':nested,'compound_components_resolve':len(rows),'compound_forms_match_concatenated_components':len(rows),'learning_curve':coverage,'non_compound_headwords_without_explicit_compound_analysis':sum(x['type']=='headword' for x in lex),'claim_limits':['One must first learn base meanings. Word sounds do not encode definitions.','Knowing components does not guarantee the exact conventional or technical gloss.','The dictionary documents modifier–head morphology but not 16,525 headword derivations.','Ranks optimize compound reuse, not conversation frequency or psychological acquisition difficulty.','Grammatical suffixes are predictable on their own rules, not a way to guess lexical roots.'],'canonical_dictionary_sha256':hashlib.sha256((ROOT/'data/lexicon.csv').read_bytes()).hexdigest()}
(OUT/'root_learnability_manifest.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf8')
md=['# Qaroshi root learning and word inference', '', '## Can a learner infer every word through grammar?', '', '**No.** Grammar reliably parses licensed suffixes and sentences; only **13,379** of the 30,000 dictionary entries are explicitly marked compounds. Those entries all have two documented modifier/head components, and every recorded component resolves to a canonical dictionary entry. The remaining **16,525** entries labeled `headword` do not have the same explicit compositional map. The **96** function words also require learning.', '', f'The compounds use **{len(immediate_freq):,} distinct immediate component words**, which recursively reduce to **{len(all_bases):,} unique base words**; **{nested}** compounds use at least one compound as their immediate component. This is a much better study target than 30,000 separate flashcards, but it does not prove that all the base words are guessable.', '', '## How composition works', '', 'Compounds are written modifier first, semantic head last. Their component boundaries are stored in the dictionary; they are not always visually obvious because the spelling concatenates them. A compound should be interpreted from its components with the dictionary sense checked if the meaning is specialized.', '', 'Examples from the canonical data:', '']
for q in ['babawayabikhimi','babawayayokhëgu','bagotëbediko','bagotëbengeka']:
 if q not in D:continue
 a=parts(q);md.append(f"- `{q}` = `{a[0]}` ({D[a[0]]['english']}) + `{a[1]}` ({D[a[1]]['english']}) → **{D[q]['english']}**")
md+=['','## Grammatical morphology is different', '', '- `goro` = fly; `goro-te` = flew, `goro-ki` = can fly, `goro-ho` = may fly. The suffixes tell you tense and modality once you know the verb root.', '- `mara` = friend; `mara-ri-m` = friends (plural) as the direct object. The reversed form `mara-m-ri` violates the suffix order.', '- Sentence-initial written resonance markers (16) are obligatory, but do not independently reveal a noun or verb meaning.', '', '## Compounds unlocked by learning the most reused **ultimate base roots**', '', '| Root words known | Compositional compounds with every base known |', '|---:|---:|']
md += [f"| {r['unique_base_roots_learned']:,} | {r['unlocked_compounds']:,} ({100*r['fraction_compounds']:.1f}%) |" for r in coverage]
md+=['', '**This is a computational coverage estimate, not a learning experiment.** It orders words by participation in compounds, not ease of learning or frequency in real conversations. A learner should combine this with common conversation vocabulary.','', '## Current design limitations to address in future standards', '', '1. **Base-root arbitrariness.** A non-compound headword like `goro` has to be learned. Technical words that were independently coined may be especially difficult; they need a pedagogical root family, a semantic derivation if justified, or a shorter ordinary-language paraphrase.', '2. **Hidden boundaries.** Concatenated modifier–head strings can look like random syllables, even when they have a canonical decomposition. Dictionary and Academy should show the constituent roots prominently.', '3. **Technical senses.** Literal root composition can suggest a broad class, while the conventional recorded gloss can be narrower. Do not promote automatic guesses to dictionary senses.', '4. **Headword audit.** Existing headwords may have genuine historical derivations not documented in the `components` field. This audit does not infer or impose new segmentation without linguistic review.', '5. **Avoid forced regularization.** Do not silently rename canonical words or replace old spelling/phonology. Draft candidates should be shown beside canonical forms and require transparent, reviewed migration.', '', '## Reproducibility','', 'Run `python tools/v16/build_root_guide.py`. It emits `data/v16/compound_decomposition_13379.csv`, `data/v16/productive_root_learning_ladder.csv` and `data/v16/root_learnability_manifest.json`. The canonical `data/lexicon.csv` is read-only.', '']
(ROOT/'Qaroshi_16_Roots_and_Inference.md').write_text('\n'.join(md),encoding='utf8')
print(json.dumps({k:v for k,v in summary.items() if k not in ('learning_curve','claim_limits','canonical_dictionary_sha256')},indent=2));print('learning ladder',coverage)
