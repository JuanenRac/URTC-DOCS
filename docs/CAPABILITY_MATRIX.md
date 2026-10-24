<!--
=============================================================================
URTC-DOCS - Capability matrix of the URTC ecosystem
Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
CC BY-SA 4.0 - see LICENSE.md
=============================================================================
-->

# Capability matrix

What each capability is *today*, said the same way for every repository. It is written from what each repository's own README, changelog and manifest state; this repository has no measurement record of its own, so a row never says more than its source does. When two documents of the same repository disagree, the row follows the more cautious one and says so.

## Levels

| Level | Meaning |
|---|---|
| **Absent** | Nothing exists: the repository says it is not written, or it is planned only. |
| **Builds** | The code compiles and links (for firmware, with the ARM toolchain) and may have host tests for its helper logic, but it has not run on the target it is for. |
| **Local** | Works and is tested on a computer (unit tests, host-native C tests, end-to-end checks with a fake transport), with no real device on the other end. |
| **Emulated** | Tested against a simulator written from the protocol description (`MockCAN`, a fake transport, a simulated bootloader). It proves the handling of a *simulated* condition, never that the real board behaves so. |
| **In use** | The repository was exercised against its real intended context for a sustained time and its documents say so in words. |
| **Verified** | Measured on the real target, and the source says so in words. |

A unit test, a simulator and a bench result are different claims, and a lighter one never stands in for a heavier one. The README of URTC-FLASHER gives the reason in its own words: two defects (an image that could never be installed because the last partial page was never acknowledged, and a read-back that dropped its last frame) passed the tests precisely because the simulation was more forgiving than the real bootloader.

**The one fact that colours every row:** no populated URTC board exists yet. Nothing in the ecosystem has been measured on one, and nothing here reaches **In use** or **Verified** for a board-facing capability. Nothing has been transmitted to a real board by any of the three PC tools.

**A caution about the `maturity` field.** The manifests of URTC-FLASHER, URTC-TESTER and URTC-WEB-STUDIO say `established`, and the SDK's definition of that word is "sustained real use in this ecosystem's own deployment". Their READMEs state that no run against a real board has happened. The field therefore cannot be read as hardware verification; read this matrix instead. The SDK's definition of `functional` cites `URTC` as "firmware flashed and running real physical tool heads", while the firmware README says no populated board exists; one of the two statements is out of date **(open question for the owner)**.

## Firmware: URTC

| Capability | Level | Evidence and limits |
|---|---|---|
| Main application, 25 tool profiles, thermal PID loops, per-tool telemetry and watchdogs | Builds | The README calls it feature-complete; the full ARM build of the four components was run for the newest release. No board. |
| Thermal-runaway guard (`thermal_guard.c`) | Local | Host test with a simulated heater (`tests/test_thermal_guard.c`). The limits (449 C iron, 310 C hotend) were never measured on a heater. |
| CAN dispatch routing, lifetime thermal counters, MLX90640 driver logic (with a fake I2C), version wire format | Local | Host-native C tests; the version wire helpers run under the address and undefined-behaviour sanitizers in the build script. 38 host suites in all compile the firmware sources against a fake HAL (`tests/host_hal/`), run under the sanitizers and `gcc -fanalyzer`, and are held to a coverage floor (95 percent of the lines of the 78 sources they compile; the CI floor is 90). |
| Main bootloader: golden-image A/B update, CRC32 and HMAC-SHA256 verified in a backup slot before the copy, anti-rollback | Builds | "Compiles and links clean"; the README asks for a bench test before trusting it unattended. |
| Expansion slave application and bootloader (STM32F303CB over a bit-banged I2C link) | Builds | Real code; the README says the I2C link with a real expansion chip was not verified. None of the six expansion variants has a schematic yet. |
| Several tool heads on one CAN bus (multinode): node address from the ID jumpers, discovery, selection of the one active head, per-node status, safe stop, address-conflict detection, a persistent switch that is off by default | Local | Implemented in the main application (0.3.8) and tested on the host only (`tests/test_multinode.c`, under the address and undefined-behaviour sanitizers; it also checks that with the switch off the receive path and every identifier are those of a single head). The bus-level behaviour of two real boards, the timing and the safe state on real outputs were never tried; no host program uses it yet. |
| Firmware PATCH number over CAN (`0x7E9` and the extended frames) | Local | Wire helpers tested on the host; the changelog says the new frames are "not verified on a physical board". |
| Firmware images and signatures published as release assets | Local | The newest release carries 17 assets and the index `firmware_manifest.json`; the build script, the asset check and its tests exist. **The published application images are signed with the public development key** (`signing_key_kind: dev` in the release manifest). |
| Release-key signing (`URTC_SIGNING_KEY_FILE`, `URTC_RELEASE=1`) | Builds | Implemented in the build script and `firmware_signing.py`; no release image uses it at the time of reading. |
| Ed25519 signatures instead of the shared HMAC key | Absent | Planned for the first hardware bring-up, with the flash-budget reasoning in `docs/FIRMWARE_SIGNING.TXT`. |
| Hardware design | Absent | Schematic and BOM are "still being finalized". |

## URTC-FLASHER

| Capability | Level | Evidence and limits |
|---|---|---|
| CAN-OTA update of the main board (HardwareID check, HMAC chunks from a published signature, per-page acknowledgement, verify, downgrade authorisation) | Emulated | Run against `MockCAN`. The README reports 47 pytest files and 515 tests, 78 of them skipping without PySide6. |
| CAN-OTA update of the expansion slave | Emulated | Same simulator; the Qt Quick deck has no slave target. |
| CRC32 and HMAC-SHA256 computation | Local | "Verified byte-for-byte against the bootloader's own C implementation". |
| Read-back (backup) of the installed firmware over CAN | Emulated | The simulated bootloader answers a read-back; the odd-size defect was found by reading the protocol, not by a board. |
| Version query including the patch number | Emulated | `tests/test_patch_number.py`; the changelog says it is tested against the simulator only. |
| SLCAN, SocketCAN, python-can transports | Local | Frame packing checked against Linux's `struct can_frame` layout with a round-trip test. No adapter in the environment where it was written. |
| Bit-rate auto-detect | Local | Listens only (`L`), so it cannot disturb a live bus; tested with fakes. |
| Full-chip SWD/JTAG programming | Builds | `verify_qt_swd_full_chip_flash.py` only builds the pyOCD / CubeProgrammer commands with `dry_run=True`. |
| Download of images from the GitHub release | Local | Host, size and digest rules have tests; the `firmware/` folder is not in git and `tools/sync_firmware.py` fills it from the newest official release, checking the digests and the Ed25519 release signature of every file. |
| Refusal of dev-signed images | Local | Opt-in (`require_production_signature`), off by default; the official images are dev-signed so far. |
| List of the official images for a board with no firmware and no image on disk | Local | The decision (boot-loader answer, empty `firmware/`) and the list are tested with a fake release; nothing is downloaded or chosen by itself, and no board was involved. |
| Check for updates of the program itself from a signed package (only a strictly newer version, SHA-256 and Ed25519 signature checked, explicit confirmation, rollback) | Local | `self_update.py` of URTC-COMMON, shared with the tester and the updater; tested with throw-away keys and fake releases, nothing is downloaded by the tests. |
| Several tool heads on one bus: the Tool heads window finds the heads, asks for a confirmation before selecting one and refuses single-head commands until one is selected | Emulated | The rules (`node_picker.py` of URTC-COMMON) are held to shared vectors and a model of the nodes; tried against a model of the bus only, not against boards. |
| Flashing through a virtual board (SLCAN over TCP, `socket://` ports and `URTC_VIRTUAL_PORT`) | Emulated | `urtc_can/virtual_board.py` of URTC-COMMON plays an SLCAN adapter and a board (application and bootloader) written from the protocol description; a test runs the real flasher through it end to end, over a TCP socket and over the real pyserial URL handler. It proves the handling of a simulated board, not a real bootloader. |

## URTC-TESTER

| Capability | Level | Evidence and limits |
|---|---|---|
| Payload encoders for the migrated control families, rejecting out-of-range values | Local | `advanced_protocol.py` has no transport import, so the tests prove boundaries and safe-off frames on any computer. |
| Qt Quick bridge logic, custom frame, telemetry watch, utility panels | Local | Four `verify_qt_*.py` end-to-end checks against a fake transport with real cross-thread signal delivery, run offscreen in CI. |
| Per-tool panels of the Qt Quick deck (25 tools) | Builds | The deck builds each panel from the encoders and sends through the checked bridge; the offscreen end-to-end scripts and the tests cover the bridge, not every panel one by one. |
| Bus statistics, health reads, safe-off of heaters, result records, session export | Local | `tests/` holds files for each of them (`test_bus_stats.py`, `test_reads_and_health.py`, `test_heater_safe_off.py`, `test_result_record.py`, `test_qt_session_export.py`). |
| SLCAN and SocketCAN transports | Local | The classes are the copy of URTC-COMMON, whose tests cover them (typed errors, a failed bind, a pyserial URL against the virtual board); no adapter in the environment where it was written. |
| Replay of a recorded `.trc` / `.asc` trace in the deck, and the Black Box viewer (chart of the recorded temperature and set-point, saved JSON / CSV records opened with no board) | Local | The player has no timer of its own and is tested with a clock moved by hand; the records are held to the shared vectors. Never tried with a trace or a record from a real board. |
| Test plans in the window (`plans/`, same engine as `--headless`, only on an armed connection) | Emulated | Run against the simulated tool head; a plan that actuates needs the operator to allow it. |
| Several tool heads on one bus (Tool heads window) | Emulated | Same rules and vectors as the flasher; tried against a model of the bus only. |
| Without a window (`--headless`): identify, self-test and test plans (JSON) with a log and a result record; a command that actuates needs the plan and the operator to allow it, and a plan can repeat a command so that the firmware's watchdog does not drop it | Emulated | Run against the simulated tool head and recorded traces that live in the tester itself (`tester_simulator.py`); the head drops an unrefreshed order like the firmware but is the same author's reading of the protocol. No board, no adapter. |
| Heater PID panel (`0x1B9` / `0x1BA`: gains, relay autotune, state) | Emulated | The frames are checked against the examples of the specification and the simulated head answers them, autotune included. The firmware function is host-tested only and was never run on a heater. |
| Identify and run read-only plans through a virtual board (`--transport serial --port socket://...`) | Emulated | The command line and the SLCAN transport run unchanged against the virtual board of URTC-COMMON over the real pyserial URL handler (4 tests). The virtual board is a model of the application, not a tool head, so the self-test of a tool reports what it cannot read. |

## URTC-WEB-STUDIO

| Capability | Level | Evidence and limits |
|---|---|---|
| SLCAN parsing, request/answer matching, image and manifest checks, tool limits, confirmations, simulator separation, trace export, eight languages | Local | Vitest; `npm run lint` type-checks. |
| Flasher Studio, Tester Studio, the bus analyser | Builds | "Real code verified only by those tests, type-checking and code review", plus the end-to-end checks in a real Chromium (Playwright) against a model of the adapter and the board. |
| Web Serial transport | Emulated | Driven by the end-to-end checks through a model of the adapter and the board that sits behind `navigator.serial` (`e2e/support/fakeBoard.ts`); never run against a USB-CAN adapter. |
| Works offline and can be installed (service worker, web app manifest, notice of a newer version) | Emulated | Checked in a real Chromium with the network switched off; the copy never keeps the GitHub API. Nothing is published: GitHub Pages is switched off until the owner turns it on. |
| Several tool heads on one bus (Heads window) | Emulated | `src/lib/nodePicker.ts` is held to the same shared vectors as the flasher and the tester; tried against a model of the bus only. |
| Control, OLED, Specs/BOM and Thermal IR tabs | Local | Labelled sandbox tabs with no CAN traffic. The thermal view there is generated noise, not a sensor reading. |
| Firmware download from the GitHub release, patch number over CAN | Local | Unit-tested logic; the browser limit (files are served from a host without CORS headers) is handled and documented. |
| Heater PID panel in Tester Studio (`0x1B9` / `0x1BA`) | Local | Frame encoding and decoding are unit-tested against the specification; the panel itself is checked by type-checking and the build only, never run against a board. |
| Replay of a recorded `.trc` / `.asc` trace into the log and the panels with no board | Local | The parser reads what the Studio exports and refuses what is not a frame; the player is tested with a clock moved by hand (speed, pause, stop, loop, long silences). Replayed frames are marked, never answer a request and are never exported as the board's. Never tried with a trace from a real bus tool. |
| Black Box viewer: chart of the recorded temperature and setpoint, and saved JSON / CSV records opened with no board | Local | Every shared vector round-trips through the JSON and the CSV; a file with a value out of range or too many samples is refused. The chart itself is checked by type-checking and the build only; no real fault record has been read. |

## URTC-SMART-RACK

| Capability | Level | Evidence and limits |
|---|---|---|
| Tool-ID decoding, lifecycle tracking, pre-heat decision, rack command protocol with CRC8, command validation, link watchdog, multi-slot inventory | Local | Host-native C tests: 467 assertions, the number the README and the manifest both quote. The serial deframer is held to 19 shared streams of bytes with their arrival times, and the host tests are held to a coverage floor. |
| Rack CRC-8 shared with the vision link (header copied from URTC-COMMON and checked against its lock) and checked against the shared vectors | Local | Host-native C tests run the vectors that URTC-COMMON writes as C tables; no board. |
| Minimum interval between two commands accepted for one tool (20 ms by default, a build option; a safe state and a retransmission are never held back) | Local | Host-native C tests with the shared limiter of URTC-COMMON; no board. |
| Serial frame version 2 (every multi-byte value big-endian, version 1 refused) | Local | Held to the shared vectors of URTC-COMMON; no board. |
| Cross-compile for Cortex-M4F | Builds | Proves compile and link against a placeholder linker script, "not that any of this runs on real silicon". |
| CAN, F-RAM and GPIO drivers; a real heater | Absent | "No PCB/schematic exists for this board yet". |

## URTC-VISION-TOOL

| Capability | Level | Evidence and limits |
|---|---|---|
| Sensor frame protocol (versioned framing, CRC8), range validation, rate limiter, diagnostics counters | Local | 165 host-native assertions, run by the CI through `build_firmware.sh`, with a coverage floor on the lines of `src/`. |
| Vision CRC-8 shared with the rack (header copied from URTC-COMMON and checked against its lock) and checked against the shared vectors | Local | Host-native C tests run the vectors that URTC-COMMON writes as C tables; no board. |
| Python vision companion: synthetic frames, false colour, RGB-to-thermal ROI alignment, temperature statistics, inspection by region, sensor drift, rack check over time | Local | 135 pytest cases (the count the README and the manifest quote), run in CI with a coverage floor. |
| `capture`: the thermal image of a URTC head through a serial CAN adapter | Emulated | Played against a simulated SLCAN adapter and head only. |
| Reading a real MLX9064x or RGB camera, per-pixel calibration | Absent | Needs a board and cameras. |

## URTC-UPDATER and the discovery chain

| Capability | Level | Evidence and limits |
|---|---|---|
| Manifest discovery, version comparison, commit comparison | Local | Own tests, including a local HTTP fixture server and temporary git repositories with a local bare remote. |
| Install and update: clone, stage, build-test, promote, keep the previous checkout as a backup | Local | Run once end to end against GitHub in an isolated workspace: a clean install and a later update of a real repository (106 own tests passing in that run). One documented run is not sustained use. |
| Commit-signature policy | Local | `warn` by default (installs and says so), `require` refuses an unsigned candidate before anything is read; both have tests. |
| QML screens | Local | The window and its dialogs are loaded offscreen in the tests (they open and answer); how they look is checked by eye. |
| Install a program from the signed package of its release (list, check, install, rollback), restore a kept installation, the two security options (signed commits, ask before the build check) | Local | Tests with throw-away keys and fake releases; nothing goes over the network. |
| Dashboard discovery of the URTC repositories | In use | The profile workflow installs a pinned revision of this updater and discovers every public repository with a URTC manifest. |

## URTC-DOCS

| Capability | Level | Evidence and limits |
|---|---|---|
| Catalogue, brand, README and publication generators; ecosystem check | Local | Unit tests run in CI, also on Windows. |
| Nightly comparison of all repositories | Local | A workflow exists; it has not run over time yet, which is why the manifest says `scaffolding`. |

## Inconsistencies noticed while reading

* FLASHER and WEB-STUDIO keep no firmware images in git: `tools/sync_firmware.py` and `scripts/sync-firmware.mjs` download the newest official release and check the digests and the detached Ed25519 `.sig` file of every asset. The application images of that release are still signed with the public development key.
* The copies of `tools/ci_validate.py` differ slightly between repositories (FLASHER and TESTER accept an "INSTALL AND RUN" heading in a function that is not called; UPDATER does not require the four community files). None of the differences changes what a manifest has to contain.
* `README_por.md` is required and compared with the English original, like the other seven translations, by `_readme_parity.py`.
