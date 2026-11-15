#!/usr/bin/env python3
"""Pronunciation sketches for noncanonical lexical proposals; NOT new dictionary entries."""
import csv,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools'))
from phonetics import ipa_word,guide_word,sound_out_word
p=ROOT/'data/v16_2/eight_root_decision_dossiers.csv'
with p.open(encoding='utf8',newline='') as f: rows=list(csv.DictReader(f))
for x in rows:
 w=x['tentative_form'];x['provisional_ipa']=ipa_word(w);x['provisional_syllabification']=guide_word(w);x['provisional_sound_out']=sound_out_word(w)
with p.open('w',encoding='utf8',newline='') as f:
 writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
print('Pronunciation candidates:',len(rows))
