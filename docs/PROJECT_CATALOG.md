<!--
=============================================================================
URTC-DOCS - Project catalogue of the URTC ecosystem
Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
CC BY-SA 4.0 - see LICENSE.md
=============================================================================
-->

# Project catalogue

Every repository of the ecosystem, written by `tools/make_catalog.py` from the `urtc.project.json` of each repository found next to this one, so that no version, maturity or role in the tables can be behind its project. Nothing between the two markers is typed by hand; the text around them is.

* **Family** is the `family` of the manifest. **Parent** is its `parent`: the repository that is the integration parent of the family, `-` for a root.
* **Maturity** follows the SDK's definition (`HYDRA-UMC-SDK/docs/PROJECT_MANIFEST.md`): *scaffolding* is real, tested code not yet exercised in its real context; *functional* has been exercised against some real target; *established* has seen sustained real use in this ecosystem's own deployment; *production* is reserved for continuous unattended deployment. For the PC tools of URTC the label does not imply a run against a real board: see `CAPABILITY_MATRIX.md`.
* **What it is** is a sentence written for this catalogue from the manifest and README of each repository (`src/urtc_docs/descriptions.py`); a repository without one shows the start of the notes of its manifest.
* The firmware repository is called exactly `URTC`. The catalogue lists the repositories that carry a `urtc.project.json` with `ecosystem: "URTC"`, which is also what URTC-UPDATER and the profile dashboard discover. `ELECTRO-HOBBY-3D-UPDATER` has its own manifest (`electro-hobby-3d.project.json`) and belongs to none of the three ecosystems: it dispatches to the updaters of HYDRA-UMC, URTC and A.R.M.O.R.
* Regenerate with `python tools/make_catalog.py` (the repositories must sit next to this one); `--check` fails when the table is stale and `--check-structure` fails only when a repository appeared or disappeared or changed kind.

<!-- catalog:begin -->
**10 repositories** in 2 families: 3 scaffolding, 6 functional, 1 established.

### Ecosystem Operations

| Repository | Version | Maturity | Role | Stack | Target | Parent | What it is |
|---|---|---|---|---|---|---|---|
| [URTC-DOCS](https://github.com/JuanenRac/URTC-DOCS) | 0.0.8 | Scaffolding | tool | python | user-pc | - | Architecture, interfaces, security baseline, capability matrix and generated project catalogue of the ecosystem, plus the tools that compare all repositories. |
| [URTC-UPDATER](https://github.com/JuanenRac/URTC-UPDATER) | 0.1.7 | Established | tool | python | user-pc | - | Finds the ecosystem repositories on a machine from their manifests and installs or updates them after an explicit confirmation. |

### URTC Tool Platform

| Repository | Version | Maturity | Role | Stack | Target | Parent | What it is |
|---|---|---|---|---|---|---|---|
| [URTC](https://github.com/JuanenRac/URTC) | 0.3.9 | Functional | firmware | firmware-c | mcu | - | Firmware of the tool-head board (STM32F303, 25 tool profiles, CAN bootloader, expansion slave) and the CAN protocol reference; no populated board exists yet. |
| [URTC-COMMON](https://github.com/JuanenRac/URTC-COMMON) | 0.0.5 | Scaffolding | library | python | user-pc | - | The CAN protocol as data: a specification with generated C, TypeScript and Python code, conformance vectors and the Python transports; nothing uses it yet. |
| [URTC-GATEWAY](https://github.com/JuanenRac/URTC-GATEWAY) | 0.0.1 | Scaffolding | tool | python | user-pc | - | Gateway in front of the CAN bus: the identifiers a host may send (made from the specification), a payload check, a rate limit and a session key, each one switchable; tested on the host only. |
| [URTC-SMART-RACK](https://github.com/JuanenRac/URTC-SMART-RACK) | 0.1.8 | Functional | firmware | firmware-c | user-pc | - | Hardware-independent C logic and rack command protocol for a tool rack with pre-heating and lifecycle tracking; no board exists yet. |
| [URTC-VISION-TOOL](https://github.com/JuanenRac/URTC-VISION-TOOL) | 0.1.2 | Functional | firmware | firmware-c | user-pc | - | Sensor-frame protocol in C and a Python thermal/RGB companion for an inspection tool head; no board or camera has been used yet. |
| [URTC-FLASHER](https://github.com/JuanenRac/URTC-FLASHER) | 0.3.8 | Functional | tool | python-qtquick | user-pc | URTC | Desktop tool that updates the board firmware over CAN (bootloader protocol, signed images) or over SWD/JTAG; tested against a simulated bootloader only. |
| [URTC-TESTER](https://github.com/JuanenRac/URTC-TESTER) | 0.3.9 | Functional | tool | python-qtquick | user-pc | URTC | Desktop live CAN-bus tester that shows the controls and telemetry of the tool profile a board reports; checked against fake transports only. |
| [URTC-WEB-STUDIO](https://github.com/JuanenRac/URTC-WEB-STUDIO) | 0.3.4 | Functional | ui | node | user-pc | URTC | Browser app that flashes and tests the board over Web Serial and SLCAN; the pure logic is tested, the transport and screens are not. |
<!-- catalog:end -->
