# Qaroshi Academy · Learner's guide

Qaroshi Academy is the practical learning companion to the Unified Standard Reference. It is a self-contained, offline HTML application with a lesson-based learning route, eight game modes, a ten-step Skyflight challenge, and spaced word review. The original wiki remains the definitive reference for detailed morphology, native writing and complete dictionary articles.

## Getting started

1. Open `Qaroshi_Academy.html` in a browser. It requires no installation, network connection, login or external libraries.
2. Choose **Guided course** to follow lessons 01 through 16. Each lesson includes ten *existing* dictionary/corpus-backed sentences, IPA and sound-out guides, a complete source lesson, and a five-question comprehension check.
3. Answer at least four of the five lesson questions correctly to mark it complete. Lessons are never locked.
4. Use **Practice games** to drill a specific skill. Every answer reveals the correct form and an explanation; there are no timers.
5. The **Skyflight challenge** mixes ten exercises in one short game. The three hearts are a low-stakes progress indicator, not a gate: losing them does not block the remaining questions.
6. Use **Review words** to revisit vocabulary previously encountered or saved. Words return on increasingly spaced intervals after successful retrieval.
7. Visit **Word explorer** to look through all 16,732 dictionary headwords/compounds, see native script and IPA, and add words to review.
8. Use **Deep guides** for the 16 unabridged topical manuals, or **Open full Qaroshi Wiki** for the original reference and all 70 grammar chapters.

## Game modes

| Mode | Task | Teaches |
| --- | --- | --- |
| Word meanings | Pick English meaning from Qaroshi | Recognition, semantic precision |
| Recall the word | Find Qaroshi from English | Retrieval, distinguishing near-neighbors |
| Sentence senses | Translate an authentic reference example | Clause meaning, pragmatic interpretation |
| Grammar endings | Identify a productive suffix | Cases, tense, aspect, voice and modality |
| Resonance radar | Choose the correct mandatory sentence marker | Sixteen written resonance registers |
| Script decoder | Decode the original Nardoragon glyph sequence | Script literacy, Romanization |
| Sentence forge | Tap shuffled words into Qaroshi order | Resonance + SOV + suffix placement |
| Sound lab | Match broad IPA to a Qaroshi word | Consonants, vowels, stress |

## Pronunciation

All exercises show broad IPA and the simplified English-style sound-out **after** the learner answers. The sound-out is approximate and does not replace IPA. Qaroshi's original glyphs are drawn from the 26 source images; sh, zh, kh and ng each represent one native letter. These games do not synthesize recorded Nardoragon speech.

## Review scheduling and privacy

Word practice uses a simple escalating interval schedule (1, 2, 4, 8, 16, 30, 60 days for consecutive correct recalls), with errors returning items immediately. This is a lightweight review algorithm, not a guarantee of recall or a diagnostic of proficiency.

Progress includes lessons completed, practice answers, correct answers, XP and per-word due dates. It is saved with browser `localStorage` when permitted. Choose **My progress → Export progress** to download a portable JSON backup; **Import progress** restores it. No remote server receives the data. Some browsers restrict storage for `file://` pages and private sessions; export a backup after study if reliable persistence matters.

## Source fidelity and limitations

- Academy 5.2 includes the **exact 16,732 lexicon records** and **3,077 example sentences** from Reference 5.1. It does not introduce new words, morphological rules or idioms.
- All 16 course lessons and 16 deep guides are embedded from the documented source files. It does not invent its own lesson translations.
- Multiple-choice exercises are generated from source-backed examples and dictionary meanings. They assess recognition of selected canonical glosses, not every possible idiomatic paraphrase.
- The word-order minigame tests a **specific documented reference sentence**. Other grammatical Qaroshi arrangements could be possible in a different context; the game labels the target as one model sentence rather than claiming it is the only grammatical wording.
- Reviews and XP are motivational learning aids, not fluency certification.
- The HTML application works without internet. The wiki link expects `Qaroshi_Wiki.html` to be in the same directory; extract the ZIP to preserve this pairing.

## Developer notes

The source UI lives in `web/academy/academy.css` and `web/academy/academy.js`. `tools/build_academy.py` deterministically assembles the standalone HTML by embedding the dictionary, corpus, lessons, deep guides, resonance table, affix inventory and 26 glyph images. Rebuild with:

```sh
python tools/build_academy.py
python -m unittest discover -s tests -v
# Optional interactive browser verification, when Playwright and Chromium are installed:
python tools/academy_smoke.py
```

No external dependencies are needed to **run** Academy in a browser. Regeneration requires Python and `mistune` as specified by the package requirements.
