# Local tests and execution limits

- Canonical lexicon count: **30,000**.
- Review worksheets: **1,000** idiom candidates and **5,000** source-linked sense cards, all structural checks passed.
- New separately authored dialog scenes: **12 / 96 turns**, all structural checks passed.
- New editorial readings: **5 / 50 sentences**, all structural checks passed.
- Grammar contrast mastery bank: **94** minimal-pair items.
- Human recording collection targets: **3,000**. Actual human recordings in this release: **0**.
- Python tests: **214** after compiled-font source test, as of this release.
- JavaScript: extracted from the embedded HTML and passed Node `--check` syntax validation.
- Browser interaction testing of the new Completion Workbench was **blocked** by the managed Chromium URL policy in this environment. The UI is a testable implementation; do not claim end-to-end browser verification on a real device.

## Commands

```bash
python tools/v8plus/build_font.py
python tools/fluency2026/audit_review.py
python tools/fluency2026/build_editorial_scenes.py
python tools/fluency2026/build_new_literature.py
python tools/completion/build_workbench.py
python -m unittest discover -s tests -q
python tools/fluency2026/bilingual_demo.py 'My throat is dry.'
python tools/fluency2026/analyzer2.py 'më mi ti-m nashi.' --pretty
```

The native font binary is a **local build output**, not included in the distribution. To validate the app manually, open `Qaroshi_Completion_Workbench.html` in a normal browser and check the sidebar, text search, mastery practice feedback, dialogue reveals, local review persistence, glyph rendering, JSON backup/restore, and microphone permission handling.
