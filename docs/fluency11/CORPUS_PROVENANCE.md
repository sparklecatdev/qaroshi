# Qaroshi 11: Independently scripted editorial conversation corpus

The project already includes 1,000 **controlled variants of a teaching-dialogue arc** totaling more than 100,000 Qaroshi tokens. Those variants are valuable for grammatical drills but should not be described as 1,000 independently written spontaneous conversations.

This release adds a **separate** corpus (`corpus/original11/`) of **49 distinct situation scripts**, **294 turns**, and **1,263 Qaroshi tokens** under the source tokenizer. The scripts were individually drafted around different problems and outcomes: permission to fly, deciding not to leave, a missing message, first-hand versus reported evidence, books and learning, asking for rest or privacy, care without promises of forever, repair requests, trust after misunderstandings, stars, shelter, grief, and boundaries. These are *separately authored editorial teaching texts*, not recordings or transcriptions of spontaneous speakers.

Each script has a stable ID, title, situation premise, individual speakers, Qaroshi text, an *editorial contextual English reading*, a separately generated literal/reference interpretation, IPA, and an English-friendly sound-out guide. Literal readings can diverge from contextual paraphrases; they are stored in different fields, not silently merged. Every word form passes lexicon/affix checks; every new turn has a licensed controlled interpretation in the current engine. This **does not** prove idiomaticity, narrative naturalness, or social acceptance.

### Next corpus milestone

A fully reviewed corpus should collect at least 1,000 *independently authored* coherent conversations, along with diverse connected texts (long-form fiction, tutorials, interpersonal dialogue, legal and technical discussions, humor, arguments, cultural tales and everyday messages). Each submission should distinguish independent authoring from procedural substitution. For authentic speech, obtain consent and provenance. Maintain stable sentence identifiers, flags for grammatical disputes, explicit translation alternatives, and a systematic corpus size report.

### Rebuild

```bash
python tools/fluency11/build_original_dialogues.py
python tools/fluency11/build_curriculum.py
```

No new corpus text was added to the original immutable 4,383-example baseline file. The original native glyphs and 16 written resonance markers remain unchanged.
