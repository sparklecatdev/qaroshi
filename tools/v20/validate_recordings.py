#!/usr/bin/env python3
"""Validate locally exported Qaroshi 20 audio metadata against canonical prompts.

Never infer speaker consent from metadata supplied by others or pronounce a
recording 'correct' from amplitude alone. This checks file integrity and schema.
"""
import argparse,csv,json,hashlib,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]

def main():
 ap=argparse.ArgumentParser(description='Check Qaroshi 20.0 exported recording metadata and optional local audio files')
 ap.add_argument('metadata',type=Path,help='Exported single recording JSON or session JSON')
 ap.add_argument('--audio-directory',type=Path,help='Optional directory with audio files named by recording ID')
 args=ap.parse_args()
 with (ROOT/'data/v20/recording_queue_3000.csv').open(encoding='utf8',newline='') as f: queue={r['record_id']:r for r in csv.DictReader(f)}
 j=json.loads(args.metadata.read_text(encoding='utf8'))
 records=j.get('recordings') if j.get('schema')=='qaroshi20-session-v1' else [j]
 if not isinstance(records,list):raise ValueError('Unsupported recording metadata schema')
 results=[]
 for idx,r in enumerate(records,1):
  issues=[];rid=r.get('record_id','');expected=queue.get(rid)
  if not expected:issues.append('unknown recording ID')
  else:
   if r.get('text')!=expected['qaroshi']:issues.append('text does not match canonical prompt')
   if r.get('source_id')!=expected['source_id']:issues.append('source identifier mismatch')
   if r.get('source_ipa')!=expected['broad_ipa']:issues.append('IPA differs from source citation field')
  if r.get('consent_user_confirmed') is not True:issues.append('the recorded speaker consent is not documented')
  if r.get('voice_shared') is not False:issues.append('sharing metadata must be reviewed separately')
  if not isinstance(r.get('bytes'),int) or r['bytes']<=0:issues.append('missing positive audio byte count')
  if not isinstance(r.get('duration_seconds'),(int,float)) or r['duration_seconds']<.2 or r['duration_seconds']>120:issues.append('duration outside 0.2 to 120 seconds')
  if not any(str(r.get('mime_type','')).startswith(x) for x in ['audio/webm','audio/ogg','audio/mp4']):issues.append('unsupported MIME type')
  if args.audio_directory and expected:
   candidates=[p for p in args.audio_directory.iterdir() if p.is_file() and p.name.startswith(rid) and p.suffix.lower() in ('.webm','.ogg','.m4a','.mp4')]
   if not candidates:issues.append('audio file not located for this record')
   elif all(p.stat().st_size!=r.get('bytes') for p in candidates):issues.append('no matching recorded file byte size')
  results.append({'record_id':rid or str(idx),'schema_ok':not issues,'issues':issues})
 print(json.dumps({'checked':len(results),'metadata_technically_valid':sum(x['schema_ok'] for x in results),
 'publication_permission_verified':False,'linguistic_accuracy_verified':False,
 'items':results},ensure_ascii=False,indent=2))
 return 1 if any(not x['schema_ok'] for x in results) else 0
if __name__=='__main__':sys.exit(main())
