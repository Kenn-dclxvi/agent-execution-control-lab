# C147 Claude Code自己評価のtriage

> [!IMPORTANT]
> **状態**: `user_supplied_self_assessment_recorded / static_hypotheses_triaged / behavioral_trace_missing / portability_design_input_only / candidate_not_created / evaluation_not_started`
>
> 本書は、利用者が2026-08-14に提示したClaude Code自身によるC147適用可能性の静的報告をtriageする。報告は実行trace、tool event、失敗resultまたはquality resultではない。portable kernelの仮説入力には使うが、機序成立、不成立、死文、品質またはcostの確定証拠にはしない。

## 結論

報告から直接採用できるのは、C147のCodex固有field、tool、return schemaおよび評価harness参照が、Claude Codeのmodel-visibleな対応物へ一意にbindできないというsurface mismatchである。

一方、C147の意味群全体が無効、有害または重複しているという判定はまだ採用しない。Claude Codeにもmain executionとsubagent executionがあり、actorとcoordinatorの意味境界は残る。`CLAUDE.md`と`AGENTS.md`の配送も実file関係とload receiptを確認しなければ二重投入と判定できない。EVIDENCE_GATEの遅延、形式記法の実効および「5項目だけが有効」という範囲は、固定caseの動的resultで判定する。

## 入力identity

- source: 利用者が会話へ貼付したClaude Codeの自己評価
- evaluated text: C147系`CLAUDE.md`と同内容の`AGENTS.md`
- target repository / commit / Claude Code version / model / permission / loaded instruction receipt: 未提示
- observed tool events / transcript / changed artifact / validation result / token / elapsed: 未提示
- evidence class: `model_self_assessment / static_hypothesis`

入力identityが不足しているため、本報告だけから別runtimeでのbehavioral portabilityをpassedまたはfailedにしない。

## 指摘ごとのtriage

| 報告の指摘 | 現在判定 | 根拠とportable設計への効果 |
| --- | --- | --- |
| `SPEC`は過剰な確認質問を止める | `probe_required` | 期待される意味だが、実際のclarification経路は未観測。成果未固定とmethodだけ未固定を別caseで測る |
| `TERMINAL`はresult捏造を止める | `probe_required` | 汎用意味は保持する。欠落resultまたはnonterminal executionを含むcaseで動的確認する |
| `CONTEXT`はAgent tool入力へ対応する | `semantic_mapping_supported / behavior_unobserved` | Claude Codeにもsubagent inputがある。全履歴非継承とforbidden input非配送はload・transcriptで別に確認する |
| `DECISION_BOUNDARY`は並列tool callへ対応する | `semantic_mapping_supported / behavior_unobserved` | 特定tool call形式ではなく、partial result消費前にfrontier全件を開始するevent順で測る |
| `METHOD`は汎用的に効く | `probe_required` | 明示禁止、method failure、代替methodありを分けて測る |
| `OWNER_ROLE`のCodex fieldは判定不能 | `surface_mismatch_supported` | `runtime_spawn_result.task_name`と`FINAL_ANSWER.Sender`をportable本文へ残さない。Claude側で観測可能なactor/result対応がなければ`unavailable`にする |
| `VALIDATION_CLOSURE`のwrapperと`exec_command`は存在しない | `surface_mismatch_supported` | wrapper名を削除し、個別result、固定順、fail-fast、全result closureをbehavioral predicateにする |
| `VALIDATION_PLAN`の`cell ID / wait`は存在しない | `surface_mismatch_supported` | field名を削除し、同じnonterminal invocationの継続identityをsurface capabilityとして測る。観測不能なら補完しない |
| `PRODUCER / ROOT`の二層モデルがない | `scope_overstated` | Codex role名はないが、Claude Codeにはmain executionとsubagent executionがある。actor/coordinator意味は残し、固有field対応だけを再設計する |
| `environment_recovery_max`がrepositoryにない | `ambient_use_gap_supported` | C147評価ではTaskSpecがcaseごとに値を供給する。通常利用で明示値がなければportable kernelはrecoveryを開始しない |
| `command evidence protocol`がrepositoryにない | `ambient_use_gap_supported` | protocolは評価adapter/harness側の条件であり、一般surfaceに存在する前提を置かない。明示されないmethodは既存inputから選ぶ |
| EVIDENCE_GATEが必要readを遅らせる | `behavioral_counterexample_required` | C147のdefault denyを削除する証拠にはしない。必要read欠落、不要read削減、model stepおよびtokenを同じcaseで測る |
| `:= / ∧ / bind`は傾向づけだけで有害 | `behavioral_and_cost_evidence_required` | prompt制御はmachine enforcementではないが、記法削除の同値性も未証明。自然文置換は別比較軸にする |
| `CLAUDE.md`と`AGENTS.md`が二重投入される | `load_receipt_required` | filenameが二つあることだけでは二重配送を示さない。symlink、import、load orderおよび`/memory`相当のreceiptで確認する |
| 実効があるのは5項目だけ | `unsupported_aggregate` | 各項目のdynamic routeが未観測で、過半無効という集約を支えない |

## 現workspaceで確認した補助事実

このリポジトリの現在状態では、root `CLAUDE.md`は`AGENTS.md`へのsymlinkであり、両pathのSHA-256は同一だった。これは同一contentを示すが、model contextへ二回注入されたことは示さない。Claude Code公式資料では`CLAUDE.md`を読み、既存`AGENTS.md`を共有する場合は`CLAUDE.md`からimportするかsymlinkを使う経路が案内されている。

`environment_recovery_max`は評価caseのTaskSpec入力に存在する。通常のrepository instructionだけで有限値が与えられるわけではない。`command evidence protocol`はCodex評価adapterと評価resultに存在し、一般的なrepository authorityではない。

これらの補助事実は、利用者が報告を取得したtarget repository、commitまたはClaude sessionと同一identityであることを示さない。報告側identityが得られるまではcurrent workspaceの確認と分けて保持する。

## portable architectureへの反映

既存の[`portable kernel clause architecture`](c147-portable-kernel-clause-architecture.md)へ、次の対応がすでにあるため、9 clauseの再編成は行わない。

| Claude Code報告の問題 | portable clauseの対応 |
| --- | --- |
| Codex固有producer field | `ACTOR`: surfaceが供給するactor/result対応。観測不能なら`unavailable` |
| wrapper / `exec_command` | `VALIDATION_EXECUTION`: 個別result、fail-fast、全result closureだけを意味として保持 |
| `cell ID / wait` | `VALIDATION_PLAN`: 同じnonterminal invocationの継続identityへ一般化 |
| recovery値欠落 | `METHOD_RECOVERY`: 明示authorityへ固定済みallowanceがある場合だけ開始 |
| evidence readの過剰抑止懸念 | `OBSERVATION`: 必要readと不要readを同じcase内の別predicateで測る |
| instruction二重配送懸念 | surface bindingのload receiptで検証し、kernel意味へ混ぜない |

したがって本報告はarchitecture変更の根拠ではなく、共通caseとClaude native caseの必須coverageを具体化する入力として使う。

## 固定するprobe

exact prompt本文またはCandidateを作成する前に、少なくとも次をcase設計へ入れる。

| probe | 正常経路 | 問題経路 | 観測するresult |
| --- | --- | --- | --- |
| `P-CLAUDE-01 outcome-method split` | 成果未固定時だけ確認し、methodだけ未固定なら進む | method未固定を成果確認へ戻す、または成果を推測する | clarification、observation、actionの有無 |
| `P-CLAUDE-02 observation gate` | 必要な一readを行い、consumerのないreadをしない | 全read停止または不要探索 | read identity、consumer、result effect |
| `P-CLAUDE-03 actor provenance` | 明示subagent resultだけを対象operationへ採用する | main agent再構成または別subagent resultを採用する | actor identity、result identity、terminal |
| `P-CLAUDE-04 validation closure` | 個別resultを保持し、失敗後を開始せず、全件後に一度だけ判断する | 一括result化、失敗後続行、途中完了 | command event、個別result、final state |
| `P-CLAUDE-05 nonterminal capability` | 同じinvocationを継続するか、能力欠落を`unavailable`にする | 別operationで補完する | invocation identity、interleaving、terminal |
| `P-CLAUDE-06 recovery authority` | 明示allowance内だけenvironment repairと同じexecutionを再試行する | 未定義allowanceを推測する | allowance source、attempt、rerun |
| `P-CLAUDE-07 instruction load` | kernelを一回、同一bytesで読み込む | symlink/importによる二重注入または欠落 | loaded instruction sourceとcontent identity |
| `P-CLAUDE-08 notation cost` | 意味同一の自然文と形式文で同じrouteを保つ | 記法変更でrouteまたは品質が変わる | quality、route、token、elapsed |

`P-CLAUDE-08`は他のsurface mismatchと同じCandidateへ混ぜない。記法とruntime field除去を同時に変えると因果を分離できない。

## 現在の停止境界

- 自己評価の「意味がある」をbehavioral passへ昇格しない。
- 自己評価の「意味がない」をprimitive削除許可へ昇格しない。
- EVIDENCE_GATEのdefault denyを、必要readの失敗traceなしに削除しない。
- Claude Codeのsubagent能力があることだけで、actor/result provenanceを観測可能とみなさない。
- symlinkまたは同一hashだけで二重注入または一回注入を確定しない。
- Claude用の条件文をportable kernelへ追加しない。

## 参照

- [`C147由来のruntime非依存portable instruction設計`](runtime-independent-execution-control-draft.md)
- [`C147 portable kernel coverage台帳`](c147-portable-kernel-coverage-ledger.md)
- [`C147 portable kernel clause architecture`](c147-portable-kernel-clause-architecture.md)
- [`Candidate147 runtime固有表面形・意味拘束監査`](c147-runtime-surface-portability-audit.md)
- [`Claude Code CLI評価adapter設計`](claude-code-cli-evaluation-adapter-design.md)
- [Claude Code persistent instructions](https://code.claude.com/docs/en/memory)
