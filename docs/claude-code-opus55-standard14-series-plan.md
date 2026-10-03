# Claude Code Opus 5.5 Standard14系列の試験方針

> [!IMPORTANT]
> **状態**: 実行前に固定した方針。正式評価の発行前に作成し、結果確認後に本文を書き換えない。後続の観測と判定は別文書へ追記する。

## 1. 必要な成果

既存のTHE-CAPTION Standard14系列と同じ目的を、Claude Code条件で測る。すなわち、固定された14ケースを各5回実行し、Control-Free、Candidate147、Candidate276の3つのプロンプトについて、品質（`quality_score`）、全エージェント合算トークン（`total_tokens`）、経過時間（`elapsed_seconds`）を比較可能な形で得る。

Codex条件の保存済み結果は、ケース選定、比較の組み合わせ、計測規則を決めるための参照に限る。Claude条件の結果とは互換比較せず、Codexとの差をプロンプト効果として算出しない。

## 2. 対象の決め方

- 登録台帳（[`evaluations/targets/README.md`](../evaluations/targets/README.md)）で実行可能な現行インスタンスは`the-caption`である。
- 直近の継続方針は、2026-09-30の[GPT-6.1 Sol比較](../evaluations/results/sol61-c147-c276-free-low-medium-standard14-n5-cli0159_2026-09-30.md)と[C276 Astra low計測](../evaluations/results/c276-astra6-low-standard14-n5-cli0159-isolated_2026-09-30.md)で、Standard14上のControl-Free・C147・C276を新しい実行条件ごとに測り直す系列である。
- バックログの[項目8](research-backlog.md)は、Claude Code系列へ着手する明示判断と認証方式の選択を再開条件としていた。2026-10-01に利用者がClaude Code条件での試験を明示的に依頼し、認証方式として評価専用設定ディレクトリでの契約アカウントログインを選んだため、この条件を満たした。

したがって対象は`the-caption`のStandard14（`the-caption-standard14-r1`）とし、基準をControl-Free、候補をC147とC276とする。比較の組み合わせはSol 6.1系列と同じく、C147−Free、C276−Free、C276−C147の3つとする。

| 役割 | prompt identity | bundle SHA-256 |
| --- | --- | --- |
| 基準 | `the-caption-3ce91a4-control-free-repository-r1` / `r1` | `999769800af5a5b4f986a0589d8527d6b4f74ace7a56eb6b19b16e3ebaf43f0d` |
| 候補 | `the-caption-3ce91a4-result-effect-scope-r1` / `r1`（C147） | `51b0395d2a82b90e12b4d457d441c43a899577128cfa887c454618c9d2e0a5cc` |
| 候補 | `the-caption-3ce91a4-execution-control-r1` / `r1`（C276） | `4d2dcd4f34749b32155139138654cbc2bb33b78fc6841ba6eb14d29c8f7a678f` |

3つのバンドルは各階層に`CLAUDE.md -> AGENTS.md`のsymlinkを持つため、Claude Codeは本文を変えずに同じ制御文を読む。移植のためのプロンプト変更は行わない。C147にはCodex固有のfield名が残るが、そのまま測る。本文を変える必要が生じた場合は別identityのCandidateとして扱い、この系列の比較変数へ混ぜない。

## 3. 固定する条件

Claude系列内では、次をプロンプト3条件で共通に固定し、prompt identityだけを比較変数にする。

| 項目 | 固定値 |
| --- | --- |
| Evaluation set | `the-caption-standard14-r1` / `r1`、identity `2096d15e9d5d072e09e92313caa296caf8853c5e86f205d4d9f819b576263c33` |
| Layer 1 | Sol 6.1系列と同じ保存済みLayer 1（`control-free-sol6-low-medium-high-campaign-20260924-r1/low`）。基準result `d141469e2cdd48bda75f1772a285ee0a`のfixture identityと照合してから複製する |
| ケース・TaskSpec・fixture | Layer 1の固定値をそのまま使う |
| 採点 | Rating v14（`outcome-terminal-state-evidence-owner-diagnostic-v14`）のケース規則。command証跡だけをClaude用collectorで作る |
| モデル | `claude-opus-5-5`（利用者指定） |
| 推論設定 | `medium`（2026-07-27以降の通常比較の運用基準） |
| CLI | `/Users/kenn/.local/share/claude/versions/2.1.220`。version出力とSHA-256を実行前と各run開始時に照合する。自動更新を止める |
| 認証 | 評価専用`CLAUDE_CONFIG_DIR`での契約アカウントOAuth。認証情報は表示・記録・変更しない |
| 権限 | `--permission-mode bypassPermissions` |
| 設定の読み込み元 | `--setting-sources project,local`、`--strict-mcp-config`（MCPなし）、`--disable-slash-commands`（skillなし）、自動メモリ無効 |
| 実行環境変数 | 親プロセスの環境を引き継がず、固定した最小の変数だけを渡す |
| 並列上限 | `max_workers=24`、`max_attempts=3`、`global_queue` |
| 反復 | 14ケース×5回=70件を各条件で実施し、計210件 |
| 外部失敗 | 除外して同じ枠を再実行する |

使用できるtoolの集合、subagentの種類、実際に解決されたモデル名は、正式発行前のprobeで観測した値を固定し、各runの開始時記録と照合する。一致しないrunは外部計測失敗として除外する。

## 4. Codex固有機能の扱い

Codex固有のtool、返却項目、継続能力を、名前の置換だけでClaudeへ対応づけない。必要な機能ごとに、Claude側で観測できる証拠を実測してから使う。対応できない項目は対応不能として記録する。

| 必要な機能 | Codex側の証拠 | Claude側で確認する証拠 |
| --- | --- | --- |
| commandの個別実行と終了状態 | `exec_command`の構造化exit code | Bash toolの`tool_result`の`is_error`と`Exit code N`の本文。成功時の終了状態はprobeで確認する |
| 実行中commandの継続 | `wait`とcell ID | 背景実行したBashの完了記録。完了を証拠で結べない場合は`evidence_incomplete`とする |
| 子エージェントの起動と結果 | `spawn_agent`とrollout | `Task` toolと`subagents/agent-*.jsonl`、`.meta.json` |
| 全エージェントのusage | rolloutの最終usage | root・subagentのtranscriptをrequest単位で重複除去した合計と、terminal resultの`modelUsage`の照合 |
| 制御文の読み込み | 開始時のrepository instructions | root `CLAUDE.md`は開始時、配下は該当directoryへ触れた時点。読み込み時点の差は条件そのものとして記録する |
| 担当と生成者の証跡 | `task_name`、`FINAL_ANSWER.Sender` | Claude側に対応する返却項目はないため、診断を`unavailable`として記録する。Rating v14では得点に影響しない |

評価adapterが実行役へ渡すcommand証跡の説明文は、Codex版がtool名`exec_command`とwrapper出力形式を前提にしているため、Claude版では「required validation commandを1件ずつ個別のBash呼び出しで実行し、複合commandにまとめない」という同じ要求だけを残す。この説明文は3条件で共通の実行条件であり、prompt identityには含めない。

## 5. 計測規則

### トークン

- `total_tokens`は、rootと全subagentのtranscriptにあるassistant応答のusageを、応答ID単位で重複除去して合計した値とする。各応答の`input_tokens`、`cache_creation_input_tokens`、`cache_read_input_tokens`、`output_tokens`をすべて含める。
- cacheの読み込みと作成はKPIへ含め、内訳は診断として別に保存する。
- transcriptに現れない補助モデルの呼び出し（terminal resultの`modelUsage`にだけ現れるもの）はKPIへ含めず、補助モデル分として診断へ保存する。
- 完全性の確認として、transcriptに現れたモデルごとの合計がterminal resultの`modelUsage`と一致することを要求する。一致しない、transcriptが欠ける、terminal resultがない場合は、値を推定せず`claude_all_agent_usage_incomplete`で除外する。
- rootだけのusage（terminal resultの`usage`）を全エージェント合計として扱わない。
- token accountingは`{"scope": "all_agents", "revision": "claude-v1", "source": "claude_code_transcript_request_usage_dedup_by_message"}`とする。Codexのaccountingとは別revisionであり、互換比較しない。

### 経過時間

既存の評価ループが計測するadapter全体の経過時間を使う。時間内訳はClaude CLI呼び出し区間だけを診断として保存する。

### 品質

Standard14のケース規則（成果物の内容、変更許可範囲、応答内容、必須commandの成功証拠、A01の終端状態）を変えずに再利用する。必須commandの判定に使うcommand証跡だけを、Claude transcriptから組み立てる。採点器には成果物、最終応答、command証跡だけを渡し、prompt identityや比較情報を渡さない。oracleや期待結果を実行役へ渡さない。

## 6. 正式発行前のゲート

1. **probe（正式ケースを使わない）**: 一時repositoryで次を確認し、結果を記録する。
   - stdout、stderr、終了状態、最終応答を個別に保存できること
   - rootと全subagentの証跡を一つのrunへ対応づけられること
   - tool実行、失敗、背景実行の継続、完了を証跡から判定できること
   - 全エージェントのusageを重複なく集計し、`modelUsage`と照合できること
   - 個人設定、`CLAUDE.md`、メモリ、skill、plugin、MCP、hookの混入範囲
2. **実装の単体試験**: 新しいadapter、collector、採点wrapper、評価基盤の受け入れ拡張について、既存Codex経路の回帰を含む全test discoveryを通す。
3. **preflight receipt**: 3条件のprofile、capsule、global planを生成し、prompt identity以外の互換条件、Layer 1、fixture、CLIの実体とhash、認証設定ディレクトリの状態を機械照合する。一項目でも不一致・未固定・未確認があれば正式評価を発行しない。

## 7. 判定条件

- 3 KPIは各条件のN=5中央値と、上記3組の差分として記録する。評価基盤は勝者、改善・悪化、採用可否を出力しない。
- 費用の扱いは[`evaluation-loop-manual.md`](evaluation-loop-manual.md)の規則を保持する。品質を維持したうえでトークンと経過時間がともに減った場合だけ費用改善方向とし、一方が増えた場合はまず費用の後退として記録する。
- この系列にはC276固有の機序ゲートが固定されていないため、機序は診断値（command protocol違反、A01の終端状態、subagent起動、制御文の読み込み）として報告し、成功率で機序成立を主張しない。
- 後続試験（N追加、別モデル、移植Candidate）へ進む条件はこの方針では定めず、結果を見て別の判断として扱う。

## 8. 非目標

- Codex結果との比較、Codex結果の再採点や変更
- プロンプト本文の変更、Candidateの作成
- CLI、認証、外部runtimeの変更
- 採用、release、ターゲット本体の変更、push、PR、merge
