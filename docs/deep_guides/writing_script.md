# Native script, transliteration, typography, and names

> **Deep reference** · Related grammar chapters: 1, 30, 33–34, 46, 50, 69 · All examples below are from the unified Qaroshi phrasebook.

## An alphabet of sounds

The original Nardoragon script consists of 26 handwritten glyphs. Each native glyph corresponds to one unit of the Qaroshi phoneme inventory, even when Romanization writes it as two characters (`sh`, `zh`, `kh`, `ng`). This makes the native alphabet a phonemic writing system, not a character-by-character cipher for English. Qaroshi Romanization is a representation of Qaroshi sounds; English spelling is not a safe input to the native-glyph converter.

## Procedure for transliterating a Qaroshi word

Normalize text to Unicode NFC, split Romanized writing into the longest recognized graphemes, preserving the four multi-letter native graphemes as indivisible units, then replace each with its corresponding original image glyph. Preserve word boundaries, ordinary punctuation and explicitly quoted foreign material as separate text/notation. If a word contains a Latin letter not in the Qaroshi native inventory, report it instead of silently inventing a native equivalent.

## Marking grammatical boundaries

Teaching text often uses hyphens in `mi-na`, `mara-tu`, `goro-te-se` to expose morphemes. These are **not** extra letters or obligatory native punctuation and can be omitted in fluent writing. A linguist can retain them in an interlinear edition to show structure, but a normal message need not expose all suffix boundaries. Conversely, hyphen omission can make some analyses less obvious; the dictionary and grammatical context must decide where the stem ends.

## Letter identity versus calligraphic freedom

The glyph artwork contains crossings and loops that distinguish original forms. Writing may stretch or stylize them, but different letter forms should remain recognizable, especially those mapped to distinct vowels `e` and `ë`, or consonants `k` and `q`. If a visual font is eventually produced, it must be checked against all 26 shapes and actual character boundaries, not merely against decorative sample words.

## Names and foreign quotation

A proper name has a pronunciation in its source language, and a faithful Qaroshi transcription must start from that pronunciation rather than blindly turning each English letter into an unrelated Qaroshi glyph. Foreign product names, handles, file paths, code, and addresses can remain quoted external strings in technical writing. Such quoted strings do not extend the alphabet or require Qaroshi phonotactic repair unless the writer intentionally adapts the name as a Qaroshi word.

## Reliable file exchange

UTF-8 is preferred, and `ë` should not be replaced with `e` as a convenience. For ASCII-only systems, specify a reversible escaping/transliteration scheme rather than silently losing information. The offline wiki can produce a visual PNG of native glyph text; this is an image, not yet a Unicode-encoded editable native-font string. Keep Romanized originals when machine searching, accessibility and copy/paste matter.

## Read and listen mentally: annotated reference examples

### S00001: Hello, friend!
**Qaroshi:** `zha ha, mara!`
**IPA:** `/ʒa ha, ˈma.ɾa/` · **Stress guide:** `zha ha, MA-ra!` · **Sound-out:** `zhah hah, MAH-rah!`
**Usage note:** Bright Trill makes the greeting lively


### S00003: Are you well?
**Qaroshi:** `hë ti haro he?`
**IPA:** `/hə ti ˈha.ɾo he/` · **Stress guide:** `hë ti HA-ro he?` · **Sound-out:** `huh tee HAH-roh heh?`
**Usage note:** Seeking Call question


### S00021: You are cute.
**Qaroshi:** `më ti lësha.`
**IPA:** `/mə ti ˈlə.ʃa/` · **Stress guide:** `më ti LË-sha.` · **Sound-out:** `muh tee LUH-shah.`
**Usage note:** Warm Hum compliment


### S00035: Please never die, so you can stay with me forever.
**Qaroshi:** `më pëla, ti sëna nu zëru ya, ko ti mi-wa sëna nëra-ki.`
**IPA:** `/mə ˈpə.la, ti ˈsə.na nu ˈzə.ɾu ja, ko ti ˈmi.wa ˈsə.na nə.ˈɾa.ki/` · **Stress guide:** `më PË-la, ti SË-na nu ZË-ru ya, ko ti MI-wa SË-na në-RA-ki.` · **Sound-out:** `muh PUH-lah, tee SUH-nah noo ZUH-roo yah, koh tee MEE-wah SUH-nah nuh-RAH-kee.`
**Usage note:** One resonance covers both clauses


### S00064: I drink water.
**Qaroshi:** `sen mi kima-m këmë.`
**IPA:** `/sen mi ˈki.mam ˈkə.mə/` · **Stress guide:** `sen mi KI-mam KË-më.` · **Sound-out:** `sehn mee KEE-mahm KUH-muh.`
**Usage note:** Object marker


### S00079: Nardoragons fly.
**Qaroshi:** `sen qaro-ri goro.`
**IPA:** `/sen qa.ˈɾo.ɾi ˈɡo.ɾo/` · **Stress guide:** `sen qa-RO-ri GO-ro.` · **Sound-out:** `sehn qah-ROH-ree GOH-roh.`
**Usage note:** General truth


### S00095: They flew; I saw it.
**Qaroshi:** `sen sa goro-te si.`
**IPA:** `/sen sa ɡo.ˈɾo.te si/` · **Stress guide:** `sen sa go-RO-te si.` · **Sound-out:** `sehn sah goh-ROH-teh see.`
**Usage note:** Direct evidence si


### S00104: Which Nardoragon did you see?
**Qaroshi:** `hë ti ruki qaro-m tika-te he?`
**IPA:** `/hə ti ˈɾu.ki ˈqa.ɾom ti.ˈka.te he/` · **Stress guide:** `hë ti RU-ki QA-rom ti-KA-te he?` · **Sound-out:** `huh tee ROO-kee QAH-rohm tee-KAH-teh heh?`
**Usage note:** Demonstrative-like which


## Guided retrieval practice

These exercises use exactly the forms shown above. First cover the answer, then write the full sentence with its resonance, case endings, and closing particles. Verify spelling against the dictionary rather than guessing from English.

1. Translate into Qaroshi: **Hello, friend!**
2. Translate into Qaroshi: **Are you well?**
3. Translate into Qaroshi: **You are cute.**
4. Translate into Qaroshi: **Please never die, so you can stay with me forever.**
5. Translate into Qaroshi: **I drink water.**
6. Translate into Qaroshi: **Nardoragons fly.**

<details><summary>Answer key: reveal after trying</summary>

1. `zha ha, mara!` · /ʒa ha, ˈma.ɾa/
2. `hë ti haro he?` · /hə ti ˈha.ɾo he/
3. `më ti lësha.` · /mə ti ˈlə.ʃa/
4. `më pëla, ti sëna nu zëru ya, ko ti mi-wa sëna nëra-ki.` · /mə ˈpə.la, ti ˈsə.na nu ˈzə.ɾu ja, ko ti ˈmi.wa ˈsə.na nə.ˈɾa.ki/
5. `sen mi kima-m këmë.` · /sen mi ˈki.mam ˈkə.mə/
6. `sen qaro-ri goro.` · /sen qa.ˈɾo.ɾi ˈɡo.ɾo/

</details>

## Study checkpoint

Before leaving this chapter, explain in your own words how its central grammatical distinction changes the truth conditions or social intention of a sentence. Then alter **one** feature of an example (resonance, tense, case, negation, evidential, or speech act) and check the resulting form in the 70-chapter grammar. A good translation must preserve what was said and how it was framed.
