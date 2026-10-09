# 評価環境：エージェントの実行環境を個人のシェル設定から切り離し、`.venv`を明示的に有効にする計画（r1）

2026-10-09。利用者の依頼（選択肢2で進める。Claudeの実行環境を変更したいので、次のタスクで実行する内容として整理する）を受けて、次のタスクで行う作業を固定する計画。この記録では、コードの変更もモデルの実行もしない。評価基盤の保守は、ルートの`CLAUDE.md`のとおり、利用者が明示的に依頼した別作業として行う。

## 目的

- Codex（Sol Low）とClaude Code（Sonnet low）の両方で、エージェントがコマンドを実行する環境を、計測するMacの個人のシェル設定から切り離す。
- そのうえで、評価の起動処理が、作業ツリーの`.venv`を明示的に有効にする。モデルが`python`、`python3`、`pytest`をそのまま実行しても、`.venv`のものが使われる状態にする。
- これにより、二つのエージェントの実行環境の差（[処理の適切さの分類](c280-c300-processing-appropriateness-audit-r1.md)の追記）をなくし、計測の隔離と再現性を保つ。

## 背景：現在の状態

[処理の適切さの分類](c280-c300-processing-appropriateness-audit-r1.md)の追記で確かめた事実をまとめる。

| 項目 | Codex（Sol Low） | Claude Code（Sonnet low） |
| --- | --- | --- |
| エージェントへ渡す環境 | 計測プロセスの環境をそのまま複製（`scripts/run_codex_evaluation.py`の`command_environment = os.environ.copy()`、起動用の`isolated_adapter.py`の`env=os.environ.copy()`） | 最小限の固定値（`scripts/run_claude_evaluation.py`の`minimal_environment`と、計測の条件の`agent_environment.claude_code.process_environment`） |
| PATH | 計測を始めたシェルのPATH（個人の設定を含む） | `/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin` |
| シェル | `SHELL=/bin/zsh`。コマンドはzshで実行され、`~/.zshenv`が読まれる（ログからの推定を含む） | `SHELL=/bin/bash`。`~/.bashrc`などは計測のMacにない |
| `.venv`の扱い | `~/.zshenv`が、THE-CAPTIONの`configs/zsh/the-caption.zsh`を読み込み、`python`・`python3`・`pip`・`pytest`を`.venv`へ振り向ける | 有効にならない。`python`はなく、`python3`は`/opt/homebrew/bin/python3`（pytestなし） |
| 作業ツリーの`.venv` | 両方とも、評価の起動処理が`runtime_links`（`materialization: venv_shim`、元は共有の`environment/.venv`）で作業ツリーの`.venv`を作る | 同左 |

問題は二つある。

1. Claude Codeでは`.venv`が有効にならず、TaskSpecが実行方法を指定しないケース（A02）で、テストの確認が失敗し、中断されていた。
2. Codexでは`.venv`が有効になるが、それは計測したMacの個人のシェル設定（`~/.zshenv`）に依存している。同じ評価を別のMacや別の利用者の環境で行うと、結果が変わりうる。

## 目標の状態

- 両エージェントとも、エージェントのプロセスへ渡す環境を、評価の起動処理が固定した値だけで作る。計測プロセスの環境を丸ごと複製しない。
- PATHの先頭に、作業ツリーの`.venv/bin`（絶対パス）を置き、`VIRTUAL_ENV`に作業ツリーの`.venv`を設定する。残りのPATHは、両エージェント共通の固定値とする。
- エージェントがコマンドを実行するシェルで、個人のシェル設定（`~/.zshenv`、`~/.zshrc`、`~/.bashrc`など）が読まれないようにする。
- 各runで、実際に使われた環境（PATH、`VIRTUAL_ENV`、シェル、個人の設定ファイルを読んだかどうか、`python3`と`pytest`の解決先）を、記録として残す。

## 次のタスクで行う作業

### 1. 実装前の確認（読み取りと小さな実験だけ）

1. **Codexがコマンドを実行するシェルの決まり方。** `SHELL`環境変数で決まるのか、ユーザーのログインシェル（OSのユーザー情報）で決まるのかを、Codex CLI 0.159.0で確かめる。
2. **zshの個人設定を読ませない方法。** `ZDOTDIR`を空のディレクトリに向ければ`~/.zshenv`が読まれないかを確かめる。計測のMacには`/etc/zshenv`がなく、`/etc/zprofile`はある。Codexを`bash`で動かせるなら、その方法も比べる。Codexの`shell_environment_policy`の設定（`--ignore-user-config`との関係を含む）で環境を固定できるかも確かめる。
3. **Claude Codeの`Bash`ツールが使う環境。** プロセスに渡したPATHと`VIRTUAL_ENV`が、`Bash`ツールのコマンドにそのまま届くかを確かめる。Claude Codeがシェルの設定を読み込む仕組み（シェルのスナップショット）が、`SHELL=/bin/bash`のときに個人の設定を読まないことも確かめる。
4. 1〜3は、評価用の作業ツリーではない一時ディレクトリで、`command -v python3`、`python3 -c "import pytest"`、`echo $VIRTUAL_ENV`のような確認コマンドだけで行う。

### 2. 起動処理の変更

- `scripts/run_claude_evaluation.py`：`minimal_environment`に、作業ツリーの`.venv/bin`をPATHの先頭に加える処理と、`VIRTUAL_ENV`の設定を加える。作業ツリーのパスはrunごとに違うため、固定値の`process_environment`には書かず、起動処理が組み立てる。
- `scripts/run_codex_evaluation.py`：`command_environment = os.environ.copy()`をやめ、固定の環境（Claudeと同じ考え方）を組み立てる。個人のシェル設定を読ませない設定（1の2で決めた方法）を加える。認証や`CODEX_HOME`など、Codexの起動に必要な値は明示的に渡す。
- 計測ディレクトリの`isolated_adapter.py`（Codexの起動用）も、`os.environ.copy()`をそのまま渡さない形にする。
- 各runの記録に、実際の環境の記録（目標の状態の最後の項目）を加える。

### 3. テスト

- 二つの起動処理について、渡す環境が固定値と作業ツリーの`.venv`だけからなること、個人の設定を示す値（計測プロセスのPATHなど）が混ざらないことを、単体テストで確かめる。
- `tests/test_kpi_revision_guard.py`など、KPIの数え方を固定するテストが変わらないことを確かめる。

### 4. 計測の条件と系列

- 実行環境が変わるため、新しい評価系列とする。保存済みのC280〜C300の結果とは比較しない（`PROMPT_ONLY_COMPARISON`）。
- 計測の条件の`agent_environment`に、実行環境の版（例：`shell_environment.revision`）、固定のPATH、`.venv`の有効化の方法を、結果の値を変えうる条件として加える。評価コードのSHA-256は`effective-v1`では記録だけの項目なので、環境の変更をコードのSHA-256の違いだけで表さない（[`evaluations/AGENTS.md`](../evaluations/AGENTS.md)の互換条件）。
- プロファイルは新しいrevisionとして作る。既存のプロファイルと結果は書き換えない。

### 5. 確かめの実行（登録しない診断）

- A02だけを、両エージェントで各N=2程度実行し、次を確かめる。登録結果にはしない。
  - `python3 -m pytest`と`python -m pytest`が`.venv`で動くこと。
  - 個人のシェル設定が読まれていないこと（各runの環境の記録で確かめる）。
  - 品質の採点が従来どおり動くこと。

### 6. 新しい系列の基準の計測

- 新しい系列の基準として、C280をSol LowとSonnet lowで各Standard14 N=5測る。
- その後にどのCandidate（C299、C300など）を測るかは、基準の結果を見てから利用者が決める。

## 停止条件

- 1の確認で、個人のシェル設定を読ませない方法が見つからない場合は、実装へ進まず、利用者に報告する。
- 5の確かめで、`.venv`が有効にならない、または個人の設定が読まれていた場合は、6へ進まない。
- 既存の結果、プロファイル、計測ディレクトリは変更しない。

## この計画で決めないこと

- プロンプトの変更。この作業は評価環境だけを変える。
- 新しい系列の基準の結果を、保存済みの系列と比べてプロンプトの効果を論じること。
- 採用、release、本体反映。

## 参照

[処理の適切さの分類](c280-c300-processing-appropriateness-audit-r1.md)、[判定基準](shared-instruction-evaluation-criteria-r1.md)、[`evaluations/AGENTS.md`](../evaluations/AGENTS.md)、[評価実行マニュアル](evaluation-loop-manual.md)、[CodexのCLIの版の共存環境の設計](codex-cli-version-coexistence-environment-design.md)、[Claudeのランタイムの表面とプラグインの方針](claude-runtime-surface-plugin-policy.md)。
