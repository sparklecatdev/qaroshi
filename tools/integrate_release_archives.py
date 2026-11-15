#!/usr/bin/env python3
"""Restore missing versioned Qaroshi 15/16 files without overwriting existing work.

Run from an up-to-date Qaroshi checkout:
  python tools/integrate_release_archives.py --archive /path/to/Qaroshi_16_2_Root_Standardization.zip
  python tools/integrate_release_archives.py --archive /path/to/Qaroshi_16_2_Root_Standardization.zip --apply

Dry-run by default. Canonical data, v14/v17, and unrelated contributors' files
are never imported/overwritten by this script.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import stat
from pathlib import Path, PurePosixPath
from zipfile import ZipFile

PREFIXES = (
    "corpus/v15/", "corpus/v15_completion/",
    "data/v15/", "data/v16/", "data/v16_1/", "data/v16_2/",
    "docs/v15/", "docs/v15_completion/", "docs/v16/", "docs/v16_1/",
    "tools/v15/", "tools/v15_completion/", "tools/v16/",
    "tools/v16_1/", "tools/v16_2/",
    "web/v15/", "web/v15_completion/", "web/v16/",
)
EXACT_FILES = {
    "tests/test_v15.py", "tests/test_v15_completion.py",
    "tests/test_standard16.py", "tests/test_v16_root_guide.py",
    "tests/test_v16_1_transparency.py", "tests/test_v16_2_lexical_decisions.py",
}
DISALLOWED_SUFFIXES = {".ttf", ".otf", ".woff", ".woff2", ".zip", ".pyc"}


def safe_path(name: str) -> str | None:
    if "\\" in name or "\x00" in name:
        return None
    parts = PurePosixPath(name).parts
    if not parts or name.startswith("/") or any(p in {"..", "."} for p in parts):
        return None
    if parts[0].startswith("Qaroshi") and len(parts) > 1:
        parts = parts[1:]
    result = "/".join(parts)
    if result not in EXACT_FILES and not result.startswith(PREFIXES):
        return None
    if PurePosixPath(result).suffix.lower() in DISALLOWED_SUFFIXES:
        return None
    if "__pycache__" in parts or ".git" in parts:
        return None
    return result


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def candidate_files(archives: list[Path]):
    seen = {}
    inconsistent = {}
    for archive in archives:
        with ZipFile(archive) as zf:
            if zf.testzip() is not None:
                raise ValueError(f"ZIP integrity failed: {archive}")
            for item in zf.infolist():
                if item.is_dir() or stat.S_ISLNK(item.external_attr >> 16):
                    continue
                path = safe_path(item.filename)
                if path is None:
                    continue
                data = zf.read(item)
                hashed = digest(data)
                if path in seen:
                    if seen[path][0] != hashed:
                        inconsistent.setdefault(path, [seen[path][0]]).append(hashed)
                else:
                    seen[path] = (hashed, data)
    return seen, inconsistent


def sync(repo: Path, archives: list[Path], apply: bool = False):
    repo = repo.resolve()
    if not (repo / ".git").exists():
        raise ValueError(f"Not a Git checkout: {repo}")
    items, inconsistent = candidate_files(archives)
    result = {
        "mode": "apply" if apply else "dry-run", "checked": len(items),
        "added": [], "would_add": [], "identical": [], "conflict": [],
        "different_release_versions": [], "archives": [p.name for p in archives],
    }
    for name in sorted(items):
        if name in inconsistent:
            result["different_release_versions"].append(
                {"path": name, "hashes": inconsistent[name]})
            continue
        sha, data = items[name]
        target = repo / name
        if target.is_symlink() or any(
            p.is_symlink() for p in target.parents if p != repo
        ):
            result["conflict"].append({"path": name, "reason": "symlink in destination"})
        elif target.exists():
            if target.is_file() and digest(target.read_bytes()) == sha:
                result["identical"].append(name)
            else:
                result["conflict"].append({
                    "path": name, "reason": "existing content differs",
                    "incoming_sha256": sha})
        elif apply:
            target.parent.mkdir(parents=True, exist_ok=True)
            try:
                with target.open("xb") as handle:
                    handle.write(data)
                result["added"].append(
                    {"path": name, "sha256": sha, "bytes": len(data)})
            except FileExistsError:
                result["conflict"].append(
                    {"path": name, "reason": "created concurrently"})
        else:
            result["would_add"].append(
                {"path": name, "sha256": sha, "bytes": len(data)})
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", required=True, action="append", type=Path)
    parser.add_argument("--repo", default=Path.cwd(), type=Path)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    result = sync(args.repo, args.archive, args.apply)
    body = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.report:
        args.report.write_text(body, encoding="utf-8")
        print(f"Report: {args.report}")
    else:
        print(body)
    if result["conflict"] or result["different_release_versions"]:
        print("Review conflicts manually; the importer never overwrites.")


if __name__ == "__main__":
    main()
