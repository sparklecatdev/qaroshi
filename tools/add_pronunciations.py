#!/usr/bin/env python3
"""Annotate all Qaroshi reference datasets with broad IPA and stress guides."""
from pathlib import Path
import csv,json
from phonetics import ipa_word, guide_word, ipa_text, guide_text, sound_out_word, sound_out_text, IPA, LETTERS
ROOT = Path(__file__).resolve().parents[1]


def read_csv(path):
    with path.open(encoding='utf-8-sig',newline='') as f:
        return list(csv.DictReader(f))


def save_csv(path, rows):
    with path.open('w',encoding='utf-8-sig',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]))
        writer.writeheader();writer.writerows(rows)


def save_json(path, rows):
    path.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


def amend_word(w, key):
    form=w[key]
    # Strip hyphen from free-standing suffix notation, but preserve the morphological data.
    w['ipa'] = ipa_word(form.strip('-'))
    w['reading'] = guide_word(form.strip('-'))
    w['sound_out'] = sound_out_word(form.strip('-'))


def annotate_rows(path, field, is_sentence=False):
    rows = read_csv(ROOT/path)
    for r in rows:
        if is_sentence:
            r['ipa']=ipa_text(r[field]);r['reading']=guide_text(r[field]);r['sound_out']=sound_out_text(r[field])
        else:amend_word(r,field)
    save_csv(ROOT/path,rows)
    save_json((ROOT/path).with_suffix('.json'),rows)
    return len(rows)


def annotate_json(path, key):
    p=ROOT/path
    rows=json.loads(p.read_text(encoding='utf-8'))
    for r in rows:amend_word(r,key)
    save_json(p,rows)
    return len(rows)


def main():
    words=annotate_rows(Path('data/lexicon.csv'),'qaroshi')
    examples=annotate_rows(Path('corpus/parallel_sentences.csv'),'qaroshi',True)
    index=read_csv(ROOT/'data/english_index.csv')
    for row in index:amend_word(row,'qaroshi')
    save_csv(ROOT/'data/english_index.csv',index)
    counts={}
    for path,key in [('data/pronouns.json','form'),('data/resonances.json','marker'),('data/morphemes.json','form'),('data/grammatical_particles.json','form')]:
        counts[path]=annotate_json(path,key)
    symbols=[{'glyph':x,'ipa':'/'+IPA[x]+'/','reading':x,'is_vowel':x in 'aeiouë'} for x in LETTERS]
    # Individual IPA sounds are segmental, not stressed syllables.
    save_json(ROOT/'data/phoneme_inventory.json',symbols)
    (ROOT/'data/pronunciation_rules.json').write_text(json.dumps({
        'edition':'4.3.1',
        'notation':'broad phonemic IPA in /slashes/',
        'grapheme_count':26,
        'vowels':['a','e','i','o','u','ë'],
        'digraph_graphemes':['sh','zh','kh','ng'],
        'stress':'penultimate syllable for words of two or more syllables; monosyllables left unmarked',
        'syllabification':'hiatus separated; maximize valid C(r/l/w/y) or single onset, all other intervocalic consonants assigned to prior coda',
        'morphology':'written hyphens separate morphemes, not obligatory phonetic pauses',
        'allophony':'r shown as /ɾ/; deliberate rolled [r] is also compatible',
        'phonetic_status':'predictable reference pronunciations; no audio claims or speaker-attested narrow transcriptions',
        'fields':{'ipa':'phonemic transcription','reading':'capitalized stressed syllable in Roman letters','sound_out':'English-oriented approximate sound-out, stress capitalized'},
    },ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    stats_path=ROOT/'data/statistics.json';stats=json.loads(stats_path.read_text(encoding='utf-8'))
    stats['pronunciation_coverage']={'lexicon':words,'phrasebook':examples,'supplementary':counts}
    stats['version']='4.3.1'
    save_json(stats_path,stats)
    release=ROOT/'RELEASE_INFO.json';info=json.loads(release.read_text(encoding='utf-8'))
    info['version']='4.3.1'
    info['release_name']='Qaroshi Unified Standard Reference 4.3.1 · Dictionary Pronunciation Patch'
    info['pronunciation']={'lexicon_entries':words,'sentences':examples,'style':'broad IPA, stress-marked reading guide and English-style sound-out'}
    save_json(release,info)
    print(f'annotated {words} lexical entries, {examples} sentences, {len(index)} English index rows, supplementary {counts}')

if __name__=='__main__':main()
