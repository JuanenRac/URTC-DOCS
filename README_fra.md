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
  <img src="https://img.shields.io/badge/Version-0.0.2-0f6cbd.svg" alt="Version">
  <img src="https://img.shields.io/badge/Maturity-scaffolding-FFB020.svg" alt="Maturity">
</p>

---

**Vérification d'honnêteté - ce qui fonctionne réellement aujourd'hui :** ce dépôt contient des documents et de petits outils. Les outils (le générateur du catalogue, celui de la marque, celui des README, la vérification de publication et la vérification de la famille) sont réels et ont des tests unitaires exécutés en CI ; le workflow nocturne les exécute sur les autres dépôts de la famille. Les documents sont écrits à partir des README, manifestes, journaux de modifications et documents de ces dépôts tels qu'ils ont été lus pour cette version, et une affirmation qui n'a pu être reliée à un dépôt est signalée comme telle. Rien ici n'est un test matériel : la matrice des capacités indique, pour chaque capacité, si elle a seulement été simulée, testée sur un ordinateur ou exécutée sur du matériel réel, et le dépôt du firmware indique qu'aucune carte assemblée n'existe encore.

---

## 📋 En un coup d'œil

| | |
|---|---|
| Version | `0.0.2` |
| Maturité | Ébauche |
| Technologie | Markdown / Mermaid / Python / SVG |
| Cible | Le PC de la personne qui l'utilise |
| Sur matériel réel | Sans objet : rien ici ne s'exécute sur du matériel |

## 🎯 Vue d'ensemble

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
* **Outils :** `make_catalog.py` écrit le catalogue, `make_brand.py` la bannière, l'icône et la carte des familles, `make_readmes.py` les huit README de ce dépôt, `publication_check.py` cherche tout ce qui serait privé avant une publication, et `check_all.sh` lance les vérifications propres à chaque dépôt de la famille et affiche une ligne PASS, FAIL ou SKIP pour chacun. `make_glance.py` écrit le tableau En un coup d'œil de chaque dépôt à partir de son manifeste et de `data/glance.json` (`--check` compare, `--apply` écrit) ; après un changement de version, `python tools/make_glance.py --apply --repo NOM` met à jour le tableau de ce dépôt.

## 🧩 Rôle dans URTC

URTC-DOCS est la mémoire de l'écosystème : l'endroit où vivent l'architecture, les interfaces, le socle de sécurité et la matrice des capacités, et où sont gardés les outils qui comparent tous les dépôts côte à côte. Chaque dépôt garde son propre README, ses tests et son contrat ; celui-ci dit comment ils s'assemblent et ce qui a réellement été prouvé.

## 📂 Structure du dépôt

```text
URTC-DOCS/
├── docs/     architecture, interfaces, matrice des capacités, socle de sécurité, modèle de menaces, première tranche, note sur le protocole CAN, catalogue généré
├── src/      les outils sous forme de paquet (catalogue, marque, README, vérification de publication)
├── tools/    scripts fins au-dessus du paquet, check_all.sh et les vérifications de CI partagées de l'écosystème
├── tests/    tests unitaires des outils
├── images/   bannière et carte de l'écosystème
├── brand/    l'icône
├── build.sh / build.bat, build-test.sh / build-test.bat, run.sh / run.bat
└── urtc.project.json, pyproject.toml, CHANGELOG.md, LICENSE, LICENSE.md
```

## 🛠️ COMPILATION ET EXÉCUTION

**Prérequis :** Python 3.10 ou plus récent ; pytest pour les tests

```bash
python tools/make_catalog.py --check  # le catalogue est à jour (nécessite les dépôts à côté de celui-ci)
python tools/make_brand.py --check    # la bannière, l'icône et la carte sont à jour
python tools/make_readmes.py --check  # les huit README sont à jour
python tools/make_glance.py --check   # les tableaux En un coup d'œil de la famille sont à jour (nécessite les dépôts à côté de celui-ci)
python tools/publication_check.py     # rien de privé ne partirait avec une publication
bash tools/check_all.sh               # les vérifications de chaque dépôt, une ligne chacun
python -m pytest tests -q             # les tests unitaires des outils
```

`build.sh` / `build.bat` avancent la version d'un cran (le compteur kilométrique de l'écosystème), installent le paquet et lancent les tests ; `build-test.sh` / `build-test.bat` vérifient sans changer aucune version.

## 🔗 Projets liés

URTC est fait de dépôts indépendants, chacun avec sa version, ses tests et son README. Voici la famille, par groupes :

* **URTC Tool Platform:** [URTC](https://github.com/JuanenRac/URTC), [URTC-FLASHER](https://github.com/JuanenRac/URTC-FLASHER), [URTC-SMART-RACK](https://github.com/JuanenRac/URTC-SMART-RACK), [URTC-TESTER](https://github.com/JuanenRac/URTC-TESTER), [URTC-VISION-TOOL](https://github.com/JuanenRac/URTC-VISION-TOOL), [URTC-WEB-STUDIO](https://github.com/JuanenRac/URTC-WEB-STUDIO)
* **Ecosystem Operations:** **URTC-DOCS** (ce dépôt), [URTC-UPDATER](https://github.com/JuanenRac/URTC-UPDATER)

**Au-delà de URTC :**

* **[HYDRA-UMC](https://github.com/JuanenRac/HYDRA-UMC)** - la carte mère du bras robotique, dont le relais CAN est documenté comme le bus sur lequel se branche la tête d'outil
* **[HYDRA-UMC-DOCS](https://github.com/JuanenRac/HYDRA-UMC-DOCS)** - la même idée pour l'écosystème HYDRA-UMC
* **[ARMOR-DOCS](https://github.com/JuanenRac/ARMOR-DOCS)** - la même idée pour l'écosystème de sécurité A.R.M.O.R.
* **[JuanenRac](https://github.com/JuanenRac/JuanenRac)** - le profil et le tableau d'état de tous les écosystèmes

## 📚 Documentation et communauté

Pour en savoir plus :

* [Matrice des capacités : ce qui est prouvé et ce qui ne l'est pas](docs/CAPABILITY_MATRIX.md)
* [Catalogue des projets : versions et types des dépôts](docs/PROJECT_CATALOG.md)
* [Protocole CAN : trois implémentations d'une spécification en prose](docs/CAN_PROTOCOL_DUPLICATION.md)
* [Journal des modifications de ce dépôt](CHANGELOG.md)
* [Licence (GPL-3.0-or-later)](LICENSE)
* Questions, idées et rapports : electrohobby3d@gmail.com

## 👤 AUTEUR

**JuanenRac (Electro Hobby 3D)** · electrohobby3d@gmail.com

## 📜 LICENCE

Logiciel : GPL-3.0-or-later - voir [LICENSE](LICENSE). Documentation : CC BY-SA 4.0 - voir [LICENSE.md](LICENSE.md).
