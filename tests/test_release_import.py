"""Regression tests for non-destructive historical release restoration."""
import importlib.util
import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile

PATH = Path(__file__).resolve().parent.parent / "tools/integrate_release_archives.py"
spec = importlib.util.spec_from_file_location("qaroshi_release_sync", PATH)
syncer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(syncer)


class SafeImportTests(unittest.TestCase):
    def test_whitelist_and_traversal(self):
        self.assertEqual(syncer.safe_path("Qaroshi/data/v16/sample.csv"), "data/v16/sample.csv")
        for invalid in (
            "Qaroshi/data/lexicon.csv", "Qaroshi/data/v17/current.csv",
            "Qaroshi/../../data/v16/escape.csv",
            "Qaroshi/data/v16/font.ttf", "C:\\data\\v16\\file.csv",
        ):
            self.assertIsNone(syncer.safe_path(invalid), invalid)

    def test_dry_run_preserve_conflict_and_idempotency(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".git").mkdir()
            old = root / "data/v16/keep.csv"
            old.parent.mkdir(parents=True)
            old.write_bytes(b"contributor edit\n")
            archive = root / "source.zip"
            with ZipFile(archive, "w") as z:
                z.writestr("Qaroshi/data/v16/keep.csv", "different source\n")
                z.writestr("Qaroshi/data/v16/new.csv", "new content\n")
                z.writestr("Qaroshi/data/lexicon.csv", "should not touch this\n")
            dry = syncer.sync(root, [archive], False)
            self.assertEqual(len(dry["would_add"]), 1)
            self.assertEqual(len(dry["conflict"]), 1)
            self.assertFalse((root / "data/v16/new.csv").exists())
            applied = syncer.sync(root, [archive], True)
            self.assertEqual(len(applied["added"]), 1)
            self.assertEqual(old.read_bytes(), b"contributor edit\n")
            self.assertEqual((root / "data/v16/new.csv").read_bytes(), b"new content\n")
            again = syncer.sync(root, [archive], True)
            self.assertEqual(again["added"], [])
            self.assertEqual(len(again["identical"]), 1)

    def test_differing_archives_are_flagged(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".git").mkdir()
            archives = []
            for key, body in [("a", "alpha"), ("b", "beta")]:
                path = root / (key + ".zip")
                with ZipFile(path, "w") as z:
                    z.writestr("Qaroshi/tools/v16/sample.py", body)
                archives.append(path)
            result = syncer.sync(root, archives, True)
            self.assertEqual(len(result["different_release_versions"]), 1)
            self.assertFalse((root / "tools/v16/sample.py").exists())


if __name__ == "__main__":
    unittest.main()
