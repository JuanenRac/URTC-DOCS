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
  <img src="https://img.shields.io/badge/Version-0.0.4-0f6cbd.svg" alt="Version">
  <img src="https://img.shields.io/badge/Maturity-scaffolding-FFB020.svg" alt="Maturity">
</p>

---

**Comprobación de honestidad - qué funciona hoy de verdad:** este repositorio contiene documentos y herramientas pequeñas. Las herramientas (el generador del catálogo, el de la marca, el de los README, la comprobación de publicación y la comprobación de la familia) son reales y tienen pruebas unitarias que se ejecutan en CI; el flujo nocturno las ejecuta contra los demás repositorios de la familia. Los documentos se han escrito a partir de los README, manifiestos, registros de cambios y documentos de esos repositorios tal como se leyeron para esta versión, y una afirmación que no se pudo rastrear hasta un repositorio queda señalada como tal. Nada de esto es una prueba de hardware: la matriz de capacidades dice, para cada capacidad, si solo se simuló, se probó en un ordenador o se ejecutó en hardware real, y el repositorio del firmware indica que todavía no existe ninguna placa montada.

---

> **Estado de seguridad física y de ciberseguridad:** este ecosistema no es un sistema de seguridad certificado y todavía no existe ninguna placa URTC poblada. Los bootloaders comprueban las imágenes de firmware con CRC32 y un HMAC-SHA256 de clave compartida, no con una firma asimétrica (prevista); las imágenes de aplicación publicadas están firmadas con la clave pública de desarrollo (`signing_key_kind: dev`), así que cualquiera puede producir una imagen que el bootloader acepte; no se ha transmitido nada a una placa real. Lee la [línea base de seguridad](docs/SECURITY_BASELINE.md) y el [modelo de amenazas](docs/THREAT_MODEL.md) antes de fiarte de cualquier afirmación de aquí para la seguridad de una persona.

## 📋 De un vistazo

| | |
|---|---|
| Versión | `0.0.4` |
| Madurez | Andamiaje |
| Tecnología | Markdown / Mermaid / Python / SVG |
| Destino | El PC de quien lo usa |
| En hardware real | No aplica: nada de esto se ejecuta en hardware |

## 🎯 Descripción general

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
* **Herramientas:** `make_catalog.py` escribe el catálogo, `make_brand.py` el banner, el icono y el mapa de familias, `make_readmes.py` los ocho README de este repositorio, `publication_check.py` busca cualquier cosa privada antes de una publicación y `check_all.sh` ejecuta las comprobaciones propias de cada repositorio de la familia e imprime una línea PASS, FAIL o SKIP por cada uno. `make_glance.py` escribe la tabla De un vistazo de cada repositorio a partir de su manifiesto y de `data/glance.json` (`--check` compara, `--apply` escribe); tras subir una versión, `python tools/make_glance.py --apply --repo NOMBRE` actualiza la tabla de ese repositorio. `check_claims.py` lee el README en inglés de cada repositorio de la familia y falla cuando una frase contiene una palabra de riesgo (E-STOP, enclavamiento, tiempo real, firmado, mTLS, FDCAN, YOLO, impulsado por IA, autónomo, certificado, ...) sin una marca de estado a su lado (previsto, no implementado, opcional, desactivado por defecto, simulado, probado, ...), salvo que una persona haya leído esa línea junto al código y la haya anotado en `data/claims_reviewed.json`.

## 🧩 Papel en URTC

URTC-DOCS es la memoria del ecosistema: el lugar donde viven la arquitectura, las interfaces, la base de seguridad y la matriz de capacidades, y donde se guardan las herramientas que comparan todos los repositorios entre sí. Cada repositorio conserva su propio README, sus pruebas y su contrato; este explica cómo encajan y qué se ha probado de verdad.

## 📂 Estructura del repositorio

```text
URTC-DOCS/
├── docs/     arquitectura, interfaces, matriz de capacidades, base de seguridad, modelo de amenazas, primer corte, nota del protocolo CAN, catálogo generado
├── src/      las herramientas como paquete (catálogo, marca, README, comprobación de publicación)
├── tools/    scripts finos sobre el paquete, check_all.sh y las comprobaciones de CI compartidas del ecosistema
├── tests/    pruebas unitarias de las herramientas
├── images/   banner y mapa del ecosistema
├── brand/    el icono
├── build.sh / build.bat, build-test.sh / build-test.bat, run.sh / run.bat
└── urtc.project.json, pyproject.toml, CHANGELOG.md, LICENSE, LICENSE.md
```

## 🛠️ COMPILACIÓN Y EJECUCIÓN

**Requisitos:** Python 3.10 o superior; pytest para las pruebas

```bash
python tools/make_catalog.py --check             # el catálogo está al día (necesita los repositorios junto a este)
python tools/make_brand.py --check               # el banner, el icono y el mapa están al día
python tools/make_readmes.py --check             # los ocho README están al día
python tools/make_glance.py --check              # las tablas De un vistazo de la familia están al día (necesita los repositorios junto a este)
python tools/publication_check.py                # nada privado saldría con una publicación
python tools/check_claims.py --require-siblings  # ningún README afirma una capacidad de riesgo sin indicar su estado (necesita los repositorios junto a este)
bash tools/check_all.sh                          # las comprobaciones de cada repositorio, una línea por cada uno
python -m pytest tests -q                        # las pruebas unitarias de las herramientas
```

`build.sh` / `build.bat` suben la versión un paso (el cuentakilómetros del ecosistema), instalan el paquete y ejecutan las pruebas; `build-test.sh` / `build-test.bat` comprueban sin cambiar ninguna versión.

## 🔗 Proyectos relacionados

URTC se compone de repositorios independientes, cada uno con su versión, sus pruebas y su README. Esta es la familia, por grupos:

* **URTC Tool Platform:** [URTC](https://github.com/JuanenRac/URTC), [URTC-COMMON](https://github.com/JuanenRac/URTC-COMMON), [URTC-FLASHER](https://github.com/JuanenRac/URTC-FLASHER), [URTC-SMART-RACK](https://github.com/JuanenRac/URTC-SMART-RACK), [URTC-TESTER](https://github.com/JuanenRac/URTC-TESTER), [URTC-VISION-TOOL](https://github.com/JuanenRac/URTC-VISION-TOOL), [URTC-WEB-STUDIO](https://github.com/JuanenRac/URTC-WEB-STUDIO)
* **Ecosystem Operations:** **URTC-DOCS** (este repositorio), [URTC-UPDATER](https://github.com/JuanenRac/URTC-UPDATER)

**Más allá de URTC:**

* **[HYDRA-UMC](https://github.com/JuanenRac/HYDRA-UMC)** - la placa base del brazo robótico, cuyo relé CAN está documentado como el bus en el que se conecta la cabeza de herramienta
* **[HYDRA-UMC-DOCS](https://github.com/JuanenRac/HYDRA-UMC-DOCS)** - la misma idea para el ecosistema HYDRA-UMC
* **[ARMOR-DOCS](https://github.com/JuanenRac/ARMOR-DOCS)** - la misma idea para el ecosistema de seguridad A.R.M.O.R.
* **[JuanenRac](https://github.com/JuanenRac/JuanenRac)** - el perfil y el panel de estado de todos los ecosistemas

## 📚 Documentación y comunidad

Dónde leer más:

* [Matriz de capacidades: qué está probado y qué no](docs/CAPABILITY_MATRIX.md)
* [Catálogo de proyectos: versiones y tipos de los repositorios](docs/PROJECT_CATALOG.md)
* [Protocolo CAN: tres implementaciones de una especificación en prosa](docs/CAN_PROTOCOL_DUPLICATION.md)
* [Registro de cambios de este repositorio](CHANGELOG.md)
* [Licencia (GPL-3.0-or-later)](LICENSE)
* Preguntas, ideas e informes: electrohobby3d@gmail.com

## 👤 AUTOR

**JuanenRac (Electro Hobby 3D)** · electrohobby3d@gmail.com

## 📜 LICENCIA

Software: GPL-3.0-or-later - véase [LICENSE](LICENSE). Documentación: CC BY-SA 4.0 - véase [LICENSE.md](LICENSE.md).
