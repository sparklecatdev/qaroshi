#!/usr/bin/env python3
"""Temporary lemma diagnostics for the remaining 182 challenges."""
from pathlib import Path
import re,sys,json
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT),str(ROOT/"tools/stress83")]
from complete import Glosses
lex=Glosses().lex
TERMS={
"daily":"student;find;missing;key;teacher;open;room;gardener;water;seedling;leaf;green;musician;pack;instrument;trip;start;sooner;baker;burn;bread;customer;complain;driver;forget;direction;longer;child;hide;notebook;search;shopkeeper;count;coin;register;balance;traveler;lose;ticket;inspector;identification",
"motion":"climber;climb;summit;peak;guide;check;route;wind;strong;ambulance;depart;leave;station;dispatcher;confirm;address;alarm;stop;bicycle;market;road;narrow;streetlight;turn on;pilot;land;aircraft;runway;lights;appear;rain;heavier;hiker;return;camp;sunset;sun set;fire;ignite;light fire;train;platform;signal;change;crossing;reopen;rescue team;approach;cliff;radio;transmit;warning;tide;rise;ferry;passenger;captain;bell;ring;fog;clear;storm;end",
"social":"artist;customer;portrait;display;show;exhibit;traveler;companion;bed;spare;available;use;offer",
"evidence":"window;open;already;comet;disappear;cloud;behind;parcel;package;arrive;yesterday;return;bridge;crack;overnight;night;dancer;miss;cue;signal;conductor;stop playing;play;performance;sensor;detect;movement;motion",
"relative":"book;student;borrow;last;final;end;page;absent;missing;librarian;shelf;tear;pull;remove;out;letter;arrive;name;nameless;warn;warning;sender;contact;envelope;damaged;faulty;replacement part;dog;follow;cyclist;owner;search;looking;choir;rehearse;shorter;expected;concert;finish;early;verse;omit;photograph;saved;show;mountain;wrong;map;correct;camera;clock;message;forward;group;explanation;story;invent;make;create;confuse;confusion;adult;ask;detail;character;identical",
"counter":"traveler;take;early;train;ticket;sold out;noon;arrive;gardener;tree;save;roots;damage;courtyard;shade;pilot;avoid;storm;radar;unavailable;passenger;land;sooner;librarian;replace;book;damaged;replacement;not arrived;reader;chapter;musician;finish;concert;power;failed;audience;hear;last song;volunteer;open;shelter;misplaced;key;guests;enter;safely;captain;ship;reach;island;current;strong;crew;rest;earlier",
"instrument":"roller;paint roller;fence;gardener;paint;technician;calibrate;sensor;reference device;reference;instrument;artist;wall;decorate;colored tile;tile;carpenter;assemble;table;wooden peg;peg;worker;secure;door;steel lock;lock",
"narrative":"sky;swallow;light;sunset;sunset arrive;last light;destroy;astronomy;cosmic;old;house;history;atmosphere;brain;storm;knock;door;wind;rain;strike;entrance;polite;request;road;abandon;path;lost;history;fire;paint;room;gold;golden;yellow;warm;colored;glow;flame;paintbrush;brush",
"technical":"battery;overheat;safety;electric circuit;electrical circuit;circuit;charge;charging;stop;charger;defective;network;connection;drop;server;attacked;attack;malicious;cyberattack;telescope;observer;noise;rule out;exclude;eliminate;signal;alien;extraterrestrial;civilization;contract;signature;void;invalid;automatically;legal"
}
for group,terms in TERMS.items():
  for term in terms.split(";"):
    def valid(row):
      return bool(re.search(r"\b"+re.escape(term)+r"\b",row["english"],re.I))
    hits=[r for r in lex if valid(r)]
    hits.sort(key=lambda row:(row["english"].casefold().split(";")[0].strip()!=term,
                              row["english"].casefold()!=term,
                              row["pos"] not in ("n","v","adj","adv","conj","part"),
                              len(row["english"]),row["id"]))
    print("PROBE",group,term,json.dumps([{"id":r["id"],"q":r["qaroshi"],"pos":r["pos"],"en":r["english"]} for r in hits[:4]],ensure_ascii=False))
