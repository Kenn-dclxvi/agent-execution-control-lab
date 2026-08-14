# Portable instruction runtime別測定成立監査

> [!IMPORTANT]
> **状態**: `local_runtime_inventory_observed / claude_schema_fields_observed / claude_probe_not_admitted / codex_existing_path_only / cursor_cli_unavailable / gemini_cli_unavailable / ui_surfaces_diagnostic_only / formal_target_not_created`
>
> 本書は2026-08-14時点のローカル実行面と、portable instructionの正式評価に必要な計測境界を監査する。portable kernel本文、Candidate、target instance、profile、評価slotまたはsurface設定変更ではない。

## 結論

現在のローカル環境では、Codex CLIとClaude Code CLIだけが実行可能なCLIとして観測できた。Codexは既存評価基盤の実行経路を持つ。Claude Codeは構造化出力と実行隔離に使えるoptionを公開しているため、独立したformal runtimeの候補にはなる。ただし、現在のCLI versionでprompt注入、認証とuser stateの隔離、all-agent token完全性、elapsed境界およびsubagent provenanceを再観測するまで正式targetへ登録しない。

CursorとGeminiのCLIはローカルで観測できなかった。ChatGPT Project、Cursor UIおよびGemini Gemは、同一kernelのloadとsemantic Caseへの応答を調べるsurface diagnosticの対象にはできるが、all-agent `total_tokens`の一次値がない限りformal resultへ昇格させない。

この差はportable kernelの意味をsurface別に変える理由にはしない。測定できないfieldは`unavailable`として保持し、推定値、別surfaceの計測またはmodel自己申告で補わない。

## ローカル実行面の観測

観測日は2026-08-14。version表示とhelpの読み取りだけを行い、外部model invocation、評価Case、repository変更を伴うprobeは実行していない。

| surface/runtime | 観測 | 現時点の扱い |
| --- | --- | --- |
| Codex CLI | `/Users/kenn/.local/bin/codex`、`codex-cli 0.146.0` | 既存Codex系列の実行面。portable targetとしては別descriptorとbaselineが必要 |
| Claude Code CLI | `/Users/kenn/.local/bin/claude`、`2.1.220 (Claude Code)` | formal runtime候補。現versionでの非評価probeが必要 |
| Cursor CLI | `cursor-agent`を`PATH`上で観測できず | UI diagnosticのみ。CLIの不存在を製品能力の不存在へ一般化しない |
| Gemini CLI | `gemini`を`PATH`上で観測できず | Gem UI diagnosticのみ。CLIの不存在をGem能力の不存在へ一般化しない |
| ChatGPT Project | ローカルCLIに対応づけない | Project instructionsを使うUI diagnosticのみ |

実行ファイルの存在は、認証済みであること、指定modelを利用できること、追加instructionsを隔離できること、またはtoken accountingが完全であることを証明しない。

## Codex CLI

`codex exec --help`では少なくとも`--model`、`--sandbox`、`--ephemeral`、`--json`、`--output-last-message`、`--config`、`--enable`および`--disable`を観測した。既存評価基盤はCodex CLI用のtoken、command evidence、elapsedおよびatomic run経路を持つ。

ただしportable instruction系列は既存THE-CAPTION系列とtarget、Case、prompt identityおよびbaselineが異なる。既存Codex resultを流用せず、新しいnamespaced targetのdescriptor、rating contract、profileおよびpreflightを固定してから測定する。

## Claude Code CLI

### 現versionで観測した候補能力

`claude --help`から次を観測した。

- 一回応答: `--print`
- 構造化出力: `--output-format json|stream-json`、`--json-schema`
- modelとeffort: `--model`、`--effort`
- prompt配送: `--system-prompt`、`--append-system-prompt`
- session永続化抑止: `--no-session-persistence`
- customization制御候補: `--bare`、`--safe-mode`、`--setting-sources`、`--strict-mcp-config`、`--disable-slash-commands`
- tool surface制御候補: `--tools`
- subagent観測候補: `--forward-subagent-text`、`--include-hook-events`、`--include-partial-messages`

これらはoptionの存在を示すだけで、組合せの意味、既定値、subscription認証での利用可能性または記録完全性を確定しない。

### 既存設計から継承できるもの

[`claude-code-cli-evaluation-adapter-design.md`](claude-code-cli-evaluation-adapter-design.md)は、Claude Code 2.1.206で次を非評価probeとして観測している。

- rootとsubagentのtranscriptおよび`modelUsage`を使うall-agent token候補
- Bash tool resultからのcommand evidence候補
- `CLAUDE_CONFIG_DIR`を空directoryへ向ける隔離が認証状態も失うこと
- Codex系列とClaude Code系列のcompatibility不成立

これらは新設計の仮説とprobe項目には使えるが、2.1.220での成立を現在値として継承しない。特にtoken field、補助model call、subagent transcript、permission modeおよびuser customizationの到達範囲は再観測する。

### formal runtimeへ進むための未観測値

| gate | 必要な観測 | 欠落時の扱い |
| --- | --- | --- |
| prompt identity | control-free条件とkernel条件で、明示したprompt bytes以外のinstruction sourceを固定または列挙できる | diagnosticのみ |
| authentication | 認証方式を固定し、認証情報そのものを保存せず同じ方式を再現できる | probeを開始しない |
| model identity | 実際に応答したmodel identityを一次resultから取得できる | formal profileを作らない |
| output identity | response、request/session identityおよびschema validityをwrite-onceで保存できる | runをadmitしない |
| all-agent tokens | root、subagentおよび補助model callを含む範囲を固定し、重複なく一次値を合算できる | tokenを推定せずrunをadmitしない |
| elapsed | harness発行直前からterminal result受領までの単調時計境界を固定できる | formal profileを作らない |
| provenance | actorまたはsubagent identityと対応resultを一次traceでbindできる | provenance Caseは`unavailable` |
| nonterminal identity | streamingまたはtool invocationの継続identityを一次traceでbindできる | continuation Caseは`unavailable` |

## UI surfaceの診断境界

ChatGPT Project、Cursor UIおよびGemini Gemでは、次をsurface diagnostic receiptとして保存できる。

- surface名と観測日
- 貼付または配置したkernel bytesのSHA-256
- model-visible Case入力
- model応答
- UIが表示するmodel identity。表示しない場合は`unavailable`
- 操作者が観測した開始時刻と終了時刻。ただしformal KPIには使わない
- instruction sourceまたは重複deliveryの観測可否

次はUI応答から推定しない。

- kernelが一回だけ注入されたこと
- hidden instructionsの不在
- all-agent `total_tokens`
- actor/result provenance
- 複数操作のatomic issuance
- nonterminal invocation identity

ChatGPT ProjectをOpenAI APIへ、Gemini GemをGemini APIへ、Cursor UIを別CLIへ置き換えたresultは、同じsurfaceのformal resultではない。

## 次に許可する非評価probe

次に実行してよいのは、Claude Code 2.1.220を対象とする一件のmeasurement-schema probeである。portable kernel、Q01-Q08またはrepository taskは使わず、固定JSONを固定schemaで返すだけの無害な入力にする。

exact input、command、admissionおよび停止条件は[`Claude Code 2.1.220 measurement-schema probe実行票`](claude-code-2.1.220-measurement-schema-probe-plan.md)へ固定した。

同実行票は一回発行され、schema適合応答、resolved model、root usageおよびterminal identityを観測した。ただしstdoutとstderrを個別保存できず、実行票のadmission条件を満たさなかった。再試行はせず、結果と次のtransport境界を[`Claude Code 2.1.220 measurement-schema probe観測結果`](claude-code-2.1.220-measurement-schema-probe-result.md)へ固定した。

probe前に次を一つのreceiptへ固定する。

1. CLI versionとexact command。
2. 認証方式および読み込ませるsetting source。secret値は記録しない。
3. system prompt bytes、user input bytesおよび期待JSON schema。
4. toolを無効にする指定とsession persistenceを無効にする指定。
5. stdout、stderr、process exit、terminal JSONおよび生成されたtraceの保存先。
6. root、subagent、補助modelを含むtoken範囲とdedup key。
7. elapsedの開始・終了境界。
8. success、unavailable、external failureおよび停止条件。

probeが一項目でも未固定ならmodel invocationを発行しない。probeの成功はadapter実装、portable kernelのsemantic conformanceまたはformal target admissionを意味しない。

## 停止条件

- local CLIの存在だけでformal measurement成立とする。
- 2.1.206の観測値を2.1.220の現在値として扱う。
- user configを隔離した結果、認証不能になった状態を別の認証方式で暗黙に回避する。
- UIの文字数、経過表示、response metadataまたは自己申告からtokenを推定する。
- diagnostic receiptをformal result、runtime間比較、採用、releaseまたはprojectionへ使う。
- measurement probeへportable kernelやtuning Caseを混ぜ、probe結果を評価証拠として再利用する。

## 参照

- [`Portable instruction semantic conformance評価設計`](portable-instruction-semantic-conformance-evaluation-design.md)
- [`C147由来のruntime非依存portable instruction設計`](runtime-independent-execution-control-draft.md)
- [`Claude Code CLI評価adapter設計`](claude-code-cli-evaluation-adapter-design.md)
- [`Claude Code 2.1.220 measurement-schema probe実行票`](claude-code-2.1.220-measurement-schema-probe-plan.md)
- [`Claude Code 2.1.220 measurement-schema probe観測結果`](claude-code-2.1.220-measurement-schema-probe-result.md)
- [`evaluation foundation v4境界`](prompt-comparison-workflow.md)
- [`target instance規則`](../evaluations/targets/AGENTS.md)
