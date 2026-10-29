<p align="center">
  <img src="images/URTC_DOCS_BANNER.svg" alt="URTC-DOCS banner" width="100%">
</p>

# 📚 URTC-DOCS

<p align="center"><a href="README.md">🇺🇸 English</a> | 🇪🇸 <b>Español</b> | <a href="README_fra.md">🇫🇷 Français</a> | <a href="README_ita.md">🇮🇹 Italiano</a> | <a href="README_deu.md">🇩🇪 Deutsch</a> | <a href="README_zho.md">🇨🇳 简体中文</a> | <a href="README_jpn.md">🇯🇵 日本語</a> | <a href="README_por.md">🇵🇹 Português</a></p>

### Arquitectura, interfaces, base de seguridad y la verdad sobre lo que está probado

<p align="center">
  <img src="https://img.shields.io/badge/License-GPL%203.0--or--later-blue.svg" alt="GPL 3.0 or later">
  <img src="https://img.shields.io/badge/Format-Markdown-083fa1.svg" alt="Format">
  <img src="https://img.shields.io/badge/Languages-8-00E5FF.svg" alt="Languages">
  <img src="https://img.shields.io/badge/Version-0.1.2-0f6cbd.svg" alt="Version">
  <img src="https://img.shields.io/badge/Maturity-scaffolding-FFB020.svg" alt="Maturity">
</p>

---

**Comprobación de honestidad - qué funciona hoy de verdad:** este repositorio contiene documentos y herramientas pequeñas. Las herramientas (el generador del catálogo, el de la marca, el de los README, la comprobación de publicación y la comprobación de la familia) son reales y tienen pruebas unitarias que se ejecutan en CI; el flujo nocturno las ejecuta contra los demás repositorios de la familia. Los documentos se han escrito a partir de los README, manifiestos, registros de cambios y documentos de esos repositorios tal como se leyeron para esta versión, y una afirmación que no se pudo rastrear hasta un repositorio queda señalada como tal. Nada de esto es una prueba de hardware: la matriz de capacidades dice, para cada capacidad, si solo se simuló, se probó en un ordenador o se ejecutó en hardware real, y el repositorio del firmware indica que todavía no existe ninguna placa montada.

---

> **Estado de seguridad física y de ciberseguridad:** este ecosistema no es un sistema de seguridad certificado y todavía no existe ninguna placa URTC poblada. Los bootloaders comprueban las imágenes de firmware con CRC32 y un HMAC-SHA256 de clave compartida, no con una firma asimétrica (prevista); las imágenes de aplicación publicadas están firmadas con la clave pública de desarrollo (`signing_key_kind: dev`), así que cualquiera puede producir una imagen que el bootloader acepte; no se ha transmitido nada a una placa real. Lee la [línea base de seguridad](docs/SECURITY_BASELINE.md) y el [modelo de amenazas](docs/THREAT_MODEL.md) antes de fiarte de cualquier afirmación de aquí para la seguridad de una persona.

## 📋 De un vistazo

| | |
|---|---|
| Versión | `0.1.2` |
| Madurez | Andamiaje |
| Tests | 153 |
| Tecnología | Markdown / Mermaid / Python / SVG |
| Destino | El PC de quien lo usa |
| En hardware real | No aplica: nada de esto se ejecuta en hardware |

**Ir a:** [Resumen](#-resumen) · [Arquitectura](#-arquitectura) · [Inicio rápido](#-inicio-rápido) · [Pruebas](#-pruebas) · [Estructura](#-estructura-del-repositorio) · [Relacionados](#-proyectos-relacionados)

## 🚦 Estado del proyecto

🟢 hecho y verificado · 🟡 funciona, con límites conocidos · 🟠 a medias o sin verificar · 🔴 sin hacer o sin funcionar. Nada es verde si nunca corrió en hardware real.

| Parte | Estado | Lo que el repositorio puede demostrar |
| --- | :---: | --- |
| Software | 🟡 | Los generadores del catálogo, de la marca y de los README, y las comprobaciones de la publicación, de las afirmaciones y de la familia, funcionan en un ordenador; no interviene hardware. |
| Pruebas | 🟢 | La batería de pruebas pasa en la CI, en Linux y en Windows, en cada subida. |
| Comprobaciones de toda la familia | 🟡 | La ejecución nocturna descarga cada repositorio de la familia y compara sus tablas resumen, afirmaciones y estructura del catálogo; una versión desfasada en el catálogo se avisa pero no hace fallar la noche. |
| Documentos de seguridad | 🟡 | La base de seguridad y el modelo de amenazas se escriben a partir de los demás repositorios tal como se leyeron; nadie ajeno al proyecto los ha revisado. |
| Documentación | 🟡 | README en ocho idiomas y documentos de referencia; las traducciones no las ha revisado ningún hablante nativo. |

## 🎯 Resumen

<p align="center">
  <img src="images/URTC_ECOSYSTEM.svg" alt="URTC ecosystem" width="100%">
</p>

La imagen siguiente muestra los repositorios de URTC, el bus CAN que une las placas y las herramientas del ordenador, y los vínculos que afirman sus documentos.

* [Arquitectura](docs/ARCHITECTURE.md): capas, flujos de datos, puertos y fronteras de confianza.
* [Interfaces](docs/INTERFACES.md): quién es dueño de cada contrato y dónde está documentado.
* [Matriz de capacidades](docs/CAPABILITY_MATRIX.md): qué está probado en software y qué necesita hardware, proyecto a proyecto.
* [Base de seguridad](docs/SECURITY_BASELINE.md): lo que el código impone y lo que aún falta; y el [modelo de amenazas](docs/THREAT_MODEL.md).
* [Primer corte vertical](docs/FIRST_VERTICAL_SLICE.md): el camino de extremo a extremo más pequeño que existe hoy.
* [Duplicación del protocolo CAN](docs/CAN_PROTOCOL_DUPLICATION.md): el protocolo está implementado tres veces a partir de prosa; qué contendría una especificación compartida.
* [Catálogo de proyectos](docs/PROJECT_CATALOG.md): cada repositorio del ecosistema, escrito a partir de su propio manifiesto.
* **Herramientas:** `make_catalog.py` escribe el catálogo, `make_brand.py` el banner, el icono y el mapa de familias, `make_readmes.py` los ocho README de este repositorio, `publication_check.py` busca cualquier cosa privada antes de una publicación y `check_all.sh` ejecuta las comprobaciones propias de cada repositorio de la familia e imprime una línea PASS, FAIL o SKIP por cada uno. `make_glance.py` escribe la tabla De un vistazo de cada repositorio a partir de su manifiesto y de `data/glance.json` (`--check` compara, `--apply` escribe); tras subir una versión, `python tools/make_glance.py --apply --repo NOMBRE` actualiza la tabla de ese repositorio. `check_claims.py` lee el README en inglés de cada repositorio de la familia y falla cuando una frase contiene una palabra de riesgo (E-STOP, enclavamiento, tiempo real, firmado, mTLS, FDCAN, YOLO, impulsado por IA, autónomo, certificado, ...) sin una marca de estado a su lado (previsto, no implementado, opcional, desactivado por defecto, simulado, probado, ...), salvo que una persona haya leído esa línea junto al código y la haya anotado en `data/claims_reviewed.json`. `check_repo_tools.py` compara los archivos que cada repositorio lleva como la misma copia (las comprobaciones de política de documentación y de paridad de README, el actualizador de versión del manifiesto, el workflow que avisa al panel) y falla cuando uno difiere. `sync_repo_tools.py` copia la versión canónica de esos archivos (`template/eh3d-repo-template`) en cada repositorio, respetando los finales de línea de cada archivo; sin `--apply` solo lista lo que cambiaría. `urtc_doctor.py` es el punto de entrada único: un informe con las herramientas de la máquina (Python, git, Node, el compilador ARM, PySide6, puertos serie), las versiones de cada repositorio (manifiesto, archivo fuente y última entrada del changelog), las copias de URTC-COMMON y el firmware incluido en el flasher y en el web studio, la validación de cada repositorio y las comprobaciones de este; `--fast` omite las validaciones y `--online` compara el firmware incluido con la última release.

## 🧩 Papel en URTC

URTC-DOCS es la memoria del ecosistema: el lugar donde viven la arquitectura, las interfaces, la base de seguridad y la matriz de capacidades, y donde se guardan las herramientas que comparan todos los repositorios entre sí. Cada repositorio conserva su propio README, sus pruebas y su contrato; este explica cómo encajan y qué se ha probado de verdad.

## 🏛️ Arquitectura

<p align="center">
  <img src="images/architecture.svg" alt="Arquitectura de URTC-DOCS: qué lee, qué contiene y qué alimenta" width="100%">
</p>

Cómo encajan las partes de este repositorio. La imagen se dibuja desde `docs/architecture.json` y se comprueba contra el código.

## 🚀 Inicio rápido

**Requisitos:** Python 3.10 o superior; pytest para las pruebas

```bash
python tools/make_catalog.py --check                 # el catálogo está al día (necesita los repositorios junto a este)
python tools/make_brand.py --check                   # el banner, el icono y el mapa están al día
python tools/make_readmes.py --check                 # los ocho README están al día
python tools/make_glance.py --check                  # las tablas De un vistazo de la familia están al día (necesita los repositorios junto a este)
python tools/publication_check.py                    # nada privado saldría con una publicación
python tools/check_claims.py --require-siblings      # ningún README afirma una capacidad de riesgo sin indicar su estado (necesita los repositorios junto a este)
python tools/check_repo_tools.py --require-siblings  # los archivos que cada repositorio lleva como la misma copia son iguales (necesita los repositorios junto a este)
bash tools/check_all.sh                              # las comprobaciones de cada repositorio, una línea por cada uno
python tools/urtc_doctor.py                          # el doctor: un informe sobre esta máquina y sobre cada repositorio
python -m pytest tests -q                            # las pruebas unitarias de las herramientas
```

## 🧪 Pruebas

La suite tiene 153 pruebas (`python -m pytest tests -q`). Ejecutan sobre ejemplos de prueba los generadores del catálogo, la marca, las tablas De un vistazo, las de estado y los README; las comprobaciones de afirmaciones, archivos compartidos, publicación y el doctor; los vectores de conformidad de las notas CAN, y comprueban que los README de este repositorio son exactamente lo que escribe el generador.

## 🏗️ Compilación y publicación

`build.sh` / `build.bat` instalan el paquete y ejecutan las pruebas, y `build-test.sh` / `build-test.bat` comprueban sin instalar; ninguno cambia una versión.

## 📂 Estructura del repositorio

<p align="center">
  <img src="images/repository-structure.svg" alt="Estructura del repositorio URTC-DOCS" width="100%">
</p>

<details>
<summary>Versión en texto del árbol</summary>

```text
URTC-DOCS/
├── docs/                                              arquitectura, interfaces, matriz de capacidades, base de seguridad, modelo de amenazas y el catálogo generado
├── src/urtc_docs/                                     las herramientas como paquete: catálogo, marca, README, De un vistazo, estado y comprobaciones
├── tools/                                             scripts finos sobre el paquete, check_all.sh y las comprobaciones de CI compartidas
├── data/                                              los números de De un vistazo y las afirmaciones revisadas
├── template/                                          la copia canónica de los archivos que comparten todos los repositorios
├── tests/                                             pruebas unitarias de las herramientas
├── brand/                                             el icono
├── images/                                            banner e imágenes de este README
├── .github/                                           flujo de CI y plantillas de issues y pull requests
├── build.sh build.bat                                 scripts de compilación
├── build-test.sh build-test.bat                       scripts de compilación y pruebas que no cambian nada en el repositorio
├── test.sh test.bat                                   ejecutan las pruebas
├── run.sh run.bat                                     arrancan el programa
├── urtc.project.json                                  manifiesto: versión, papel, madurez y comando de compilación
├── CHANGELOG.md                                       qué cambió en cada versión
├── SECURITY.md SUPPORT.md                             política de seguridad y soporte
├── CONTRIBUTING.md CODE_OF_CONDUCT.md                 cómo contribuir y código de conducta
├── .gitattributes .gitignore                          ajustes de Git
├── bump.py bump_version.py bump_manifest_version.py   scripts que suben la versión
├── LICENSE LICENSE.md                                 licencia del software y de la documentación
└── pyproject.toml requirements-dev.lock ruff.toml     paquete, herramientas fijadas y ajustes de lint
```

</details>

## 🗺️ Hoja de ruta y límites conocidos

**Límites conocidos hoy**

* La base de seguridad y el modelo de amenazas se escriben a partir de los demás repositorios tal como se leyeron; nadie ajeno al proyecto los ha revisado.
* La ejecución nocturna descarga todos los repositorios de la familia y compara sus tablas resumen, afirmaciones y estructura del catálogo; una versión desfasada en el catálogo se señala pero no hace fallar la noche.
* Los documentos describen software; no interviene hardware y ninguna afirmación sobre placas se ha comprobado en una placa.

**Siguiente**

* Mantener al día el catálogo, las tablas De un vistazo y la matriz de capacidades a medida que cambian los repositorios.

## 🌍 Idiomas

El README y los textos existen en inglés, español, francés, italiano, alemán, chino, japonés y portugués de Portugal.

## 🔗 Proyectos relacionados

URTC se compone de repositorios independientes, cada uno con su versión, sus pruebas y su README. Esta es la familia, por grupos:

* **URTC Tool Platform:**
  * [URTC](https://github.com/JuanenRac/URTC) - firmware de la placa del cabezal de herramienta (25 perfiles de herramienta, bootloader CAN) y la referencia del protocolo CAN.
  * [URTC-COMMON](https://github.com/JuanenRac/URTC-COMMON) - el protocolo CAN escrito una sola vez como datos (especificación, tablas generadas, vectores de conformidad) y el código que comparten los programas.
  * [URTC-FLASHER](https://github.com/JuanenRac/URTC-FLASHER) - herramienta de escritorio que actualiza el firmware de la placa por CAN o por SWD/JTAG.
  * [URTC-GATEWAY](https://github.com/JuanenRac/URTC-GATEWAY) - pasarela delante del bus CAN: solo deja pasar los identificadores de una lista, limita su frecuencia y pide una clave de sesión.
  * [URTC-SMART-RACK](https://github.com/JuanenRac/URTC-SMART-RACK) - lógica en C independiente del hardware y protocolo de órdenes para un soporte de herramientas con precalentamiento y seguimiento del ciclo de vida.
  * [URTC-TESTER](https://github.com/JuanenRac/URTC-TESTER) - probador de escritorio del bus CAN en vivo que muestra los controles y la telemetría del perfil de herramienta que informa una placa.
  * [URTC-VISION-TOOL](https://github.com/JuanenRac/URTC-VISION-TOOL) - protocolo de tramas de sensor en C y un acompañante en Python térmico/RGB para un cabezal de inspección.
  * [URTC-WEB-STUDIO](https://github.com/JuanenRac/URTC-WEB-STUDIO) - aplicación de navegador que graba y prueba la placa por Web Serial y SLCAN, sin instalar nada.
* **Ecosystem Operations:**
  * **URTC-DOCS** (este repositorio) - arquitectura, interfaces, línea base de seguridad y catálogo generado del ecosistema, más las herramientas que comparan todos los repositorios.
  * [URTC-UPDATER](https://github.com/JuanenRac/URTC-UPDATER) - herramienta de escritorio que detecta, instala y actualiza los repositorios de la familia URTC, una acción explícita cada vez.

**Proyectos hermanos (independientes, con la misma base y herramientas):**

* **[HYDRA-UMC-DOCS](https://github.com/JuanenRac/HYDRA-UMC-DOCS)** - proyecto hermano: el centro de documentación de HYDRA-UMC, un ecosistema independiente que comparte base y herramientas con este
* **[ARMOR-DOCS](https://github.com/JuanenRac/ARMOR-DOCS)** - proyecto hermano: el centro de documentación de A.R.M.O.R., el ecosistema de seguridad, también independiente y sobre la misma base
* **[JuanenRac](https://github.com/JuanenRac/JuanenRac)** - el perfil y el panel de estado de todos los ecosistemas

## 📚 Documentación

Dónde leer más:

* [Matriz de capacidades: qué está probado y qué no](docs/CAPABILITY_MATRIX.md)
* [Catálogo de proyectos: versiones y tipos de los repositorios](docs/PROJECT_CATALOG.md)
* [Protocolo CAN: tres implementaciones de una especificación en prosa](docs/CAN_PROTOCOL_DUPLICATION.md)
* [Registro de cambios de este repositorio](CHANGELOG.md)
* [Licencia (GPL-3.0-or-later)](LICENSE)

## 🤝 Contribuir y comunidad

* Antes de una pull request ejecuta `URTC_CI=1 python tools/ci_validate.py`: debe pasar. Consulta [CONTRIBUTING.md](CONTRIBUTING.md) y el [código de conducta](CODE_OF_CONDUCT.md).
* El README existe en ocho idiomas: un cambio en el texto se hace en los ocho archivos, y las secciones compartidas con otros repositorios las escribe `tools/readme_sections.py` de URTC-COMMON.
* No describas como funcionando en una placa lo que solo se ha compilado.
* Informa de una vulnerabilidad en privado: [SECURITY.md](SECURITY.md). Preguntas, ideas e informes: electrohobby3d@gmail.com ([SUPPORT.md](SUPPORT.md)).
* Preguntas, ideas e informes: electrohobby3d@gmail.com

## 👤 AUTOR

**JuanenRac (Electro Hobby 3D)** · electrohobby3d@gmail.com

## 📜 LICENCIA

Software: GPL-3.0-or-later - véase [LICENSE](LICENSE). Documentación: CC BY-SA 4.0 - véase [LICENSE.md](LICENSE.md).
