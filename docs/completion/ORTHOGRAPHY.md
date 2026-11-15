# Native writing system interoperability and keyboard testing

The 26 original Nardoragon handwritten signs each correspond to one Qaroshi segment. The four Romanized digraphs `sh`, `zh`, `kh`, and `ng` each represent **one** native sign; ordinary Latin C, F, J, V and X are not additional native letters. Romanization remains the portable interchange spelling for mainstream Unicode systems.

The experimental font builder `tools/v8plus/build_font.py` produces a local TrueType file with **temporary Private Use Area** positions U+E000–U+E019, as documented in `fonts/mapping.json`. These positions are neither Unicode-standard assignments nor guaranteed to interoperate without the matching mapping/font.

For a build environment with the installed dependencies, run:

```bash
python tools/v8plus/build_font.py
python -m unittest discover -s tests -q
```

The shared archive includes source glyph art and the builder, not a compiled font. Browser visual rendering uses embedded or referenced image glyphs. The experimental XKB map is `keyboards/qaroshi.xkb`; the Keyman source is `keyboards/keyman/qaroshi_provisional.kmn`. A source file alone does **not** prove that a keyboard installs correctly on any particular OS. Never overwrite a user's system keyboard configuration without their informed consent.

A native keyboard release should be tested for letter order, four digraphs, Unicode normalization, composing marks, punctuation, numbers, input focus, accessibility, and recovery without the native font. Preserve a Romanized fallback for copy/paste, search, and cross-device communication.

The punctuation, capitalization, line wrapping, and native-script hyphen behavior require explicit editorial decisions and sample text before permanent standardization.
