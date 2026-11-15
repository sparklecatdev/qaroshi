import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class SiteNavigationTests(unittest.TestCase):
    def test_linked_tools_exist(self):
        navigation = (ROOT / "web" / "qaroshi.js").read_text(encoding="utf-8")
        links = set(re.findall(r'href="(Qaroshi_[^"#?]+\.html)"', navigation))
        self.assertTrue(links, "No tool links found in the wiki navigation")
        for link in sorted(links):
            with self.subTest(link=link):
                self.assertTrue((ROOT / link).is_file(), f"Missing linked tool: {link}")


if __name__ == "__main__":
    unittest.main()
