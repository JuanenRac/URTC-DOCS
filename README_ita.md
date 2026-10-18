<p align="center">
  <img src="images/URTC_DOCS_BANNER.svg" alt="URTC-DOCS banner" width="100%">
</p>

# 📚 URTC-DOCS

<p align="center"><a href="README.md">🇺🇸 English</a> | <a href="README_spa.md">🇪🇸 Español</a> | <a href="README_fra.md">🇫🇷 Français</a> | 🇮🇹 <b>Italiano</b> | <a href="README_deu.md">🇩🇪 Deutsch</a> | <a href="README_zho.md">🇨🇳 简体中文</a> | <a href="README_jpn.md">🇯🇵 日本語</a> | <a href="README_por.md">🇵🇹 Português</a></p>

### Architettura, interfacce, base di sicurezza e la verità su ciò che è provato

<p align="center">
  <img src="https://img.shields.io/badge/License-GPL%203.0--or--later-blue.svg" alt="GPL 3.0 or later">
  <img src="https://img.shields.io/badge/Format-Markdown-083fa1.svg" alt="Format">
  <img src="https://img.shields.io/badge/Languages-8-00E5FF.svg" alt="Languages">
  <img src="https://img.shields.io/badge/Version-0.0.1-0f6cbd.svg" alt="Version">
  <img src="https://img.shields.io/badge/Maturity-scaffolding-FFB020.svg" alt="Maturity">
</p>

---

**Verifica di onestà - cosa funziona davvero oggi:** questo repository contiene documenti e piccoli strumenti. Gli strumenti (il generatore del catalogo, quello del marchio, quello dei README, il controllo di pubblicazione e il controllo della famiglia) sono reali e hanno test unitari eseguiti in CI; il workflow notturno li esegue sugli altri repository della famiglia. I documenti sono scritti a partire dai README, manifesti, registri delle modifiche e documenti di quei repository così come sono stati letti per questa versione, e un'affermazione che non si è potuta ricondurre a un repository è segnalata come tale. Nulla qui è un test hardware: la matrice delle capacità dice, per ogni capacità, se è stata solo simulata, provata su un computer o eseguita su hardware reale, e il repository del firmware dichiara che non esiste ancora alcuna scheda assemblata.

---

## 📋 In breve

| | |
|---|---|
| Versione | `0.0.1` |
| Maturità | Impalcatura |
| Stack | Markdown e Python 3.10+ (solo libreria standard) |
| Destinazione | Un PC di sviluppo (nessun servizio, nessuna porta) |
| Su hardware reale | Non applicabile: è documentazione e strumenti; registra ciò che gli altri repository hanno eseguito su hardware |

## 🎯 Panoramica

<p align="center">
  <img src="images/URTC_ECOSYSTEM.svg" alt="URTC ecosystem" width="100%">
</p>

L'immagine qui sotto mostra i repository di URTC, il bus CAN che collega le schede e gli strumenti del computer, e i collegamenti che i loro documenti affermano.

* [Architettura](docs/ARCHITECTURE.md): livelli, flussi di dati, porte e confini di fiducia.
* [Interfacce](docs/INTERFACES.md): chi possiede ogni contratto e dove è documentato.
* [Matrice delle capacità](docs/CAPABILITY_MATRIX.md): cosa è provato in software e cosa richiede hardware, progetto per progetto.
* [Base di sicurezza](docs/SECURITY_BASELINE.md): cosa il codice impone e cosa manca ancora; e il [modello delle minacce](docs/THREAT_MODEL.md).
* [Prima fetta verticale](docs/FIRST_VERTICAL_SLICE.md): il più piccolo percorso da un capo all'altro che esiste oggi.
* [Duplicazione del protocollo CAN](docs/CAN_PROTOCOL_DUPLICATION.md): il protocollo è implementato tre volte a partire da un testo; cosa conterrebbe una specifica condivisa.
* [Catalogo dei progetti](docs/PROJECT_CATALOG.md): ogni repository dell'ecosistema, scritto a partire dal proprio manifesto.
* **Strumenti:** `make_catalog.py` scrive il catalogo, `make_brand.py` il banner, l'icona e la mappa delle famiglie, `make_readmes.py` gli otto README di questo repository, `publication_check.py` cerca qualsiasi cosa privata prima di una pubblicazione e `check_all.sh` esegue i controlli propri di ogni repository della famiglia e stampa una riga PASS, FAIL o SKIP per ciascuno.

## 🧩 Ruolo in URTC

URTC-DOCS è la memoria dell'ecosistema: il luogo in cui vivono l'architettura, le interfacce, la base di sicurezza e la matrice delle capacità, e dove si conservano gli strumenti che confrontano tutti i repository fianco a fianco. Ogni repository conserva il proprio README, i propri test e il proprio contratto; questo dice come si incastrano e cosa è stato davvero provato.

## 📂 Struttura del repository

```text
URTC-DOCS/
├── docs/     architettura, interfacce, matrice delle capacità, base di sicurezza, modello delle minacce, prima fetta, nota sul protocollo CAN, catalogo generato
├── src/      gli strumenti come pacchetto (catalogo, marchio, README, controllo di pubblicazione)
├── tools/    script sottili sopra il pacchetto, check_all.sh e i controlli CI condivisi dell'ecosistema
├── tests/    test unitari degli strumenti
├── images/   banner e mappa dell'ecosistema
├── brand/    l'icona
├── build.sh / build.bat, build-test.sh / build-test.bat, run.sh / run.bat
└── urtc.project.json, pyproject.toml, CHANGELOG.md, LICENSE, LICENSE.md
```

## 🛠️ COMPILAZIONE ED ESECUZIONE

**Requisiti:** Python 3.10 o successivo; pytest per i test

```bash
python tools/make_catalog.py --check  # il catalogo è aggiornato (servono i repository accanto a questo)
python tools/make_brand.py --check    # il banner, l'icona e la mappa sono aggiornati
python tools/make_readmes.py --check  # gli otto README sono aggiornati
python tools/publication_check.py     # nulla di privato uscirebbe con una pubblicazione
bash tools/check_all.sh               # i controlli di ogni repository, una riga ciascuno
python -m pytest tests -q             # i test unitari degli strumenti
```

`build.sh` / `build.bat` alzano la versione di un passo (il contachilometri dell'ecosistema), installano il pacchetto ed eseguono i test; `build-test.sh` / `build-test.bat` controllano senza cambiare alcuna versione.

## 🔗 Progetti correlati

URTC è fatto di repository indipendenti, ciascuno con la propria versione, i propri test e il proprio README. Ecco la famiglia, per gruppi:

* **URTC Tool Platform:** [URTC](https://github.com/JuanenRac/URTC), [URTC-FLASHER](https://github.com/JuanenRac/URTC-FLASHER), [URTC-SMART-RACK](https://github.com/JuanenRac/URTC-SMART-RACK), [URTC-TESTER](https://github.com/JuanenRac/URTC-TESTER), [URTC-VISION-TOOL](https://github.com/JuanenRac/URTC-VISION-TOOL), [URTC-WEB-STUDIO](https://github.com/JuanenRac/URTC-WEB-STUDIO)
* **Ecosystem Operations:** **URTC-DOCS** (questo repository), [URTC-UPDATER](https://github.com/JuanenRac/URTC-UPDATER)

**Oltre URTC:**

* **[HYDRA-UMC](https://github.com/JuanenRac/HYDRA-UMC)** - la scheda madre del braccio robotico, il cui relay CAN è documentato come il bus a cui si collega la testa utensile
* **[HYDRA-UMC-DOCS](https://github.com/JuanenRac/HYDRA-UMC-DOCS)** - la stessa idea per l'ecosistema HYDRA-UMC
* **[ARMOR-DOCS](https://github.com/JuanenRac/ARMOR-DOCS)** - la stessa idea per l'ecosistema di sicurezza A.R.M.O.R.
* **[JuanenRac](https://github.com/JuanenRac/JuanenRac)** - il profilo e il pannello di stato di tutti gli ecosistemi

## 📚 Documentazione e comunità

Dove leggere di più:

* [Matrice delle capacità: cosa è provato e cosa no](docs/CAPABILITY_MATRIX.md)
* [Catalogo dei progetti: versioni e tipi dei repository](docs/PROJECT_CATALOG.md)
* [Protocollo CAN: tre implementazioni di una specifica in prosa](docs/CAN_PROTOCOL_DUPLICATION.md)
* [Registro delle modifiche di questo repository](CHANGELOG.md)
* [Licenza (GPL-3.0-or-later)](LICENSE)
* Domande, idee e segnalazioni: electrohobby3d@gmail.com

## 👤 AUTORE

**JuanenRac (Electro Hobby 3D)** · electrohobby3d@gmail.com

## 📜 LICENZA

Software: GPL-3.0-or-later - vedi [LICENSE](LICENSE). Documentazione: CC BY-SA 4.0 - vedi [LICENSE.md](LICENSE.md).
