# Restoring Qaroshi 15.x–16.x without overwriting newer work

This branch was created **from the live `main` branch**, rather than copying an old release over the working repository. It is intentionally non-destructive. Do not replace `data/lexicon.csv`, existing grammar, the 26 glyphs, `data/v17/`, the current 17.0 communicator, `README.md`, `index.html`, or contributor-managed files with copies from archived packages.

## What is already committed in this PR

- `tools/integrate_release_archives.py`: ZIP verification, strict version-path allowlist, dry-run preview, SHA-256 comparisons, no-overwrite import, explicit conflict reports.
- `tests/test_release_import.py`: checks canonical path exclusion, traversal/path rejection, preservation of divergent contributor edits, and idempotency.
- Select versioned editorial review datasets and guides from the 15/16 development work. These **are review drafts, not accepted language standards**.

## The bulk historical source still needed

Source used: `Qaroshi_16_2_Root_Standardization.zip`, which contains the v15, v15.1, v16, v16.1 and v16.2 versioned data, corpus, tools, docs and tests. A separate downloadable `Qaroshi_GitHub_v15_v16_Missing_Source_Patch.zip` was prepared with **113 versioned source paths**, approximately 73 MB uncompressed / 6.9 MB compressed, excluding canonical and existing 14/17 material.

**That bulk package has not been committed to this pull request.** The branch is an actual partial integration, not a complete source synchronization or release.

### Safe local import procedure

1. Ensure a clean clone of the latest `main`; create a separate integration branch or check out this PR branch.
2. Download the original local `Qaroshi_16_2_Root_Standardization.zip` from the conversation's deliverables, and keep it outside the Git checkout.
3. Preview the proposed import:

   ```sh
   python tools/integrate_release_archives.py --archive /path/to/Qaroshi_16_2_Root_Standardization.zip --repo . --report qaroshi-import-preview.json
   ```

4. Review the JSON report. In particular, **never override** `conflict` or `different_release_versions` paths blindly.
5. Apply only the missing paths:

   ```sh
   python tools/integrate_release_archives.py --archive /path/to/Qaroshi_16_2_Root_Standardization.zip --repo . --apply --report qaroshi-import-result.json
   ```

6. Run the existing validation suite, inspect `git status` and `git diff --stat`, then commit the reviewed additions. No force-push, no reset of `main`, no automatic merge of proposed new roots.

You can supply multiple archives using repeated `--archive`; conflicting versions of the same path are **skipped** and listed separately instead of picking a winner.

### QA / semantic limits

The 15.1 generated material is heavily repetitive and **not** a naturalistic speaker corpus. All 16.x transparent alternatives, proposed root forms, and idioms remain editorial candidates. This importer copies source files without making any new spelling or semantic convention official.

## Important integration policy

An externally edited existing file always takes precedence over a historical ZIP when bytes differ. The import tool preserves it and records a conflict. A reviewer may later merge specific differences deliberately, with provenance, tests and an explicit decision. This is essential because the live repository has changes beyond the archived releases.

**Do not mark this PR complete until the remaining source paths are pushed and tests pass on the GitHub branch.**
