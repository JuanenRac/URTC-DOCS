# Changelog: URTC-DOCS 📚

All notable changes to this project will be documented in this file. The
version number follows this ecosystem's "odometer" scheme: PATCH +1 on
every explicit bump, rolling into MINOR past 9 (`0.0.9` -> `0.1.0`); MAJOR is
bumped manually only. See `bump_version.py`.

## [Unreleased]

- The architecture and capability documents describe the Qt Quick window as the only window of the flasher and the tester, and the project catalogue follows the shorter manifest notes.
- The manifest declares how far the project has been shown to work (`evidence`: host-test) and `tools/ci_validate.py` checks the value.

## [0.0.7] - The capability matrix lists the multinode extension

- docs/CAPABILITY_MATRIX.md has a row for several tool heads on one CAN bus: implemented in the main firmware behind a switch that is off by default, Local level (host tests only), nothing tried on boards and no host program using it yet.

## [0.0.6] - An explicit bump command: building never changes the version

- Building no longer changes the version: build.sh and build.bat only read it, and raising it is the explicit `python bump.py` step. The README sources and the eight generated READMEs say so.
- Every licence statement and source header says GPL-3.0-or-later.

## [0.0.5] - The doctor: one report on the machine and on every repository

- New tool tools/urtc_doctor.py (command doctor of the package): one report with the tools of the machine (Python, git, Node, the ARM compiler, PySide6, pytest, serial ports, which are only listed), the versions of every repository (manifest, version in its source file and newest CHANGELOG entry must agree), every copy of URTC-COMMON (as locked, and not behind URTC-COMMON when it is next to this repository), the firmware bundled by URTC-FLASHER and URTC-WEB-STUDIO (consistent with its manifests, and the same images in both), the own validation of every repository and the checks of this one.
- --fast leaves out the checks that start other programs, --online compares the bundled firmware with the newest firmware release on GitHub (a pre-release counts); every line is PASS, FAIL, WARN or SKIP, a check that could not run is never a PASS, and the exit status is non-zero on a FAIL and when nothing could be checked. 19 tests.
- The README (all eight languages) documents the doctor next to the other tools.
- bump_manifest_version.py prints URTC instead of the name of another ecosystem.
- The At a glance tables of the repositories that were behind their manifest were refreshed.
- The nightly workflow also runs the doctor (--fast), so a version that disagrees with its source file or changelog, a copy of URTC-COMMON that was edited or fell behind, and bundled firmware that differs between the flasher and the web studio are reported the night they appear.

## [0.0.4]

- New check `tools/check_claims.py` (module `claims`, 12 tests): it reads the English README of every repository of the ecosystem and fails when a sentence has a risk word (E-STOP, interlock, real-time, signed, FDCAN, torque, certified, ...) and no status marker next to it, unless the line is in `data/claims_reviewed.json`.
- The nightly run and `tools/check_all.sh` run the claim check; the README documents the rule in the eight languages and carries the short safety and security status note.
- `docs/THREAT_MODEL.md` has a section that sets the capabilities a reader from outside concluded from the READMEs against what the repositories contain.
- The glance data and the catalogue follow the maturity that the manifests now declare.

## [0.0.3] - URTC-COMMON joins the family

- **New repository in the family:** URTC-COMMON (the CAN protocol as data: a machine-readable specification, generated C, TypeScript and Python code, conformance vectors and the Python transports) is now in the Related Projects section of the eight READMEs, in the generated project catalogue, in the At a glance data and in the map of the ecosystem, on its own row because it sits between the host tools and the operations repositories.
- **CAN protocol note and interface table:** `docs/CAN_PROTOCOL_DUPLICATION.md` has a status paragraph (items 1, 3, 4 and 5 now exist in URTC-COMMON, nothing imports it yet, and the two identifiers the firmware implements that no prose or tool describes), and `docs/INTERFACES.md` and `docs/ARCHITECTURE.md` say that a test now compares the copies with the specification.

## [0.0.2] - The At a glance tables

- **At a glance:** `tools/make_glance.py` inserts, or rewrites in place, the At a glance table in the README and its seven translations of every repository of the ecosystem, written from the manifest of each repository (version, maturity, stack, target) and from `data/glance.json` (test count when it is known, target, and one hardware statement chosen from a closed vocabulary that is translated once in the eight languages). It keeps the line endings of each file, never duplicates the section, and `--check` fails when a section is missing, misplaced or stale; `--repo NAME` limits it to one repository.
- **After a version bump:** run `python tools/make_glance.py --apply --repo NAME` to refresh the Version cell of that repository.
- **Nightly check:** the nightly workflow and `tools/check_all.sh` now compare the At a glance tables of all the sibling repositories with their manifests, so a table that was not refreshed after a version bump is reported.
- **This README:** the table of this repository is written by the same tool, so the labels are the ones used in the other repositories.

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
