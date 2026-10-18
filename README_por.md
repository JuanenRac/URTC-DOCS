<p align="center">
  <img src="images/URTC_DOCS_BANNER.svg" alt="URTC-DOCS banner" width="100%">
</p>

# 📚 URTC-DOCS

<p align="center"><a href="README.md">🇺🇸 English</a> | <a href="README_spa.md">🇪🇸 Español</a> | <a href="README_fra.md">🇫🇷 Français</a> | <a href="README_ita.md">🇮🇹 Italiano</a> | <a href="README_deu.md">🇩🇪 Deutsch</a> | <a href="README_zho.md">🇨🇳 简体中文</a> | <a href="README_jpn.md">🇯🇵 日本語</a> | 🇵🇹 <b>Português</b></p>

### Arquitetura, interfaces, base de segurança e a verdade sobre o que está comprovado

<p align="center">
  <img src="https://img.shields.io/badge/License-GPL%203.0--or--later-blue.svg" alt="GPL 3.0 or later">
  <img src="https://img.shields.io/badge/Format-Markdown-083fa1.svg" alt="Format">
  <img src="https://img.shields.io/badge/Languages-8-00E5FF.svg" alt="Languages">
  <img src="https://img.shields.io/badge/Version-0.0.2-0f6cbd.svg" alt="Version">
  <img src="https://img.shields.io/badge/Maturity-scaffolding-FFB020.svg" alt="Maturity">
</p>

---

**Verificação de honestidade - o que funciona mesmo hoje:** este repositório contém documentos e pequenas ferramentas. As ferramentas (o gerador do catálogo, o da marca, o dos README, a verificação de publicação e a verificação da família) são reais e têm testes unitários executados na CI; o fluxo noturno executa-as sobre os restantes repositórios da família. Os documentos são escritos a partir dos README, manifestos, registos de alterações e documentos desses repositórios tal como foram lidos para esta versão, e uma afirmação que não se conseguiu rastrear até um repositório fica assinalada como tal. Nada aqui é um teste de hardware: a matriz de capacidades diz, para cada capacidade, se foi apenas simulada, testada num computador ou executada em hardware real, e o repositório do firmware indica que ainda não existe nenhuma placa montada.

---

## 📋 Num relance

| | |
|---|---|
| Versão | `0.0.2` |
| Maturidade | Estrutura inicial |
| Tecnologia | Markdown / Mermaid / Python / SVG |
| Destino | O PC de quem o usa |
| Em hardware real | Não aplicável: nada aqui corre em hardware |

## 🎯 Visão geral

<p align="center">
  <img src="images/URTC_ECOSYSTEM.svg" alt="URTC ecosystem" width="100%">
</p>

A imagem abaixo mostra os repositórios do URTC, o barramento CAN que liga as placas e as ferramentas do computador, e as ligações que os seus documentos afirmam.

* [Arquitetura](docs/ARCHITECTURE.md): camadas, fluxos de dados, portas e fronteiras de confiança.
* [Interfaces](docs/INTERFACES.md): quem é dono de cada contrato e onde está documentado.
* [Matriz de capacidades](docs/CAPABILITY_MATRIX.md): o que está comprovado em software e o que precisa de hardware, projeto a projeto.
* [Base de segurança](docs/SECURITY_BASELINE.md): o que o código impõe e o que ainda falta; e o [modelo de ameaças](docs/THREAT_MODEL.md).
* [Primeiro corte vertical](docs/FIRST_VERTICAL_SLICE.md): o caminho de ponta a ponta mais pequeno que existe hoje.
* [Duplicação do protocolo CAN](docs/CAN_PROTOCOL_DUPLICATION.md): o protocolo está implementado três vezes a partir de texto; o que conteria uma especificação partilhada.
* [Catálogo de projetos](docs/PROJECT_CATALOG.md): cada repositório do ecossistema, escrito a partir do seu próprio manifesto.
* **Ferramentas:** `make_catalog.py` escreve o catálogo, `make_brand.py` o banner, o ícone e o mapa das famílias, `make_readmes.py` os oito README deste repositório, `publication_check.py` procura qualquer coisa privada antes de uma publicação e `check_all.sh` executa as verificações próprias de cada repositório da família e imprime uma linha PASS, FAIL ou SKIP por cada um. `make_glance.py` escreve a tabela Num relance de cada repositório a partir do seu manifesto e de `data/glance.json` (`--check` compara, `--apply` escreve); depois de subir uma versão, `python tools/make_glance.py --apply --repo NOME` atualiza a tabela desse repositório.

## 🧩 Papel no URTC

O URTC-DOCS é a memória do ecossistema: o lugar onde vivem a arquitetura, as interfaces, a base de segurança e a matriz de capacidades, e onde se guardam as ferramentas que comparam todos os repositórios lado a lado. Cada repositório mantém o seu próprio README, os seus testes e o seu contrato; este explica como encaixam e o que foi realmente comprovado.

## 📂 Estrutura do repositório

```text
URTC-DOCS/
├── docs/     arquitetura, interfaces, matriz de capacidades, base de segurança, modelo de ameaças, primeiro corte, nota do protocolo CAN, catálogo gerado
├── src/      as ferramentas como pacote (catálogo, marca, README, verificação de publicação)
├── tools/    scripts finos sobre o pacote, check_all.sh e as verificações de CI partilhadas do ecossistema
├── tests/    testes unitários das ferramentas
├── images/   banner e mapa do ecossistema
├── brand/    o ícone
├── build.sh / build.bat, build-test.sh / build-test.bat, run.sh / run.bat
└── urtc.project.json, pyproject.toml, CHANGELOG.md, LICENSE, LICENSE.md
```

## 🛠️ COMPILAÇÃO E EXECUÇÃO

**Requisitos:** Python 3.10 ou superior; pytest para os testes

```bash
python tools/make_catalog.py --check  # o catálogo está atualizado (precisa dos repositórios ao lado deste)
python tools/make_brand.py --check    # o banner, o ícone e o mapa estão atualizados
python tools/make_readmes.py --check  # os oito README estão atualizados
python tools/make_glance.py --check   # as tabelas Num relance da família estão atualizadas (precisa dos repositórios ao lado deste)
python tools/publication_check.py     # nada privado sairia com uma publicação
bash tools/check_all.sh               # as verificações de cada repositório, uma linha por cada um
python -m pytest tests -q             # os testes unitários das ferramentas
```

`build.sh` / `build.bat` sobem a versão um passo (o conta-quilómetros do ecossistema), instalam o pacote e executam os testes; `build-test.sh` / `build-test.bat` verificam sem alterar nenhuma versão.

## 🔗 Projetos relacionados

O URTC é feito de repositórios independentes, cada um com a sua versão, os seus testes e o seu README. Esta é a família, por grupos:

* **URTC Tool Platform:** [URTC](https://github.com/JuanenRac/URTC), [URTC-FLASHER](https://github.com/JuanenRac/URTC-FLASHER), [URTC-SMART-RACK](https://github.com/JuanenRac/URTC-SMART-RACK), [URTC-TESTER](https://github.com/JuanenRac/URTC-TESTER), [URTC-VISION-TOOL](https://github.com/JuanenRac/URTC-VISION-TOOL), [URTC-WEB-STUDIO](https://github.com/JuanenRac/URTC-WEB-STUDIO)
* **Ecosystem Operations:** **URTC-DOCS** (este repositório), [URTC-UPDATER](https://github.com/JuanenRac/URTC-UPDATER)

**Para além do URTC:**

* **[HYDRA-UMC](https://github.com/JuanenRac/HYDRA-UMC)** - a placa-mãe do braço robótico, cujo relé CAN está documentado como o barramento onde a cabeça de ferramenta se liga
* **[HYDRA-UMC-DOCS](https://github.com/JuanenRac/HYDRA-UMC-DOCS)** - a mesma ideia para o ecossistema HYDRA-UMC
* **[ARMOR-DOCS](https://github.com/JuanenRac/ARMOR-DOCS)** - a mesma ideia para o ecossistema de segurança A.R.M.O.R.
* **[JuanenRac](https://github.com/JuanenRac/JuanenRac)** - o perfil e o painel de estado de todos os ecossistemas

## 📚 Documentação e comunidade

Onde ler mais:

* [Matriz de capacidades: o que está comprovado e o que não está](docs/CAPABILITY_MATRIX.md)
* [Catálogo de projetos: versões e tipos dos repositórios](docs/PROJECT_CATALOG.md)
* [Protocolo CAN: três implementações de uma especificação em prosa](docs/CAN_PROTOCOL_DUPLICATION.md)
* [Registo de alterações deste repositório](CHANGELOG.md)
* [Licença (GPL-3.0-or-later)](LICENSE)
* Perguntas, ideias e relatórios: electrohobby3d@gmail.com

## 👤 AUTOR

**JuanenRac (Electro Hobby 3D)** · electrohobby3d@gmail.com

## 📜 LICENÇA

Software: GPL-3.0-or-later - ver [LICENSE](LICENSE). Documentação: CC BY-SA 4.0 - ver [LICENSE.md](LICENSE.md).
