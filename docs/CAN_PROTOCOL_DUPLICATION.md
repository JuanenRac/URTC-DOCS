<!--
=============================================================================
URTC-DOCS - Study note: the CAN protocol is implemented three times
Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
CC BY-SA 4.0 - see LICENSE.md
=============================================================================
-->

# The CAN protocol is implemented three times

A study note, not a plan. Whether to build what is described under "What a shared specification would hold" is a decision that belongs to the owner of the ecosystem.

**Status.** A first version of items 1, 3, 4 and 5 now exists in its own repository, [URTC-COMMON](https://github.com/JuanenRac/URTC-COMMON): a machine-readable frame table (`spec/can_protocol.json`, with a JSON Schema), the SLCAN subset, the conformance vectors copied there and extended, and a C header, a TypeScript module and a Python module generated from the table, with a check that fails when one is out of date. A test there compares the table with the firmware, the three tools and the identifiers listed in the prose, when they are checked out next to it. Its first reading also found two identifiers, `0x1A8` and `0x1A9` (read-back of the fault recorder), that the firmware implements and that neither the prose nor any tool describes. Item 2 (the sequences as state machines) and the rules for change (item 6) are only started, no tool or firmware imports URTC-COMMON yet, and the questions for the owner below are unchanged. The text of this note describes the situation as it was read before that repository existed.

## The situation

The wire protocol of the tool head (identifiers, DLC, payload layouts, big-endian fields, magic payloads, telemetry periods, the bootloader sequence and the SLCAN framing the host tools use to carry it) is specified in one place, as prose: `URTC/docs/CANBUS.TXT` (about 1,500 lines). Three repositories read that prose and each keep their own implementation of the part they need:

| Implementation | Files | What it covers |
|---|---|---|
| **URTC-FLASHER** (Python) | `flasher_config.py` (identifier constants, magic values, timing), `flasher_protocol.py` (the update, read-back, version and slave sequences), `flasher_transports.py` (`SLCAN`, `SocketCAN`, `PythonCAN`, `MockCAN`) | Bootloader protocol, version query with the patch number, saved-state erase, expansion type, free tool configuration, serial number, MLX variant, slave relay `0x210`-`0x219`. |
| **URTC-TESTER** (Python) | `tester_config.py` (identifier constants), `advanced_protocol.py` (pure payload encoders and decoders), `tester_transports.py` (`SLCAN`, `SocketCAN`) | The per-tool runtime commands and telemetry, global lighting and status, expansion passthrough, saved state, thermal camera. |
| **URTC-WEB-STUDIO** (TypeScript) | `src/lib/canIds.ts`, `src/lib/flasher.ts`, `src/lib/slcan.ts` plus the Web Serial hook `src/hooks/useSerialCanBus.ts` | Both of the above in one application, with its own SLCAN reader. |

The firmware is a fourth reader of the same prose, in C. The two bootloaders and the application are checked against each other by the firmware's own host tests, but not against the three host implementations.

## What a scan of the three found (as read for this version)

These figures come from a text scan of `CAN_ID_*` constants and of the `ID:` headers of `CANBUS.TXT`; they are a sketch of the situation, not a measurement of correctness.

* The reference has 85 `ID:` headers. The three implementations define 38 (FLASHER), 55 (TESTER) and 82 (WEB-STUDIO) distinct identifiers. Nine identifiers are defined by all three; 29 (the bootloader and slave range) by FLASHER and WEB-STUDIO only; TESTER and WEB-STUDIO share 44 that FLASHER does not carry.
* **Two identifiers of the reference, `0x220` and `0x221` (generic read and write of a slave application register), are defined by none of the three.**
* **`0x243`** (basic-mode reading of the functional testing head) is defined by TESTER and WEB-STUDIO and documented in the reference only inside prose and in the summary list at the end, not under an `ID:` header. A scan that trusts the headers misses it.
* **The magic payloads are written out in several places.** The bootloader-entry value appears as a literal in two places of `flasher_protocol.py` (main board and slave) and as a named constant in WEB-STUDIO; the downgrade value is a literal in FLASHER and a named constant in WEB-STUDIO; the saved-state erase value is a named constant in all three. At the time of reading the values agree.
* **The transport copies have diverged.** TESTER's README says its SLCAN and SocketCAN classes "are identical" to the flasher's. A comparison of the class bodies shows they are not: TESTER serialises writes with a lock and reports a failed serial write as a typed error; FLASHER's copy has no write lock; FLASHER closes the socket after a failed bind and TESTER's copy does not; TESTER clears its application-level receive buffer on open and FLASHER's does not. Each is a reasonable local fix. None reached the other copy.
* **The reference disagrees with itself in a detail.** The description of `0x110` still speaks of "the 12 tool profiles" while the same document, the manifest and the README define 25.
* **Coverage differs by design.** FLASHER has `python-can` and a simulated bootloader (`MockCAN`) that the others lack; WEB-STUDIO parses only standard `t` frames (and has a test that `T`, `r` and `R` are rejected); TESTER has no bootloader frames at all.

## What it costs

* A change of a frame layout or of a safety limit has to be made in the firmware, in up to three host implementations and in the prose, with nothing to say that one of them was missed.
* A simulator written from the prose by the same person who wrote the flasher shares the flasher's reading of it. The two defects that the flasher's README says its simulator hid are the proof that "agrees with the simulator" and "agrees with the bootloader" are different statements.
* A reader cannot tell which implementation is right when two disagree. Today the answer is "the prose, as interpreted by whoever reads it".

## What a shared specification would hold

Nothing of this exists. It is the description of a possible next step so that the decision can be taken with the content in view.

**1. A machine-readable frame table**, one record per identifier:

* identifier, direction (master to head, head to master, or both with the rule that decides), the tool or tools for which it is valid, the DLC (exact, minimum, maximum);
* each field: byte offset, width, signedness, endianness, unit, valid range, enumerated values, reserved bits, and what a receiver does with a value out of range (clamp, ignore, reject, silently treat as unknown);
* gates: active-tool dependence, whether a critical error blocks it, whether the board answers while in the bootloader, whether a magic payload is required and which;
* timing: telemetry period, watchdog timeout, acknowledgement and page timeouts, the grace window of the version query;
* the response frame(s) of a query, including the frames that arrive in a fixed order (the four-frame answers) and the legacy-length rules (an older board answers with fewer bytes; a missing byte means "not reported", not zero).

**2. The sequences as small state machines**: bootloader update (start, chunks, pages and acknowledgements, partial last page, end, verify, status codes and reasons), read-back with its page pacing, the version query with the `0x7E9` grace window and the legacy fallback, the slave relay, and the one-shot downgrade authorisation.

**3. The carrier rules**: the SLCAN subset that is relied on (standard data frames only, hex case, terminator, the `Sx`, `O` and `L` commands and their codes, the 8-byte limit, what is done with an adapter's status characters), and the SocketCAN and python-can mappings.

**4. Conformance vectors**, language-neutral files that every implementation runs:

* *Encode* vectors: a command and its parameters, and the exact frames expected.
* *Decode* vectors: frames, and the decoded fields expected, including the short legacy forms.
* *Negative* vectors: a DLC too short or too long, a value out of range, a wrong magic payload, an identifier above `0x7FF`, a frame that must be ignored in the current state.
* *Sequence* vectors: the full frame trace of a successful update, of each verify-failure reason, of a read-back whose size is not a multiple of 8, of an image whose size is not a whole number of pages, of a version query against a board with and without the patch frame.
* *SLCAN line* vectors: well-formed `t` lines, the rejected `T`, `r` and `R`, truncated and non-hex payloads, optional timestamp suffixes.

A first, small set of these vectors now exists: `tests/fixtures/can_conformance_vectors.json` (identifier table of the 82 identifiers that at least two clients define, the four magic payloads, SLCAN encode and decode lines, the `0x111` quick-state answer, the version query with and without the `0x7E9` patch frame, the end-of-update minor field and the version order). This repository only checks that the file is coherent; the Flasher, the Tester and the Web Studio each keep a committed copy and run their own reader against it, so there is no run-time dependency between the repositories. What the first comparison showed:

* The identifiers and magic payloads that the clients share all agree in value; only the constant names differ.
* The serial readers of the Flasher and the Tester accepted a signed, `0x`-prefixed or underscore-separated field as a number (a property of Python's `int(..., 16)`), and the Flasher's reader handed an extended 29-bit frame on as if it were a standard one, which the Tester's reader and the SocketCAN and python-can transports of both already discarded. Both readers now require real hexadecimal digits, and the Flasher's discards extended frames.
* An adapter timestamp after the payload is ignored by the Web Studio and makes the Flasher and the Tester drop the line. The protocol never enables timestamps, so the vector marks this as a tolerated difference instead of asserting one behaviour.
* The Web Studio builds its per-tool command frames inside its React components, so those cannot be compared with the Tester's encoders without first moving them into plain functions.

**5. Generated or checked artefacts**: a C header for the firmware, Python constants for the two desktop tools, TypeScript constants for the browser app, all produced from the table (or at least checked against it), plus a drift check like the scan above that fails when an identifier exists in one place and not in the table.

**6. Rules for change**: a version of the specification, a rule for additive changes (new identifiers, trailing bytes) that older receivers ignore, and the host contract style already used for the patch number ("a board that predates it never sends it; a host that does not see it within a grace window falls back").

## Questions for the owner

1. Is the prose to stay the reference, with vectors extracted from it, or should the table become the reference and the prose be generated from it?
2. Where should it live: in `URTC` (next to the firmware, which already owns the prose), in this repository, or in its own repository? A constraint to respect: changes to `URTC` must not rebuild or alter the committed or published binaries.
3. Should the firmware's host tests consume the same vectors, so that the C side is a fourth implementation under the same check?
4. Is the simulator (`MockCAN`) to be regenerated from the sequences, so that it stops being a second reading of the prose?
5. Is a drift check that only compares identifier sets, without any vector, worth having first as the cheapest step?
6. Should `0x220` and `0x221` be given a host implementation, or marked as firmware-only in the reference?

## Sources

`URTC/docs/CANBUS.TXT`, `URTC-FLASHER` (`flasher_config.py`, `flasher_protocol.py`, `flasher_transports.py`, README), `URTC-TESTER` (`tester_config.py`, `advanced_protocol.py`, `tester_transports.py`, README), `URTC-WEB-STUDIO` (`src/lib/canIds.ts`, `src/lib/flasher.ts`, `src/lib/slcan.ts`, `src/hooks/useSerialCanBus.ts`, README). The numbers above change with every release of those repositories.
