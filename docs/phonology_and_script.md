# Qaroshi Phonology and Native Script

The Qaroshi native alphabet has **26 symbols**, preserving the originally supplied Nardoragon handwritten character shapes. Romanization lists them in the source chart order:

`k a w t r q o d sh z u ë i g kh zh e ng h b p m s n y l`

Six vowels have the reference sound values `a /a/`, `e /e/`, `i /i/`, `o /o/`, `u /u/`, `ë /ə/`. Notable consonants: `q /q/`, `kh /x/`, `sh /ʃ/`, `zh /ʒ/`, `ng /ŋ/`, `y /j/`; `r` is typically tapped or rolled. Remaining consonants have their usual broad Latin phonetic value. Stress is generally penultimate: *qa-RO-shi*, *NA-ro*, *LË-sha*. The diaeresis on `ë` indicates a distinct vowel, not stress.

Standard syllables follow `(C)(r/l/w/y)V(C)` with common syllable-final `m,n,ng,r,l`. Short particles and expressive words permit other codas, including the register `rak`. Some consonant combinations arise where compound roots meet. Fast speech may contract identical adjacent vowels without changing spelling.

## Morphological boundaries and compound pronunciation · amendment 27

A root, a compound join and a grammatical suffix remain analytically separable, whether or not a speaker realizes a rapid-speech vowel coalescence. The **dictionary form never loses a vowel** because two component vowels happen to meet. The four official digraphs (`sh`, `zh`, `kh`, `ng`) are single graphemes in the established spelling, but **a learner must not infer compound components simply from an English-looking letter split**. Look up the documented compound decomposition and use hyphens or centered dots only in **teaching analyses** to expose a boundary. Those segmentation marks are not new native letters or alternate canonical spellings. The original 26-letter inventory and default penultimate citation stress are unchanged; no new mandatory assimilation or speaker-recorded allophone is claimed.

## One-to-one glyph mapping

The digraphs `sh`, `zh`, `kh`, `ng` are single native letters. Grapheme conversion therefore takes the longest matching letter first. Input `shazhakhng` is parsed `sh · a · zh · a · kh · ng`. A `sh` character is **not** an `s` followed by an `h` in standard Qaroshi orthography. The Romanized alphabet is therefore not a direct English-like character stream.

Each glyph is included in `assets/glyphs/<romanized-letter>.png`; the full source chart is `assets/alphabet_reference.png`. The the offline wiki script converter and offline dictionary converter compose those bitmaps into lines of native writing. This is a faithful letter-image renderer, **not a Unicode font or an official set of assigned code points**. The images may be resized for display, but their crossing strokes and characteristic loops should remain recognizable. Punctuation and Arabic digits are allowed as technical overlay characters, not native letters.

## Text encoding and transliteration

Use NFC-normalized UTF-8. Do not collapse `ë` into `e`; these may distinguish words and grammatical particles. Hyphens identify morpheme breaks in teaching text, and may be omitted in fluent native script. Spaces separate words; writing flows left to right, top to bottom. In an ASCII-only environment, a transport-specific reversible escape for `ë` may be adopted, but it must be labeled and decoded before lexical lookup. A lossless transport format can store the ordered array of 26 glyph names plus explicit spaces/punctuation.

## Example

`më pëla, ti sëna nu zëru ya, ko ti mi-wa sëna nëra-ki.`

The correct sentence-initial Warm Hum marker is **`më`**, not `meë` or `mê`. The native renderer represents each Qaroshi sound as its original handwritten glyph. Compound and inflection hyphens do not represent separate native signs.

## Priorities for native typography

A reusable keyboard font/IME would require selecting consistent stroke geometry, glyph advance widths, kerning and ligature handling, and legally usable character mapping. Neither a font nor keyboard layout is bundled in Standard 2.0. The immediate goals are legible native sample writing, reversible glyph ID encoding, and testing the readability of handwritten ligatures.

## Complete IPA lookup and sentence pronunciation

The full sound-value table, stress and syllabification conventions, and examples are in **[Pronunciation and IPA](pronunciation.md)**. Every entry in `data/lexicon.csv` has `ipa` and `reading` fields; every row in `corpus/parallel_sentences.csv` has corresponding sentence fields. The offline wiki includes live IPA transcription in the native writing converter.


---

## Detailed transliteration algorithm

First determine whether the input is **Qaroshi Romanization** or a foreign language written with Latin letters. Only the former can be reliably mapped character-by-character to the 26 native glyphs. Normalize the text to NFC so that `ë` is represented consistently. Then scan left-to-right taking recognized digraphs `sh`, `zh`, `kh`, and `ng` as one letter before trying one-character graphemes. Preserve spaces and punctuation as layout marks, not as extra native letters. If a grapheme is not found, report or retain it visibly instead of silently replacing it with a supposedly “similar” sound.

### Romanization versus transcription

**Romanization** represents the written Qaroshi letter sequence in Latin-looking characters. **Phonemic transcription** uses IPA to represent intended sounds and normal stress. **Phonetic transcription** in the narrow sense would require details such as release, length, coarticulation, and local performance; the current standard does not assert those for each word. An English-style sound-out is neither a formal Romanization nor precise IPA. These labels should remain distinct on every learner-facing dictionary page.

### Words, suffixes and whitespace

`-na`, `-te` and related morpheme boundaries are included as hyphens in learner text because they help reveal grammar. They do not constitute extra native glyphs, and ordinary native writing may join them to the root. Whitespace still separates words. A sentence can be written in Romanized form and rendered as glyph images in the converter without reanalyzing the syntax; however, a graphic output is not equivalent to encoded editable plain text in an established native Unicode block.

### Text accessibility and export

When distributing native glyph screenshots or PNG exports, provide adjacent Romanization and the English translation where needed. This makes the content searchable, accessible to a screen reader, and inspectable for spelling. Store original PNG glyph assets with their original distinctions intact. In technical code or filenames, preserve the foreign string as an external quotation rather than mangling it into a near-sounding Qaroshi word. The [Native script handbook](deep_guides/writing_script.md) provides examples and an error checklist.
