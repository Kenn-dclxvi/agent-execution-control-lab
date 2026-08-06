# Prompt set KPI evidence workflow

## 目的

固定条件下の各runを独立して保存し、後から実効互換条件を満たす任意のrun集合を固定して集計・比較する。`N`はrunのidentityではなく、分析時に選択したsample件数とする。

扱うKPIは次の3つだけとする。

- `quality_score`: case成果全体の0〜4 scoreから算出した値
- `total_tokens`: root agentと、そのrunから起動された全SA sessionの最終token usageの合計
- `elapsed_seconds`: task開始から終了までの時間

Worker routing、child session数、root / child token内訳、並列／逐次実行、再割当てはdiagnosticであり、KPIへ追加しない。比較viewはこれらの診断値をKPI差の説明に使えるが、Worker起動の有無だけで品質またはコスト判定を反転させない。

選択した各sampleの`total_tokens`と`elapsed_seconds`は全caseの合計、`quality_score`は全case scoreを0〜100へ正規化した値とする。代表値は選択sampleの中央値である。数値差は明示したcandidate analysisからreference analysisを引くが、優先順位、閾値、`winner`、改善・悪化を出力しない。

このworkflowはpromptの作成、改善、採用、release判断、THE-CAPTION本体反映を行わない。

採用側がtokenまたはelapsedの許容幅を使う場合、その値、直接baseline、比較単位をcandidate result確認前に別artifactへ固定する。Layer 4は許容幅やwinnerを生成せず、compatibility keyが異なるresultを正式なコスト判定へ渡さない。

## 保存単位

2026-07-31以降の一次保存単位は、1つのimmutableな`prompt_set_identity`、1 case、1 sampleにbindしたatomic runである。run poolはprompt identityとcase別の実効条件だけを持つ検索索引であり、member一覧、`N`、coverage、iteration集合を持たない。

`desired-count`は不足runをmaterializeするwrite-once dispatch planだけに置く。pool内の保存runをcase別に数え、要求件数との差だけを発行する。例えばStandard14のF03だけ5件あり、全caseを5件へ揃える場合は、残る13 case × 5 = 65 runだけを発行する。分析時は使用するatomic run IDをselection receiptへ固定し、その派生analysisを作る。既存selection、analysis、runを更新しない。

実行schedulerは分析互換性と分離する。同じ`resource_class`で実行できる独立runは、prompt、case、coverage、計画sample数が異なっても一つのpair-aware global queueへ入れてよい。比較対象の同一case / sampleを近接配置しつつ、空いたworkerへ次のready runを投入する。このhostの新規試験は外側並列上限を`M=24`へ固定する。

`prompt_set_identity`は少なくとも次を含む。

```json
{
  "name": "<prompt set name>",
  "revision": "<immutable revision>"
}
```

`revision`の代わりに、または併記してlowercase SHA-256の`bundle_sha256`を使用できる。可変の名前だけではresultを登録できない。

## Layer

| Layer | 役割 | 出力 | 禁止 |
| --- | --- | --- | --- |
| 1. Evaluation set | 外部setとfixtureを固定する | revision、set identity、case別fixture identityを含むcapsule | 結果を見た後のin-place変更、prompt変更 |
| 2. Execution | 1 prompt setの1 case / 1 iterationを実行する | 成果、`total_tokens`、時間、model-invisible binding | 採点、比較、prompt変更 |
| 3. Quality rating | 各成果をblindで採点する | 0〜4のscoreと短い事実根拠 | prompt identityの参照、比較、改善提案 |
| 4. KPI comparison | prompt set resultを登録し、保存resultからviewを作る | append-only result、任意個の一覧・中央値・明示差分 | 一次結果の変更、優劣判定、改善提案 |

情報はLayer 1から4へ一方向に渡す。各Layerは自分の出力だけを作り、既存出力を上書きしない。比較viewは保存済みresultを参照する派生artifactであり、一次結果を変更しない。

fixtureとworkspaceの物理materializationはLayer接続の実装詳細である。sourceとdestinationの独立性および論理contentを保つ限りCopy-on-Writeを使用でき、copy方式をprompt set identity、互換条件、KPIへ追加しない。storage監査とGCは[`evaluation-storage-maintenance.md`](evaluation-storage-maintenance.md)に分離する。

## Capsule boundary

Evaluation set sourceは`set_id`と`revision`を持つ。Run capsuleは次を分離する。

- `binding`: `prompt_set_identity`、`case_id`、`iteration`
- `comparison_conditions`: prompt identity以外の互換条件
- `adapter` / `parameters`: executor入力。`parameters`は基盤に対してopaque

`comparison_conditions`は次を必須とする。

- `target_repository_ref`
- `model`
- `agent_environment`
- `task_spec`
- `permission`
- `executor_parameters`
- `quality_rating`。rating contract identity、owner-producer evidence revision、必要な場合はall-agent command evidence revisionを含む
- `repetition_condition`。少なくとも正の整数`iterations`を含む

prompt bundle pathやprompt固有parameterを`comparison_conditions.executor_parameters`へ混ぜない。比較対象間で固定するexecutor条件だけを格納し、prompt固有値は`binding.prompt_set_identity`またはopaqueな`parameters`へ置く。

`comparison_conditions.executor_parameters.token_accounting`には、`scope: all_agents`、`revision: v1`、`source: codex_rollout_final_usage_by_workspace`を固定する。異なるscopeまたはrevisionを持つresultは互換比較しない。

Agentがmodelへ提示するskill、app、plugin catalogが変わり得る実行では、その有効・無効policyとmodel-visible catalog identityを`comparison_conditions.agent_environment`へ固定する。adapterはroot rolloutの`skills_instructions / apps_instructions / plugins_instructions` blockからidentityを計算する。expected identityと異なるrunは外部計測失敗として除外し、同じslotを再実行する。profile上のruntime identityだけで実効catalog一致を推定しない。

Layer 1は`.git`内部を除くfixtureのpath、type、mode、contentまたはsymlink targetからcase別fixture identityを計算する。atomic runの実効条件にはEvaluation set identity、対象case、case別fixture identity、TaskSpec、model、Agent/runtime/CLI、permission、executor挙動、rating、token accountingを含める。`N`、coverage、iteration集合、計画順序、`max_workers`は実効条件へ含めず、完全なexecution provenanceとstratumとしてrunへ保存する。

保存済みresultを基準にする比較では、fixtureを同じsourceから再生成しない。基準resultと対応する保存済みLayer 1を`prepare-comparison-layer1`で検証・複製し、candidate capsuleとglobal planの生成後に`preflight-comparison`で全互換条件を照合する。比較用Layer 1の生成receiptがあるcycleでは、Layer 2がpreflight receiptを実行直前に再検証する。

## `quality_score`

quality raterが各caseの成果全体を0から4で採点する。

```text
quality_score[i] = sum(case_score[i]) / (4 * case数) * 100
quality_score = median(quality_score[1], ..., quality_score[N])
```

quality raterへ渡すのはmodel-visible caseとblindなexecution evidenceだけである。`layer2/bindings/`、Run capsule、oracle、grader、expected resultをmodel-visible入力へ混ぜない。raterはscoreと短い事実根拠だけを返し、promptの選択や改善提案を行わない。

現行rating contractは[`outcome-terminal-state-evidence-owner-diagnostic-v14`](../evaluations/rating-contracts/outcome-terminal-state-evidence-owner-diagnostic-v14.json)とする。v14は第13版の条件をすべて維持し、A01だけを応答文面の分類からversioned terminal-state evidenceへ切り替える。`required_value_state=unresolved`、terminal responseあり、final changed path 0件、試験・変更operation未開始を合わせて`outcome_state=awaiting_required_value`とする。疑問符、質問語、文末表現、応答本文はこの状態の導出とquality scoreに使用しない。本文は表示証拠として保持する。command evidenceは`all-agent-command-evidence/v5` collectorを要求し、A01には`terminal-state-evidence/v1`も要求する。revision別要求の正本は[`evaluations/rating-contracts/README.md`](../evaluations/rating-contracts/README.md)とする。

v14が維持するv13の要点は次のとおりである。

- 実行役へ提示した成果条件が抽象的なときは、成立を判定できる任意の証拠で満たされたとみなす。提示した抽象条件を特定の質問項目、特定の試験コマンド、特定の実装手順へ具体化して必須要求へ格上げしない。コマンド名がmodel-visibleに明示された場合だけ、そのコマンドを必須試験として扱う。
- score `4`は、提示した成果条件と禁止境界をすべて満たすこと（`case_quality_rules`で`diagnostic_only`とした提示要素を除く）と、TaskSpecまたは適用されるリポジトリ規則がコマンド名まで明示した必須試験の成功証拠があることを要件とする。
- command evidenceは`all-agent-command-evidence/v5` collectorで`command`と`exit_code`をbindする。終了状態を取得できない実行は計測失敗として除外し同じ枠を再実行する。コマンド名まで明示された必須コマンドの未実行または失敗だけをqualityへ反映し、提示した抽象条件から特定コマンドを推定して必須化しない。
- owner-producer evidence（担当者と生成者の証跡）はrunごとにbindするが、**診断だけに使用し成果品質の点数を変更しない**。format違反、評価器所有の一時出力削除試行、F10 Monthlyの数値line状態も診断へ保存する。
- rater入力では、候補の識別情報、条件名、実行役へ提示していない正解条件・質問項目・試験コマンド、提示した抽象条件から推定した特定コマンドを必須試験として扱う判断、優劣または採用情報を禁止する。

許可path判定はLayer 2 adapterをSSOTとし、Layer 3は必須成果pathだけを確認する。既存resultは履歴として保持し、rating contract revisionが異なるresultを互換比較へ混ぜない。

2026-07-26に[`Baseline、ControlFreeRepository、Candidate5、Candidate35、Candidate43、Candidate71の標準14項目各N=5`](../evaluations/results/baseline-control-free-repository-c5-c35-c43-c71-v13-standard14-n5_2026-07-26.md)を最初のv13互換result集合として登録した。各条件70 / 70件、計420 / 420件がvalid・rateableである。v12以前のresultは同一comparisonへ混ぜない。v14はv13とは別のcompatibility conditionであり、v13以前のresultと同一comparisonへ混ぜない。v10 / v11 / v12 / v13 profileは既存resultの再現用として保持する。

なお、この節が以前`outcome-abstract-condition-preserving-owner-diagnostic-v13`を現行として指定していた記述は、v13時点の契約に基づくものである。v13で採点した既存resultは当時の契約のまま保持し、v14で再採点したものとして扱わない。同様に、この節が以前`owner-producer-quality-v8`を現行として指定し、owner-producer evidenceをscore `4`の必要条件、response markerのNFKC / casefold照合を要求していた記述は、v8時点の契約に基づくものである。v8からv12で採点した既存resultは当時の契約のまま保持し、再採点しない。revision別の要求は[`evaluations/rating-contracts/README.md`](../evaluations/rating-contracts/README.md)を参照する。

## Evaluation foundation世代

評価基盤（evaluation foundation）の世代は、単独の`v1` / `v2` / `v3` / `v4`で表記する。この節を世代遷移の正本とする。採点契約（`Rating v13` / `Rating v14`）、result schema（`prompt-set-result/v1`）、command evidence protocol（`command evidence v3`）は別系統の版番号であり、単独の`vN`で書かない。

| 世代 | 保存単位 | 主なartifact | 状態 |
|---|---|---|---|
| v1 | cycle単位 | `winner`、`kpi_order`、`decision.json` | 履歴 |
| v2 | 固定A / B比較 | `comparison.json`、`difference_b_minus_a` | 履歴 |
| v3 | 1 prompt setごとのappend-only registry result | `prompt-set-result/v1`（root-only token）、`prompt-set-result/v2`（all-agent token） | 履歴互換 |
| v4 | 1 case × 1 sampleのatomic run | `runs/<atomic_run_id>.json`、`pools/<pool_key>.json` | 現行 |

切替点は次のとおり。

- **v1 / v2 → v3**: v1 cycle、result、profileは2026-07-15までに作成した。同日中にv3 registry resultの登録も始まっているため、result file名だけでは世代を分離できない。個々のresultの世代は、当該resultが宣言するschema fieldを正とする。
- **v3内のtoken accounting改訂**: 2026-07-16までに保存した`prompt-set-result/v1`は`total_tokens`へroot agentだけを数えている。all-agent revisionは`execution-capsule/v2`、`evaluation-set/v2`、`execution/v3`、`prompt-set-result/v2`、`prompt-set-comparison-view/v2`を使う。詳細は「旧artifactの扱い」節を正本とする。
- **v3 → v4**: 2026-07-31に[`scripts/atomic_run_registry.py`](../scripts/atomic_run_registry.py)を追加した時点で切り替わった。`evaluations/results/`でv4経路の最初のresultは[`Candidate106 / Candidate107 Standard14 atomic N=5`](../evaluations/results/candidate106-candidate107-validation-wrapper-reentry-closure-v14-medium-standard14-atomic-n5-cli0146_2026-07-31.md)である。以降のfile名は`-atomic-n<N>-`または`-atomic-reuse-`を持つ。

世代間の扱いは次に限定する。

- 旧世代のresultを新世代のschemaへin-place変換しない。identityと内容を遡及変更しない。
- v3 prompt-set resultをv4へ取り込む場合は、`atomic_run_registry.py import-result`による索引化だけを行う。元resultは変更しない。
- 異なる世代のresultを同一comparisonへ混ぜない。
- 世代を上げる場合は、この節へ行を追加し、切替点と最初のresultを併記する。既存行を書き換えない。

## Append-only result registry

### Atomic run registry（現行）

[`atomic_run_registry.py`](../scripts/atomic_run_registry.py)は次をwrite-onceで保存する。

```text
<registry>/
├── runs/<atomic_run_id>.json
└── pools/<pool_key>.json
```

`runs/`は1 runのidentity、実効条件、execution provenance、3 KPI、sourceを保持する。`pools/`は実効互換なrunを検索するための条件索引であり、run memberや件数を保持しない。既存prompt-set resultは`import-result`でatomic runへ索引化できる。元resultは変更しない。

`plan-missing`はpool内のrunをcase別に数え、不足slotだけをdispatch planへ固定する。`select-runs`はcaseごとに選んだrun IDをselection receiptへ固定する。`aggregate-selection`と`compare-analyses`は派生artifactだけを作る。

### Prompt-set result registry（履歴互換）

`record-result`は全caseと`1..N`が揃い、全valid runが採点済みであることを確認して次へwrite-onceで保存する。

```text
<registry>/
└── results/
    └── <result_id>.json
```

各resultは次を保持する。

- immutableな`prompt_set_identity`とそのSHA-256
- 互換条件の実体と`compatibility_key`
- case別の`quality_score`、`total_tokens`、`elapsed_seconds`
- iteration別の3 KPIと中央値
- 除外attempt
- 作成時刻とresult全体のcontent SHA-256

registryは比較相手を固定するmutable indexを持たず、`query-results`が保存fileを走査する。既存resultを別比較のために書き換えたり、現行prompt revisionへ読み替えたりしない。

## 互換条件と任意個比較

atomic比較では、prompt identityを除いたcase別の実効条件から`comparison_key`を作る。計画上の`N`または`max_workers`だけが異なるrunは同じpoolへ蓄積できる。`max_workers`差は消去せずexecution stratumへ残し、比較viewはstratum別件数と差分を併記する。model、CLI、model-visible catalog、fixture、TaskSpecなど実効条件が異なるrunは同じpoolへ入れない。

poolの一部caseだけを選ぶ場合、selectionの`comparison_key`は選択caseの実効条件だけから再計算する。pool全体のcoverageを引き継がない。`register-selection-result`は選択済みatomic runと固定profileを照合し、保存済み比較resultから全fixture catalogを継承できる。これにより、Standard14 pool内のA01 / A02 / F01だけを新しいtargeted比較へ再利用しても、残りcaseの再実行やrun identityの書換えを必要としない。

以下の`compare`は履歴互換のprompt-set result経路である。

`compare`は2件以上の`result_id`を受け付ける。全resultの`compatibility_key`と互換条件実体が完全一致しない場合はfail closedする。

viewには選択した全prompt setのidentity、iteration別KPI、中央値、除外attemptを列挙する。数値差は利用者が指定した`reference_result_id`をsubtrahendとし、他の各resultをminuendとして次の形で出力する。

```json
{
  "minuend_result_id": "<selected result>",
  "subtrahend_result_id": "<reference result>",
  "kpis": {
    "quality_score": "minuend - subtrahend",
    "total_tokens": "minuend - subtrahend",
    "elapsed_seconds": "minuend - subtrahend"
  }
}
```

差分の符号を有利・不利へ変換しない。referenceは基準線にすぎず、baseline、採用状態、順位を意味しない。

## Token accountingとextension boundary

評価基盤が解釈するtoken値はall-agentの`total_tokens`だけである。adapterはrootの`codex exec` sessionを起点に、同じevaluation workspaceを持つ全descendant sessionの最終`total_tokens`を合算する。cached inputを含む各sessionのprovider報告値を使用し、親子間の重複を補正しない。

root / SA別値、thread identity、session数、rollout fileなどの集計根拠は`layer2/extensions/<run_id>/all-agent-usage/`へ分離する。これらの内訳はquality ratingとKPI comparisonへ入力しない。root sessionまたはdescendant sessionの最終usageが欠ける場合は推定せず、`codex_all_agent_usage_incomplete`の外部計測失敗としてrunを除外し、同じslotを再実行する。

## 旧artifactの扱い

2026-07-15までに作成したv1 cycle、result、profileには`winner`、`kpi_order`、`decision.json`が含まれる。v2には固定A / Bの`comparison.json`と`difference_b_minus_a`が含まれる。いずれも当時の契約による履歴であり、内容やidentityを遡及変更しない。

v3のall-agent token accounting revisionは`execution-capsule/v2`、`evaluation-set/v2`、`execution/v3`、`prompt-set-result/v2`、`prompt-set-comparison-view/v2`を使用する。root agentだけを`total_tokens`へ保存したv3 `prompt-set-result/v1`と`prompt-set-comparison-view/v1`は履歴として保持し、in-place変更しない。保存sessionから完全に再構成できる場合だけ、元result IDを由来としてv2 resultをappend-only追加する。v1/v2 evaluation foundation cycleをv3 resultとして読み込まない。
