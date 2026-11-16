#!/usr/bin/env python3
"""Score independent blind comprehension responses without fabricating results.

Usage:
  python tools/standard_8/score_comprehension.py --blank responses.csv
  python tools/standard_8/score_comprehension.py --responses responses.csv --out report.json

The answer key is kept in a SEPARATE file and should not be given to learners.
No human data, names, or audio are included in the public test distribution.
"""
from __future__ import annotations
import argparse,collections,csv,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def read(path):
 with Path(path).open(encoding='utf8',newline='') as f:return list(csv.DictReader(f))
def blank(path):
 items=read(ROOT/'data/standard_8/blind_comprehension_prompts.csv')
 with Path(path).open('w',encoding='utf8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=['id','choice','reviewer_anonymous_code','comment'],lineterminator='\n')
  w.writeheader();w.writerows({'id':x['id'],'choice':'','reviewer_anonymous_code':'','comment':''} for x in items)
 return len(items)
def score(responses):
 answers={x['id']:x for x in read(ROOT/'data/standard_8/sealed_answer_key.csv')}
 cats={x['id']:x['category'] for x in read(ROOT/'data/standard_8/blind_comprehension_prompts.csv')}
 respondents=collections.defaultdict(dict)
 for x in read(responses):
  i=x.get('id','').strip();c=x.get('choice','').strip().upper();name=x.get('reviewer_anonymous_code','').strip()
  if not name or not c:continue
  if i not in answers:raise ValueError('Unknown question ID '+i)
  if c not in 'ABC' or len(c)!=1:raise ValueError('Invalid choice for '+i)
  if i in respondents[name]:raise ValueError('Duplicate reviewer+item: '+name+' '+i)
  respondents[name][i]=c
 if not respondents:raise ValueError('No responses: no proficiency or comprehension outcomes can be claimed')
 summary=[];confusion=collections.Counter()
 for user,resp in sorted(respondents.items()):
  per={}
  for category in sorted(set(cats.values())):
   answered=[i for i in resp if cats[i]==category]
   n=sum(resp[i]==answers[i]['correct'] for i in answered)
   per[category]={'answered':len(answered),'correct':n,'accuracy':round(n/len(answered),4) if answered else None}
   for i in answered:
    if resp[i]!=answers[i]['correct']:confusion[i]+=1
  summary.append({'reviewer_anonymous_code':user,'answered':len(resp),'overall_accuracy':round(sum(resp[i]==answers[i]['correct'] for i in resp)/len(resp),4),'categories':per})
 return {'status':'actual submitted blind answers only','reviewers':len(respondents),'results':summary,
  'most_confused_items':[{'id':i,'incorrect_responses':n} for i,n in confusion.most_common(50)],
  'human_review_required':'These scores measure closed-source matching, not spontaneous fluency or independently validated native usage.'}
if __name__=='__main__':
 ap=argparse.ArgumentParser();mode=ap.add_mutually_exclusive_group(required=True);mode.add_argument('--blank');mode.add_argument('--responses');ap.add_argument('--out');args=ap.parse_args()
 if args.blank:print('Blank response rows:',blank(args.blank))
 else:
  result=score(args.responses)
  data=json.dumps(result,ensure_ascii=False,indent=2)+'\n'
  if args.out:Path(args.out).write_text(data,encoding='utf8')
  else:print(data)
