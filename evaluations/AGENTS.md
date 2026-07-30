# evaluations instructions

`evaluations/`の指示は、evaluation foundation v3の境界を扱う。root `AGENTS.md`の共通規則に加えて、この領域規則を適用する。評価基盤のLayerと境界は`docs/prompt-comparison-workflow.md`、実行方法は`docs/evaluation-loop-manual.md`を正本とする。

## Target instance

計測系列は評価対象repositoryごとのinstanceとして別管理する。instanceの登録、layout、境界の正本は`evaluations/targets/README.md`とする。

- target非依存のkernel（`scripts/`のfixture固定と4 Layer実行、`layer2/`）へ、target固有のpath、case ID、分岐を追加しない。
- target固有の採点補助はinstance側のmoduleとして分け、既存instanceのmoduleを新instanceの都合で変更しない。
- 既存instance `the-caption`のartifact path（`evaluations/cases`、`evaluations/profiles`、`evaluations/sets`、`evaluations/rating-contracts`、`evaluations/results`、`prompts/`配下）を移動しない。
- 新instanceのartifactは`evaluations/targets/<target_id>/`配下へ閉じる。
- 別instanceのresultを同一比較へ入れない。rating contractがinstance単位である以上、`quality_score`の絶対値をinstance間で比較しない。
- instanceのdescriptorは参照とtarget固有identityだけを持ち、gate command、bundle target map、resultの実体を複製しない。

## 4 Layer

評価は次の4 Layerに限定する。

1. Evaluation set
2. Execution
3. Quality rating
4. KPI comparison

各Layerは自分の出力だけを作る。

- 前段artifactを変更しない。
- 後段の判断責務へ越境しない。
- prompt作成、改善提案、採用、release、本体反映を評価基盤へ持ち込まない。

## 3 KPI

評価基盤が扱うKPIは次の3つだけとする。

- `quality_score`
- all-agent `total_tokens`
- `elapsed_seconds`

次はdiagnosticとして扱い、KPIへ追加しない。

- tool call
- model step
- worker routing
- root／worker別token
- session情報
- context継承
- command内訳

評価基盤は次を出力しない。

- `winner`
- 改善または悪化の断定
- KPIの優先順位
- 採用可否
- release判断
- projection判断

## Compatibility

比較可能な結果は、次の条件が一致するものに限定する。

- evaluation set revision
- target repository ref
- prompt set以外のcomparison conditions
- model
- Agent環境
- TaskSpec
- permission
- fixture
- executor parameter
- case
- iteration
- repetition condition
- token accounting revision

compatibility keyが異なるresultを同一比較へ混ぜない。
単一caseまたは少数反復の結果を、評価範囲外へ一般化しない。
このhostの新規試験はprofileの`max_workers=24`を固定する。readyなslot数が24未満でも設定値をslot数へ合わせて変更せず、実際の同時実行数とprofileへ固定した並列上限を区別する。

上記は履歴prompt-set resultの完全一致条件である。atomic run経路では、prompt以外のEvaluation set、case、fixture、TaskSpec、rating、model、reasoning、Agent/runtime/CLI、permission、executor挙動、token accountingを実効互換条件とする。`N`、coverage、iteration集合、計画順序、`max_workers`はexecution provenanceへ分離し、run poolのmember identityにしない。異なる`max_workers`のrunを同じpoolで再利用する場合も、analysisはexecution stratum別の件数と差分を保持する。

## Model-visible境界

- TaskSpecと適用されるrepository authorityをmodel-visible入力として扱う。
- oracle、grader、expected result、private commandをmodel-invisible情報として分離する。
- model-visibleでない特定commandを、抽象成果条件から推定してquality必須条件へ格上げしない。
- 抽象成果条件は、その成立を判定できる任意の有効な証拠で満たせるものとして扱う。
- tuningに使ったcaseを、同一revisionのheld-out evidenceとして扱わない。

## Immutable history

- 一次結果は、prompt set名に加えてrevisionまたはbundle hashを含むimmutableな`prompt_set_identity`へbindする。可変名やcondition labelだけでresultを登録しない。
- evaluation set、profile、rating contractをrevision単位で固定する。
- resultはwrite-onceの`result_id`とcontent SHA-256で固定し、revisionで上書きしない。
- 結果確認後に評価基準（profileまたは採点rating）を変える場合は、新しいrevisionとして扱う。
- 過去resultを新契約でin-place再採点しない。
- 既存resultのscore、identity、schemaを現在解釈へ上書きしない。
- root-only token resultをall-agentへ補正する場合も、元resultを残して新schema resultをappendする。
- excluded attemptとenvironment failureをprompt qualityへ混ぜない。
- 全session usageが取得できないrunのtokenを推定しない。
