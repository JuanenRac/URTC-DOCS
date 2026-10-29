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
  <img src="https://img.shields.io/badge/Version-0.1.1-0f6cbd.svg" alt="Version">
  <img src="https://img.shields.io/badge/Maturity-scaffolding-FFB020.svg" alt="Maturity">
</p>

---

**Verifica di onestà - cosa funziona davvero oggi:** questo repository contiene documenti e piccoli strumenti. Gli strumenti (il generatore del catalogo, quello del marchio, quello dei README, il controllo di pubblicazione e il controllo della famiglia) sono reali e hanno test unitari eseguiti in CI; il workflow notturno li esegue sugli altri repository della famiglia. I documenti sono scritti a partire dai README, manifesti, registri delle modifiche e documenti di quei repository così come sono stati letti per questa versione, e un'affermazione che non si è potuta ricondurre a un repository è segnalata come tale. Nulla qui è un test hardware: la matrice delle capacità dice, per ogni capacità, se è stata solo simulata, provata su un computer o eseguita su hardware reale, e il repository del firmware dichiara che non esiste ancora alcuna scheda assemblata.

---

> **Stato di sicurezza (safety e security):** questo ecosistema non è un sistema di sicurezza certificato e non esiste ancora alcuna scheda URTC assemblata. I bootloader controllano le immagini firmware con CRC32 e un HMAC-SHA256 a chiave condivisa, non con una firma asimmetrica (prevista); le immagini applicative pubblicate sono firmate con la chiave pubblica di sviluppo (`signing_key_kind: dev`), quindi chiunque può produrre un'immagine accettata dal bootloader; nulla è stato trasmesso a una scheda reale. Leggi la [base di sicurezza](docs/SECURITY_BASELINE.md) e il [modello delle minacce](docs/THREAT_MODEL.md) prima di fidarti di qualsiasi affermazione qui per la sicurezza di una persona.

## 📋 In breve

| | |
|---|---|
| Versione | `0.1.1` |
| Maturità | Impalcatura |
| Test | 153 |
| Tecnologia | Markdown / Mermaid / Python / SVG |
| Destinazione | Il PC di chi lo usa |
| Su hardware reale | Non applicabile: nulla qui gira su hardware |

**Vai a:** [Panoramica](#-panoramica) · [Architettura](#-architettura) · [Avvio rapido](#-avvio-rapido) · [Test](#-test) · [Struttura](#-struttura-del-repository) · [Correlati](#-progetti-correlati)

## 🚦 Stato del progetto

🟢 fatto e verificato · 🟡 funziona, con limiti noti · 🟠 a metà o non verificato · 🔴 non fatto o non funzionante. Nulla è verde se non ha mai girato su hardware reale.

| Parte | Stato | Ciò che il repository può dimostrare |
| --- | :---: | --- |
| Software | 🟡 | I generatori del catalogo, del marchio e dei README, e i controlli della pubblicazione, delle affermazioni e della famiglia, girano su un computer; nessun hardware coinvolto. |
| Test | 🟢 | La suite di test passa nella CI, su Linux e su Windows, a ogni push. |
| Controlli su tutta la famiglia | 🟡 | L'esecuzione notturna scarica ogni repository della famiglia e ne confronta le tabelle riassuntive, le affermazioni e la struttura del catalogo; una versione non aggiornata nel catalogo viene segnalata ma non fa fallire la notte. |
| Documenti di sicurezza | 🟡 | La base di sicurezza e il modello delle minacce sono scritti a partire dagli altri repository come sono stati letti; nessuno al di fuori del progetto li ha rivisti. |
| Documentazione | 🟡 | README in otto lingue e documenti di riferimento; le traduzioni non sono state riviste da madrelingua. |

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
* **Strumenti:** `make_catalog.py` scrive il catalogo, `make_brand.py` il banner, l'icona e la mappa delle famiglie, `make_readmes.py` gli otto README di questo repository, `publication_check.py` cerca qualsiasi cosa privata prima di una pubblicazione e `check_all.sh` esegue i controlli propri di ogni repository della famiglia e stampa una riga PASS, FAIL o SKIP per ciascuno. `make_glance.py` scrive la tabella In breve di ogni repository dal suo manifesto e da `data/glance.json` (`--check` confronta, `--apply` scrive); dopo un aumento di versione, `python tools/make_glance.py --apply --repo NOME` aggiorna la tabella di quel repository. `check_claims.py` legge il README inglese di ogni repository della famiglia e fallisce quando una frase contiene una parola a rischio (E-STOP, interblocco, tempo reale, firmato, mTLS, FDCAN, YOLO, guidato dall'IA, autonomo, certificato, ...) senza un indicatore di stato accanto (previsto, non implementato, opzionale, disattivato per impostazione predefinita, simulato, provato, ...), a meno che una persona abbia letto quella riga accanto al codice e l'abbia inserita in `data/claims_reviewed.json`. `check_repo_tools.py` confronta i file che ogni repository porta come la stessa copia (i controlli della politica di documentazione e della parità dei README, lo strumento che aumenta la versione del manifesto, il workflow che avvisa la dashboard) e fallisce quando uno differisce. `sync_repo_tools.py` scrive la copia canonica di quei file (`template/eh3d-repo-template`) in ogni repository, mantenendo le terminazioni di riga di ciascun file; senza `--apply` elenca soltanto ciò che cambierebbe. `urtc_doctor.py` è l'unico punto di ingresso: un rapporto sugli strumenti della macchina (Python, git, Node, il compilatore ARM, PySide6, porte seriali), sulle versioni di ogni repository (manifest, file sorgente e ultima voce del changelog), sulle copie di URTC-COMMON e sul firmware incluso nel flasher e nel web studio, sulla convalida di ogni repository e sui controlli di questo; `--fast` salta le convalide e `--online` confronta il firmware incluso con l'ultima release.

## 🧩 Ruolo in URTC

URTC-DOCS è la memoria dell'ecosistema: il luogo in cui vivono l'architettura, le interfacce, la base di sicurezza e la matrice delle capacità, e dove si conservano gli strumenti che confrontano tutti i repository fianco a fianco. Ogni repository conserva il proprio README, i propri test e il proprio contratto; questo dice come si incastrano e cosa è stato davvero provato.

## 🏛️ Architettura

<p align="center">
  <img src="images/architecture.svg" alt="Architettura di URTC-DOCS: che cosa legge, che cosa contiene e che cosa alimenta" width="100%">
</p>

Come si incastrano le parti di questo repository. L'immagine è disegnata da `docs/architecture.json` e verificata rispetto al codice.

## 🚀 Avvio rapido

**Requisiti:** Python 3.10 o successivo; pytest per i test

```bash
python tools/make_catalog.py --check                 # il catalogo è aggiornato (servono i repository accanto a questo)
python tools/make_brand.py --check                   # il banner, l'icona e la mappa sono aggiornati
python tools/make_readmes.py --check                 # gli otto README sono aggiornati
python tools/make_glance.py --check                  # le tabelle In breve della famiglia sono aggiornate (servono i repository accanto a questo)
python tools/publication_check.py                    # nulla di privato uscirebbe con una pubblicazione
python tools/check_claims.py --require-siblings      # nessun README afferma una capacità a rischio senza il suo stato (richiede i repository accanto a questo)
python tools/check_repo_tools.py --require-siblings  # i file che ogni repository porta come la stessa copia sono uguali (richiede i repository accanto a questo)
bash tools/check_all.sh                              # i controlli di ogni repository, una riga ciascuno
python tools/urtc_doctor.py                          # il doctor: un rapporto su questa macchina e su ogni repository
python -m pytest tests -q                            # i test unitari degli strumenti
```

## 🧪 Test

La suite ha 153 test (`python -m pytest tests -q`). Eseguono su dati di prova i generatori del catalogo, del marchio, delle tabelle In breve, delle tabelle di stato e dei README, i controlli di affermazioni, file condivisi, pubblicazione e il doctor, i vettori di conformità delle note CAN, e verificano che i README di questo repository siano esattamente ciò che scrive il generatore.

## 🏗️ Compilazione e rilascio

`build.sh` / `build.bat` installano il pacchetto ed eseguono i test, e `build-test.sh` / `build-test.bat` controllano senza installare; nessuno cambia una versione.

## 📂 Struttura del repository

<p align="center">
  <img src="images/repository-structure.svg" alt="Struttura del repository URTC-DOCS" width="100%">
</p>

<details>
<summary>Versione testuale dell'albero</summary>

```text
URTC-DOCS/
├── docs/                                              architettura, interfacce, matrice delle capacità, base di sicurezza, modello delle minacce e catalogo generato
├── src/urtc_docs/                                     gli strumenti come pacchetto: catalogo, marchio, README, In breve, stato, controlli
├── tools/                                             script sottili sopra il pacchetto, check_all.sh e i controlli di CI condivisi
├── data/                                              i numeri di In breve e le affermazioni riviste
├── template/                                          la copia canonica dei file che ogni repository condivide
├── tests/                                             test unitari degli strumenti
├── brand/                                             l'icona
├── images/                                            banner e immagini di questo README
├── .github/                                           workflow di CI e modelli per issue e pull request
├── build.sh build.bat                                 script di compilazione
├── build-test.sh build-test.bat                       script di compilazione e test che non cambiano nulla nel repository
├── test.sh test.bat                                   eseguono i test
├── run.sh run.bat                                     avviano il programma
├── urtc.project.json                                  manifesto: versione, ruolo, maturità e comando di compilazione
├── CHANGELOG.md                                       che cosa è cambiato in ogni versione
├── SECURITY.md SUPPORT.md                             politica di sicurezza e supporto
├── CONTRIBUTING.md CODE_OF_CONDUCT.md                 come contribuire e codice di condotta
├── .gitattributes .gitignore                          impostazioni di Git
├── bump.py bump_version.py bump_manifest_version.py   script che alzano la versione
├── LICENSE LICENSE.md                                 licenza del software e della documentazione
└── pyproject.toml requirements-dev.lock ruff.toml     pacchetto, strumenti bloccati e impostazioni di lint
```

</details>

## 🗺️ Roadmap e limiti noti

**Limiti noti oggi**

* La base di sicurezza e il modello delle minacce sono scritti a partire dagli altri repository così come sono stati letti; nessuno al di fuori del progetto li ha rivisti.
* L'esecuzione notturna scarica ogni repository della famiglia e confronta le loro tabelle riassuntive, le affermazioni e la struttura del catalogo; una versione obsoleta nel catalogo viene segnalata ma non fa fallire la notte.
* I documenti descrivono software; non interviene hardware e nessuna affermazione sulle schede è stata verificata su una scheda.

**Prossimi passi**

* Tenere aggiornati il catalogo, le tabelle In breve e la matrice delle capacità man mano che i repository cambiano.

## 🌍 Lingue

Il README e i testi esistono in inglese, spagnolo, francese, italiano, tedesco, cinese, giapponese e portoghese europeo.

## 🔗 Progetti correlati

URTC è fatto di repository indipendenti, ciascuno con la propria versione, i propri test e il proprio README. Ecco la famiglia, per gruppi:

* **URTC Tool Platform:** [URTC](https://github.com/JuanenRac/URTC), [URTC-COMMON](https://github.com/JuanenRac/URTC-COMMON), [URTC-FLASHER](https://github.com/JuanenRac/URTC-FLASHER), [URTC-GATEWAY](https://github.com/JuanenRac/URTC-GATEWAY), [URTC-SMART-RACK](https://github.com/JuanenRac/URTC-SMART-RACK), [URTC-TESTER](https://github.com/JuanenRac/URTC-TESTER), [URTC-VISION-TOOL](https://github.com/JuanenRac/URTC-VISION-TOOL), [URTC-WEB-STUDIO](https://github.com/JuanenRac/URTC-WEB-STUDIO)
* **Ecosystem Operations:** **URTC-DOCS** (questo repository), [URTC-UPDATER](https://github.com/JuanenRac/URTC-UPDATER)

**Progetti fratelli (indipendenti, con la stessa base e gli stessi strumenti):**

* **[HYDRA-UMC-DOCS](https://github.com/JuanenRac/HYDRA-UMC-DOCS)** - progetto fratello: il centro di documentazione di HYDRA-UMC, un ecosistema indipendente che condivide base e strumenti con questo
* **[ARMOR-DOCS](https://github.com/JuanenRac/ARMOR-DOCS)** - progetto fratello: il centro di documentazione di A.R.M.O.R., l'ecosistema di sicurezza, anch'esso indipendente e sulla stessa base
* **[JuanenRac](https://github.com/JuanenRac/JuanenRac)** - il profilo e il pannello di stato di tutti gli ecosistemi

## 📚 Documentazione

Dove leggere di più:

* [Matrice delle capacità: cosa è provato e cosa no](docs/CAPABILITY_MATRIX.md)
* [Catalogo dei progetti: versioni e tipi dei repository](docs/PROJECT_CATALOG.md)
* [Protocollo CAN: tre implementazioni di una specifica in prosa](docs/CAN_PROTOCOL_DUPLICATION.md)
* [Registro delle modifiche di questo repository](CHANGELOG.md)
* [Licenza (GPL-3.0-or-later)](LICENSE)

## 🤝 Contribuire e comunità

* Prima di una pull request esegui `URTC_CI=1 python tools/ci_validate.py`: deve passare. Vedi [CONTRIBUTING.md](CONTRIBUTING.md) e il [codice di condotta](CODE_OF_CONDUCT.md).
* Il README esiste in otto lingue: una modifica del testo si fa in tutti e otto i file, e le sezioni condivise con altri repository le scrive `tools/readme_sections.py` di URTC-COMMON.
* Non descrivere come funzionante su una scheda ciò che è stato solo compilato.
* Segnala una vulnerabilità in privato: [SECURITY.md](SECURITY.md). Domande, idee e segnalazioni: electrohobby3d@gmail.com ([SUPPORT.md](SUPPORT.md)).
* Domande, idee e segnalazioni: electrohobby3d@gmail.com

## 👤 AUTORE

**JuanenRac (Electro Hobby 3D)** · electrohobby3d@gmail.com

## 📜 LICENZA

Software: GPL-3.0-or-later - vedi [LICENSE](LICENSE). Documentazione: CC BY-SA 4.0 - vedi [LICENSE.md](LICENSE.md).
