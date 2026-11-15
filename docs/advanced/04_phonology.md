# Phonology beyond the dictionary: fluent pronunciation, stress and rhythm

The 26 native written signs map to six vowels and twenty consonants. The four Romanized sequences `sh`, `zh`, `kh`, `ng` each represent **one native letter**, not two. The transcription system in this reference is *broad phonemic IPA*; it encodes the distinctions needed to identify words, not every possible accent or physical realization.

## 1. The phonemic inventory and articulation

Vowels: `/a e i o u ə/`, written `a e i o u ë`. The five noncentral vowels are relatively stable; `ë` is a mid-central schwa. Consonant contrasts include `/q/` a uvular voiceless stop distinct from `/k/`; `/x/` a velar fricative (`kh`), `/ɾ/` a tap (`r`); `/ŋ/` a velar nasal (`ng`), `/ʃ/` (`sh`), and `/ʒ/` (`zh`). Other consonants are read through the existing inventory. English-style sound-outs are approximate because English does not exactly match `/q/`, the tap `/ɾ/`, or monophthong `/e o/`.

`qaro` /ˈqa.ɾo/ (Nardoragon) should not be written as English `kwaro`. `qaroshi` /qa.ˈɾo.ʃi/ has three syllables. `gëro` /ˈɡə.ɾo/ = throat; `dërawa` /də.ˈɾa.wa/ = dry. `khura` /ˈxu.ɾa/ = air/breath. The spelling `më` is a single syllable `/mə/`, not `meë`.

## 2. Syllabification

The reference pronunciation converter uses a greedy grapheme analysis followed by syllable division that maximizes permissible medial onsets. A permitted two-consonant medial onset may end in `r`, `l`, `w`, or `y` when the preceding consonant is not itself a glide. Other clusters split with at least the final consonant beginning the next syllable. Adjacent vowels belong to separate syllables (hiatus); do not insert an unmarked English diphthong. A written hyphen marks morphology, not an extra sound.

## 3. Stress

Ordinary lexical stress is **penultimate**: `gëro` /ˈɡə.ɾo/, `qaroshi` /qa.ˈɾo.ʃi/. Monosyllables need no lexical-stress marker. Regular suffixation can change the phonological word's syllable count, thus shifting the surface penultimate stress. The dictionary shows the syllabification **of each listed word**, not necessarily every potential speech-rate contraction of a sentence. Strong rhetorical emphasis may add phrasal prominence on a contrasted word without changing its dictionary IPA.

## 4. Prosodic phrases

A whole sentence naturally has a **prosodic contour**: stronger prominence toward a focused predicate or contrast, and a final boundary cue. Statements typically decline in pitch toward a pause; real questions can rise or have other contours; imperatives may be sharper. This is a **pedagogical description**, not a mandated sound file or a proven inventory of tonal phonemes. Typed resonance supplies the register independently of melody. A `hë` seeking-call question and a `khar` alarmed question share `he` but differ in stance.

## 5. Word boundaries in fluent speech

Written word boundaries and syllable boundaries are different. A speaker may reduce pauses between frequently adjacent words or attach a weak grammatical particle prosodically to a neighboring word. In written IPA provided by the dictionary, each full word retains its own phonemic form and stress conventions. Do **not** silently delete a vowel or consonant in machine-generated IPA merely because the phrase is spoken quickly: no sound law in the standard authorizes that deletion across all registers.

For transcription of actual recordings, annotate observed boundary reduction on a **second narrow-phonetic layer** if evidence exists. Do not replace standardized dictionary pronunciations with speculation about natural connected speech.

## 6. Coarticulation and allophony (non-contrastive expectations)

At faster speaking rates, place of articulation can be influenced by neighboring sounds. For example a nasal adjacent to a velar consonant may become more velar, and an alveolar consonant before a palatal sound may shift slightly. These are plausible phonetic tendencies and **not currently standard obligatory sound changes**. They should be labeled potential allophony, not separate dictionary phonemes or alternate Romanized spelling rules. `/q/` and `/k/` remain meaningfully distinct, as do `/s/` and `/ʃ/` and `/z/` and `/ʒ/`.

## 7. Rhythm and typed resonance

`më`, `zha`, and `qor` are real pronounceable words with normal segmental forms; their social meaning also affects how a sentence is naturally delivered. A Warm Hum is often voiced gently, while Deep Resonance is more sustained. They **do not introduce extra vowels** or change the phonemes of every following word. In text, the resonance marker is obligatory even in contexts with no audio or vocal performance.

## 8. Sandhi and why the standard is conservative

The term *sandhi* refers to systematic sound changes at word boundaries. Qaroshi 7.0 does **not** prescribe a universal sandhi rule without speaker recordings or a sufficient contrastive corpus. Instead, this chapter specifies a conservative formal reading: full underlying vowels remain audible, each word is pronounceable from its standalone phonemic entry, and suffixes are interpreted as part of the phonological word. A later descriptive dialect study may document reductions; they should not retroactively falsify the existing 30,000 broad IPA fields.

## 9. Phonotactic diagnostics

An editorial new form must segment into the 26 established signs. `sh` is recognized before `s+h`, `kh` before `k+h`, and `ng` before `n+g`. A proposed borrowed form with a non-inventory symbol is either transliterated using existing phonemes, flagged as an unassimilated foreign quotation, or left in source orthography with a gloss. It does not gain a native glyph by assumption. If a new compound would create a difficult medial cluster, a hyphenated teaching spelling can clarify the morphological boundary without adding a phoneme.

## 10. Pronunciation practice and minimal contrasts

Practice the articulatory **contrast** rather than memorizing English spellings: `/k/` vs `/q/` (front velar versus farther-back uvular closure); `/k/` vs `/x/` (stop versus fricative); `/s/` vs `/ʃ/` (alveolar versus postalveolar frication); `/z/` vs `/ʒ/` (voiced alveolar versus voiced postalveolar); `/n/` vs `/ŋ/` (front nasal versus velar nasal); `/ɾ/` vs English approximated `r` (one tongue tap versus continuous approximant); `/e/` vs `/ə/` (front vowel versus central schwa).

The drills in `data/phonology/drills.json` use existing words when a reliable matched pair is available, and otherwise test sound identification without claiming two unattested words form a lexical minimal pair.

## 11. Recording protocol

For future audio validation, record **the same sentence** at slow, conversational and emphatic rates, without changing its typed marker. Preserve a consistent microphone and speaker. Annotate source, word-by-word alignment, IPA deviations, stress shift, perceived register and confidence. One speaker's reduction does not establish universal dialect phonology. Archive raw recordings only with appropriate speaker consent.

## 12. Limits

This edition provides a stronger phonological theory and practice protocol, not an acoustic corpus. It would be misleading to promise exact sound playback for a language whose recorded speaker corpus has not been supplied. The embedded IPA remains reproducible and deterministic; the “English sound-out” remains a learning aid, not a second orthographic standard.
