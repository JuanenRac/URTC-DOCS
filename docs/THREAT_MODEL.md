<!--
=============================================================================
URTC-DOCS - Threat model of the URTC ecosystem
Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
CC BY-SA 4.0 - see LICENSE.md
=============================================================================
-->

# Threat model

A desk analysis of who could do what to the URTC ecosystem, what stops them today and what does not. It extends the firmware repository's own `docs/CAN_THREAT_MODEL.TXT` (which is the reference for the bus) to the host tools, the distribution of firmware and the repositories. It was not tested against an attacker, and no board exists to test it on. Every row says whether its mitigation is **code** (checked by tests), **setting** (off unless chosen), **requirement** (something the installation must provide) or **none**.

## What is worth protecting

| Asset | Why |
|---|---|
| People and property near a tool head | The heads include a 10 W laser, heater stages (T12 iron, hot air, 3D-printer hotend), a spot welder, an ultrasonic welder, a drill and motors. The firmware README opens with a safety notice. |
| The firmware on the boards | A bad image can brick a board that can then only be recovered over SWD. |
| The signing key | It decides which images a board accepts. |
| The machines and accounts of the author and of users | The updater and the tools run code on a PC. |
| Private material of the author | Notes, credentials, personal addresses must stay out of the public repositories. |

## Who

| Actor | Capability assumed |
|---|---|
| **A node on the bus** (a robot controller that malfunctions, a service laptop, a device added by mistake) | Puts any 11-bit frame with up to 8 bytes on the wires. |
| **Somebody with physical access to a board** | Reads or reprograms it over SWD/JTAG. |
| **A network attacker between a PC and GitHub** | Limited by HTTPS; assumed unable to forge GitHub's certificate. |
| **A holder of the GitHub account or of a repository** | Publishes a commit, a release or an asset. |
| **An operator who makes a mistake** | Clicks the wrong button, flashes the wrong file, uses the wrong bit rate. |
| **A reader of the public repositories** | Reads everything that is published, including history. |

## Scenarios

### On the bus

| # | Scenario | What stops it | Kind | What does not |
|---|---|---|---|---|
| B1 | A rogue or faulty node commands a head: arms the laser (`0x160`, two bytes, no magic), starts a motor, heater, weld or UV pulse. | Nothing on the bus. The actuator watchdog stops the output when the node stops repeating the frame. | none (watchdog limits the duration) | The command itself. The firmware says this is "a property of the bus, not a bug to be fixed in this firmware". |
| B2 | Hazard created by B1 (laser fire, burn, fire). | A hardware interlock wired in series with the laser line and the driver supply, an enclosure switch or key switch, and an emergency stop that removes actuator power. | requirement (R1, R5) | Anything in software: the interlock line PB6 is software controlled; a "stop" frame is not an emergency stop. |
| B3 | A corrupted or misrouted frame triggers a destructive command (bootloader entry, saved-state erase, feeder reset). | 4-byte magic payloads. | code | A node that knows the magic values, which are published. |
| B4 | A flood of frames, or bus-off, starves the tool head or hides its answers. | The scan-probe impact frame `0x095` has the lowest identifier, so it wins arbitration; error counters are readable (`0x7FB`/`0x7FC`). | code (partial) | Rate limiting does not exist in the firmware; the threat model says it belongs in a gateway. |
| B5 | A tool is installed on a bus that is bridged to Wi-Fi or Ethernet. | Nothing. | requirement (R3) | There is no whitelisting gateway in the ecosystem. |
| B6 | A wrong bit rate on the adapter produces error frames on a running bus. | URTC-FLASHER's and URTC-TESTER's auto-detect only listens (`L`); an explicit rate is the user's choice. | code | A manual wrong choice. |

### On the firmware

| # | Scenario | What stops it | Kind | What does not |
|---|---|---|---|---|
| F1 | A node sends a malicious firmware image through the bootloader protocol. | HMAC-SHA256 over the image under the board's key, CRC32, HardwareID, size; the image is verified in a backup slot before it replaces the main slot. | code (host-tested pieces; bootloader never run on a board) | Anybody who holds the key. For a board built with the public development key, that is everyone. |
| F2 | An old, vulnerable but validly signed image is replayed (rollback). | Anti-rollback comparing major, minor and, when both carry one, patch. | code | A one-shot downgrade authorisation (`0x7FD` + magic) exists on purpose; it does not skip the signature, only the version order. A legacy flasher that sends no patch can reinstall the same major.minor. |
| F3 | The key leaks, or is read from a board's flash. | Nothing once it has leaked; the key is injected at build time from a private file and is not in the repository or in either flashing tool. | none after the fact | Symmetric design: one board's flash reveals the key of every board built with it; read-out protection is not mentioned anywhere traced **(inferred)**. Replacement is the planned Ed25519 scheme, not built. |
| F4 | The published images are signed with the development key. | Release builds refuse that key. | setting | The newest published release is dev-signed, so this scenario is open for any board that trusts it. |
| F5 | An update is interrupted (power loss, cable pulled). | Update goes to the backup slot; the main slot is touched only after verification; a power loss before the copy leaves the running firmware untouched. | code (by design; not tested on a board) | The README's guarantee covers a power loss *before* the copy starts; what happens to a loss during the page-by-page copy into the main slot is not stated **(not traced)**. |
| F6 | The wrong image is flashed (the slave's image on the main board). | The bootloader's HardwareID check; FLASHER also compares the manifest's `component` and `hardware_id` with the target before the first frame. | code | An image with no manifest, flashed with a key typed at run time. |

### On the distribution and the host tools

| # | Scenario | What stops it | Kind | What does not |
|---|---|---|---|---|
| D1 | A release asset is replaced or corrupted. | The tools compare the image with its published `.sha256`; the bootloader checks the signature. | code | A replacement that also replaces the `.sha256` and the manifest is caught only by the signature, which is dev-key today. |
| D2 | A download is redirected to a foreign host. | FLASHER accepts only GitHub release assets and the asset hosts GitHub redirects to, checks the host before and after the redirect, and compares sizes. | code | A compromise of GitHub itself. |
| D3 | The operator flashes a development-signed image to a production board. | A red warning; with `require_production_signature` the image is refused. | setting | Off by default; the bundled official images are dev-signed. |
| D4 | A page or script in WEB-STUDIO sends the wrong frame to a real bus. | Tested rules keep the simulator apart from the real bus; confirmations for dangerous actions; a safe-off path. | code (logic only) | The Web Serial transport and the screens have no automated tests. |
| D5 | A key typed in at run time is stored. | FLASHER and WEB-STUDIO keep it in memory and do not save it. | code (as documented) | A key written by hand into the local `urtc_config.json` (git-ignored) stays on that PC. |

### On the repositories and the updater

| # | Scenario | What stops it | Kind | What does not |
|---|---|---|---|---|
| R1 | The GitHub account or a repository is compromised and a malicious commit is published. | The updater asks for an explicit confirmation of each project action, builds in a staging directory and keeps a backup; with `require` it refuses an unsigned candidate before reading the manifest. | setting | By default (`warn`) an unsigned commit is installed with a warning, and the build script runs on the user's PC. |
| R2 | The dashboard installs a changed updater. | The profile workflow installs the updaters from a fixed revision. | code | The pins are moved by hand. |
| R3 | A private key, address or note reaches a public file. | The public/private boundary check in each CI, the `.gitignore` rule for `.env` files, and `tools/publication_check.py` (with `--history` for removed lines). | code | A secret with no recognisable shape; the check says it proves nothing about absence. |
| R4 | An operator edits a generated file (catalogue, README, banner) and it drifts. | The unit tests and `--check` modes compare the generated files with their source. | code | Nothing prevents the edit, only its survival. |

## Residual risks, in the order they would matter on a real installation

1. The bus carries unauthenticated commands for devices that can burn or injure; the only mitigation is the installation (R1-R5), which nothing verifies.
2. The firmware signing key in use is the public development key.
3. The scheme is symmetric, so physical access to one board is access to the signing key.
4. The updater runs remote build scripts; the safer policy is opt-in.
5. Everything above is described for software that has never run on the board it is for. A first bring-up will test the watchdogs, the thermal guard, the bootloader copy and the interlock for the first time.

## Out of scope here

Electrical safety of the board itself, EMC, the mechanical design, the security of the robot controller that sits on the other end of the bus, and the HYDRA-UMC and A.R.M.O.R. ecosystems. For the first, the firmware repository's safety notice and its PCB, BOM and pinout documents are the sources.
