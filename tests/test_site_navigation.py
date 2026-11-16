"""Validate Wiki tool links against shipped pages or verified compressed apps."""
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools' / 'maintenance'))
from build_pages import restored_files

class SiteNavigationTests(unittest.TestCase):
    def test_linked_tools_exist(self):
        navigation = (ROOT / 'web' / 'qaroshi.js').read_text(encoding='utf-8')
        links = set(re.findall(r'href="(Qaroshi_[^"#?]+[.]html)"', navigation))
        self.assertTrue(links, 'No tool links found in Wiki navigation')
        compressed_verified = restored_files()
        for link in sorted(links):
            with self.subTest(link=link):
                self.assertTrue(
                    (ROOT / link).is_file() or link in compressed_verified,
                    f'Missing linked tool in checkout and compressed releases: {link}'
                )

    def test_latest_links_are_present(self):
        navigation = (ROOT / 'web' / 'qaroshi.js').read_text(encoding='utf-8')
        for name in ('Qaroshi_21_23_Translation_Immersion_Academy.html',
                     'Qaroshi_20_Speech_Studio.html',
                     'Qaroshi_18_19_Living_Language_Studio.html',
                     'explore.html'):
            with self.subTest(name=name): self.assertIn(name, navigation)
        self.assertNotIn('RELEASE 17', navigation)

if __name__ == '__main__':
    unittest.main()
