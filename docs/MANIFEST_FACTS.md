# Manifest facts

The manifest of a repository (`urtc.project.json`) says what the repository is. `tools/sync_manifests.py` keeps the part of it that can be computed in step with the repository, and refuses a manifest that contradicts it. The traffic lights of the "Project status" table come from the manifest, so they stay honest without anyone editing them.

## What is computed

| Fact | Contradiction (fails) | Information (never fails) |
| --- | --- | --- |
| Shipped version (`native_version`, components) | differs from the manifest `version` | no shipped file found |
| Changelog | newest released heading differs from the manifest `version` | entries under `[Unreleased]` |
| Tests | `evidence` is host-test, simulator, bench or field and there are no test files | |
| Simulation | `evidence` is `simulator` and no workflow runs a simulator, replay or fake bench | a simulation runs but `evidence` is `none` |
| Release (online) | the newest release is newer than the manifest | the manifest version is not released yet |
| Continuous integration (online) | | the last completed run of `main` is not green |

## What is never written

`maturity`, `evidence` and `hardware_bound` are judgements. A bench or field test is a human record: the manifest keeps it in the optional `evidence_record` field and the tool only reports when it is missing. A green hardware light needs `evidence: field`.

## Use

```
python tools/sync_manifests.py --check                 # every clone next to this repository, offline
python tools/sync_manifests.py --check --online        # also the newest release and the last run of main (gh, cached, at most --max-calls calls)
python tools/sync_manifests.py --self                  # this repository only, from its working tree
python tools/sync_manifests.py --apply                 # write data/manifest_facts.json
python tools/sync_manifests.py --apply-manifests       # raise the version of a manifest to the shipped one (never lowers it)
```

`data/manifest_waivers.json` lists the findings a repository accepts for now. The nightly workflow `manifest-facts.yml` runs the check over the whole family, opens one issue when a manifest contradicts the facts, and sends one grouped pull request with the changed facts file. Test counts are handled by `tools/check_test_counts.py`.
