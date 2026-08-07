# evaluations instructions

`evaluations/`の指示は、現行のevaluation foundation v4の境界を扱う。v3以前のprompt-set resultは履歴として保持し、v4へその場で変換しない。ルートの`AGENTS.md`の共通規則に加えて、この領域規則を適用する。評価基盤のレイヤーと境界、および世代（`v1`〜`v4`）の定義と遷移は`docs/prompt-comparison-workflow.md`、実行方法は`docs/evaluation-loop-manual.md`を正本とする。

## READMEと索引の責務

- `evaluations/README.md`は評価領域の入口とアーティファクト配置だけを示す。CLI手順、レイヤー詳細、互換条件を複製せず、対応する正本へ委譲する。
- 配下READMEはアーティファクトの現在の索引と所在を示す。ケース、プロファイル、rating contract、result本体の識別子、score、statusをREADME側へ移さない。
- READMEへ数値や状態を要約する場合も一次アーティファクトへの導線を付け、要約を正本として扱わない。
- 過去の形成経緯や個別Candidateの判断は、必要な導線を残してケース / プロファイル索引からresultまたは`docs/`の研究記録へ委譲する。

## ターゲットインスタンス

計測系列は評価対象リポジトリごとのインスタンスとして別管理する。インスタンスの登録、layout、境界の正本は`evaluations/targets/README.md`とする。

- ターゲット非依存のkernel（`scripts/`のfixture固定と4 Layer実行、`layer2/`）へ、ターゲット固有のパス、case ID、分岐を追加しない。
- ターゲット固有の採点補助はインスタンス側のモジュールとして分け、既存インスタンスのモジュールを新インスタンスの都合で変更しない。
- 既存インスタンス `the-caption`のアーティファクトのパス（`evaluations/cases`、`evaluations/profiles`、`evaluations/sets`、`evaluations/rating-contracts`、`evaluations/results`、`prompts/`配下）を移動しない。
- 新インスタンスのアーティファクトは`evaluations/targets/<target_id>/`配下へ閉じる。
- 別インスタンスのresultを同一比較へ入れない。rating contractがインスタンス単位である以上、`quality_score`の絶対値をインスタンス間で比較しない。
- インスタンスのディスクリプタは参照とターゲット固有の識別子だけを持ち、gate command、bundle target map、resultの実体を複製しない。

## ケースアーティファクト

`evaluations/cases/`は`the-caption`の`legacy_root`ケースアーティファクトを保持する。ケース追加・revision更新は次を守る。

- 1ケースが基盤へ渡す固定点はcase ID、開始リポジトリのfixture、アダプタへ渡すopaque payloadとする。TaskSpec、model-visible入力、期待成果などの可変フィールドはpayloadへ閉じ、kernelが意味解釈しない境界を維持する。
- oracle、grader、expected result、private commandはmodel-invisibleに保ち、model-visibleなTaskSpecやrepository authorityへ漏らさない。
- case revision、fixture identity、seed / reference behaviorを固定し、既存revisionを結果確認後にその場で変更しない。
- ケース追加の根拠は、既存セットで見えない実測失敗、または評価対象の制御が既存ケースで観測不能であることとする。family番号を埋めることや同じcontrol pathの反復数を増やすことだけを追加理由にしない。
- チューニングに使用したケースを同一revisionのheld-out evidenceとして扱わない。
- `evaluations/cases/README.md`はケース設計規則や採点規則の正本にせず、`the-caption` legacy-rootのケース索引、variation、現在状態、関連セット / resultへの導線に限定する。

## プロファイルアーティファクト

`evaluations/profiles/`は`the-caption`の`legacy_root` execution profileを保持する。

- 実行前にmodel、reasoning、Agent/runtime/CLI、permission、environment、実行ポリシー、対象セット / ケース、rating contract、repetition、停止条件を固定する。結果確認後に条件を変える場合は新しいprofile revisionとする。
- 実行順はexecution provenanceとして保存するが、プロンプトセット間のKPI補正には使わない。実測のトークンと経過時間を環境補正して比較値へ変換しない。
- candidate固有のquality / mechanism gateでは対象プロンプトだけを先に実行する。gate前に比較相手の再実行を必須化しない。
- 比較resultが必要になった時点で保存済み互換resultを優先し、不足スロットだけを新規のdispatchへ固定する。既存runを習慣的に再実行しない。
- `evaluations/profiles/README.md`はprofile identity、用途、条件要約、対応resultへの導線を示す索引とする。score、KPI、停止判断の正本はresult本体または対応する研究記録とし、READMEの要約を判定根拠へ格上げしない。
- `evaluations/profiles/`直下の全profile JSONは、ファイル名を知らなくても`evaluations/profiles/README.md`から到達できるよう、README本体またはREADMEが直接リンクする`evaluations/profiles/index/*.md`で少なくとも1回は直接リンクする。索引シャードはプロファイル名と所在だけを持ち、評価史を複製しない。
- プロファイル索引を変更した場合は、ディレクトリ直下の全profile JSONがREADMEまたはREADME直結のシャードから被参照であること、READMEが全シャードを参照すること、profile JSONとシャードのリンクに実体不存在がないことを機械確認する。
- プロファイルを追加・削除した変更では、索引シャードとREADMEの導線を`scripts/generate_profile_index.py --write`で再生成する。シャードを手書きで部分更新せず、生成物と手元の状態が一致することを同スクリプトの引数なし実行で確認する。

## 4 Layer

評価は次の4 Layerに限定する。

1. Evaluation set
2. Execution
3. Quality rating
4. KPI comparison

各Layerは自分の出力だけを作る。

- 前段のアーティファクトを変更しない。
- 後段の判断責務へ越境しない。
- プロンプト作成、改善提案、採用、release、本体反映を評価基盤へ持ち込まない。

## 3 KPI

評価基盤が扱うKPIは次の3つだけとする。

- `quality_score`
- all-agent `total_tokens`
- `elapsed_seconds`

次は診断情報として扱い、KPIへ追加しない。

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

## 互換条件

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
単一ケースまたは少数反復の結果を、評価範囲外へ一般化しない。
このホストの新規試験はプロファイルの`max_workers`をqualification済み上限`24`へ固定する。readyなスロット数が24未満でも設定値をスロット数へ合わせて変更せず、実際の同時実行数とプロファイルへ固定した並列上限を区別する。

上記は履歴のprompt-set resultの完全一致条件である。atomic run経路では、プロンプト以外のEvaluation set、ケース、fixture、TaskSpec、rating、model、reasoning、Agent/runtime/CLI、permission、executor挙動、token accountingを実効互換条件とする。`N`、coverage、iteration集合、計画順序、`max_workers`はexecution provenanceへ分離し、run poolのmember identityにしない。異なる`max_workers`のrunを同じプールで再利用する場合も、分析はexecution stratum別の件数と差分を保持する。

## 比較試験の実行前ゲート

ルートの`AGENTS.md`が定めるゲートの内訳をこの節の正本とする。

- 実行予定条件から、Evaluation set identity、全ケースのfixture identity（path、type、mode、content、symlink targetを含む）、TaskSpec、case revision、rating、model、reasoning、Agent/runtime/CLI、permission、executor parameter、設定上の`M`、`N`とiteration集合を確定し、基準resultの互換条件と機械照合する。atomic run経路で実効互換条件へ含めない項目は`互換条件`の規定に従う。
- プロンプト比較では、事前に宣言したprompt identity以外の互換条件が完全一致することを実行前ゲートとする。完全一致を証明するpreflight receiptを保存してから実行する。
- Layer 4へ登録する試験では、発行予定のケース / iteration集合が固定Layer 1の全case coverageとresult schemaの登録条件を満たすこともpreflightで機械検証する。満たさない試験を非登録の診断として実施する場合は、その状態と再利用不能なゲートを一件目の発行前に明示する。
- 試験ごとにfixture、file mode、ランタイム、設定上の並列上限などの実行環境を最適化しない。保存済み基準resultと比較する場合は、その基準で固定したLayer 1を再利用する。複数条件を新規実行する場合は、一つのLayer 1を先に固定して全条件へ複製する。
- 保存済みprompt-set resultとの履歴互換サイクルは`prepare-comparison-layer1`で基準Layer 1から生成し、capsuleとglobal planの生成後に`preflight-comparison`を通す。比較用Layer 1を`freeze-set`で再生成しない。`comparison-preflight.json`がない、失効した、または改ざんされた旧経路サイクルの`run`は禁止する。
- atomic run経路では、既存resultを`atomic_run_registry.py import-result`でrun単位へ索引化し、`plan-missing`で要求サンプル数との差だけをwrite-onceのdispatch planへ固定する。`prepare_atomic_plan.py`でpool identity、dispatch plan hash、プロンプト、Evaluation set、ケース、fixture、TaskSpec、rating、model、reasoning、Agent/runtime/CLI、permission、executor挙動、設定上の`M`を機械照合してから不足runだけを発行する。既存runを再実行せず、完了・採点後は各runを個別登録する。

## Model-visible境界

- TaskSpecと適用されるrepository authorityをmodel-visible入力として扱う。
- oracle、grader、expected result、private commandをmodel-invisibleな情報として分離する。
- model-visibleでない特定のcommandを、抽象成果条件から推定してquality必須条件へ格上げしない。
- 抽象成果条件は、その成立を判定できる任意の有効な証拠で満たせるものとして扱う。
- チューニングに使ったケースを、同一revisionのheld-out evidenceとして扱わない。

## 不変の履歴

- 一次結果は、prompt set名に加えてrevisionまたはbundle hashを含む不変の`prompt_set_identity`へbindする。可変名やcondition labelだけでresultを登録しない。
- evaluation set、プロファイル、rating contractをrevision単位で固定する。
- resultはwrite-onceの`result_id`とcontent SHA-256で固定し、revisionで上書きしない。
- 結果確認後に評価基準（プロファイルまたは採点rating）を変える場合は、新しいrevisionとして扱う。
- 過去のresultを新契約でその場で再採点しない。
- 既存resultのscore、識別子、schemaを現在解釈へ上書きしない。
- root-only token resultをall-agentへ補正する場合も、元のresultを残して新しいschemaのresultをappendする。
- excluded attemptとenvironment failureをprompt qualityへ混ぜない。
- 全session usageが取得できないrunのトークンを推定しない。

## Result索引

`evaluations/results/README.md`は、このディレクトリへ登録済みのresultを引くための索引とする。

- 索引は要約と所在だけを持つ。数値、score、状態の正本は各result本体とし、正本を索引へ移さない。
- 節は新しい系列から並べ、節内は実行順（古い順）で並べる。節を追加または改称した場合は目次を追従させる。
- 新しいresultは該当する節の末尾へ追記する。ファイル先頭やファイル末尾への場当たり追記をしない。
- 一件のresultにつき一段落とする。要約はresultへのリンク、件数、スコア分布、主要KPI、現在状態に限定する。
- 既存段落を現在解釈へ書き換えない。後続の再解釈は当該段落へ併記文として追加し、当時の記述を残す。
- 節を再編する場合は段落の移動だけを行い、本文を書き換えない。移動後に段落集合が変わっていないことを機械確認する。
- ディレクトリ内の全resultを索引から参照可能にする。要約未作成のresultは専用節へリンクだけ登録し、要約を推測で作らない。
- 索引を変更した場合は、リンク切れ0件と全resultの被参照を機械確認してから完了とする。
