<!--
=============================================================================
URTC-DOCS - The first vertical slice
Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
CC BY-SA 4.0 - see LICENSE.md
=============================================================================
-->

# First vertical slice

The smallest path from a published firmware release to a finished update sequence that exists today and that anybody can reproduce from clean checkouts, with no board and no adapter. It proves that **the pieces agree with each other as software**: the release assets, the manifests, the signature fields, the image checks and the bootloader protocol as the flasher understands it. It does not prove that a real bootloader accepts the sequence, and it says plainly where the path stops.

## The path

1. **URTC** builds four components and publishes them as the assets of a GitHub release (`URTC_MAIN_FIRMWARE_v<ver>.bin` with its `.sha256` and `.bin.manifest.json`, the same for the bootloader and the expansion slave, and the index `firmware_manifest.json`). The application manifests carry `hmac_sha256`, `signing_key_kind` and `signing_key_id`.
2. **URTC-FLASHER** `tools/sync_firmware.py` (no argument) downloads the assets of the newest release into a temporary folder, runs the digest and signature checks, and only then replaces its `firmware/` folder.
3. `urtc_flasher.py --cli --transport mock --file <image>` checks the image (it exists, fits the 112 KB slot, starts with a plausible Cortex-M vector table, matches its published sha256), takes the signature from the manifest, and plays the complete update against `MockCAN`, the in-memory bootloader: `0x7F0`, `0x7F1`, four `0x7F7` chunks, every `0x7F2` page with its `0x7F3` acknowledgement, `0x7F4`, and the final status.
4. `--mock-fail 0x03` makes the simulated bootloader report a signature mismatch after a complete transfer, which exercises the failure path and the exit status.

## How to run it

```bash
git clone https://github.com/JuanenRac/URTC-FLASHER.git && cd URTC-FLASHER
python -m venv .venv && . .venv/bin/activate      # .venv\Scripts\activate on Windows
pip install pyserial                              # needed even for the mock transport on a PC with no SocketCAN
python tools/sync_firmware.py                     # newest release into firmware/
python urtc_flasher.py --cli --transport mock --file firmware/URTC_MAIN_FIRMWARE_v<ver>.bin
python urtc_flasher.py --cli --transport mock --file firmware/URTC_MAIN_FIRMWARE_v<ver>.bin --mock-fail 0x03
```

Replace `<ver>` with the version that `sync_firmware.py` printed. The folder that ships in the repository holds an older release than the newest one at the time of reading, so the sync is worth running.

## What was observed

The sequence above was run for this document in a fresh clone, with the newest release and then with the older bundled image. Each run ended with `SUCCESS: firmware update complete.` and the second command with `FAILED: Bootloader reported failure: Verify FAILED - main slot untouched - HMAC signature mismatch`. The run printed `Using the signature published in the manifest (key: dev)` and a note that the image is signed with the public development key. About 36 pages are transferred; the whole simulated transfer took about twenty seconds because the simulator paces the pages.

## Where the path stops

* **The bootloader is simulated.** `MockCAN` was written from `docs/CANBUS.TXT`. The flasher's own README records two defects that passed its tests because the simulator was more forgiving than the real bootloader, so a green run is a statement about the flasher, not about the bootloader.
* **No bus, no adapter, no board.** The SLCAN and SocketCAN transports are not part of this path.
* **The signature is not verified by anything real.** The simulator reports what it is told to; only the bootloader of a board verifies HMAC-SHA256. The image is signed with the public development key.
* **The other tools are not in the path.** URTC-TESTER and URTC-WEB-STUDIO read the same assets and speak the same protocol, but each has its own tests; running the browser app's `npm test` or the tester's `python -m pytest` is a separate check, not a continuation of this one.
* **The expansion slave** is a second relay of the same sequence (`0x210`-`0x219`); the command-line mode of the flasher in this path updates the main board.

## What the next slice would add

The smallest addition that would make the path mean something on hardware is one populated board on a bench, a USB-CAN adapter with SLCAN firmware, a bootloader built with a private key, and the same command with `--transport serial` instead of `mock`, followed by `0x7F8` to read the version back. None of those exists in the repositories today.
