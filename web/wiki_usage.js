/* Qaroshi Wiki 9.7: meaningful, source-bound lexical usage guides.
 * The field dictionary gloss is not secretly expanded into a new sense.
 * Morphological examples below are FORM ILLUSTRATIONS, never forged sentences.
 */
(function(root){
  'use strict';
  const plain=s=>String(s??'').trim();
  const exact=s=>plain(s).normalize('NFC').toLowerCase();
  const SUFFIX_FORMS=new Set(['-ri','-m','-na','-lo','-gu','-de','-wa','-tu','-shi','-së','-lë',
    '-te','-yu','-se','-mo','-në','-ki','-ho','-du','-la','-ru','-li','-wo','-ne','-nga','-za']);
  function candidateTokens(sentence){
    return plain(sentence).normalize('NFC').toLowerCase()
      .match(/[a-zë]+(?:-[a-zë]+)*/g)||[];
  }
  // Choose the LONGEST canonical lemma that exactly matches a surface token
  // with a legal, explicitly recorded suffix chain. In particular, "qaro"
  // must not be indexed as a mention of "qaro-naro" merely because a string
  // starts with those letters, and compound headwords must not be reduced to
  // an unrelated first syllable.
  function resolveToken(surface,byWord,suffixes=SUFFIX_FORMS){
    const word=exact(surface);
    if(byWord.has(word))return {headword:word,suffixes:[],surface:word};
    const pieces=word.split('-');
    for(let end=pieces.length-1;end>0;end--){
      const lemma=pieces.slice(0,end).join('-');
      const tails=pieces.slice(end).map(x=>'-'+x);
      if(byWord.has(lemma)&&tails.every(x=>suffixes.has(x)))
        return {headword:lemma,suffixes:tails,surface:word};
    }
    return null;
  }
  function sourceIndex(sentences,byWord,affixes){
    const known=new Set([...SUFFIX_FORMS,...(affixes||[]).map(x=>x.form)]);
    const indexed=new Map();
    for(const item of sentences){
      const occurrences=new Map();
      for(const token of candidateTokens(item.qaroshi)){
        const found=resolveToken(token,byWord,known);
        if(!found)continue;
        const prev=occurrences.get(found.headword);
        if(!prev||found.suffixes.length>prev.suffixes.length)occurrences.set(found.headword,found);
      }
      for(const [lemma,match] of occurrences){
        if(!indexed.has(lemma))indexed.set(lemma,[]);
        indexed.get(lemma).push({sentence:item,...match});
      }
    }
    return indexed;
  }
  // Highlight only a token that resolves to THIS complete dictionary lemma.
  // Thus qaro is not incorrectly highlighted inside another compound root.
  function highlight(text,lemma,byWord,affixes){
    const escape=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
    const allowed=new Set([...SUFFIX_FORMS,...(affixes||[]).map(x=>x.form)]);
    const parts=plain(text).split(/([A-Za-zëË]+(?:-[A-Za-zëË]+)*)/g);
    return parts.map(part=>{
      if(!part||!/^[A-Za-zëË]+(?:-[A-Za-zëË]+)*$/.test(part))return escape(part);
      const resolved=resolveToken(part,byWord,allowed);
      if(resolved&&resolved.headword===exact(lemma))
        return '<mark class="lexical-highlight">'+escape(part)+'</mark>';
      return escape(part);
    }).join('');
  }
  const CLASSES={
    n:{label:'Noun',how:'Names a person, object, place, event or concept. Its role in a sentence is shown with a case ending when needed.',
      placement:'Noun phrases can be subjects, objects, recipients, possessors and other participants. An adjective usually follows the noun.',
      chapter:'04',guide:'nouns_cases'},
    pron:{label:'Pronoun',how:'Refers to a person or group without repeating a noun. Case endings show its role in the sentence.',
      placement:'Pronouns use the same case slot as noun phrases. Inclusive and exclusive “we” are different dictionary words.',
      chapter:'05',guide:'nouns_cases'},
    v:{label:'Verb',how:'Expresses an action, process or state. The finite verb carries tense and optional aspect or modality, not person agreement.',
      placement:'The ordinary main-clause order places the verb after its participants. Required participants depend on this verb’s particular sense.',
      chapter:'06',guide:'verb_workshop'},
    adj:{label:'Adjective',how:'Describes a quality. Adjectives can modify nouns or serve as a present-time predicate without an English-style “is”.',
      placement:'The adjective normally follows its noun. In a predicate, it describes the subject after the sentence-opening resonance.',
      chapter:'29',guide:'sentence_anatomy'},
    adv:{label:'Adverb',how:'Contributes time, manner, degree or another circumstance, depending on the documented meaning.',
      placement:'Placement and scope depend on the type of adverb and the whole clause; not every adverb belongs in the same slot.',
      chapter:'13',guide:'sentence_anatomy'},
    det:{label:'Determiner',how:'Helps specify, quantify or identify a noun phrase.',
      placement:'A determiner belongs with the phrase it restricts. Interpret numerical and quantifier scope using the surrounding clause.',
      chapter:'22',guide:'nouns_cases'},
    conj:{label:'Conjunction',how:'Connects clauses or ideas and can change which proposition is asserted, conditional or contrasted.',
      placement:'Check the connective’s own documented rule for clause position and scope; its English gloss alone does not fix the full logic.',
      chapter:'11',guide:'clauses_and_counterfactuals'},
    part:{label:'Particle',how:'Marks a grammatical, discourse or interpersonal function rather than naming an ordinary object.',
      placement:'A particle’s position depends on its source-defined function; some follow resonance, others attach after a predicate or phrase.',
      chapter:'20',guide:'sentence_anatomy'},
    post:{label:'Postposition',how:'Expresses a relation to a preceding noun phrase.',
      placement:'A postposition follows the phrase to which it applies, rather than preceding it as an English preposition would.',
      chapter:'13',guide:'nouns_cases'},
    qword:{label:'Question word',how:'Asks for information about a participant, circumstance or other part of the clause.',
      placement:'Question scope and position follow Qaroshi interrogative rules; the initial resonance expresses intention, not question type.',
      chapter:'09',guide:'asking_and_negating'},
    intj:{label:'Interjection',how:'An expressive word or brief exclamation.',
      placement:'A complete independent sentence still follows the resonance system; an interjection is not itself evidence of tense or truth.',
      chapter:'16',guide:'conversation_social'},
    register:{label:'Resonance marker',how:'Sets the intended interpersonal or emotional resonance of an independent sentence.',
      placement:'The resonance marker comes first in an independent sentence. It does not substitute for evidence, tense or question grammar.',
      chapter:'02',guide:'resonance_mastery'}
  };
  const generic={label:'Lexical entry',how:'This entry has a documented lexical gloss and word class, but no separately source-licensed usage rule for this class.',
    placement:'Use the reference grammar and any recorded examples to determine its grammatical placement.',
    chapter:'35',guide:'dictionary_compounding'};
  function profile(word,data){
    const kind=plain(word.pos);
    const reson=(data.resonances||[]).find(x=>exact(x.marker)===exact(word.qaroshi));
    const particle=(data.grammaticalParticles||[]).find(x=>exact(x.form)===exact(word.qaroshi) && x.pos===kind);
    const pron=(data.pronouns||[]).find(x=>exact(x.form)===exact(word.qaroshi));
    const frame=(data.grammarFrames||[]).find(x=>exact(x.lemma)===exact(word.qaroshi));
    const cat=reson?'register':kind;
    const spec=CLASSES[cat]||generic;
    const forms=[];
    const original=word.qaroshi;
    if(kind==='n'){
      forms.push({text:original+'-m',label:'As a direct object',meaning:'case -m'});
      forms.push({text:original+'-na',label:'Possessive / genitive',meaning:'case -na'});
      forms.push({text:original+'-lo',label:'Location or time context',meaning:'case -lo'});
      forms.push({text:original+'-ri',label:'Plural form',meaning:'nominal -ri'});
    }else if(kind==='pron'){
      forms.push({text:original+'-m',label:'As an object',meaning:'case -m'});
      forms.push({text:original+'-na',label:'As a possessor',meaning:'case -na'});
      forms.push({text:original+'-tu',label:'As a recipient',meaning:'case -tu'});
    }else if(kind==='v'){
      forms.push({text:original,label:'Unmarked tense / general',meaning:'root'});
      forms.push({text:original+'-te',label:'Past',meaning:'tense -te'});
      forms.push({text:original+'-yu',label:'Future',meaning:'tense -yu'});
      forms.push({text:original+'-se',label:'Ongoing aspect',meaning:'aspect -se'});
      forms.push({text:'nu '+original,label:'Negated predicate',meaning:'nu before verb'});
    }
    const patterns=kind==='n'?
      [{pattern:'[subject] '+original+'-m [verb]',note:'Direct-object slot, when a verb licenses an object'},
        {pattern:'[possessor]-na '+original,note:'Possessive noun phrase'}]:
      kind==='pron'?
      [{pattern:'sen '+original+' [predicate].',note:'Subject slot; the complete predicate depends on the intended claim'}]:
      kind==='v'?
      [{pattern:'sen [subject] [other licensed participants] '+original+'.',note:'Neutral clause layout; omit brackets and supply the required roles'}]:
      kind==='adj'?
      [{pattern:'[noun] '+original,note:'Adjective following its noun'},
        {pattern:'sen [subject] '+original+'.',note:'Present-time adjective predicate; replace the placeholder'}]:
      kind==='det'?
      [{pattern:original+' [noun phrase]',note:'Modifier slot, where licensed by the specific determiner'}]:
      kind==='register'?
      [{pattern:original+' [complete clause].',note:'Sentence-initial resonance, independent of question or statement syntax'}]:
      [];
    const sourceRule=particle?.rule||'';
    let targeted=spec.how,placement=spec.placement;
    if(reson){
      targeted='The '+reson.name+' register expresses '+reson.meaning+'. It indicates the intended reception of the utterance, not an additional assertion about its truth.';
      placement='Write '+word.qaroshi+' at the beginning of an independent sentence. Questions and statements can both use this register; the sentence structure determines the speech act.';
    }
    if(pron)targeted+=' The source pronoun inventory gloss is “'+pron.english+'”.';
    return {
      kind:cat,label:spec.label,gloss:word.english,domain:word.domain,
      targeted,placement,forms,patterns,
      sourceRule,sourceRuleKind:particle?'Recorded particle rule':null,
      frame:frame?{frame:frame.frame,definition:frame.definition,selectionNote:frame.selection_note,
        roles:frame.required_roles||[],optional:frame.licensed_optional_roles||[]}:null,
      isResonance:!!reson,resonanceName:reson?.name||'',
      chapter:spec.chapter,guide:spec.guide,
      note:word.note||'',components:word.components||'',
      examplesAreAttested:false,meaningIsEditorialGloss:true
    };
  }
  root.QaroshiUsage=Object.freeze({profile,sourceIndex,resolveToken,candidateTokens,highlight,CLASSES});
})(typeof window!=='undefined'?window:globalThis);
