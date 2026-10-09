# 評価環境：エージェントの実行環境の切り離しと`.venv`の有効化の実施記録（r1）

2026-10-09。[計画](agent-runtime-venv-isolation-plan-r1.md)の1〜5を実施した記録。6（新しい系列の基準の計測）は、この記録の時点では実施していない。評価基盤の保守は、ルートの`CLAUDE.md`のとおり、利用者が明示的に依頼した別作業として行った。プロンプトは変更していない。

## 1. 実装前の確認の結果

評価用の作業ツリーではない一時ディレクトリに、起動処理と同じ方法（`venv_shim`）で`.venv`を作り、Codex CLI 0.159.0（`gpt-6.1-sol` low）とClaude Code 2.1.288（`claude-sonnet-5-5` low）に、同じ確認用のコマンドを一回だけ実行させた。

### Codex

| 渡した環境と設定 | 実行したシェル | `~/.zshenv` | `python3`の解決先 |
| --- | --- | --- | --- |
| 計測プロセスの環境を複製（従来） | zsh（非ログイン、スナップショット経由） | 読まれた | `/opt/homebrew/bin/python3` |
| 固定の環境、`SHELL=/bin/bash` | zsh | 読まれた | `/opt/homebrew/bin/python3` |
| 固定の環境、`ZDOTDIR`を空のディレクトリ | zsh | 読まれない | `/usr/bin/python3`（`.venv/bin`がPATHの末尾へ移動） |
| 上に加えて`--disable shell_snapshot` | zsh（ログイン） | 読まれない | `/usr/bin/python3`（同上） |
| 固定の環境、`ZDOTDIR`を空のディレクトリ、`-c allow_login_shell=false` | zsh（非ログイン） | 読まれない | 作業ツリーの`.venv/bin/python3` |

- Codexがコマンドを実行するシェルは、`SHELL`環境変数ではなく、OSのユーザー情報のログインシェルで決まる。`SHELL=/bin/bash`を渡してもzshで実行された。
- `ZDOTDIR`を空のディレクトリに向けると、`~/.zshenv`は読まれない。ただし、Codexはシェルの設定をログインシェルとして取り込むため、`/etc/zprofile`の`path_helper`がPATHを並べ替え、`.venv/bin`がシステムのパスより後ろへ回る。
- `-c allow_login_shell=false`を加えると、ログインシェルにならず、渡したPATHがそのまま使われる。シェルのスナップショット機能の有無は結果を変えなかったため、既定のままとする。
- Codexは、PATHの先頭に自身の補助ディレクトリ（`codex-path`、`CODEX_HOME/tmp/arg0/...`）を加える。これはCodex本体の挙動で、`python3`などの解決先は変えない。

### Claude Code

- `Bash`ツールは`SHELL=/bin/bash`のとおりbash（非ログイン、非対話）で実行され、起動処理が渡したPATHと`VIRTUAL_ENV`がそのまま届いた。個人の設定は読まれなかった。PATHの先頭に`.venv/bin`を加えれば、`python3`、`python`、`pytest`は作業ツリーの`.venv`に解決された。

計画の停止条件（個人のシェル設定を読ませない方法が見つからない）には当たらないため、実装へ進んだ。

## 2. 起動処理の変更

- 共通の部品として`scripts/agent_shell_environment.py`を追加した。計測の条件に`agent_environment.shell_environment`（`revision: fixed-path-workspace-venv-r1`）を宣言した場合だけ、エージェントのプロセスへ渡す環境を、利用者の識別、エージェント自身の設定、評価の受け渡しに要る値と、次の値だけで作る。
  - PATH：作業ツリーの`.venv/bin`（絶対パス）の後に、条件で固定した`/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin`。
  - `VIRTUAL_ENV`：作業ツリーの`.venv`。
  - `ZDOTDIR`：runごとに作る空のディレクトリ（run終了後に削除）。
- `scripts/run_codex_evaluation.py`は、宣言がある場合、`os.environ.copy()`をやめ、上の環境に`CODEX_HOME`と成功時の受け渡しの値だけを加える。`SHELL`にはOSのユーザー情報のログインシェルを入れる。コマンドに`-c allow_login_shell=false`を加える。
- `scripts/run_claude_evaluation.py`は、宣言がある場合、`process_environment`からPATHを受け取らず（指定があれば起動しない）、上の環境を組み立てる。シェルは`process_environment`の`SHELL`（`/bin/bash`）のまま。
- 両方とも、エージェントを起動する前に、同じ環境と同じシェルの起動方法（`-c`）で確認用のコマンドを実行し、`shell-environment/receipt.json`へ記録する。記録には、渡したPATH・`VIRTUAL_ENV`・`ZDOTDIR`・シェル、シェルの中で見えたPATH、定義済みのシェル関数の数、ログインかどうか、`python3`・`python`・`pytest`の解決先、`python3`がpytestを読み込めるかを残す。条件と合わない場合は起動しない。
- 宣言のない既存の条件は、従来どおり動く。保存済みの結果、プロファイル、計測ディレクトリは変更していない。
- Codexの起動用の`isolated_adapter.py`は、新しい計測ディレクトリに新しく作った（SHA-256 `33fc2aa3ef12a29acdc3b9377457dc103ed996227aeb8bcb69221a800174a4af`）。計測プロセスの環境を複製せず、`HOME`、`USER`、`LOGNAME`、`TMPDIR`、`LANG`、`CODEX_RUNTIME_MANAGER`、`EVAL_*`、固定のPATH、`CODEX_HOME`だけをアダプタへ渡す。アダプタのコードは、計測ディレクトリへ固定したコードの複製から実行する。

## 3. テスト

- `tests/test_agent_shell_environment.py`を追加し、`tests/test_run_codex_evaluation.py`と`tests/test_claude_evaluation.py`へ確認を加えた。渡す環境が固定値と作業ツリーの`.venv`だけからなること、計測プロセスのPATHなどの個人の値が混ざらないこと、受け渡しの値でPATHやシェルを上書きできないこと、実際のzshとbashで`.venv`に解決され個人の設定が読まれないこと、`ZDOTDIR`に設定ファイルがあれば検出されることを確かめる。
- 全test discoveryでは、変更前のmainと同じ6件（`test_bundle_storage_format`、`test_evaluation_target_descriptor_v2`、`test_evaluation_target_registry`）だけが失敗し、追加分の失敗はない。`tests/test_kpi_revision_guard.py`は通った。

## 4. 計測の条件と系列

- 新しい評価系列のプロファイルを、C280の既存プロファイルから作った。既存のプロファイルは変更していない。
  - [`c280-sol61-low-standard14-n5-cli0159-isolated-shellenv-20261009-r1`](../evaluations/profiles/c280-sol61-low-standard14-n5-cli0159-isolated-shellenv-20261009-r1.json)
  - [`c280-claude-sonnet55-low-standard14-n5-cli2288-shellenv-r1`](../evaluations/profiles/c280-claude-sonnet55-low-standard14-n5-cli2288-shellenv-r1.json)
- 元のプロファイルとの違いは次のとおり。
  - 両方：`agent_environment.shell_environment`を加えた（実行環境の版、固定のPATH、`.venv`の場所、有効化の方法、個人の設定ファイルを読ませない方法）。結果の値を変えうる条件として照合される。
  - Sol Low：起動用スクリプトのSHA-256（`personal_instruction_isolation.launcher_sha256`）を新しいものにした。
  - Sonnet low：`process_environment`からPATHを除いた。
  - 両方：記録だけの項目である評価コードのSHA-256に、`scripts/agent_shell_environment.py`を加え、変更後の値にした。
- 保存済みのC280〜C300の結果とは比較しない（`PROMPT_ONLY_COMPARISON`）。

## 5. 確かめの実行（登録しない診断）

A02だけを、上の条件で両エージェント各N=2実行した（計測ディレクトリ`runs/shellenv-r1-a02-diagnostic-20261009-r1`）。結果は登録していない。

| 確認 | Sol Low | Sonnet low |
| --- | --- | --- |
| 起動前の確認（`receipt.json`の`ok`） | 2/2 | 2/2 |
| 個人の設定の読み込み | なし（2/2） | なし（2/2） |
| モデルが見た`python3`の解決先 | 作業ツリーの`.venv` | 作業ツリーの`.venv` |
| テストの実行 | `.venv/bin/python -m pytest`で成功（2/2） | `python -m pytest`で成功（2/2） |
| 品質の採点（従来の採点ツール） | 4点が2件 | 4点が2件 |

- Sonnet lowは、従来の環境では中断していた`python -m pytest`が、そのまま`.venv`で動き、テストを成功させてから報告した。
- Sol Lowのコマンドは`/bin/zsh -c`（非ログイン）で実行された。
- 計画の停止条件（`.venv`が有効にならない、個人の設定が読まれていた）には当たらない。

## 次に行うこと

計画の6として、新しい系列の基準となるC280を、Sol LowとSonnet lowで各Standard14 N=5測る。その後にどのCandidateを測るかは、基準の結果を見てから利用者が決める。

## 参照

[計画](agent-runtime-venv-isolation-plan-r1.md)、[処理の適切さの分類](c280-c300-processing-appropriateness-audit-r1.md)、[`evaluations/AGENTS.md`](../evaluations/AGENTS.md)。
