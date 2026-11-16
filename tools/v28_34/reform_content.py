"""Manually authored normative/teaching distinctions for Qaroshi 28–34.

No content here represents independent speaker evidence. Automated analyses in
build_release.py are tagged separately from these consciously authored rules.
"""
# New function-word spelling was checked against the full 30,000-word lexicon.
NEW_DETERMINER = {
  'lemma':'nëgëra','pos':'det','meaning':'not every; not all members of a specified nonempty group',
  'logical_form':'∃x∈D ¬P(x)','grammar_class':'quantifier','position':'immediately precedes quantified noun phrase',
  'contrast':'ngënao D nu P = ∀x∈D ¬P(x); shërano D P = ∃x∈D P(x)',
  'scope':'restricts only the quantified nominal subject in a simple distributive clause',
  'count_domain':'presupposes at least one member of the relevant domain; asserts at least one counterexample',
  'frozen_lexicon_compatibility':'post-7.0 lexical overlay, not a replacement for an existing canonical ID',
  'adopted':'normative in amendment 30; unrecorded in historical 7.0 files',
  'example':'sen nëgëra qaro goro.',
  'translation':'Not every Nardoragon flies (at least one does not).',
}
# Existing expressions are source-backed. These values clarify their *truth conditions*,
# not their metaphorical force or their social frequency.
LOGIC_EXAMPLES=[
 ('L30-01','sen ngënao qaro goro.','every','Every Nardoragon flies.','forall x in D: P(x)','does not imply more than one exists'),
 ('L30-02','sen ngënao qaro nu goro.','every_neg','No Nardoragon flies.','forall x in D: not P(x)','do not read as merely not everyone'),
 ('L30-03','sen nëgëra qaro goro.','not_every','Not every Nardoragon flies.','exists x in D: not P(x)','does not entail that anyone flies'),
 ('L30-04','sen shërano qaro goro.','some','Some Nardoragon flies.','exists x in D: P(x)','does not entail that some do not fly'),
 ('L30-05','sen dëna qaro ngëshi haro.','only','Only this Nardoragon is well.','P(focus) and relevant alternatives are not P','requires identified relevant comparison set'),
 ('L30-06','sen dëna qaro tëmiri haro.','even','Even this Nardoragon is well.','P(focus) with unexpected relative scale','not a separate assertive evidential'),
 ('L30-07','sen nura naro-lo eri.','nobody','Nobody is at home.','no human x in domain has P(x)','do not add ordinary predicate nu'),
 ('L30-08','sen ngënao qaro goro-në.','habitual_all','Every Nardoragon habitually flies.','forall x in D: habitual_P(x)','not every member continuously flies'),
 ('L30-09','sen ngënao qaro nu goro-në.','habitual_none','No Nardoragon habitually flies.','forall x in D: not habitual_P(x)','not the same as never flew'),
 ('L30-10','sen shoru sa goro, mi naro-lo nëra-yu.','unless','Unless they fly, I will remain at home.','if not P then Q; P does not force not-Q','do not translate unless as iff'),
 ('L30-11','sen shërano qaro nu goro.','some_neg','Some Nardoragons do not fly.','exists x in D: not P(x)','same truth condition as nëgëra in simple positive subject scope'),
 ('L30-12','sen qaro-ri qësho po goro.','at_least','At least two Nardoragons fly.','count(P(x)) >= 2','the number is expressed in base six'),
 ('L30-13','sen qaro-ri rëshu po goro.','at_most','At most two Nardoragons fly.','count(P(x)) <= 2','zero is compatible; do not assume two'),
 ('L30-14','sen qaro-ri nëmi po goro.','exactly','Exactly two Nardoragons fly.','count(P(x)) = 2','must not be simplified to at least two'),
 ('L30-15','sen dëna qaro bëso haro.','also','This Nardoragon is also well.','P(focus) plus relevant alternative P','presupposes meaningful alternative'),
 ('L30-16','sen nëgëra qaro haro.','not_every_adjectival','Not every Nardoragon is well.','exists x in D: not well(x)','negates universal claim, not a finite predicate by nu'),
]
# Edit decisions target *interaction behavior* rather than fabricate sound reductions.
DISCOURSE_RULES=[
 ('D31-01','complete_sentence','All written independent finite assertions and direct questions retain exactly one initial resonance','sen mi haro.','mi haro.','Required structure, even in informal chat'),
 ('D31-02','minimal_reply','An answer consisting only of shë/nu is a contextual fragment','shë','sen shë.','Both licensed; first fragment, second complete written response'),
 ('D31-03','subject_drop','Subject omission is licensed only if one immediately salient referent makes it uniquely recoverable','nëm përo.','nu daru.','Omission cannot be used to hide participants in consent-sensitive utterances'),
 ('D31-04','self_correction','dënaro repairs the current speaker’s earlier propositional claim, not a different person’s words','sen dënaro mi ti-m daru-yu.','qëlo mi ti-m daru-yu.','A correction requires the newly intended proposition'),
 ('D31-05','mishearing','qëlo signals a hearing repair; it does not itself retract the previous claim','hë qëlo ti haro he?','sen dënaro mi haro.','Keep mishearing separate from claim revision'),
 ('D31-06','silence','Unanswered invitation or request means no answer, never automatic agreement','hë ti haro he?','','Evidence cannot be inferred from silence'),
 ('D31-07','topic_shift','tëshi introduces a new topic only following initial resonance','sen tëshi mi haro.','tëshi sen mi haro.','One resonance initial remains obligatory'),
 ('D31-08','voluntary_request','pëshu makes refusal explicitly permissible without asserting agreement','më tëqoro ti mi-wa goro ya.','më ti mi-wa goro.','Social stance and content are separate'),
 ('D31-09','rumor','hu reports information; it does not establish eyewitness truth','sen sa goro-te hu.','sen sa goro-te si.','Use source distinctions deliberately'),
 ('D31-10','paraphrase','wëlëmi is paraphrase; qëhano is verbatim quote; never stack on the same span','sen wëlëmi mi ti-m nashi.','sen qëhano wëlëmi mi ti-m nashi.','Quoted complete clauses still need their own resonance'),
 ('D31-11','referent_switch','Repeat noun or use name when two possible people could be sa','sen sa haro.','','Anaphora must have one salient candidate'),
 ('D31-12','politeness','hë requests information, pëla expresses politeness; resonance cannot assert consent','më pëla ngëlawe shiri ya.','','A pleasant attitude is not authorization'),
 ('D31-13','ellipsis','A short label or answer can omit recoverable structure; a full finite clause cannot drop its resonance','nu','nu haro.','Distinguish fragment from incomplete sentence'),
 ('D31-14','repair_in_turn','After an explicit correction, quote the earlier form only as superseded','sen dënaro mi ti-m daru-yu.','','Cannot silently rewrite earlier speaker turn'),
 ('D31-15','conditional_promise','An invitation, promise and obligation must remain lexically distinct','qor mi ti-m daru-yu.','dal mi ti-m daru-du.','Future and duty do not imply each other'),
 ('D31-16','register_switch','To change resonance, close the independent sentence and begin a new marked one','sen mi haro. zha mi goro-yu!','sen mi haro zha mi goro-yu.','No mid-sentence marker stacking'),
 ('D31-17','negative_answer','Bare nu is a fragment, not a complete denial of arbitrary preceding content','nu','sen mi nu haro.','Use full statement to make the negated proposition clear'),
 ('D31-18','uncertain_assertion','shurëmi leaves content unresolved; absence of evidence is not affirmative proof','zher shurëmi sa haro.','sen sa haro si.','Do not upgrade stance to evidence'),
 ('D31-19','group_pronouns','naru includes listener, muru excludes; not interchangeable for commitments','sen naru qaroshi-m shiri.','','Choose group membership intentionally'),
 ('D31-20','rhetorical_question','Rhetorical question frame marks no expected literal answer','hë yëhano ti haro he?','hë ti haro he?','Do not infer interrogative force solely from punctuation'),
]
# Canonical lexical distinctions already supported by the earlier reviewed 24–27
# senses. These comparisons do not assert new pronunciations or usage frequencies.
LEXICAL_PAIRS=[
 ('nashi','mali','cherish deeply vs romantic love'),('nashi','lani','cherish deeply vs familial caring'),
 ('mali','lani','romantic love vs familial care'),('tika','sëmi','see/perceive vs know'),
 ('shëliro','zhëmi','read text vs understand meaning'),('goro','gura','fly vs travel'),
 ('nëra','nëru','stay/remain vs rest'),('pëli','hari','transfer a theme to a recipient vs possess'),
 ('këmë','shëma','drink liquid vs eat food'),('sharoa','shiri','ask vs speak generally'),
 ('pëla','pëlë','ordinary politeness vs deferential request'),('si','hu','direct observation vs reported information'),
 ('hu','ye','report vs inference'),('ngënao','shërano','all vs some'),
 ('ngënao','nëgëra','universal vs not universal'),('ngëshi','tëmiri','only vs even'),
 ('zhoro','mënoro','still ongoing vs not yet'),('mënoro','nësha','not yet vs no longer'),
 ('wë','wënu','real possibility vs contrary-to-fact condition'),('dasha','shoru','even if vs unless'),
 ('qor','sen','solemn resonance vs neutral'),('më','zha','warm resonance vs playful'),
 ('naru','muru','we inclusive vs exclusive'),('tiri','ti','plural you vs singular'),
 ('gëwëmi','ngëshi','except for vs only'),('rëno','ngëra','none vs all'),
 ('nashu','nëzha','collective vs distributive'),('rëshi','ngëshi','focus vs exclusivity'),
 ('këra','ngëshi','adverb exclusively vs focus particle'),('tëmiri','yara','even focused participant vs discourse unexpected also'),
]
# Authorial classification of existing documented literary expressions:
# no fabricated traditional/colloquial frequency claim.
LITERARY_CONVENTIONS={
 'FX001':('deliberation','resisting premature action'),
 'FX002':('commitment','enduring intention, not literal immortality'),
 'FX003':('aspiration','distant goal is salient'),
 'FX004':('stability','choose not to chase every distraction'),
 'FX005':('loyalty','stand beside a friend'),
 'FX006':('confidence','wing imagery must not denote literal ability'),
 'FX007':('reflection','read beyond the words'),
 'FX008':('belonging','seek shelter or familiarity'),
 'FX009':('grief','suppressed feelings rather than physical silence'),
 'FX010':('courage','future effort is not guaranteed success'),
 'FX011':('lost_focus','goal no longer salient'),
 'FX012':('grounding','small task restores emotional balance'),
 'FX013':('community','protect collective belonging'),
 'FX014':('care','cherishing does not automatically entail romance'),
 'FX015':('belonging','desire for home'),
 'FX016':('evidence','silence is not proof of absence'),
 'FX017':('creativity','transform experience into writing'),
 'FX018':('loyalty','intent is not a legal obligation'),
 'FX019':('safety','feeling accepted'),
 'FX020':('shyness','reluctance to confess'),
 'FX021':('defiance','leave intolerable conditions'),
 'FX022':('recognition','acknowledge another person'),
 'FX023':('self_care','protect the means of acting'),
 'FX024':('completion','end of effort'),
 'FX025':('discovery','unexpected safe place'),
 'FX026':('hope','longer timescale of aspirations'),
 'FX027':('collaboration','collective planned effort'),
 'FX028':('longing','anticipated reunion'),
 'FX029':('change','refuse to remain in current state'),
 'FX030':('restraint','choose not to speak immediately'),
 'FX031':('inquiry','search for purpose'),
 'FX032':('companionship','offered presence without coercion'),
}

# Manually inspected against the listed canonical corpus clauses (the
# v15–17 editorial examples displayed during the v28–34 review). For each
# item this only licenses the *observed object-bearing exemplar*, not every
# possible patient class, passive derivation or causative. It is separate from
# and narrower than the 25 complete, previously manually reviewed verb frames.
EXEMPLAR_REVIEWED_VERBS = '''
khunikhu khurëngi semeqi werëhi koniri
khushësi bozilu khukhiri khungëtu khuwohu khungëmi khuwëshu khungëgu
khuziru khuziqu khupizhi khugëhi khurëni khuhangu beqishi khukhëmi
khuseru bowewi khushëzu borumu khuzhaqi khubezi deqori dekhoyi
denuzu deraru demamu deqëqi demënu deseri demomu deqoyi subimu
ngigamu sugënu zohowi zorësu zoshëzu zosuqi zomunu zoronu surashu
bemati sunaku zosozhu zohoyi guselu gusulu gushëqi gunayi guhini
gusuru guqaki kerodu mëli keguyi ketangi keshobu kezhingu wenganu
wemomi wewëtu sebilu sezhikhi serepu seropi senëni sekhëshu semawu
rezhisi relapi luditu lurezhu repoqu reshuli reweshu retëku tëpopu
tënipi tëhakhi tëdiru tënisi gizuku giburi gitebu gireru nëshongu
zhalëwa nëkati nëqobi nëgegi ngidoti ngilepi ngirihi ngihuzhi ngitini
ngizhukhu deshemu nguyeqi ngukeri ngupiqu nguwosi ngumawi
'''.split()
assert len(EXEMPLAR_REVIEWED_VERBS)==len(set(EXEMPLAR_REVIEWED_VERBS))
