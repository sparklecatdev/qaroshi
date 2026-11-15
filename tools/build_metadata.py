#!/usr/bin/env python3
"""Generate auxiliary indexes and schema documentation data for Qaroshi 2.0."""
from pathlib import Path
from collections import Counter
import csv,json
ROOT=Path(__file__).resolve().parents[1]
rows=list(csv.DictReader((ROOT/'data/lexicon.csv').open(encoding='utf-8-sig')))
reverse=[]
for r in rows:
 for alias in r['english'].split(';'):
  reverse.append({'english':alias.strip(),'qaroshi':r['qaroshi'],'pos':r['pos'],
                  'domain':r['domain'],'review':r['review'],'edition':r['edition'],'id':r['id']})
reverse.sort(key=lambda r:(r['english'].lower(),r['pos'],r['qaroshi']))
with (ROOT/'data/english_index.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=['english','qaroshi','pos','domain','review','edition','id']);w.writeheader();w.writerows(reverse)
res=[('më','Warm Hum','affection, tenderness, vulnerability'),('zha','Bright Trill','excitement, play, delight'),('qor','Deep Resonance','solemnity, promises, authority'),('sen','Still Voice','neutral information'),('hë','Seeking Call','sincere inquiry, curiosity'),('lën','Hidden Hum','shyness, bashfulness'),('sur','Falling Song','grief, sadness'),('rak','Rough Growl','anger, defiance'),('khar','Sharp Cry','alarm, fear'),('yë','Rising Echo','wonder, surprise'),('nëm','Quiet Breath','contentment, peace'),('wen','Distant Call','longing'),('dal','Firm Pulse','determination, resolve'),('rëm','High Crest','pride, triumph'),('hol','Open Heart','gratitude'),('zher','Broken Echo','doubt, suspicion')]
(ROOT/'data/resonances.json').write_text(json.dumps([{'marker':w,'name':name,'meaning':gloss,'mandatory_sentence_initial':True} for w,name,gloss in res],indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
pron={'mi':'I/me','ti':'you (singular)','sa':'they (singular)','naru':'we (inclusive)','muru':'we (exclusive)','tiri':'you (plural)','sari':'they (plural)','miyo':'one/people generally','yano':'someone','nura':'nobody'}
(ROOT/'data/pronouns.json').write_text(json.dumps([{'form':k,'english':v} for k,v in pron.items()],indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
import sys
sys.path.insert(0,str(ROOT/'source'))
from functional_v2 import MORPHEMES,FUNCTIONS
(ROOT/'data/morphemes.json').write_text(json.dumps([{'form':x[0],'category':x[1],'meaning':x[2],'rule':x[3]} for x in MORPHEMES],ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(ROOT/'data/grammatical_particles_v2.json').write_text(json.dumps([{'form':x[0],'pos':x[1],'english':x[2],'rule':x[3]} for x in FUNCTIONS],ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('English index',len(reverse),'resonances',len(res),'pronouns',len(pron))

from functional_v3 import FUNCTIONS_V3
from morphemes_v3 import MORPHEMES_V3
(ROOT/'data/grammatical_particles_v3.json').write_text(json.dumps(
 [{'form':x[0],'pos':x[1],'english':x[2],'rule':x[3],'review':'proposed'} for x in FUNCTIONS_V3],
 ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(ROOT/'data/morphemes_v3.json').write_text(json.dumps(MORPHEMES_V3,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
