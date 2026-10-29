# =============================================================================
# URTC-DOCS - src/urtc_docs/status.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""The "Project status" table of the README: the one of this repository, and the check that every repository has one.

Every README of the family ends with a "Project status" section: a table with one row per real part of the
repository and a traffic light in the Status column (and only the light). The other repositories get their table
from the shared README sections of URTC-COMMON; the README of this repository is written by readmes.py, which
takes the section from :func:`render_own`. :func:`check_text` says what is wrong with the section of one README
(missing, no lights, a cell that is not a light, too few rows) and :func:`check_repo` runs it over the eight
READMEs of a repository and compares the lights of the translations with the English one.
"""
from __future__ import annotations

import re
from pathlib import Path

from . import glance

LIGHTS = ("🟢", "🟡", "🟠", "🔴")
MIN_ROWS = 3
HEADING = re.compile(r"^## (?:💡|🚦) \S")   # the shared sections write it with the traffic-light icon (universal layout); this repository's own README still has the bulb
ANY_H2 = re.compile(r"^## ")
FENCE = re.compile(r"^\s*(```|~~~)")

# code -> (heading, legend, the three column heads)
UI: dict[str, tuple[str, str, tuple[str, str, str]]] = {
    "en": ("Project status", "🟢 done and verified · 🟡 works, with known limits · 🟠 half done or not verified · 🔴 not done or not working. Nothing is green if it never ran on real hardware.",
           ("Part", "Status", "What the repository can show")),
    "es": ("Estado del proyecto", "🟢 hecho y verificado · 🟡 funciona, con límites conocidos · 🟠 a medias o sin verificar · 🔴 sin hacer o sin funcionar. Nada es verde si nunca corrió en hardware real.",
           ("Parte", "Estado", "Lo que el repositorio puede demostrar")),
    "de": ("Projektstatus", "🟢 fertig und überprüft · 🟡 funktioniert, mit bekannten Grenzen · 🟠 halb fertig oder nicht überprüft · 🔴 nicht gemacht oder funktioniert nicht. Nichts ist grün, wenn es nie auf echter Hardware lief.",
           ("Teil", "Status", "Was das Repository belegen kann")),
    "fr": ("État du projet", "🟢 fait et vérifié · 🟡 fonctionne, avec des limites connues · 🟠 à moitié fait ou non vérifié · 🔴 non fait ou non fonctionnel. Rien n'est vert si cela n'a jamais tourné sur du vrai matériel.",
           ("Partie", "État", "Ce que le dépôt peut démontrer")),
    "it": ("Stato del progetto", "🟢 fatto e verificato · 🟡 funziona, con limiti noti · 🟠 a metà o non verificato · 🔴 non fatto o non funzionante. Nulla è verde se non ha mai girato su hardware reale.",
           ("Parte", "Stato", "Ciò che il repository può dimostrare")),
    "ja": ("プロジェクトの状況", "🟢 完了・検証済み · 🟡 動作するが既知の制限あり · 🟠 途中、または未検証 · 🔴 未実施または動作しない。実機で一度も動いていないものは緑になりません。",
           ("項目", "状態", "リポジトリが示せること")),
    "zh": ("项目状态", "🟢 已完成并已验证 · 🟡 可用，但有已知限制 · 🟠 做了一半或未验证 · 🔴 未完成或不能用。从未在真实硬件上运行过的内容不会是绿色。",
           ("部分", "状态", "仓库能够证明的内容")),
    "pt": ("Estado do projeto", "🟢 feito e verificado · 🟡 funciona, com limites conhecidos · 🟠 a meio ou por verificar · 🔴 por fazer ou a não funcionar. Nada é verde se nunca correu em hardware real.",
           ("Parte", "Estado", "O que o repositório consegue demonstrar")),
}

# the rows of this repository: (part, light, note) per language, the same lights in every language
OWN_ROWS: dict[str, list[tuple[str, str, str]]] = {
    "en": [
        ("Software", "🟡", "The generators of the catalogue, the brand and the READMEs, and the checks of the publication, the claims and the family, run on a computer; no hardware is involved."),
        ("Tests", "🟢", "The test suite passes in the CI, on Linux and on Windows, on every push."),
        ("Checks across the family", "🟡", "The nightly run fetches every repository of the family and compares their summary tables, claims and catalogue structure; a stale version in the catalogue is reported but does not fail the night."),
        ("Security documents", "🟡", "The security baseline and the threat model are written from the other repositories as they were read; nobody outside the project has reviewed them."),
        ("Documentation", "🟡", "README in eight languages and reference documents; the translations were not reviewed by native speakers."),
    ],
    "es": [
        ("Software", "🟡", "Los generadores del catálogo, de la marca y de los README, y las comprobaciones de la publicación, de las afirmaciones y de la familia, funcionan en un ordenador; no interviene hardware."),
        ("Pruebas", "🟢", "La batería de pruebas pasa en la CI, en Linux y en Windows, en cada subida."),
        ("Comprobaciones de toda la familia", "🟡", "La ejecución nocturna descarga cada repositorio de la familia y compara sus tablas resumen, afirmaciones y estructura del catálogo; una versión desfasada en el catálogo se avisa pero no hace fallar la noche."),
        ("Documentos de seguridad", "🟡", "La base de seguridad y el modelo de amenazas se escriben a partir de los demás repositorios tal como se leyeron; nadie ajeno al proyecto los ha revisado."),
        ("Documentación", "🟡", "README en ocho idiomas y documentos de referencia; las traducciones no las ha revisado ningún hablante nativo."),
    ],
    "de": [
        ("Software", "🟡", "Die Generatoren für Katalog, Marke und READMEs sowie die Prüfungen von Veröffentlichung, Aussagen und Familie laufen auf einem Computer; keine Hardware beteiligt."),
        ("Tests", "🟢", "Die Testsuite besteht bei jedem Push in der CI, unter Linux und unter Windows."),
        ("Prüfungen über die Familie", "🟡", "Der nächtliche Lauf holt jedes Repository der Familie und vergleicht deren Übersichtstabellen, Aussagen und die Struktur des Katalogs; eine veraltete Version im Katalog wird gemeldet, lässt die Nacht aber nicht scheitern."),
        ("Sicherheitsdokumente", "🟡", "Die Sicherheitsgrundlage und das Bedrohungsmodell sind aus den anderen Repositorys geschrieben, so wie sie gelesen wurden; niemand außerhalb des Projekts hat sie geprüft."),
        ("Dokumentation", "🟡", "README in acht Sprachen und Referenzdokumente; die Übersetzungen wurden nicht von Muttersprachlern geprüft."),
    ],
    "fr": [
        ("Logiciel", "🟡", "Les générateurs du catalogue, de la marque et des README, et les vérifications de la publication, des affirmations et de la famille, tournent sur un ordinateur ; aucun matériel impliqué."),
        ("Tests", "🟢", "La suite de tests passe dans la CI, sous Linux et sous Windows, à chaque push."),
        ("Vérifications sur toute la famille", "🟡", "L'exécution de nuit récupère chaque dépôt de la famille et compare leurs tableaux de synthèse, leurs affirmations et la structure du catalogue ; une version périmée dans le catalogue est signalée mais ne fait pas échouer la nuit."),
        ("Documents de sécurité", "🟡", "La base de sécurité et le modèle de menaces sont écrits à partir des autres dépôts tels qu'ils ont été lus ; personne en dehors du projet ne les a relus."),
        ("Documentation", "🟡", "README en huit langues et documents de référence ; les traductions n'ont pas été relues par des locuteurs natifs."),
    ],
    "it": [
        ("Software", "🟡", "I generatori del catalogo, del marchio e dei README, e i controlli della pubblicazione, delle affermazioni e della famiglia, girano su un computer; nessun hardware coinvolto."),
        ("Test", "🟢", "La suite di test passa nella CI, su Linux e su Windows, a ogni push."),
        ("Controlli su tutta la famiglia", "🟡", "L'esecuzione notturna scarica ogni repository della famiglia e ne confronta le tabelle riassuntive, le affermazioni e la struttura del catalogo; una versione non aggiornata nel catalogo viene segnalata ma non fa fallire la notte."),
        ("Documenti di sicurezza", "🟡", "La base di sicurezza e il modello delle minacce sono scritti a partire dagli altri repository come sono stati letti; nessuno al di fuori del progetto li ha rivisti."),
        ("Documentazione", "🟡", "README in otto lingue e documenti di riferimento; le traduzioni non sono state riviste da madrelingua."),
    ],
    "ja": [
        ("ソフトウェア", "🟡", "カタログ、ブランド、README のジェネレーターと、公開前・主張・ファミリー全体の検査はコンピューター上で動作します。ハードウェアは関与しません。"),
        ("テスト", "🟢", "テストスイートはプッシュごとに CI で、Linux と Windows の両方で通ります。"),
        ("ファミリー全体の検査", "🟡", "夜間の実行でファミリーのすべてのリポジトリを取得し、概要表、主張、カタログの構造を比較します。カタログのバージョンが古い場合は報告されますが、夜間の実行は失敗扱いになりません。"),
        ("セキュリティ文書", "🟡", "セキュリティの基準と脅威モデルは、読み取った時点の他のリポジトリをもとに書かれています。プロジェクト外の人によるレビューは受けていません。"),
        ("ドキュメント", "🟡", "8 言語の README と参照ドキュメントがあります。翻訳はネイティブによるレビューを受けていません。"),
    ],
    "zh": [
        ("软件", "🟡", "目录、品牌和 README 的生成器，以及发布、声明和整个系列的检查，都在电脑上运行；不涉及硬件。"),
        ("测试", "🟢", "每次推送时，测试套件都会在 CI 中通过，Linux 和 Windows 均如此。"),
        ("整个系列的检查", "🟡", "每晚的运行会取回系列中的每个仓库，并比较它们的概览表、声明和目录结构；目录中过期的版本会被报告，但不会让当晚的运行失败。"),
        ("安全文档", "🟡", "安全基线和威胁模型是根据读到的其他仓库内容写成的；项目之外没有人审阅过。"),
        ("文档", "🟡", "提供八种语言的 README 和参考文档；翻译未经母语者审阅。"),
    ],
    "pt": [
        ("Software", "🟡", "Os geradores do catálogo, da marca e dos README, e as verificações da publicação, das afirmações e da família, funcionam num computador; não envolve hardware."),
        ("Testes", "🟢", "A bateria de testes passa na CI, em Linux e em Windows, em cada envio."),
        ("Verificações de toda a família", "🟡", "A execução noturna obtém cada repositório da família e compara as suas tabelas-resumo, afirmações e a estrutura do catálogo; uma versão desatualizada no catálogo é assinalada, mas não faz falhar a noite."),
        ("Documentos de segurança", "🟡", "A base de segurança e o modelo de ameaças são escritos a partir dos outros repositórios tal como foram lidos; ninguém fora do projeto os reviu."),
        ("Documentação", "🟡", "README em oito línguas e documentos de referência; as traduções não foram revistas por falantes nativos."),
    ],
}


def _cell(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ").strip()


def render_own(code: str) -> str:
    """The section for the README of this repository in one language, with LF line endings and a closing blank line."""
    heading, legend, heads = UI[code]
    lines = [f"## 💡 {heading}", "", legend, "", "| " + " | ".join(heads) + " |", "| --- | :---: | --- |"]
    lines += [f"| {_cell(part)} | {light} | {_cell(note)} |" for part, light, note in OWN_ROWS[code]]
    lines.append("")
    return "\n".join(lines) + "\n"


def _section(lines: list[str]) -> list[str] | None:
    """The lines of the status section (heading included), or None when the README has none."""
    fenced, start = False, None
    for index, line in enumerate(lines):
        if FENCE.match(line):
            fenced = not fenced
        elif not fenced and ANY_H2.match(line):
            if start is not None:
                return lines[start:index]
            if HEADING.match(line):
                start = index
    return lines[start:] if start is not None else None


def lights(text: str) -> list[str]:
    """The lights of the Status column in order; raises ValueError saying what is wrong with the section."""
    block = _section(text.replace("\r\n", "\n").split("\n"))
    if block is None:
        raise ValueError("the 'Project status' section is missing")
    rows = [line for line in block if line.startswith("|")]
    if len(rows) < 2 + MIN_ROWS:
        raise ValueError(f"the 'Project status' table needs a header and at least {MIN_ROWS} rows")
    found = []
    for row in rows[2:]:
        cells = [part.strip() for part in re.split(r"(?<!\\)\|", row.strip().strip("|"))]
        if len(cells) != 3 or not cells[0] or not cells[2]:
            raise ValueError(f"a row of the 'Project status' table does not have a part, a status and a note: {row[:60]}")
        if cells[1] not in LIGHTS:
            raise ValueError(f"the Status column must hold only a light, not {cells[1][:20]!r}")
        found.append(cells[1])
    return found


def check_text(text: str) -> list[str]:
    """What is wrong with the status section of one README: [] when it is a valid table of lights."""
    try:
        lights(text)
    except ValueError as error:
        return [str(error)]
    return []


def check_repo(repo: Path) -> list[str]:
    """One line per problem in the eight READMEs of a repository: a missing or malformed table, or lights that differ from the English one."""
    problems: list[str] = []
    english: list[str] | None = None
    for code, filename in glance.LANGUAGE_FILES.items():
        path = repo / filename
        if not path.is_file():
            continue
        try:
            found = lights(path.read_bytes().decode("utf-8"))
        except ValueError as error:
            problems.append(f"{repo.name}/{filename}: {error}")
            continue
        if code == "en":
            english = found
        elif english is not None and found != english:
            problems.append(f"{repo.name}/{filename}: the lights of the 'Project status' table differ from README.md")
    return problems
