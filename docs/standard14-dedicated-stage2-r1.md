# STD14専用素材の工程2実装・局所検証記録 第1版

2026年10月4日。工程1の全14項目の仕様を、隔離した管理worktreeで専用コードと採点へ実装した。モデル試験は0件。工程3へ固定成果を渡す。評価代替の成立、モデル差の保持、トークン・時間の削減は未認定である。

## 目的・対象・維持条件

必要な成果は、STD14全14件の情報と依存を保つ専用実装、元JSON TaskSpec、14ケースのseed、0〜4点の採点、正常・誤成果の局所検査、双方向対応、配送境界と固定条件の記録である。実装先は `evaluations/targets/standard14-dedicated-control/`、集合は `dedicated14-r1` とした。旧the-caption、compact、Claudeのアーティファクトとターゲット非依存kernelは変更しなかった。

工程1の保存元は読み取り専用で扱った。5成果と当時の索引をバイト一致で引き継ぎ、索引へ本記録の導線だけを追記した。元checkout、以前の実装用worktreeには変更しなかった。以前のworktreeは管理対象ではないためattachが拒否され、指定commit `fcad5e118af0d0ad69f60cc0faa79dae5ef389af` から `standard14-dedicated-stage2` を作成した。

実際の作業設定は `gpt-6.1-sol / medium`。セッションの `turn_context` から必要な設定だけを[環境記録](../evaluations/targets/standard14-dedicated-control/registrations/environment-r1.json)へ射影した。工程1文書の同一チャット前提は変更せず、最新依頼による新チャットでの実施を本記録へ明記する。工程3、モデル試験、push・PR・merge、追加チャット、委譲は未実施。

## 実装と局所証拠

[専用素材の入口](../evaluations/targets/standard14-dedicated-control/README.md)から全成果を参照できる。baseは一つで、展開時には一件のseedだけを適用する。各workspaceへ独立したGitを作り、base、seed、Free配置を固定する。月次は指定seedのdiffを現在HEADの親と区別する配置にした。元TaskSpecのバイト列を保存し、配送時の月次seed SHAだけを置換する。

snapshotの正規化・key生成・日付・JST・hash形式・空拒否と、run.shの全文を保持した。モード解決は旧分岐を原文保持し、実ファイルからsnapshot／live CSVを選択して小さなledgerへ流す。通常callerがmodeを省略する関係も保持する。日付はtimelineから初回・再試行を経て資産別fetchのexclusive endへ渡る。原子的保存は実tempfileとmock replace失敗を使う。Reactは全fundsから列表示を決め、検索後のrows、全cell、空表示のcolSpanへ結ぶ。Nodeのpackageとlockは旧バイト列を保持する。

[局所検証](../evaluations/targets/standard14-dedicated-control/registrations/local-qualification-r1.json)は全14件を展開し、正常参照、期待するseed故障、24種類の独立コード誤成果、143件の操作・criterion証拠を検査した。Pythonの正常baseは44件が成功した。F06のseedでは通常試験の成功だけを回帰復元の証明にせず、欠落を別確認した。正常回帰テストは、空拒否を消した場合とmessageを変えた場合に失敗する。型だけ、assert Trueの誤成果は、その感度喪失として検出する。

[追加48検査](../evaluations/targets/standard14-dedicated-control/registrations/supplemental-qualification-r1.json)では、依存二ファイル、文書二section、legacy説明、周辺routing、禁止path、コマンド未実行・失敗・終了不明を分けた。月次と他入口は設計側で実Pythonを起動した。A02に未提示の特定diffコマンドを追加しない検査も含む。[Node終了証拠](../evaluations/targets/standard14-dedicated-control/registrations/node-qualification-r1.json)には、元のnpm ci、lint、buildの成功を保存した。Reactは5入力と、header／cell片側、trim欠落、rowsによる判定、固定colSpanの誤成果を検査した。

## 採点と対応の限界

[双方向対応](../evaluations/targets/standard14-dedicated-control/registrations/criterion-map-r1.json)は旧42criterionを同じ意味の新検査へ結ぶ。採点器は境界違反を0点、主要成果なしを1点、一部成立を2点、主要成果成立と明示検証不足を3点、全条件成立を4点にする。必須コマンドが開始済みで終了状態だけ取れない場合は品質点へ混ぜず計測失敗にする。有効な0点は再実行で消さない。

A01は本文の質問語や疑問符を使わず、未確定値、単一終了、変更なし、編集・試験未開始から停止状態を導く。回答前test、質問後の回答なしtest、編集後revertを操作証拠で区別する。F05の二つの確認内容をA01へ追加しない。F10月次の数値行、空の確認事項の表記、生成者情報は減点材料にしない。

`runtime/inspect_artifact.py` は最終treeを独立した固定検査へ結ぶ。応答内容とtest差分の意味判定は、保存証拠のhashを持つ独立判定記録を入力する契約とし、実行役の自己申告を入力しない。**この意味判定の実モデル実行への運用接続は未確認である。** 局所の合成証拠で採点分岐が通ることと、保存応答からその証拠を取得できることを同一視しない。全criterionへの対応表は存在するが、全ての実モデル応答を自動採点できることを今回の完了条件として主張しない。

## 配送・固定条件・保存量

[配送境界検査](../evaluations/targets/standard14-dedicated-control/registrations/delivery-audit-r1.json)でroot0 byte、非root3正本の旧原文一致、元TaskSpec一致と月次SHA置換、14件coverageを確認した。設計書・oracle・grader・過去結果は配送treeにもGitにも入れない。これは配送境界の検査であり、ホスト全体の読取りを新しいruntimeで強制した証明ではない。

[固定記録](../evaluations/targets/standard14-dedicated-control/registrations/source-freeze-r1.json)にpath/type/mode/content、caseのGit関係、TaskSpec、authority、採点器、収集器のhashを結ぶ。[保存量](../evaluations/targets/standard14-dedicated-control/registrations/storage-r1.json)は論理量、割当量、行数、case別Git objects、Node依存を分ける。モデル試験中のピークと終了後保持量、実読込み量は未測定。今回の小さい素材からコスト削減率を認定しない。

CLI0.159.0の実体と共有Python3.14.5・依存identityを環境記録へ結んだ。ローカルNode/npmの版とhashも記録したが、旧F04の保存環境と同一であることは未確認である。profileは各推論設定28枠、上限24、一枠一回、24件と4件の順を固定し、全て `execution_enabled=false` とした。

## 工程3へ渡す未確認事項

[発行条件](../evaluations/targets/standard14-dedicated-control/registrations/admission-r1.json)は `ready=false`、モデル発行0件を維持する。工程3は同じ局所試験を無条件にやり直さず、固定diffと対応・局所証拠を読んで、以下を最終確認する。

- 各項目の要求・欠落情報・正本・コード依存・誤成果が、元STD14の判断の難しさを保っているか。テスト件数や点数の一致だけで判定しない。
- 42criterionの新検査に、未提示の要件や意味判定の穴がないか。特にF06の追加test感度、F10両option、A01／F05とA02／F07の情報差を確認する。
- 保存応答とtest差分の独立意味判定を、既存の固定収集・採点経路へ接続できるか。接続できない間は未採点を4点へ補完しない。
- 旧Node/npmとcacheの同一性、固定モデル一覧、CLIの基本・developer・skills・toolsと質問方式、空homeと権限、全担当usage、時間区間、Layer 1とatomic planの照合を完了できるか。

不備を工程3で見つけた場合、モデルスロットを発行せず、該当成果と未達条件を特定する。Low28件の測定成立を確認するまではMedium・Highへ進まない。工程3の確認・測定によって本記録を当時の成功へ遡及改変しない。
