# =============================================================================
# URTC-DOCS - src/urtc_docs/readme_drift_text.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""The words about the shared-file check that README.md and its translations add to the generated text.

``TOOLS`` documents ``tools/check_repo_tools.py`` in the list of tools; ``COMMENT`` is the comment of its command in
the build and run block.
"""
from __future__ import annotations

TOOLS: dict[str, str] = {
    "en": " `check_repo_tools.py` compares the files every repository carries as the same copy (the documentation-policy and README-parity checks, the manifest version bumper, the dashboard notifier workflow) and fails when one differs. `sync_repo_tools.py` puts the canonical copy of those files (`template/eh3d-repo-template`) into every repository, keeping each file's line endings; without `--apply` it only lists what would change.",
    "es": " `check_repo_tools.py` compara los archivos que cada repositorio lleva como la misma copia (las comprobaciones de política de documentación y de paridad de README, el actualizador de versión del manifiesto, el workflow que avisa al panel) y falla cuando uno difiere. `sync_repo_tools.py` copia la versión canónica de esos archivos (`template/eh3d-repo-template`) en cada repositorio, respetando los finales de línea de cada archivo; sin `--apply` solo lista lo que cambiaría.",
    "de": " `check_repo_tools.py` vergleicht die Dateien, die jedes Repository als dieselbe Kopie führt (die Prüfungen der Dokumentationsrichtlinie und der README-Parität, das Werkzeug zum Erhöhen der Manifestversion, der Workflow für die Dashboard-Meldung), und schlägt fehl, wenn eine abweicht. `sync_repo_tools.py` schreibt die kanonische Kopie dieser Dateien (`template/eh3d-repo-template`) in jedes Repository und behält dabei die Zeilenenden jeder Datei; ohne `--apply` listet es nur auf, was sich ändern würde.",
    "fr": " `check_repo_tools.py` compare les fichiers que chaque dépôt porte comme la même copie (les contrôles de politique de documentation et de parité des README, l'outil de montée de version du manifeste, le workflow d'avis au tableau de bord) et échoue lorsqu'un fichier diffère. `sync_repo_tools.py` écrit la copie canonique de ces fichiers (`template/eh3d-repo-template`) dans chaque dépôt en conservant les fins de ligne de chaque fichier ; sans `--apply` il liste seulement ce qui changerait.",
    "it": " `check_repo_tools.py` confronta i file che ogni repository porta come la stessa copia (i controlli della politica di documentazione e della parità dei README, lo strumento che aumenta la versione del manifesto, il workflow che avvisa la dashboard) e fallisce quando uno differisce. `sync_repo_tools.py` scrive la copia canonica di quei file (`template/eh3d-repo-template`) in ogni repository, mantenendo le terminazioni di riga di ciascun file; senza `--apply` elenca soltanto ciò che cambierebbe.",
    "ja": " `check_repo_tools.py` は、各リポジトリが同一のコピーとして持つファイル(ドキュメント方針と README 同等性の検査、マニフェストのバージョン更新ツール、ダッシュボードへ通知するワークフロー)を比較し、どれかが異なると失敗します。 `sync_repo_tools.py` は、それらのファイルの正規コピー(`template/eh3d-repo-template`)を各ファイルの改行コードを保ったまま全リポジトリへ書き込みます。`--apply` を付けない場合は、変更される内容を一覧表示するだけです。",
    "zh": " `check_repo_tools.py` 比较每个仓库作为同一份副本携带的文件(文档策略与 README 一致性检查、清单版本升级工具、通知仪表板的工作流),任何一个不同就会失败。 `sync_repo_tools.py` 会把这些文件的规范副本(`template/eh3d-repo-template`)写入每个仓库,并保留各文件的换行符;不带 `--apply` 时只列出将会改变的内容。",
    "pt": " `check_repo_tools.py` compara os ficheiros que cada repositório tem como a mesma cópia (as verificações da política de documentação e da paridade dos README, a ferramenta que sobe a versão do manifesto, o workflow que avisa o painel) e falha quando um difere. `sync_repo_tools.py` escreve a cópia canónica desses ficheiros (`template/eh3d-repo-template`) em cada repositório, mantendo os fins de linha de cada ficheiro; sem `--apply` apenas lista o que mudaria.",
}

COMMENT: dict[str, str] = {
    "en": "the files every repository carries as the same copy are the same (needs the repositories next to this one)",
    "es": "los archivos que cada repositorio lleva como la misma copia son iguales (necesita los repositorios junto a este)",
    "de": "die Dateien, die jedes Repository als dieselbe Kopie führt, sind gleich (braucht die Repositorys neben diesem)",
    "fr": "les fichiers que chaque dépôt porte comme la même copie sont identiques (nécessite les dépôts à côté de celui-ci)",
    "it": "i file che ogni repository porta come la stessa copia sono uguali (richiede i repository accanto a questo)",
    "ja": "各リポジトリが同一コピーとして持つファイルは同じ内容(このリポジトリの隣に他のリポジトリが必要)",
    "zh": "每个仓库作为同一份副本携带的文件内容一致(需要与本仓库相邻的其他仓库)",
    "pt": "os ficheiros que cada repositório tem como a mesma cópia são iguais (precisa dos repositórios ao lado deste)",
}
