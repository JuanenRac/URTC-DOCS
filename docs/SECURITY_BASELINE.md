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
* **Bootloader.** Updates go to a backup slot and are copied only after size, CRC32, HardwareID and, on the main board, an Ed25519 record verified against a table of public keys have matched (the main bootloader holds no secret; the signed rollback counter is kept in its metadata); any mismatch leaves the main slot untouched and the bootloader never jumps into an image that failed a check. Anti-rollback compares major, minor and (when both carry one) patch; a downgrade needs a one-shot authorisation that must be sent again for each attempt and the image must still be correctly signed. The expansion slave bootloader holds no key: the main board verifies the Ed25519 record of the slave image and the slave checks CRC32, a plain SHA-256 and that the main board confirmed that image in that update session, so the slave trusts the main board over the link bus.
* **Host tests with sanitizers:** 38 suites compile the firmware sources against a fake HAL and run under the address and undefined-behaviour sanitizers and `gcc -fanalyzer`, with a coverage floor; they cover the version wire format, the dispatch routing, the thermal guard, the counters, the handlers of the tools and both bootloaders. The firmware is also held to the shared vectors of URTC-COMMON.
* **The bootloader answers a read-back or a downgrade authorisation only in the session the application started** (the application leaves a mark in a backup register of the RTC block when it accepts `0x7F0`; the bootloader reads it once and clears it).

### Host tools

* **Encoders refuse instead of clamping** (URTC-TESTER, `advanced_protocol.py`), and the transports of FLASHER and TESTER refuse an identifier above `0x7FF` or a payload above 8 bytes before sending.
* **URTC-FLASHER** refuses an image whose sha256 differs from its published manifest before any bus traffic; refuses an image built for the other board (`component` and `hardware_id` are compared before the first frame); sends only the signature record published next to the image (the `.imgsig` file) and never signs; shows a red warning for an image signed with the public development key and, with `require_production_signature` set, refuses it; says what it replaces (installed -> new) and warns about a downgrade; writes an update report with its own digest; keeps the deadline arithmetic on the monotonic clock; keeps worker threads away from the window; restricts downloads to GitHub release assets and the asset hosts it redirects to, checking the host before the request and again on the final address, and compares the byte count with the announced size.
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

## Who verifies what, and with which key

Written from the key files of URTC (`keys/image_trust.json` and `keys/registry.json`); `tools/check_claims.py` fails when it is behind them.

<!-- signing-table:begin (written from data/signing_facts.json; do not edit) -->
| Key | Algorithm | Public value (start) | Signs | Checked by |
|---|---|---|---|---|
| `urtc-release-ed25519` | Ed25519 | `4020c46d76c8ebac` | Every asset of an official release | URTC-FLASHER, URTC-WEB-STUDIO and the publishing tool, before they trust a download |
| `urtc-main-bootloader-hmac-development` | HMAC-SHA256 | `2526cc3e9011ec7c` | Nothing any current bootloader checks | Only the main bootloader of the earlier generation |
| `urtc-image-signing-release-current` | Ed25519 | `80344f1a557fac5d` | The application images of official builds | The main bootloader of an official build |
| `urtc-image-signing-release-next` | Ed25519 | `ac856598a0ac8e45` | Nothing yet: reserved for the next image-signing key | The main bootloader of an official build, which already trusts it |
| `urtc-image-signing-development` | Ed25519 | `81f29be04dfa58f3` | Bench images; its seed is published, so it proves nothing about who made one | The main bootloader of a bench build |
| (no key) | SHA-256 | - | The image of the expansion slave | The slave bootloader, which also asks that the main board confirmed that exact image |
<!-- signing-table:end -->

## What is a setting that is off, or only advice

* **`sign_evidence`** in URTC-TESTER and URTC-FLASHER (and in the settings of URTC-UPDATER for its export): off by default; anything other than the plain value `true` keeps it off. When it is on the evidence records carry an Ed25519 signature of a key that stays on the computer (`record_key_file`, never printed); if the key cannot be used nothing is written. The programs that read records say "signed by <alias>" or "unknown key" with a list of public keys (`trusted_keys`) and always show a signature that fails.
* **`require_production_signature`** in URTC-FLASHER: off by default.
* **Every protection of URTC-GATEWAY** can be switched off from its configuration file or command line.
* **The release signing key** (`URTC_SIGNING_KEY_FILE`, `URTC_RELEASE=1`): official releases are signed with the release image-signing key (their manifests say `signing_key_kind: release` and carry an Ed25519 record, `<image>.imgsig`), while bench builds trust a public development key (`signing_key_kind: dev`) whose seed is published. The release table of the bootloader holds the current key and a reserved next key; its private halves stay outside every repository (`keys/registry.json`, `keys/image_trust.json`).
* **Requirements R1-R5** of the firmware threat model (an interlock independent of the microcontroller, a closed bus, no bridging, a private signing key, an emergency stop that cuts power): installation requirements, not features. Nothing in software enforces or even detects them.

## What is missing

| Gap | Why it matters | Where it is acknowledged |
|---|---|---|
| **No sender authentication or encryption on the bus** | Any node that can put a frame on the wires is "the master": it can start the laser (`0x160`), drive motors, weld, reset the board into its bootloader (`0x7F0` + magic), erase the saved state, or change the free tool configuration. | `CAN_THREAT_MODEL.TXT`: "a property of the bus, not a bug to be fixed in this firmware"; protection belongs in a gateway in front of the bus. |
| **A bench bootloader trusts a public development key** | Anybody can produce an image that a bootloader built with the development trust table accepts. Official releases are signed with the release image-signing key and carry the `.imgsig` record, but a board that was flashed with a bench bootloader keeps trusting the development key until it is reflashed over SWD. | `FIRMWARE_SIGNING.TXT` ("bench use only") and the release manifest (`signing_key_kind`). Fine while no board exists; a blocker for any deployment. |
| **The expansion slave does not verify a signature itself** | The slave bootloader did not have room for an Ed25519 verifier (about 7 KB short), so the main board verifies the record of the slave image and the slave checks a plain SHA-256 and the main board's confirmation. A node that can impersonate the main board on the link bus can make the slave install an image. The main bootloader has no symmetric key to read out of a board's flash: its table holds public keys only. | `FIRMWARE_SIGNING.TXT` (the expansion slave) and `SLAVE_BOOT_CONFIRMATION.md`. |
| **A key lost, or a bootloader built with the other table** | A board flashed with a bench bootloader keeps accepting only images signed with the development key; if the image-signing key is lost, the reserved next key of the table is the way forward, and a board whose table holds neither can only be updated over SWD. There is no remote command that changes or revokes a key. | `FIRMWARE_SIGNING.TXT`, section 6. |
| **A digest and the file it protects come from the same place** | The `.sha256` and the manifest are release assets next to the image; they detect corruption and a mismatched download, not a replaced release. The real check is the bootloader's signature. | Implicit in `FIRMWARE_DISTRIBUTION.md`; stated here. |
| **The updater runs the build script of whatever it clones** | A compromised repository or account would make the updater execute attacker code after the user confirmed. The default signature policy only warns. | `signature.py`: "a compromised account or repository could push a commit that this tool would then build and run". |
| **No hardware E-stop in firmware** | A "stop" frame is not an emergency stop; the laser line PB6 is software controlled. | `CAN_THREAT_MODEL.TXT` R1, R5: an installation requirement. |
| **WEB-STUDIO transport only tried against a model** | The end-to-end checks drive the page in a real Chromium through a model of the adapter and the board, never a real adapter; behaviour that could send the wrong frame on a real bus is covered by those checks and by review. | README of URTC-WEB-STUDIO. |
| **Copies of the shared protocol code** | A fix is made once in URTC-COMMON and has to reach each copy; a lock file makes the CI of a repository fail when its copy fell behind or was edited, but a repository can still stay on an older copy until its refresh. | `CAN_PROTOCOL_DUPLICATION.md`. |
| **Shared CI checks are copies** | A rule changed in the SDK reaches a repository only when its sync script runs. | `INTERFACES.md`. |

## What a reader should conclude

The firmware and the tools are written to survive accidents (corrupted frames, lost power during an update, an operator's wrong click) and say clearly that they do not survive a hostile node on the bus. The one place that stops a hostile node, the signature check of the bootloader, is an Ed25519 check against a table of public keys: official releases are signed with a key that stays off every repository, and a bench build trusts a public development key that anybody can use. None of this has been exercised on a real board.
