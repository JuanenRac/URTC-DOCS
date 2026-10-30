<p align="center">
  <img src="images/URTC_DOCS_BANNER.svg" alt="URTC-DOCS banner" width="100%">
</p>

# 📚 URTC-DOCS

<p align="center"><a href="README.md">🇺🇸 English</a> | <a href="README_spa.md">🇪🇸 Español</a> | <a href="README_fra.md">🇫🇷 Français</a> | <a href="README_ita.md">🇮🇹 Italiano</a> | <a href="README_deu.md">🇩🇪 Deutsch</a> | 🇨🇳 <b>简体中文</b> | <a href="README_jpn.md">🇯🇵 日本語</a> | <a href="README_por.md">🇵🇹 Português</a></p>

### 架构、接口、安全基线，以及关于哪些已被证实的实情

<p align="center">
  <img src="https://img.shields.io/badge/License-GPL%203.0--or--later-blue.svg" alt="GPL 3.0 or later">
  <img src="https://img.shields.io/badge/Format-Markdown-083fa1.svg" alt="Format">
  <img src="https://img.shields.io/badge/Languages-8-00E5FF.svg" alt="Languages">
  <img src="https://img.shields.io/badge/Version-0.1.2-0f6cbd.svg" alt="Version">
  <img src="https://img.shields.io/badge/Maturity-scaffolding-FFB020.svg" alt="Maturity">
</p>

---

**诚实性检查 - 今天真正能运行的部分：** 本仓库包含文档和小工具。这些工具（目录生成器、品牌素材生成器、README 生成器、发布检查和家族检查）是真实的，并有在 CI 中运行的单元测试；夜间工作流会针对家族中的其他仓库运行它们。文档依据这些仓库的 README、清单、变更日志和文档编写，以为本版本阅读时的内容为准，无法追溯到某个仓库的说法会被如实标明。这里的任何内容都不是硬件测试：能力矩阵会对每项能力说明它只是被模拟、在计算机上测试过，还是在真实硬件上运行过，固件仓库也说明目前尚不存在已焊装的电路板。

---

> **安全与安防现状:**本生态系统不是经认证的安全系统,目前也不存在已组装的 URTC 电路板。引导程序使用 CRC32 和共享密钥的 HMAC-SHA256 校验固件映像,而非非对称签名(计划中);已发布的应用映像使用公开的开发密钥签名(`signing_key_kind: dev`),因此任何人都可以生成引导程序接受的映像;尚未向任何真实电路板发送过任何内容。在依赖此处任何说法来保障人身安全之前,请先阅读[安全基线](docs/SECURITY_BASELINE.md)和[威胁模型](docs/THREAT_MODEL.md)。

## 📋 速览

| | |
|---|---|
| 版本 | `0.1.2` |
| 成熟度 | 雏形 |
| 测试 | 153 |
| 技术栈 | Markdown / Mermaid / Python / SVG |
| 目标 | 使用者的电脑 |
| 真实硬件 | 不适用：这里的内容不在硬件上运行 |

**跳转到：** [概述](#-概述) · [架构](#-架构) · [快速开始](#-快速开始) · [测试](#-测试) · [结构](#-仓库结构) · [相关项目](#-相关项目)

## 🚦 项目状态

🟢 已完成并已验证 · 🟡 可用，但有已知限制 · 🟠 做了一半或未验证 · 🔴 未完成或不能用。从未在真实硬件上运行过的内容不会是绿色。

| 部分 | 状态 | 仓库能够证明的内容 |
| --- | :---: | --- |
| 软件 | 🟡 | 目录、品牌和 README 的生成器，以及发布、声明和整个系列的检查，都在电脑上运行；不涉及硬件。 |
| 测试 | 🟡 | 每次推送时，测试套件都会在 CI 中通过，Linux 和 Windows 均如此。 |
| 整个系列的检查 | 🟡 | 每晚的运行会取回系列中的每个仓库，并比较它们的概览表、声明和目录结构；目录中过期的版本会被报告，但不会让当晚的运行失败。 |
| 安全文档 | 🟡 | 安全基线和威胁模型是根据读到的其他仓库内容写成的；项目之外没有人审阅过。 |
| 文档 | 🟡 | 提供八种语言的 README 和参考文档；翻译未经母语者审阅。 |

## 🎯 概述

<p align="center">
  <img src="images/URTC_ECOSYSTEM.svg" alt="URTC ecosystem" width="100%">
</p>

下图显示 URTC 的各个仓库、连接电路板与电脑端工具的 CAN 总线，以及它们的文档所陈述的联系。

* [架构](docs/ARCHITECTURE.md): 分层、数据流、端口和信任边界。
* [接口](docs/INTERFACES.md): 每份契约归谁所有，以及记录在哪里。
* [能力矩阵](docs/CAPABILITY_MATRIX.md): 哪些在软件中已证实、哪些需要硬件，逐个项目说明。
* [安全基线](docs/SECURITY_BASELINE.md): 代码已强制执行的内容和仍然缺少的内容；以及[威胁模型](docs/THREAT_MODEL.md)。
* [第一个垂直切片](docs/FIRST_VERTICAL_SLICE.md): 今天已存在的最小端到端路径。
* [CAN 协议的重复实现](docs/CAN_PROTOCOL_DUPLICATION.md): 该协议依据一份文字说明被实现了三次；共享规范将包含什么。
* [项目目录](docs/PROJECT_CATALOG.md): 生态中的每个仓库，依据其自身清单生成。
* **工具：** `make_catalog.py` 生成目录，`make_brand.py` 生成横幅、图标和家族图，`make_readmes.py` 生成本仓库的八份 README，`publication_check.py` 在发布前查找任何私有内容，`check_all.sh` 运行家族中每个仓库自己的检查，并为每个仓库输出一行 PASS、FAIL 或 SKIP。`make_glance.py` 根据每个仓库的清单和 `data/glance.json` 生成其“速览”表（`--check` 比较，`--apply` 写入）；提升版本后，运行 `python tools/make_glance.py --apply --repo NAME` 即可刷新该仓库的表。`check_claims.py` 读取该系列每个仓库的英文 README,当某个句子含有风险词(E-STOP、联锁、实时、已签名、mTLS、FDCAN、YOLO、AI 驱动、自主、已认证等)而旁边没有状态标记(计划中、未实现、可选、默认关闭、模拟、已测试等),且不在人工对照代码读过并登记于 `data/claims_reviewed.json` 的行中时,检查失败。 `check_repo_tools.py` 比较每个仓库作为同一份副本携带的文件(文档策略与 README 一致性检查、清单版本升级工具、通知仪表板的工作流),任何一个不同就会失败。 `sync_repo_tools.py` 会把这些文件的规范副本(`template/eh3d-repo-template`)写入每个仓库,并保留各文件的换行符;不带 `--apply` 时只列出将会改变的内容。 `urtc_doctor.py` 是唯一的入口：它生成一份报告，包含本机工具（Python、git、Node、ARM 编译器、PySide6、串口）、每个仓库的版本（清单、源文件和最新的 changelog 条目）、URTC-COMMON 的副本以及烧录工具和 Web 工作室内置的固件、每个仓库的验证和本仓库的检查；`--fast` 跳过验证，`--online` 将内置固件与最新发布版本比较。

## 🧩 在 URTC 中的角色

URTC-DOCS 是整个生态的记忆：架构、接口、安全基线和能力矩阵都放在这里，同时也保存着把所有仓库并排比较的工具。每个仓库保留自己的 README、测试和契约；本仓库说明它们如何配合，以及真正证实了什么。

## 🏛️ 架构

<p align="center">
  <img src="images/architecture.svg" alt="URTC-DOCS 的架构：读取什么、包含什么、供给什么" width="100%">
</p>

本仓库各部分如何协作。图片由 `docs/architecture.json` 绘制，并与代码核对。

## 🚀 快速开始

**要求：** Python 3.10 或更新版本；测试需要 pytest

```bash
python tools/make_catalog.py --check                 # 目录是最新的（需要本仓库旁边有其他仓库）
python tools/make_brand.py --check                   # 横幅、图标和家族图是最新的
python tools/make_readmes.py --check                 # 八份 README 是最新的
python tools/make_glance.py --check                  # 家族的“速览”表是最新的（需要本仓库旁边有其他仓库）
python tools/publication_check.py                    # 发布时不会带出任何私有内容
python tools/check_claims.py --require-siblings      # 没有任何 README 在不说明状态的情况下声称具备高风险能力(需要与本仓库相邻的其他仓库)
python tools/check_repo_tools.py --require-siblings  # 每个仓库作为同一份副本携带的文件内容一致(需要与本仓库相邻的其他仓库)
bash tools/check_all.sh                              # 每个仓库的检查，每个一行
python tools/urtc_doctor.py                          # 医生：关于本机和每个仓库的一份报告
python -m pytest tests -q                            # 工具的单元测试
```

## 🧪 测试

测试套件共有 153 个测试（`python -m pytest tests -q`）。它们用测试数据运行目录、品牌、速览表、状态表和 README 的生成器，运行声明、共用文件、发布和 doctor 的检查，运行 CAN 说明的一致性向量，并检查本仓库的 README 与生成器写出的内容完全一致。

## 🏗️ 构建与发布

`build.sh` / `build.bat` 安装包并运行测试，`build-test.sh` / `build-test.bat` 不安装直接检查；两者都不会改变版本。

## 📂 仓库结构

<p align="center">
  <img src="images/repository-structure.svg" alt="URTC-DOCS 的仓库结构" width="100%">
</p>

<details>
<summary>目录树的文本版</summary>

```text
URTC-DOCS/
├── docs/                                              架构、接口、能力矩阵、安全基线、威胁模型和生成的目录
├── src/urtc_docs/                                     以软件包形式提供的工具：目录、品牌、README、速览、状态和检查
├── tools/                                             封装在软件包之上的轻量脚本、check_all.sh 以及共用的 CI 检查
├── data/                                              速览中的数字和已审阅的声明
├── template/                                          各仓库共用文件的标准副本
├── tests/                                             工具的单元测试
├── brand/                                             图标
├── images/                                            横幅和本 README 的图片
├── .github/                                           CI 工作流以及 Issue 和 Pull Request 模板
├── build.sh build.bat                                 构建脚本
├── build-test.sh build-test.bat                       构建并测试的脚本，不会修改仓库内容
├── test.sh test.bat                                   运行测试
├── run.sh run.bat                                     启动程序
├── urtc.project.json                                  清单：版本、角色、成熟度和构建命令
├── CHANGELOG.md                                       每个版本的变更
├── SECURITY.md SUPPORT.md                             安全政策和支持
├── CONTRIBUTING.md CODE_OF_CONDUCT.md                 如何参与贡献和行为准则
├── .gitattributes .gitignore                          Git 设置
├── bump.py bump_version.py bump_manifest_version.py   提升版本号的脚本
├── LICENSE LICENSE.md                                 软件许可证和文档许可证
└── pyproject.toml requirements-dev.lock ruff.toml     软件包、锁定的工具和 lint 设置
```

</details>

## 🗺️ 路线图与已知限制

**目前已知的限制**

* 安全基线和威胁模型是根据阅读时的其他仓库写成的；项目之外没有人审阅过。
* 夜间运行会获取家族中的每个仓库，并比较它们的汇总表、声明和目录结构；目录中的过期版本会被报告，但不会让当晚运行失败。
* 这些文档描述的是软件；不涉及硬件，关于板子的声明也没有在板子上验证过。

**下一步**

* 随着各仓库的变化，保持目录、速览表和能力矩阵为最新。

## 🌍 语言

README 和文本提供英语、西班牙语、法语、意大利语、德语、汉语、日语和欧洲葡萄牙语版本。

## 🔗 相关项目

URTC 由相互独立的仓库组成，每个仓库都有自己的版本、测试和 README。以下是按组划分的家族：

* **URTC Tool Platform:**
  * [URTC](https://github.com/JuanenRac/URTC) - 工具头电路板的固件(25 个工具配置、CAN 引导程序)以及 CAN 协议参考。
  * [URTC-COMMON](https://github.com/JuanenRac/URTC-COMMON) - 只写一次的 CAN 协议数据(规范、生成的表格、一致性向量)以及各程序共享的代码。
  * [URTC-FLASHER](https://github.com/JuanenRac/URTC-FLASHER) - 通过 CAN 或 SWD/JTAG 更新电路板固件的桌面工具。
  * [URTC-GATEWAY](https://github.com/JuanenRac/URTC-GATEWAY) - 位于 CAN 总线前的网关:只放行列表中的标识符,限制其速率,并要求会话密钥。
  * [URTC-SMART-RACK](https://github.com/JuanenRac/URTC-SMART-RACK) - 用于带预热和生命周期跟踪的工具架的、与硬件无关的 C 逻辑和命令协议。
  * [URTC-TESTER](https://github.com/JuanenRac/URTC-TESTER) - 桌面实时 CAN 总线测试器,显示电路板所报告工具配置的控件和遥测。
  * [URTC-VISION-TOOL](https://github.com/JuanenRac/URTC-VISION-TOOL) - C 语言的传感器帧协议,以及用于检测工具头的 Python 热成像/RGB 配套程序。
  * [URTC-WEB-STUDIO](https://github.com/JuanenRac/URTC-WEB-STUDIO) - 通过 Web Serial 和 SLCAN 烧录并测试电路板的浏览器应用,无需安装。
* **Ecosystem Operations:**
  * [URTC-DEVTOOLS](https://github.com/JuanenRac/URTC-DEVTOOLS) - 家族共用的仓库工具，作为带版本的整套工具，并用锁文件区分被改动的副本和已过时的副本。
  * **URTC-DOCS** (本仓库) - 生态系统的架构、接口、安全基线和生成的目录,以及比较所有仓库的工具。
  * [URTC-UPDATER](https://github.com/JuanenRac/URTC-UPDATER) - 检测、安装并更新 URTC 家族仓库的桌面工具,每次只执行一个明确的操作。

**姊妹项目（相互独立，共用同一基础和工具）：**

* **[HYDRA-UMC-DOCS](https://github.com/JuanenRac/HYDRA-UMC-DOCS)** - 姊妹项目：HYDRA-UMC 的文档中心，一个独立的生态，与本生态共用基础和工具
* **[ARMOR-DOCS](https://github.com/JuanenRac/ARMOR-DOCS)** - 姊妹项目：A.R.M.O.R. 安全生态的文档中心，同样独立，建立在同一基础上
* **[JuanenRac](https://github.com/JuanenRac/JuanenRac)** - 所有生态的个人主页和状态面板

## 📚 文档

更多阅读：

* [能力矩阵：哪些已证实，哪些没有](docs/CAPABILITY_MATRIX.md)
* [项目目录：各仓库的版本和类型](docs/PROJECT_CATALOG.md)
* [CAN 协议：同一份文字规范的三个实现](docs/CAN_PROTOCOL_DUPLICATION.md)
* [本仓库的变更日志](CHANGELOG.md)
* [许可证 (GPL-3.0-or-later)](LICENSE)

## 🤝 参与贡献与社区

* 提交 Pull Request 之前请运行 `URTC_CI=1 python tools/ci_validate.py`：必须通过。参见 [CONTRIBUTING.md](CONTRIBUTING.md) 和[行为准则](CODE_OF_CONDUCT.md)。
* README 有八种语言：修改文字时要同步修改全部八个文件，与其他仓库共用的章节由 URTC-COMMON 的 `tools/readme_sections.py` 写入。
* 不要把仅仅构建过的东西描述为已在板子上运行。
* 请私下报告漏洞：[SECURITY.md](SECURITY.md)。问题、想法和报告：electrohobby3d@gmail.com（[SUPPORT.md](SUPPORT.md)）。
* 问题、想法和报告：electrohobby3d@gmail.com

## 👤 作者

**JuanenRac (Electro Hobby 3D)** · electrohobby3d@gmail.com

## 📜 许可证

软件：GPL-3.0-or-later - 见 [LICENSE](LICENSE)。文档：CC BY-SA 4.0 - 见 [LICENSE.md](LICENSE.md)。
