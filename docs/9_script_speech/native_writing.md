# Native writing and experimental typeface

Qaroshi has 26 native glyphs, written left to right with spaces between words. Its Romanization is not English A–Z: `sh`, `zh`, `kh`, `ng` are **single native letters**, and `ë` differs from `e`. Letter order: `k a w t r q o d sh z u ë i g kh zh e ng h b p m s n y l`.

The bundled experimental outline font maps the 26 signs to **U+E000 through U+E019**, temporary Unicode Private Use Area assignments. This permits practical typing in the Study Studio but is **not an official Unicode encoding**. Plain PUA text may display incorrectly without the accompanying font and mapping. Always preserve Romanized text as a searchable/accessibility companion.

Use NFC normalization, match digraphs greedily, and strip educational morpheme hyphens only for native glyph display. Periods, question marks, commas, quotation marks, numbers and URLs may appear as technical overlays, not newly invented native glyphs. `he` remains obligatory in full questions and `ya` in commands even when punctuation is printed.

The font is traced from the original handwritten glyph artwork. Strokes, hinting, spacing and platform keyboard integration remain experimental. The on-screen keyboard works in browsers and on touchscreens. Native Windows, macOS, Android and iOS keyboard installers require separate platform testing.
