#!/usr/bin/env python3
"""Diagnostic, not new grammar. Explore original source glossary for unsolved cases."""
import json,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT),str(ROOT/"tools/stress83")]
from complete import Glosses
from tools.stress81.scenarios import EMBED,COUNTER,NARRATIVE,TECH,MOTION,SOCIAL,EVIDENCE,DAILY
lex=Glosses().lex
TERMS = {
    "relative": "relative clause;person;called;call;yesterday;left;sunrise;book;borrow;missing;last page;last;page;librarian;shelves;shelf;tear;letter;arrive;nameless;name;warn;warning;sender;envelope;damage;machine;engineer;repair;stop;again;team;inspect;wiring;wire;replacement;faulty;dog;follow;cyclist;wait;near;bridge;owner;busy;road;song;choir;rehearse;short;expected;concert;finish;early;verse;omit;photograph;save;mountain;map;wrong;camera;clock;moderator;delete;forward;disclose;private;data;group;explanation;medicine;patient;request;available;doctor;suggest;alternative;shipment;delay;story;child;invent;confuse;adult;detail;characters;identical",
    "technical": "battery;overheat;safety circuit;charge;charging;charger;defective;audit log;incomplete;investigator;record;operator;delete;evidence;network connection;disconnect;drop;client;retry;server;attack;laboratory;sample;contaminate;experiment;repeat;hypothesis;false;encrypt;encrypted;file;copy;access key;rotate;decrypt;contents;temperature sensor;drift;measurement;calibrate;equipment;permanent;damage;patient record;error;clinician;verify;source;dishonest;bridge inspection;corrosion;engineer;assess;structure;collapse;telescope;record;faint;signal;observer;noise;alien;civilization;contract;signature;party;clarification;void;prove;inference;possibly;possible;independently;verify;report;assert",
    "narrative": "sky;swallow;last light;light;sunset;forest;keep;secret;clock;argue;silence;river;carry;thousand;memory;town;hold;breath;mountain;refuse;move;old house;house;remember;winter;storm;knock;door;road;forget;traveler;fire;paint;room;gold;warm;colored;poet;narrator;story;sentence;word;quote;read;reading;interpret;figurative;metaphor;literal;actually;think;first;correct;intention;suggest;imagine;fiction;personify",
    "counterfactual": "courier;deliver;letter;address;unreadable;recipient;reply;travel;traveler;early train;train;ticket;sold out;arrive;noon;garden;gardener;save;tree;root;badly;damage;courtyard;shade;student;solve;equation;variable;class;understand;proof;pilot;avoid;storm;radar;unavailable;passenger;land;sooner;librarian;replace;damaged book;book;reader;chapter;musician;finish;concert;power;fail;audience;hear;last song;mechanic;repair;engine;part;missing;vehicle;start;volunteer;open;shelter;key;misplace;guest;enter;safely;captain;reach;island;current;strong;crew;rest;earlier;able;ability;permission;allowed;must;obligation;despite;barrier",
    "consent": "consent;withdraw consent;revoke;permission;explicit;silently;leave;departure;silence;prior;before;action;not treat as consent;offer;reject;decline;refuse;informed;ask;request;grant;authorization;boundary;change;undo;earlier;statement;take back",
    "motion":"courier;river;cross;bridge;inspect;storm;end;passenger;board;ferry;captain;bell;sound;fog;clear;climber;summit;guide;route;check;wind;grow;strong;ambulance;leave;station;dispatcher;confirm;address;alarm;stop;bicycle;pass;market;road;narrow;streetlight;light up;pilot;land;aircraft;runway;light;appear;rain;heavy;tourist;museum;enter;door;open;exhibition;begin;hiker;return;camp;sun;set;fire;ignite;train;platform;signal;change;crossing;reopen;rescue team;approach;cliff;radio;transmit;warn;tide;rise"
}
for group, terms in TERMS.items():
    for term in terms.split(";"):
        needle=re.compile(r"\b"+re.escape(term)+r"\b",re.I)
        hits=[l for l in lex if needle.search(l["english"])]
        hits.sort(key=lambda l:(
            not l["english"].casefold().split(";")[0].strip()==term,
            l["pos"] not in ("n","v","adj","adv"),
            l["type"] not in ("headword","core"),
            len(l["english"]),l["id"]))
        print("GLOSS",group,term,json.dumps([{"id":v["id"],"word":v["qaroshi"],"pos":v["pos"],"meaning":v["english"]} for v in hits[:3]],ensure_ascii=False))
