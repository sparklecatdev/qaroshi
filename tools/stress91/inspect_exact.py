#!/usr/bin/env python3
"""Temporary source spot checks: no editorial translations are inferred."""
import sys,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT),str(ROOT/"tools/stress83")]
from complete import Glosses
lex=Glosses().lex
roots="tika daru eri goro yëla këna zhëmiro shërawëmi shërawëhe shërawëro shiwari shëliro shërawëhu shërawëro gura shërawë shënawë zhëmiwa wënarë subali për?".split()
for q in roots:
  found=[x for x in lex if x["qaroshi"]==q]
  print("ROOT",q,json.dumps([{"id":x["id"],"en":x["english"],"pos":x["pos"]} for x in found[:5]],ensure_ascii=False))
for id_ in ("Q004439","Q000953","Q000952","Q000?daru","Q004444","Q004491","Q004500","Q004949","Q004066","Q5001714"):
  found=[x for x in lex if x["id"]==id_]
  print("CHECKID",id_,json.dumps([{"qaroshi":x["qaroshi"],"en":x["english"]} for x in found],ensure_ascii=False))
