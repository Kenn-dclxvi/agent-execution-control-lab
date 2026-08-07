# Runtime非依存Execution Control抽象化 草案

> [!NOTE]
> **状態**: `draft / deferred / candidate_not_created / evaluation_not_started`
>
> この文書は将来の横断設計を残すための草案であり、prompt制御の正本、Candidate、評価結果、採用判断、release、projectionのいずれでもない。現在は[`feature_review_phase1`](feature-review-phase1-plan.md)の機能見直しを優先し、本草案を現行frontierとして進めない。FR-01のquality reviewと将来のaudit見直しは同一機能として扱わない。

## 結論

現在の機能見直し・追加を先に進め、その結果として採用されたpromptが安定した後に、**runtime固有のfield、tool名、待機identity、context継承表現を一度横断監査し、制御上の不変条件とruntime上の観測方法を分離する**。

再開時はCandidate147を固定親としない。機能見直しの結果、新しいpromptが採用されていれば、その時点の`adopted`なprompt identityを比較基準へ一意にbindする。Candidate147は現時点の基準・履歴として保持し、過去releaseをin-placeで書き換えない。

抽象化案はまずCodexの既存互換条件を固定した比較で検証する。そこで確認するのは「Codex固有の語や観測形式をprompt本文から減らしても、既存の品質・route・terminal closureを維持できるか」であり、Codexでの成功だけからClaude Codeその他runtimeでの互換性を主張しない。

## 背景

現行root `AGENTS.md`へ逐語転記されているCandidate147系の制御には、構造的不変条件とともに次のようなruntime固有表現が含まれる。

- `fork_turns`
- `runtime_spawn_result.task_name`
- `FINAL_ANSWER.Sender`
- `wait`
- `custom exec wrapper` / `exec_command`
- `validation wrapper` / `cell ID`
- `environment_recovery_max`

これらはCandidate147の評価時に成立した制御本文の一部であり、現時点では削除・置換済みとは扱わない。一方、[`candidate71-control-abstraction-analysis.md`](candidate71-control-abstraction-analysis.md)では、制御の構造とruntime上のprovenance観測手順を分離して読む必要性が既に示されている。

また、[`claude-code-cli-evaluation-adapter-design.md`](claude-code-cli-evaluation-adapter-design.md)のprobeでは、Claude CodeはCodexとは異なるprompt注入、subagent identity、command evidence、token accountingを持つため、既存Codex resultとの互換比較が成立しないと整理されている。この差は外部runtimeを変更して解く対象ではなく、**prompt側が特定runtimeの表面形へ過剰に依存していないかを診断する材料**として使う。

## 目的

1. prompt本文に残すものを、runtimeのAPI名ではなく**成果品質を維持する制御不変条件**へ寄せる。
2. runtime固有fieldやprimitiveが必要な場合も、それ自体を制御の意味と混同しない。
3. 機能追加後のprompt全体を対象に一度依存箇所を棚卸しし、同じ意味の依存をまとめて分類する。
4. 抽象化による品質・route・costへの影響を、既存のCodex比較基盤でprompt差分として測定する。
5. 将来別runtimeを評価する場合、promptの意味差とexecutor差を分離しやすい状態にする。

## 非目標

- Claude Code CLI、Codex CLI、tool adapter、runtime hook、外部wrapperを変更して問題を解かない。
- Claude Codeで利用できるprimitiveへ一対一で書き換えることを目的にしない。
- Codexでの評価結果をClaude Codeその他runtimeへ一般化しない。
- 現在進行中の機能見直しとruntime抽象化を同一Candidateまたは同一比較単位へ混ぜない。
- Candidate147のrelease、評価result、projectionを後から書き換えない。
- 未定義のrecovery回数やruntime capabilityを推測で補完しない。
- 本草案だけを根拠にCandidate、採用、release、projectionへ進めない。

## 抽象化の基本形

prompt本文では次の二層を分離して扱う。

```text
control invariant
    ↓
runtime-observable binding
```

`control invariant`はTaskSpec、repository authority、producer/result/terminal stateなど、runtimeが変わっても維持したい意味を固定する。

`runtime-observable binding`は、そのruntimeで不変条件を観測・実行するためのfield、ID、tool invocation、return shapeである。runtime固有表現をprompt本文へ残すのは、抽象的な不変条件だけでは既存の誤経路を防げないことを互換試験で確認した場合に限る。

## 現時点の抽象化候補

以下はCandidate仕様ではなく、再開時に検証する仮説である。

| 現行のruntime固有表現 | 抽象化する意味の候補 | 再開時の論点 |
| --- | --- | --- |
| `fork_turns=none` | producerへ必要十分な明示contextだけを渡し、不要な履歴継承を行わない | 継承量の数値指定まで品質に必要か |
| `runtime_spawn_result.task_name` / `FINAL_ANSWER.Sender` | 起動前にbindしたproducer execution identityと、受領resultのprovenanceを同一operationへbind可能である | どの観測証跡までをpromptで要求する必要があるか |
| `wait` | 同期・待機resultそのものをproducer identityの代替証跡にしない | 待機primitive名の禁止が必要か、provenance条件だけで十分か |
| `custom exec wrapper` / `exec_command` | required validationを個別execution unitとして扱い、順序、individual pass condition、stop condition、fail-fast、全result集約を維持する | command間model re-entry禁止が不変条件か、Codex固有配送方法か |
| `validation wrapper` / `cell ID` | nonterminal validation executionを一意なidentityへbindし、そのexecutionがterminalになるまで別operationへ進まない | 特定の`cell ID`というfield名が必要か |
| `environment_recovery_max` | environment recoveryを始める前に、同一operationで消費可能なrecovery budgetが明示的にbindされている | budget authorityと未定義時の扱いをどこで固定するか |

## 再開時の設計手順

### 1. 基準promptを固定する

再開時点で`adopted`なprompt identityを一意にbindする。機能見直しでCandidate147以後のpromptが採用されていれば、そのpromptを基準とし、Candidate147へ戻して抽象化しない。

### 2. runtime依存を横断棚卸しする

基準promptと適用中repository instructionから、特定runtimeの次の要素を直接参照する表現を列挙する。

- field / return schema
- tool / primitive名
- context inheritance method
- asynchronous execution / wait identity
- command dispatch method
- recovery counter / capability

今回観測した7語だけで一覧を固定せず、機能追加で新しく導入された依存も同じ棚卸しへ含める。

### 3. 依存を分類する

各表現を次のいずれかへ分類する。

- `semantic_invariant`: runtime名を外しても意味を一意に固定できる。
- `observable_binding_required`: 意味は抽象化できるが、誤result admission等を防ぐため観測可能なruntime bindingが必要。
- `method_detail`: 現在のruntimeでは実装方法として使われているだけで、prompt不変条件には不要な可能性がある。
- `unresolved_runtime_boundary`: repository内promptだけでは強制できる表現へ落とせない。

`unresolved_runtime_boundary`は外部executor変更へ展開せず、このrepositoryでは未解決として停止する。

### 4. Candidate単位を切る

棚卸しはまとめて行うが、比較Candidateでは因果を失わない単位へ分ける。同じ抽象化原理で一つの判断として扱える表現だけを一変更へまとめ、producer provenance、validation配送、context境界、recovery budgetなど異なるeffectを無条件に一Candidateへ混ぜない。

### 5. Codex条件で互換比較する

保存済みresultを比較基準にする場合は、評価slot発行前に通常のpreflight gateを通す。宣言したprompt identity以外のEvaluation set、case、fixture、TaskSpec、rating、model、reasoning、Agent/runtime/CLI、permission、executor behavior、token accounting等を一致させる。

最初に変更対象のcontrol pathを直接観測するtargeted gateを行い、qualityとmechanismを確認する。targetedで成立した場合だけ、必要なStandard14およびcost比較へ進む。

## Codex評価で言えること／言えないこと

### 言えること

互換条件を固定したCodex試験で品質・必要route・terminal closureが維持された場合、対象のruntime固有表現について、**そのCodex条件では従来の具体語が制御成立の必要条件ではなかった**と判断できる。

### 言えないこと

- Claude Codeで同じrouteが成立する。
- runtime間でtoken、elapsed、tool callが直接比較できる。
- 抽象文だけで任意runtimeのprimitive差を吸収できる。
- executor側のatomicity、delivery、identity不足をpromptで補完できる。

別runtimeでの実証が必要なら、Codex系列とは別の互換条件・baseline・resultとして扱う。

## 再開条件

本草案は次のいずれかが成立するまで`deferred`を維持する。

1. 現在優先している`feature_review_phase1`の機能追加・判定が、runtime抽象化の基準promptを固定できる区切りまで到達した。
2. ユーザーがruntime依存低減を明示的に再開した。

再開時には、最初に**その時点のadopted prompt全体のruntime依存inventory**を作り、本草案の候補表を現在値として使い回さない。

## 未決事項

- `VALIDATION_CLOSURE`で保持すべき本質は、個別validation、fail-fast、全result受領後の一度の判断までか、command間model re-entry禁止まで含むか。
- producer provenanceの最低限の証跡を、runtime field名なしでどこまで一意に固定できるか。
- context継承の「最小」を量ではなくinformation boundaryとして定義した場合、既存のCONTEXT効果を維持できるか。
- `environment_recovery_max`のauthorityをTaskSpec、repository instruction、別の固定設定のどこへ置くべきか。
- 機能見直し系列で新しいruntime依存表現が追加されるか。

## 関連文書

- [`feature-review-phase1-plan.md`](feature-review-phase1-plan.md): 現在優先する機能見直しフェーズ。
- [`prompt-control-design-principles.md`](prompt-control-design-principles.md): prompt制御の設計原則の正本。
- [`candidate71-control-abstraction-analysis.md`](candidate71-control-abstraction-analysis.md): 構造的不変条件とruntime依存表現を分ける先行分析。
- [`claude-code-cli-evaluation-adapter-design.md`](claude-code-cli-evaluation-adapter-design.md): Claude Code CLI条件を既存Codex resultと分離して扱う評価adapter設計。
- [`prompt-comparison-workflow.md`](prompt-comparison-workflow.md): 比較条件とLayer境界の正本。
