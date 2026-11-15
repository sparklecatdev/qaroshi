#!/usr/bin/env python3
from pathlib import Path
root=Path(__file__).resolve().parents[1];d=root/'docs'
APPEND={
 'translation.md':r'''

---

## An end-to-end translation workshop

Translation begins with an **analysis of what the source asserts**, not a search for matching dictionary words. A phrase may describe an action, a quality, an unreal premise, a goal, a remembered fact or a request. Identify its main predicate first. English makes extensive use of word order, articles and auxiliary verbs, while Qaroshi expresses many analogous distinctions through case marking, suffixes, particles and the required written resonance. A sentence can be grammatically well formed and still fail to translate the user's intended speech act.

### Step 1: give each participant a role

In `sen mi mara-tu kima-m pëli.`, the subject `mi` is the giver, the dative `mara-tu` is the recipient and the object `kima-m` is the transferred theme. A literal parse is `REG I friend-DAT water-OBJ give`. The natural English is “I give water to a friend.” If English happened to say “I give a friend water,” the Qaroshi semantic roles would remain the same. Translate *relationships* first, linear order second.

### Step 2: distinguish event time, event shape and modal force

From a verb root such as `goro` fly, the inflectional ending can express past `-te`, future `-yu`, ongoing `-se`, habitual `-në`, ability `-ki`, permission `-ho` or requirement `-du`. These features do not correspond to one generic English auxiliary word. In an instruction, confusing “may enter” with “must enter” is a substantive error. In a personal promise, confusing “can help” with “will help” changes the speaker's commitment. Annotate all relevant suffix slots before choosing the English tense and auxiliaries.

### Step 3: preserve the interrogative or directive force

Direct yes/no questions end in `he`, while requests/commands end in `ya`. A sentence with `pëla` and `ya` is not merely a friendly statement. An optative with `yëmë` expresses a wish without commanding another person. The resonance marker shapes how these speech acts are offered: `khar` can make a question alarmed, while `hë` can make it sincerely curious. A narrator's English “she asked nervously” may be the most faithful way to retain a register if a literal wording would be clumsy.

### Step 4: represent logical clauses faithfully

A `ro` clause states a reason and a `ko` clause states a purpose. A real condition with `wë` is not the same as a counterfactual with `wënu`, particularly when the consequence closes with `qinë`. Translators should identify whether the underlying relationship is cause, intention, possibility, temporal sequence, concession or exception. Flattening “unless,” “even if,” and “because” into a simple “if” silently changes the meaning.

### Step 5: carry evidence and quotation integrity

`si` indicates personally witnessed information, `hu` a report and `ye` inference. An English translation can sometimes use a phrase such as “apparently,” “I saw” or “according to the report.” Do not translate an inferential sentence into an unqualified observation. Likewise, the later grammar distinguishes exact quotation and paraphrase, particularly important in scientific, legal and personal statements.

### Step 6: solve ambiguity instead of hiding it

The dictionary lists specific lexical senses. A single English word can name unrelated concepts; for instance, the social sense of *trust* is not automatically the cryptographic sense. When the exact Qaroshi term is absent, use a documented compound or explain with a fuller clause. Do not treat an invented English calque as an established Qaroshi idiom. When two parses remain plausible, note the uncertainty for the reader rather than inserting details that were never stated.

## A line-by-line translation test

Use the following controlled examples; they are taken from the bilingual phrasebook and preserve its wording.

| Qaroshi | Literal analytical focus | English |
|---|---|---|
| `më ti lësha.` | Warm Hum + you + cute predicate | You are cute. |
| `sen mi kima-m këmë.` | neutral + I + water-OBJ + drink | I drink water. |
| `hë ti haro he?` | question resonance + you + well + question ending | Are you well? |
| `sen sa goro-te si.` | neutral + they + flew + witnessed | They flew; I saw it. |
| `sen sa goro-te hu.` | neutral + they + flew + reported | They flew, according to a report. |
| `sen mi naro-gu gura.` | neutral + I + home-GOAL + travel | I'm going toward home. |
| `sen mi naro-de gura.` | neutral + I + home-SOURCE + travel | I'm leaving home. |

The first two columns are not intended to be read in a natural English order; the literal column is a pedagogical check that each morphological segment has been interpreted. Where English can be more idiomatic without losing information, prioritize a faithful natural translation after documenting the morphology.

## Independent translation rubric

A careful translation passes five tests: **content** (the same participants and events), **grammar** (case and suffix roles represented), **scope** (negation, quantity, condition and focus), **stance** (resonance and social intention), and **evidence** (how the proposition is known). Passing only the content test is not enough for legal, medical, technical or intimate writing. The [Sentence atlas](deep_guides/sentence_atlas.md), [Complex clause guide](deep_guides/clauses_and_counterfactuals.md) and [Editing clinic](deep_guides/editing_troubleshooting.md) provide extended practice.
''',
 'lexicography.md':r'''

---

## Reading entries as a lexicographer

A headword is a spelling connected to a defined lexical sense and grammatical behavior. It is not an instruction to substitute the English gloss wherever an English writer happens to use the same letters. The English gloss *safe* might represent a state, a safety-related device or an instruction to avoid danger; these belong to different semantic categories even if English shares the word. The lexicon therefore separates **part of speech**, **definition/sense**, **domain**, **word components**, **usage note** and **phonetics**.

### Three tests before choosing a word

**Semantic test:** What is the exact intended meaning? If an English term is polysemous, locate the correct sense. **Syntactic test:** Is the entry a noun, verb, adjective, adverb or function word? Do not force a noun directly into a verb slot without a documented conversion process. **Pragmatic test:** Does the entry imply romance, family, ownership, legal status, permission, or a technical property that the source actually intends? Avoid silently intensifying the claim.

## Inflected forms are predictable, but lexical senses are not

`qaro-ri` is the regular plural of `qaro`, not a second unrelated entry with a new root. `goro-te-se` expresses past continuous flying by ordinary verb morphology. By contrast, `qaroshi` is a specific lexical compound, because the conventional meaning “the Nardoragon language” matters. When a reader sees `naro`, `naro-gu` and `naro-de`, the differences are grammatical roles; when a reader sees a head-final compound, the definition may be specialized beyond the simplest literal sum.

Compounding works modifier-first and head-last in documented examples. That does not mean any two dictionary words can be concatenated and accepted automatically. A new technical term needs unambiguous root choices, a well-documented semantic relationship and a natural use in a sentence. Where the relationship cannot be expressed cleanly by a compound, a content clause or relative clause may be clearer.

## Using the reverse index critically

English-to-Qaroshi lookup is best treated as a list of possible senses. It does not demonstrate that two results are mutually interchangeable; they may belong to different domains or word classes. Exact Qaroshi spelling has priority over accent-folded search. In particular, `ë` and `e` are distinct native vowels even though the search tool may allow `gero` to retrieve `gëro`. The displayed dictionary entry, not the approximate search string, is the spelling to use in writing.

## Stable identifiers and maintenance

A lexical entry has a stable `id`, enabling citations across the wiki and data exports. A word page may have related topical entries, but those are **not a formal synonym set**. For careful cross-referencing, cite the exact headword and ID, record which definition was used, and retain the original broad IPA fields. If a definition is clarified later, distinguish an editorial gloss improvement from a change in the word's denotation. The [Dictionary mastery guide](deep_guides/dictionary_compounding.md) expands this into a full practical workflow.
''',
 'pronunciation.md':r'''

---

## Practical articulation and stress training

A pronunciation entry can show three complementary kinds of help. **IPA** indicates the intended phonemes with minimal ambiguity; the **Qaroshi syllable guide** groups syllables and capitalizes a stress-bearing syllable; and the **English-style sound-out** is an approximate bridge for beginners. Where these disagree with an English reader's first impression, the IPA remains the reference. For instance, Qaroshi `q` /q/ is never English letter-name “cue,” and `kh` /x/ is not two separate consonants.

### Train vowels before whole sentences

Sustain each vowel without adding a glide: `a /a/`, `e /e/`, `i /i/`, `o /o/`, `u /u/`, `ë /ə/`. Then switch deliberately between pairs likely to be confused by an English speaker: `e` versus `ë`, `i` versus `e`, and pure `o` versus English diphthongal “oh.” The reference does not assert that invented minimal pairs are part of the dictionary; use existing headwords in the dictionary for lexical practice rather than fabricating similar-looking words.

### Train consonant place and manner

Contrast `k /k/` against farther-back `q /q/`; practice the fricative duration of `kh /x/`; keep `ng /ŋ/` nasal with no added stop; use a single tap for `r /ɾ/`; voice `zh /ʒ/` while keeping `sh /ʃ/` unvoiced. English spelling conventions do not determine these sounds: `sh`, `zh`, `kh`, `ng` are four single native letters written as Romanized digraphs.

### Apply stress mechanically

For a word with multiple syllables, the default stress falls on the penultimate syllable; the pronunciation tools print that stress in capitals for learning. `qaroshi` is `qa-RO-shi` /qa.ˈɾo.ʃi/; `gëro` is `GË-ro` /ˈɡə.ɾo/; `dërawa` is `dë-RA-wa` /də.ˈɾa.wa/. Hyphens marking cases or tense do not become audible interruptions. For long compounds, predict the broad citation pronunciation from the final word before adding emotional delivery.

## Four-pass pronunciation routine

1. **Segment:** find each native letter, using the longest of `sh/zh/kh/ng` where appropriate.
2. **Syllabify:** locate the six vowels and divide the word according to the standard `(C)(r/l/w/y)V(C)` pattern.
3. **Stress:** emphasize the penultimate syllable of a multisyllabic citation form.
4. **Read in context:** keep grammatical endings connected to their root and communicate the written resonance through an appropriate speaking style without treating it as a scientifically prescribed pitch pattern.

## Learning practice with reference sentences

| Qaroshi sentence | IPA | English |
|---|---|---|
| `më ti lësha.` | `/mə ti ˈlə.ʃa/` | You are cute. |
| `sen mi-na gëro dërawa.` | `/sen ˈmi.na ˈɡə.ɾo də.ˈɾa.wa/` | My throat is dry. |
| `sen mi kima-m këmë.` | `/sen mi ˈki.mam ˈkə.mə/` | I drink water. |

The examples isolate vowel quality, tapped `r`, and the absence of a present copula. Broad IPA is not a claim about an individual voice recording, and the exact syllable boundary of a cliticized phrase may vary in connected speech. More practice, including all 26 original glyphs, is in the [Pronunciation laboratory](deep_guides/pronunciation_lab.md).
''',
 'phonology_and_script.md':r'''

---

## Detailed transliteration algorithm

First determine whether the input is **Qaroshi Romanization** or a foreign language written with Latin letters. Only the former can be reliably mapped character-by-character to the 26 native glyphs. Normalize the text to NFC so that `ë` is represented consistently. Then scan left-to-right taking recognized digraphs `sh`, `zh`, `kh`, and `ng` as one letter before trying one-character graphemes. Preserve spaces and punctuation as layout marks, not as extra native letters. If a grapheme is not found, report or retain it visibly instead of silently replacing it with a supposedly “similar” sound.

### Romanization versus transcription

**Romanization** represents the written Qaroshi letter sequence in Latin-looking characters. **Phonemic transcription** uses IPA to represent intended sounds and normal stress. **Phonetic transcription** in the narrow sense would require details such as release, length, coarticulation, and local performance; the current standard does not assert those for each word. An English-style sound-out is neither a formal Romanization nor precise IPA. These labels should remain distinct on every learner-facing dictionary page.

### Words, suffixes and whitespace

`-na`, `-te` and related morpheme boundaries are included as hyphens in learner text because they help reveal grammar. They do not constitute extra native glyphs, and ordinary native writing may join them to the root. Whitespace still separates words. A sentence can be written in Romanized form and rendered as glyph images in the converter without reanalyzing the syntax; however, a graphic output is not equivalent to encoded editable plain text in an established native Unicode block.

### Text accessibility and export

When distributing native glyph screenshots or PNG exports, provide adjacent Romanization and the English translation where needed. This makes the content searchable, accessible to a screen reader, and inspectable for spelling. Store original PNG glyph assets with their original distinctions intact. In technical code or filenames, preserve the foreign string as an external quotation rather than mangling it into a near-sounding Qaroshi word. The [Native script handbook](deep_guides/writing_script.md) provides examples and an error checklist.
''',
 'wiki_usage.md':r'''

## Learning in the wiki, not just looking up words

The **Learn Qaroshi** sidebar section contains a staged sixteen-lesson course, sixteen topic manuals, twenty-one worked sentence parses, and a practice workbook. The best order is to begin with Start here and the Pronunciation laboratory, complete lessons 1–8, read the Nouns/Cases and Verb workshop guides, complete lessons 9–16, and finish with the workbook. Every practice answer is tied to an existing sentence in the canonical phrasebook, so a learner can inspect its original context and pronunciation on the corresponding phrase page.

The **Grammar** section remains normative: opening a grammar chapter now also shows links to relevant deeper guides. The **Dictionary** remains the reference for exact lexemes, suffix-like spellings, and Romanized pronunciation, and the original glyph converter is the place to check native writing. The deep guides explain and teach the standard; they do not add a second competing grammar.

### How to self-test

Hide the English column in a course lesson and translate Qaroshi from its IPA and written text. Next hide Qaroshi and reconstruct the entire sentence from English. Check the first resonance, each case suffix, predicate suffix, negation, and final `he` or `ya` before opening the answer key. The workbook's diagnosis questions contain deliberately **incorrect** forms for editing practice, which should not be copied as normal Qaroshi sentences.

### Finding your place on mobile

Open the menu button at the upper right. The same learning and grammar links are present in the mobile sidebar, and the sidebar closes after navigation. Long lesson tables are scrollable within their reading section where necessary; the page itself should not become wider than the viewport. The `/#learn` view is the index for all training materials and is readable offline.
'''
}
for name,txt in APPEND.items():
    p=d/name
    with p.open('a',encoding='utf8') as out:out.write(txt)
    print('expanded',name,len(p.read_text(encoding='utf8')))
