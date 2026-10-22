# =============================================================================
# URTC-DOCS - src/urtc_docs/descriptions.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""One sober sentence per repository, for the generated project catalogue.

Each sentence says what the repository's own manifest and README say it does,
without the claims that only hardware could prove. A repository missing from
this table still appears in the catalogue (with the start of the notes of its
manifest) and the structure check of the nightly run reports it.
"""
from __future__ import annotations

DESCRIPTIONS: dict[str, str] = {
    "URTC": "Firmware of the tool-head board (STM32F303, 25 tool profiles, CAN bootloader, expansion slave) and the CAN protocol reference; no populated board exists yet.",
    "URTC-COMMON": "The CAN protocol as data: a specification with generated C, TypeScript and Python code, conformance vectors and the Python transports; nothing uses it yet.",
    "URTC-DOCS": "Architecture, interfaces, security baseline, capability matrix and generated project catalogue of the ecosystem, plus the tools that compare all repositories.",
    "URTC-FLASHER": "Desktop tool that updates the board firmware over CAN (bootloader protocol, signed images) or over SWD/JTAG; tested against a simulated bootloader only.",
    "URTC-GATEWAY": "Gateway in front of the CAN bus: the identifiers a host may send (made from the specification), a payload check, a rate limit and a session key, each one switchable; tested on the host only.",
    "URTC-SMART-RACK": "Hardware-independent C logic and rack command protocol for a tool rack with pre-heating and lifecycle tracking; no board exists yet.",
    "URTC-TESTER": "Desktop live CAN-bus tester that shows the controls and telemetry of the tool profile a board reports; checked against fake transports only.",
    "URTC-UPDATER": "Finds the ecosystem repositories on a machine from their manifests and installs or updates them after an explicit confirmation.",
    "URTC-VISION-TOOL": "Sensor-frame protocol in C and a Python thermal/RGB companion for an inspection tool head; no board or camera has been used yet.",
    "URTC-WEB-STUDIO": "Browser app that flashes and tests the board over Web Serial and SLCAN; the pure logic is tested, the transport and screens are not.",
}
