# Qaroshi 14.0: Language Consistency checkpoint

**Date:** 2026-11-15  
**Status:** Tested local source ZIP, editorial review tooling, **not a ratified linguistic standard**. The full 401-file distribution has **not** been uploaded to this branch.

## Scope and results

The 14.0 local release preserves the previous 30,000 dictionary entries, 4,383 reference examples, 90 grammar chapters, original 26 glyph images and 16 obligatory written resonance markers byte-for-byte. It records SHA-256 digests for 29 canonical source files.

- **689** prior editorial source sentences screened; **103** legacy translation-risk rows retained in an editable review queue.
- The 103 rows have **28 high**, **7 medium**, and **68 low** priority review classifications. High priority means further semantic attention is warranted, **not** that the passage is demonstrably wrong.
- **28** manually drafted standalone-English correction proposals, plus **14** additional grammar-engine interpretation suggestions; total **42 unapproved translation proposals**.
- **115** source-string groups with different contextual English translations. These are differences for review, not automatically contradictions.
- Full priority/action queues for **1,000** earlier idiom candidates (440 high, 14 medium, 546 low) and **5,000** sense cards (4,079 high, 712 medium, 209 low). No new conventional idiom or independently verified sense has been claimed.
- **20** explicit grammatical/semantic interpretation decisions and **20** executable rule categories. **442** newly checked positive/negative morphology regressions.
- A new standalone responsive **Semantic Workbench** with review queues, risk explanations, meaning cues, rulebook, a limited browser grammar-check preview, local editorial decisions, JSON export/import and dark/mobile mode.
- **759 Python tests** pass in the build with local optional font; **759 run with one font-dependent skip** on fresh extraction. **27 desktop/mobile Chromium interaction checks** pass with zero page errors.
- The **401-file ZIP** passed archive CRC checking and a fresh extraction test. Font binaries are intentionally excluded.

## Examples needing contextual review

- Source `qor mi nënayaro ti-wa nëra-yu.` explicitly means staying **with you**, while one English contextual line says **with them**.
- Source `sen mi shima-m pëmi-yu.` expresses an unqualified future book purchase, but one contextual English reading adds “Possibly” and another intention.
- Some `-ki` ability, `-ho` permission and `si` direct-observation features were paraphrased without those overt distinctions.

These are annotated proposals, not silent rewrites of original documents.

## What remains

Independent translation adjudication of 103 flagged rows; actual speaker/community review of the 1,000 idioms and 5,000 sense cards; extensive testing of nested scope, quotation and argument structures; general semantic parsing; and full publication/merge of the source ZIP. Structural checks do **not** establish cultural naturalness.

The source package includes `tools/v14/semantic_validator.py`, `tools/v14/build_audit.py`, `tools/v14/build_regression.py`, `tests/test_standard14.py`, `data/v14/` reports, and `Qaroshi_14_Semantic_Workbench.html`. The branch only contains this checkpoint and earlier development documentation so far.

**Please retain Draft status** until human review and a reproducible full-source GitHub upload are completed.