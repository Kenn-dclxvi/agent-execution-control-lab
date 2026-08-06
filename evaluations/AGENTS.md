# evaluations instructions

`evaluations/`の指示は、現行のevaluation foundation v4の境界を扱う。v3以前のprompt-set resultは履歴として保持し、v4へin-place変換しない。root `AGENTS.md`の共通規則に加えて、この領域規則を適用する。評価基盤のLayerと境界、および世代（`v1`〜`v4`）の定義と遷移は`docs/prompt-comparison-workflow.md`、実行方法は`docs/evaluation-loop-manual.md`を正本とする。

## READMEと索引の責務

- `evaluations/README.md`は評価領域の入口とartifact配置だけを示す。CLI手順、Layer詳細、compatibility条件を複製せず、対応する正本へ委譲する。
- 配下READMEはartifactの現在の索引と所在を示す。case、profile、rating contract、result本体のidentity、score、statusをREADME側へ移さない。
- READMEへ数値や状態を要約する場合も一次artifactへの導線を付け、要約を正本として扱わない。
- 過去の形成経緯や個別Candidateの判断は、必要な導線を残してcase / profile索引からresultまたは`docs/`の研究記録へ委譲する。

## Target instance

計測系列は評価対象repositoryごとのinstanceとして別管理する。instanceの登録、layout、境界の正本は`evaluations/targets/README.md`とする。

- target非依存のkernel（`scripts/`のfixture固定と4 Layer実行、`layer2/`）へ、target固有のpath、case ID、分岐を追加しない。
- target固有の採点補助はinstance側のmoduleとして分け、既存instanceのmoduleを新instanceの都合で変更しない。
- 既存instance `the-caption`のartifact path（`evaluations/cases`、`evaluations/profiles`、`evaluations/sets`、`evaluations/rating-contracts`、`evaluations/results`、`prompts/`配下）を移動しない。
- 新instanceのartifactは`evaluations/targets/<target_id>/`配下へ閉じる。
- 別instanceのresultを同一比較へ入れない。rating contractがinstance単位である以上、`quality_score`の絶対値をinstance間で比較しない。
- instanceのdescriptorは参照とtarget固有identityだけを持ち、gate command、bundle target map、resultの実体を複製しない。

## Case artifact

`evaluations/cases/`は`the-caption`の`legacy_root` case artifactを保持する。case追加・revision更新は次を守る。

- 1 caseが基盤へ渡す固定点はcase ID、開始repository fixture、adapterへ渡すopaque payloadとする。TaskSpec、model-visible入力、期待成果などの可変fieldはpayloadへ閉じ、kernelが意味解釈しない境界を維持する。
- oracle、grader、expected result、private commandはmodel-invisibleに保ち、model-visible TaskSpecやrepository authorityへ漏らさない。
- case revision、fixture identity、seed / reference behaviorを固定し、既存revisionを結果確認後にin-place変更しない。
- case追加の根拠は、既存setで見えない実測失敗、または評価対象controlが既存caseで観測不能であることとする。family番号を埋めることや同じcontrol pathの反復数を増やすことだけを追加理由にしない。
- tuningに使用したcaseを同一revisionのheld-out evidenceとして扱わない。
- `evaluations/cases/README.md`はcase設計規則や採点規則の正本にせず、`the-caption` legacy-rootのcase索引、variation、現在状態、関連set / resultへの導線に限定する。

## Profile artifact

`evaluations/profiles/`は`the-caption`の`legacy_root` execution profileを保持する。

- 実行前にmodel、reasoning、Agent/runtime/CLI、permission、environment、実行policy、対象set / case、rating contract、repetition、停止条件を固定する。結果確認後に条件を変える場合は新しいprofile revisionとする。
- 実行順はexecution provenanceとして保存するが、prompt set間のKPI補正には使わない。実測tokenとelapsedを環境補正して比較値へ変換しない。
- candidate固有のquality / mechanism gateでは対象promptだけを先に実行する。gate前に比較相手の再実行を必須化しない。
- 比較resultが必要になった時点で保存済み互換resultを優先し、不足slotだけを新規dispatchへ固定する。既存runを習慣的に再実行しない。
- `evaluations/profiles/README.md`はprofile identity、用途、条件要約、対応resultへの導線を示す索引とする。score、KPI、停止判断の正本はresult本体または対応する研究記録とし、READMEの要約を判定根拠へ格上げしない。
- `evaluations/profiles/`直下の全profile JSONは、file名を知らなくても`evaluations/profiles/README.md`から到達できるよう、README本体またはREADMEが直接linkする`evaluations/profiles/index/*.md`で少なくとも1回は直接linkする。索引shardはprofile名と所在だけを持ち、評価史を複製しない。
- profile索引を変更した場合は、directory直下の全profile JSONがREADMEまたはREADME直結shardから被参照であること、READMEが全shardを参照すること、profile JSONとshardのlinkに実体不存在がないことを機械確認する。
- profileを追加・削除した変更では、index shardとREADMEの導線を`scripts/generate_profile_index.py --write`で再生成する。shardを手書きで部分更新せず、生成物と手元の状態が一致することを同scriptの引数なし実行で確認する。

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

## Result索引

`evaluations/results/README.md`は、このdirectoryへ登録済みのresultを引くための索引とする。

- 索引は要約と所在だけを持つ。数値、score、状態の正本は各result本体とし、正本を索引へ移さない。
- 節は新しい系列から並べ、節内は実行順（古い順）で並べる。節を追加または改称した場合は目次を追従させる。
- 新しいresultは該当する節の末尾へ追記する。file先頭やfile末尾への場当たり追記をしない。
- 一件のresultにつき一段落とする。要約はresultへのlink、件数、score分布、主要KPI、現在状態に限定する。
- 既存段落を現在解釈へ書き換えない。後続の再解釈は当該段落へ併記文として追加し、当時の記述を残す。
- 節を再編する場合は段落の移動だけを行い、本文を書き換えない。移動後に段落集合が変わっていないことを機械確認する。
- directory内の全resultを索引から参照可能にする。要約未作成のresultは専用節へlinkだけ登録し、要約を推測で作らない。
- 索引を変更した場合は、link切れ0件と全resultの被参照を機械確認してから完了とする。
