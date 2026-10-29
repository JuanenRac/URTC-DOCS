<p align="center">
  <img src="images/URTC_DOCS_BANNER.svg" alt="URTC-DOCS banner" width="100%">
</p>

# 📚 URTC-DOCS

<p align="center"><a href="README.md">🇺🇸 English</a> | <a href="README_spa.md">🇪🇸 Español</a> | 🇫🇷 <b>Français</b> | <a href="README_ita.md">🇮🇹 Italiano</a> | <a href="README_deu.md">🇩🇪 Deutsch</a> | <a href="README_zho.md">🇨🇳 简体中文</a> | <a href="README_jpn.md">🇯🇵 日本語</a> | <a href="README_por.md">🇵🇹 Português</a></p>

### Architecture, interfaces, socle de sécurité et la vérité sur ce qui est prouvé

<p align="center">
  <img src="https://img.shields.io/badge/License-GPL%203.0--or--later-blue.svg" alt="GPL 3.0 or later">
  <img src="https://img.shields.io/badge/Format-Markdown-083fa1.svg" alt="Format">
  <img src="https://img.shields.io/badge/Languages-8-00E5FF.svg" alt="Languages">
  <img src="https://img.shields.io/badge/Version-0.1.2-0f6cbd.svg" alt="Version">
  <img src="https://img.shields.io/badge/Maturity-scaffolding-FFB020.svg" alt="Maturity">
</p>

---

**Vérification d'honnêteté - ce qui fonctionne réellement aujourd'hui :** ce dépôt contient des documents et de petits outils. Les outils (le générateur du catalogue, celui de la marque, celui des README, la vérification de publication et la vérification de la famille) sont réels et ont des tests unitaires exécutés en CI ; le workflow nocturne les exécute sur les autres dépôts de la famille. Les documents sont écrits à partir des README, manifestes, journaux de modifications et documents de ces dépôts tels qu'ils ont été lus pour cette version, et une affirmation qui n'a pu être reliée à un dépôt est signalée comme telle. Rien ici n'est un test matériel : la matrice des capacités indique, pour chaque capacité, si elle a seulement été simulée, testée sur un ordinateur ou exécutée sur du matériel réel, et le dépôt du firmware indique qu'aucune carte assemblée n'existe encore.

---

> **État de la sûreté et de la cybersécurité :** cet écosystème n'est pas un système de sécurité certifié et aucune carte URTC assemblée n'existe encore. Les bootloaders contrôlent les images de firmware par CRC32 et un HMAC-SHA256 à clé partagée, pas par une signature asymétrique (prévue) ; les images d'application publiées sont signées avec la clé publique de développement (`signing_key_kind: dev`), si bien que n'importe qui peut produire une image acceptée par le bootloader ; rien n'a été transmis à une carte réelle. Lisez la [base de sécurité](docs/SECURITY_BASELINE.md) et le [modèle de menaces](docs/THREAT_MODEL.md) avant de vous fier à une affirmation d'ici pour la sécurité d'une personne.

## 📋 En un coup d'œil

| | |
|---|---|
| Version | `0.1.2` |
| Maturité | Ébauche |
| Tests | 153 |
| Technologie | Markdown / Mermaid / Python / SVG |
| Cible | Le PC de la personne qui l'utilise |
| Sur matériel réel | Sans objet : rien ici ne s'exécute sur du matériel |

**Aller à :** [Présentation](#-présentation) · [Architecture](#-architecture) · [Démarrage rapide](#-démarrage-rapide) · [Tests](#-tests) · [Structure](#-structure-du-dépôt) · [Liés](#-projets-liés)

## 🚦 État du projet

🟢 fait et vérifié · 🟡 fonctionne, avec des limites connues · 🟠 à moitié fait ou non vérifié · 🔴 non fait ou non fonctionnel. Rien n'est vert si cela n'a jamais tourné sur du vrai matériel.

| Partie | État | Ce que le dépôt peut démontrer |
| --- | :---: | --- |
| Logiciel | 🟡 | Les générateurs du catalogue, de la marque et des README, et les vérifications de la publication, des affirmations et de la famille, tournent sur un ordinateur ; aucun matériel impliqué. |
| Tests | 🟢 | La suite de tests passe dans la CI, sous Linux et sous Windows, à chaque push. |
| Vérifications sur toute la famille | 🟡 | L'exécution de nuit récupère chaque dépôt de la famille et compare leurs tableaux de synthèse, leurs affirmations et la structure du catalogue ; une version périmée dans le catalogue est signalée mais ne fait pas échouer la nuit. |
| Documents de sécurité | 🟡 | La base de sécurité et le modèle de menaces sont écrits à partir des autres dépôts tels qu'ils ont été lus ; personne en dehors du projet ne les a relus. |
| Documentation | 🟡 | README en huit langues et documents de référence ; les traductions n'ont pas été relues par des locuteurs natifs. |

## 🎯 Présentation

<p align="center">
  <img src="images/URTC_ECOSYSTEM.svg" alt="URTC ecosystem" width="100%">
</p>

L'image ci-dessous montre les dépôts d'URTC, le bus CAN qui relie les cartes et les outils du poste, et les liens qu'affirment leurs documents.

* [Architecture](docs/ARCHITECTURE.md): couches, flux de données, ports et frontières de confiance.
* [Interfaces](docs/INTERFACES.md): qui possède chaque contrat et où il est documenté.
* [Matrice des capacités](docs/CAPABILITY_MATRIX.md): ce qui est prouvé en logiciel et ce qui exige du matériel, projet par projet.
* [Socle de sécurité](docs/SECURITY_BASELINE.md): ce que le code impose et ce qui manque encore ; et le [modèle de menaces](docs/THREAT_MODEL.md).
* [Première tranche verticale](docs/FIRST_VERTICAL_SLICE.md): le plus petit chemin de bout en bout qui existe aujourd'hui.
* [Duplication du protocole CAN](docs/CAN_PROTOCOL_DUPLICATION.md): le protocole est implémenté trois fois à partir d'un texte ; ce que contiendrait une spécification partagée.
* [Catalogue des projets](docs/PROJECT_CATALOG.md): chaque dépôt de l'écosystème, écrit à partir de son propre manifeste.
* **Outils :** `make_catalog.py` écrit le catalogue, `make_brand.py` la bannière, l'icône et la carte des familles, `make_readmes.py` les huit README de ce dépôt, `publication_check.py` cherche tout ce qui serait privé avant une publication, et `check_all.sh` lance les vérifications propres à chaque dépôt de la famille et affiche une ligne PASS, FAIL ou SKIP pour chacun. `make_glance.py` écrit le tableau En un coup d'œil de chaque dépôt à partir de son manifeste et de `data/glance.json` (`--check` compare, `--apply` écrit) ; après un changement de version, `python tools/make_glance.py --apply --repo NOM` met à jour le tableau de ce dépôt. `check_claims.py` lit le README anglais de chaque dépôt de la famille et échoue lorsqu'une phrase contient un mot à risque (E-STOP, verrouillage, temps réel, signé, mTLS, FDCAN, YOLO, piloté par IA, autonome, certifié, ...) sans marqueur d'état à côté (prévu, non implémenté, optionnel, désactivé par défaut, simulé, testé, ...), sauf si une personne a lu cette ligne à côté du code et l'a inscrite dans `data/claims_reviewed.json`. `check_repo_tools.py` compare les fichiers que chaque dépôt porte comme la même copie (les contrôles de politique de documentation et de parité des README, l'outil de montée de version du manifeste, le workflow d'avis au tableau de bord) et échoue lorsqu'un fichier diffère. `sync_repo_tools.py` écrit la copie canonique de ces fichiers (`template/eh3d-repo-template`) dans chaque dépôt en conservant les fins de ligne de chaque fichier ; sans `--apply` il liste seulement ce qui changerait. `urtc_doctor.py` est le point d'entrée unique : un rapport sur les outils de la machine (Python, git, Node, le compilateur ARM, PySide6, ports série), les versions de chaque dépôt (manifeste, fichier source et dernière entrée du changelog), les copies d'URTC-COMMON et le firmware embarqué par le flasher et le web studio, la validation de chaque dépôt et les vérifications de celui-ci ; `--fast` omet les validations et `--online` compare le firmware embarqué avec la dernière release.

## 🧩 Rôle dans URTC

URTC-DOCS est la mémoire de l'écosystème : l'endroit où vivent l'architecture, les interfaces, le socle de sécurité et la matrice des capacités, et où sont gardés les outils qui comparent tous les dépôts côte à côte. Chaque dépôt garde son propre README, ses tests et son contrat ; celui-ci dit comment ils s'assemblent et ce qui a réellement été prouvé.

## 🏛️ Architecture

<p align="center">
  <img src="images/architecture.svg" alt="Architecture d'URTC-DOCS : ce qu'il lit, ce qu'il contient et ce qu'il alimente" width="100%">
</p>

Comment les parties de ce dépôt s'articulent. L'image est dessinée à partir de `docs/architecture.json` et vérifiée par rapport au code.

## 🚀 Démarrage rapide

**Prérequis :** Python 3.10 ou plus récent ; pytest pour les tests

```bash
python tools/make_catalog.py --check                 # le catalogue est à jour (nécessite les dépôts à côté de celui-ci)
python tools/make_brand.py --check                   # la bannière, l'icône et la carte sont à jour
python tools/make_readmes.py --check                 # les huit README sont à jour
python tools/make_glance.py --check                  # les tableaux En un coup d'œil de la famille sont à jour (nécessite les dépôts à côté de celui-ci)
python tools/publication_check.py                    # rien de privé ne partirait avec une publication
python tools/check_claims.py --require-siblings      # aucun README n'affirme une capacité risquée sans son statut (nécessite les dépôts à côté de celui-ci)
python tools/check_repo_tools.py --require-siblings  # les fichiers que chaque dépôt porte comme la même copie sont identiques (nécessite les dépôts à côté de celui-ci)
bash tools/check_all.sh                              # les vérifications de chaque dépôt, une ligne chacun
python tools/urtc_doctor.py                          # le doctor : un rapport sur cette machine et sur chaque dépôt
python -m pytest tests -q                            # les tests unitaires des outils
```

## 🧪 Tests

La suite compte 153 tests (`python -m pytest tests -q`). Ils exécutent sur des jeux d'essai les générateurs du catalogue, de la marque, des tableaux En un coup d'œil, des tableaux d'état et des README, les contrôles des affirmations, des fichiers partagés, de la publication et le doctor, les vecteurs de conformité des notes CAN, et vérifient que les README de ce dépôt sont exactement ce qu'écrit le générateur.

## 🏗️ Compilation et publication

`build.sh` / `build.bat` installent le paquet et lancent les tests, et `build-test.sh` / `build-test.bat` vérifient sans installer ; aucun ne change de version.

## 📂 Structure du dépôt

<p align="center">
  <img src="images/repository-structure.svg" alt="Structure du dépôt URTC-DOCS" width="100%">
</p>

<details>
<summary>Version texte de l'arborescence</summary>

```text
URTC-DOCS/
├── docs/                                              architecture, interfaces, matrice des capacités, socle de sécurité, modèle de menaces et catalogue généré
├── src/urtc_docs/                                     les outils sous forme de paquet : catalogue, marque, README, En un coup d'œil, état, contrôles
├── tools/                                             scripts légers au-dessus du paquet, check_all.sh et les contrôles de CI partagés
├── data/                                              les chiffres d'En un coup d'œil et les affirmations relues
├── template/                                          la copie canonique des fichiers que partagent tous les dépôts
├── tests/                                             tests unitaires des outils
├── brand/                                             l'icône
├── images/                                            bannière et images de ce README
├── .github/                                           workflow de CI et modèles d'issues et de pull requests
├── build.sh build.bat                                 scripts de compilation
├── build-test.sh build-test.bat                       scripts de compilation et de test qui ne changent rien dans le dépôt
├── test.sh test.bat                                   lancent les tests
├── run.sh run.bat                                     lancent le programme
├── urtc.project.json                                  manifeste : version, rôle, maturité et commande de compilation
├── CHANGELOG.md                                       ce qui a changé à chaque version
├── SECURITY.md SUPPORT.md                             politique de sécurité et assistance
├── CONTRIBUTING.md CODE_OF_CONDUCT.md                 comment contribuer et code de conduite
├── .gitattributes .gitignore                          réglages Git
├── bump.py bump_version.py bump_manifest_version.py   scripts qui augmentent la version
├── LICENSE LICENSE.md                                 licence du logiciel et de la documentation
└── pyproject.toml requirements-dev.lock ruff.toml     paquet, outils figés et réglages de lint
```

</details>

## 🗺️ Feuille de route et limites connues

**Limites connues aujourd'hui**

* Le socle de sécurité et le modèle de menaces sont écrits à partir des autres dépôts tels qu'ils ont été lus ; personne en dehors du projet ne les a relus.
* L'exécution de nuit récupère chaque dépôt de la famille et compare leurs tableaux de synthèse, leurs affirmations et la structure du catalogue ; une version périmée dans le catalogue est signalée mais ne fait pas échouer la nuit.
* Les documents décrivent du logiciel ; aucun matériel n'intervient et aucune affirmation sur des cartes n'a été vérifiée sur une carte.

**Ensuite**

* Tenir à jour le catalogue, les tableaux En un coup d'œil et la matrice des capacités à mesure que les dépôts changent.

## 🌍 Langues

Le README et les textes existent en anglais, espagnol, français, italien, allemand, chinois, japonais et portugais européen.

## 🔗 Projets liés

URTC est fait de dépôts indépendants, chacun avec sa version, ses tests et son README. Voici la famille, par groupes :

* **URTC Tool Platform:**
  * [URTC](https://github.com/JuanenRac/URTC) - firmware de la carte de la tête d'outil (25 profils d'outil, bootloader CAN) et référence du protocole CAN.
  * [URTC-COMMON](https://github.com/JuanenRac/URTC-COMMON) - le protocole CAN écrit une seule fois comme données (spécification, tables générées, vecteurs de conformité) et le code que les programmes partagent.
  * [URTC-FLASHER](https://github.com/JuanenRac/URTC-FLASHER) - outil de bureau qui met à jour le firmware de la carte par CAN ou par SWD/JTAG.
  * [URTC-GATEWAY](https://github.com/JuanenRac/URTC-GATEWAY) - passerelle devant le bus CAN : ne laisse passer que les identifiants d'une liste, limite leur cadence et demande une clé de session.
  * [URTC-SMART-RACK](https://github.com/JuanenRac/URTC-SMART-RACK) - logique C indépendante du matériel et protocole de commandes pour un support d'outils avec préchauffage et suivi du cycle de vie.
  * [URTC-TESTER](https://github.com/JuanenRac/URTC-TESTER) - testeur de bureau du bus CAN en direct qui affiche les commandes et la télémétrie du profil d'outil signalé par une carte.
  * [URTC-VISION-TOOL](https://github.com/JuanenRac/URTC-VISION-TOOL) - protocole de trames de capteur en C et compagnon Python thermique/RVB pour une tête d'outil d'inspection.
  * [URTC-WEB-STUDIO](https://github.com/JuanenRac/URTC-WEB-STUDIO) - application de navigateur qui flashe et teste la carte via Web Serial et SLCAN, sans rien installer.
* **Ecosystem Operations:**
  * **URTC-DOCS** (ce dépôt) - architecture, interfaces, base de sécurité et catalogue généré de l'écosystème, plus les outils qui comparent tous les dépôts.
  * [URTC-UPDATER](https://github.com/JuanenRac/URTC-UPDATER) - outil de bureau qui détecte, installe et met à jour les dépôts de la famille URTC, une action explicite à la fois.

**Projets frères (indépendants, avec la même base et les mêmes outils) :**

* **[HYDRA-UMC-DOCS](https://github.com/JuanenRac/HYDRA-UMC-DOCS)** - projet frère : le centre de documentation de HYDRA-UMC, un écosystème indépendant qui partage la base et les outils de celui-ci
* **[ARMOR-DOCS](https://github.com/JuanenRac/ARMOR-DOCS)** - projet frère : le centre de documentation d'A.R.M.O.R., l'écosystème de sécurité, lui aussi indépendant et construit sur la même base
* **[JuanenRac](https://github.com/JuanenRac/JuanenRac)** - le profil et le tableau d'état de tous les écosystèmes

## 📚 Documentation

Pour en savoir plus :

* [Matrice des capacités : ce qui est prouvé et ce qui ne l'est pas](docs/CAPABILITY_MATRIX.md)
* [Catalogue des projets : versions et types des dépôts](docs/PROJECT_CATALOG.md)
* [Protocole CAN : trois implémentations d'une spécification en prose](docs/CAN_PROTOCOL_DUPLICATION.md)
* [Journal des modifications de ce dépôt](CHANGELOG.md)
* [Licence (GPL-3.0-or-later)](LICENSE)

## 🤝 Contribuer et communauté

* Avant une pull request, lancez `URTC_CI=1 python tools/ci_validate.py` : il doit réussir. Voir [CONTRIBUTING.md](CONTRIBUTING.md) et le [code de conduite](CODE_OF_CONDUCT.md).
* Le README existe en huit langues : une modification du texte se fait dans les huit fichiers, et les sections partagées avec d'autres dépôts sont écrites par `tools/readme_sections.py` d'URTC-COMMON.
* Ne décrivez pas comme fonctionnant sur une carte ce qui a seulement été compilé.
* Signalez une vulnérabilité en privé : [SECURITY.md](SECURITY.md). Questions, idées et rapports : electrohobby3d@gmail.com ([SUPPORT.md](SUPPORT.md)).
* Questions, idées et rapports : electrohobby3d@gmail.com

## 👤 AUTEUR

**JuanenRac (Electro Hobby 3D)** · electrohobby3d@gmail.com

## 📜 LICENCE

Logiciel : GPL-3.0-or-later - voir [LICENSE](LICENSE). Documentation : CC BY-SA 4.0 - voir [LICENSE.md](LICENSE.md).
