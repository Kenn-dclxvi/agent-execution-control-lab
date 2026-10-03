# Claude Code 2.1.284 評価経路probeの観測結果

> [!IMPORTANT]
> **状態**: 正式ケースを使わない非評価probeの記録。2026-10-01に実施した。評価resultではなく、[Claude Code Opus 5.5 Standard14系列の試験方針](claude-code-opus55-standard14-series-plan.md)の正式発行前ゲートとして、計測経路の成立と実行条件の固定根拠を残す。

## 1. 実行ファイルの選定

方針で予定していたスタンドアロンCLI `2.1.220`は、評価専用設定でのログイン後に`claude-opus-5-5`を指定すると、APIから次の応答が返り実行できなかった。

```text
API Error: 400 Claude Code 2.1.220 does not support this model; version 2.1.280 or newer is required.
```

CLIの更新はこの作業の範囲外のため、`claude update`は行っていない。代わりに、このMacに既に存在するデスクトップアプリ同梱のClaude Code `2.1.284`を、ファイルを変更せずに評価用の実行ファイルとして固定した。

| 項目 | 値 |
| --- | --- |
| 絶対パス | `/Users/kenn/Library/Application Support/Claude/claude-code/2.1.284/claude.app/Contents/MacOS/claude` |
| version出力 | `2.1.284 (Claude Code)` |
| SHA-256 | `4241eb34a941f9e7ca960ed845714b40f381a0365fe36d06077a1296bc6f97b2` |
| 署名 | `codesign --verify --strict`成功、Identifier `com.anthropic.claude-code`、TeamIdentifier `Q6L2SF6YDW` |
| 認証 | 評価専用`CLAUDE_CONFIG_DIR`でのclaude.ai OAuth（契約種別`team`、`apiKeySource: none`）。認証情報の値は表示・記録していない |

この実行ファイルはデスクトップアプリの更新で置き換わる可能性がある。各runの開始時にSHA-256とversion出力を照合し、一致しない場合はadapterが起動前に停止する。

## 2. 設定の読み込み元と混入範囲

| 対象 | 観測 | 扱い |
| --- | --- | --- |
| HOMEを空の一時directoryへ替える方法 | `Not logged in`で起動できない | 採用しない。認証情報の複製もしない |
| 個人の`~/.claude`（`CLAUDE.md`、`settings.json`、plugin） | 評価専用`CLAUDE_CONFIG_DIR`を使うため読まれない。評価専用directoryの中身は`.claude.json`と`backups`だけで、`CLAUDE.md`、settings、agents、commands、skills、plugins、hooksは存在しない | 各runの開始時に禁止項目の不存在を確認する |
| user / project / localの設定 | `--setting-sources project,local`。fixtureに`.claude/settings*.json`はない | 固定 |
| MCP | `--strict-mcp-config`で`mcp_servers: []` | 固定 |
| skill | `--disable-slash-commands`で`skills: []`、`slash_commands: []` | 固定 |
| 自動メモリ | `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`で`memory_paths: null` | 固定 |
| 組み込みplugin `agents-md@builtin` | サーバー側の機能フラグでrunごとに有無が変わる。`session.start`、`prompt.context`、`agent.spawn`、`tool.call`にhookを持つ。`--settings '{"enabledPlugins":{"agents-md@builtin":false}}'`で3回とも外れた | 無効に固定する。制御文は`CLAUDE.md -> AGENTS.md`経路だけで届く |
| 組み込みplugin `telemetry@builtin` | 常に有効 | 期待値として固定する |
| 親プロセスの環境変数 | デスクトップアプリの`ANTHROPIC_BASE_URL`や`CLAUDE_CODE_*`が混ざる | 引き継がず、固定した最小の変数だけを渡す |
| Bash toolのshell | 既定はzshで`~/.zshrc`を読む | `SHELL=/bin/bash`に固定する。`~/.bashrc`と`~/.bash_profile`は存在しない |
| アカウント由来の文脈 | `session_context`としてアカウントのメールアドレスとgit status、`credential_org`、commit用のattributionがharnessから注入される | 設定では外せない。3条件で共通の実行環境として記録する |

## 3. 使用するtool

既定のtool一覧には、外部へ作用するもの（Web検索・取得、Cron、通知、Remote Trigger、Workflow、worktree、Design同期など）が含まれる。評価では`--tools`で次の7つに固定し、各runの開始記録（init event）がこの一覧と一致することを確認する。

```text
Task, Bash, Edit, NotebookEdit, Read, TaskStop, Write
```

subagentの種類は`claude`、`Explore`、`general-purpose`、`Plan`、`statusline-setup`の5つである。transcript上のsubagent起動tool名は`Agent`として記録される。

## 4. 計測経路の確認

正式ケースを使わない一時repositoryで、成功command、失敗command、背景実行の成功と失敗、Read、subagent起動を含む課題を実行した。

| 確認項目 | 結果 |
| --- | --- |
| stdout、stderr、終了状態、最終応答の個別保存 | 成立。stdoutはstream-json、stderrは別file、process終了状態はadapterが保持し、最終応答は最後のresult eventの`result` |
| rootと全subagentの証跡の対応づけ | 成立。subagentは`<session>/subagents/agent-<id>.jsonl`と`.meta.json`（`agentType`、`toolUseId`、`spawnDepth`）に記録され、rootの`toolUseResult.agentId`と一致した |
| 前景commandの成功と失敗 | 成立。成功は`tool_result.is_error=false`、失敗は`is_error=true`と本文先頭の`Exit code N` |
| 背景実行の継続と完了 | 成立。harnessがstdoutへ`system / task_notification`（`tool_use_id`、`status`、`(exit code 0)`または`failed with exit code 4`）を出し、transcriptにも`queue-operation`または`queued_command`として記録した。モデルが自分の文章に「完了した」と書いた例があったため、モデルの文章は判定に使わない |
| 継続による複数result | 背景実行の完了がモデルの応答終了後に届くと、sessionが再開しresult eventが2回出た。`modelUsage`は最後のresultで累積値になっていた |
| 全エージェントusage | 成立。rootとsubagentのassistant応答を応答ID単位で重複除去した合計が、最後のresultの`modelUsage`と4項目すべて一致した（例: 136,478 = root 119,935 + subagent 16,543） |
| 制御文の読み込み時点 | root `CLAUDE.md`は開始時の`instructions`、配下の`CLAUDE.md`はそのdirectoryのfileを読んだ時点の`nested_memory`として記録された |

## 5. 評価ループを通した確認

練習用の1ケース（`data.txt`の値を変えて`sh check.sh`で確かめる課題）を、正式と同じadapterと評価ループで1回実行した。status `valid`、必須command `sh check.sh`は`successful`、全エージェントtokenは35,011、変更pathは`data.txt`だけ、tool一覧などの開始記録の不一致は0件、root `CLAUDE.md`の読み込みを記録できた。

## 6. Codex固有機能との対応

| Codex側 | Claude側の対応 | 判定 |
| --- | --- | --- |
| `exec_command`の構造化exit code | Bash `tool_result`の`is_error`と`Exit code N` | 実測で対応可能 |
| `wait`とcell IDによる継続 | 背景Bashと`task_notification` | 実測で対応可能。ただし同じ呼び出しを継続するのではなく、完了通知による会話の再開である |
| `spawn_agent`とrollout | `Agent` toolとsubagent transcript | 実測で対応可能 |
| custom exec wrapperの出力形式 | 該当機能なし | 対応不能。adapterの説明文から削除した |
| `task_name`、`FINAL_ANSWER.Sender`による担当と生成者の証跡 | 該当する返却項目なし | 対応不能。診断を`unavailable_on_claude_surface`として記録する |
| 補助モデルのusage | このprobeでは`modelUsage`に補助モデルは現れなかった | 現れた場合はKPIへ含めず診断へ保存する |

## 7. 保存場所

非公開の生の記録（stdout、stderr、debug log、transcript）は`/Volumes/SN7100/_verification/THE-CAPTION-prompt-ab-measurement/runs/claude-opus55-free-c147-c276-standard14-n5-cli2220-20261001-r1/probe/`と`smoke/`、評価専用設定directoryの`projects/`に置いた。repositoryへはcommitしない。
