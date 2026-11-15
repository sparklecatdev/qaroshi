# The ten requested Qaroshi completion tasks

**Evaluation standard:** "completed" means the deliverable was actually generated and tested. "partial" means a meaningful artifact exists, but the intended linguistic, empirical, or platform-level requirement is not met. Files listed below are relative to the ZIP root. Nothing here attests to a real-world speaker community or invents linguistic field evidence.

| # | Task | Status | Concrete evidence | Outstanding condition |
|--:|---|---|---|---|
| 1 | Review 1,000 idioms | **Structural pass, cultural review outstanding** | `data/review/idiom_review_1000.csv`, 1,000 lexically grounded candidates from 25 metaphor families; all structurally checked | Independent idiomaticity judgements; reviewer/editor acceptance |
| 2 | Finalize 5,000 word senses | **Source match, semantic review outstanding** | `data/review/sense_review_5000.csv`, all linked to existing canonical headwords and checked for basic grammatical consistency | Individually verified polysemy, synonyms/antonyms, restrictions, natural examples |
| 3 | 1,000 distinct natural conversations | **Not met** | 12 separately authored scenes / 96 utterances, plus existing 1,000 controlled, templated practice exchanges | At least 988 more independent, non-template, reviewed coherent conversations |
| 4 | Natural 100,000-word corpus | **Not met** | 123,000 earlier controlled pedagogical Qaroshi tokens; 5 newly drafted short readings / 50 sentences | A genuinely diverse, coherent corpus with documented provenance, genres, tokenization and editorial review |
| 5 | Resolve grammar ambiguities | **Partial** | `tools/fluency2026/analyzer2.py`, 209 current automated tests and 4,200 existing grammar fixtures; 94 minimal meaning contrasts | Comprehensive semantic scope, word-order freedom, idiomaticity and ambiguity adjudication |
| 6 | Finish native writing system | **Partial** | 26 original glyphs, experimental font builder tested with a compiled local TTF; XKB and Keyman sources; browser glyph viewer | Native platform keyboard certification, interoperable long-term encoding, punctuation decisions and distribution approval |
| 7 | Spoken Qaroshi | **Human audio / dialect goals unmet** | 3,000 target-manifest rows and consent-first microphone helper; IPA and English-style guides | **0 human audio samples** and no empirically supported regional dialect data; acquire actual consented speakers |
| 8 | Bidirectional translation and grammar tools | **Limited subset delivered** | `analyzer2.py`, `bilingual_demo.py`, conservative browser checker | General-purpose context-sensitive translation and syntax/semantic parsing; independent blind evaluation |
| 9 | Advanced Academy | **Partial** | Original Academy and 24 lessons, plus 94 contrast questions, 12 dialogues, 5 readings, local scoring and export in completion workbench | Full adaptive advanced curriculum, benchmarked mastery levels, speaking/listening instruction, instructional review |
| 10 | Finalize/publish standard and literature | **Local release candidate; community approval pending** | Complete verified ZIP, cultural review docs, 5 additional editorial readings, existing GitHub draft PR | Merge an accepted standard after documented review; upload all source to public repository / reproducible release; grow substantive independently authored literature |

## Evidence rules

An automated structural check cannot certify naturalness, phonetic recordings, semantic truth, consent, or genuine social conventions. The current workbench reports such distinctions explicitly. Stage labels are editorial metadata, not grammatical markers and not claims of an attested native speech community.

## Next independent steps

1. Assign reviewers to idiom and sense rows; record rationale, minimal contrasts and acceptance, not just a binary vote.
2. Have multiple writers independently author new conversations and longer prose; blind check meaning and morphology before promoting them.
3. Recruit consented speakers, document pronunciation and variation, then compare the recordings to the existing broad IPA.
4. Test keyboard source on real Windows, macOS, Linux, Android and iOS devices and maintain versioned mapping tests.
5. Retest advanced grammar and translation with unseen examples; publish only reviewed change sets and preserve older standard semantics.
