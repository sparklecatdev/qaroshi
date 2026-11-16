"""Protect curated site navigation, latest release integrity and source hygiene."""
from __future__ import annotations
import bz2
import hashlib
import importlib.util
import json
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

class SiteMaintenanceTests(unittest.TestCase):
    def test_catalog_exact_releases_and_unique_paths(self):
        d=json.loads((ROOT/'data/site_catalog.json').read_text(encoding='utf-8'))
        self.assertEqual(d['edition'],'23')
        apps=d['apps'];self.assertEqual(len(apps),10)
        self.assertEqual(len({a['href'] for a in apps}),10)
        self.assertTrue(all(a['href'].endswith('.html') for a in apps))
        self.assertTrue(any(a['id']=='translate' for a in apps))

    def test_must_preserve_canonical_baselines(self):
        m=json.loads((ROOT/'data/v14/baseline_sha256.json').read_text())['sha256']
        self.assertEqual(len(m),29)
        for rel,sha in m.items():
            self.assertEqual(hashlib.sha256((ROOT/rel).read_bytes()).hexdigest(),sha,rel)

    def test_restored_assets_have_expected_digest(self):
        import sys
        sys.path.insert(0,str(ROOT/'tools/maintenance'))
        from build_pages import restored_files
        data=restored_files()
        self.assertEqual(len(data),3)
        self.assertTrue(all(x.startswith(b'<!doctype html>') for x in data.values()))

    def test_portal_uses_html_safe_embedded_catalog(self):
        s=(ROOT/'explore.html').read_text(encoding='utf-8')
        self.assertIn('id="catalog"',s)
        self.assertIn('data-filter="Learn"',s)
        self.assertIn('role=',s)
        self.assertNotIn('__QAROSHI_SITE_CATALOG__',s)

    def test_pages_only_publishes_html(self):
        import sys
        sys.path.insert(0,str(ROOT/'tools/maintenance'))
        from build_pages import stage
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)
            info=stage(p)
            self.assertTrue(info['excludes_raw_data'])
            self.assertEqual(info['html_files'],19)
            self.assertEqual((p/'index.html').read_bytes(),(ROOT/'Qaroshi_Wiki.html').read_bytes())
            self.assertFalse((p/'data').exists())
            self.assertFalse((p/'tests').exists())
            self.assertFalse(any(p.glob('*.zip')))

    def test_restorer_checks_integrity_and_no_silent_overwrite(self):
        path=ROOT/'tools/v21_23/restore_artifacts.py'
        spec=importlib.util.spec_from_file_location('qaroshi_restorer_test',path)
        mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
        with tempfile.TemporaryDirectory() as t:
            temp=Path(t);(temp/'data/v21').mkdir(parents=True)
            original=b'{"source":"original"}\n'
            archive=temp/'Qaroshi_21_23_Precomputed_Data.zip'
            with zipfile.ZipFile(archive,'w') as z:z.writestr('data/v21/probe.json',original)
            html=b'<!doctype html><html><title>test</title></html>'
            compressed=temp/'Qaroshi_21_23_Translation_Immersion_Academy.html.bz2'
            compressed.write_bytes(bz2.compress(html))
            meta={'files':{archive.name:hashlib.sha256(archive.read_bytes()).hexdigest(),compressed.name:hashlib.sha256(compressed.read_bytes()).hexdigest()},'site_sha256':hashlib.sha256(html).hexdigest()}
            manifest=temp/'Qaroshi_21_23_SOURCE_MANIFEST.json';manifest.write_text(json.dumps(meta))
            mod.ROOT=temp;mod.SITE=temp/'Qaroshi_21_23_Translation_Immersion_Academy.html';mod.ARCHIVE=archive;mod.COMPRESSED=compressed;mod.MANIFEST=manifest
            self.assertEqual(mod.restore(),mod.SITE)
            self.assertEqual((temp/'data/v21/probe.json').read_bytes(),original)
            (temp/'data/v21/probe.json').write_text('contributor edit')
            with self.assertRaises(FileExistsError):mod.restore()
            self.assertEqual((temp/'data/v21/probe.json').read_text(),'contributor edit')
            mod.restore(force=True)
            self.assertEqual((temp/'data/v21/probe.json').read_bytes(),original)
            compressed.write_bytes(b'corrupt compressed input')
            with self.assertRaises(ValueError):mod.restore()

if __name__=='__main__':unittest.main()
