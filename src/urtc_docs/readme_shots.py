# =============================================================================
# URTC-DOCS - src/urtc_docs/readme_shots.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""The pictures of the READMEs: which images each program shows (they live in its ``images/screenshots/``) and what each one says, in the eight
languages. They are taken at 1920x1080 with made-up sample data, never on a real installation. ``tools/apply_screenshots.py`` writes them."""
from __future__ import annotations

CODES = ("en", "es", "de", "fr", "it", "ja", "zh", "pt")
FILES = {
    "en": "README.md", "es": "README_spa.md", "de": "README_deu.md", "fr": "README_fra.md",
    "it": "README_ita.md", "ja": "README_jpn.md", "zh": "README_zho.md", "pt": "README_por.md",
}

HEADING = {
    "en": "Screenshots", "es": "Capturas de pantalla", "de": "Screenshots", "fr": "Captures d'écran",
    "it": "Schermate", "ja": "スクリーンショット", "zh": "屏幕截图", "pt": "Capturas de ecrã",
}

NOTE = {
    "en": "Captured at 1920×1080 on a test bench, with sample data and no real installation behind them.",
    "es": "Capturadas a 1920×1080 en un banco de pruebas, con datos de ejemplo y sin ninguna instalación real detrás.",
    "de": "Aufgenommen mit 1920×1080 auf einem Prüfstand, mit Beispieldaten und ohne eine echte Anlage dahinter.",
    "fr": "Capturées en 1920×1080 sur un banc d'essai, avec des données d'exemple et sans installation réelle derrière.",
    "it": "Catturate a 1920×1080 su un banco di prova, con dati di esempio e senza alcuna installazione reale dietro.",
    "ja": "テストベンチで 1920×1080 で撮影。サンプルデータを使用しており、実際の設備は接続されていません。",
    "zh": "在测试台上以 1920×1080 截取，使用示例数据，背后没有真实的安装。",
    "pt": "Capturadas a 1920×1080 numa bancada de testes, com dados de exemplo e sem qualquer instalação real por trás.",
}


def _c(*texts: str) -> dict[str, str]:
    return dict(zip(CODES, texts, strict=True))


# one caption per kind of screen; the order of the languages is en, es, de, fr, it, ja, zh, pt
CAPTIONS = {
    "flasher_deck": _c(
        "The window as it opens: the connection, the firmware inventory, the four checkpoints of a CAN-OTA update and the device configuration.",
        "La ventana al abrirse: la conexión, el inventario de firmware, los cuatro puntos de control de una actualización CAN-OTA y la configuración del dispositivo.",
        "Das Fenster beim Öffnen: die Verbindung, das Firmware-Inventar, die vier Kontrollpunkte einer CAN-OTA-Aktualisierung und die Gerätekonfiguration.",
        "La fenêtre à l'ouverture : la connexion, l'inventaire des firmwares, les quatre points de contrôle d'une mise à jour CAN-OTA et la configuration de l'appareil.",
        "La finestra all'apertura: la connessione, l'inventario dei firmware, i quattro punti di controllo di un aggiornamento CAN-OTA e la configurazione del dispositivo.",
        "起動直後のウィンドウ：接続、ファームウェアの一覧、CAN-OTA 更新の 4 つのチェックポイント、デバイス設定。",
        "刚打开时的窗口：连接、固件清单、CAN-OTA 更新的四个检查点以及设备配置。",
        "A janela ao abrir: a ligação, o inventário de firmware, os quatro pontos de controlo de uma atualização CAN-OTA e a configuração do dispositivo."),
    "tester_deck": _c(
        "The window as it opens: the transport gate, the listen-only safety mode, the tool profiles and the identity and health checkpoints.",
        "La ventana al abrirse: la puerta de transporte, el modo seguro de solo escucha, los perfiles de herramienta y los puntos de control de identidad y salud.",
        "Das Fenster beim Öffnen: das Transport-Tor, der Sicherheitsmodus „nur lauschen“, die Werkzeugprofile und die Kontrollpunkte für Identität und Zustand.",
        "La fenêtre à l'ouverture : la porte de transport, le mode sûr en écoute seule, les profils d'outil et les points de contrôle d'identité et de santé.",
        "La finestra all'apertura: il varco di trasporto, la modalità sicura di solo ascolto, i profili degli utensili e i punti di controllo di identità e salute.",
        "起動直後のウィンドウ：トランスポートゲート、受信専用の安全モード、ツールプロファイル、識別と健全性のチェックポイント。",
        "刚打开时的窗口：传输入口、仅监听的安全模式、工具配置文件以及身份与健康检查点。",
        "A janela ao abrir: a porta de transporte, o modo seguro só de escuta, os perfis de ferramenta e os pontos de controlo de identidade e saúde."),
    "heads": _c(
        "Tool heads on the bus: a modelled bus with six heads, one in each state a head can be in (selected, address conflict, fault latched, in its bootloader, lost and ready).",
        "Cabezales en el bus: un bus modelado con seis cabezales, uno en cada estado posible (seleccionado, conflicto de dirección, fallo retenido, en su bootloader, perdido y listo).",
        "Werkzeugköpfe am Bus: ein modellierter Bus mit sechs Köpfen, jeder in einem anderen möglichen Zustand (gewählt, Adresskonflikt, Fehler gehalten, im Bootloader, verloren und bereit).",
        "Têtes d'outil sur le bus : un bus modélisé avec six têtes, une dans chaque état possible (sélectionnée, conflit d'adresse, défaut mémorisé, dans son bootloader, perdue et prête).",
        "Teste utensile sul bus: un bus modellato con sei teste, una per ogni stato possibile (selezionata, conflitto di indirizzo, guasto memorizzato, nel bootloader, persa e pronta).",
        "バス上のツールヘッド：6 つのヘッドを持つモデル化したバスで、各ヘッドが取り得る状態（選択中、アドレス競合、障害保持、ブートローダー中、喪失、準備完了）を 1 つずつ示します。",
        "总线上的工具头：一条模拟总线上的六个工具头，每个处于一种可能的状态（已选择、地址冲突、故障锁定、处于引导程序、丢失和就绪）。",
        "Cabeças de ferramenta no barramento: um barramento modelado com seis cabeças, cada uma num estado possível (selecionada, conflito de endereço, falha retida, no bootloader, perdida e pronta)."),
    "help": _c(
        "The Help window: the steps for using the program, written in the language of the window.",
        "La ventana de Ayuda: los pasos para usar el programa, escritos en el idioma de la ventana.",
        "Das Hilfefenster: die Schritte zur Benutzung des Programms, in der Sprache des Fensters.",
        "La fenêtre d'aide : les étapes d'utilisation du programme, dans la langue de la fenêtre.",
        "La finestra della Guida: i passi per usare il programma, scritti nella lingua della finestra.",
        "ヘルプウィンドウ：プログラムの使い方の手順を、ウィンドウの言語で表示します。",
        "帮助窗口：使用该程序的各个步骤，使用窗口的语言显示。",
        "A janela de Ajuda: os passos para utilizar o programa, escritos no idioma da janela."),
    "updates": _c(
        "The update window: a newer signed package is installed only after you confirm it.",
        "La ventana de actualizaciones: un paquete firmado más reciente solo se instala después de que lo confirmes.",
        "Das Update-Fenster: ein neueres signiertes Paket wird erst nach deiner Bestätigung installiert.",
        "La fenêtre de mise à jour : un paquet signé plus récent n'est installé qu'après votre confirmation.",
        "La finestra degli aggiornamenti: un pacchetto firmato più recente viene installato solo dopo la tua conferma.",
        "更新ウィンドウ：新しい署名付きパッケージは、確認した後にのみインストールされます。",
        "更新窗口：只有在你确认之后，才会安装较新的已签名软件包。",
        "A janela de atualizações: um pacote assinado mais recente só é instalado depois de o confirmar."),
    "updater_deck": _c(
        "The window over a workspace with the family in it: every project with its maturity, stack and local version, and the safe update actions.",
        "La ventana sobre un espacio de trabajo con la familia: cada proyecto con su madurez, pila y versión local, y las acciones de actualización segura.",
        "Das Fenster über einem Arbeitsbereich mit der Familie darin: jedes Projekt mit Reifegrad, Stack und lokaler Version sowie die sicheren Aktualisierungsaktionen.",
        "La fenêtre sur un espace de travail contenant la famille : chaque projet avec sa maturité, sa pile et sa version locale, et les actions de mise à jour sûres.",
        "La finestra su uno spazio di lavoro con la famiglia: ogni progetto con maturità, stack e versione locale, e le azioni di aggiornamento sicuro.",
        "ファミリー全体を含む作業領域を表示したウィンドウ：各プロジェクトの成熟度、スタック、ローカルバージョンと、安全な更新操作。",
        "显示包含整个系列的工作区的窗口：每个项目的成熟度、技术栈和本地版本，以及安全更新操作。",
        "A janela sobre uma área de trabalho com a família: cada projeto com a sua maturidade, pilha e versão local, e as ações de atualização segura."),
    "packages": _c(
        "The Packages window: the programs of the family that a release publishes as a signed package, each checking its own release.",
        "La ventana de Paquetes: los programas de la familia que una versión publica como paquete firmado, cada uno comprobando su propia versión.",
        "Das Paket-Fenster: die Programme der Familie, die ein Release als signiertes Paket veröffentlicht, jedes prüft sein eigenes Release.",
        "La fenêtre des paquets : les programmes de la famille qu'une version publie comme paquet signé, chacun vérifiant sa propre version.",
        "La finestra dei pacchetti: i programmi della famiglia che una versione pubblica come pacchetto firmato, ciascuno con il controllo della propria versione.",
        "パッケージウィンドウ：リリースが署名付きパッケージとして公開するファミリーのプログラムを、それぞれ自身のリリースを確認しながら表示します。",
        "软件包窗口：系列中以已签名软件包形式发布的程序，每个程序检查各自的发布版本。",
        "A janela de Pacotes: os programas da família que uma versão publica como pacote assinado, cada um a verificar a sua própria versão."),
    "web_control": _c(
        "Tool matrix and control: the 25 tool profiles of the firmware with their jumpers, and the controls of the selected tool (a simulator tab: it sends nothing to the bus).",
        "Matriz de herramientas y control: los 25 perfiles de herramienta del firmware con sus puentes, y los controles de la herramienta seleccionada (pestaña de simulador: no envía nada al bus).",
        "Werkzeugmatrix und Steuerung: die 25 Werkzeugprofile der Firmware mit ihren Jumpern und die Bedienelemente des gewählten Werkzeugs (Simulator-Tab: sendet nichts auf den Bus).",
        "Matrice des outils et commande : les 25 profils d'outil du firmware avec leurs cavaliers, et les commandes de l'outil sélectionné (onglet simulateur : il n'envoie rien sur le bus).",
        "Matrice degli utensili e controllo: i 25 profili utensile del firmware con i loro jumper e i comandi dell'utensile selezionato (scheda simulatore: non invia nulla al bus).",
        "ツールマトリクスと制御：ファームウェアの 25 のツールプロファイルとそのジャンパー、選択したツールの操作（シミュレーターのタブ：バスには何も送信しません）。",
        "工具矩阵与控制：固件的 25 个工具配置及其跳线，以及所选工具的控件（模拟器标签页：不会向总线发送任何内容）。",
        "Matriz de ferramentas e controlo: os 25 perfis de ferramenta do firmware com os seus jumpers e os controlos da ferramenta selecionada (separador de simulador: não envia nada para o barramento)."),
    "web_oled": _c(
        "OLED and hardware monitor: the status screen of the tool, the five identification jumpers, the status LED and the 8-LED ring (a simulator tab).",
        "OLED y monitor de hardware: la pantalla de estado de la herramienta, los cinco puentes de identificación, el LED de estado y el anillo de 8 LED (pestaña de simulador).",
        "OLED und Hardware-Monitor: der Statusbildschirm des Werkzeugs, die fünf Kennungs-Jumper, die Status-LED und der 8-LED-Ring (Simulator-Tab).",
        "OLED et moniteur matériel : l'écran d'état de l'outil, les cinq cavaliers d'identification, la LED d'état et l'anneau de 8 LED (onglet simulateur).",
        "OLED e monitor hardware: la schermata di stato dell'utensile, i cinque jumper di identificazione, il LED di stato e l'anello da 8 LED (scheda simulatore).",
        "OLED とハードウェアモニター：ツールのステータス画面、5 本の識別ジャンパー、ステータス LED、8 LED リング（シミュレーターのタブ）。",
        "OLED 与硬件监视器：工具的状态屏幕、五个识别跳线、状态 LED 和 8 灯环（模拟器标签页）。",
        "OLED e monitor de hardware: o ecrã de estado da ferramenta, os cinco jumpers de identificação, o LED de estado e o anel de 8 LED (separador de simulador)."),
    "web_flasher": _c(
        "Flasher: the flash map of the board, the image and its manifest ready to send, and the options of a CAN-OTA update (modelled board; nothing is sent).",
        "Flasher: el mapa de flash de la placa, la imagen y su manifiesto listos para enviar, y las opciones de una actualización CAN-OTA (placa modelada; no se envía nada).",
        "Flasher: die Flash-Karte der Platine, das Image und sein Manifest versandbereit sowie die Optionen einer CAN-OTA-Aktualisierung (modellierte Platine; es wird nichts gesendet).",
        "Flasher : la carte flash de la carte, l'image et son manifeste prêts à l'envoi, et les options d'une mise à jour CAN-OTA (carte modélisée ; rien n'est envoyé).",
        "Flasher: la mappa flash della scheda, l'immagine e il suo manifesto pronti all'invio e le opzioni di un aggiornamento CAN-OTA (scheda modellata; non si invia nulla).",
        "フラッシャー：ボードのフラッシュマップ、送信準備が整ったイメージとそのマニフェスト、CAN-OTA 更新のオプション（モデル化したボード。何も送信しません）。",
        "刷写器：电路板的闪存映射、准备发送的映像及其清单，以及 CAN-OTA 更新的选项（模拟电路板，不发送任何内容）。",
        "Flasher: o mapa de flash da placa, a imagem e o seu manifesto prontos a enviar e as opções de uma atualização CAN-OTA (placa modelada; não se envia nada)."),
    "web_thermal": _c(
        "Thermal inspection: a false-colour image of a 32×24 infrared array with a simulated hot spot (a simulator tab).",
        "Inspección térmica: una imagen en falso color de una matriz infrarroja de 32×24 con un punto caliente simulado (pestaña de simulador).",
        "Thermische Inspektion: ein Falschfarbenbild eines 32×24-Infrarot-Arrays mit einem simulierten Hotspot (Simulator-Tab).",
        "Inspection thermique : une image en fausses couleurs d'une matrice infrarouge de 32×24 avec un point chaud simulé (onglet simulateur).",
        "Ispezione termica: un'immagine a falsi colori di una matrice a infrarossi 32×24 con un punto caldo simulato (scheda simulatore).",
        "サーモグラフィ検査：32×24 の赤外線アレイの擬似カラー画像と、模擬のホットスポット（シミュレーターのタブ）。",
        "热成像检查：32×24 红外阵列的伪彩色图像，带有一个模拟的热点（模拟器标签页）。",
        "Inspeção térmica: uma imagem em falsa cor de uma matriz de infravermelhos de 32×24 com um ponto quente simulado (separador de simulador)."),
    "web_tester": _c(
        "Tester diagnostics: the black box and the thermal counters over time, read from a modelled board.",
        "Diagnóstico del tester: la caja negra y los contadores térmicos a lo largo del tiempo, leídos de una placa modelada.",
        "Tester-Diagnose: die Blackbox und die thermischen Zähler im Zeitverlauf, gelesen von einer modellierten Platine.",
        "Diagnostic du testeur : la boîte noire et les compteurs thermiques dans le temps, lus sur une carte modélisée.",
        "Diagnostica del tester: la scatola nera e i contatori termici nel tempo, letti da una scheda modellata.",
        "テスター診断：ブラックボックスと、時間経過に伴う温度カウンター（モデル化したボードから読み取り）。",
        "测试器诊断：黑匣子和随时间变化的热计数器，读取自模拟电路板。",
        "Diagnóstico do testador: a caixa negra e os contadores térmicos ao longo do tempo, lidos de uma placa modelada."),
}

# repository -> [(file in images/screenshots/, caption key)]
SHOTS = {
    "URTC-FLASHER": [("deck", "flasher_deck"), ("heads", "heads"), ("help", "help"), ("updates", "updates")],
    "URTC-TESTER": [("deck", "tester_deck"), ("heads", "heads"), ("help", "help"), ("updates", "updates")],
    "URTC-UPDATER": [("deck", "updater_deck"), ("packages", "packages"), ("help", "help"), ("updates", "updates")],
    "URTC-WEB-STUDIO": [("control", "web_control"), ("oled", "web_oled"), ("flasher", "web_flasher"), ("thermal", "web_thermal"), ("tester", "web_tester")],
}
