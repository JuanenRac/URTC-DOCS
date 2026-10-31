<!--
=============================================================================
URTC-DOCS - Security baseline of the URTC ecosystem
Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
CC BY-SA 4.0 - see LICENSE.md
=============================================================================
-->

# Security baseline

What the code of the ecosystem enforces today, what is only an option that is off by default, and what is missing. It is a reading of the repositories, **not the result of a penetration test or of an external review**, and nothing in it has been tried against an attacker or on a real board. Read it with `THREAT_MODEL.md`, which turns the same facts into scenarios.

The sources are named in each line: `URTC` (`docs/CAN_THREAT_MODEL.TXT`, `docs/FIRMWARE_SIGNING.TXT`, `docs/FIRMWARE_DISTRIBUTION.md`, `docs/CANBUS.TXT`), `URTC-FLASHER`, `URTC-TESTER`, `URTC-WEB-STUDIO`, `URTC-UPDATER`, `URTC-GATEWAY`, `URTC-COMMON` and the shared CI checks.

## Network position

* **There is no always-on network service in the ecosystem.** The boards sit on a wired CAN bus; the PC tools open a local serial port, a SocketCAN interface or (browser) a Web Serial port; the updater and the programs that check for updates make outbound HTTPS requests to GitHub. A TCP port is opened only by three optional things, each on request: the gateway (when someone starts it), the virtual board of URTC-COMMON (loopback only, for trying the tools with no hardware) and the development server of the web studio (`localhost` only).
* **The bus is assumed closed.** The threat model of the firmware requires that only the robot controller and the tool heads are on the wires and that a service adapter is plugged in only while someone services the machine, with the hazardous heads disarmed. Nothing in software checks this.
* **The bus is not to be bridged to Wi-Fi, Ethernet or the internet** without a gateway that forwards a whitelist of identifiers and rate-limits them (requirement R3 of the firmware threat model). URTC-GATEWAY is that gateway, as software: it has only been tested against fakes and a local socket, and it does not replace the hardware measures of the threat model.

## What the software enforces

### Firmware (on the host-test and build level; never on a board)

* **Actuator watchdogs.** If the commands stop, the output stops: 250 ms for the laser, drill, heaters, fans and UV, per the threat model.
* **Critical-error gate.** After a declared critical error, every command except lighting (`0x100`) and the read-only diagnostics (`0x110`, `0x190`, ...) is refused until the board is reset.
* **Magic payloads** on destructive one-shot commands (`0x7F0` enter bootloader, `0x7FD` authorise a downgrade, `0x192` erase the saved state, the feeder reset), so a corrupted or misrouted frame cannot trigger them by chance. This is protection against accidents; the values are public.
* **Thermal-runaway guard** on the iron, the hot air and the hotend: a maximum on the *measured* temperature, a heating watch and a holding check; a fault cuts the heater, latches the error and reports the reason in `0x111`.
* **Range checks on what the board measures,** whatever the bus says.
* **Recovered state is never re-armed.** The saved heater, laser and motor setpoints can be read after a reset but are not applied.
* **Entering the bootloader cuts power to every actuator inline** before the reset.
* **Bootloader.** Updates go to a backup slot and are copied only after size, CRC32, HMAC-SHA256 and HardwareID have matched; any mismatch leaves the main slot untouched and the bootloader never jumps into an image that failed a check. Anti-rollback compares major, minor and (when both carry one) patch; a downgrade needs a one-shot authorisation that must be sent again for each attempt and the image must still be correctly signed.
* **Host tests with sanitizers:** 38 suites compile the firmware sources against a fake HAL and run under the address and undefined-behaviour sanitizers and `gcc -fanalyzer`, with a coverage floor; they cover the version wire format, the dispatch routing, the thermal guard, the counters, the handlers of the tools and both bootloaders. The firmware is also held to the shared vectors of URTC-COMMON.
* **The bootloader answers a read-back or a downgrade authorisation only in the session the application started** (the application leaves a mark in a backup register of the RTC block when it accepts `0x7F0`; the bootloader reads it once and clears it).

### Host tools

* **Encoders refuse instead of clamping** (URTC-TESTER, `advanced_protocol.py`), and the transports of FLASHER and TESTER refuse an identifier above `0x7FF` or a payload above 8 bytes before sending.
* **URTC-FLASHER** refuses an image whose sha256 differs from its published manifest before any bus traffic; refuses an image built for the other board (`component` and `hardware_id` are compared before the first frame); sends only a published signature and never signs; shows a red warning for an image signed with the public development key and, with `require_production_signature` set, refuses it; says what it replaces (installed -> new) and warns about a downgrade; writes an update report with its own digest; keeps the deadline arithmetic on the monotonic clock; keeps worker threads away from the window; restricts downloads to GitHub release assets and the asset hosts it redirects to, checking the host before the request and again on the final address, and compares the byte count with the announced size.
* **Bit-rate auto-detect only listens** (SLCAN `L`), so searching cannot disturb a running bus.
* **URTC-WEB-STUDIO** keeps its simulator apart from the real bus by tested rules, asks for confirmation of dangerous actions, has a safe-off path, parses only standard `t` frames, refuses an image whose digest differs from the published one, stops a flash when the manifest cannot be downloaded instead of asking for a key, and shows no key in its JavaScript.
* **The programs that update themselves** (the flasher, the tester and the updater, through `self_update.py` of URTC-COMMON) offer only a strictly newer version for their own system, require the SHA-256 and the Ed25519 signature of the package to match, ask for an explicit confirmation and keep the previous version for a rollback; the options are conservative (no check unless the person asks, no way to skip the checksum or the signature or to add a host).
* **URTC-GATEWAY** lets through only the identifiers listed (the dangerous ones are refused unless the operator unlocks them), checks the length and values of every payload against the specification, limits the rate per identifier and for the link, and asks a peer to prove it holds a key with an HMAC over a connection nonce and a counter. Every protection can be switched off, and the program lists each one that is off when it starts.
* **URTC-UPDATER** never acts on its own initiative: a selected project always needs an explicit confirmation, and a batch is sequential and confirmed. It clones into a staging directory, runs the project's non-versioning build check there, promotes with renames and keeps the previous checkout as a backup. The commit-signature policy is `warn` by default and `require` on request (`URTC_UPDATER_REQUIRE_SIGNED=1` or the settings file); with `require`, an unsigned candidate is refused before its manifest is read or anything is built. Signed commits are required by default (`signature_policy: require`), and so is a question before the build check (the project, commit, author, signature and the scripts the candidate changed are shown before it runs); without a window or a terminal the run fails closed unless the person answered in advance (`--yes`, `URTC_UPDATER_ASSUME_YES=1` or `assume_yes_without_asking`). `signature_policy: warn` and `confirm_before_build: false` go back to the previous behaviour.

### Repositories and CI

* **No secrets in git by policy.** `.gitignore` must exclude `.env` files and keep `.env.example` (checked by `ci_validate.py`); the FLASHER's local key file `urtc_config.json` is git-ignored.
* **Public/private boundary check** (`_doc_policy.py`) in every repository's CI: no private document names, no internal tracking codes.
* **Least privilege workflows.** The CI workflows that were read (URTC-UPDATER, URTC-DOCS) declare `contents: read`; the dashboard notifier declares no permissions and does nothing without its optional secret.
* **Pinned dependencies where it matters.** The profile workflow installs the updaters from a fixed revision, not from `main`.
* **Publication check** (`tools/publication_check.py` in this repository) for private keys, public IP addresses, personal e-mail addresses, tracked secret files, private document names and commits by someone other than the project's author, across all repositories next to it.

## What is a setting that is off, or only advice

* **`require_production_signature`** in URTC-FLASHER: off by default.
* **Every protection of URTC-GATEWAY** can be switched off from its configuration file or command line.
* **The release signing key** (`URTC_SIGNING_KEY_FILE`, `URTC_RELEASE=1`): the build supports it and refuses the development key in release mode, but the newest published release manifest says `signing_key_kind: dev` for both application images.
* **Requirements R1-R5** of the firmware threat model (an interlock independent of the microcontroller, a closed bus, no bridging, a private signing key, an emergency stop that cuts power): installation requirements, not features. Nothing in software enforces or even detects them.

## What is missing

| Gap | Why it matters | Where it is acknowledged |
|---|---|---|
| **No sender authentication or encryption on the bus** | Any node that can put a frame on the wires is "the master": it can start the laser (`0x160`), drive motors, weld, reset the board into its bootloader (`0x7F0` + magic), erase the saved state, or change the free tool configuration. | `CAN_THREAT_MODEL.TXT`: "a property of the bus, not a bug to be fixed in this firmware"; protection belongs in a gateway in front of the bus. |
| **Published firmware is signed with the public development key** | Anybody can produce an image that a board built with that bootloader key accepts. | `FIRMWARE_SIGNING.TXT` ("bench use only") and the release manifest. Fine while no board exists; a blocker for any deployment. |
| **Symmetric signature (HMAC-SHA256)** | The key lives in every bootloader; whoever can read one board's flash holds the signing key of every board built with it. No document or source traced for this repository mentions flash read-out protection **(inferred, not stated by the project)**. | `FIRMWARE_SIGNING.TXT`, section "Why not Ed25519 (yet)": planned for the first hardware bring-up; it needs a flash-layout change on the slave. |
| **A key lost, or a bootloader built with the other key** | Boards flashed with a development-key bootloader keep accepting only development-signed images; losing a release key means those boards can only be updated over SWD. | `FIRMWARE_SIGNING.TXT`. |
| **A digest and the file it protects come from the same place** | The `.sha256` and the manifest are release assets next to the image; they detect corruption and a mismatched download, not a replaced release. The real check is the bootloader's signature. | Implicit in `FIRMWARE_DISTRIBUTION.md`; stated here. |
| **The updater runs the build script of whatever it clones** | A compromised repository or account would make the updater execute attacker code after the user confirmed. The default signature policy only warns. | `signature.py`: "a compromised account or repository could push a commit that this tool would then build and run". |
| **No hardware E-stop in firmware** | A "stop" frame is not an emergency stop; the laser line PB6 is software controlled. | `CAN_THREAT_MODEL.TXT` R1, R5: an installation requirement. |
| **WEB-STUDIO transport only tried against a model** | The end-to-end checks drive the page in a real Chromium through a model of the adapter and the board, never a real adapter; behaviour that could send the wrong frame on a real bus is covered by those checks and by review. | README of URTC-WEB-STUDIO. |
| **Copies of the shared protocol code** | A fix is made once in URTC-COMMON and has to reach each copy; a lock file makes the CI of a repository fail when its copy fell behind or was edited, but a repository can still stay on an older copy until its refresh. | `CAN_PROTOCOL_DUPLICATION.md`. |
| **Shared CI checks are copies** | A rule changed in the SDK reaches a repository only when its sync script runs. | `INTERFACES.md`. |

## What a reader should conclude

The firmware and the tools are written to survive accidents (corrupted frames, lost power during an update, an operator's wrong click) and say clearly that they do not survive a hostile node on the bus. The one place that stops a hostile node, the signature check of the bootloader, is only as strong as the key, and the key published today is the public development one. None of this has been exercised on a real board.
