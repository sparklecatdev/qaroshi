from pathlib import Path
import zipfile,hashlib,json
root=Path(__file__).resolve().parents[1]
out=Path('/mnt/data')
(out/'Qaroshi_Wiki_5.1.html').write_bytes((root/'Qaroshi_Wiki.html').read_bytes())
index=json.loads((root/'docs/deep_guides/guide_index.json').read_text())
parts=['# Qaroshi Unified Standard 5.1 — Study Handbook','',
       'The complete learning-library companion to the unified Qaroshi reference. Includes 16 topic manuals, a sixteen-lesson course, 21 worked sentence analyses and workbook answer keys. Existing vocabulary and syntax are unchanged.','',
       '## Contents','']
for i,x in enumerate(index,1):parts.append(f'{i}. {x["title"]}')
for i,x in enumerate(index,1):
 parts.extend(['','\n---\n',f'<!-- GUIDE {i}: {x["id"]} -->','', (root/x['path']).read_text(encoding='utf8').strip()])
book=out/'Qaroshi_5.1_Study_Handbook.md';book.write_text('\n'.join(parts)+'\n',encoding='utf8')
archive=out/'Qaroshi_Unified_Standard_5.1_Deep_Guides.zip'
with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=8) as z:
 files=sorted(f for f in root.rglob('*') if f.is_file() and '__pycache__' not in f.parts and f.suffix!='.pyc')
 for p in files:
  z.write(p,arcname='Qaroshi_Standard_5.1/'+str(p.relative_to(root)))
 z.write(book,arcname='Qaroshi_Standard_5.1/Qaroshi_5.1_Study_Handbook.md')
with zipfile.ZipFile(archive) as z:
 bad=z.testzip()
 assert bad is None,bad
 assert 'Qaroshi_Standard_5.1/Qaroshi_Wiki.html' in z.namelist()
 assert 'Qaroshi_Standard_5.1/docs/deep_guides/graded_course.md' in z.namelist()
 print(json.dumps({'archive':str(archive),'zip_files':len(z.namelist()),'bytes':archive.stat().st_size,'study_handbook_bytes':book.stat().st_size,'standalone_wiki_bytes':(out/'Qaroshi_Wiki_5.1.html').stat().st_size,'sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),'integrity_ok':True},indent=2))
