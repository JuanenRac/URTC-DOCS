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
  <img src="https://img.shields.io/badge/Version-0.1.2-0f6cbd.svg" alt="Version">
  <img src="https://img.shields.io/badge/Maturity-scaffolding-FFB020.svg" alt="Maturity">
</p>

---

**Verificação de honestidade - o que funciona mesmo hoje:** este repositório contém documentos e pequenas ferramentas. As ferramentas (o gerador do catálogo, o da marca, o dos README, a verificação de publicação e a verificação da família) são reais e têm testes unitários executados na CI; o fluxo noturno executa-as sobre os restantes repositórios da família. Os documentos são escritos a partir dos README, manifestos, registos de alterações e documentos desses repositórios tal como foram lidos para esta versão, e uma afirmação que não se conseguiu rastrear até um repositório fica assinalada como tal. Nada aqui é um teste de hardware: a matriz de capacidades diz, para cada capacidade, se foi apenas simulada, testada num computador ou executada em hardware real, e o repositório do firmware indica que ainda não existe nenhuma placa montada.

---

> **Estado de segurança (safety e security):** este ecossistema não é um sistema de segurança certificado e ainda não existe nenhuma placa URTC montada. Os bootloaders verificam as imagens de firmware com CRC32 e um HMAC-SHA256 de chave partilhada, não com uma assinatura assimétrica (prevista); as imagens de aplicação publicadas estão assinadas com a chave pública de desenvolvimento (`signing_key_kind: dev`), pelo que qualquer pessoa pode produzir uma imagem que o bootloader aceita; nada foi transmitido a uma placa real. Leia a [base de segurança](docs/SECURITY_BASELINE.md) e o [modelo de ameaças](docs/THREAT_MODEL.md) antes de confiar em qualquer afirmação aqui para a segurança de uma pessoa.

## 📋 Num relance

| | |
|---|---|
| Versão | `0.1.3` |
| Maturidade | Estrutura inicial |
| Testes | 183 |
| Tecnologia | Markdown / Mermaid / Python / SVG |
| Destino | O PC de quem o usa |
| Em hardware real | Não aplicável: nada aqui corre em hardware |

**Ir para:** [Visão geral](#-visão-geral) · [Arquitetura](#-arquitetura) · [Início rápido](#-início-rápido) · [Testes](#-testes) · [Estrutura](#-estrutura-do-repositório) · [Relacionados](#-projetos-relacionados)

## 🚦 Estado do projeto

🟢 feito e verificado · 🟡 funciona, com limites conhecidos · 🟠 a meio ou por verificar · 🔴 por fazer ou a não funcionar. Nada é verde se nunca correu em hardware real.

| Parte | Estado | O que o repositório consegue demonstrar |
| --- | :---: | --- |
| Software | 🟡 | Os geradores do catálogo, da marca e dos README, e as verificações da publicação, das afirmações e da família, funcionam num computador; não envolve hardware. |
| Testes | 🟡 | A bateria de testes passa na CI, em Linux e em Windows, em cada envio. |
| Verificações de toda a família | 🟡 | A execução noturna obtém cada repositório da família e compara as suas tabelas-resumo, afirmações e a estrutura do catálogo; uma versão desatualizada no catálogo é assinalada, mas não faz falhar a noite. |
| Documentos de segurança | 🟡 | A base de segurança e o modelo de ameaças são escritos a partir dos outros repositórios tal como foram lidos; ninguém fora do projeto os reviu. |
| Documentação | 🟡 | README em oito línguas e documentos de referência; as traduções não foram revistas por falantes nativos. |

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
* **Ferramentas:** `make_catalog.py` escreve o catálogo, `make_brand.py` o banner, o ícone e o mapa das famílias, `make_readmes.py` os oito README deste repositório, `publication_check.py` procura qualquer coisa privada antes de uma publicação e `check_all.sh` executa as verificações próprias de cada repositório da família e imprime uma linha PASS, FAIL ou SKIP por cada um. `make_glance.py` escreve a tabela Num relance de cada repositório a partir do seu manifesto e de `data/glance.json` (`--check` compara, `--apply` escreve); depois de subir uma versão, `python tools/make_glance.py --apply --repo NOME` atualiza a tabela desse repositório. `check_claims.py` lê o README em inglês de cada repositório da família e falha quando uma frase tem uma palavra de risco (E-STOP, interlock, tempo real, assinado, mTLS, FDCAN, YOLO, orientado por IA, autónomo, certificado, ...) sem uma marca de estado ao lado (previsto, não implementado, opcional, desativado por defeito, simulado, testado, ...), a menos que uma pessoa tenha lido essa linha junto ao código e a tenha registado em `data/claims_reviewed.json`. `check_repo_tools.py` compara os ficheiros que cada repositório tem como a mesma cópia (as verificações da política de documentação e da paridade dos README, a ferramenta que sobe a versão do manifesto, o workflow que avisa o painel) e falha quando um difere. `sync_repo_tools.py` escreve a cópia canónica desses ficheiros (`template/eh3d-repo-template`) em cada repositório, mantendo os fins de linha de cada ficheiro; sem `--apply` apenas lista o que mudaria. As mesmas ferramentas escrevem e verificam um ficheiro de bloqueio, `tools/devtools.lock.json`, em cada repositório (a versão do conjunto partilhado do URTC-DEVTOOLS e o SHA-256 de cada ficheiro partilhado): são assinalados uma cópia editada, um ficheiro em falta, um ficheiro que o bloqueio não lista ou uma cópia que ficou atrás do conjunto. O `status_lights.py` é um dos ficheiros partilhados: o validador de cada repositório falha quando uma luz da sua tabela Project status está acima do que o seu manifesto (`maturity`, `evidence`) permite. `urtc_doctor.py` é o ponto de entrada único: um relatório com as ferramentas da máquina (Python, git, Node, o compilador ARM, PySide6, portas série), as versões de cada repositório (manifesto, ficheiro de código e entrada mais recente do changelog), as cópias de URTC-COMMON e o firmware incluído no flasher e no web studio, a validação de cada repositório e as verificações deste; `--fast` omite as validações e `--online` compara o firmware incluído com a release mais recente.

## 🧩 Papel no URTC

O URTC-DOCS é a memória do ecossistema: o lugar onde vivem a arquitetura, as interfaces, a base de segurança e a matriz de capacidades, e onde se guardam as ferramentas que comparam todos os repositórios lado a lado. Cada repositório mantém o seu próprio README, os seus testes e o seu contrato; este explica como encaixam e o que foi realmente comprovado.

## 🏛️ Arquitetura

<p align="center">
  <img src="images/architecture.svg" alt="Arquitetura do URTC-DOCS: o que lê, o que contém e o que alimenta" width="100%">
</p>

Como as partes deste repositório se encaixam. A imagem é desenhada a partir de `docs/architecture.json` e verificada com o código.

## 🚀 Início rápido

**Requisitos:** Python 3.10 ou superior; pytest para os testes

```bash
python tools/make_catalog.py --check                 # o catálogo está atualizado (precisa dos repositórios ao lado deste)
python tools/make_brand.py --check                   # o banner, o ícone e o mapa estão atualizados
python tools/make_readmes.py --check                 # os oito README estão atualizados
python tools/make_glance.py --check                  # as tabelas Num relance da família estão atualizadas (precisa dos repositórios ao lado deste)
python tools/publication_check.py                    # nada privado sairia com uma publicação
python tools/check_claims.py --require-siblings      # nenhum README afirma uma capacidade de risco sem o seu estado (precisa dos repositórios ao lado deste)
python tools/check_repo_tools.py --require-siblings  # os ficheiros que cada repositório tem como a mesma cópia são iguais (precisa dos repositórios ao lado deste)
bash tools/check_all.sh                              # as verificações de cada repositório, uma linha por cada um
python tools/urtc_doctor.py                          # o doctor: um relatório sobre esta máquina e sobre cada repositório
python -m pytest tests -q                            # os testes unitários das ferramentas
```

## 🧪 Testes

O conjunto tem 183 testes (`python -m pytest tests -q`). Executam, sobre dados de teste, os geradores do catálogo, da marca, das tabelas Num relance, das tabelas de estado e dos README, as verificações de afirmações, ficheiros partilhados, publicação e o doctor, os vetores de conformidade das notas CAN, e verificam que os README deste repositório são exatamente o que o gerador escreve.

## 🏗️ Compilação e publicação

`build.sh` / `build.bat` instalam o pacote e executam os testes, e `build-test.sh` / `build-test.bat` verificam sem instalar; nenhum altera a versão.

## 📂 Estrutura do repositório

<p align="center">
  <img src="images/repository-structure.svg" alt="Estrutura do repositório URTC-DOCS" width="100%">
</p>

<details>
<summary>Versão em texto da árvore</summary>

```text
URTC-DOCS/
├── docs/                                              arquitetura, interfaces, matriz de capacidades, base de segurança, modelo de ameaças e o catálogo gerado
├── src/urtc_docs/                                     as ferramentas como pacote: catálogo, marca, README, Num relance, estado, verificações
├── tools/                                             scripts finos sobre o pacote, check_all.sh e as verificações de CI partilhadas
├── data/                                              os números de Num relance e as afirmações revistas
├── template/                                          a cópia canónica dos ficheiros que todos os repositórios partilham
├── tests/                                             testes unitários das ferramentas
├── brand/                                             o ícone
├── images/                                            faixa e imagens deste README
├── .github/                                           fluxo de CI e modelos de issues e pull requests
├── build.sh build.bat                                 scripts de compilação
├── build-test.sh build-test.bat                       scripts de compilação e testes que não alteram nada no repositório
├── test.sh test.bat                                   executam os testes
├── run.sh run.bat                                     arrancam o programa
├── urtc.project.json                                  manifesto: versão, papel, maturidade e comando de compilação
├── CHANGELOG.md                                       o que mudou em cada versão
├── SECURITY.md SUPPORT.md                             política de segurança e suporte
├── CONTRIBUTING.md CODE_OF_CONDUCT.md                 como contribuir e código de conduta
├── .gitattributes .gitignore                          definições do Git
├── bump.py bump_version.py bump_manifest_version.py   scripts que sobem a versão
├── LICENSE LICENSE.md                                 licença do software e da documentação
└── pyproject.toml requirements-dev.lock ruff.toml     pacote, ferramentas fixadas e definições de lint
```

</details>

## 🗺️ Roteiro e limites conhecidos

**Limites conhecidos hoje**

* A base de segurança e o modelo de ameaças são escritos a partir dos outros repositórios tal como foram lidos; ninguém fora do projeto os reviu.
* A execução noturna obtém todos os repositórios da família e compara as suas tabelas-resumo, afirmações e estrutura do catálogo; uma versão desatualizada no catálogo é assinalada mas não faz a noite falhar.
* Os documentos descrevem software; não há hardware envolvido e nenhuma afirmação sobre placas foi verificada numa placa.

**A seguir**

* Manter o catálogo, as tabelas Num relance e a matriz de capacidades atualizados à medida que os repositórios mudam.

## 🌍 Idiomas

O README e os textos existem em inglês, espanhol, francês, italiano, alemão, chinês, japonês e português europeu.

## 🔗 Projetos relacionados

O URTC é feito de repositórios independentes, cada um com a sua versão, os seus testes e o seu README. Esta é a família, por grupos:

* **URTC Tool Platform:**
  * [URTC](https://github.com/JuanenRac/URTC) - firmware da placa da cabeça de ferramenta (25 perfis de ferramenta, bootloader CAN) e a referência do protocolo CAN.
  * [URTC-COMMON](https://github.com/JuanenRac/URTC-COMMON) - o protocolo CAN escrito uma só vez como dados (especificação, tabelas geradas, vetores de conformidade) e o código que os programas partilham.
  * [URTC-FLASHER](https://github.com/JuanenRac/URTC-FLASHER) - ferramenta de ambiente de trabalho que atualiza o firmware da placa por CAN ou por SWD/JTAG.
  * [URTC-GATEWAY](https://github.com/JuanenRac/URTC-GATEWAY) - gateway à frente do barramento CAN: só deixa passar os identificadores de uma lista, limita a sua taxa e pede uma chave de sessão.
  * [URTC-SMART-RACK](https://github.com/JuanenRac/URTC-SMART-RACK) - lógica em C independente do hardware e protocolo de comandos para um suporte de ferramentas com pré-aquecimento e acompanhamento do ciclo de vida.
  * [URTC-TESTER](https://github.com/JuanenRac/URTC-TESTER) - testador de ambiente de trabalho do barramento CAN em direto que mostra os controlos e a telemetria do perfil de ferramenta que uma placa reporta.
  * [URTC-VISION-TOOL](https://github.com/JuanenRac/URTC-VISION-TOOL) - protocolo de tramas de sensor em C e um companheiro em Python térmico/RGB para uma cabeça de ferramenta de inspeção.
  * [URTC-WEB-STUDIO](https://github.com/JuanenRac/URTC-WEB-STUDIO) - aplicação de navegador que grava e testa a placa por Web Serial e SLCAN, sem instalar nada.
* **Ecosystem Operations:**
  * [URTC-DEVTOOLS](https://github.com/JuanenRac/URTC-DEVTOOLS) - as ferramentas de repositório partilhadas da família como um conjunto com versão e um ficheiro de bloqueio que distingue uma cópia editada de uma desatualizada.
  * **URTC-DOCS** (este repositório) - arquitetura, interfaces, base de segurança e catálogo gerado do ecossistema, mais as ferramentas que comparam todos os repositórios.
  * [URTC-UPDATER](https://github.com/JuanenRac/URTC-UPDATER) - ferramenta de ambiente de trabalho que deteta, instala e atualiza os repositórios da família URTC, uma ação explícita de cada vez.

**Projetos irmãos (independentes, com a mesma base e as mesmas ferramentas):**

* **[HYDRA-UMC-DOCS](https://github.com/JuanenRac/HYDRA-UMC-DOCS)** - projeto irmão: o centro de documentação do HYDRA-UMC, um ecossistema independente que partilha a base e as ferramentas com este
* **[ARMOR-DOCS](https://github.com/JuanenRac/ARMOR-DOCS)** - projeto irmão: o centro de documentação do A.R.M.O.R., o ecossistema de segurança, também independente e sobre a mesma base
* **[JuanenRac](https://github.com/JuanenRac/JuanenRac)** - o perfil e o painel de estado de todos os ecossistemas

## 📚 Documentação

Onde ler mais:

* [Matriz de capacidades: o que está comprovado e o que não está](docs/CAPABILITY_MATRIX.md)
* [Catálogo de projetos: versões e tipos dos repositórios](docs/PROJECT_CATALOG.md)
* [Protocolo CAN: três implementações de uma especificação em prosa](docs/CAN_PROTOCOL_DUPLICATION.md)
* [Registo de alterações deste repositório](CHANGELOG.md)
* [Licença (GPL-3.0-or-later)](LICENSE)

## 🤝 Contribuir e comunidade

* Antes de um pull request execute `URTC_CI=1 python tools/ci_validate.py`: tem de passar. Veja [CONTRIBUTING.md](CONTRIBUTING.md) e o [código de conduta](CODE_OF_CONDUCT.md).
* O README existe em oito idiomas: uma alteração ao texto faz-se nos oito ficheiros, e as secções partilhadas com outros repositórios são escritas por `tools/readme_sections.py` do URTC-COMMON.
* Não descreva como a funcionar numa placa aquilo que só foi compilado.
* Comunique uma vulnerabilidade em privado: [SECURITY.md](SECURITY.md). Perguntas, ideias e relatórios: electrohobby3d@gmail.com ([SUPPORT.md](SUPPORT.md)).
* Perguntas, ideias e relatórios: electrohobby3d@gmail.com

## 👤 AUTOR

**JuanenRac (Electro Hobby 3D)** · electrohobby3d@gmail.com

## 📜 LICENÇA

Software: GPL-3.0-or-later - ver [LICENSE](LICENSE). Documentação: CC BY-SA 4.0 - ver [LICENSE.md](LICENSE.md).
