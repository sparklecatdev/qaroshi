#!/usr/bin/env python3
"""Read-only structural and publication audit for the Qaroshi repository.

This is not a semantic proof of natural fluency or an attestation service.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]


def loadcsv(p):
    with p.open(encoding='utf-8-sig',newline='') as f:
        return list(csv.DictReader(f))


def audit(check_site=False):
    issues=[];warnings=[];checks={}
    baseline=json.loads((ROOT/'data/v14/baseline_sha256.json').read_text(encoding='utf-8'))['sha256']
    mismatch=[]
    for name,expected in baseline.items():
        p=ROOT/name
        if not p.exists() or hashlib.sha256(p.read_bytes()).hexdigest()!=expected:
            mismatch.append(name)
    checks['frozen_canonical_paths']=len(baseline)
    if mismatch:issues.append('Baseline checksum drift: '+', '.join(mismatch))
    lex=loadcsv(ROOT/'data/lexicon.csv')
    examples=loadcsv(ROOT/'corpus/parallel_sentences.csv')
    checks['canonical_entries']=len(lex)
    checks['controlled_reference_examples']=len(examples)
    if len(lex)!=30000 or len({r['qaroshi'] for r in lex})!=30000:
        issues.append('Canonical word count or headword spelling uniqueness changed')
    if len(examples)!=4383 or len({r['id'] for r in examples})!=4383:
        issues.append('Reference example count or source IDs changed')
    incomplete=[r['id'] for r in lex if not (r.get('english') and r.get('ipa') and r.get('sound_out'))]
    if incomplete:issues.append(f'{len(incomplete)} canonical entries missing gloss or pronunciation')
    grammar=(ROOT/'docs/grammar.md').read_text(encoding='utf-8')
    chapters=sorted({int(x) for x in re.findall(r'^##\s+(\d+)\.',grammar,re.M)})
    checks['grammar_chapters']=len(chapters)
    if chapters!=list(range(1,91)):
        issues.append('Canonical grammar chapter coverage changed')
    resonances=json.loads((ROOT/'data/resonances.json').read_text(encoding='utf-8'))
    checks['written_resonances']=len(resonances)
    if len(resonances)!=16:issues.append('Resonance inventory mismatch')
    glyphs=[p for p in (ROOT/'assets/glyphs').glob('*.png')]
    checks['native_glyphs']=len(glyphs)
    if len(glyphs)!=26:issues.append('Native glyph inventory mismatch')
    catalog=json.loads((ROOT/'data/site_catalog.json').read_text(encoding='utf-8'))
    apps=catalog['apps'];checks['navigation_apps']=len(apps)
    if len(set(x['id'] for x in apps))!=len(apps) or len(set(x['href'] for x in apps))!=len(apps):
        issues.append('Duplicate public navigation IDs or targets')
    for entry in apps:
        if not (entry['href'].endswith('.html') and not entry['href'].startswith('/') and '..' not in Path(entry['href']).parts):
            issues.append('Unexpected external/unsafe catalog URL '+entry['href'])
    if catalog['edition']!='23':issues.append('Current tools catalog incorrectly labelled')
    policy=(ROOT/'docs/maintenance/QUALITY_AND_ARCHIVE_POLICY.md').read_text(encoding='utf-8')
    if '103' not in policy or '65' not in policy:
        issues.append('Quality policy does not expose unresolved review records')
    source=ROOT/'Qaroshi_21_23_SOURCE_MANIFEST.json'
    if source.exists():
        data=json.loads(source.read_text(encoding='utf-8'))
        mismatches=[]
        # Historical release manifests stay immutable. Approved changes to a
        # source template after its historical release require an exact,
        # separately recorded Git blob identity, rather than a silent rehash.
        overlay_path=ROOT/'docs/maintenance/APPROVED_SOURCE_OVERRIDES.json'
        approved=json.loads(overlay_path.read_text(encoding='utf-8')) if overlay_path.exists() else {}
        overridden=[]
        for rel,expected in data['files'].items():
            item=ROOT/rel
            if item.exists() and hashlib.sha256(item.read_bytes()).hexdigest()==expected:
                continue
            override=approved.get(rel)
            if item.exists() and override and override.get('historical_sha256')==expected:
                raw=item.read_bytes()
                git_blob=hashlib.sha1(b'blob '+str(len(raw)).encode('ascii')+b'\\0'+raw).hexdigest()
                if git_blob==override.get('approved_git_blob_sha1') and override.get('reason'):
                    overridden.append(rel)
                    continue
            mismatches.append(rel)
        orphaned=sorted(set(approved)-set(data['files']))
        if orphaned:issues.append('Source overrides without archived manifest entries: '+', '.join(orphaned))
        if mismatches:issues.append('Current release source-manifest mismatches: '+', '.join(mismatches))
        checks['release_manifest_sha256_paths']=len(data['files'])
        checks['approved_post_release_source_overrides']=len(overridden)
        if overridden:
            warnings.append('Explicitly approved post-release source changes (historical checksums retained): '+', '.join(overridden))
    else:
        warnings.append('Optional 21–23 release source-manifest missing')
    # Historic browser QA records are retained, not silently classified as junk.
    historic=list(ROOT.glob('data/v*/browser_report.json'))+list(ROOT.glob('corpus/**/browser_test_report.json'))
    checks['historical_qa_records_preserved']=len(historic)
    log_like=[p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*')
              if p.is_file() and (p.suffix in {'.log','.tmp','.pyc'} or p.name.endswith('test_log.txt'))
              and not any(s in p.parts for s in ('__pycache__','_site'))]
    checks['local_transient_log_files']=len(log_like)
    if log_like:warnings.append('Local transient files present (not source by default): '+', '.join(log_like[:8]))
    if check_site:
        from build_pages import stage
        import tempfile
        with tempfile.TemporaryDirectory(prefix='qaroshi-audit-') as temp:
            stats=stage(Path(temp))
            checks['published_html_files']=stats['html_files']
            checks['public_data_excluded']=stats['excludes_raw_data']
    return {'passed':not issues,'checks':checks,'issues':issues,'warnings':warnings,
            'scope':'Structural, build, archive and baseline integrity; not natural speaker semantic certification'}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--site',action='store_true',help='Build and audit the curated Pages artifact')
    parser.add_argument('--json',type=Path,help='Optional JSON output path for a local report')
    args=parser.parse_args()
    report=audit(check_site=args.site)
    if args.json:
        args.json.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))
    if not report['passed']:sys.exit(1)

if __name__=='__main__':main()
