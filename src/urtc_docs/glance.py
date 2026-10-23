# =============================================================================
# URTC-DOCS - src/urtc_docs/glance.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""The "At a glance" table of the README of every repository, in the eight languages.

Where the facts come from:

* the manifest of the repository (version, maturity, role, technologies, deployment target), so the
  table cannot say anything the manifest does not;
* data/glance.json of this documentation hub (test count when it is known, an optional target and the
  hardware statement, chosen from a closed vocabulary), so every claim about hardware is one of a few
  sentences that are translated once, here.

The section sits in README.md and in the seven translations right before the first "## " heading
that follows the honesty check. :func:`apply_to_text` inserts it when it is missing and rewrites it
in place when it is there (never a second copy); :func:`check_text` says what is missing, misplaced
or stale. Line endings (LF or CRLF) of the file are kept.

This file is shared, line by line, with the other documentation hub (HYDRA-UMC-DOCS).
"""
from __future__ import annotations

import json
import re
from pathlib import Path

# language code -> README file suffix
LANGUAGE_FILES: dict[str, str] = {
    "en": "README.md",
    "es": "README_spa.md",
    "de": "README_deu.md",
    "fr": "README_fra.md",
    "it": "README_ita.md",
    "ja": "README_jpn.md",
    "zh": "README_zho.md",
    "pt": "README_por.md",
}

MANIFEST_NAMES = ("hydra-umc.project.json", "urtc.project.json", "electro-hobby-3d.project.json")

HARDWARE_KEYS = ("not_applicable", "not_run", "simulated", "bench", "in_use")
TARGET_KEYS = ("cm5", "user_pc", "dev_server", "android", "ios", "wearos", "board", "browser")
DEFAULT_TARGET = {"cm5": "cm5", "user-pc": "user_pc", "dev-server": "dev_server", "wearable": "wearos"}
MAX_STACK_ITEMS = 5

LABELS: dict[str, dict[str, str]] = {
    "en": {"heading": "At a glance", "version": "Version", "maturity": "Maturity", "tests": "Tests", "stack": "Stack", "target": "Target", "hardware": "On real hardware"},
    "es": {"heading": "De un vistazo", "version": "Versión", "maturity": "Madurez", "tests": "Tests", "stack": "Tecnología", "target": "Destino", "hardware": "En hardware real"},
    "de": {"heading": "Auf einen Blick", "version": "Version", "maturity": "Reifegrad", "tests": "Tests", "stack": "Technik", "target": "Ziel", "hardware": "Auf echter Hardware"},
    "fr": {"heading": "En un coup d'œil", "version": "Version", "maturity": "Maturité", "tests": "Tests", "stack": "Technologie", "target": "Cible", "hardware": "Sur matériel réel"},
    "it": {"heading": "In breve", "version": "Versione", "maturity": "Maturità", "tests": "Test", "stack": "Tecnologia", "target": "Destinazione", "hardware": "Su hardware reale"},
    "ja": {"heading": "ひと目で", "version": "バージョン", "maturity": "成熟度", "tests": "テスト", "stack": "技術", "target": "対象", "hardware": "実機での確認"},
    "zh": {"heading": "速览", "version": "版本", "maturity": "成熟度", "tests": "测试", "stack": "技术栈", "target": "目标", "hardware": "真实硬件"},
    "pt": {"heading": "Num relance", "version": "Versão", "maturity": "Maturidade", "tests": "Testes", "stack": "Tecnologia", "target": "Destino", "hardware": "Em hardware real"},
}

MATURITY: dict[str, dict[str, str]] = {
    "en": {"scaffolding": "Scaffolding", "functional": "Functional", "established": "Established", "production": "Production"},
    "es": {"scaffolding": "Andamiaje", "functional": "Funcional", "established": "Establecido", "production": "En producción"},
    "de": {"scaffolding": "Gerüst", "functional": "Funktionsfähig", "established": "Etabliert", "production": "Im Betrieb"},
    "fr": {"scaffolding": "Ébauche", "functional": "Fonctionnel", "established": "Établi", "production": "En production"},
    "it": {"scaffolding": "Impalcatura", "functional": "Funzionale", "established": "Consolidato", "production": "In produzione"},
    "ja": {"scaffolding": "足場段階", "functional": "機能する", "established": "確立", "production": "本番運用"},
    "zh": {"scaffolding": "雏形", "functional": "可用", "established": "成熟", "production": "生产"},
    "pt": {"scaffolding": "Estrutura inicial", "functional": "Funcional", "established": "Estabelecido", "production": "Em produção"},
}

TARGETS: dict[str, dict[str, str]] = {
    "en": {
        "cm5": "The Raspberry Pi CM5 of a HYDRA-UMC cell",
        "user_pc": "The PC of the person using it",
        "dev_server": "A development server",
        "android": "An Android phone or tablet",
        "ios": "An iPhone or iPad",
        "wearos": "A Wear OS watch (paired with the phone)",
        "board": "A microcontroller board (the firmware); built on a PC",
        "browser": "A web browser on the user's PC",
    },
    "es": {
        "cm5": "La Raspberry Pi CM5 de una celda HYDRA-UMC",
        "user_pc": "El PC de quien lo usa",
        "dev_server": "Un servidor de desarrollo",
        "android": "Un teléfono o tableta Android",
        "ios": "Un iPhone o iPad",
        "wearos": "Un reloj Wear OS (emparejado con el teléfono)",
        "board": "Una placa con microcontrolador (el firmware); se compila en un PC",
        "browser": "Un navegador web en el PC del usuario",
    },
    "de": {
        "cm5": "Der Raspberry Pi CM5 einer HYDRA-UMC-Zelle",
        "user_pc": "Der PC der Person, die es benutzt",
        "dev_server": "Ein Entwicklungsserver",
        "android": "Ein Android-Telefon oder -Tablet",
        "ios": "Ein iPhone oder iPad",
        "wearos": "Eine Wear-OS-Uhr (mit dem Telefon gekoppelt)",
        "board": "Eine Mikrocontroller-Platine (die Firmware); wird auf einem PC gebaut",
        "browser": "Ein Webbrowser auf dem PC des Benutzers",
    },
    "fr": {
        "cm5": "Le Raspberry Pi CM5 d'une cellule HYDRA-UMC",
        "user_pc": "Le PC de la personne qui l'utilise",
        "dev_server": "Un serveur de développement",
        "android": "Un téléphone ou une tablette Android",
        "ios": "Un iPhone ou un iPad",
        "wearos": "Une montre Wear OS (appairée au téléphone)",
        "board": "Une carte à microcontrôleur (le firmware) ; compilé sur un PC",
        "browser": "Un navigateur web sur le PC de l'utilisateur",
    },
    "it": {
        "cm5": "Il Raspberry Pi CM5 di una cella HYDRA-UMC",
        "user_pc": "Il PC di chi lo usa",
        "dev_server": "Un server di sviluppo",
        "android": "Uno smartphone o tablet Android",
        "ios": "Un iPhone o iPad",
        "wearos": "Un orologio Wear OS (abbinato al telefono)",
        "board": "Una scheda con microcontrollore (il firmware); compilato su un PC",
        "browser": "Un browser web sul PC dell'utente",
    },
    "ja": {
        "cm5": "HYDRA-UMC セルの Raspberry Pi CM5",
        "user_pc": "利用者の PC",
        "dev_server": "開発用サーバー",
        "android": "Android のスマートフォンまたはタブレット",
        "ios": "iPhone または iPad",
        "wearos": "Wear OS ウォッチ（スマートフォンとペアリング）",
        "board": "マイコン基板（ファームウェア）。ビルドは PC で行います",
        "browser": "利用者の PC 上の Web ブラウザー",
    },
    "zh": {
        "cm5": "HYDRA-UMC 工作单元的 Raspberry Pi CM5",
        "user_pc": "使用者的电脑",
        "dev_server": "开发服务器",
        "android": "Android 手机或平板",
        "ios": "iPhone 或 iPad",
        "wearos": "Wear OS 手表（与手机配对）",
        "board": "微控制器板（固件）；在电脑上构建",
        "browser": "使用者电脑上的网页浏览器",
    },
    "pt": {
        "cm5": "O Raspberry Pi CM5 de uma célula HYDRA-UMC",
        "user_pc": "O PC de quem o usa",
        "dev_server": "Um servidor de desenvolvimento",
        "android": "Um telemóvel ou tablet Android",
        "ios": "Um iPhone ou iPad",
        "wearos": "Um relógio Wear OS (emparelhado com o telemóvel)",
        "board": "Uma placa com microcontrolador (o firmware); compila-se num PC",
        "browser": "Um navegador web no PC do utilizador",
    },
}

HARDWARE: dict[str, dict[str, str]] = {
    "en": {
        "not_applicable": "Not applicable: nothing here runs on hardware",
        "not_run": "Not yet: no run on real hardware is recorded for this version",
        "simulated": "Simulated only: tested against emulators, fakes or simulators; no run on real hardware is recorded for this version",
        "bench": "Run on a bench setup: the honesty check above says which parts ran on real hardware",
        "in_use": "In daily use on real hardware: the honesty check above says where",
    },
    "es": {
        "not_applicable": "No aplica: nada de esto se ejecuta en hardware",
        "not_run": "Todavía no: no consta ninguna ejecución en hardware real para esta versión",
        "simulated": "Solo simulado: probado con emuladores, dobles de prueba o simuladores; no consta ninguna ejecución en hardware real para esta versión",
        "bench": "Ejecutado en un banco de pruebas: la comprobación de honestidad de arriba dice qué partes funcionaron en hardware real",
        "in_use": "En uso diario en hardware real: la comprobación de honestidad de arriba dice dónde",
    },
    "de": {
        "not_applicable": "Nicht zutreffend: nichts hiervon läuft auf Hardware",
        "not_run": "Noch nicht: für diese Version ist kein Lauf auf echter Hardware vermerkt",
        "simulated": "Nur simuliert: gegen Emulatoren, Attrappen oder Simulatoren getestet; für diese Version ist kein Lauf auf echter Hardware vermerkt",
        "bench": "Auf einem Prüfstand gelaufen: die Ehrlichkeitsprüfung oben sagt, welche Teile auf echter Hardware liefen",
        "in_use": "Im täglichen Einsatz auf echter Hardware: die Ehrlichkeitsprüfung oben sagt, wo",
    },
    "fr": {
        "not_applicable": "Sans objet : rien ici ne s'exécute sur du matériel",
        "not_run": "Pas encore : aucune exécution sur du matériel réel n'est consignée pour cette version",
        "simulated": "Simulé seulement : testé avec des émulateurs, des doubles de test ou des simulateurs ; aucune exécution sur du matériel réel n'est consignée pour cette version",
        "bench": "Exécuté sur un banc d'essai : la vérification d'honnêteté ci-dessus indique quelles parties ont tourné sur du matériel réel",
        "in_use": "En usage quotidien sur du matériel réel : la vérification d'honnêteté ci-dessus indique où",
    },
    "it": {
        "not_applicable": "Non applicabile: nulla qui gira su hardware",
        "not_run": "Non ancora: per questa versione non risulta alcuna esecuzione su hardware reale",
        "simulated": "Solo simulato: provato con emulatori, test double o simulatori; per questa versione non risulta alcuna esecuzione su hardware reale",
        "bench": "Eseguito su un banco di prova: la verifica di onestà qui sopra indica quali parti hanno girato su hardware reale",
        "in_use": "In uso quotidiano su hardware reale: la verifica di onestà qui sopra indica dove",
    },
    "ja": {
        "not_applicable": "対象外：ここにあるものはハードウェア上では動きません",
        "not_run": "まだです：このバージョンについて実機での動作記録はありません",
        "simulated": "シミュレーションのみ：エミュレーター、模擬部品、シミュレーターで試験済み。このバージョンについて実機での動作記録はありません",
        "bench": "ベンチ環境で動作：上の正直さの確認に、どの部分が実機で動いたかが書かれています",
        "in_use": "実機で日常的に使用：上の正直さの確認に、どこで使っているかが書かれています",
    },
    "zh": {
        "not_applicable": "不适用：这里的内容不在硬件上运行",
        "not_run": "尚未：此版本没有在真实硬件上运行的记录",
        "simulated": "仅模拟：使用模拟器、替身或仿真测试；此版本没有在真实硬件上运行的记录",
        "bench": "已在试验台上运行：上面的诚实性检查说明了哪些部分在真实硬件上运行过",
        "in_use": "在真实硬件上日常使用：上面的诚实性检查说明了在哪里",
    },
    "pt": {
        "not_applicable": "Não aplicável: nada aqui corre em hardware",
        "not_run": "Ainda não: não há registo de execução em hardware real para esta versão",
        "simulated": "Só simulado: testado com emuladores, dublês de teste ou simuladores; não há registo de execução em hardware real para esta versão",
        "bench": "Executado numa bancada de ensaio: a verificação de honestidade acima diz que partes correram em hardware real",
        "in_use": "Em uso diário em hardware real: a verificação de honestidade acima diz onde",
    },
}

HEADING = re.compile(r"^## 📋 (.+?)\s*$")
ANY_H2 = re.compile(r"^## ")
FENCE = re.compile(r"^\s*(```|~~~)")
ALL_HEADINGS = {labels["heading"] for labels in LABELS.values()}


class GlanceError(Exception):
    """Something the table cannot be written from (unknown key, missing manifest, bad data file)."""


def load_manifest(repo: Path) -> dict:
    for name in MANIFEST_NAMES:
        path = repo / name
        if path.is_file():
            return json.loads(path.read_text(encoding="utf-8"))
    raise GlanceError(f"{repo.name}: no manifest ({', '.join(MANIFEST_NAMES)})")


def load_data(path: Path) -> dict[str, dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    repos = data.get("repos")
    if not isinstance(repos, dict):
        raise GlanceError(f"{path}: 'repos' must be an object")
    for name, entry in repos.items():
        if entry.get("hardware") not in HARDWARE_KEYS:
            raise GlanceError(f"{name}: 'hardware' must be one of {', '.join(HARDWARE_KEYS)}")
        if entry.get("target") not in (None, *TARGET_KEYS):
            raise GlanceError(f"{name}: 'target' must be null or one of {', '.join(TARGET_KEYS)}")
        tests = entry.get("tests")
        if tests is not None and not (isinstance(tests, dict) and isinstance(tests.get("count"), int) and tests["count"] > 0):
            raise GlanceError(f"{name}: 'tests' must be null or an object with a positive integer 'count'")
    return repos


def _cell(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ").strip()


def stack_text(manifest: dict) -> str:
    technologies = [str(item) for item in manifest.get("technologies", []) if str(item).strip()]
    if not technologies:
        technologies = [str(manifest.get("stack", "")).strip()]
    return " / ".join(technologies[:MAX_STACK_ITEMS])


def target_key(manifest: dict, entry: dict) -> str | None:
    """The target key, or None when the repository has no place it runs (a library) or says so."""
    if "target" in entry:
        return entry["target"]
    if manifest.get("role") == "library":
        return None
    return DEFAULT_TARGET.get(str(manifest.get("deployment_target")))


def render_section(code: str, manifest: dict, entry: dict) -> str:
    """The section for one language, with LF line endings and a closing blank line."""
    labels = LABELS[code]
    maturity = str(manifest["maturity"])
    rows = [
        (labels["version"], f"`{manifest['version']}`"),
        (labels["maturity"], MATURITY[code].get(maturity, maturity.capitalize())),
    ]
    tests = entry.get("tests")
    if tests:
        command = tests.get("command")
        rows.append((labels["tests"], f"{tests['count']} (`{command}`)" if command else str(tests["count"])))
    rows.append((labels["stack"], _cell(stack_text(manifest))))
    key = target_key(manifest, entry)
    if key:
        rows.append((labels["target"], TARGETS[code][key]))
    rows.append((labels["hardware"], HARDWARE[code][entry["hardware"]]))
    lines = [f"## 📋 {labels['heading']}", "", "| | |", "|---|---|"]
    lines += [f"| {name} | {value} |" for name, value in rows]
    lines.append("")
    return "\n".join(lines) + "\n"


def _split(text: str) -> tuple[list[str], str]:
    newline = "\r\n" if "\r\n" in text else "\n"
    return text.replace("\r\n", "\n").split("\n"), newline


def _headings(lines: list[str]) -> list[int]:
    """Indexes of the level-two headings that are not inside a code fence."""
    found, fenced = [], False
    for index, line in enumerate(lines):
        if FENCE.match(line):
            fenced = not fenced
        elif not fenced and ANY_H2.match(line):
            found.append(index)
    return found


def locate(lines: list[str]) -> tuple[int | None, int | None, int | None]:
    """(start of an existing section, its end, the index where a new one belongs)."""
    headings = _headings(lines)
    start = end = None
    for position, index in enumerate(headings):
        heading = HEADING.match(lines[index])
        if heading and heading.group(1) in ALL_HEADINGS:
            start = index
            end = headings[position + 1] if position + 1 < len(headings) else len(lines)
            break
    others = [index for index in headings if index != start]
    return start, end, (others[0] if others else None)


def apply_to_text(text: str, section: str) -> str:
    """Insert the section before the first heading, or rewrite it where it is. Idempotent."""
    lines, newline = _split(text)
    start, end, first_other = locate(lines)
    block = section.split("\n")[:-1]  # ends with the blank line of the section
    if start is not None:
        lines[start:end] = block
    else:
        if first_other is None:
            raise GlanceError("no level-two heading to put the section before")
        lines[first_other:first_other] = block
    return newline.join(lines)


def check_text(text: str, section: str) -> list[str]:
    """What is wrong with the section of a README: [] when it is exactly what it must be."""
    lines, _ = _split(text)
    start, end, first_other = locate(lines)
    if start is None:
        return ["the section is missing"]
    problems = []
    if first_other is not None and first_other < start:
        problems.append("the section is not the first level-two heading")
    current = "\n".join(lines[start:end]) + "\n"
    if current != section:
        problems.append("the section is stale (version, maturity, stack, target or hardware differ from the data)")
    return problems


def readme_path(repo: Path, code: str) -> Path:
    return repo / LANGUAGE_FILES[code]


def expected_sections(repo: Path, entry: dict) -> dict[str, str]:
    manifest = load_manifest(repo)
    return {code: render_section(code, manifest, entry) for code in LANGUAGE_FILES}


def apply_repo(repo: Path, entry: dict) -> list[str]:
    """Write the eight sections of one repository; return the files that changed."""
    changed = []
    for code, section in expected_sections(repo, entry).items():
        path = readme_path(repo, code)
        original = path.read_bytes().decode("utf-8")
        updated = apply_to_text(original, section)
        if updated != original:
            path.write_bytes(updated.encode("utf-8"))
            changed.append(path.name)
    return changed


def check_repo(repo: Path, entry: dict) -> list[str]:
    """One line per problem found in the eight READMEs of a repository."""
    problems = []
    for code, section in expected_sections(repo, entry).items():
        path = readme_path(repo, code)
        if not path.is_file():
            problems.append(f"{repo.name}/{path.name}: the file is missing")
            continue
        for problem in check_text(path.read_bytes().decode("utf-8"), section):
            problems.append(f"{repo.name}/{path.name}: {problem}")
    return problems
