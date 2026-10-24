<p align="center">
  <img src="images/URTC_DOCS_BANNER.svg" alt="URTC-DOCS banner" width="100%">
</p>

# 📚 URTC-DOCS

<p align="center"><a href="README.md">🇺🇸 English</a> | <a href="README_spa.md">🇪🇸 Español</a> | <a href="README_fra.md">🇫🇷 Français</a> | <a href="README_ita.md">🇮🇹 Italiano</a> | 🇩🇪 <b>Deutsch</b> | <a href="README_zho.md">🇨🇳 简体中文</a> | <a href="README_jpn.md">🇯🇵 日本語</a> | <a href="README_por.md">🇵🇹 Português</a></p>

### Architektur, Schnittstellen, Sicherheitsbasis und die Wahrheit über das, was belegt ist

<p align="center">
  <img src="https://img.shields.io/badge/License-GPL%203.0--or--later-blue.svg" alt="GPL 3.0 or later">
  <img src="https://img.shields.io/badge/Format-Markdown-083fa1.svg" alt="Format">
  <img src="https://img.shields.io/badge/Languages-8-00E5FF.svg" alt="Languages">
  <img src="https://img.shields.io/badge/Version-0.1.0-0f6cbd.svg" alt="Version">
  <img src="https://img.shields.io/badge/Maturity-scaffolding-FFB020.svg" alt="Maturity">
</p>

---

**Ehrlichkeitsprüfung - was heute wirklich läuft:** dieses Repository enthält Dokumente und kleine Werkzeuge. Die Werkzeuge (der Katalog-Generator, der Marken-Generator, der README-Generator, die Veröffentlichungsprüfung und die Familienprüfung) sind echt und haben Unit-Tests, die in der CI laufen; der nächtliche Workflow führt sie gegen die übrigen Repositories der Familie aus. Die Dokumente sind aus den READMEs, Manifesten, Änderungsprotokollen und Dokumenten dieser Repositories geschrieben, wie sie für diese Version gelesen wurden, und eine Aussage, die sich nicht auf ein Repository zurückführen ließ, ist als solche gekennzeichnet. Nichts davon ist ein Hardwaretest: Die Fähigkeitenmatrix sagt für jede Fähigkeit, ob sie nur simuliert, auf einem Computer getestet oder auf echter Hardware ausgeführt wurde, und das Firmware-Repository gibt an, dass noch keine bestückte Platine existiert.

---

> **Stand von Sicherheit (Safety) und Security:** Dieses Ökosystem ist kein zertifiziertes Sicherheitssystem, und es existiert noch keine bestückte URTC-Platine. Die Bootloader prüfen Firmware-Images mit CRC32 und einem HMAC-SHA256 mit gemeinsamem Schlüssel, nicht mit einer asymmetrischen Signatur (geplant); die veröffentlichten Anwendungs-Images sind mit dem öffentlichen Entwicklungsschlüssel signiert (`signing_key_kind: dev`), sodass jeder ein vom Bootloader akzeptiertes Image erzeugen kann; an eine echte Platine wurde noch nichts gesendet. Lesen Sie die [Sicherheitsbasis](docs/SECURITY_BASELINE.md) und das [Bedrohungsmodell](docs/THREAT_MODEL.md), bevor Sie sich für die Sicherheit einer Person auf eine Aussage hier verlassen.

## 📋 Auf einen Blick

| | |
|---|---|
| Version | `0.1.0` |
| Reifegrad | Gerüst |
| Technik | Markdown / Mermaid / Python / SVG |
| Ziel | Der PC der Person, die es benutzt |
| Auf echter Hardware | Nicht zutreffend: nichts hiervon läuft auf Hardware |

## 🎯 Überblick

<p align="center">
  <img src="images/URTC_ECOSYSTEM.svg" alt="URTC ecosystem" width="100%">
</p>

Das Bild unten zeigt die Repositories von URTC, den CAN-Bus, der die Platinen und die PC-Werkzeuge verbindet, und die Verbindungen, die ihre Dokumente behaupten.

* [Architektur](docs/ARCHITECTURE.md): Schichten, Datenflüsse, Ports und Vertrauensgrenzen.
* [Schnittstellen](docs/INTERFACES.md): wem jeder Vertrag gehört und wo er dokumentiert ist.
* [Fähigkeitenmatrix](docs/CAPABILITY_MATRIX.md): was in Software belegt ist und was Hardware braucht, Projekt für Projekt.
* [Sicherheitsbasis](docs/SECURITY_BASELINE.md): was der Code durchsetzt und was noch fehlt; und das [Bedrohungsmodell](docs/THREAT_MODEL.md).
* [Erster vertikaler Schnitt](docs/FIRST_VERTICAL_SLICE.md): der kleinste durchgehende Pfad, den es heute gibt.
* [Duplizierung des CAN-Protokolls](docs/CAN_PROTOCOL_DUPLICATION.md): das Protokoll ist dreimal aus einem Text heraus implementiert; was eine gemeinsame Spezifikation enthalten würde.
* [Projektkatalog](docs/PROJECT_CATALOG.md): jedes Repository des Ökosystems, aus seinem eigenen Manifest geschrieben.
* **Werkzeuge:** `make_catalog.py` schreibt den Katalog, `make_brand.py` das Banner, das Symbol und die Familienkarte, `make_readmes.py` die acht READMEs dieses Repositorys, `publication_check.py` sucht vor einer Veröffentlichung nach allem Privaten, und `check_all.sh` führt die eigenen Prüfungen jedes Repositorys der Familie aus und gibt je eine Zeile PASS, FAIL oder SKIP aus. `make_glance.py` schreibt die Tabelle Auf einen Blick jedes Repositorys aus dessen Manifest und aus `data/glance.json` (`--check` vergleicht, `--apply` schreibt); nach einer Versionserhöhung aktualisiert `python tools/make_glance.py --apply --repo NAME` die Tabelle dieses Repositorys. `check_claims.py` liest das englische README jedes Repositorys der Familie und schlägt fehl, wenn ein Satz ein Risikowort enthält (E-STOP, Verriegelung, Echtzeit, signiert, mTLS, FDCAN, YOLO, KI-gesteuert, autonom, zertifiziert, ...) und daneben keine Statusmarkierung steht (geplant, nicht implementiert, optional, standardmäßig aus, simuliert, getestet, ...), es sei denn, eine Person hat diese Zeile neben dem Code gelesen und in `data/claims_reviewed.json` eingetragen. `check_repo_tools.py` vergleicht die Dateien, die jedes Repository als dieselbe Kopie führt (die Prüfungen der Dokumentationsrichtlinie und der README-Parität, das Werkzeug zum Erhöhen der Manifestversion, der Workflow für die Dashboard-Meldung), und schlägt fehl, wenn eine abweicht. `sync_repo_tools.py` schreibt die kanonische Kopie dieser Dateien (`template/eh3d-repo-template`) in jedes Repository und behält dabei die Zeilenenden jeder Datei; ohne `--apply` listet es nur auf, was sich ändern würde. `urtc_doctor.py` ist der einzige Einstiegspunkt: ein Bericht über die Werkzeuge des Rechners (Python, git, Node, den ARM-Compiler, PySide6, serielle Ports), die Versionen jedes Repositorys (Manifest, Quelldatei und neuester Changelog-Eintrag), die Kopien von URTC-COMMON und die vom Flasher und vom Web Studio mitgelieferte Firmware, die Validierung jedes Repositorys und die Prüfungen dieses Repositorys; `--fast` lässt die Validierungen weg und `--online` vergleicht die mitgelieferte Firmware mit dem neuesten Release.

## 🧩 Rolle in URTC

URTC-DOCS ist das Gedächtnis des Ökosystems: der Ort, an dem Architektur, Schnittstellen, Sicherheitsbasis und Fähigkeitenmatrix liegen und an dem die Werkzeuge aufbewahrt werden, die alle Repositories nebeneinander vergleichen. Jedes Repository behält sein eigenes README, seine Tests und seinen Vertrag; dieses sagt, wie sie zusammenpassen und was wirklich belegt wurde.

## 📂 Repository-Struktur

```text
URTC-DOCS/
├── docs/     Architektur, Schnittstellen, Fähigkeitenmatrix, Sicherheitsbasis, Bedrohungsmodell, erster Schnitt, Notiz zum CAN-Protokoll, erzeugter Katalog
├── src/      die Werkzeuge als Paket (Katalog, Marke, READMEs, Veröffentlichungsprüfung)
├── tools/    dünne Skripte über dem Paket, check_all.sh und die gemeinsamen CI-Prüfungen des Ökosystems
├── tests/    Unit-Tests der Werkzeuge
├── images/   Banner und Karte des Ökosystems
├── brand/    das Symbol
├── data/     die Daten, die die Generatoren lesen (die Zahlen von „Auf einen Blick“, die geprüften Aussagen)
├── template/ die maßgebliche Kopie der Dateien, die alle Repositories teilen, und das Werkzeug, das sie einspielt
├── build.sh / build.bat, build-test.sh / build-test.bat, run.sh / run.bat
└── urtc.project.json, pyproject.toml, CHANGELOG.md, LICENSE, LICENSE.md
```

## 🛠️ BUILD & AUSFÜHRUNG

**Voraussetzungen:** Python 3.10 oder neuer; pytest für die Tests

```bash
python tools/make_catalog.py --check                 # der Katalog ist aktuell (braucht die Repositories neben diesem)
python tools/make_brand.py --check                   # Banner, Symbol und Karte sind aktuell
python tools/make_readmes.py --check                 # die acht READMEs sind aktuell
python tools/make_glance.py --check                  # die Tabellen Auf einen Blick der Familie sind aktuell (braucht die Repositories neben diesem)
python tools/publication_check.py                    # nichts Privates würde mit einer Veröffentlichung hinausgehen
python tools/check_claims.py --require-siblings      # kein README nennt eine riskante Fähigkeit ohne ihren Status (braucht die Repositorys neben diesem)
python tools/check_repo_tools.py --require-siblings  # die Dateien, die jedes Repository als dieselbe Kopie führt, sind gleich (braucht die Repositorys neben diesem)
bash tools/check_all.sh                              # die Prüfungen jedes Repositorys, eine Zeile je Repository
python tools/urtc_doctor.py                          # der Doctor: ein Bericht über diesen Rechner und jedes Repository
python -m pytest tests -q                            # die Unit-Tests der Werkzeuge
```

`build.sh` / `build.bat` installieren das Paket und führen die Tests aus, und `build-test.sh` / `build-test.bat` prüfen, ohne zu installieren; keines ändert eine Version. `python bump.py` erhöht die Version um einen Schritt (der Kilometerzähler des Ökosystems).

## 🔗 Verwandte Projekte

URTC besteht aus unabhängigen Repositories mit jeweils eigener Version, eigenen Tests und eigenem README. Das ist die Familie, nach Gruppen:

* **URTC Tool Platform:** [URTC](https://github.com/JuanenRac/URTC), [URTC-COMMON](https://github.com/JuanenRac/URTC-COMMON), [URTC-FLASHER](https://github.com/JuanenRac/URTC-FLASHER), [URTC-GATEWAY](https://github.com/JuanenRac/URTC-GATEWAY), [URTC-SMART-RACK](https://github.com/JuanenRac/URTC-SMART-RACK), [URTC-TESTER](https://github.com/JuanenRac/URTC-TESTER), [URTC-VISION-TOOL](https://github.com/JuanenRac/URTC-VISION-TOOL), [URTC-WEB-STUDIO](https://github.com/JuanenRac/URTC-WEB-STUDIO)
* **Ecosystem Operations:** **URTC-DOCS** (dieses Repository), [URTC-UPDATER](https://github.com/JuanenRac/URTC-UPDATER)

**Über URTC hinaus:**

* **[HYDRA-UMC](https://github.com/JuanenRac/HYDRA-UMC)** - die Hauptplatine des Roboterarms, deren CAN-Relay als der Bus dokumentiert ist, an dem der Werkzeugkopf hängt
* **[HYDRA-UMC-DOCS](https://github.com/JuanenRac/HYDRA-UMC-DOCS)** - dieselbe Idee für das Ökosystem HYDRA-UMC
* **[ARMOR-DOCS](https://github.com/JuanenRac/ARMOR-DOCS)** - dieselbe Idee für das Sicherheits-Ökosystem A.R.M.O.R.
* **[JuanenRac](https://github.com/JuanenRac/JuanenRac)** - das Profil und das Status-Dashboard aller Ökosysteme

## 📚 Dokumentation & Community

Wo man mehr liest:

* [Fähigkeitenmatrix: was belegt ist und was nicht](docs/CAPABILITY_MATRIX.md)
* [Projektkatalog: Versionen und Arten der Repositories](docs/PROJECT_CATALOG.md)
* [CAN-Protokoll: drei Implementierungen einer Prosa-Spezifikation](docs/CAN_PROTOCOL_DUPLICATION.md)
* [Änderungsprotokoll dieses Repositorys](CHANGELOG.md)
* [Lizenz (GPL-3.0-or-later)](LICENSE)
* Fragen, Ideen und Meldungen: electrohobby3d@gmail.com

## 👤 AUTOR

**JuanenRac (Electro Hobby 3D)** · electrohobby3d@gmail.com

## 📜 LIZENZ

Software: GPL-3.0-or-later - siehe [LICENSE](LICENSE). Dokumentation: CC BY-SA 4.0 - siehe [LICENSE.md](LICENSE.md).
