# =============================================================================
# URTC-DOCS - src/urtc_docs/readme_related_text.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""One short line per repository of the family, in the eight languages, for Related Projects.

``DESCRIPTIONS[language][repository]`` is the line written after the name of the repository in the
Related Projects section of every README of the family (see ``readmes.related_lines``). The lines
say what each repository is for, without claims that only hardware could prove. Portuguese is the
Portuguese of Portugal.
"""
from __future__ import annotations

DESCRIPTIONS: dict[str, dict[str, str]] = {
    "en": {
        "URTC": "firmware of the tool-head board (25 tool profiles, CAN bootloader) and the CAN protocol reference.",
        "URTC-COMMON": "the CAN protocol written once as data (specification, generated tables, conformance vectors) and the code the programs share.",
        "URTC-FLASHER": "desktop tool that updates the board firmware over CAN or over SWD/JTAG.",
        "URTC-GATEWAY": "gateway in front of the CAN bus: lets only listed identifiers through, limits their rate and asks for a session key.",
        "URTC-SMART-RACK": "hardware-independent C logic and command protocol for a tool rack with pre-heating and lifecycle tracking.",
        "URTC-TESTER": "desktop live CAN-bus tester that shows the controls and telemetry of the tool profile a board reports.",
        "URTC-VISION-TOOL": "sensor-frame protocol in C and a Python thermal/RGB companion for an inspection tool head.",
        "URTC-WEB-STUDIO": "browser app that flashes and tests the board over Web Serial and SLCAN, with nothing to install.",
        "URTC-DOCS": "architecture, interfaces, security baseline and generated catalogue of the ecosystem, plus the tools that compare all repositories.",
        "URTC-UPDATER": "desktop tool that detects, installs and updates the repositories of the URTC family, one explicit action at a time.",
    },
    "es": {
        "URTC": "firmware de la placa del cabezal de herramienta (25 perfiles de herramienta, bootloader CAN) y la referencia del protocolo CAN.",
        "URTC-COMMON": "el protocolo CAN escrito una sola vez como datos (especificación, tablas generadas, vectores de conformidad) y el código que comparten los programas.",
        "URTC-FLASHER": "herramienta de escritorio que actualiza el firmware de la placa por CAN o por SWD/JTAG.",
        "URTC-GATEWAY": "pasarela delante del bus CAN: solo deja pasar los identificadores de una lista, limita su frecuencia y pide una clave de sesión.",
        "URTC-SMART-RACK": "lógica en C independiente del hardware y protocolo de órdenes para un soporte de herramientas con precalentamiento y seguimiento del ciclo de vida.",
        "URTC-TESTER": "probador de escritorio del bus CAN en vivo que muestra los controles y la telemetría del perfil de herramienta que informa una placa.",
        "URTC-VISION-TOOL": "protocolo de tramas de sensor en C y un acompañante en Python térmico/RGB para un cabezal de inspección.",
        "URTC-WEB-STUDIO": "aplicación de navegador que graba y prueba la placa por Web Serial y SLCAN, sin instalar nada.",
        "URTC-DOCS": "arquitectura, interfaces, línea base de seguridad y catálogo generado del ecosistema, más las herramientas que comparan todos los repositorios.",
        "URTC-UPDATER": "herramienta de escritorio que detecta, instala y actualiza los repositorios de la familia URTC, una acción explícita cada vez.",
    },
    "de": {
        "URTC": "Firmware der Werkzeugkopf-Platine (25 Werkzeugprofile, CAN-Bootloader) und die Referenz des CAN-Protokolls.",
        "URTC-COMMON": "das CAN-Protokoll einmal als Daten geschrieben (Spezifikation, erzeugte Tabellen, Konformitätsvektoren) und der Code, den die Programme teilen.",
        "URTC-FLASHER": "Desktop-Werkzeug, das die Platinen-Firmware über CAN oder über SWD/JTAG aktualisiert.",
        "URTC-GATEWAY": "Gateway vor dem CAN-Bus: lässt nur gelistete Kennungen durch, begrenzt ihre Rate und verlangt einen Sitzungsschlüssel.",
        "URTC-SMART-RACK": "hardwareunabhängige C-Logik und Befehlsprotokoll für eine Werkzeugablage mit Vorheizen und Lebenszyklusverfolgung.",
        "URTC-TESTER": "Desktop-Live-Tester für den CAN-Bus, der die Bedienelemente und die Telemetrie des von einer Platine gemeldeten Werkzeugprofils zeigt.",
        "URTC-VISION-TOOL": "Sensorrahmen-Protokoll in C und ein Python-Thermo-/RGB-Begleiter für einen Inspektions-Werkzeugkopf.",
        "URTC-WEB-STUDIO": "Browser-App, die die Platine über Web Serial und SLCAN flasht und testet, ohne Installation.",
        "URTC-DOCS": "Architektur, Schnittstellen, Sicherheitsbasis und erzeugter Katalog des Ökosystems sowie die Werkzeuge, die alle Repositories vergleichen.",
        "URTC-UPDATER": "Desktop-Werkzeug, das die Repositories der URTC-Familie erkennt, installiert und aktualisiert, jeweils eine ausdrückliche Aktion.",
    },
    "fr": {
        "URTC": "firmware de la carte de la tête d'outil (25 profils d'outil, bootloader CAN) et référence du protocole CAN.",
        "URTC-COMMON": "le protocole CAN écrit une seule fois comme données (spécification, tables générées, vecteurs de conformité) et le code que les programmes partagent.",
        "URTC-FLASHER": "outil de bureau qui met à jour le firmware de la carte par CAN ou par SWD/JTAG.",
        "URTC-GATEWAY": "passerelle devant le bus CAN : ne laisse passer que les identifiants d'une liste, limite leur cadence et demande une clé de session.",
        "URTC-SMART-RACK": "logique C indépendante du matériel et protocole de commandes pour un support d'outils avec préchauffage et suivi du cycle de vie.",
        "URTC-TESTER": "testeur de bureau du bus CAN en direct qui affiche les commandes et la télémétrie du profil d'outil signalé par une carte.",
        "URTC-VISION-TOOL": "protocole de trames de capteur en C et compagnon Python thermique/RVB pour une tête d'outil d'inspection.",
        "URTC-WEB-STUDIO": "application de navigateur qui flashe et teste la carte via Web Serial et SLCAN, sans rien installer.",
        "URTC-DOCS": "architecture, interfaces, base de sécurité et catalogue généré de l'écosystème, plus les outils qui comparent tous les dépôts.",
        "URTC-UPDATER": "outil de bureau qui détecte, installe et met à jour les dépôts de la famille URTC, une action explicite à la fois.",
    },
    "it": {
        "URTC": "firmware della scheda della testa utensile (25 profili utensile, bootloader CAN) e riferimento del protocollo CAN.",
        "URTC-COMMON": "il protocollo CAN scritto una sola volta come dati (specifica, tabelle generate, vettori di conformità) e il codice condiviso dai programmi.",
        "URTC-FLASHER": "strumento desktop che aggiorna il firmware della scheda via CAN o via SWD/JTAG.",
        "URTC-GATEWAY": "gateway davanti al bus CAN: lascia passare solo gli identificatori di un elenco, ne limita la frequenza e chiede una chiave di sessione.",
        "URTC-SMART-RACK": "logica C indipendente dall'hardware e protocollo di comandi per un portautensili con preriscaldamento e tracciamento del ciclo di vita.",
        "URTC-TESTER": "tester desktop del bus CAN in tempo reale che mostra i comandi e la telemetria del profilo utensile segnalato da una scheda.",
        "URTC-VISION-TOOL": "protocollo di frame del sensore in C e un companion Python termico/RGB per una testa utensile di ispezione.",
        "URTC-WEB-STUDIO": "app per browser che programma e collauda la scheda via Web Serial e SLCAN, senza installare nulla.",
        "URTC-DOCS": "architettura, interfacce, base di sicurezza e catalogo generato dell'ecosistema, più gli strumenti che confrontano tutti i repository.",
        "URTC-UPDATER": "strumento desktop che rileva, installa e aggiorna i repository della famiglia URTC, un'azione esplicita alla volta.",
    },
    "ja": {
        "URTC": "ツールヘッド基板のファームウェア(25 のツールプロファイル、CAN ブートローダー)と CAN プロトコルのリファレンス。",
        "URTC-COMMON": "一度だけデータとして書かれた CAN プロトコル(仕様、生成された表、適合ベクトル)と、各プログラムが共有するコード。",
        "URTC-FLASHER": "CAN または SWD/JTAG で基板のファームウェアを更新するデスクトップツール。",
        "URTC-GATEWAY": "CAN バスの手前に置くゲートウェイ。一覧にある識別子だけを通し、レートを制限し、セッション鍵を求めます。",
        "URTC-SMART-RACK": "予熱とライフサイクル追跡を備えたツールラック向けの、ハードウェア非依存の C ロジックとコマンドプロトコル。",
        "URTC-TESTER": "基板が報告するツールプロファイルの操作部とテレメトリを表示する、デスクトップ用のライブ CAN バステスター。",
        "URTC-VISION-TOOL": "C のセンサーフレームプロトコルと、検査用ツールヘッド向けの Python サーマル/RGB コンパニオン。",
        "URTC-WEB-STUDIO": "Web Serial と SLCAN で基板の書き込みとテストを行うブラウザアプリ。インストール不要。",
        "URTC-DOCS": "エコシステムのアーキテクチャ、インターフェース、セキュリティベースライン、生成されたカタログと、全リポジトリを比較するツール。",
        "URTC-UPDATER": "URTC ファミリーのリポジトリを検出・インストール・更新するデスクトップツール。操作は一つずつ明示的に行います。",
    },
    "zh": {
        "URTC": "工具头电路板的固件(25 个工具配置、CAN 引导程序)以及 CAN 协议参考。",
        "URTC-COMMON": "只写一次的 CAN 协议数据(规范、生成的表格、一致性向量)以及各程序共享的代码。",
        "URTC-FLASHER": "通过 CAN 或 SWD/JTAG 更新电路板固件的桌面工具。",
        "URTC-GATEWAY": "位于 CAN 总线前的网关:只放行列表中的标识符,限制其速率,并要求会话密钥。",
        "URTC-SMART-RACK": "用于带预热和生命周期跟踪的工具架的、与硬件无关的 C 逻辑和命令协议。",
        "URTC-TESTER": "桌面实时 CAN 总线测试器,显示电路板所报告工具配置的控件和遥测。",
        "URTC-VISION-TOOL": "C 语言的传感器帧协议,以及用于检测工具头的 Python 热成像/RGB 配套程序。",
        "URTC-WEB-STUDIO": "通过 Web Serial 和 SLCAN 烧录并测试电路板的浏览器应用,无需安装。",
        "URTC-DOCS": "生态系统的架构、接口、安全基线和生成的目录,以及比较所有仓库的工具。",
        "URTC-UPDATER": "检测、安装并更新 URTC 家族仓库的桌面工具,每次只执行一个明确的操作。",
    },
    "pt": {
        "URTC": "firmware da placa da cabeça de ferramenta (25 perfis de ferramenta, bootloader CAN) e a referência do protocolo CAN.",
        "URTC-COMMON": "o protocolo CAN escrito uma só vez como dados (especificação, tabelas geradas, vetores de conformidade) e o código que os programas partilham.",
        "URTC-FLASHER": "ferramenta de ambiente de trabalho que atualiza o firmware da placa por CAN ou por SWD/JTAG.",
        "URTC-GATEWAY": "gateway à frente do barramento CAN: só deixa passar os identificadores de uma lista, limita a sua taxa e pede uma chave de sessão.",
        "URTC-SMART-RACK": "lógica em C independente do hardware e protocolo de comandos para um suporte de ferramentas com pré-aquecimento e acompanhamento do ciclo de vida.",
        "URTC-TESTER": "testador de ambiente de trabalho do barramento CAN em direto que mostra os controlos e a telemetria do perfil de ferramenta que uma placa reporta.",
        "URTC-VISION-TOOL": "protocolo de tramas de sensor em C e um companheiro em Python térmico/RGB para uma cabeça de ferramenta de inspeção.",
        "URTC-WEB-STUDIO": "aplicação de navegador que grava e testa a placa por Web Serial e SLCAN, sem instalar nada.",
        "URTC-DOCS": "arquitetura, interfaces, base de segurança e catálogo gerado do ecossistema, mais as ferramentas que comparam todos os repositórios.",
        "URTC-UPDATER": "ferramenta de ambiente de trabalho que deteta, instala e atualiza os repositórios da família URTC, uma ação explícita de cada vez.",
    },
}
