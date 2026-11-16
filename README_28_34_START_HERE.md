# Qaroshi 28–34 · Language reform, not another app

The authoritative adopted rules for this phase are in **[docs/language_reform_28_34.md](docs/language_reform_28_34.md)**. This is an amendment to the original 90-chapter Standard 7.0 grammar and the preceding 24–27 amendment. It is intentionally source-only: no new website, chatbot, dashboard or generated dictionary padding.

## The essential new word

`nëgëra` /nə.ˈɡə.ɾa/ is an adopted, **new post-7.0 determiner** for *not every / not all*, placed immediately before a quantified subject noun. `sen nëgëra qaro goro.` means **at least one Nardoragon does not fly**; it makes no claim that any others do. Existing `ngënao qaro nu goro` means **no Nardoragon flies**. Source grammar resonance is still required for complete written sentences.

The frozen 30,000-word base lexicon and its 29 SHA-256 reference hashes were not rewritten. The **new edition adds one formally editioned word in an overlay**, so the effective edition-specific inventory is **30,001**, not a false claim that the old `data/lexicon.csv` suddenly contains 30,001 records.

## Seven coordinated language updates

| Chapter | Source | Status |
| --- | --- | --- |
| 28, Core semantics | `data/v28_34/core_semantic_index_800.csv`, `meaning_boundaries.csv` | 800 source-linked existing headwords and 30 normative sense contrasts; only preexisting curated senses are fully lexically reviewed |
| 29, Valency and argument structure | `data/v28_34/verb_frame_inventory_400.csv` | 25 fully reviewed frames, 108 exactly source-licensed exemplar patterns, 267 provisional corpus observations |
| 30, Formal logic | `data/v28_34/adopted_function_words.json`, `quantifier_scope_examples.csv`, `finite_model_truth_tables.json` | New `nëgëra`, scope contrasts and finite-model truth-condition checks |
| 31, Conversational grammar | `data/v28_34/conversational_usage_rules.json` | 20 normative restrictions on fragments, repair, pronoun reference, turns and consent |
| 32, Word formation | `data/v28_34/canonical_compound_audit_13379.csv.gz`, `word_formation_audit_summary.json` | All 13,379 established compounds structurally audited; no bulk renaming |
| 33, Figurative and cultural expression | `data/v28_34/literary_conventions_32.json` | 32 existing editorial literary meanings classified, with explicit interpretation limits |
| 34, Standard conformance | `tools/v28_34/reform_core.py`, `tests/test_v28_34_language.py` | Conservative rule interpreter, compatibility and no-mutation checks |

**Editorial distinctions are deliberate:** one documented example does not establish every possible use of a verb; a shared English gloss does not prove synonymy; an editor-created literary interpretation is not an independently recorded folk saying. This precision makes a language easier to learn, not less complete.

## Build and verify

From repository root:

```bash
python tools/v28_34/build_release.py
python tools/v28_34/reform_core.py 'sen nëgëra qaro goro.'
python -m unittest tests.test_v28_34_language -q
python -m unittest discover -s tests -q
```

The source builder is deterministic. Historic source hashes remain fixed; adding a new lexical entry or changing a rule in the future requires an editioned amendment, explicit examples, and regression tests instead of quietly replacing a 7.0 record.
