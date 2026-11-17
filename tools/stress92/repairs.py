"""Versioned, evidence-linked surface corrections applied ONLY to the 9.2 view."""
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
REGISTRY=ROOT/"data/standard_9_2/semantic_repairs.json"

def apply(rows:list[dict])->tuple[list[dict],list[dict]]:
    document=json.loads(REGISTRY.read_text(encoding="utf8"))
    patches={x["case_id"]:x for x in document["corrections"]}
    assert len(patches)==len(document["corrections"])==1
    old_ids={r["id"] for r in rows}
    assert set(patches).issubset(old_ids)
    out=[]
    changed=[]
    for original in rows:
        row=dict(original)
        id_=row["id"]
        row["prior_9_1_editorial_candidate"]=original["qaroshi_full_candidate"]
        row["9_2_correction_reason"]=""
        if id_ in patches:
            patch=patches[id_]
            assert row["english"]==patch["english_target"],(id_,"source English mismatch")
            assert row["qaroshi_full_candidate"]==patch["previous_9_1"],(id_,"original proposal moved")
            assert patch["current_9_2"]!=patch["previous_9_1"]
            assert patch["current_9_2"].endswith(" qinë.")
            row["qaroshi_full_candidate"]=patch["current_9_2"]
            row["9_2_correction_reason"]=patch["reason"]
            changed.append(id_)
        out.append(row)
    assert changed==sorted(patches)
    assert len(out)==len(rows)==500
    assert document["independently_speaker_verified"] is False
    assert document["old_originals_preserved"] is True
    return out,document["corrections"]
