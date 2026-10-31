<p align="center">
  <img src="images/URTC_DOCS_BANNER.svg" alt="URTC-DOCS banner" width="100%">
</p>

# 📚 URTC-DOCS

<p align="center">🇺🇸 <b>English</b> | <a href="README_spa.md">🇪🇸 Español</a> | <a href="README_fra.md">🇫🇷 Français</a> | <a href="README_ita.md">🇮🇹 Italiano</a> | <a href="README_deu.md">🇩🇪 Deutsch</a> | <a href="README_zho.md">🇨🇳 简体中文</a> | <a href="README_jpn.md">🇯🇵 日本語</a> | <a href="README_por.md">🇵🇹 Português</a></p>

### Architecture, interfaces, security baseline and the truth about what is proven

<p align="center">
  <img src="https://img.shields.io/badge/License-GPL%203.0--or--later-blue.svg" alt="GPL 3.0 or later">
  <img src="https://img.shields.io/badge/Format-Markdown-083fa1.svg" alt="Format">
  <img src="https://img.shields.io/badge/Languages-8-00E5FF.svg" alt="Languages">
  <img src="https://img.shields.io/badge/Version-0.1.3-0f6cbd.svg" alt="Version">
  <img src="https://img.shields.io/badge/Maturity-scaffolding-FFB020.svg" alt="Maturity">
</p>

---

**Honesty check - what actually runs today:** this repository holds documents and small tools. The tools (the catalogue generator, the brand generator, the README generator, the publication check and the family check) are real and have unit tests that run in CI; the nightly workflow runs them against the other repositories of the family. The documents are written from the READMEs, manifests, changelogs and documents of those repositories as they were read for this version, and a statement that could not be traced to a repository is marked as such. Nothing here is a hardware test: the capability matrix says, for each capability, whether it was only simulated, tested on a computer or run on real hardware, and the firmware repository states that no populated board exists yet.

---

> **Safety and security status:** this ecosystem is not a certified safety system, and no populated URTC board exists yet. The bootloaders check firmware images with CRC32 and a shared-key HMAC-SHA256, not with an asymmetric signature (planned); the published application images are signed with the public development key (`signing_key_kind: dev`), so anyone can produce an image the bootloader accepts; nothing has been transmitted to a real board. Read the [security baseline](docs/SECURITY_BASELINE.md) and the [threat model](docs/THREAT_MODEL.md) before relying on any statement here for the safety of a person.

## 📋 At a glance

| | |
|---|---|
| Version | `0.1.3` |
| Maturity | Scaffolding |
| Tests | 183 |
| Stack | Markdown / Mermaid / Python / SVG |
| Target | The PC of the person using it |
| On real hardware | Not applicable: nothing here runs on hardware |

**Jump to:** [Overview](#-overview) · [Architecture](#-architecture) · [Quick start](#-quick-start) · [Testing](#-testing) · [Structure](#-repository-structure) · [Related](#-related-projects)

## 🚦 Project status

🟢 done and verified · 🟡 works, with known limits · 🟠 half done or not verified · 🔴 not done or not working. Nothing is green if it never ran on real hardware.

| Part | Status | What the repository can show |
| --- | :---: | --- |
| Software | 🟡 | The generators of the catalogue, the brand and the READMEs, and the checks of the publication, the claims and the family, run on a computer; no hardware is involved. |
| Tests | 🟡 | The test suite passes in the CI, on Linux and on Windows, on every push. |
| Checks across the family | 🟡 | The nightly run fetches every repository of the family and compares their summary tables, claims and catalogue structure; a stale version in the catalogue is reported but does not fail the night. |
| Security documents | 🟡 | The security baseline and the threat model are written from the other repositories as they were read; nobody outside the project has reviewed them. |
| Documentation | 🟡 | README in eight languages and reference documents; the translations were not reviewed by native speakers. |

## 🎯 Overview

<p align="center">
  <img src="images/URTC_ECOSYSTEM.svg" alt="URTC ecosystem" width="100%">
</p>

The picture below shows the repositories of URTC, the CAN bus that joins the boards and the host tools, and the links that their documents state.

* [Architecture](docs/ARCHITECTURE.md): layers, data flows, ports and trust boundaries.
* [Interfaces](docs/INTERFACES.md): who owns each contract and where it is documented.
* [Capability matrix](docs/CAPABILITY_MATRIX.md): what is proven in software and what needs hardware, project by project.
* [Security baseline](docs/SECURITY_BASELINE.md): what the code enforces and what is still missing; and the [threat model](docs/THREAT_MODEL.md).
* [First vertical slice](docs/FIRST_VERTICAL_SLICE.md): the smallest end-to-end path that exists today.
* [CAN protocol duplication](docs/CAN_PROTOCOL_DUPLICATION.md): the protocol is implemented three times from prose; what a shared specification would hold.
* [Project catalogue](docs/PROJECT_CATALOG.md): every repository of the ecosystem, written from its own manifest.
* **Tools:** `make_catalog.py` writes the catalogue, `make_brand.py` the banner, icon and family map, `make_readmes.py` the eight READMEs of this repository, `publication_check.py` looks for anything private before a publication, and `check_all.sh` runs the own checks of every repository of the family and prints one PASS, FAIL or SKIP line each. `make_glance.py` writes the At a glance table of every repository from its manifest and from `data/glance.json` (`--check` compares, `--apply` writes); after a version bump, `python tools/make_glance.py --apply --repo NAME` refreshes the table of that repository. `check_claims.py` reads the English README of every repository of the family and fails when a sentence has a risk word (E-STOP, interlock, real-time, signed, mTLS, FDCAN, YOLO, AI-driven, autonomous, certified, ...) and no status marker next to it (planned, not implemented, optional, off by default, simulated, tested, ...), unless a person has read that line next to the code and put it in `data/claims_reviewed.json`. `check_repo_tools.py` compares the files every repository carries as the same copy (the documentation-policy and README-parity checks, the manifest version bumper, the dashboard notifier workflow) and fails when one differs. `sync_repo_tools.py` puts the canonical copy of those files (`template/eh3d-repo-template`) into every repository, keeping each file's line endings; without `--apply` it only lists what would change. The same tools write and check a lock file, `tools/devtools.lock.json`, in each repository (the version of the shared set from URTC-DEVTOOLS and the SHA-256 of every shared file): an edited copy, a missing file, a file the lock does not list or a copy that fell behind the set are reported. `status_lights.py` is one of the shared files: the validator of each repository fails when a light of its Project status table is above what its manifest (`maturity`, `evidence`) allows. `urtc_doctor.py` is the single entry point: one report with the tools of the machine (Python, git, Node, the ARM compiler, PySide6, serial ports), the versions of every repository (manifest, source file and newest changelog entry), the copies of URTC-COMMON and the firmware bundled by the flasher and the web studio, the validation of every repository and the checks of this one; `--fast` leaves out the validations and `--online` compares the bundled firmware with the newest release.

## 🧩 Role in URTC

URTC-DOCS is the memory of the ecosystem: the place where the architecture, the interfaces, the security baseline and the capability matrix live, and where the tools that compare all the repositories side by side are kept. Each repository keeps its own README, tests and contract; this one says how they fit together and what has really been proven.

## 🏛️ Architecture

<p align="center">
  <img src="images/architecture.svg" alt="URTC-DOCS architecture: what it reads, what it holds and what it feeds" width="100%">
</p>

How the parts of this repository fit together. The picture is drawn from `docs/architecture.json` and checked against the code.

## 🚀 Quick start

**Requirements:** Python 3.10 or newer; pytest for the tests

```bash
python tools/make_catalog.py --check                 # the catalogue is current (needs the repositories next to this one)
python tools/make_brand.py --check                   # the banner, icon and map are current
python tools/make_readmes.py --check                 # the eight READMEs are current
python tools/make_glance.py --check                  # the At a glance tables of the family are current (needs the repositories next to this one)
python tools/publication_check.py                    # nothing private would leave with a publication
python tools/check_claims.py --require-siblings      # no README states a risky capability without its status (needs the repositories next to this one)
python tools/check_repo_tools.py --require-siblings  # the files every repository carries as the same copy are the same (needs the repositories next to this one)
bash tools/check_all.sh                              # the checks of every repository, one line each
python tools/urtc_doctor.py                          # the doctor: one report on this machine and on every repository
python -m pytest tests -q                            # the unit tests of the tools
```

## 🧪 Testing

The suite has 183 tests (`python -m pytest tests -q`). They run the generators of the catalogue, the brand, the At a glance tables, the status tables and the READMEs on fixtures, the checks of the claims, the shared files, the publication and the doctor, the conformance vectors of the CAN notes, and check that the READMEs of this repository are exactly what the generator writes.

## 🏗️ Build & Release

`build.sh` / `build.bat` install the package and run the tests, and `build-test.sh` / `build-test.bat` check without installing; neither changes a version.

## 📂 Repository Structure

<p align="center">
  <img src="images/repository-structure.svg" alt="Repository structure of URTC-DOCS" width="100%">
</p>

<details>
<summary>Text version of the tree</summary>

```text
URTC-DOCS/
├── docs/                                              architecture, interfaces, capability matrix, security baseline, threat model and the generated catalogue
├── src/urtc_docs/                                     the tools as a package: catalogue, brand, READMEs, At a glance, status, checks
├── tools/                                             thin scripts over the package, check_all.sh and the shared CI checks
├── data/                                              the numbers of At a glance and the reviewed claims
├── template/                                          the canonical copy of the files every repository shares
├── tests/                                             unit tests of the tools
├── brand/                                             the icon
├── images/                                            banner and the pictures of this README
├── .github/                                           CI workflow, issue and pull-request templates
├── build.sh build.bat                                 build scripts
├── build-test.sh build-test.bat                       build and test scripts that change nothing in the repository
├── test.sh test.bat                                   run the tests
├── run.sh run.bat                                     start the program
├── urtc.project.json                                  manifest: version, role, maturity and build command
├── CHANGELOG.md                                       what changed in each version
├── SECURITY.md SUPPORT.md                             security policy and support
├── CONTRIBUTING.md CODE_OF_CONDUCT.md                 how to contribute and the code of conduct
├── .gitattributes .gitignore                          Git settings
├── bump.py bump_version.py bump_manifest_version.py   scripts that raise the version
├── LICENSE LICENSE.md                                 software license and documentation license
└── pyproject.toml requirements-dev.lock ruff.toml     package, locked tools and lint settings
```

</details>

## 🗺️ Roadmap & Known limits

**Known limits today**

* The security baseline and the threat model are written from the other repositories as they were read; nobody outside the project has reviewed them.
* The nightly run fetches every repository of the family and compares their summary tables, claims and catalogue structure; a stale version in the catalogue is reported but does not fail the night.
* The documents describe software; no hardware is involved and none of the claims about boards has been checked on a board.

**Next**

* Keep the catalogue, the At a glance tables and the capability matrix current as the repositories change.

## 🌍 Languages

README and texts exist in English, Spanish, French, Italian, German, Chinese, Japanese and European Portuguese.

## 🔗 Related Projects

URTC is made of independent repositories, each with its own version, tests and README. This is the family, by group:

* **URTC Tool Platform:**
  * [URTC](https://github.com/JuanenRac/URTC) - firmware of the tool-head board (25 tool profiles, CAN bootloader) and the CAN protocol reference.
  * [URTC-COMMON](https://github.com/JuanenRac/URTC-COMMON) - the CAN protocol written once as data (specification, generated tables, conformance vectors) and the code the programs share.
  * [URTC-FLASHER](https://github.com/JuanenRac/URTC-FLASHER) - desktop tool that updates the board firmware over CAN or over SWD/JTAG.
  * [URTC-GATEWAY](https://github.com/JuanenRac/URTC-GATEWAY) - gateway in front of the CAN bus: lets only listed identifiers through, limits their rate and asks for a session key.
  * [URTC-SMART-RACK](https://github.com/JuanenRac/URTC-SMART-RACK) - hardware-independent C logic and command protocol for a tool rack with pre-heating and lifecycle tracking.
  * [URTC-TESTER](https://github.com/JuanenRac/URTC-TESTER) - desktop live CAN-bus tester that shows the controls and telemetry of the tool profile a board reports.
  * [URTC-VISION-TOOL](https://github.com/JuanenRac/URTC-VISION-TOOL) - sensor-frame protocol in C and a Python thermal/RGB companion for an inspection tool head.
  * [URTC-WEB-STUDIO](https://github.com/JuanenRac/URTC-WEB-STUDIO) - browser app that flashes and tests the board over Web Serial and SLCAN, with nothing to install.
* **Ecosystem Operations:**
  * [URTC-DEVTOOLS](https://github.com/JuanenRac/URTC-DEVTOOLS) - the shared repository tools of the family as one versioned set, with a lock file that tells a copy that was edited from one that fell behind.
  * **URTC-DOCS** (this repository) - architecture, interfaces, security baseline and generated catalogue of the ecosystem, plus the tools that compare all repositories.
  * [URTC-UPDATER](https://github.com/JuanenRac/URTC-UPDATER) - desktop tool that detects, installs and updates the repositories of the URTC family, one explicit action at a time.

**Sister projects (independent, with the same base and tools):**

* **[HYDRA-UMC-DOCS](https://github.com/JuanenRac/HYDRA-UMC-DOCS)** - sister project: the documentation hub of HYDRA-UMC, an independent ecosystem that shares this one's base and tools
* **[ARMOR-DOCS](https://github.com/JuanenRac/ARMOR-DOCS)** - sister project: the documentation hub of A.R.M.O.R., the security ecosystem, also independent and on the same base
* **[JuanenRac](https://github.com/JuanenRac/JuanenRac)** - the profile and the status dashboard of all the ecosystems

## 📚 Documentation

Where to read more:

* [Capability matrix: what is proven and what is not](docs/CAPABILITY_MATRIX.md)
* [Project catalogue: versions and kinds of the repositories](docs/PROJECT_CATALOG.md)
* [CAN protocol: three implementations of one prose specification](docs/CAN_PROTOCOL_DUPLICATION.md)
* [Changelog of this repository](CHANGELOG.md)
* [License (GPL-3.0-or-later)](LICENSE)

## 🤝 Contributing & Community

* Before a pull request run `URTC_CI=1 python tools/ci_validate.py`: it must pass. See [CONTRIBUTING.md](CONTRIBUTING.md) and the [code of conduct](CODE_OF_CONDUCT.md).
* The README exists in eight languages: a change to the text is made in all eight files, and the sections shared with other repositories are written by `tools/readme_sections.py` of URTC-COMMON.
* Do not describe as working on a board what has only been built.
* Report a vulnerability privately: [SECURITY.md](SECURITY.md). Questions, ideas and reports: electrohobby3d@gmail.com ([SUPPORT.md](SUPPORT.md)).
* Questions, ideas and reports: electrohobby3d@gmail.com

## 👤 AUTHOR

**JuanenRac (Electro Hobby 3D)** · electrohobby3d@gmail.com

## 📜 LICENSE

Software: GPL-3.0-or-later - see [LICENSE](LICENSE). Documentation: CC BY-SA 4.0 - see [LICENSE.md](LICENSE.md).
