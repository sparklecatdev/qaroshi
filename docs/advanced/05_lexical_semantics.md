# Lexical semantics, valency, relations and idioms

A large wordlist does not automatically produce a versatile language. Lexical semantics captures **which sense a word has**, **what constructions it selects**, **what it contrasts with**, and **what it tends to occur beside**. Qaroshi 7.0 introduces separately maintained structured semantics without reassigning the stable identifiers of the 30,000 dictionary entries.

## 1. A dictionary entry is not a semantic atom

A lexical *form* may have several related senses. `naro` covers a home, nesting place or safe shelter. Those are related contextual interpretations; they should not be presented as three entirely unrelated roots. Conversely, `nashi` (cherish), `mali` (romantic love), and `lani` (kin-like nurture) are distinct predicates even if English sometimes translates all as “love.” A translation chooses a **sense**, not merely a spelling.

Each structured sense record has: `lemma`, `pos`, `sense_id`, `definition`, `frame`, `domain`, `selectional_preferences`, `register`, `examples`, and optional semantic relations. A form can have more than one sense record. The separate frame table is especially important for verbs whose English translation might suggest an extra object or preposition not present in Qaroshi.

## 2. Selectional preferences vs grammatical impossibility

`këmë` (drink liquid) normally takes a liquid direct object, so `kima-m këmë` is the default pairing. The syntax does not prevent fantasy poetry in which someone “drinks light.” That is a **metaphor**, not evidence that `këmë` ordinarily means “consume any substance.” A medical translation should maintain the literal frame; a story can mark the figurative sense deliberately.

`daru` can protect a person or place; it takes the thing protected as a direct object. `pëli` (give) normally includes a thing (`-m`) and a recipient (`-tu`). `tika` (see/notice) is transitive but an object may be omitted when understood. `goro` (fly) is intransitive unless its causative is formed or a different lexical verb is chosen.

## 3. Near-synonyms and lexical choice

*Near-synonymy* means the words overlap in some contexts but differ in nuance. `gura` = go/travel, `wori` = explore/wander, `goro` = fly; their English glosses may overlap in “travel” contexts but they encode different event manners. `nëra` = remain/stay, not necessarily rest; `nëru` = rest, not necessarily remain in a location. A translator must not swap them merely because the sentence stays understandable.

## 4. Antonyms and scales

An antonym pair can be gradable (“warm/cold”), complementary (“alive/dead”), or relational (“give/receive”). The absence of a recognized lexical antonym is not a flaw: `nu` may express a negative property, but it is not always an adequate substitute for a conventional opposite. For instance “not good” can include neutral or unknown outcomes, whereas “dangerous” asserts an additional negative property.

## 5. Hyponymy and taxonomy

A specific term is a *hyponym* of a broader category. An identifiable Nardoragon is a `qaro`; a `qaru` is a Nardoragon hatchling. The narrower category entails the broader only when the definitions establish inclusion. The type hierarchy should not guess biology from English labels alone. The structured relations database records only curated links and leaves unverified ones blank.

## 6. Collocations

A **collocation** is a conventional combination: `mi-na naro` (my home), `kima-m këmë` (drink water), `mara-tu kima-m pëli` (give water to a friend), `ti-m nashi` (cherish you), `banu-shi goro` (fly with wings), `naro-lo nëra` (stay at home). These combinations are stronger evidence for idiomatic usage than any one word's isolated translation. A new expression may be grammatical but less natural if a more specific conventional word exists.

## 7. Compounds and transparent structure

Qaroshi compounds normally put **modifier before head**. `qaro + shi → qaroshi` literally “Nardoragon language.” `zhalo + shi → zhaloshi` = fire-voice/roar; a specialist term may have acquired a narrower meaning than its components suggest. The 30,000-entry dictionary includes many such transparent technical combinations; their presence means the language can name concepts productively, not that all were independently established through spontaneous speech. When a compound has several possible meanings, prefer a full explanatory clause in technical prose.

## 8. Idiom versus proverb versus ordinary metaphor

An **idiom** has a conventional nonliteral interpretation; a **proverb** is a reusable general statement; a **metaphor** maps features of one conceptual domain to another and may be newly coined. The idiom catalog identifies each expression's literal reading, intended figurative meaning, appropriate context, cultural caveats and resonance sensitivity. It does not invent a historical origin for a saying unless a source exists.

Idioms are **phrases**, not isolated lexical bases; they are cataloged separately from the 30,000-word dictionary so the count remains honest. Some are Nardoragon cultural expressions involving wings, roosts, fire and stars, while others are everyday conversational patterns.

## 9. Register and taboo terms

Profanity, intimate vocabulary and clinical anatomy require clear register notes. A clinical body-part term is not automatically an insult, and a vulgar synonym is not appropriate for a medical form. A person-directed curse can be harmful even when superficially phrased as an exclamation. The Academy retains learner control over random exposure to mature vocabulary. Formal translations prefer explicit and unambiguous terms where precision matters.

## 10. Figurative extensions and polysemy

Do not indiscriminately turn every “wing” term into an idiom for freedom, or every “fire” into a metaphor for anger. An expression qualifies for the idiom register only when documented as a convention in the reference. If the intended meaning is spontaneous poetic imagery, label it accordingly, and preserve the literal words so readers can still interpret the image.

## 11. Semantic compatibility test

A curated semantic relation must identify the exact participating word/sense IDs; verify both lemmas exist, that part-of-speech constraints hold, and that examples have the agreed roles. A synonym link is not automatically symmetric when senses differ. `translation_equivalent` is a language-pair relation, not a native synonym relation. A coarse English gloss must not be used as proof of precise equivalence.

## 12. Translation priorities

Prioritize (1) truth conditions and reference, (2) social force and consent, (3) argument roles and tense/aspect, (4) evidential/confidence stance, (5) lexical register, and only then (6) compactness and elegance. When no idiomatic Qaroshi equivalent exists, use a literal explanation rather than claiming one by analogy. The language is most useful when a speaker can say something **clearly**, even if the shortest possible phrase is not yet conventional.
