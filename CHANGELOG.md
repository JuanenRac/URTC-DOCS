# Changelog

All notable changes to this project are documented here.

## [Unreleased]

- **The threat model and the security baseline follow the updater's new defaults:** signed commits and the question before the build check are on by default, a run with nobody to ask fails closed, and the residual risk about remote build scripts says what lowering the protections means.
- **The shared tools have a lock file:** `tools/sync_repo_tools.py` writes `tools/devtools.lock.json` in each repository (the version of the set and the SHA-256 of every shared file it carries) when URTC-DEVTOOLS, the repository that now versions the set, is next to the repositories, and `tools/check_repo_tools.py` compares the lock with the files (an edited copy, a missing file, a file the lock does not list) and with the version of the set (a copy that fell behind). A repository without a lock is not an error yet. URTC-DEVTOOLS is listed in Related Projects, the catalogue and the map of the ecosystem.
- **`status_lights.py` is a shared file of the family:** the template carries it, `check_repo_tools` compares the copies, and the validator of every repository fails when a light of the Project status table is above what the manifest (`maturity`, `evidence`) allows; the own table of this repository follows it.
- **A design note on packaging the shared repository tooling:** `docs/REPOSITORY_TOOLING.md` says what the repositories copy today, what is wrong with copies, the options (copies, a package from git, a subtree or submodule, a package index) and a proposal that keeps the copies and adds a version and a lock file to the set; it is a note, nothing is built, and the copies shared with the sister ecosystems stay out of any change made in one place.

## [0.1.2] - Related projects with a line for each repository, the nightly checks and the universal README

- **Related Projects lists the URTC family:** the section names the repositories of URTC by group, each with one short line about what it is for, and, in one short line each, the sister projects (independent ecosystems of the same author that share the base and the tools), in the eight languages. It no longer says that URTC is part of another ecosystem. The section is written from one text and one list: `tools/make_related.py` puts it in the READMEs of the other repositories of the family (`--check` fails when one differs, and the nightly run does it), and `docs/ARCHITECTURE.md` describes HYDRA-UMC as a sister project.
- **The numbers of At a glance and the reviewed claims follow the new READMEs of the family:** the test counts of the repositories that state them (718, 153, 500, 79, 467, 183, 425, 560 and 531 tests) are in `data/glance.json`, and the sentences about security and safety that the new Security & Safety sections add were read and entered in `data/claims_reviewed.json`.
- **The README of this repository follows the universal layout in the eight languages,** written by `tools/make_readmes.py`: Project status is the second section, and Architecture and Repository Structure are drawn from `docs/architecture.json` and `docs/structure.json` by the shared picture tools, which every repository of the family now carries (and the template holds). `tools/make_glance.py` also writes the "Jump to" line that follows the At a glance table once a README has the Architecture section.
- **The layout of the README is checked in the CI:** the validator runs `tools/universal_readme_check.py` and lists, as a warning, what differs from the universal layout of the README.

- **The At a glance and Project status checks follow the universal layout:** Project status may sit right after At a glance with the traffic-light icon (the shared README sections put it there), and the marker comment that opens it is not read as part of the At a glance table.
- **The nightly run also checks that the checks leave every repository untouched:** after the own validation of each repository, its working tree must be exactly as it was (a check that rewrites a tracked file, or leaves a new file that is not ignored, is reported). The test count of the rack in the "At a glance" data is current.

## [0.1.1] - The dev dependencies are closed with hashes and the types are checked and a static check on every push

- The architecture, the interfaces, the capability matrix, the security baseline, the threat model and the first slice describe the shared code, the gateway, the signed packages, the offline copy of the web studio and the current test counts, and no longer list disagreements that were solved; the project tree of the README lists the data and the template.
- **The dev dependencies are closed with hashes and the types are checked:** `requirements-dev.lock` pins every package the tests need, with the hash of every file (the CI and the build scripts install it with `--require-hashes`, then the project itself without dependencies), and `mypy` runs on `src` and `tools` in the CI (thirteen findings fixed with casts and annotations, no behaviour changed).
- **A static check on every push:** `ruff.toml` (unused names, exception chaining and syntax errors, the rules the flasher and the tester already ran) and a step of the CI that runs `ruff check .` with a pinned ruff; it found an unused import and an f-string without placeholders, now fixed.
- The capability matrix lists the virtual board in the flasher and in the tester, the trace replay and the Black Box viewer of the web studio.
- The CI holds the tests to a coverage floor of 84 percent of the package (measured 92; `pytest-cov` is in the `dev` extra).

## [0.1.0] - Capability matrix and family tables brought up to date

- **The capability matrix lists what the tester and the web studio gained:** the headless mode with test plans and the simulated head, and the heater PID panel, each at the level its evidence supports (emulated in the tester, local in the web studio), with the limits stated.

- **The matrix lists the other new capabilities:** the list of official images for a bare board in the flasher, and the CRC-8 that the rack and the vision tool now share, each at the level its evidence supports.

- **The project catalogue follows the manifests:** the versions of the seven repositories that were released together are current in `docs/PROJECT_CATALOG.md`.

- **The test counters of the family tables are measured again:** URTC-COMMON shows 337 tests and URTC-FLASHER 466 in their At a glance tables, instead of the numbers from earlier versions.

## [0.0.9] - Repository template and the gateway joins the family

- **A repository template** (`template/eh3d-repo-template`): the canonical copy of the files every repository carries as the same file, with the name of the repository as `<REPO>`. `tools/sync_repo_tools.py` writes it into the repositories (keeping the line endings of each copy; without `--apply` it only lists the differences) and `tools/check_repo_tools.py` now compares the copies with the template instead of with the majority.
- URTC-GATEWAY joins the family: the map, the catalogue, the list of related projects and the glance data know it.

## [0.0.8] - A check of the files every repository shares

- `tools/ci_validate.py` fails when a versioned file has the name of a Windows path (a colon, the character a file system uses to store one, or a first folder named like a drive or a user profile): a path handed to WSL without translation once put build output inside a repository. The same check (`tools/_tracked_names.py`) is in every URTC repository.
- **The shared-file check also compares the dashboard notifier**: `tools/check_repo_tools.py` now reads `.github/workflows/dashboard-dispatch.yml` of every repository next to the documentation-policy, README-parity and version-bump tools, and reports the repository whose copy differs (the name of the repository and the line endings do not count). The notifier runs after the CI of a push to `main` finished green (`workflow_run`), no longer on the push itself.
- The `build-test` scripts use the interpreter named by `URTC_PYTHON` (which URTC-UPDATER sets to its own) and, without it, the first `python3` or `py -3` found.
- **New check `tools/check_repo_tools.py`** (module `drift`, 7 tests, also `run.sh repo-tools`): the files every repository carries as the same copy (`tools/_doc_policy.py`, `tools/_readme_parity.py`, `bump_manifest_version.py`) are compared across the repositories next to this one, the name of the repository and the line endings being the only thing allowed to differ; the text most repositories share is the reference and a repository that differs is named with its first differing line. It runs in `tools/check_all.sh` and in the nightly ecosystem check, and the README of each language lists it in eight languages.
- The brand generator no longer writes the banner of this repository: it is made, like every project banner, by the profile's `tools/project_banner.py`, and the generator keeps the icon and the map of the families.
- The banner follows the animated style of the ecosystem banners, with the name, the kind and the technologies of the project.
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
