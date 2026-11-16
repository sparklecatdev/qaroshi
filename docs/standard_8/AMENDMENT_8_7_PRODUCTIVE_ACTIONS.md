# 8.7: productive everyday actions

This editorial addition records 97 further active V1 uses, each anchored to an existing dictionary verb and an existing editorial example with an overt `-m` object. They extend the 8.4 and 8.6 overlays without changing earlier entries or frozen baselines. The source examples are constructed editorial material, not independently observed speech.

## Using these frames

In the restricted model `RESONANCE SUBJECT OBJECT-m [nu] VERB`, the subject is the participant performing or experiencing the action and the object is the participant or thing in the listed role. Existing tense, aspect, modal and tender suffixes may compose in the standard order. `nu` immediately before the predicate negates the action; final `he` marks a polar question. An overt noun plural precedes case (`-ri-m`). For example:

* `sen mi shiwaro-m khukhiri.` — I encrypt a message (source S00251).
* `sen ti shiwaro-ri-m nu khukhiri-yu he?` — Will you not encrypt messages? This is a newly composed editorial example; the negative question does not assert encryption.
* `sen mi shërawëlon-m khungëmi-te.` — I saved a file. The file need not have a separate backup.

Each role below is a narrow characterization of its source example, not permission for arbitrary objects of the same general kind. The dictionary gloss “book a ticket” and the existing example “book a flight” differ in specificity; the flight example is retained with that limitation, without asserting every travel reservation is licensed. Where the dictionary word describes a successful result, negating that verb does not say whether an attempt occurred. These entries do not add passive, causative, recipient, instrument, or complement permissions. They do not assert a time, result, or actor beyond the sentence's grammar and lexical meaning.

The `tools/stress87/validate.py` checker recognizes only a transparent subset: an overt pronoun subject, one dictionary noun or pronoun object (optionally plural), one of these predicates, optional local negation, optional `he`, and a restricted suffix sequence. Its match means **form only**: it does not check the object role, truth conditions, translation, naturalness, or wider grammar. A sentence outside this subset is not thereby ungrammatical. In particular it does not analyze noun subjects, omitted hyphens, other grammatical roles, or arbitrary embedding.

## Source-linked roles and limits

The full source sentence, dictionary IDs and translation are preserved in [the machine-readable overlay](../../data/standard_8/valency_overlay_8_7.json). Boundaries describe what is *not* entailed; they are not additional claims about what happened.

| Verb | Dictionary gloss | Example object role | Boundary | Source |
| --- | --- | --- | --- | --- |
| `shëroli` | translate; carry meaning between languages | language or material translated | Translation does not guarantee accuracy or identify the target language. | S00133 |
| `khushësi` | install software | software installed | Installation does not guarantee that the software runs correctly. | S00236 |
| `bozilu` | reset a password | password reset | Resetting does not imply that the account is secure. | S00241 |
| `khukhiri` | encrypt | message encrypted | Encryption does not guarantee that the recipient can decrypt the message. | S00251 |
| `khungëtu` | decrypt | message decrypted | Decryption does not imply that its contents are true. | S00256 |
| `khuwohu` | open a file | file opened | Opening a file does not imply that it was read or edited. | S00261 |
| `khungëmi` | save a file | file saved | Saving does not imply that a backup exists elsewhere. | S00266 |
| `khuwëshu` | rename a file | file renamed | Renaming does not imply that its contents changed. | S00271 |
| `khungëgu` | delete a file | file deleted | Deletion does not imply that all copies have disappeared. | S00276 |
| `khuziru` | restore a file | file restored | Restoring a file does not imply that it is complete or correct. | S00281 |
| `khuziqu` | copy a file | file copied | Copying does not imply that the original was removed. | S00286 |
| `khunikhu` | archive data | file archived | Archiving does not imply that the file is permanently retained. | S00291 |
| `khupizhi` | search a folder | folder searched | Searching a folder does not imply that the sought item was found. | S00296 |
| `khugëhi` | compile | source code compiled | Compilation does not imply that the program is correct. | S00301 |
| `khurëni` | review code | source code reviewed | Review does not imply approval or the discovery of every defect. | S00306 |
| `beqishi` | diagnose a fault | software fault diagnosed | Diagnosis does not imply repair. | S00316 |
| `khurëngi` | test software | software release tested | Testing does not prove that the release is defect-free. | S00321 |
| `khukhëmi` | benchmark | computer benchmarked | Benchmarking does not imply that the computer is fast. | S00326 |
| `khuseru` | configure | router configured | Configuration does not guarantee connectivity or security. | S00336 |
| `bowewi` | host a server | server hosted | Hosting does not imply that the server is publicly accessible. | S00341 |
| `khushëzu` | restart | server restarted | Restarting does not imply that a fault was fixed. | S00346 |
| `borumu` | filter packets | network packets filtered | Filtering does not by itself say which packets are allowed. | S00351 |
| `khuzhaqi` | query a database | database queried | A query does not guarantee a useful result. | S00356 |
| `khubezi` | restore data | backup restored | Restoration does not prove the backup was complete. | S00361 |
| `deqori` | edit a photo | photograph edited | Editing does not imply publication or permission to publish. | S00371 |
| `denuzu` | review a film | film reviewed | Reviewing does not imply a favorable judgment. | S00381 |
| `deraru` | publish a book | book published | Publication does not imply that anyone has read the book. | S00386 |
| `demamu` | listen to music | music listened to | Listening does not imply liking or understanding. | S00391 |
| `deqëqi` | publish a song | song published | Publication does not imply that anyone has heard the song. | S00396 |
| `demënu` | create art | painting created | Creating does not imply exhibiting or selling the painting. | S00401 |
| `deseri` | critique art | artwork critiqued | Critique does not imply a negative judgment. | S00406 |
| `demomu` | tell a story | story told | Telling a story does not assert that it is true. | S00411 |
| `deqoyi` | read poetry | poetry read | Reading does not imply memorization or agreement. | S00416 |
| `subimu` | cite a source | research paper cited | Citation does not imply endorsement or verification. | S00421 |
| `ngigamu` | investigate | research question investigated | Investigation does not guarantee an answer. | S00426 |
| `sugënu` | test a prediction | hypothesis tested | Testing does not imply confirmation. | S00431 |
| `zohowi` | verify a calculation | calculation verified | Verification does not specify the method used. | S00436 |
| `zoshëzu` | reduce a fraction | fraction reduced | Reduction does not specify the representation used. | S00446 |
| `zosuqi` | solve an equation | equation solved | Solving does not identify the solution. | S00451 |
| `zomunu` | check a proof | proof checked | Checking does not assert that the proof is valid. | S00456 |
| `surashu` | publish research | research paper published | Publication does not establish the truth of its claims. | S00466 |
| `bemati` | measure precisely | pressure measured | Measurement does not give a value or unit by itself. | S00476 |
| `sunaku` | measure temperature | temperature measured | Measurement does not give a value or unit by itself. | S00481 |
| `zosozhu` | measure an angle | angle measured | Measurement does not give a value or unit by itself. | S00486 |
| `zohoyi` | measure an area | area measured | Measurement does not give a value or unit by itself. | S00491 |
| `guselu` | measure blood pressure | blood pressure measured | Measurement alone does not establish a diagnosis. | S00496 |
| `gusulu` | alleviate symptoms | symptoms alleviated | Alleviation does not imply that their cause is cured. | S00501 |
| `gushëqi` | clean a wound | wound cleaned | Cleaning does not imply that the wound has healed. | S00506 |
| `gunayi` | bandage a wound | wound bandaged | Bandaging does not imply that the wound has healed. | S00511 |
| `guhini` | prescribe medication | medicine prescribed | Prescribing does not imply that medicine was taken. | S00516 |
| `gusuru` | care for a patient | patient cared for | Care does not guarantee recovery. | S00521 |
| `guqaki` | examine medically | patient examined medically | Examination does not itself provide a diagnosis. | S00526 |
| `kerodu` | reassure | person reassured | Reassuring someone does not establish that all danger has gone. | S00541 |
| `mëli` | comfort; soothe | person comforted | Comforting does not guarantee relief. | S00546 |
| `keguyi` | respect | person respected | Respect does not imply agreement with every decision. | S00551 |
| `ketangi` | respect boundaries | boundary respected | Respecting a boundary does not imply the boundary is permanent. | S00561 |
| `keshobu` | accept an invitation | invitation accepted | Acceptance does not imply that attendance occurred. | S00566 |
| `kezhingu` | decline an invitation | invitation declined | Declining an invitation does not imply hostility. | S00571 |
| `wenganu` | enact policy | policy enacted | Enactment does not imply effective implementation. | S00586 |
| `wemomi` | repeal a law | law repealed | Repeal does not establish whether prior conduct was lawful. | S00591 |
| `werëhi` | elect | candidate elected | Election does not imply that the candidate has taken office. | S00596 |
| `wewëtu` | organize a protest | protest organized | Organizing does not imply that the protest took place. | S00606 |
| `sebilu` | convert currency | currency converted | Conversion does not specify an exchange rate. | S00611 |
| `sezhikhi` | save money | money saved | Saving does not specify an amount or guarantee safety. | S00616 |
| `serepu` | spend money | money spent | Spending does not imply that the purchase was worthwhile. | S00621 |
| `seropi` | repay | loan repaid | Repayment does not itself say who lent the money. | S00626 |
| `senëni` | refund | purchase refunded | A refund does not imply that the original payment was fraudulent. | S00631 |
| `semawu` | negotiate price | price negotiated | Negotiation does not imply agreement. | S00646 |
| `rezhisi` | drive | car driven | Driving does not imply arrival at a destination. | S00661 |
| `relapi` | rent a car | car rented | Renting does not transfer ownership. | S00666 |
| `luditu` | climb a mountain | mountain climbed | Climbing does not by itself identify the route taken. | S00676 |
| `lurezhu` | cross a river | river crossed | Crossing does not specify the means of travel. | S00681 |
| `repoqu` | cross a road | road crossed | Crossing does not specify whether a marked crossing was used. | S00686 |
| `reshuli` | navigate a route | route navigated | Navigating does not imply arrival on time. | S00696 |
| `reweshu` | book a ticket | flight booked | The source applies the ticket-booking verb to a flight; booking does not imply that the flight occurred. | S00701 |
| `retëku` | reserve a seat | seat reserved | Reserving does not imply that the seat was used. | S00706 |
| `tëpopu` | clean a house | house cleaned | Cleaning does not imply every part is spotless. | S00711 |
| `tënipi` | tidy a room | room tidied | Tidying does not imply washing or disinfection. | S00716 |
| `tëhakhi` | paint a wall | wall painted | Painting does not specify its color. | S00721 |
| `tëdiru` | assemble furniture | furniture assembled | Assembly does not imply that it is sturdy. | S00726 |
| `tënisi` | make a bed | bed made | Making a bed does not imply that anyone slept in it. | S00731 |
| `gizuku` | wash clothing | clothing washed | Washing does not imply that the clothing is dry. | S00736 |
| `giburi` | polish shoes | shoes polished | Polishing does not imply that the shoes were repaired. | S00741 |
| `gireru` | sew | shirt sewn | Sewing does not specify who will wear the shirt. | S00751 |
| `nëshongu` | prepare a meal | food prepared | Preparing food does not imply that it was eaten. | S00756 |
| `zhalëwa` | cook; heat food to prepare it | meal cooked | Cooking does not imply that the meal was eaten. | S00761 |
| `nëkati` | follow a recipe | recipe followed | Following a recipe does not guarantee a successful dish. | S00766 |
| `nëqobi` | measure ingredients | ingredient measured | Measurement does not state a quantity. | S00771 |
| `nëgegi` | peel a vegetable | vegetable peeled | Peeling does not imply that it was cooked. | S00776 |
| `ngidoti` | submit homework | assignment submitted | Submission does not imply acceptance or a passing grade. | S00791 |
| `ngirihi` | pass an exam | exam passed | Passing does not imply a perfect score. | S00801 |
| `ngihuzhi` | fail an exam | exam failed | Failure does not identify the reason or score. | S00806 |
| `deshemu` | write poetry | poem written | Writing does not imply publication. | S00821 |
| `nguyeqi` | groom wings | wing groomed | Grooming does not imply medical treatment. | S00826 |
| `ngukeri` | guard a nest | nest guarded | Guarding does not guarantee that no harm occurs. | S00831 |
| `ngupiqu` | repair wing membrane | wing membrane repaired | Repair does not specify the technique used. | S00836 |
| `ngumawi` | share a roost | roost shared | Sharing does not imply equal ownership. | S00846 |

## Measurement and limits

`python tools/stress87/benchmark.py` reports recognition of the 97 source examples and transparent positive and negative forms generated from those same examples. These checks exercise suffix order, case forms, negation and questions, but are not held out, are not a semantic accuracy measurement and do not demonstrate independent learner comprehension. The earlier 404 undrafted challenges and unreviewed senses remain open; this release does not claim the language is complete or independently attested.
