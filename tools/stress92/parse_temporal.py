"""Bounded source-linked Qaroshi structural interpreter for unseen event pairs.

Unlike the stress92 renderer this independently parses the surface string and
recovers its event IDs, ordering, attribution and actual-world assertion
commitments. It deliberately abstains on all unlisted lexical frames. It is
not a Qaroshi-wide parser or independent English-meaning verification.
"""
from __future__ import annotations
import json
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MOTION = ROOT / "data/standard_8/motion_frames_9_1.json"


class Undecodable(ValueError):
    pass


@dataclass(frozen=True)
class Interpretation:
    main_family: int
    endpoint_family: int
    relation: str
    matrix_event_asserted: bool
    indefinite_source_report: bool
    direct_polar_question: bool
    implied_event_causation: bool = False


def _lexical_frames()->tuple[dict[str,int],dict[str,int]]:
    events=json.loads(MOTION.read_text(encoding="utf8"))
    mains={x["main"]:int(x["family"]) for x in events}
    ends={x["before"]:int(x["family"]) for x in events}
    assert len(mains)==len(ends)==10
    return mains,ends


def parse(q:str)->Interpretation:
    if "\n" in q or "  " in q:
        raise Undecodable("Noncanonical whitespace")
    if "-ki-te" in q or "-ho-te" in q or "-du-te" in q:
        raise Undecodable("Bad tense/modality ordering")
    main,ends=_lexical_frames()
    reported=False
    question=False
    if q.startswith("sen ana ") and q.endswith(" do yano mi-tu shiri-te."):
        reported=True
        relation="reported_after"
        center=q[len("sen ana "):-len(" do yano mi-tu shiri-te.")]
    elif q.startswith("sen ana ") and q.endswith("."):
        relation="after"
        center=q[len("sen ana "):-1]
    elif q.startswith("sen ëna ") and q.endswith("."):
        relation="before"
        center=q[len("sen ëna "):-1]
    elif q.startswith("sen yaro ") and q.endswith("."):
        relation="when"
        center=q[len("sen yaro "):-1]
    elif q.startswith("hë ëna ") and q.endswith(" he?"):
        relation="question_before"
        question=True
        center=q[len("hë ëna "):-len(" he?")]
    else:
        raise Undecodable("Unsupported clause operator, evidence or question form")
    # A comma unambiguously divides the two independently source-licensed
    # finite propositions. It does not permit omitted roles or invented verbs.
    clauses=center.split(", ")
    if len(clauses)!=2 or not all(clauses):
        raise Undecodable("Must contain exactly two complete event clauses")
    left,right=clauses
    if relation in ("after","reported_after"):
        event1,event2=left,right
    else:
        event1,event2=right,left
    if event1 not in main or event2 not in ends:
        raise Undecodable("Unlicensed event predicate, actor, patient or endpoint")
    first,second=main[event1],ends[event2]
    if first==second:
        raise Undecodable("Original same-family pair is not held out")
    return Interpretation(
        main_family=first,endpoint_family=second,relation=relation,
        matrix_event_asserted=not (reported or question),
        indefinite_source_report=reported,direct_polar_question=question,
    )


def parse_not_until_two_sentences(text:str)->dict:
    """Check a complete phase-negative and LATER positive event.

    A negative until-clause without the independently stated later P cannot
    entail positive P; repeating the same endpoint preserves anaphora.
    """
    if not text.startswith("sen torëne ") or ". sen ana " not in text or not text.endswith("."):
        raise Undecodable("Not-until requires two independent finite statements")
    early,later=text.split(". sen ana ",1)
    early=early[len("sen torëne "):]
    boundary,sep,neg=early.partition(", ")
    later_boundary,sep2,positive=later[:-1].partition(", ")
    if not sep or not sep2 or boundary!=later_boundary:
        raise Undecodable("Two statements require the same explicit endpoint")
    if " nu " not in neg:
        raise Undecodable("Pre-boundary main predicate is not explicitly negated")
    expected=neg.replace(" nu "," ",1)
    if expected!=positive:
        raise Undecodable("Different main-event role or negation placement")
    mains,ends=_lexical_frames()
    if positive not in mains or boundary not in ends:
        raise Undecodable("Unlicensed main or endpoint")
    if mains[positive]==ends[boundary]:
        # The original same-family not-until is allowed by this parser; it
        # is not part of the heldout cross-family suite.
        pass
    return {
        "main_family":mains[positive],
        "endpoint_family":ends[boundary],
        "negative_before_boundary":True,
        "positive_event_asserted_later":True,
        "same_endpoint":True,
        "causation_asserted":False,
    }
