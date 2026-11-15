# Portable Qaroshi spelling and keyboard specification

Qaroshi native writing consists of 26 original Nardoragon letters, including a separate glyph for each of `sh`, `zh`, `kh`, and `ng`. Romanized `ë` is one vowel letter. The writing direction is left to right. A complete independent written sentence starts with one of the 16 obligatory resonance markers. In Romanized teaching texts, spaces separate words, the hyphen separates visible inflectional suffixes, commas signal clause boundaries, and `.?!` are ordinary portable punctuation, **not new native Qaroshi glyphs**.

## Reversible transliteration

Transliteration prioritizes the longest valid grapheme in this order: `sh`, `zh`, `kh`, `ng`, then one-letter elements. Text is Unicode NFC normalized; unknown Latin characters are passed through with an explicit warning in strict mode. The 26 user-provided glyph forms are supplied as PNG assets. **U+E000–U+E019 is a temporary private-use mapping, not a Unicode assignment**; unstyled PUA text is not portable. For exchanging text across devices, prefer Romanization until a stable interoperable font and mapping have been tested.

## Keyboard targets

- **Linux:** XKB draft source `keyboards/qaroshi.xkb`, requiring integration and OS testing.
- **Desktop/mobile:** portable Keyman `.kmn` draft source for subsequent compilation and target-specific installer packaging, *not yet verified in Keyman Developer*.
- **Browser:** original Studio on-screen glyph keyboard and the alphabet image work without a native IME.
- **Native font source:** `fonts/build_from_glyphs.py` builds a temporary-use typeface using the user's original PNG artwork on a local computer. Generated font binaries are deliberately not included in this package.

## Accessibility and final review

Before approval test right-to-left language contexts, search/copy/paste, selection, deletion across digraphs, IME behavior, screen reader labels, mobile landscape, high contrast, font scaling and fallback glyph handling. The native script is a living community decision; no official Unicode allocation or completed platform certification is claimed.
