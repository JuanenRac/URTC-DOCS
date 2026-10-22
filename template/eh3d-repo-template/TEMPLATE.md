# Repository template

The canonical copy of the files that every repository of the family carries as the same file. The name of the repository is
written `<REPO>` here and replaced by the real name when a file is put into a repository; the line endings of each copy are kept.

| File | What it is |
|---|---|
| `tools/_doc_policy.py` | the documentation policy check |
| `tools/_readme_parity.py` | the check that the eight READMEs have the same sections and links |
| `tools/_tracked_names.py` | the check for versioned files named like a Windows path |
| `bump_manifest_version.py` | the manifest version bumper |
| `.github/workflows/dashboard-dispatch.yml` | the notice to the central dashboard, sent after a green CI on `main` |

```
python tools/sync_repo_tools.py            # list the copies that differ from the template
python tools/sync_repo_tools.py --apply    # write the template into those repositories
python tools/check_repo_tools.py           # fail when a copy differs (it compares with this template)
```

Edit a file here, run the synchroniser, and commit each repository: never edit one copy by hand. The files a repository may
legitimately differ in (its CI workflow, its build check, its validation) are not part of the template; they have their own marked
sections inside the file of each repository.
