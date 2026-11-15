# Qaroshi pronunciation and IPA

**Reference 4.3.1 · applies to every dictionary word and phrasebook entry**

Every one of the 11,878 dictionary entries and 2,017 example sentences has three visible pronunciation fields:

- **IPA**: a phonemic transcription between slashes, for example `qaroshi` **/qa.ˈɾo.ʃi/**. This is the sound-level reference, not an English approximation.
- **English-style sound-out**: approximate phonetic spelling with the stressed syllable capitalized, for example `gëro` = **GUH-roh** and `qaroshi` = **qah-ROH-shee**. Approximate spellings are not substitutes for the precise IPA; e, o, q, kh, and tapped r require the letter-by-letter notes.
- **Reading guide**: Romanized syllables separated by hyphens, with the stressed syllable in CAPITAL LETTERS, for example **qa-RO-shi**. A one-syllable word is not capitalized.

The dictionary displays all three fields, with the English sound-out first, and gives a Latin-sound breakdown beneath each individual word article. These are phoneme sounds, not English letter names. The dictionary displays pronunciation, including on individual word pages. Core case, verb and derivational suffixes have matching pronunciation entries in `data/affixes.json`. The phrasebook displays full-sentence IPA, and the native-script converter generates both forms for typed Qaroshi. IPA is also shown beside identifiable Qaroshi examples in grammar articles. Both fields are searchable in the wiki.

## The six vowels

| Native letter | IPA | Articulation |
|---|---|---|
| `a` | /a/ | Open central/front unrounded vowel, a full open *ah* sound |
| `e` | /e/ | Mid-high front unrounded vowel, pure monophthong, not an English diphthong |
| `i` | /i/ | Close front unrounded vowel |
| `o` | /o/ | Mid-high back rounded vowel, pure monophthong |
| `u` | /u/ | Close back rounded vowel |
| `ë` | /ə/ | Central unstressed-sounding schwa; this vowel **can** carry word stress |

All six vowels remain distinct in careful speech, regardless of stress. Unlike the English letter *e*, written `ë` is a separate Qaroshi letter.

## The twenty consonants

| Romanization | IPA | Pronunciation note |
|---|---|---|
| `b` | /b/ | Voiced bilabial stop |
| `d` | /d/ | Voiced alveolar stop |
| `g` | /ɡ/ | Voiced velar stop, always hard |
| `h` | /h/ | Glottal fricative |
| `k` | /k/ | Voiceless velar stop |
| `kh` | /x/ | Voiceless velar fricative, as in Scottish *loch* |
| `l` | /l/ | Lateral approximant |
| `m` | /m/ | Bilabial nasal |
| `n` | /n/ | Alveolar nasal |
| `ng` | /ŋ/ | Velar nasal, as in *sing*, no added /g/ |
| `p` | /p/ | Voiceless bilabial stop |
| `q` | /q/ | Voiceless uvular stop, articulated farther back than /k/ |
| `r` | /ɾ/ | Single tap in this broad IPA style; a rolled [r] is possible in deliberate or expressive speech |
| `s` | /s/ | Voiceless alveolar fricative |
| `sh` | /ʃ/ | As in *ship* |
| `t` | /t/ | Voiceless alveolar stop |
| `w` | /w/ | Labial-velar approximant |
| `y` | /j/ | Consonant at the beginning of English *yes*, not a vowel |
| `z` | /z/ | Voiced alveolar fricative |
| `zh` | /ʒ/ | As in *measure* |

**Important:** `kh`, `ng`, `sh`, and `zh` are four single letters in native Qaroshi. They do not count as two consecutive consonants when determining syllables or stress.

## Syllabification and stress

1. The reference expects one syllable per vowel occurrence. Adjacent vowels are treated as separate syllables unless a documented lexical exception overrides the rule.
2. In between vowels, a legal complex onset of consonant plus `r`, `l`, `w`, or `y` is kept together. Otherwise the next syllable begins with the last intervening consonant. The rest of the cluster closes the preceding syllable.
3. Primary stress falls on the **penultimate syllable** when a word has two or more syllables. One-syllable function words have no written stress mark in the broad IPA field.
4. Hyphens are morphological teaching punctuation, not automatic pauses or stresses. A suffix can move the stress of the full word.
5. Sentence IPA transcribes each word, retaining commas as optional pause cues. Final `.`, `!`, `?` are not pronunciation segments, so they are omitted from the IPA field.

The IPA uses a dot `.` for a **syllable boundary**, and `ˈ` immediately before the **stressed syllable**. For example:

| Qaroshi | IPA | Stress guide | English |
|---|---|---|---|
| `qaroshi` | /qa.ˈɾo.ʃi/ | qa-RO-shi | Qaroshi language |
| `më` | /mə/ | më | Warm Hum marker |
| `lësha` | /ˈlə.ʃa/ | LË-sha | cute |
| `gëro` | /ˈɡə.ɾo/ | GË-ro | throat |
| `dërawa` | /də.ˈɾa.wa/ | dë-RA-wa | dry |
| `khura` | /ˈxu.ɾa/ | KHU-ra | wind |
| `mi-na` | /ˈmi.na/ | MI-na | my |
| `daru-yu` | /da.ˈɾu.ju/ | da-RU-yu | will protect |

## Whole-sentence examples

**My throat is dry** (neutral):

- Qaroshi: `sen mi-na gëro dërawa.`
- IPA: **/sen ˈmi.na ˈɡə.ɾo də.ˈɾa.wa/**
- Stress guide: **sen MI-na GË-ro dë-RA-wa.**

**You are cute** (Warm Hum):

- Qaroshi: `më ti lësha.`
- IPA: **/mə ti ˈlə.ʃa/**
- Stress guide: **më ti LË-sha.**

**Please never die so you can stay with me forever** (Warm Hum):

- Qaroshi: `më pëla, ti sëna nu zëru ya, ko ti mi-wa sëna nëra-ki.`
- IPA: **/mə ˈpə.la, ti ˈsə.na nu ˈzə.ɾu ja, ko ti ˈmi.wa ˈsə.na nə.ˈɾa.ki/**
- Stress guide: **më PË-la, ti SË-na nu ZË-ru ya, ko ti MI-wa SË-na në-RA-ki.**

## Rhythm, resonance, and pronunciation

Resonance markers are **written words**, with their own ordinary sounds, not hidden phonetic annotations. `më`, `zha`, `qor`, and the other 13 core registers are pronounced as transcribed in the dictionary. A resonance marker can change the *delivery* of a sentence (warm humming, bright trilling, solemn depth) without changing the segmental phonemic IPA. This means that the phonemic transcription records lexical sounds, while expressive register describes social intention separately.

The reference does not claim to capture speaking rate, pitch, individual vocal anatomy, dialect variation, or every coarticulatory adjustment. For teaching and searching, it uses a predictable **broad citation pronunciation** rather than inventing ultra-precise acoustic detail.

## Limitations and technical use

- IPA values are generated from established letter-to-sound and stress conventions. They are **not audio recordings**, nor empirical descriptions of every community variant.
- English-like pronunciation guides are necessarily imperfect for `q` /q/, `kh` /x/, and pure `e` /e/ and `o` /o/. Prefer the IPA and articulation descriptions for these.
- The reference currently has no native-speaker-validated exception lexicon for non-default stress. This can be added without changing the underlying spelling.
- Programmatic transcription: `python tools/phonetics.py "më ti lësha."`; refresh the full dictionary fields via `python tools/add_pronunciations.py`.
- The HTML wiki runs offline and transcribes typed Romanized text locally. No speech synthesis or audio service is required.

## The ordinary Latin A–Z alphabet

For **all 26 Latin letters**, American English letter names, their IPA, and the distinction from Qaroshi Romanization, see [Latin A–Z phonetics](latin_alphabet.md). The wiki includes an A–Z lookup and a tool to pronounce *spelled-out English letters*, not the natural pronunciation of full English words.
