# C147由来のruntime非依存portable instruction設計

> [!IMPORTANT]
> **状態**: `frontier_reopened_by_user / required_outcome_bound / source_candidate_c147 / target_surfaces_chatgpt_codex_claude_cursor_gemini / portable_kernel_exact_draft_written / q01_q08_static_counterexamples_repaired / target_instance_not_created / candidate_not_created / evaluation_not_started`
>
> 利用者が2026-08-14に、C147のCodex依存をなくし、ChatGPT Projectのproject instructions、Codex、Claude Code、CursorおよびGemini Gemで使える形へ進めることを明示した。本書はその要求、境界および作成前gateを固定する。Candidate本文、評価結果、採用、releaseまたはprojectionではない。

## 結論

C147 `the-caption-3ce91a4-result-effect-scope-r1`を別runtime向けに単純改名しない。次の三つを分離する。

1. **portable kernel**: 全対象環境へ同一bytesで渡す、製品名とruntime API名を含まない制御本文。文字数削減自体を目的または作成gateにしない。
2. **surface binding**: 同じkernelを各環境の指示面へ届ける配置だけを定める。制御条件を追加、削除または上書きしない。
3. **runtime別result**: 同じ意味が成立したかを環境ごとに独立して測定する。別runtimeの結果を互換比較へ混ぜない。

portable kernelに共通の固定文字数上限を置かない。利用者が確認した現在のChatGPT Projectの8,000文字枠にはC147相当量を収容でき、Gemini Gemでは文字数制限を観測していない。これらはsurfaceの現在値であり、制御意味を削る理由やkernelのidentityにはしない。各surfaceへ同一bytesを配送できるかはload portabilityの事前確認とし、本文の長さは品質と機序が成立した後のコスト診断に限定する。

## 利用者が求める結果

同じportable kernelを対象環境の永続指示面へ入れたとき、各環境で利用可能かつ許可された操作について、次の制御意味が同じであることを求める。

- 利用者が選ぶ成果と、AIが選ぶ手段を分ける。
- 未固定の成果は推測せず、その値だけを確認する。
- 観測は、未完了判断に現在必要な値を返せる場合だけ許可する。
- 一つの操作、一つの実行主体、一つの結果を対応づけ、別主体の記述で補完しない。
- 結果の効果を、その結果で対象、許可、手段または停止条件が変わる未開始操作だけへ限定する。
- 状態変更前に必要な成果全体、変更条件および維持条件を一案へ閉じる。
- 必須検証は開始前に全件と停止条件を固定し、個別結果を保持して、必要結果が揃うまで完了にしない。
- 利用不能な能力、未確認の結果または未許可の操作を、別手段や説明で成立したことにしない。

「動く」とは、各環境が実際に提供する能力の範囲で上の判断境界を守り、能力がない場合は`unavailable`として止まれることを指す。全環境が同じtool、並列実行、subagent、filesystem、commandまたは非同期resultを持つことは要求しない。

## 現行C147をそのまま使えない理由

C147本文は7,090文字であり、文字数自体は現在観測したChatGPT Projectの配送障壁ではない。変更理由は長さではなく、runtime固有の役割名、field、発行境界および継続方法を制御意味と同じ本文へ固定していることである。

Candidate204とCandidate205は、Codex固有表面語を0件にしてもC147の正の発行遷移、発行対象集合およびresult収集障壁を復元できなかった。短縮や一般語への置換だけでは意味保存にならない反例として扱う。portable kernelはC147より短いことを要求せず、必要な意味を保った結果として長くなることも許容する。

### 能力と観測点

C147は次のCodex固有表面を含む。

- `root / worker / session`
- `fork_turns=none`
- `runtime_spawn_result.task_name / FINAL_ANSWER.Sender`
- `model step / custom exec wrapper / exec_command`
- `cell ID / wait / commentary`
- `environment_recovery_max`

削除するのは名称であり、名称が担っていた次の意味まで削除してはならない。

- producerとcoordinatorの権限差
- producer起動identityと受領result provenanceの対応
- 選択済み操作を、途中resultを次判断へ使う前に開始する境界
- 検証結果の個別性、fail-fastおよび全result収集
- nonterminalな同一操作の継続
- 明示済みrecovery allowanceだけの消費

ただし、runtimeが機械的identity、発行atomicityまたは継続tokenを提供しない場合、それをcustom instructionだけで存在することにはできない。観測不能な機序を成功条件へ含めず、必要な制御がそれなしでは閉じない場合は当該環境で`unavailable`とする。

## portabilityの四段階

| 段階 | 判定内容 | 他段階から自動継承しないこと |
| --- | --- | --- |
| load portability | 同じkernelが指示面へ欠落なく入る | 読み込まれたことは遵守や機序成立を意味しない |
| semantic portability | 製品固有語なしで同じpredicate、permission、result effect、terminalを表す | 文面類似は実際の経路閉鎖を意味しない |
| behavioral portability | 固定caseで問題経路を閉じ、正常経路を維持する | 一runtimeの成功を他runtimeへ一般化しない |
| enforcement portability | runtime permissionまたはhookが判断と独立に操作を禁止する | prompt-only系列の成果として主張しない |

本研究の対象は前三段階である。第四段階を必要とする問題を、Claude Code、Cursor、Codex CLI、tool adapter、hookまたは外部wrapperの変更で解かない。

## surface binding

2026-08-14時点の公式資料へ基づき、同一kernelの配送先を次へ固定する。今後の仕様変更は新しいbinding revisionで扱う。

| 環境 | 配送先 | bindingに許可する差 |
| --- | --- | --- |
| ChatGPT Project | project instructionsへkernel本文を直接貼付 | なし |
| Codex / Codex developer surfaces | root `AGENTS.md`または対応するglobal guidance | 配置だけ |
| Claude Code | `CLAUDE.md`から同じ`AGENTS.md`をimport、または同一bytesを配置 | import指定だけ |
| Cursor | root `AGENTS.md`、またはAlways適用のproject rule | 配置metadataだけ |
| Gemini Gem | custom Gemのinstructionsへkernel本文を直接貼付 | なし |

kernelに製品名、ファイル名、tool名、field名または「この環境では」の条件分岐を入れない。surface bindingにも制御条件を追加しない。同じ意味を成立させるため環境別の条件文が必要になった場合は、同一kernelのportability不成立として記録する。

## C147 coverageの作成前gate

portable kernel本文へ進む前に、[`c147-functional-decomposition-reanalysis.md`](c147-functional-decomposition-reanalysis.md)の81 primitiveを一件ずつ次のいずれかへ分類する。

| classification | 条件 |
| --- | --- |
| `preserved_in_kernel` | runtime固有語なしで同じ入力、許可、正の遷移、禁止またはterminalをkernelが直接持つ |
| `surface_capability_bound` | 意味はkernelにあり、観測値または操作能力だけをruntimeが供給する。bindingは意味を変更しない |
| `not_applicable_to_common_target` | 共通targetに該当する操作classが存在せず、除外しても別経路へ意味が漏れない |
| `unresolved_runtime_boundary` | runtime固有の観測または強制がなければ問題経路を閉じられない |
| `removal_not_justified` | 省略の効果を保存証拠と共通caseで判定できない |

`unresolved_runtime_boundary`または`removal_not_justified`が一件でも残る状態で、見た目を簡潔にするため意味を省略しない。文字数にかかわらずcoverageが閉じなければCandidateを作成しない。

13条項の見出しをそのまま残すことは要求しない。ただし次の意味群を一つの短い一般論へ潰す場合、C147で別地点を閉じていた入口が全て残ることを示す。

| 意味群 | C147の供給元 |
| --- | --- |
| 成果と操作の形成 | `SPEC / INDEPENDENCE` |
| 実行主体と来歴 | `PRODUCER / OWNER_ROLE / ROOT` |
| 入力と観測の限定 | `CONTEXT / EVIDENCE_GATE` |
| 結果の局所効果と発行境界 | `DECISION_BOUNDARY` |
| 完了 | `TERMINAL` |
| 検証 | `VALIDATION_PLAN / VALIDATION_CLOSURE` |
| 手段失敗と回復 | `METHOD / RECOVERY` |

## 共通targetとruntime別測定

既存`the-caption` resultを横展開しない。ChatGPT ProjectとGemini Gemはローカルrepository、commandおよび同じproducer機能を前提にできず、targetとexecutorが同時に変わるためである。

### 共通のsemantic conformance target

新しい`namespaced` target instanceとして、toolを必要としない明示的な操作台帳をmodel-visible入力にする。各caseは、許可された観測、状態変更、検証、先行resultおよび停止条件をテキスト上で固定し、全環境で同じ入出力を扱えるようにする。

最低限、次の経路を別caseへ分ける。

1. 未固定成果だけを確認し、証拠探索を始めない。
2. 手段だけが未固定なら、成果確認へ戻らない。
3. consumerのない観測を発行しない。
4. 一resultの失敗を独立操作へ伝播させない。
5. provenanceが対応しない結果で完了しない。
6. 必須検証の一件失敗後に後続を成功扱いしない。
7. 能力または観測点がない場合に結果を補完せず`unavailable`にする。

共通Caseと採点境界は[`Portable instruction semantic conformance評価設計`](portable-instruction-semantic-conformance-evaluation-design.md)を正本とする。all-agent `total_tokens`を一次値として取得できないUI surfaceは正式なv4 resultへ登録せず、surface diagnostic receiptへ留める。3 KPIとcompatibility conditionを固定できるruntimeだけが、同じtarget内のbaseline対kernelを正式に測定できる。runtime間で`quality_score`、tokenまたはelapsedの絶対値を比較しない。

### native execution series

semantic conformance通過後に限り、Codex、Claude CodeおよびCursorでは各runtimeのnative operationを使う別系列を作る。ChatGPT Webで同じnative capabilityを持たないcaseを無理に対応づけない。各runtimeのprompt injection、permission、tool result、token accountingおよびelapsed sourceを独立したcompatibility conditionへ固定する。

## Candidate作成前の残件

管理用のportable kernel本文草案と81 primitive逆引きは[`C147 portable kernel一枚化草案`](c147-portable-kernel-one-sheet-draft.md)、14件のheld-out、private oracle、ratingおよび汎用graderは[`held-out r1`](portable-instruction-semantic-conformance-heldout-r1/)で固定した。現時点では次が未完了なので、Candidate bundle、profileまたは評価slotを作成しない。

1. control-free baselineの測定成立。
2. 各surfaceで同一bytesが読み込まれたことのreceipt。
3. 品質、機序、対象外影響、KPIおよび安定性のruntime別停止条件。
4. formal target identity、直接の基準、allowed deltaおよび非目標の固定。

control-free baseline前の測定成立監査では、repository target v1へprotocol identityを偽装しない[`semantic target登録設計`](portable-instruction-semantic-target-registration-design.md)、単一Case packet materializer、v2 subject/runtime compatibility preflight、formal target登録、共通TaskSpec wrapper、runtime capability catalog、persisted all-agent transcript contractおよびCodex N=1 Profileまで固定した。次の作業は14 Caseのwrite-once dispatch planとProfile preflightを固定し、adapter実行入口をそのplanへ限定することである。成功動作のtool順を短い手順へ転記せず、C204/C205で消えた正の遷移、対象集合および収集障壁を採点可能なまま保持する。

Claude Code自身によるC147の静的適用可能性報告は[`C147 Claude Code自己評価のtriage`](c147-claude-code-self-assessment-triage.md)へ記録した。Codex固有field、wrapper、継続identityおよびambient recovery/protocol不足はsurface mismatchとして採用し、EVIDENCE_GATEの有害性、形式記法の実効および5項目だけが有効という集約はdynamic probe待ちとする。

runtime別の3 KPI、instruction isolationおよびprovenanceの測定可否は[`Portable instruction runtime別測定成立監査`](portable-instruction-runtime-measurement-feasibility-audit.md)を正本とする。2026-08-14時点でformal runtime候補はローカルで観測したCodex CLIとClaude Code CLIに限り、ChatGPT Project、Cursor UIおよびGemini Gemはsurface diagnosticから開始する。

## 停止条件

- 簡潔さ、文字数またはsurfaceの推奨長だけを理由に、保存証拠が支えるC147の意味を未評価で削る。
- 製品固有語を別の製品固有語へ置き換える。
- surface bindingがkernelのpermission、dependency、result effectまたはterminalを変更する。
- custom instructionsだけでは観測不能なidentityやatomicityを、成立済みと宣言する。
- 一runtimeの成功を他runtime、別target、採用、releaseまたはprojectionへ一般化する。
- 既存THE-CAPTIONのcase、fixture、oracleまたは保存resultをportable系列へ混ぜる。

いずれかが成立した案は`prompt_control_not_demonstrated / candidate_not_created`として棄却し、外部executor変更へ広げない。

## 公式surface資料

- [ChatGPT custom instructions](https://help.openai.com/en/articles/8096356-custom-instructions-for-chatgpt)
- [Codex custom instructions with AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
- [Claude Code persistent instructions](https://code.claude.com/docs/en/memory)
- [Cursor rules and AGENTS.md](https://docs.cursor.com/context/rules-for-ai)
- [Gemini custom Gems](https://support.google.com/gemini/answer/15235603)

## リポジトリ内参照

- [`prompt-control-design-principles.md`](prompt-control-design-principles.md)
- [`c147-functional-decomposition-reanalysis.md`](c147-functional-decomposition-reanalysis.md)
- [`c147-control-group-overlap-optimality-audit.md`](c147-control-group-overlap-optimality-audit.md)
- [`c147-runtime-surface-portability-audit.md`](c147-runtime-surface-portability-audit.md)
- [`candidate204-m5-causal-analysis.md`](candidate204-m5-causal-analysis.md)
- [`candidate205-m5-causal-analysis.md`](candidate205-m5-causal-analysis.md)
- [`claude-code-cli-evaluation-adapter-design.md`](claude-code-cli-evaluation-adapter-design.md)
- [`c147-claude-code-self-assessment-triage.md`](c147-claude-code-self-assessment-triage.md)
- [`portable-instruction-semantic-conformance-evaluation-design.md`](portable-instruction-semantic-conformance-evaluation-design.md)
- [`portable-instruction-runtime-measurement-feasibility-audit.md`](portable-instruction-runtime-measurement-feasibility-audit.md)
- [`evaluations/targets/README.md`](../evaluations/targets/README.md)
