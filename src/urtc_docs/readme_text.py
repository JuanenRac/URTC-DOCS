# =============================================================================
# URTC-DOCS - src/urtc_docs/readme_text.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""The words of README.md and of its seven translations, one block per language.

Every language has exactly the same keys; the tests refuse a missing one. The
numbers (version, maturity) are not written here: they are read from the manifest.
"""
from __future__ import annotations

# code -> (file name, label shown in the language bar)
LANGUAGES: dict[str, tuple[str, str]] = {
    "en": ("README.md", "🇺🇸 English"),
    "es": ("README_spa.md", "🇪🇸 Español"),
    "fr": ("README_fra.md", "🇫🇷 Français"),
    "it": ("README_ita.md", "🇮🇹 Italiano"),
    "de": ("README_deu.md", "🇩🇪 Deutsch"),
    "zh": ("README_zho.md", "🇨🇳 简体中文"),
    "ja": ("README_jpn.md", "🇯🇵 日本語"),
    "pt": ("README_por.md", "🇵🇹 Português"),
}

TEXT: dict[str, dict[str, object]] = {
    "en": {
        "subtitle": "Architecture, interfaces, security baseline and the truth about what is proven",
        "honesty_label": "Honesty check - what actually runs today:",
        "honesty": "this repository holds documents and small tools. The tools (the catalogue generator, the brand generator, the README generator, the publication check and the family check) are real and have unit tests that run in CI; the nightly workflow runs them against the other repositories of the family. The documents are written from the READMEs, manifests, changelogs and documents of those repositories as they were read for this version, and a statement that could not be traced to a repository is marked as such. Nothing here is a hardware test: the capability matrix says, for each capability, whether it was only simulated, tested on a computer or run on real hardware, and the firmware repository states that no populated board exists yet.",
        "h_overview": "Overview",
        "overview_intro": "The picture below shows the repositories of URTC, the CAN bus that joins the boards and the host tools, and the links that their documents state.",
        "overview": [
            [
                "Architecture",
                "docs/ARCHITECTURE.md",
                "layers, data flows, ports and trust boundaries."
            ],
            [
                "Interfaces",
                "docs/INTERFACES.md",
                "who owns each contract and where it is documented."
            ],
            [
                "Capability matrix",
                "docs/CAPABILITY_MATRIX.md",
                "what is proven in software and what needs hardware, project by project."
            ],
            [
                "Security baseline",
                "docs/SECURITY_BASELINE.md",
                "what the code enforces and what is still missing; and the [threat model](docs/THREAT_MODEL.md)."
            ],
            [
                "First vertical slice",
                "docs/FIRST_VERTICAL_SLICE.md",
                "the smallest end-to-end path that exists today."
            ],
            [
                "CAN protocol duplication",
                "docs/CAN_PROTOCOL_DUPLICATION.md",
                "the protocol is implemented three times from prose; what a shared specification would hold."
            ],
            [
                "Project catalogue",
                "docs/PROJECT_CATALOG.md",
                "every repository of the ecosystem, written from its own manifest."
            ]
        ],
        "tools_label": "Tools:",
        "tools": "`make_catalog.py` writes the catalogue, `make_brand.py` the banner, icon and family map, `make_readmes.py` the eight READMEs of this repository, `publication_check.py` looks for anything private before a publication, and `check_all.sh` runs the own checks of every repository of the family and prints one PASS, FAIL or SKIP line each. `make_glance.py` writes the At a glance table of every repository from its manifest and from `data/glance.json` (`--check` compares, `--apply` writes); after a version bump, `python tools/make_glance.py --apply --repo NAME` refreshes the table of that repository.",
        "h_role": "Role in URTC",
        "role": "URTC-DOCS is the memory of the ecosystem: the place where the architecture, the interfaces, the security baseline and the capability matrix live, and where the tools that compare all the repositories side by side are kept. Each repository keeps its own README, tests and contract; this one says how they fit together and what has really been proven.",
        "h_structure": "Repository Structure",
        "tree": {
            "docs": "architecture, interfaces, capability matrix, security baseline, threat model, first slice, CAN protocol note, generated catalogue",
            "src": "the tools as a package (catalogue, brand, READMEs, publication check)",
            "tools": "thin scripts over the package, check_all.sh, and the shared CI checks of the ecosystem",
            "tests": "unit tests of the tools",
            "images": "banner and map of the ecosystem",
            "brand": "the icon",
            "data": "the data the generators read (the numbers of At a glance, the reviewed claims)",
            "template": "the canonical copy of the files every repository shares, and the tool that puts it in place"
        },
        "h_dev": "BUILD & RUN",
        "dev_requirements": "**Requirements:** Python 3.10 or newer; pytest for the tests",
        "dev_comments": ["the catalogue is current (needs the repositories next to this one)", "the banner, icon and map are current", "the eight READMEs are current", 'the At a glance tables of the family are current (needs the repositories next to this one)', "nothing private would leave with a publication", "the checks of every repository, one line each", "the unit tests of the tools"],
        "dev_note": "`build.sh` / `build.bat` install the package and run the tests, and `build-test.sh` / `build-test.bat` check without installing; neither changes a version. `python bump.py` raises the version by one step (the ecosystem's odometer).",
        "h_related": "Related Projects",
        "related_intro": "URTC is made of independent repositories, each with its own version, tests and README. This is the family, by group:",
        "related_this": "this repository",
        "related_beyond": "Beyond URTC:",
        "beyond": [
            [
                "HYDRA-UMC",
                "https://github.com/JuanenRac/HYDRA-UMC",
                "the robot-arm motherboard whose CAN relay is documented as the bus the tool head sits on"
            ],
            [
                "HYDRA-UMC-DOCS",
                "https://github.com/JuanenRac/HYDRA-UMC-DOCS",
                "the same idea for the HYDRA-UMC ecosystem"
            ],
            [
                "ARMOR-DOCS",
                "https://github.com/JuanenRac/ARMOR-DOCS",
                "the same idea for the A.R.M.O.R. security ecosystem"
            ],
            [
                "JuanenRac",
                "https://github.com/JuanenRac/JuanenRac",
                "the profile and the status dashboard of all the ecosystems"
            ]
        ],
        "h_docs": "Documentation & Community",
        "docs_intro": "Where to read more:",
        "docs_links": [
            [
                "Capability matrix: what is proven and what is not",
                "docs/CAPABILITY_MATRIX.md"
            ],
            [
                "Project catalogue: versions and kinds of the repositories",
                "docs/PROJECT_CATALOG.md"
            ],
            [
                "CAN protocol: three implementations of one prose specification",
                "docs/CAN_PROTOCOL_DUPLICATION.md"
            ],
            [
                "Changelog of this repository",
                "CHANGELOG.md"
            ],
            [
                "License (GPL-3.0-or-later)",
                "LICENSE"
            ]
        ],
        "docs_contact": "Questions, ideas and reports: electrohobby3d@gmail.com",
        "h_author": "AUTHOR",
        "h_license": "LICENSE",
        "license": "Software: GPL-3.0-or-later - see [LICENSE](LICENSE). Documentation: CC BY-SA 4.0 - see [LICENSE.md](LICENSE.md)."
    },
    "es": {
        "subtitle": "Arquitectura, interfaces, base de seguridad y la verdad sobre lo que está probado",
        "honesty_label": "Comprobación de honestidad - qué funciona hoy de verdad:",
        "honesty": "este repositorio contiene documentos y herramientas pequeñas. Las herramientas (el generador del catálogo, el de la marca, el de los README, la comprobación de publicación y la comprobación de la familia) son reales y tienen pruebas unitarias que se ejecutan en CI; el flujo nocturno las ejecuta contra los demás repositorios de la familia. Los documentos se han escrito a partir de los README, manifiestos, registros de cambios y documentos de esos repositorios tal como se leyeron para esta versión, y una afirmación que no se pudo rastrear hasta un repositorio queda señalada como tal. Nada de esto es una prueba de hardware: la matriz de capacidades dice, para cada capacidad, si solo se simuló, se probó en un ordenador o se ejecutó en hardware real, y el repositorio del firmware indica que todavía no existe ninguna placa montada.",
        "h_overview": "Descripción general",
        "overview_intro": "La imagen siguiente muestra los repositorios de URTC, el bus CAN que une las placas y las herramientas del ordenador, y los vínculos que afirman sus documentos.",
        "overview": [
            [
                "Arquitectura",
                "docs/ARCHITECTURE.md",
                "capas, flujos de datos, puertos y fronteras de confianza."
            ],
            [
                "Interfaces",
                "docs/INTERFACES.md",
                "quién es dueño de cada contrato y dónde está documentado."
            ],
            [
                "Matriz de capacidades",
                "docs/CAPABILITY_MATRIX.md",
                "qué está probado en software y qué necesita hardware, proyecto a proyecto."
            ],
            [
                "Base de seguridad",
                "docs/SECURITY_BASELINE.md",
                "lo que el código impone y lo que aún falta; y el [modelo de amenazas](docs/THREAT_MODEL.md)."
            ],
            [
                "Primer corte vertical",
                "docs/FIRST_VERTICAL_SLICE.md",
                "el camino de extremo a extremo más pequeño que existe hoy."
            ],
            [
                "Duplicación del protocolo CAN",
                "docs/CAN_PROTOCOL_DUPLICATION.md",
                "el protocolo está implementado tres veces a partir de prosa; qué contendría una especificación compartida."
            ],
            [
                "Catálogo de proyectos",
                "docs/PROJECT_CATALOG.md",
                "cada repositorio del ecosistema, escrito a partir de su propio manifiesto."
            ]
        ],
        "tools_label": "Herramientas:",
        "tools": "`make_catalog.py` escribe el catálogo, `make_brand.py` el banner, el icono y el mapa de familias, `make_readmes.py` los ocho README de este repositorio, `publication_check.py` busca cualquier cosa privada antes de una publicación y `check_all.sh` ejecuta las comprobaciones propias de cada repositorio de la familia e imprime una línea PASS, FAIL o SKIP por cada uno. `make_glance.py` escribe la tabla De un vistazo de cada repositorio a partir de su manifiesto y de `data/glance.json` (`--check` compara, `--apply` escribe); tras subir una versión, `python tools/make_glance.py --apply --repo NOMBRE` actualiza la tabla de ese repositorio.",
        "h_role": "Papel en URTC",
        "role": "URTC-DOCS es la memoria del ecosistema: el lugar donde viven la arquitectura, las interfaces, la base de seguridad y la matriz de capacidades, y donde se guardan las herramientas que comparan todos los repositorios entre sí. Cada repositorio conserva su propio README, sus pruebas y su contrato; este explica cómo encajan y qué se ha probado de verdad.",
        "h_structure": "Estructura del repositorio",
        "tree": {
            "docs": "arquitectura, interfaces, matriz de capacidades, base de seguridad, modelo de amenazas, primer corte, nota del protocolo CAN, catálogo generado",
            "src": "las herramientas como paquete (catálogo, marca, README, comprobación de publicación)",
            "tools": "scripts finos sobre el paquete, check_all.sh y las comprobaciones de CI compartidas del ecosistema",
            "tests": "pruebas unitarias de las herramientas",
            "images": "banner y mapa del ecosistema",
            "brand": "el icono",
            "data": "los datos que leen los generadores (las cifras de De un vistazo, las afirmaciones revisadas)",
            "template": "la copia canónica de los archivos que comparten todos los repositorios y la herramienta que la coloca"
        },
        "h_dev": "COMPILACIÓN Y EJECUCIÓN",
        "dev_requirements": "**Requisitos:** Python 3.10 o superior; pytest para las pruebas",
        "dev_comments": ["el catálogo está al día (necesita los repositorios junto a este)", "el banner, el icono y el mapa están al día", "los ocho README están al día", 'las tablas De un vistazo de la familia están al día (necesita los repositorios junto a este)', "nada privado saldría con una publicación", "las comprobaciones de cada repositorio, una línea por cada uno", "las pruebas unitarias de las herramientas"],
        "dev_note": "`build.sh` / `build.bat` instalan el paquete y ejecutan las pruebas, y `build-test.sh` / `build-test.bat` comprueban sin instalar; ninguno cambia una versión. `python bump.py` sube la versión un paso (el cuentakilómetros del ecosistema).",
        "h_related": "Proyectos relacionados",
        "related_intro": "URTC se compone de repositorios independientes, cada uno con su versión, sus pruebas y su README. Esta es la familia, por grupos:",
        "related_this": "este repositorio",
        "related_beyond": "Más allá de URTC:",
        "beyond": [
            [
                "HYDRA-UMC",
                "https://github.com/JuanenRac/HYDRA-UMC",
                "la placa base del brazo robótico, cuyo relé CAN está documentado como el bus en el que se conecta la cabeza de herramienta"
            ],
            [
                "HYDRA-UMC-DOCS",
                "https://github.com/JuanenRac/HYDRA-UMC-DOCS",
                "la misma idea para el ecosistema HYDRA-UMC"
            ],
            [
                "ARMOR-DOCS",
                "https://github.com/JuanenRac/ARMOR-DOCS",
                "la misma idea para el ecosistema de seguridad A.R.M.O.R."
            ],
            [
                "JuanenRac",
                "https://github.com/JuanenRac/JuanenRac",
                "el perfil y el panel de estado de todos los ecosistemas"
            ]
        ],
        "h_docs": "Documentación y comunidad",
        "docs_intro": "Dónde leer más:",
        "docs_links": [
            [
                "Matriz de capacidades: qué está probado y qué no",
                "docs/CAPABILITY_MATRIX.md"
            ],
            [
                "Catálogo de proyectos: versiones y tipos de los repositorios",
                "docs/PROJECT_CATALOG.md"
            ],
            [
                "Protocolo CAN: tres implementaciones de una especificación en prosa",
                "docs/CAN_PROTOCOL_DUPLICATION.md"
            ],
            [
                "Registro de cambios de este repositorio",
                "CHANGELOG.md"
            ],
            [
                "Licencia (GPL-3.0-or-later)",
                "LICENSE"
            ]
        ],
        "docs_contact": "Preguntas, ideas e informes: electrohobby3d@gmail.com",
        "h_author": "AUTOR",
        "h_license": "LICENCIA",
        "license": "Software: GPL-3.0-or-later - véase [LICENSE](LICENSE). Documentación: CC BY-SA 4.0 - véase [LICENSE.md](LICENSE.md)."
    },
    "fr": {
        "subtitle": "Architecture, interfaces, socle de sécurité et la vérité sur ce qui est prouvé",
        "honesty_label": "Vérification d'honnêteté - ce qui fonctionne réellement aujourd'hui :",
        "honesty": "ce dépôt contient des documents et de petits outils. Les outils (le générateur du catalogue, celui de la marque, celui des README, la vérification de publication et la vérification de la famille) sont réels et ont des tests unitaires exécutés en CI ; le workflow nocturne les exécute sur les autres dépôts de la famille. Les documents sont écrits à partir des README, manifestes, journaux de modifications et documents de ces dépôts tels qu'ils ont été lus pour cette version, et une affirmation qui n'a pu être reliée à un dépôt est signalée comme telle. Rien ici n'est un test matériel : la matrice des capacités indique, pour chaque capacité, si elle a seulement été simulée, testée sur un ordinateur ou exécutée sur du matériel réel, et le dépôt du firmware indique qu'aucune carte assemblée n'existe encore.",
        "h_overview": "Vue d'ensemble",
        "overview_intro": "L'image ci-dessous montre les dépôts d'URTC, le bus CAN qui relie les cartes et les outils du poste, et les liens qu'affirment leurs documents.",
        "overview": [
            [
                "Architecture",
                "docs/ARCHITECTURE.md",
                "couches, flux de données, ports et frontières de confiance."
            ],
            [
                "Interfaces",
                "docs/INTERFACES.md",
                "qui possède chaque contrat et où il est documenté."
            ],
            [
                "Matrice des capacités",
                "docs/CAPABILITY_MATRIX.md",
                "ce qui est prouvé en logiciel et ce qui exige du matériel, projet par projet."
            ],
            [
                "Socle de sécurité",
                "docs/SECURITY_BASELINE.md",
                "ce que le code impose et ce qui manque encore ; et le [modèle de menaces](docs/THREAT_MODEL.md)."
            ],
            [
                "Première tranche verticale",
                "docs/FIRST_VERTICAL_SLICE.md",
                "le plus petit chemin de bout en bout qui existe aujourd'hui."
            ],
            [
                "Duplication du protocole CAN",
                "docs/CAN_PROTOCOL_DUPLICATION.md",
                "le protocole est implémenté trois fois à partir d'un texte ; ce que contiendrait une spécification partagée."
            ],
            [
                "Catalogue des projets",
                "docs/PROJECT_CATALOG.md",
                "chaque dépôt de l'écosystème, écrit à partir de son propre manifeste."
            ]
        ],
        "tools_label": "Outils :",
        "tools": "`make_catalog.py` écrit le catalogue, `make_brand.py` la bannière, l'icône et la carte des familles, `make_readmes.py` les huit README de ce dépôt, `publication_check.py` cherche tout ce qui serait privé avant une publication, et `check_all.sh` lance les vérifications propres à chaque dépôt de la famille et affiche une ligne PASS, FAIL ou SKIP pour chacun. `make_glance.py` écrit le tableau En un coup d'œil de chaque dépôt à partir de son manifeste et de `data/glance.json` (`--check` compare, `--apply` écrit) ; après un changement de version, `python tools/make_glance.py --apply --repo NOM` met à jour le tableau de ce dépôt.",
        "h_role": "Rôle dans URTC",
        "role": "URTC-DOCS est la mémoire de l'écosystème : l'endroit où vivent l'architecture, les interfaces, le socle de sécurité et la matrice des capacités, et où sont gardés les outils qui comparent tous les dépôts côte à côte. Chaque dépôt garde son propre README, ses tests et son contrat ; celui-ci dit comment ils s'assemblent et ce qui a réellement été prouvé.",
        "h_structure": "Structure du dépôt",
        "tree": {
            "docs": "architecture, interfaces, matrice des capacités, socle de sécurité, modèle de menaces, première tranche, note sur le protocole CAN, catalogue généré",
            "src": "les outils sous forme de paquet (catalogue, marque, README, vérification de publication)",
            "tools": "scripts fins au-dessus du paquet, check_all.sh et les vérifications de CI partagées de l'écosystème",
            "tests": "tests unitaires des outils",
            "images": "bannière et carte de l'écosystème",
            "brand": "l'icône",
            "data": "les données lues par les générateurs (les chiffres de En un coup d'œil, les affirmations relues)",
            "template": "la copie de référence des fichiers que partagent tous les dépôts et l'outil qui la met en place"
        },
        "h_dev": "COMPILATION ET EXÉCUTION",
        "dev_requirements": "**Prérequis :** Python 3.10 ou plus récent ; pytest pour les tests",
        "dev_comments": ["le catalogue est à jour (nécessite les dépôts à côté de celui-ci)", "la bannière, l'icône et la carte sont à jour", "les huit README sont à jour", "les tableaux En un coup d'œil de la famille sont à jour (nécessite les dépôts à côté de celui-ci)", "rien de privé ne partirait avec une publication", "les vérifications de chaque dépôt, une ligne chacun", "les tests unitaires des outils"],
        "dev_note": "`build.sh` / `build.bat` installent le paquet et lancent les tests, et `build-test.sh` / `build-test.bat` vérifient sans installer ; aucun ne change de version. `python bump.py` avance la version d'un cran (le compteur kilométrique de l'écosystème).",
        "h_related": "Projets liés",
        "related_intro": "URTC est fait de dépôts indépendants, chacun avec sa version, ses tests et son README. Voici la famille, par groupes :",
        "related_this": "ce dépôt",
        "related_beyond": "Au-delà de URTC :",
        "beyond": [
            [
                "HYDRA-UMC",
                "https://github.com/JuanenRac/HYDRA-UMC",
                "la carte mère du bras robotique, dont le relais CAN est documenté comme le bus sur lequel se branche la tête d'outil"
            ],
            [
                "HYDRA-UMC-DOCS",
                "https://github.com/JuanenRac/HYDRA-UMC-DOCS",
                "la même idée pour l'écosystème HYDRA-UMC"
            ],
            [
                "ARMOR-DOCS",
                "https://github.com/JuanenRac/ARMOR-DOCS",
                "la même idée pour l'écosystème de sécurité A.R.M.O.R."
            ],
            [
                "JuanenRac",
                "https://github.com/JuanenRac/JuanenRac",
                "le profil et le tableau d'état de tous les écosystèmes"
            ]
        ],
        "h_docs": "Documentation et communauté",
        "docs_intro": "Pour en savoir plus :",
        "docs_links": [
            [
                "Matrice des capacités : ce qui est prouvé et ce qui ne l'est pas",
                "docs/CAPABILITY_MATRIX.md"
            ],
            [
                "Catalogue des projets : versions et types des dépôts",
                "docs/PROJECT_CATALOG.md"
            ],
            [
                "Protocole CAN : trois implémentations d'une spécification en prose",
                "docs/CAN_PROTOCOL_DUPLICATION.md"
            ],
            [
                "Journal des modifications de ce dépôt",
                "CHANGELOG.md"
            ],
            [
                "Licence (GPL-3.0-or-later)",
                "LICENSE"
            ]
        ],
        "docs_contact": "Questions, idées et rapports : electrohobby3d@gmail.com",
        "h_author": "AUTEUR",
        "h_license": "LICENCE",
        "license": "Logiciel : GPL-3.0-or-later - voir [LICENSE](LICENSE). Documentation : CC BY-SA 4.0 - voir [LICENSE.md](LICENSE.md)."
    },
    "it": {
        "subtitle": "Architettura, interfacce, base di sicurezza e la verità su ciò che è provato",
        "honesty_label": "Verifica di onestà - cosa funziona davvero oggi:",
        "honesty": "questo repository contiene documenti e piccoli strumenti. Gli strumenti (il generatore del catalogo, quello del marchio, quello dei README, il controllo di pubblicazione e il controllo della famiglia) sono reali e hanno test unitari eseguiti in CI; il workflow notturno li esegue sugli altri repository della famiglia. I documenti sono scritti a partire dai README, manifesti, registri delle modifiche e documenti di quei repository così come sono stati letti per questa versione, e un'affermazione che non si è potuta ricondurre a un repository è segnalata come tale. Nulla qui è un test hardware: la matrice delle capacità dice, per ogni capacità, se è stata solo simulata, provata su un computer o eseguita su hardware reale, e il repository del firmware dichiara che non esiste ancora alcuna scheda assemblata.",
        "h_overview": "Panoramica",
        "overview_intro": "L'immagine qui sotto mostra i repository di URTC, il bus CAN che collega le schede e gli strumenti del computer, e i collegamenti che i loro documenti affermano.",
        "overview": [
            [
                "Architettura",
                "docs/ARCHITECTURE.md",
                "livelli, flussi di dati, porte e confini di fiducia."
            ],
            [
                "Interfacce",
                "docs/INTERFACES.md",
                "chi possiede ogni contratto e dove è documentato."
            ],
            [
                "Matrice delle capacità",
                "docs/CAPABILITY_MATRIX.md",
                "cosa è provato in software e cosa richiede hardware, progetto per progetto."
            ],
            [
                "Base di sicurezza",
                "docs/SECURITY_BASELINE.md",
                "cosa il codice impone e cosa manca ancora; e il [modello delle minacce](docs/THREAT_MODEL.md)."
            ],
            [
                "Prima fetta verticale",
                "docs/FIRST_VERTICAL_SLICE.md",
                "il più piccolo percorso da un capo all'altro che esiste oggi."
            ],
            [
                "Duplicazione del protocollo CAN",
                "docs/CAN_PROTOCOL_DUPLICATION.md",
                "il protocollo è implementato tre volte a partire da un testo; cosa conterrebbe una specifica condivisa."
            ],
            [
                "Catalogo dei progetti",
                "docs/PROJECT_CATALOG.md",
                "ogni repository dell'ecosistema, scritto a partire dal proprio manifesto."
            ]
        ],
        "tools_label": "Strumenti:",
        "tools": "`make_catalog.py` scrive il catalogo, `make_brand.py` il banner, l'icona e la mappa delle famiglie, `make_readmes.py` gli otto README di questo repository, `publication_check.py` cerca qualsiasi cosa privata prima di una pubblicazione e `check_all.sh` esegue i controlli propri di ogni repository della famiglia e stampa una riga PASS, FAIL o SKIP per ciascuno. `make_glance.py` scrive la tabella In breve di ogni repository dal suo manifesto e da `data/glance.json` (`--check` confronta, `--apply` scrive); dopo un aumento di versione, `python tools/make_glance.py --apply --repo NOME` aggiorna la tabella di quel repository.",
        "h_role": "Ruolo in URTC",
        "role": "URTC-DOCS è la memoria dell'ecosistema: il luogo in cui vivono l'architettura, le interfacce, la base di sicurezza e la matrice delle capacità, e dove si conservano gli strumenti che confrontano tutti i repository fianco a fianco. Ogni repository conserva il proprio README, i propri test e il proprio contratto; questo dice come si incastrano e cosa è stato davvero provato.",
        "h_structure": "Struttura del repository",
        "tree": {
            "docs": "architettura, interfacce, matrice delle capacità, base di sicurezza, modello delle minacce, prima fetta, nota sul protocollo CAN, catalogo generato",
            "src": "gli strumenti come pacchetto (catalogo, marchio, README, controllo di pubblicazione)",
            "tools": "script sottili sopra il pacchetto, check_all.sh e i controlli CI condivisi dell'ecosistema",
            "tests": "test unitari degli strumenti",
            "images": "banner e mappa dell'ecosistema",
            "brand": "l'icona",
            "data": "i dati letti dai generatori (le cifre di In breve, le affermazioni riviste)",
            "template": "la copia di riferimento dei file condivisi da tutti i repository e lo strumento che la installa"
        },
        "h_dev": "COMPILAZIONE ED ESECUZIONE",
        "dev_requirements": "**Requisiti:** Python 3.10 o successivo; pytest per i test",
        "dev_comments": ["il catalogo è aggiornato (servono i repository accanto a questo)", "il banner, l'icona e la mappa sono aggiornati", "gli otto README sono aggiornati", 'le tabelle In breve della famiglia sono aggiornate (servono i repository accanto a questo)', "nulla di privato uscirebbe con una pubblicazione", "i controlli di ogni repository, una riga ciascuno", "i test unitari degli strumenti"],
        "dev_note": "`build.sh` / `build.bat` installano il pacchetto ed eseguono i test, e `build-test.sh` / `build-test.bat` controllano senza installare; nessuno cambia una versione. `python bump.py` alza la versione di un passo (il contachilometri dell'ecosistema).",
        "h_related": "Progetti correlati",
        "related_intro": "URTC è fatto di repository indipendenti, ciascuno con la propria versione, i propri test e il proprio README. Ecco la famiglia, per gruppi:",
        "related_this": "questo repository",
        "related_beyond": "Oltre URTC:",
        "beyond": [
            [
                "HYDRA-UMC",
                "https://github.com/JuanenRac/HYDRA-UMC",
                "la scheda madre del braccio robotico, il cui relay CAN è documentato come il bus a cui si collega la testa utensile"
            ],
            [
                "HYDRA-UMC-DOCS",
                "https://github.com/JuanenRac/HYDRA-UMC-DOCS",
                "la stessa idea per l'ecosistema HYDRA-UMC"
            ],
            [
                "ARMOR-DOCS",
                "https://github.com/JuanenRac/ARMOR-DOCS",
                "la stessa idea per l'ecosistema di sicurezza A.R.M.O.R."
            ],
            [
                "JuanenRac",
                "https://github.com/JuanenRac/JuanenRac",
                "il profilo e il pannello di stato di tutti gli ecosistemi"
            ]
        ],
        "h_docs": "Documentazione e comunità",
        "docs_intro": "Dove leggere di più:",
        "docs_links": [
            [
                "Matrice delle capacità: cosa è provato e cosa no",
                "docs/CAPABILITY_MATRIX.md"
            ],
            [
                "Catalogo dei progetti: versioni e tipi dei repository",
                "docs/PROJECT_CATALOG.md"
            ],
            [
                "Protocollo CAN: tre implementazioni di una specifica in prosa",
                "docs/CAN_PROTOCOL_DUPLICATION.md"
            ],
            [
                "Registro delle modifiche di questo repository",
                "CHANGELOG.md"
            ],
            [
                "Licenza (GPL-3.0-or-later)",
                "LICENSE"
            ]
        ],
        "docs_contact": "Domande, idee e segnalazioni: electrohobby3d@gmail.com",
        "h_author": "AUTORE",
        "h_license": "LICENZA",
        "license": "Software: GPL-3.0-or-later - vedi [LICENSE](LICENSE). Documentazione: CC BY-SA 4.0 - vedi [LICENSE.md](LICENSE.md)."
    },
    "de": {
        "subtitle": "Architektur, Schnittstellen, Sicherheitsbasis und die Wahrheit über das, was belegt ist",
        "honesty_label": "Ehrlichkeitsprüfung - was heute wirklich läuft:",
        "honesty": "dieses Repository enthält Dokumente und kleine Werkzeuge. Die Werkzeuge (der Katalog-Generator, der Marken-Generator, der README-Generator, die Veröffentlichungsprüfung und die Familienprüfung) sind echt und haben Unit-Tests, die in der CI laufen; der nächtliche Workflow führt sie gegen die übrigen Repositories der Familie aus. Die Dokumente sind aus den READMEs, Manifesten, Änderungsprotokollen und Dokumenten dieser Repositories geschrieben, wie sie für diese Version gelesen wurden, und eine Aussage, die sich nicht auf ein Repository zurückführen ließ, ist als solche gekennzeichnet. Nichts davon ist ein Hardwaretest: Die Fähigkeitenmatrix sagt für jede Fähigkeit, ob sie nur simuliert, auf einem Computer getestet oder auf echter Hardware ausgeführt wurde, und das Firmware-Repository gibt an, dass noch keine bestückte Platine existiert.",
        "h_overview": "Überblick",
        "overview_intro": "Das Bild unten zeigt die Repositories von URTC, den CAN-Bus, der die Platinen und die PC-Werkzeuge verbindet, und die Verbindungen, die ihre Dokumente behaupten.",
        "overview": [
            [
                "Architektur",
                "docs/ARCHITECTURE.md",
                "Schichten, Datenflüsse, Ports und Vertrauensgrenzen."
            ],
            [
                "Schnittstellen",
                "docs/INTERFACES.md",
                "wem jeder Vertrag gehört und wo er dokumentiert ist."
            ],
            [
                "Fähigkeitenmatrix",
                "docs/CAPABILITY_MATRIX.md",
                "was in Software belegt ist und was Hardware braucht, Projekt für Projekt."
            ],
            [
                "Sicherheitsbasis",
                "docs/SECURITY_BASELINE.md",
                "was der Code durchsetzt und was noch fehlt; und das [Bedrohungsmodell](docs/THREAT_MODEL.md)."
            ],
            [
                "Erster vertikaler Schnitt",
                "docs/FIRST_VERTICAL_SLICE.md",
                "der kleinste durchgehende Pfad, den es heute gibt."
            ],
            [
                "Duplizierung des CAN-Protokolls",
                "docs/CAN_PROTOCOL_DUPLICATION.md",
                "das Protokoll ist dreimal aus einem Text heraus implementiert; was eine gemeinsame Spezifikation enthalten würde."
            ],
            [
                "Projektkatalog",
                "docs/PROJECT_CATALOG.md",
                "jedes Repository des Ökosystems, aus seinem eigenen Manifest geschrieben."
            ]
        ],
        "tools_label": "Werkzeuge:",
        "tools": "`make_catalog.py` schreibt den Katalog, `make_brand.py` das Banner, das Symbol und die Familienkarte, `make_readmes.py` die acht READMEs dieses Repositorys, `publication_check.py` sucht vor einer Veröffentlichung nach allem Privaten, und `check_all.sh` führt die eigenen Prüfungen jedes Repositorys der Familie aus und gibt je eine Zeile PASS, FAIL oder SKIP aus. `make_glance.py` schreibt die Tabelle Auf einen Blick jedes Repositorys aus dessen Manifest und aus `data/glance.json` (`--check` vergleicht, `--apply` schreibt); nach einer Versionserhöhung aktualisiert `python tools/make_glance.py --apply --repo NAME` die Tabelle dieses Repositorys.",
        "h_role": "Rolle in URTC",
        "role": "URTC-DOCS ist das Gedächtnis des Ökosystems: der Ort, an dem Architektur, Schnittstellen, Sicherheitsbasis und Fähigkeitenmatrix liegen und an dem die Werkzeuge aufbewahrt werden, die alle Repositories nebeneinander vergleichen. Jedes Repository behält sein eigenes README, seine Tests und seinen Vertrag; dieses sagt, wie sie zusammenpassen und was wirklich belegt wurde.",
        "h_structure": "Repository-Struktur",
        "tree": {
            "docs": "Architektur, Schnittstellen, Fähigkeitenmatrix, Sicherheitsbasis, Bedrohungsmodell, erster Schnitt, Notiz zum CAN-Protokoll, erzeugter Katalog",
            "src": "die Werkzeuge als Paket (Katalog, Marke, READMEs, Veröffentlichungsprüfung)",
            "tools": "dünne Skripte über dem Paket, check_all.sh und die gemeinsamen CI-Prüfungen des Ökosystems",
            "tests": "Unit-Tests der Werkzeuge",
            "images": "Banner und Karte des Ökosystems",
            "brand": "das Symbol",
            "data": "die Daten, die die Generatoren lesen (die Zahlen von „Auf einen Blick“, die geprüften Aussagen)",
            "template": "die maßgebliche Kopie der Dateien, die alle Repositories teilen, und das Werkzeug, das sie einspielt"
        },
        "h_dev": "BUILD & AUSFÜHRUNG",
        "dev_requirements": "**Voraussetzungen:** Python 3.10 oder neuer; pytest für die Tests",
        "dev_comments": ["der Katalog ist aktuell (braucht die Repositories neben diesem)", "Banner, Symbol und Karte sind aktuell", "die acht READMEs sind aktuell", 'die Tabellen Auf einen Blick der Familie sind aktuell (braucht die Repositories neben diesem)', "nichts Privates würde mit einer Veröffentlichung hinausgehen", "die Prüfungen jedes Repositorys, eine Zeile je Repository", "die Unit-Tests der Werkzeuge"],
        "dev_note": "`build.sh` / `build.bat` installieren das Paket und führen die Tests aus, und `build-test.sh` / `build-test.bat` prüfen, ohne zu installieren; keines ändert eine Version. `python bump.py` erhöht die Version um einen Schritt (der Kilometerzähler des Ökosystems).",
        "h_related": "Verwandte Projekte",
        "related_intro": "URTC besteht aus unabhängigen Repositories mit jeweils eigener Version, eigenen Tests und eigenem README. Das ist die Familie, nach Gruppen:",
        "related_this": "dieses Repository",
        "related_beyond": "Über URTC hinaus:",
        "beyond": [
            [
                "HYDRA-UMC",
                "https://github.com/JuanenRac/HYDRA-UMC",
                "die Hauptplatine des Roboterarms, deren CAN-Relay als der Bus dokumentiert ist, an dem der Werkzeugkopf hängt"
            ],
            [
                "HYDRA-UMC-DOCS",
                "https://github.com/JuanenRac/HYDRA-UMC-DOCS",
                "dieselbe Idee für das Ökosystem HYDRA-UMC"
            ],
            [
                "ARMOR-DOCS",
                "https://github.com/JuanenRac/ARMOR-DOCS",
                "dieselbe Idee für das Sicherheits-Ökosystem A.R.M.O.R."
            ],
            [
                "JuanenRac",
                "https://github.com/JuanenRac/JuanenRac",
                "das Profil und das Status-Dashboard aller Ökosysteme"
            ]
        ],
        "h_docs": "Dokumentation & Community",
        "docs_intro": "Wo man mehr liest:",
        "docs_links": [
            [
                "Fähigkeitenmatrix: was belegt ist und was nicht",
                "docs/CAPABILITY_MATRIX.md"
            ],
            [
                "Projektkatalog: Versionen und Arten der Repositories",
                "docs/PROJECT_CATALOG.md"
            ],
            [
                "CAN-Protokoll: drei Implementierungen einer Prosa-Spezifikation",
                "docs/CAN_PROTOCOL_DUPLICATION.md"
            ],
            [
                "Änderungsprotokoll dieses Repositorys",
                "CHANGELOG.md"
            ],
            [
                "Lizenz (GPL-3.0-or-later)",
                "LICENSE"
            ]
        ],
        "docs_contact": "Fragen, Ideen und Meldungen: electrohobby3d@gmail.com",
        "h_author": "AUTOR",
        "h_license": "LIZENZ",
        "license": "Software: GPL-3.0-or-later - siehe [LICENSE](LICENSE). Dokumentation: CC BY-SA 4.0 - siehe [LICENSE.md](LICENSE.md)."
    },
    "zh": {
        "subtitle": "架构、接口、安全基线，以及关于哪些已被证实的实情",
        "honesty_label": "诚实性检查 - 今天真正能运行的部分：",
        "honesty": "本仓库包含文档和小工具。这些工具（目录生成器、品牌素材生成器、README 生成器、发布检查和家族检查）是真实的，并有在 CI 中运行的单元测试；夜间工作流会针对家族中的其他仓库运行它们。文档依据这些仓库的 README、清单、变更日志和文档编写，以为本版本阅读时的内容为准，无法追溯到某个仓库的说法会被如实标明。这里的任何内容都不是硬件测试：能力矩阵会对每项能力说明它只是被模拟、在计算机上测试过，还是在真实硬件上运行过，固件仓库也说明目前尚不存在已焊装的电路板。",
        "h_overview": "简介",
        "overview_intro": "下图显示 URTC 的各个仓库、连接电路板与电脑端工具的 CAN 总线，以及它们的文档所陈述的联系。",
        "overview": [
            [
                "架构",
                "docs/ARCHITECTURE.md",
                "分层、数据流、端口和信任边界。"
            ],
            [
                "接口",
                "docs/INTERFACES.md",
                "每份契约归谁所有，以及记录在哪里。"
            ],
            [
                "能力矩阵",
                "docs/CAPABILITY_MATRIX.md",
                "哪些在软件中已证实、哪些需要硬件，逐个项目说明。"
            ],
            [
                "安全基线",
                "docs/SECURITY_BASELINE.md",
                "代码已强制执行的内容和仍然缺少的内容；以及[威胁模型](docs/THREAT_MODEL.md)。"
            ],
            [
                "第一个垂直切片",
                "docs/FIRST_VERTICAL_SLICE.md",
                "今天已存在的最小端到端路径。"
            ],
            [
                "CAN 协议的重复实现",
                "docs/CAN_PROTOCOL_DUPLICATION.md",
                "该协议依据一份文字说明被实现了三次；共享规范将包含什么。"
            ],
            [
                "项目目录",
                "docs/PROJECT_CATALOG.md",
                "生态中的每个仓库，依据其自身清单生成。"
            ]
        ],
        "tools_label": "工具：",
        "tools": "`make_catalog.py` 生成目录，`make_brand.py` 生成横幅、图标和家族图，`make_readmes.py` 生成本仓库的八份 README，`publication_check.py` 在发布前查找任何私有内容，`check_all.sh` 运行家族中每个仓库自己的检查，并为每个仓库输出一行 PASS、FAIL 或 SKIP。`make_glance.py` 根据每个仓库的清单和 `data/glance.json` 生成其“速览”表（`--check` 比较，`--apply` 写入）；提升版本后，运行 `python tools/make_glance.py --apply --repo NAME` 即可刷新该仓库的表。",
        "h_role": "在 URTC 中的角色",
        "role": "URTC-DOCS 是整个生态的记忆：架构、接口、安全基线和能力矩阵都放在这里，同时也保存着把所有仓库并排比较的工具。每个仓库保留自己的 README、测试和契约；本仓库说明它们如何配合，以及真正证实了什么。",
        "h_structure": "仓库结构",
        "tree": {
            "docs": "架构、接口、能力矩阵、安全基线、威胁模型、第一个切片、CAN 协议说明、生成的目录",
            "src": "以包形式提供的工具（目录、品牌素材、README、发布检查）",
            "tools": "包之上的薄脚本、check_all.sh，以及生态共享的 CI 检查",
            "tests": "工具的单元测试",
            "images": "横幅和生态图",
            "brand": "图标",
            "data": "生成器读取的数据（“速览”中的数字、已审阅的声明）",
            "template": "所有仓库共享文件的规范副本，以及把它放到位的工具"
        },
        "h_dev": "构建与运行",
        "dev_requirements": "**要求：** Python 3.10 或更新版本；测试需要 pytest",
        "dev_comments": ["目录是最新的（需要本仓库旁边有其他仓库）", "横幅、图标和家族图是最新的", "八份 README 是最新的", '家族的“速览”表是最新的（需要本仓库旁边有其他仓库）', "发布时不会带出任何私有内容", "每个仓库的检查，每个一行", "工具的单元测试"],
        "dev_note": "`build.sh` / `build.bat` 安装包并运行测试，`build-test.sh` / `build-test.bat` 不安装直接检查；两者都不会改变版本。`python bump.py` 将版本提升一步（生态的里程表规则）。",
        "h_related": "相关项目",
        "related_intro": "URTC 由相互独立的仓库组成，每个仓库都有自己的版本、测试和 README。以下是按组划分的家族：",
        "related_this": "本仓库",
        "related_beyond": "URTC 之外：",
        "beyond": [
            [
                "HYDRA-UMC",
                "https://github.com/JuanenRac/HYDRA-UMC",
                "机械臂主板，其 CAN 中继在文档中被记载为工具头所接入的总线"
            ],
            [
                "HYDRA-UMC-DOCS",
                "https://github.com/JuanenRac/HYDRA-UMC-DOCS",
                "同样的思路，用于 HYDRA-UMC 生态"
            ],
            [
                "ARMOR-DOCS",
                "https://github.com/JuanenRac/ARMOR-DOCS",
                "同样的思路，用于 A.R.M.O.R. 安防生态"
            ],
            [
                "JuanenRac",
                "https://github.com/JuanenRac/JuanenRac",
                "所有生态的个人主页和状态面板"
            ]
        ],
        "h_docs": "文档与社区",
        "docs_intro": "更多阅读：",
        "docs_links": [
            [
                "能力矩阵：哪些已证实，哪些没有",
                "docs/CAPABILITY_MATRIX.md"
            ],
            [
                "项目目录：各仓库的版本和类型",
                "docs/PROJECT_CATALOG.md"
            ],
            [
                "CAN 协议：同一份文字规范的三个实现",
                "docs/CAN_PROTOCOL_DUPLICATION.md"
            ],
            [
                "本仓库的变更日志",
                "CHANGELOG.md"
            ],
            [
                "许可证 (GPL-3.0-or-later)",
                "LICENSE"
            ]
        ],
        "docs_contact": "问题、想法和报告：electrohobby3d@gmail.com",
        "h_author": "作者",
        "h_license": "许可证",
        "license": "软件：GPL-3.0-or-later - 见 [LICENSE](LICENSE)。文档：CC BY-SA 4.0 - 见 [LICENSE.md](LICENSE.md)。"
    },
    "ja": {
        "subtitle": "アーキテクチャ、インターフェース、セキュリティ基準、そして何が実証済みかという事実",
        "honesty_label": "正直さの確認 - 今日実際に動くもの：",
        "honesty": "このリポジトリにはドキュメントと小さなツールがあります。ツール（カタログ生成、ブランド素材生成、README 生成、公開前チェック、ファミリーチェック）は実在し、CI で実行される単体テストがあります。夜間ワークフローは、ファミリーの他のリポジトリに対してそれらを実行します。ドキュメントは、このバージョンのために読んだ時点の各リポジトリの README、マニフェスト、変更履歴、ドキュメントから書かれており、リポジトリまでたどれなかった記述はその旨を明記しています。ここにあるものはハードウェアテストではありません。能力マトリクスは各能力について、シミュレーションのみか、コンピュータ上でテスト済みか、実機で動作したかを示します。ファームウェアのリポジトリは、実装済みの基板がまだ存在しないと述べています。",
        "h_overview": "概要",
        "overview_intro": "下の図は、URTC のリポジトリ、基板とパソコン側ツールをつなぐ CAN バス、そして各ドキュメントが述べる関係を示します。",
        "overview": [
            [
                "アーキテクチャ",
                "docs/ARCHITECTURE.md",
                "レイヤー、データの流れ、ポート、信頼境界。"
            ],
            [
                "インターフェース",
                "docs/INTERFACES.md",
                "各契約の所有者と、その文書の場所。"
            ],
            [
                "能力マトリクス",
                "docs/CAPABILITY_MATRIX.md",
                "ソフトウェアで実証済みのものとハードウェアが必要なものを、プロジェクトごとに。"
            ],
            [
                "セキュリティ基準",
                "docs/SECURITY_BASELINE.md",
                "コードが強制していることとまだ足りないこと。および[脅威モデル](docs/THREAT_MODEL.md)。"
            ],
            [
                "最初の垂直スライス",
                "docs/FIRST_VERTICAL_SLICE.md",
                "今日存在する最小のエンドツーエンド経路。"
            ],
            [
                "CAN プロトコルの重複実装",
                "docs/CAN_PROTOCOL_DUPLICATION.md",
                "プロトコルは文章の説明から三回実装されています。共有仕様に含まれるはずの内容。"
            ],
            [
                "プロジェクトカタログ",
                "docs/PROJECT_CATALOG.md",
                "エコシステムの全リポジトリを、それぞれのマニフェストから生成。"
            ]
        ],
        "tools_label": "ツール：",
        "tools": "`make_catalog.py` はカタログを、`make_brand.py` はバナー・アイコン・ファミリーマップを、`make_readmes.py` はこのリポジトリの 8 つの README を書きます。`publication_check.py` は公開前に非公開のものを探し、`check_all.sh` はファミリーの各リポジトリ自身のチェックを実行して、1 件ごとに PASS、FAIL、SKIP の 1 行を出力します。 `make_glance.py` は各リポジトリのマニフェストと `data/glance.json` から「ひと目で」の表を書きます（`--check` は比較、`--apply` は書き込み）。バージョンを上げた後は `python tools/make_glance.py --apply --repo NAME` でそのリポジトリの表を更新します。",
        "h_role": "URTC での役割",
        "role": "URTC-DOCS はエコシステムの記憶です。アーキテクチャ、インターフェース、セキュリティ基準、能力マトリクスがここにあり、すべてのリポジトリを並べて比較するツールもここに置かれています。各リポジトリは自分の README、テスト、契約を持ち続けます。このリポジトリは、それらがどう組み合わさるか、そして実際に何が実証されたかを述べます。",
        "h_structure": "リポジトリ構成",
        "tree": {
            "docs": "アーキテクチャ、インターフェース、能力マトリクス、セキュリティ基準、脅威モデル、最初のスライス、CAN プロトコルのメモ、生成されたカタログ",
            "src": "パッケージとしてのツール（カタログ、ブランド、README、公開前チェック）",
            "tools": "パッケージの上の薄いスクリプト、check_all.sh、エコシステム共通の CI チェック",
            "tests": "ツールの単体テスト",
            "images": "バナーとエコシステムマップ",
            "brand": "アイコン",
            "data": "ジェネレーターが読むデータ（「ひと目で」の数値、確認済みの主張）",
            "template": "全リポジトリが共有するファイルの正本と、それを配置するツール"
        },
        "h_dev": "ビルドと実行",
        "dev_requirements": "**必要なもの：** Python 3.10 以降、テスト用に pytest",
        "dev_comments": ["カタログが最新（このリポジトリの隣に他のリポジトリが必要）", "バナー、アイコン、マップが最新", "8 つの README が最新", 'ファミリー全体の「ひと目で」の表が最新（このリポジトリの隣に他のリポジトリが必要）', "公開で非公開のものが外に出ない", "各リポジトリのチェックを 1 行ずつ", "ツールの単体テスト"],
        "dev_note": "`build.sh` / `build.bat` はパッケージをインストールしてテストを実行し、`build-test.sh` / `build-test.bat` はインストールせずに確認します。どちらもバージョンは変えません。`python bump.py` がバージョンを 1 段階上げます（エコシステムのオドメーター方式）。",
        "h_related": "関連プロジェクト",
        "related_intro": "URTC は独立したリポジトリで構成され、それぞれに固有のバージョン、テスト、README があります。グループ別のファミリーは次のとおりです：",
        "related_this": "このリポジトリ",
        "related_beyond": "URTC の外：",
        "beyond": [
            [
                "HYDRA-UMC",
                "https://github.com/JuanenRac/HYDRA-UMC",
                "ロボットアームのマザーボード。そのCANリレーが、ツールヘッドが接続されるバスとして文書化されています"
            ],
            [
                "HYDRA-UMC-DOCS",
                "https://github.com/JuanenRac/HYDRA-UMC-DOCS",
                "HYDRA-UMC エコシステム向けの同じ考え方"
            ],
            [
                "ARMOR-DOCS",
                "https://github.com/JuanenRac/ARMOR-DOCS",
                "A.R.M.O.R. セキュリティエコシステム向けの同じ考え方"
            ],
            [
                "JuanenRac",
                "https://github.com/JuanenRac/JuanenRac",
                "すべてのエコシステムのプロフィールとステータスダッシュボード"
            ]
        ],
        "h_docs": "ドキュメントとコミュニティ",
        "docs_intro": "さらに読むには：",
        "docs_links": [
            [
                "能力マトリクス：実証済みのものとそうでないもの",
                "docs/CAPABILITY_MATRIX.md"
            ],
            [
                "プロジェクトカタログ：各リポジトリのバージョンと種類",
                "docs/PROJECT_CATALOG.md"
            ],
            [
                "CAN プロトコル：文章による一つの仕様の三つの実装",
                "docs/CAN_PROTOCOL_DUPLICATION.md"
            ],
            [
                "このリポジトリの変更履歴",
                "CHANGELOG.md"
            ],
            [
                "ライセンス (GPL-3.0-or-later)",
                "LICENSE"
            ]
        ],
        "docs_contact": "質問、アイデア、報告：electrohobby3d@gmail.com",
        "h_author": "作者",
        "h_license": "ライセンス",
        "license": "ソフトウェア：GPL-3.0-or-later - [LICENSE](LICENSE) を参照。ドキュメント：CC BY-SA 4.0 - [LICENSE.md](LICENSE.md) を参照。"
    },
    "pt": {
        "subtitle": "Arquitetura, interfaces, base de segurança e a verdade sobre o que está comprovado",
        "honesty_label": "Verificação de honestidade - o que funciona mesmo hoje:",
        "honesty": "este repositório contém documentos e pequenas ferramentas. As ferramentas (o gerador do catálogo, o da marca, o dos README, a verificação de publicação e a verificação da família) são reais e têm testes unitários executados na CI; o fluxo noturno executa-as sobre os restantes repositórios da família. Os documentos são escritos a partir dos README, manifestos, registos de alterações e documentos desses repositórios tal como foram lidos para esta versão, e uma afirmação que não se conseguiu rastrear até um repositório fica assinalada como tal. Nada aqui é um teste de hardware: a matriz de capacidades diz, para cada capacidade, se foi apenas simulada, testada num computador ou executada em hardware real, e o repositório do firmware indica que ainda não existe nenhuma placa montada.",
        "h_overview": "Visão geral",
        "overview_intro": "A imagem abaixo mostra os repositórios do URTC, o barramento CAN que liga as placas e as ferramentas do computador, e as ligações que os seus documentos afirmam.",
        "overview": [
            [
                "Arquitetura",
                "docs/ARCHITECTURE.md",
                "camadas, fluxos de dados, portas e fronteiras de confiança."
            ],
            [
                "Interfaces",
                "docs/INTERFACES.md",
                "quem é dono de cada contrato e onde está documentado."
            ],
            [
                "Matriz de capacidades",
                "docs/CAPABILITY_MATRIX.md",
                "o que está comprovado em software e o que precisa de hardware, projeto a projeto."
            ],
            [
                "Base de segurança",
                "docs/SECURITY_BASELINE.md",
                "o que o código impõe e o que ainda falta; e o [modelo de ameaças](docs/THREAT_MODEL.md)."
            ],
            [
                "Primeiro corte vertical",
                "docs/FIRST_VERTICAL_SLICE.md",
                "o caminho de ponta a ponta mais pequeno que existe hoje."
            ],
            [
                "Duplicação do protocolo CAN",
                "docs/CAN_PROTOCOL_DUPLICATION.md",
                "o protocolo está implementado três vezes a partir de texto; o que conteria uma especificação partilhada."
            ],
            [
                "Catálogo de projetos",
                "docs/PROJECT_CATALOG.md",
                "cada repositório do ecossistema, escrito a partir do seu próprio manifesto."
            ]
        ],
        "tools_label": "Ferramentas:",
        "tools": "`make_catalog.py` escreve o catálogo, `make_brand.py` o banner, o ícone e o mapa das famílias, `make_readmes.py` os oito README deste repositório, `publication_check.py` procura qualquer coisa privada antes de uma publicação e `check_all.sh` executa as verificações próprias de cada repositório da família e imprime uma linha PASS, FAIL ou SKIP por cada um. `make_glance.py` escreve a tabela Num relance de cada repositório a partir do seu manifesto e de `data/glance.json` (`--check` compara, `--apply` escreve); depois de subir uma versão, `python tools/make_glance.py --apply --repo NOME` atualiza a tabela desse repositório.",
        "h_role": "Papel no URTC",
        "role": "O URTC-DOCS é a memória do ecossistema: o lugar onde vivem a arquitetura, as interfaces, a base de segurança e a matriz de capacidades, e onde se guardam as ferramentas que comparam todos os repositórios lado a lado. Cada repositório mantém o seu próprio README, os seus testes e o seu contrato; este explica como encaixam e o que foi realmente comprovado.",
        "h_structure": "Estrutura do repositório",
        "tree": {
            "docs": "arquitetura, interfaces, matriz de capacidades, base de segurança, modelo de ameaças, primeiro corte, nota do protocolo CAN, catálogo gerado",
            "src": "as ferramentas como pacote (catálogo, marca, README, verificação de publicação)",
            "tools": "scripts finos sobre o pacote, check_all.sh e as verificações de CI partilhadas do ecossistema",
            "tests": "testes unitários das ferramentas",
            "images": "banner e mapa do ecossistema",
            "brand": "o ícone",
            "data": "os dados que os geradores leem (os números de «Num relance», as afirmações revistas)",
            "template": "a cópia de referência dos ficheiros que todos os repositórios partilham e a ferramenta que a coloca"
        },
        "h_dev": "COMPILAÇÃO E EXECUÇÃO",
        "dev_requirements": "**Requisitos:** Python 3.10 ou superior; pytest para os testes",
        "dev_comments": ["o catálogo está atualizado (precisa dos repositórios ao lado deste)", "o banner, o ícone e o mapa estão atualizados", "os oito README estão atualizados", 'as tabelas Num relance da família estão atualizadas (precisa dos repositórios ao lado deste)', "nada privado sairia com uma publicação", "as verificações de cada repositório, uma linha por cada um", "os testes unitários das ferramentas"],
        "dev_note": "`build.sh` / `build.bat` instalam o pacote e executam os testes, e `build-test.sh` / `build-test.bat` verificam sem instalar; nenhum altera a versão. `python bump.py` sobe a versão um passo (o conta-quilómetros do ecossistema).",
        "h_related": "Projetos relacionados",
        "related_intro": "O URTC é feito de repositórios independentes, cada um com a sua versão, os seus testes e o seu README. Esta é a família, por grupos:",
        "related_this": "este repositório",
        "related_beyond": "Para além do URTC:",
        "beyond": [
            [
                "HYDRA-UMC",
                "https://github.com/JuanenRac/HYDRA-UMC",
                "a placa-mãe do braço robótico, cujo relé CAN está documentado como o barramento onde a cabeça de ferramenta se liga"
            ],
            [
                "HYDRA-UMC-DOCS",
                "https://github.com/JuanenRac/HYDRA-UMC-DOCS",
                "a mesma ideia para o ecossistema HYDRA-UMC"
            ],
            [
                "ARMOR-DOCS",
                "https://github.com/JuanenRac/ARMOR-DOCS",
                "a mesma ideia para o ecossistema de segurança A.R.M.O.R."
            ],
            [
                "JuanenRac",
                "https://github.com/JuanenRac/JuanenRac",
                "o perfil e o painel de estado de todos os ecossistemas"
            ]
        ],
        "h_docs": "Documentação e comunidade",
        "docs_intro": "Onde ler mais:",
        "docs_links": [
            [
                "Matriz de capacidades: o que está comprovado e o que não está",
                "docs/CAPABILITY_MATRIX.md"
            ],
            [
                "Catálogo de projetos: versões e tipos dos repositórios",
                "docs/PROJECT_CATALOG.md"
            ],
            [
                "Protocolo CAN: três implementações de uma especificação em prosa",
                "docs/CAN_PROTOCOL_DUPLICATION.md"
            ],
            [
                "Registo de alterações deste repositório",
                "CHANGELOG.md"
            ],
            [
                "Licença (GPL-3.0-or-later)",
                "LICENSE"
            ]
        ],
        "docs_contact": "Perguntas, ideias e relatórios: electrohobby3d@gmail.com",
        "h_author": "AUTOR",
        "h_license": "LICENÇA",
        "license": "Software: GPL-3.0-or-later - ver [LICENSE](LICENSE). Documentação: CC BY-SA 4.0 - ver [LICENSE.md](LICENSE.md)."
    }
}
