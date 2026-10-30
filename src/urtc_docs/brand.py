# =============================================================================
# URTC-DOCS - src/urtc_docs/brand.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""The banner, the icon and the map of the ecosystem of this repository, in the look of URTC.

The look is the one of the URTC banners: a near-black gradient, thin amber
circuit traces, a glowing line emblem, cyan accents and bold letter-spaced
titles. The map shows the repositories and the few links that their documents
state; it carries no counts and no versions, so it cannot go stale.
"""
from __future__ import annotations

import html

AMBER = "#FFB020"
CYAN = "#00E5FF"
GREEN = "#00FF66"
BG_FROM, BG_TO = "#07090C", "#12161C"
TAGS = ("ARCHITECTURE", "INTERFACES", "CAN", "SECURITY", "CATALOG", "PYTHON")

WIDTH, BOX_W, BOX_H = 1200, 290, 78
# repository -> (column centre, row, what it is); rows: 0 boards, 1 bus, 2 host tools, 3 shared protocol library, 4 operations
NODES: dict[str, tuple[int, int, str]] = {
    "URTC": (200, 0, "tool-head board firmware"),
    "URTC-SMART-RACK": (600, 0, "rack firmware, no board yet"),
    "URTC-VISION-TOOL": (1000, 0, "inspection head, no board yet"),
    "URTC-FLASHER": (200, 2, "flash over CAN or SWD"),
    "URTC-TESTER": (600, 2, "live bus tester"),
    "URTC-WEB-STUDIO": (1000, 2, "browser flasher and tester"),
    "URTC-COMMON": (600, 3, "the CAN protocol as data"),
    "URTC-GATEWAY": (1000, 3, "filters the frames to the bus"),
    "URTC-UPDATER": (350, 4, "reads the manifests"),
    "URTC-DEVTOOLS": (600, 4, "the shared tools, versioned"),
    "URTC-DOCS": (850, 4, "this repository"),
}
SOLID_ON_BUS = ("URTC", "URTC-FLASHER", "URTC-TESTER", "URTC-WEB-STUDIO")
DASHED_ON_BUS = ("URTC-SMART-RACK", "URTC-VISION-TOOL")
BUS_ROW = 1
TOP, STEP = 110, 118


def defs() -> str:
    return (
        f'<defs><linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%"><stop stop-color="{BG_FROM}"/><stop offset="1" stop-color="{BG_TO}"/></linearGradient>'
        '<filter id="g"><feGaussianBlur stdDeviation="4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>'
    )


def emblem(stroke: str = AMBER, accent: str = CYAN, width: float = 4) -> str:
    """A tool-changer head with three interchangeable heads, in a box of about 140 by 200 around the origin."""
    return (
        f'<g stroke="{stroke}" stroke-width="{width}" fill="none" stroke-linecap="round" stroke-linejoin="round">'
        '<circle r="34"/>'
        f'<circle r="10" fill="{stroke}" stroke="none"/>'
        f'<path d="M0,-34 V-74 M-24,20 L-52,58 M24,20 L52,58" stroke="{accent}" stroke-width="{width * 0.85}"/>'
        '<rect x="-16" y="-98" width="32" height="24" rx="4"/>'
        '<circle cx="-52" cy="66" r="12"/><circle cx="52" cy="66" r="12"/></g>'
    )


def book(stroke: str = AMBER, width: float = 4) -> str:
    """An open book, in a box of about 120 by 90 around the origin."""
    return (
        f'<path d="M-62,-34 Q-30,-46 0,-30 Q30,-46 62,-34 V34 Q30,22 0,38 Q-30,22 -62,34 Z" fill="none" stroke="{stroke}" stroke-width="{width}" stroke-linejoin="round"/>'
        f'<path d="M0,-30 V38" stroke="{stroke}" stroke-width="{width / 2}" opacity=".7"/>'
        f'<path d="M-46,-16 Q-30,-22 -14,-14 M-46,0 Q-30,-6 -14,2 M14,-14 Q30,-22 46,-16 M14,2 Q30,-6 46,0" fill="none" stroke="{stroke}" stroke-width="2.4" opacity=".6"/>'
    )


def banner(name: str = "URTC-DOCS", tagline: str = "ARCHITECTURE, INTERFACES & CAN PROTOCOL MAP") -> str:
    name, tagline = html.escape(name), html.escape(tagline)
    tag_xs = [105 + index * 150 for index in range(len(TAGS))]
    tags = "".join(f'<text x="{x}" y="360">#{html.escape(tag)}</text>' for x, tag in zip(tag_xs, TAGS))
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 400" role="img" aria-labelledby="title desc">
  <title id="title">{name}</title><desc id="desc">{name} | URTC ecosystem project banner</desc>
  {defs()}
  <rect width="1200" height="400" fill="url(#bg)"/><g fill="none" stroke="{AMBER}" stroke-width="1" opacity=".25"><path d="M0 100H200L250 150H600"/><path d="M1200 300H1000L950 250H600"/></g>
  <g transform="translate(205 185) scale(.9)" filter="url(#g)">{book()}</g>
  <g transform="translate(990 175) scale(.8)" filter="url(#g)" opacity=".9">{emblem()}</g>
  <text x="360" y="136" font-family="Arial,sans-serif" font-size="50" font-weight="bold" fill="#FFF" letter-spacing="8">URTC</text><text x="364" y="181" font-family="Arial,sans-serif" font-size="17" fill="{AMBER}" letter-spacing="4">UNIVERSAL ROBOT TOOL CONTROLLER</text><text x="360" y="246" font-family="Arial,sans-serif" font-size="29" font-weight="bold" fill="#FFF">{name}</text><text x="362" y="282" font-family="Arial,sans-serif" font-size="15" fill="{CYAN}" opacity=".85" letter-spacing="3">{tagline}</text>
  <g font-family="monospace" font-size="12" fill="{AMBER}" opacity=".7">{tags}</g>
</svg>
"""


def icon() -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="32" height="32" role="img" aria-labelledby="title">
  <title id="title">URTC-DOCS</title>
  <defs><linearGradient id="bgIcon" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#0A0D12"/><stop offset="50%" stop-color="#121720"/><stop offset="100%" stop-color="{BG_FROM}"/></linearGradient></defs>
  <rect width="32" height="32" rx="4" fill="url(#bgIcon)"/>
  <g transform="translate(16 16) scale(0.2)">{book(AMBER, 9)}</g>
</svg>
"""


def _position(row: int) -> float:
    return TOP + row * STEP


def ecosystem_map(nodes: dict[str, tuple[int, int, str]] | None = None) -> str:
    nodes = nodes or NODES
    rows = max(row for _, row, _ in nodes.values()) + 1
    last_row = rows - 1
    height = _position(rows) + 10
    bus_y = _position(BUS_ROW) + BOX_H / 2
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {height}" role="img" aria-labelledby="title desc">',
        '  <title id="title">URTC</title><desc id="desc">The repositories of URTC, the CAN bus that joins the boards and the host tools, and the links that their documents state</desc>',
        f"  {defs()}",
        f'  <rect width="{WIDTH}" height="{height}" fill="url(#bg)"/>',
        '  <text x="600" y="46" text-anchor="middle" font-family="Arial,sans-serif" font-size="26" font-weight="bold" fill="#FFF" letter-spacing="6">URTC ECOSYSTEM</text>',
        f'  <path d="M60 {bus_y} H1140" stroke="{AMBER}" stroke-width="3" opacity=".85"/>',
        f'  <text x="400" y="{bus_y - 10}" text-anchor="middle" font-family="monospace" font-size="13" fill="{AMBER}">CAN bus, 500 kbit/s: URTC/docs/CANBUS.TXT</text>',
        f'  <text x="800" y="{bus_y + 24}" text-anchor="middle" font-family="monospace" font-size="12" fill="{CYAN}" opacity=".8">via a USB-CAN adapter (SLCAN / SocketCAN)</text>',
    ]
    for name, (x, row, _) in nodes.items():
        top = _position(row)
        if name in SOLID_ON_BUS or name in DASHED_ON_BUS:
            dashed = ' stroke-dasharray="5 6"' if name in DASHED_ON_BUS else ""
            y1 = top + BOX_H if row < BUS_ROW else top
            parts.append(f'  <path d="M{x} {y1} V{bus_y}" stroke="{CYAN}" stroke-width="1.8" opacity=".6"{dashed}/><circle cx="{x}" cy="{bus_y}" r="4" fill="{AMBER}"/>')
    operations = sorted((x, name) for name, (x, row, _) in nodes.items() if row == last_row)
    if len(operations) == 2:
        y = _position(last_row) + BOX_H / 2
        parts.append(f'  <path d="M{operations[0][0] + BOX_W / 2} {y} H{operations[1][0] - BOX_W / 2}" stroke="{GREEN}" stroke-width="1.2" stroke-dasharray="4 6" opacity=".5"/>')
    for name, (x, row, sub) in nodes.items():
        top = _position(row)
        accent = AMBER if name == "URTC" else CYAN
        size = 15 if len(name) > 15 else 17
        parts.append(
            f'  <g transform="translate({x - BOX_W / 2} {top})"><rect width="{BOX_W}" height="{BOX_H}" rx="12" fill="#161208" stroke="{accent}" stroke-width="1.4" opacity=".95"/>'
            f'<text x="{BOX_W / 2}" y="34" text-anchor="middle" font-family="Arial,sans-serif" font-size="{size}" font-weight="bold" fill="#FFF">{html.escape(name)}</text>'
            f'<text x="{BOX_W / 2}" y="58" text-anchor="middle" font-family="monospace" font-size="12" fill="{accent}" opacity=".85">{html.escape(sub)}</text></g>'
        )
    parts.append(
        f'  <text x="600" y="{height - 14}" text-anchor="middle" font-family="monospace" font-size="12" fill="{GREEN}" opacity=".7">'
        "dashed to the bus: documented for it, but no board exists yet  ·  green: URTC-UPDATER reads the manifests that URTC-DOCS tabulates</text>"
    )
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def outputs() -> dict[str, str]:
    """Published path (relative to the repository) -> content."""
    return {
        "images/URTC_ECOSYSTEM.svg": ecosystem_map(),
        "brand/URTC_DOCS_ICON.svg": icon(),
    }
