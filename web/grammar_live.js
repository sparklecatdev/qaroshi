/* Qaroshi 9.3 verified-subset grammar for the standalone Wiki.
 * Source licenses are embedded from data/standard_9_3/grammar_licenses.json
 * and data/semantics/valency_frames.json. No network, eval, or NLP guessing.
 * The browser parser and composer are tested against the source Python engine.
 */
(function(root){
  'use strict';
  const CASES={recipient:'tu',patient:'m',goal:'gu',source:'de',location:'lo',comitative:'wa'};
  const ORDER=['recipient','patient','goal','source','location','comitative'];
  const TEMPO={after:'ana',before:'ëna',when:'yaro',if:'wë',counterfactual:'wënu'};
  const REVERSE=Object.fromEntries(Object.entries(TEMPO).map(([k,v])=>[v,k]));
  const DEFAULTS={tense:'',aspect:'',modal:'',negated:false};
  class GrammarError extends Error {
    constructor(message){super(message);this.name='GrammarError'}
  }
  function createGrammar(spec,frameList){
    if(!spec || !Array.isArray(frameList) || frameList.length!==25)
      throw new GrammarError('The 9.3 source licenses are unavailable.');
    const lex=new Map(spec.nouns.map(n=>[n.form,n]));
    const frames=new Map(frameList.map(f=>[f.lemma,f]));
    const licenses=spec.verb_overrides;
    if(Object.keys(licenses).length!==25)throw new GrammarError('Unexpected number of reviewed verbs');
    const resonances=new Set(spec.allowed_resonances);
    const allowed=(root,role)=>licenses[root]?.[role]||[];
    function noun(form,role,verb){
      const item=lex.get(form);
      if(!item)throw new GrammarError('Unknown or unlicensed '+role+': '+form);
      if(!allowed(verb,role).includes(item.class))
        throw new GrammarError(verb+' does not license '+role+' of type '+item.class);
    }
    function checkAtom(a){
      if(!a || typeof a!=='object' || Array.isArray(a))throw new GrammarError('Expected an action');
      if(a.type && a.type!=='atom')throw new GrammarError('Unknown action node type');
      const rule=licenses[a.verb],frame=frames.get(a.verb);
      if(!rule || !frame)throw new GrammarError('Verb or sense is not reviewed: '+(a.verb||'none'));
      noun(a.actor,'subject',a.verb);
      if(frame.required_roles.includes('object:-m')&&!a.patient)
        throw new GrammarError('Required object is missing');
      if(frame.frame==='V0'&&a.patient)
        throw new GrammarError('Intransitive action cannot take a direct object');
      if(frame.frame==='V2'&&!a.recipient)
        throw new GrammarError('Transfer requires a recipient');
      if(a.patient)noun(a.patient,'patient',a.verb);
      for(const role of ORDER){if(role!=='patient'&&a[role])noun(a[role],role,a.verb);}
      for(const [key,allowedValues] of [['tense',spec.tense_suffixes],['aspect',spec.aspect_suffixes],['modal',spec.modal_suffixes]]){
        if(!allowedValues.includes(a[key]||''))throw new GrammarError('Invalid '+key+' suffix');
      }
      for(const key of Object.keys(a)){
        if(!['type','actor','verb',...ORDER,'tense','aspect','modal','negated'].includes(key))
          throw new GrammarError('Unsupported action field: '+key);
      }
    }
    function checkSentence(s){
      if(!s || !resonances.has(s.resonance||'sen'))throw new GrammarError('Unknown opening resonance');
      if(!['statement','polar'].includes(s.mood||'statement'))throw new GrammarError('Unknown sentence mood');
      if(!['','reported_to_speaker','unknown_whether'].includes(s.attribution||''))
        throw new GrammarError('Unsupported embedded assertion');
      if(!spec.evidentials.includes(s.evidential||''))throw new GrammarError('Unsupported evidence marker');
      if(s.mood==='polar'&&s.attribution)throw new GrammarError('Direct and embedded question scopes cannot be mixed');
      if(s.evidential && (s.attribution || s.mood==='polar'))
        throw new GrammarError('Evidence marker conflicts with a question/report scope');
      const p=s.proposition;
      if(!p)throw new GrammarError('Sentence has no proposition');
      if(p.type==='atom')checkAtom(p);
      else if(p.type==='link'){
        if(!TEMPO[p.relation])throw new GrammarError('Unlicensed temporal/conditional connector');
        if(!p.first || !p.second || p.first.type!=='atom'||p.second.type!=='atom')
          throw new GrammarError('Nested links are outside this reviewed grammar subset');
        checkAtom(p.first);checkAtom(p.second);
        if(p.relation==='counterfactual'&&(p.first.tense||'')!=='te')
          throw new GrammarError('Past counterfactual requires a past antecedent');
      }else throw new GrammarError('Unknown proposition structure');
    }
    function cleanAtom(a){return {
      type:'atom',actor:a.actor,verb:a.verb,
      patient:a.patient||null,recipient:a.recipient||null,
      goal:a.goal||null,source:a.source||null,location:a.location||null,comitative:a.comitative||null,
      tense:a.tense||'',aspect:a.aspect||'',modal:a.modal||'',negated:!!a.negated
    }}
    function atomText(a){
      checkAtom(a);
      const words=[a.actor];
      for(const role of ORDER)if(a[role])words.push(a[role]+'-'+CASES[role]);
      if(a.negated)words.push('nu');
      words.push(a.verb+[a.tense,a.aspect,a.modal].filter(Boolean).map(x=>'-'+x).join(''));
      return words.join(' ');
    }
    function propositionText(p){
      if(p.type==='atom')return atomText(p);
      const left=atomText(p.first),right=atomText(p.second);
      return TEMPO[p.relation]+' '+left+', '+right+(p.relation==='counterfactual'?' qinë':'');
    }
    function render(s){
      checkSentence(s);
      let body=propositionText(s.proposition);
      if(s.attribution==='reported_to_speaker')body+=' do yano mi-tu shiri-te';
      if(s.attribution==='unknown_whether')body+=' he do mi nu sëmi';
      if(s.evidential)body+=' '+s.evidential;
      const opening=s.resonance||'sen';
      return opening+' '+body+((s.mood||'statement')==='polar'?' he?':'.');
    }
    function parseFinite(token){
      const pieces=token.split('-');
      if(pieces.length>4||!pieces[0]||pieces.some(x=>!x))
        throw new GrammarError('Malformed predicate ending');
      const [verb,...rest]=pieces;
      let i=0,tense='',aspect='',modal='';
      for(const [key,opts] of [['tense',['te','yu']],['aspect',['se','mo','në']],['modal',['ki','ho','du']]]){
        if(opts.includes(rest[i])){
          if(key==='tense')tense=rest[i];
          if(key==='aspect')aspect=rest[i];
          if(key==='modal')modal=rest[i];
          i++;
        }
      }
      if(i!==rest.length)throw new GrammarError('Wrong tense, aspect, or modal order');
      return {verb,tense,aspect,modal};
    }
    function parseAtom(text){
      if(!text||text.includes('  ')||/[,.?!«»]/.test(text))throw new GrammarError('Not a single finite action');
      let t=text.split(' ');
      if(t.length<2)throw new GrammarError('Missing subject or predicate');
      const pred=parseFinite(t.pop());
      const actor=t.shift();
      let negated=false;
      if(t.at(-1)==='nu'){negated=true;t.pop();}
      if(t.includes('nu'))throw new GrammarError('Negation must be immediately before the predicate');
      const reverse=Object.fromEntries(Object.entries(CASES).map(([k,v])=>[v,k]));
      const roles={};
      for(const arg of t){
        const k=arg.lastIndexOf('-');
        if(k<=0)throw new GrammarError('Argument requires a case marker');
        const form=arg.slice(0,k),role=reverse[arg.slice(k+1)];
        if(!role||role in roles)throw new GrammarError('Unknown or repeated case role');
        roles[role]=form;
      }
      const a=cleanAtom({actor,...pred,...roles,negated});
      checkAtom(a);
      return a;
    }
    function parseProposition(text){
      const i=text.indexOf(' '),head=i>=0?text.slice(0,i):text;
      if(head in REVERSE){
        let rem=text.slice(i+1),relation=REVERSE[head];
        if(rem.split(', ').length!==2)throw new GrammarError('Linked clauses require exactly two complete actions');
        if(relation==='counterfactual'){
          if(!rem.endsWith(' qinë'))throw new GrammarError('Unreal consequent is missing qinë');
          rem=rem.slice(0,-' qinë'.length);
        }
        const [left,right]=rem.split(', ');
        const p={type:'link',relation,first:parseAtom(left),second:parseAtom(right)};
        if(relation==='counterfactual'&&p.first.tense!=='te')
          throw new GrammarError('Unreal antecedent needs past tense');
        return p;
      }
      return parseAtom(text);
    }
    function parse(text){
      if(typeof text!=='string'||!text||text!==text.trim()||text.includes('\n')||text.includes('  '))
        throw new GrammarError('Noncanonical sentence spacing');
      const i=text.indexOf(' '),resonance=text.slice(0,i);
      if(i<0||!resonances.has(resonance))throw new GrammarError('Missing opening resonance');
      let body=text.slice(i+1),mood='statement',attribution='',evidential='';
      if(body.endsWith(' he?')){mood='polar';body=body.slice(0,-' he?'.length);}
      else if(body.endsWith('.'))body=body.slice(0,-1);
      else throw new GrammarError('A sentence must end in a period or he?');
      if(body.endsWith(' do yano mi-tu shiri-te')){
        attribution='reported_to_speaker';body=body.slice(0,-' do yano mi-tu shiri-te'.length);
      }else if(body.endsWith(' he do mi nu sëmi')){
        attribution='unknown_whether';body=body.slice(0,-' he do mi nu sëmi'.length);
      }else{
        for(const suffix of ['si','hu','ye']){
          if(body.endsWith(' '+suffix)){
            evidential=suffix;body=body.slice(0,-suffix.length-1);break;
          }
        }
      }
      const s={resonance,mood,attribution,evidential,proposition:parseProposition(body)};
      checkSentence(s);
      if(render(s)!==text)throw new GrammarError('Noncanonical case order or conflicting clause scope');
      return s;
    }
    function meaning(s){
      checkSentence(s);
      const p=s.proposition,atoms=p.type==='atom'?[p]:[p.first,p.second];
      const isQ=s.mood==='polar',reported=s.attribution==='reported_to_speaker',
        unknown=s.attribution==='unknown_whether',
        hypothetical=p.type==='link'&&['if','counterfactual'].includes(p.relation);
      return {
        roles:atoms.map(a=>({actor:a.actor,patient:a.patient||null,recipient:a.recipient||null,
          goal:a.goal||null,source:a.source||null,location:a.location||null,comitative:a.comitative||null,
          verb:a.verb,negated:!!a.negated,tense:a.tense||'',aspect:a.aspect||'',modal:a.modal||''})),
        relation:p.type==='link'?p.relation:'single',
        speech_act:isQ?'question':reported?'report':unknown?'ignorance_of_whether':'assertion',
        matrix_event_asserted:!(isQ||reported||unknown||hypothetical),
        conditional_antecedent_asserted:hypothetical?false:null,
        counterfactual:p.type==='link'&&p.relation==='counterfactual',
        report_source:reported?'indefinite_person':null,
        evidential:s.evidential||null,
        permissive_is_not_completed_action:atoms.some(a=>a.modal==='ho'),
        obligation_does_not_entail_completion:atoms.some(a=>a.modal==='du'),
        source_boundary:'exact 9.3 lexical license; no independent speaker verification'
      };
    }
    function candidateNouns(verb,role){
      return (spec.nouns||[]).filter(n=>allowed(verb,role).includes(n.class));
    }
    function atom({actor,verb,patient,recipient,goal,source,location,comitative,tense='',aspect='',modal='',negated=false}){
      return cleanAtom({actor,verb,patient,recipient,goal,source,location,comitative,tense,aspect,modal,negated});
    }
    return Object.freeze({parse,render,meaning,atom,checkAtom,checkSentence,candidateNouns,
      spec,frames:frameList,GrammarError,caseRoles:CASES});
  }
  root.QaroshiGrammar=Object.freeze({createGrammar,GrammarError});
})(typeof window!=='undefined'?window:globalThis);
