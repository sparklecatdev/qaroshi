#!/usr/bin/env python3
"""Source-grounded release documentation for editorial lexical consistency."""
import csv,json,hashlib,collections
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];D=ROOT/'data/v16_2'
def rows(f):
 with (D/f).open(encoding='utf8',newline='') as x:return list(csv.DictReader(x))
R=json.loads((D/'review_summary.json').read_text(encoding='utf8'))
A=rows('all_3817_candidates_screened.csv');M=rows('individually_editorially_reviewed.csv');G=rows('eight_root_decision_dossiers.csv');E=rows('hypothetical_new_root_derivatives.csv')
counts=collections.Counter(x['status'] for x in A)
flags=collections.Counter()
for a in A:
 for flag in a['risk_codes'].split(' | '):flags[flag]+=1
start='''# Qaroshi 16.2: Root Standardization & Editorial Learnability

**Release category:** Compatible editorial-development and review tooling, *not an approved standards revision*.

## The learner’s central problem

A dictionary with 30,000 words feels much larger than it needs to. Existing grammar correctly predicts inflections (e.g., `goro-te` past, `goro-ki` ability, `goro-ho` permission), and the 13,379 documented canonical compounds can often be understood by learning component roots. But 16,525 headwords lack the same official internal derivation. A proposed compound is useful only if its components have the **right senses**, its length is practical, and its meaning would be understood without an English-gloss cheat sheet.

**What we did not do:** Rename or replace a single canonical entry, claim any new word has been speaker-attested, or silently approve invented roots.

## Screening totals

| Category | Records |
|---|---:|
| Pre-existing 16.1 proposed component pairs screened | 3,817 |
| Individually editorially inspected | 65 |
| Editorial trial for further contextual testing | 44 |
| Editorial hold for ambiguity | 9 |
| Editorial rejection of misleading source senses | 12 |
| Machine-only shortlist, **not individually reviewed** | 1,963 |
| Other unreviewed items deferred | 1,789 |
| Narrow proposed root dossiers (all noncanonical) | 8 |
| Reuse-first decisions | 8 |
| Hypothetical new-root compounds for review | 26 |
| Grammar / meaning learning contrasts | 16 |
| Approved new canonical words | **0** |

The machine shortlist is intentionally NOT called a list of valid new words. The ranking can prioritize review, but it does not establish conventional usage.

## Examples from individual editorial judgments

| Existing standard | Existing meaning | Optional candidate | Editorial outcome | Why |
|---|---|---|---|---|
'''
order=['banuaro','khezhëpe','ngodudi','lamiti','wazola','nguzora','zadonë','sakazo','pizikha','këngopu','ngizhobi','giduno','nëqido','rawaro','zhuzozha','ngukhëgo','ngusuqo','ngalerazi','ngolutuli','zudëshi']
by={x['canonical_word']:x for x in M}
for k in order:
 if k not in by:continue
 x=by[k];start+='| `'+x['canonical_word']+'` | '+x['canonical_english'].split(';')[0].replace('|','/')+' | `'+x['candidate_form']+'` | '+x['status'].replace('manual_','')+' | '+x['editorial_note'].replace('|','/')+' |\n'
start+='''
**The important failures:** “meter” for music is not a water measuring meter; “tip” as a gratuity is not an animal-tail tip; “grooming” used for abuse cannot be presumed to mean ordinary feather or tail care. Such expressions are clearly rejected in the trial register. Similar parenthetical domain senses across the other candidates remain under manual review.

## Why only 65 individual semantic judgments?

An explicit note was written for each of these forms with an independent testable boundary. Another 1,963 forms pass a cheap gloss/length/component heuristic, but automatically labeling those as “approved natural Qaroshi” would repeat the very error this revision is designed to fix.

## Eight minimal missing-root dossiers

The draft *root spellings* are invented. They are not historical etymologies, canonical lexemes, or guaranteed learnable words. Productive payoff must justify any extra memorization burden.

| Concept | Trial form | Citation IPA (machine generated) | Status | Narrow definition |
|---|---|---|---|---|
'''
for x in G:start+=f"| {x['concept']} | `{x['tentative_form']}` | `{x['provisional_ipa']}` | {x['proposal_status']} | {x['narrow_proposed_sense']} |\n"
start+='''
### Reuse existing structure first

- `rekesi` is already a canonical **verb** meaning cycle. A noun for recurring cycles requires POS and derivation review; `rekesi-rëma` literally indicates a cycling *event*, not automatically every technical cycle.
- `dëmi` means help/assist and the existing instrument suffix `-këlë` may support a helping device. Do not promote that combination to a standardized noun without testing its meaning.
- The reflexive suffix `-ne` already helps with self-directed verbal actions. It does not mean every English word containing “self” should be turned into the same pseudo-root.
- `ha` is an existing hello/greeting interjection; `maho` already denotes consent; `mëna` means fact/established information. Reuse these when their recorded meaning genuinely fits.
- “Call” has human telephone/contact and animal vocalization senses. One new universal translation would conflate them; it is deliberately not coined here.

The proposed generic card root is restricted to physical identity/payment tokens, excluding computer memory cards. The proposed signature root is for handwritten personal marks, excluding musical time signatures and cryptographic signatures. The proposed cycle noun root is **deferred** because the canonical verb and derivational rules need review first.

## Semantic review procedure

1. Compare the English source meaning with the **entire primary gloss of both component roots**, not merely overlapping English letters.
2. Check polysemy, technical qualifiers, grammatical POS, and word-formation order.
3. Reject misleading meanings even when the spelling concatenates perfectly.
4. Test the candidate in at least three **independently written** Qaroshi contexts and request an unaided interpretation from another person. Those human observations do not exist yet.
5. Compare the time, ambiguity, and memory cost of the proposed compound with the existing short word. A longer transparent expression can be useful as an explanation without replacing the word used in ordinary speech.
6. Record the review outcome and supporting contexts; only then consider an optional glossary note, accepted parallel expression, or formal lexical change.

## Reproducibility and compatibility

Run from the extracted `Qaroshi/` directory:

```bash
python tools/v16_2/build_reform.py
python tools/v16_2/build_pronunciation.py
python tools/v16_2/build_studio.py
python -m unittest discover -s tests -q
```

The offline Studio displays **30,000 canonical dictionary entries** and the complete 3,817-variant review board. User notes are stored locally and export/import as JSON. No external API is required.

**Limitations:** The 16.1 generated source alternatives are hypotheses. Manual editorial screening by one author is not an empirical speaker study. No standard forms were altered. A word cannot be inferred merely from its letters if it is a genuine independent root.
'''
(ROOT/'Qaroshi_16_2_Root_Standardization_Guide.md').write_text(start,encoding='utf8')
report='''# Qaroshi 16.2 Release Notes

**Status:** Development milestone, backwards-compatible; no canonical lexical adoption.

This release carries forward the exact 30,000-entry reference plus the verified 16.1 source, adding an editorial/semantic decision layer. It creates no conventional idiom, naturalistic speaker record or new canonical lexeme.

## Contents

- `data/v16_2/all_3817_candidates_screened.csv`: every source proposal, senses, source word, spelling, risk codes, score and distinct status.
- `data/v16_2/individually_editorially_reviewed.csv`: 65 specifically inspected records, with detailed rationale (44 controlled trials, 9 holds, 12 rejections).
- `data/v16_2/machine_shortlist_unapproved.csv`: 1,963 machine-ranked but unreviewed suggestions.
- `data/v16_2/eight_root_decision_dossiers.csv`: 8 candidate root sense boundaries, pronunciation guesses, nearest spellings and missing-concept reuse analysis.
- `data/v16_2/reuse_before_coinage.csv`: 8 cases where existing words or suffixes should be investigated first.
- `data/v16_2/hypothetical_new_root_derivatives.csv`: 26 restricted experimental compounds.
- `data/v16_2/sixteen_grammar_and_learnability_examples.csv`: grammar-versus-vocabulary contrasts.
- `Qaroshi_16_2_Root_Standardization_Studio.html`: standalone 30,000-word dictionary and candidate comparison app with local notes and export/import.
- `tools/v16_2/`: reproducible audit, pronunciation, documentation, and app builders; Chromium check script.
- `tests/test_v16_2_lexical_decisions.py`: individual human-editorial-trial, false-friend, source-integrity and root tests.

## Pending review

There are **zero approved canonical replacements** and **zero speaker-attested newly coined roots**. The word-list learning benefit is a hypothesis requiring real speaker feedback. The source ZIP is standalone; any GitHub checkpoint is not equivalent to publication of the entire archive.
'''
(ROOT/'Qaroshi_16_2_Release_Notes.md').write_text(report,encoding='utf8')
(ROOT/'README_16_2_START_HERE.md').write_text('''# Qaroshi 16.2: Start here

Open `Qaroshi_16_2_Root_Standardization_Studio.html` in a desktop or mobile browser. No server or account required.

The default dictionary remains 30,000 canonical words. Navigate to **Editorial review** to compare transparent forms with their canonical equivalents, and filter to 44 `manual_trial` entries to see the strongest individually screened constructions. Do not study those as approved canonical forms.

**Missing roots** distinguishes 8 invented root dossiers from 8 existing roots or grammar rules that could avoid coinage. **Learn by building** contains 16 grammar contrasts.

Read `Qaroshi_16_2_Root_Standardization_Guide.md` and `Qaroshi_16_2_Release_Notes.md` before publishing or teaching any unaccepted lexical proposal. The original Wiki, Academy, Fluency Labs, earlier corpus and prior review tools are still present.

The correct next step is real independent semantic testing, not a mass rename.
''',encoding='utf8')
print('Generated 3 docs, counts:',dict(counts),'flags:',dict(flags))
