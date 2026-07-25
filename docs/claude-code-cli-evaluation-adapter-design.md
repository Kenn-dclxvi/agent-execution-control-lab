# Claude Code CLI評価adapter設計

## 位置付け

この文書は、Layer 2 executorをCodex CLI（`codex exec`）からClaude Code CLI（`claude -p`）へ置き換える試験方法の**設計検討**である。2026-07-25時点で実装、評価、採用のいずれも行っていない。

- evaluation foundation v3の4 Layer、3 KPI、result schemaは変更しない。境界の正本は[`prompt-comparison-workflow.md`](prompt-comparison-workflow.md)と[`evaluations/AGENTS.md`](../evaluations/AGENTS.md)、実行方法の正本は[`evaluation-loop-manual.md`](evaluation-loop-manual.md)とする。
- 既存の`scripts/run_codex_evaluation.py`、既存collector、既存registryのresultは変更対象にしない。
- 「## 未確定事項」の項目は確定仕様ではない。実装前に決定または実測が必要である。

## 結論

Claude Code CLIでの試験は成立する見込みだが、**既存Codex resultとの互換比較は成立しない**。次の3点が理由である。

1. prompt制御本文の注入時点がCodexと異なる（後述の実測）。
2. all-agent tokenの取得源と数値の意味が異なるため、新しいtoken accounting revisionになる。
3. `agent_environment`と`executor_parameters`が変わり、compatibility keyが一致しない。

したがってClaude Code条件は、既存Codex系列とは独立した系列として、baselineから再測定する。

## 実測した前提

実測日は2026-07-25。実測環境は`claude --version` = `2.1.206 (Claude Code)`、`codex --version` = `codex-cli 0.144.0`。probeは評価caseを使わず、一時repository上で`--permission-bypass`条件（`--permission-mode bypassPermissions`）と`--output-format json`で実行した。以下の値はそのprobeで観測した一次値であり、評価resultではない。

### prompt overlayはそのまま適用できる

[`the-caption-3ce91a4-validation-closure-release-r1`](../prompts/releases/the-caption-3ce91a4-validation-closure-release-r1/README.md)の`manifest.json`は19 targetを持ち、そのうち5件が`CLAUDE.md -> AGENTS.md`のsymlink（root、`docs/`、`scripts/`、`src/`、`tests/`）である。overlay後のworkspaceで、Claude Code CLIはCodexと同じ本文を読む。bundle形式とoverlay手順（正本は[`prompt-file-bundle.md`](prompt-file-bundle.md)）を変更する必要はない。

### 注入時点がCodexと異なる

Codex条件では、開始時のrepository instructionsへ対象bundleのpath-scoped `AGENTS.md`が注入されていることを開始gateで確認している（[`desktop-evaluation-slot.md`](desktop-evaluation-slot.md)）。Claude Code CLIでは、root `CLAUDE.md`は開始時に読まれるが、配下directoryの`CLAUDE.md`は当該directoryのfileへ触れた時点で追加注入される。2026-07-25の作業sessionで、`docs/`、`evaluations/`、`scripts/`の`CLAUDE.md`が該当directoryのfile参照後に注入されることを観測した。

制御本文が実行のどの時点でmodel-visibleになるかは評価条件そのものである。よってCodex条件の結果と同一比較へ混ぜない。

### all-agent tokenは取得できる

1 subagent（`Agent` tool、`subagent_type: general-purpose`、`spawnDepth: 1`）を起動させたprobeの観測値。

| 対象 | 値 | 取得源 |
| --- | --- | --- |
| root | 72,407 | `~/.claude/projects/<slug>/<session-id>.jsonl` |
| subagent | 37,032 | `~/.claude/projects/<slug>/<session-id>/subagents/agent-<agent-id>.jsonl` |
| 合算 | 109,439 | 上記2件の合計 |
| `result.modelUsage["claude-sonnet-5"]`合計 | 109,439 | `--output-format json`のresult |
| `result.usage`合計 | 72,407 | 同result（**rootのみでall-agentではない**） |
| `claude-haiku-4-5-20251001` | 611 | `result.modelUsage`のみ。transcriptには現れない |

補足として次を確認した。

- transcriptの`assistant`行の`usage`はrequest単位であり、同一`requestId`が複数行に現れる。`requestId`でdedupしないと二重計上になる。
- subagent transcriptには`agent-<agent-id>.meta.json`が併置され、`agentType`、`toolUseId`、`spawnDepth`を持つ。
- rootのTask結果（`toolUseResult`）にも`agentId`、`resolvedModel`、`totalTokens`、`usage`が入る。突合材料として使える。

### command証跡はharness側でbindできる

Bash tool結果の記録形状を観測した。

| 結果 | 記録 |
| --- | --- |
| 成功 | `toolUseResult`が`{"stdout":…,"stderr":…,"interrupted":false,"isImage":false,"noOutputExpected":false}`、tool_result blockの`is_error`が`false` |
| 非zero exit | tool_result blockの`is_error`が`true`、内容が`"Exit code 3\nbad"`（`exit 3`かつstderr `bad`のcommandに対して） |

成功時の記録にexit codeは含まれないが、`is_error`が`false`であることをexit 0の証跡として使える。非zero時はexit codeを文字列から取得できる。いずれもmodelの自己申告ではなくharness記録であり、「Agentの自己申告だけを除外根拠にしない」という既存要件（[`evaluation-loop-manual.md`](evaluation-loop-manual.md)）を満たせる。

### user config隔離は認証に当たる

`CLAUDE_CONFIG_DIR`を空directoryへ向けたprobeは`Not logged in · Please run /login`で終了し、exit codeは1だった。Codexの`--ignore-user-config`相当の隔離を成立させるには、API key認証（`ANTHROPIC_API_KEY`または`apiKeyHelper`）が前提になる。

## adapter対応表

新設する`scripts/run_claude_evaluation.py`が満たす対応関係。executor contract（環境変数、`token-usage/v2`、`run-status/v1`）は既存のまま使う。

| Codex adapterの条件 | Claude Code CLI側 |
| --- | --- |
| `codex exec --json -` | `claude -p --output-format stream-json --verbose`（または`--output-format json`） |
| `--output-last-message <file>` | resultの`result`文字列 |
| `-m <model>` | `--model` |
| `model_reasoning_effort="high"` | `--effort` |
| `-s workspace-write` + `approval_policy="never"` | `--permission-mode bypassPermissions`（`--allow-dangerously-skip-permissions`の付与要否は実装時に確定する） |
| `--ignore-user-config --ignore-rules --strict-config` | `CLAUDE_CONFIG_DIR`隔離（API key前提）、または`--setting-sources project` + `--strict-mcp-config` + `--disable-slash-commands` |
| `--disable memories` | settingsの`autoMemoryEnabled: false`、または`CLAUDE_CODE_DISABLE_AUTO_MEMORY` |
| `--enable multi_agent`、`agents.max_threads=4` | subagentは常時利用可能。並列上限に対応する候補は`CLAUDE_CODE_MAX_TOOL_USE_CONCURRENCY`（既定値は未確定） |
| `--disable apps` / `plugins` / `plugin_sharing`とcatalog SHA-256固定 | plugin未指定、`--strict-mcp-config`、hook無効化。catalog identityの固定方法は未確定 |
| `codex --version` | `claude --version` |

`executor_parameters`の外側条件（`max_workers: 24`、`max_attempts: 3`、`schedule_policy: global_queue`、`monitor_interval_seconds: 5`）はexecutorに依存しないため、Claude Code条件でも同じ意味で使える。

## 新設するschema revision

既存revisionをin-placeで変更せず、新しいrevisionを追加する（[`scripts/AGENTS.md`](../scripts/AGENTS.md)）。

### token accounting

```json
{
  "scope": "all_agents",
  "revision": "v1",
  "source": "claude_code_transcript_request_usage_by_session"
}
```

算出は、root transcriptと`subagents/*.jsonl`の`assistant`行usageを`requestId` dedupで合算する。完全性gateとして`result.modelUsage`と突合し、transcript合算がmodelUsage合計を超える場合、または差分が宣言済みの補助model以外を含む場合はfail closedする。合算できないrunはtokenを推定せず外部失敗として除外する（既存の`codex_all_agent_usage_incomplete`と同じ扱いの別reason code）。

Codexの`total_token_usage.total_tokens`はsession累計であり、Claude側はrequest別usageの合算でcache read / creationを含む。値の意味が異なるため、既存Codex resultと同一比較へ混ぜない。

### command evidence collector

既存の`all-agent-command-evidence/v5`はCodexの`item.completed` / `command_execution`とrolloutの構造に依存するため流用しない。新collectorは、root transcriptと全subagent transcriptのBash `tool_use`と対応する`tool_result`から次を組む。

| 分類 | 判定 |
| --- | --- |
| attempted | Bash `tool_use` blockが存在する |
| successful | 対応する`tool_result`の`is_error`が`false`（exit 0として扱う） |
| failed | `is_error`が`true`かつ内容からexit codeを取得できる |
| evidence_incomplete | `is_error`が`true`だがexit codeを取得できない（interrupt、permission拒否など） |

`evidence_incomplete`はrunを除外して同じslotを再試行する既存方針に合わせる。

### external failure検出

Codexのstderr signatureと`Selected model is at capacity.`検出の代わりに、resultの`is_error`、`subtype`、`api_error_status`、`permission_denials`の非空、transcript欠落、usage完全性不足を検出源とする。reason codeは新設する。

## 互換性の帰結

`agent_environment`、`executor_parameters`、token accounting revisionが変わるため、既存Codex resultとcompatibility keyは一致しない。

- Claude Code条件では、baseline（現行本体prompt相当）から再測定し、独立したprofile revision（例: `*-claude-r1`）として登録する。
- 同一candidate bundleをCodexとClaude Codeで測った結果は、別条件の独立resultである。`compare`は互換条件一致を要求するため、CLI間差分viewを評価基盤は出力しない。CLI間比較を行う場合は、評価基盤外の観察として扱うか、新しい比較次元を明示要件として別設計する。

## 未確定事項

確定仕様として扱わない。実装前に決定または実測する。

1. **認証方式**。API key + `CLAUDE_CONFIG_DIR`隔離（決定性が高い）か、subscriptionのまま既定config dirを使い、user levelの`CLAUDE.md`とsettingsを開始gateで確認する方式か。環境identityの固定方法がこの決定に依存する。
2. `CLAUDE_CODE_MAX_TOOL_USE_CONCURRENCY`の既定値と、subagent並列度への実効性。
3. 補助model call（probeで観測した`claude-haiku-4-5-20251001` 611 tokens）をKPIへ含めるか。transcript基準へ統一し補助callはdiagnosticへ回す案を検討中だが未決である。
4. model-visible capability catalog（skills、plugins、MCP）の固定方法とidentity source。既存実装はCodex rolloutのdeveloper messageに依存する。
5. subagent transcriptの出力が設定で変わるか（binary内に`subagentTranscripts`という設定keyらしい文字列が存在するが、意味と既定値は未確認）。並列起動と`spawnDepth > 1`での網羅性も未実測である。
6. `--permission-mode bypassPermissions`単独で`workspace-write` + `approval_policy="never"`と同等の実行範囲になるか。

## 段階計画

| Phase | 内容 |
| --- | --- |
| 0 | 認証方式の決定（未確定事項1） |
| 1 | probe（評価case不使用）: 並列・入れ子subagentのtranscript網羅性、並列度env varの効果、`CLAUDE.md`注入到達点、result schemaの安定性、未確定事項2〜6の実測 |
| 2 | `scripts/run_claude_evaluation.py`と新collectorの実装、および対応するunit testの追加 |
| 3 | pilot: 標準14項目のうち1 case、1 iterationで`freeze-set` → `run` → `rate` → `record-result`をend-to-end確認 |
| 4 | 本測定: baselineとcandidateを標準14項目×5回で新profile revisionへ登録 |

## 非目標

- 既存Codex adapter、既存collector、既存registry resultの変更。
- 既存resultの再採点、再解釈、in-place変更。
- CodexとClaude Codeの結果を同一比較へ載せること。
- prompt本文の変更（executor変更とprompt変更を同一比較単位へ混ぜない）。
- 採用、release、THE-CAPTION本体反映の判断。
