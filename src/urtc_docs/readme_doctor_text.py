# =============================================================================
# URTC-DOCS - src/urtc_docs/readme_doctor_text.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""The words about the doctor report that README.md and its translations add to the generated text.

``TOOLS`` documents ``tools/urtc_doctor.py`` in the list of tools; ``COMMENT`` is the comment of its command in the
build and run block.
"""
from __future__ import annotations

TOOLS: dict[str, str] = {
    "en": " `urtc_doctor.py` is the single entry point: one report with the tools of the machine (Python, git, Node, the ARM compiler, PySide6, serial ports), the versions of every repository (manifest, source file and newest changelog entry), the copies of URTC-COMMON and the firmware bundled by the flasher and the web studio, the validation of every repository and the checks of this one; `--fast` leaves out the validations and `--online` compares the bundled firmware with the newest release.",
    "es": " `urtc_doctor.py` es el punto de entrada único: un informe con las herramientas de la máquina (Python, git, Node, el compilador ARM, PySide6, puertos serie), las versiones de cada repositorio (manifiesto, archivo fuente y última entrada del changelog), las copias de URTC-COMMON y el firmware incluido en el flasher y en el web studio, la validación de cada repositorio y las comprobaciones de este; `--fast` omite las validaciones y `--online` compara el firmware incluido con la última release.",
    "de": " `urtc_doctor.py` ist der einzige Einstiegspunkt: ein Bericht über die Werkzeuge des Rechners (Python, git, Node, den ARM-Compiler, PySide6, serielle Ports), die Versionen jedes Repositorys (Manifest, Quelldatei und neuester Changelog-Eintrag), die Kopien von URTC-COMMON und die vom Flasher und vom Web Studio mitgelieferte Firmware, die Validierung jedes Repositorys und die Prüfungen dieses Repositorys; `--fast` lässt die Validierungen weg und `--online` vergleicht die mitgelieferte Firmware mit dem neuesten Release.",
    "fr": " `urtc_doctor.py` est le point d'entrée unique : un rapport sur les outils de la machine (Python, git, Node, le compilateur ARM, PySide6, ports série), les versions de chaque dépôt (manifeste, fichier source et dernière entrée du changelog), les copies d'URTC-COMMON et le firmware embarqué par le flasher et le web studio, la validation de chaque dépôt et les vérifications de celui-ci ; `--fast` omet les validations et `--online` compare le firmware embarqué avec la dernière release.",
    "it": " `urtc_doctor.py` è l'unico punto di ingresso: un rapporto sugli strumenti della macchina (Python, git, Node, il compilatore ARM, PySide6, porte seriali), sulle versioni di ogni repository (manifest, file sorgente e ultima voce del changelog), sulle copie di URTC-COMMON e sul firmware incluso nel flasher e nel web studio, sulla convalida di ogni repository e sui controlli di questo; `--fast` salta le convalide e `--online` confronta il firmware incluso con l'ultima release.",
    "ja": " `urtc_doctor.py` は唯一の入口です。マシンのツール（Python、git、Node、ARM コンパイラー、PySide6、シリアルポート）、各リポジトリのバージョン（マニフェスト、ソースファイル、changelog の最新エントリ）、URTC-COMMON のコピー、フラッシャーと Web スタジオに同梱されたファームウェア、各リポジトリの検証、そしてこのリポジトリのチェックを 1 つのレポートにまとめます。`--fast` は検証を省略し、`--online` は同梱ファームウェアを最新リリースと比較します。",
    "zh": " `urtc_doctor.py` 是唯一的入口：它生成一份报告，包含本机工具（Python、git、Node、ARM 编译器、PySide6、串口）、每个仓库的版本（清单、源文件和最新的 changelog 条目）、URTC-COMMON 的副本以及烧录工具和 Web 工作室内置的固件、每个仓库的验证和本仓库的检查；`--fast` 跳过验证，`--online` 将内置固件与最新发布版本比较。",
    "pt": " `urtc_doctor.py` é o ponto de entrada único: um relatório com as ferramentas da máquina (Python, git, Node, o compilador ARM, PySide6, portas série), as versões de cada repositório (manifesto, ficheiro de código e entrada mais recente do changelog), as cópias de URTC-COMMON e o firmware incluído no flasher e no web studio, a validação de cada repositório e as verificações deste; `--fast` omite as validações e `--online` compara o firmware incluído com a release mais recente.",
}

COMMENT: dict[str, str] = {
    "en": "the doctor: one report on this machine and on every repository",
    "es": "el doctor: un informe sobre esta máquina y sobre cada repositorio",
    "de": "der Doctor: ein Bericht über diesen Rechner und jedes Repository",
    "fr": "le doctor : un rapport sur cette machine et sur chaque dépôt",
    "it": "il doctor: un rapporto su questa macchina e su ogni repository",
    "ja": "ドクター：このマシンと各リポジトリについての 1 つのレポート",
    "zh": "医生：关于本机和每个仓库的一份报告",
    "pt": "o doctor: um relatório sobre esta máquina e sobre cada repositório",
}
