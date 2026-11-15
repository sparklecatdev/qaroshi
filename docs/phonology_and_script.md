# Qaroshi Phonology and Native Script

The Qaroshi native alphabet has **26 symbols**, preserving the originally supplied Nardoragon handwritten character shapes. Romanization lists them in the source chart order:

`k a w t r q o d sh z u ë i g kh zh e ng h b p m s n y l`

Six vowels have the reference sound values `a /a/`, `e /e/`, `i /i/`, `o /o/`, `u /u/`, `ë /ə/`. Notable consonants: `q /q/`, `kh /x/`, `sh /ʃ/`, `zh /ʒ/`, `ng /ŋ/`, `y /j/`; `r` is typically tapped or rolled. Remaining consonants have their usual broad Latin phonetic value. Stress is generally penultimate: *qa-RO-shi*, *NA-ro*, *LË-sha*. The diaeresis on `ë` indicates a distinct vowel, not stress.

Standard syllables follow `(C)(r/l/w/y)V(C)` with common syllable-final `m,n,ng,r,l`. Short particles and expressive words permit other codas, including the register `rak`. Some consonant combinations arise where compound roots meet. Fast speech may contract identical adjacent vowels without changing spelling.

## One-to-one glyph mapping

The digraphs `sh`, `zh`, `kh`, `ng` are single native letters. Grapheme conversion therefore takes the longest matching letter first. Input `shazhakhng` is parsed `sh · a · zh · a · kh · ng`. A `sh` character is **not** an `s` followed by an `h` in standard Qaroshi orthography. The Romanized alphabet is therefore not a direct English-like character stream.

Each glyph is included in `assets/glyphs/<romanized-letter>.png`; the full source chart is `assets/alphabet_reference.png`. The `tools/qaroshi.py render` and offline dictionary converter compose those bitmaps into lines of native writing. This is a faithful letter-image renderer, **not a Unicode font or an official set of assigned code points**. The images may be resized for display, but their crossing strokes and characteristic loops should remain recognizable. Punctuation and Arabic digits are allowed as technical overlay characters, not native letters.

## Text encoding and transliteration

Use NFC-normalized UTF-8. Do not collapse `ë` into `e`; these may distinguish words and grammatical particles. Hyphens identify morpheme breaks in teaching text, and may be omitted in fluent native script. Spaces separate words; writing flows left to right, top to bottom. In an ASCII-only environment, a transport-specific reversible escape for `ë` may be adopted, but it must be labeled and decoded before lexical lookup. A lossless transport format can store the ordered array of 26 glyph names plus explicit spaces/punctuation.

## Example

`më pëla, ti sëna nu zëru ya, ko ti mi-wa sëna nëra-ki.`

The correct sentence-initial Warm Hum marker is **`më`**, not `meë` or `mê`. The native renderer represents each Qaroshi sound as its original handwritten glyph. Compound and inflection hyphens do not represent separate native signs.

## Priorities for native typography

A reusable keyboard font/IME would require selecting consistent stroke geometry, glyph advance widths, kerning and ligature handling, and legally usable character mapping. Neither a font nor keyboard layout is bundled in Standard 2.0. The immediate goals are legible native sample writing, reversible glyph ID encoding, and testing the readability of handwritten ligatures.
