# Changelog: URTC-DOCS 📚

All notable changes to this project will be documented in this file. The
version number follows this ecosystem's "odometer" scheme: PATCH +1 on
every real build, rolling into MINOR past 9 (`0.0.9` -> `0.1.0`); MAJOR is
bumped manually only. See `bump_version.py`.

## [0.0.1] - The documentation and tooling hub of the ecosystem

- **Documents:** the architecture (boards, CAN bus, tool heads, host tools, data flows, trust boundaries), the interfaces and who owns each contract, the capability matrix (what is proven in software and what needs a board, project by project), the security baseline, the threat model, the first vertical slice and the generated project catalogue. They are written from the READMEs, manifests, changelogs and documents of the other repositories, and mark what could not be traced.
- **CAN protocol study note:** `docs/CAN_PROTOCOL_DUPLICATION.md` records that the CAN protocol is implemented three times (URTC-FLASHER, URTC-TESTER, URTC-WEB-STUDIO) from one prose reference, lists the places where the copies already differ, and describes what a shared specification with conformance vectors would hold. Nothing of it is built: it is a pending decision of the owner.
- **Project catalogue:** `tools/make_catalog.py` writes the table from the manifests found next to this repository (`--check` for the whole table, `--check-structure` for which repositories exist and of what kind), with one curated sentence per repository.
- **Brand:** `tools/make_brand.py` writes the banner, the icon and the map of the ecosystem in the look of URTC.
- **READMEs:** `tools/make_readmes.py` writes the README of this repository in the eight languages (English, Spanish, French, Italian, German, Chinese, Japanese and European Portuguese) from one source, with the same sections and links in each.
- **Publication check:** `tools/publication_check.py` looks, in every repository of the ecosystem, for private keys, public IP addresses, personal e-mail addresses, tracked secret files, names of private documents, internal tracking codes, commits by someone else or with a co-author trailer, and (with `--history`) for lines that were committed and later removed. A key header or an address inside a test fixture, four small numbers that look like a version, and the name of an AI provider in a commit message are findings to review, not blocks.
- **Ecosystem check:** `tools/check_all.sh` runs the own `tools/ci_validate.py` of every repository next to this one and prints one PASS, FAIL or SKIP line each (a skipped check is never reported as a pass), then the checks of this repository.
- **CI:** the baseline workflow runs the shared validation, the generator checks and the unit tests, also on Windows; a nightly workflow fetches the other repositories and compares them.
- **Shared checks:** `tools/ci_validate.py`, `tools/_doc_policy.py`, `tools/_readme_parity.py`, `tools/build_test.py` and `bump_manifest_version.py` are the copies used by the other URTC repositories, not re-implemented here.
