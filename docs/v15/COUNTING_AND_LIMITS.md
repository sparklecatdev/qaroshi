# Exact counts, editorial limitations and reproduction

## Counting

Only whitespace-separated tokens in Qaroshi source sentences are counted. English translations, titles, IPA, punctuation-only fields and metadata are excluded. An editorial **piece** is a separately drafted conversation or prose text with a title, genre and premise. A distinct *sentence surface* is the identical normalized spelling of a Qaroshi sentence; repeated everyday greetings can appear in many independently drafted scenes and must not be presented as distinct lexical constructions.

For an independent editorial library we include: 49 release-11 dialogues, 54 release-12 dialogues, 73 newly written release-15 dialogues, 18 release-12 prose texts, 5 release-13 short readings and 12 release-15 prose texts. In total: 176 dialogues, 35 prose texts, 1,594 aligned utterances and 6,828 Qaroshi whitespace tokens. This is editorial development text, not independently validated natural speech. The large controlled-dialogue drill collection is stored elsewhere but excluded.

## Quality limitations

- New 15.0 work contains 561 sentence occurrences and 312 exact unique sentence strings; **347 occurrences belong to repeated-sentence groups**.
- 48 new exact Qaroshi sentences have more than one contextual English interpretation; 223 such groups exist cumulatively. Some are reasonable situational paraphrases, some may be erroneous. None has been automatically labelled wrong.
- A passing morphological screen confirms no *recognized* surface-rule violation. It cannot establish idiomatic word choice, complex scope, social meaning or historical usage.
- The 15.0 texts are original editorial constructions with multiple social purposes and a range of topics, but have **zero speaker attestations or independent semantic approvals**.
- The previous 123,000-token practice-dialogue inventory is not an independently authored naturalistic 100,000-word corpus. It is not counted toward this milestone.

## Inputs and exact outputs

`tools/v15/build_corpus.py` parses the original authored scene and prose files into a reproducible JSON corpus, CSV and Markdown reader with sentence IPA, approximate sound-out and v14 rule IDs. `tools/v15/build_browser.py` integrates all source-backed prior original editorial releases and produces `Qaroshi_15_Corpus_Library.html`, `full_editorial_parallel.csv`, `editorial_piece_catalog.csv`, `all_editorial_qaroshi_only.txt` and cumulative metrics. `tools/v15/quality_audit.py` measures form repetition and translation variation without inventing editorial decisions.

## Review expectations

A contributor reviewing a passage should check the meaning independently from its English gloss; parse tense, case, modality, evidence and reference; highlight all ambiguous readings; and record the adjudicated interpretation separately. Speaker recordings require informed consent and a license. Cultural/religious/regional dialect claims must not be asserted without sources.
