# Qaroshi 20.0 · Spoken Language & Pronunciation

**Release category:** Completed source-grounded phonemic pronunciation curriculum and private recording software. **Not an empirical speaker/dialect standard, and no new sounds or spellings.**

## The phonemic foundation

The native alphabet has 26 letters, represented in the canonical order `k a w t r q o d sh z u ë i g kh zh e ng h b p m s n y l`. Four Romanized digraphs (`sh`, `zh`, `kh`, `ng`) represent a single native letter each. The vowel phonemes are /a e i o u ə/. The consonant inventory and articulatory descriptions are in `data/v20/phoneme_reference_26.csv` and the older `docs/pronunciation.md`.

Default citation stress is **penultimate**, even if the word contains written case or verb suffixes: hyphens in Romanized teaching texts are *not pauses*. `qaroshi` is /qa.ˈɾo.ʃi/, `gëro` is /ˈɡə.ɾo/, and `dërawa` is /də.ˈɾa.wa/. Primary stress marks are lexical teaching conventions, not measured durations or fixed intonation.

## Connected speech and resonance

All 16 written resonance markers have their own phonemic realizations, like `më` /mə/ and `zha` /ʒa/. Resonance communicates pragmatic intent such as warmth, curiosity, solemnity, uncertainty, alarm, and gratitude. It does **not** mandate a unique, scientifically verified pitch contour. The linked `resonance_delivery_prompts.csv` shows documented sentences for every marker, with the rare markers represented by as few examples as the source contains.

Use phrase boundary cues from punctuation and conversational semantics; avoid chopping morphemes at teaching hyphens. Spontaneous coarticulatory changes, informal reductions, and dialect-specific pronunciations must be independently observed before becoming normative. Do not manufacture phonological reduction rules to make speech sound casual.

## Learning and practice

The offline `Qaroshi_20_Speech_Studio.html` contains:

- **26** source-linked sound cards with articulation guidance and dictionary examples
- **144** real canonical lexical sound contrasts, changing exactly one native grapheme per pair
- **105** word-stress exercises, with a **non-speech** tone-rhythm player for accent placement
- **110** existing source resonance contexts and **140** controlled connected-speech reading prompts
- A **14-day** self-paced speaking course
- A **3,000-item recording queue**: 656 documented phrase prompts and 2,344 canonical-word prompts, each with source ID, text, broad IPA and approximate sound-out
- An optional private in-browser recorder, replay, downloadable audio, explicit recording consent, local technical loudness checks, metadata exports and an in-session recording list

**These are 3,000 prompts, not 3,000 recordings.** No pre-recorded human speech, text-to-speech voice model, invented native-speaker corpus, or independently attested dialect is included.

## Responsible recording protocol

1. Obtain the actual recorded person's permission **before** opening the microphone. If the voice is not yours, the owner must understand what is being captured and how it will be used.
2. Identify the prompt and expected broad citation IPA. Capture the exact utterance without adding unrelated speech.
3. Check a technical waveform and audio playback. A possible clip/low-volume flag is not a pronunciation grade.
4. Independently review correctness of syllables, vowel quality, consonant place, penultimate stress, resonance and background noise. Document uncertainty, not guesswork.
5. Export both the audio file and JSON metadata. The browser page never uploads it; browser memory will not persist after closing the tab.
6. Collect **separate explicit publication permission** before releasing another person's voice, using it for voice synthesis, or using it to characterize a dialect. The JSON's consent checkbox records only local capture permission, not publication rights.
7. Run `python tools/v20/validate_recordings.py /path/to/metadata.json --audio-directory /path/to/downloaded/audio` to check source IDs and metadata fields. This validator does not certify voice identity, linguistic naturalness, consent authenticity or dialect.

## What remains human-dependent

The source only defines **citation pronunciation**. Accurate, consented human recordings, demonstrated intelligibility, observed casual reductions, reliable dialect boundaries and speaker-verified intonation require actual participants and independent adjudication. No release script can complete those empirical tasks without records.

## Build without network access

```bash
python tools/v20/build_release.py
python -m unittest tests.test_v20_speech -q
python tools/v20/browser_smoke.py
```

The app is a standalone HTML file and uses standard browser microphone APIs only when explicitly requested. A microphone requires browser permission and sometimes a secure context (HTTPS or localhost). The HTML remains usable for reading, drills, sound contrasts, and rhythm without microphone permission.
