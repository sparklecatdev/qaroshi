#!/usr/bin/env python3
"""Create independent-reader trial materials and score supplied human judgments.

This script never fills participant data or claims independent comprehension.
The answer key is distributed separately but is not cryptographically secret.
"""
from __future__ import annotations
import argparse,collections,csv,hashlib,json,random
from pathlib import Path
from tools.standard10.resources import assemble

SEED=10010
N_ITEMS=80
VALID=("meaning_preserved","partial","incorrect","cannot_determine")

def write_csv(path,rows,fields):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields,extrasaction="ignore")
        w.writeheader();w.writerows(rows)

def read_csv(path):
    with Path(path).open(encoding="utf-8-sig",newline="") as f:
        return list(csv.DictReader(f))

def build(out):
    source=assemble();rng=random.Random(SEED)
    pools=collections.defaultdict(list)
    for dialogue in source["dialogues"]:
        for idx,t in enumerate(dialogue["turns"]):
            if len(t["qaroshi"].split())<3 or len(t["english"])<10:continue
            prior=dialogue["turns"][idx-1]["qaroshi"] if idx else ""
            pools[dialogue["source"]].append((dialogue,idx,t,prior))
    picks=[]
    for pool in pools.values():
        rng.shuffle(pool);used=collections.Counter()
        for item in pool:
            if used[item[0]["id"]]>=3:continue
            used[item[0]["id"]]+=1;picks.append(item)
    rng.shuffle(picks)
    unique=set();selected=[]
    for d,i,t,prior in picks:
        key=(t["qaroshi"].casefold(),prior.casefold())
        if key in unique:continue
        unique.add(key);selected.append((d,i,t,prior))
        if len(selected)==N_ITEMS:break
    if len(selected)!=N_ITEMS:raise ValueError("Insufficient independent trial prompts")
    reader=[];key=[];empty=[]
    for i,(d,idx,t,prior) in enumerate(selected,1):
        id_=f"BL10-{i:03d}"
        reader.append({
            "item_id":id_,"previous_qaroshi_context":prior,
            "target_qaroshi":t["qaroshi"],
            "task":"Without an English key, paraphrase the target and identify actor, roles, negation, uncertainty and permission when relevant.",
        })
        key.append({
            "item_id":id_,"scene_id":d["id"],"title":d["title"],
            "source_path":d["source"],"turn_number":idx+1,
            "contextual_editorial_english":t["english"],
            "literal_editorial_english":t["literal_english"],
            "status":d["status"],
            "warning":"Editorial target is not independently certified semantic truth.",
        })
        empty.append({
            "item_id":id_,"reader_anonymous_code":"","first_pass_english_paraphrase":"",
            "actor_object_scope_notes":"","uncertainty_0_to_3":"",
            "adjudicator_anonymous_code":"","semantic_rating":"",
            "adjudicator_notes":"","reader_confirmed_no_key_access":"",
        })
    write_csv(out/"learner_blind_items.csv",reader,list(reader[0]))
    write_csv(out/"facilitator_english_key.csv",key,list(key[0]))
    write_csv(out/"empty_response_and_adjudication.csv",empty,list(empty[0]))
    report={
        "items":N_ITEMS,"scenes":len({d[0]["id"] for d in selected}),
        "sources":dict(collections.Counter(d[0]["source"] for d in selected)),
        "blinded_reader_answer_rows":0,"human_adjudications":0,
        "reader_sheet_sha256":hashlib.sha256(json.dumps(reader,ensure_ascii=False,sort_keys=True).encode()).hexdigest(),
        "item_status":"editorial stimuli, unvalidated independent comprehension",
        "warning":"Keeping the key and reader sheet in separate files does not make a public GitHub key secret.",
    }
    (out/"manifest.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    protocol="""# Standard 10 independent comprehension protocol

No participants, responses or independent outcomes are created by these scripts.

1. Recruit volunteers who did not author or previously read the source scenes. Obtain consent and assign anonymous codes without putting names, handles or raw chats in the public repository.
2. Distribute ONLY learner_blind_items.csv, with the full facilitator_english_key.csv withheld from readers. The key is NOT cryptographically sealed, especially if visible in public GitHub Actions.
3. Randomize reading order across people. First collect a free English paraphrase, actor and participant identifications, negation, certainty, evidence source, permission vs ability, and a confidence/uncertainty rating. Accept 'cannot determine' rather than forcing guesses.
4. Retain first-pass responses. A second human adjudicator compares them with the source English key, noting ambiguity and any questionable original editorial gloss. Record one of meaning_preserved, partial, incorrect, cannot_determine plus reasons. Do not use edit distance as semantic proof.
5. Separate independently recruited reading from self-study after browsing the Wiki. Check whether readers accessed the key and report this limitation.
6. Keep filled response forms confidential; do not upload identifying participant data. This script accepts a human completed table and reports supplied judgments, not proof of independent fluency.
7. Run python tools/standard10/trial.py --score path/to/filled_responses.csv --out path/to/report.json only after real data are collected.

Historical editorial examples are stimuli, not spontaneous native speech. This protocol cannot validate its own English answer key; disagreements require documented editorial correction or independent adjudication.
"""
    (out/"PROTOCOL.md").write_text(protocol,encoding="utf-8")
    return report

def score(path):
    respondents=collections.defaultdict(list)
    seen=set()
    required=("item_id","reader_anonymous_code","first_pass_english_paraphrase",
              "adjudicator_anonymous_code","semantic_rating","reader_confirmed_no_key_access")
    for row in read_csv(path):
        if not any(row.get(k,"").strip() for k in required[1:]):continue
        for k in required:
            if not row.get(k,"").strip():raise ValueError("Incomplete human response field "+k)
        id_=row["item_id"]
        if not id_.startswith("BL10-") or len(id_)!=8 or not id_[-3:].isdigit() or not 1<=int(id_[-3:])<=N_ITEMS:
            raise ValueError("Unknown trial item "+id_)
        if row["semantic_rating"] not in VALID:raise ValueError("Rating must be one of "+str(VALID))
        if row["reader_confirmed_no_key_access"] not in ("yes","no","unsure"):
            raise ValueError("Key-access declaration must be yes/no/unsure")
        pair=(row["reader_anonymous_code"],id_)
        if pair in seen:raise ValueError("Duplicate reader item "+repr(pair))
        seen.add(pair);respondents[row["reader_anonymous_code"]].append(row)
    if not respondents:raise ValueError("No completed human responses, so comprehension cannot be scored")
    readers=[];totals=collections.Counter()
    for code,rows in sorted(respondents.items()):
        c=collections.Counter(x["semantic_rating"] for x in rows)
        totals.update(c)
        readers.append({
            "reader_anonymous_code":code,"answered":len(rows),
            "ratings":dict(c),
            "meaning_preserved_fraction":round(c["meaning_preserved"]/len(rows),4),
            "no_key_access_yes":sum(x["reader_confirmed_no_key_access"]=="yes" for x in rows),
        })
    return {
        "status":"Results from a supplied human-filled CSV; authorship and independence cannot be software authenticated",
        "reviewers":len(readers),"rated_items":sum(map(len,respondents.values())),
        "rating_counts":dict(totals),"readers":readers,
        "warning":"A submitted score does not establish native-like proficiency or correctness of the editorial answer key.",
    }

if __name__=="__main__":
    p=argparse.ArgumentParser()
    mode=p.add_mutually_exclusive_group(required=True)
    mode.add_argument("--build",action="store_true")
    mode.add_argument("--score")
    p.add_argument("--out",required=True)
    args=p.parse_args()
    if args.build:result=build(Path(args.out))
    else:
        result=score(Path(args.score))
        path=Path(args.out)
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,ensure_ascii=False,indent=2))
