"""Additional conservative Qaroshi 8.3 source-grounded clause experiments.

Returned phrases are deliberately *hypotheses*. English morphology is decoded
only to locate a canonical indexing gloss; no independent native acceptance.
"""
from __future__ import annotations
import re

IRREGULAR = {
 "left":"leave","went":"go","came":"come","found":"find","fell":"fall",
 "grew":"grow","took":"take","bought":"buy","saw":"see","wrote":"write",
 "forgot":"forget","forgotten":"forget","hid":"hide","hidden":"hide",
 "brought":"bring","thought":"think","told":"tell","made":"make",
 "sent":"send","held":"hold","kept":"keep","lost":"lose","paid":"pay",
 "stood":"stand","flew":"fly","ran":"run","read":"read","cut":"cut",
 "heard":"hear","rang":"ring","began":"begin","ended":"end",
 "was":"be","were":"be","did":"do","had":"have","put":"put",
}
def base(s):
 s=s.casefold().strip()
 if s in IRREGULAR:return IRREGULAR[s]
 if s.endswith("ied"):return s[:-3]+"y"
 if s.endswith("ed"):
  t=s[:-2]
  if t.endswith(("pp","tt","nn","gg","rr","ll")):t=t[:-1]
  return t
 if s.endswith("s") and not s.endswith("ss"):return s[:-1]
 return s

def find_sentence(s, lex):
 """Recognize one simple third-person clause, rejecting unchecked syntax."""
 s=s.lower().strip(" .!?")
 passive=re.fullmatch(r"(?:the|a) ([a-z-]+) (?:was|were) ([a-z-]+)",s)
 if passive:
  who,verb=passive.groups()
  n,ni,_=lex.choose(who,"n")
  v,vi,_=lex.choose(base(verb),"v")
  if n and v:
   return {"qr":n+" "+v+"-li-te","witnesses":[("patient",who,n,ni),("predicate",base(verb),v,vi)],
           "warning":"passive requires lexical voice license; cannot be certified by suffix alone"}
 simple=re.fullmatch(r"(?:the|a) ([a-z-]+) ([a-z-]+)(?: (?:the|a) ([a-z-]+))?",s)
 if not simple:return None
 who,verb,obj=simple.groups()
 n,ni,_=lex.choose(who,"n")
 v,vi,_=lex.choose(base(verb),"v")
 if not n or not v:return None
 witness=[("subject",who,n,ni),("predicate",base(verb),v,vi)]
 phrase=n
 if obj:
  o,oi,_=lex.choose(obj,"n")
  if not o:return None
  phrase+=" "+o+"-m"
  witness.append(("object",obj,o,oi))
 return {"qr":phrase+" "+v+"-te","witnesses":witness,
         "warning":"source indexing senses; verb arguments and event interpretation require review"}

def build_one(domain,idx,variant,lex):
 import scenarios
 if domain=="time_motion":
  who,past,bare,after,before=scenarios.MOTION[idx]
  first=find_sentence(who+" "+past,lex)
  second=find_sentence(after,lex)
  third=find_sentence(before,lex)
  if variant in (1,3) and first and second:
   connective="ana" if variant==1 else "tëwaro"
   q=("sen "+connective+" "+first["qr"]+", "+second["qr"]+".")
   return q,first["witnesses"]+second["witnesses"],"Temporal subclause ordering and valency must be checked"
  if variant==2 and first and third:
   return "sen ëna "+third["qr"]+", "+first["qr"]+".",first["witnesses"]+third["witnesses"],"Earlier-than temporal scope requires review"
  if variant==4 and first and third:
   return "sen "+first["qr"].replace(" "+first["qr"].split(" ")[-1]," nu "+first["qr"].split(" ")[-1])+" torëne "+third["qr"]+".", first["witnesses"]+third["witnesses"],"Until-implicature and exact event boundary must be checked"
  if variant==5 and first and second:
   return "hë "+first["qr"]+" ëna "+second["qr"]+" he?",first["witnesses"]+second["witnesses"],"Question scope across two finite temporal clauses requires review"
 if domain=="counterfactual_modal":
  who,base_action,part,barrier,consequence=scenarios.COUNTER[idx]
  action=find_sentence(who+" "+part,lex)
  # Fallback: the English perfect participle should locate base lexical verb.
  result=find_sentence(consequence.replace(" would have "," "),lex)
  if variant==1 and action and result:
   return "sen wënu "+action["qr"]+", "+result["qr"]+".",action["witnesses"]+result["witnesses"],"Past contrary-to-fact and resultant-event status require manual interpretation"
  if variant in (2,3,4) and action:
   baseform=action["qr"].rsplit(" ",1)
   root=baseform[-1]
   if root.endswith("-te"):root=root[:-3]
   modal={2:"-ki",3:"-ho",4:"-du"}[variant]
   q="sen "+baseform[0]+" "+root+modal+"."
   # The barrier/concession is not translated, so this is deliberately
   # PARTIAL and must not be returned as a complete full sentence.
   return None,action["witnesses"],"Only modal core located; the full English concessive proposition remains untranslated"
 if domain=="technical_precision":
  claim,consequence,unsupported=scenarios.TECH[idx]
  p=find_sentence(claim,lex)
  if p and variant in (1,2):
   # The documented report/document statement needs a separate matrix
   # predicate with explicit source; even a plausible string is provisional.
   narrator="shiri-te" if variant==1 else "shiroli-te"
   n="rërawëhu" if variant==1 else "sa"
   return "sen "+p["qr"]+" do "+n+" "+narrator+".",p["witnesses"],"Report-author attribution and technical vocabulary require sense validation"
  if p and variant==3:
   return "zher "+p["qr"]+" ye.",p["witnesses"],"Inference is not automatically independent verification; English caveat needs explicit wording"
 if domain=="embedding_reference":
  head,predicate,consequence,reason=scenarios.EMBED[idx]
  # Avoid silently dropping identity in complex relatives. The 8.1 he/do
  # rule alone cannot license the missing referent and relative sha.
  return None,[],"Relative head, reference tracking and selectional verbs require individually specified structures"
 if domain=="social_consent":
  return None,[],"Consent/revocation require lexical verb frames, not automatic warm resonance"
 if domain=="narrative_figures":
  return None,[],"An English metaphor needs a source-licensed Qaroshi literal paraphrase or deliberately new literary convention"
 return None,[],"No additional source-grounded pattern in this restricted composer"
