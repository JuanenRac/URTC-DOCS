<p align="center">
  <img src="images/URTC_DOCS_BANNER.svg" alt="URTC-DOCS banner" width="100%">
</p>

# 📚 URTC-DOCS

<p align="center"><a href="README.md">🇺🇸 English</a> | <a href="README_spa.md">🇪🇸 Español</a> | <a href="README_fra.md">🇫🇷 Français</a> | <a href="README_ita.md">🇮🇹 Italiano</a> | <a href="README_deu.md">🇩🇪 Deutsch</a> | <a href="README_zho.md">🇨🇳 简体中文</a> | 🇯🇵 <b>日本語</b> | <a href="README_por.md">🇵🇹 Português</a></p>

### アーキテクチャ、インターフェース、セキュリティ基準、そして何が実証済みかという事実

<p align="center">
  <img src="https://img.shields.io/badge/License-GPL%203.0--or--later-blue.svg" alt="GPL 3.0 or later">
  <img src="https://img.shields.io/badge/Format-Markdown-083fa1.svg" alt="Format">
  <img src="https://img.shields.io/badge/Languages-8-00E5FF.svg" alt="Languages">
  <img src="https://img.shields.io/badge/Version-0.0.5-0f6cbd.svg" alt="Version">
  <img src="https://img.shields.io/badge/Maturity-scaffolding-FFB020.svg" alt="Maturity">
</p>

---

**正直さの確認 - 今日実際に動くもの：** このリポジトリにはドキュメントと小さなツールがあります。ツール（カタログ生成、ブランド素材生成、README 生成、公開前チェック、ファミリーチェック）は実在し、CI で実行される単体テストがあります。夜間ワークフローは、ファミリーの他のリポジトリに対してそれらを実行します。ドキュメントは、このバージョンのために読んだ時点の各リポジトリの README、マニフェスト、変更履歴、ドキュメントから書かれており、リポジトリまでたどれなかった記述はその旨を明記しています。ここにあるものはハードウェアテストではありません。能力マトリクスは各能力について、シミュレーションのみか、コンピュータ上でテスト済みか、実機で動作したかを示します。ファームウェアのリポジトリは、実装済みの基板がまだ存在しないと述べています。

---

> **安全性とセキュリティの現状:** このエコシステムは認証された安全システムではなく、実装済みの URTC 基板もまだ存在しません。ブートローダーはファームウェアイメージを CRC32 と共有鍵の HMAC-SHA256 で検査しており、非対称署名ではありません(予定)。公開されているアプリケーションイメージは公開の開発用鍵(`signing_key_kind: dev`)で署名されているため、誰でもブートローダーが受け入れるイメージを作れます。実際の基板には何も送信されていません。ここに書かれた内容を人の安全のために頼る前に、[セキュリティベースライン](docs/SECURITY_BASELINE.md)と[脅威モデル](docs/THREAT_MODEL.md)をお読みください。

## 📋 ひと目で

| | |
|---|---|
| バージョン | `0.0.5` |
| 成熟度 | 足場段階 |
| 技術 | Markdown / Mermaid / Python / SVG |
| 対象 | 利用者の PC |
| 実機での確認 | 対象外：ここにあるものはハードウェア上では動きません |

## 🎯 概要

<p align="center">
  <img src="images/URTC_ECOSYSTEM.svg" alt="URTC ecosystem" width="100%">
</p>

下の図は、URTC のリポジトリ、基板とパソコン側ツールをつなぐ CAN バス、そして各ドキュメントが述べる関係を示します。

* [アーキテクチャ](docs/ARCHITECTURE.md): レイヤー、データの流れ、ポート、信頼境界。
* [インターフェース](docs/INTERFACES.md): 各契約の所有者と、その文書の場所。
* [能力マトリクス](docs/CAPABILITY_MATRIX.md): ソフトウェアで実証済みのものとハードウェアが必要なものを、プロジェクトごとに。
* [セキュリティ基準](docs/SECURITY_BASELINE.md): コードが強制していることとまだ足りないこと。および[脅威モデル](docs/THREAT_MODEL.md)。
* [最初の垂直スライス](docs/FIRST_VERTICAL_SLICE.md): 今日存在する最小のエンドツーエンド経路。
* [CAN プロトコルの重複実装](docs/CAN_PROTOCOL_DUPLICATION.md): プロトコルは文章の説明から三回実装されています。共有仕様に含まれるはずの内容。
* [プロジェクトカタログ](docs/PROJECT_CATALOG.md): エコシステムの全リポジトリを、それぞれのマニフェストから生成。
* **ツール：** `make_catalog.py` はカタログを、`make_brand.py` はバナー・アイコン・ファミリーマップを、`make_readmes.py` はこのリポジトリの 8 つの README を書きます。`publication_check.py` は公開前に非公開のものを探し、`check_all.sh` はファミリーの各リポジトリ自身のチェックを実行して、1 件ごとに PASS、FAIL、SKIP の 1 行を出力します。 `make_glance.py` は各リポジトリのマニフェストと `data/glance.json` から「ひと目で」の表を書きます（`--check` は比較、`--apply` は書き込み）。バージョンを上げた後は `python tools/make_glance.py --apply --repo NAME` でそのリポジトリの表を更新します。`check_claims.py` は、ファミリーの各リポジトリの英語 README を読み、リスクのある語(E-STOP、インターロック、リアルタイム、署名済み、mTLS、FDCAN、YOLO、AI 駆動、自律、認証済みなど)を含む文の隣に状態の印(計画中、未実装、任意、既定で無効、シミュレーション、テスト済みなど)がなく、かつ担当者がコードと突き合わせて読み `data/claims_reviewed.json` に登録した行でもない場合に失敗します。 `urtc_doctor.py` は唯一の入口です。マシンのツール（Python、git、Node、ARM コンパイラー、PySide6、シリアルポート）、各リポジトリのバージョン（マニフェスト、ソースファイル、changelog の最新エントリ）、URTC-COMMON のコピー、フラッシャーと Web スタジオに同梱されたファームウェア、各リポジトリの検証、そしてこのリポジトリのチェックを 1 つのレポートにまとめます。`--fast` は検証を省略し、`--online` は同梱ファームウェアを最新リリースと比較します。

## 🧩 URTC での役割

URTC-DOCS はエコシステムの記憶です。アーキテクチャ、インターフェース、セキュリティ基準、能力マトリクスがここにあり、すべてのリポジトリを並べて比較するツールもここに置かれています。各リポジトリは自分の README、テスト、契約を持ち続けます。このリポジトリは、それらがどう組み合わさるか、そして実際に何が実証されたかを述べます。

## 📂 リポジトリ構成

```text
URTC-DOCS/
├── docs/     アーキテクチャ、インターフェース、能力マトリクス、セキュリティ基準、脅威モデル、最初のスライス、CAN プロトコルのメモ、生成されたカタログ
├── src/      パッケージとしてのツール（カタログ、ブランド、README、公開前チェック）
├── tools/    パッケージの上の薄いスクリプト、check_all.sh、エコシステム共通の CI チェック
├── tests/    ツールの単体テスト
├── images/   バナーとエコシステムマップ
├── brand/    アイコン
├── build.sh / build.bat, build-test.sh / build-test.bat, run.sh / run.bat
└── urtc.project.json, pyproject.toml, CHANGELOG.md, LICENSE, LICENSE.md
```

## 🛠️ ビルドと実行

**必要なもの：** Python 3.10 以降、テスト用に pytest

```bash
python tools/make_catalog.py --check             # カタログが最新（このリポジトリの隣に他のリポジトリが必要）
python tools/make_brand.py --check               # バナー、アイコン、マップが最新
python tools/make_readmes.py --check             # 8 つの README が最新
python tools/make_glance.py --check              # ファミリー全体の「ひと目で」の表が最新（このリポジトリの隣に他のリポジトリが必要）
python tools/publication_check.py                # 公開で非公開のものが外に出ない
python tools/check_claims.py --require-siblings  # どの README も、状態を示さずにリスクのある機能を主張していない(このリポジトリの隣に他のリポジトリが必要)
bash tools/check_all.sh                          # 各リポジトリのチェックを 1 行ずつ
python tools/urtc_doctor.py                      # ドクター：このマシンと各リポジトリについての 1 つのレポート
python -m pytest tests -q                        # ツールの単体テスト
```

`build.sh` / `build.bat` はバージョンを 1 段階上げ（エコシステムのオドメーター方式）、パッケージをインストールしてテストを実行します。`build-test.sh` / `build-test.bat` はバージョンを変えずに確認します。

## 🔗 関連プロジェクト

URTC は独立したリポジトリで構成され、それぞれに固有のバージョン、テスト、README があります。グループ別のファミリーは次のとおりです：

* **URTC Tool Platform:** [URTC](https://github.com/JuanenRac/URTC), [URTC-COMMON](https://github.com/JuanenRac/URTC-COMMON), [URTC-FLASHER](https://github.com/JuanenRac/URTC-FLASHER), [URTC-SMART-RACK](https://github.com/JuanenRac/URTC-SMART-RACK), [URTC-TESTER](https://github.com/JuanenRac/URTC-TESTER), [URTC-VISION-TOOL](https://github.com/JuanenRac/URTC-VISION-TOOL), [URTC-WEB-STUDIO](https://github.com/JuanenRac/URTC-WEB-STUDIO)
* **Ecosystem Operations:** **URTC-DOCS** (このリポジトリ), [URTC-UPDATER](https://github.com/JuanenRac/URTC-UPDATER)

**URTC の外：**

* **[HYDRA-UMC](https://github.com/JuanenRac/HYDRA-UMC)** - ロボットアームのマザーボード。そのCANリレーが、ツールヘッドが接続されるバスとして文書化されています
* **[HYDRA-UMC-DOCS](https://github.com/JuanenRac/HYDRA-UMC-DOCS)** - HYDRA-UMC エコシステム向けの同じ考え方
* **[ARMOR-DOCS](https://github.com/JuanenRac/ARMOR-DOCS)** - A.R.M.O.R. セキュリティエコシステム向けの同じ考え方
* **[JuanenRac](https://github.com/JuanenRac/JuanenRac)** - すべてのエコシステムのプロフィールとステータスダッシュボード

## 📚 ドキュメントとコミュニティ

さらに読むには：

* [能力マトリクス：実証済みのものとそうでないもの](docs/CAPABILITY_MATRIX.md)
* [プロジェクトカタログ：各リポジトリのバージョンと種類](docs/PROJECT_CATALOG.md)
* [CAN プロトコル：文章による一つの仕様の三つの実装](docs/CAN_PROTOCOL_DUPLICATION.md)
* [このリポジトリの変更履歴](CHANGELOG.md)
* [ライセンス (GPL-3.0-or-later)](LICENSE)
* 質問、アイデア、報告：electrohobby3d@gmail.com

## 👤 作者

**JuanenRac (Electro Hobby 3D)** · electrohobby3d@gmail.com

## 📜 ライセンス

ソフトウェア：GPL-3.0-or-later - [LICENSE](LICENSE) を参照。ドキュメント：CC BY-SA 4.0 - [LICENSE.md](LICENSE.md) を参照。
