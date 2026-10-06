# STD14の開始状態と履歴対応の最終判定 第1版

2026年10月4日。GPT-6 Astra Highによる最終確認を完了した。**契約案の基本的な区分は受け入れるが、開始履歴を保持する条件は修正が必要である。現行素材を低コストな同等代替とは認定しない。** 修正条件を[契約第2版](../evaluations/targets/standard14-dedicated-control/registrations/stage7-start-state-contract-r2.json)に固定した。これは設計の受入であり、新素材の作成・受入や測定許可ではない。

必要な成果は、全14ケースの要求・維持条件・判断材料・難しさを保持する評価代替に向けた、開始状態の対応判定である。既存の工程2作業領域を対象に、元計画・仕様と工程7の保存済み照合を読み、未確認だった直接の親関係だけ証拠を補った。このチャットが一人で判定した。元TaskSpec、42条件、採点、素材、旧新の結果、各N2、Low不再発行、別インスタンス帰属を保持した。[入力と方針](../evaluations/targets/standard14-dedicated-control/registrations/stage7-final-input-binding-r1.json)と[実際の作業設定](../evaluations/targets/standard14-dedicated-control/registrations/stage7-final-work-model-binding-r1.json)を保存した。設定は本チャットの `turn_context` の `gpt-6-astra / high` へ結んでいる。

## 契約案をどこまで受け入れるか

| 判定対象 | 判定 | 根拠と限界 |
|---|---|---|
| 同じ11項目と型を要求し、未宣言項目を拒否すること | 受入 | 構築用情報の片側追加や項目欠落を検出できる。旧側9項目の記録を後から補完しない |
| 正本・実行器の一致、ケース・実行ID・TaskSpec・素材identityの結合 | 必要条件として受入 | 識別子の偽装を避けられる。ただし起動記録同士の一致は、起動前の実HEAD・clean状態の証明ではない |
| 容量値を同値必須から外すこと | 受入 | 素材短縮の診断値なので数値差を固定条件不一致にしない。同じ対象・時点・測り方を固定する必要がある |
| 祖先関係と開始履歴の意味対応 | 修正必要 | 祖先であることだけでは、root本文の消失、空コミット、baseとseedの同一性、branch状態を区別できない |
| 保存済み84組の完全な比較受入 | 不成立を維持 | 旧側全84件の2項目欠落と事前宣言の矛盾がある。新しい診断で過去の発行前ゲートは成立しない |
| 新素材の受入、難しさ、低コストな代替認定 | 証拠不足 | 新しい履歴素材は未作成。保存失敗72件の検出や終了保持量の差は、モデルにとっての難しさを証明しない |

[元の契約案](../evaluations/targets/standard14-dedicated-control/registrations/stage7-start-state-contract-r1.json)は上記の必要条件として有効であり、廃棄しない。ただし、履歴の扱いを未決のまま残す第1版単独を、素材対応の完了条件にはできない。[機械可読判定](../evaluations/targets/standard14-dedicated-control/registrations/stage7-final-verdict-r1.json)に各判断を分けて保存した。

[局所照合実装](../evaluations/targets/standard14-dedicated-control/runtime/stage7_start_state_audit_r1.py)の5検査は、項目・型の拒否と正本の比較を確認するものとして妥当である。`history_correspondence_status=unresolved` と事前clean未認定を残す設計も妥当であり、実装が完全な開始ゲートを検証したとは読まない。全件照合と5検査は再実行していない。

## 履歴差の役割

[既存の84組照合](../evaluations/targets/standard14-dedicated-control/registrations/stage7-start-state-audit-r1.json)では、旧側のseedからFree開始への差分はroot `AGENTS.md` の58行削除で、5980 byteから0 byteになる。専用側の同区間には内容差分がなく、`repository authority` と `repository start` の二つの空コミットがある。

今回の[直接親関係の補足証拠](../evaluations/targets/standard14-dedicated-control/registrations/stage7-history-semantics-evidence-r1.json)では、各ケースのLow1の旧新28作業領域からcommit objectを読み、他5組の保存開始記録が同じobject IDを指すことへ結んだ。旧側のFree開始は全14件でseedの直接の子である。また、SD14-05・06・11・13では旧側のbaseとseedが同一なのに、専用側には空のseedコミットが追加されていた。この4件で旧 `seed^..seed` が示すのは元baseの過去変更であり、ケースの故障注入ではない。祖先関係の真偽だけではこの区別が失われる。

rootの旧本文は全14件で同じSHA-256 `daa311bffd40c36dbc8120cf8f9ecaea6e37cc97e329631130b224f387fd98e5` を持つ。これは現在有効な指示ではなく、開始前に指示を除いたという履歴の材料である。実行開始treeのrootを0 byteに保つことと、過去の本文・削除差分を参照可能に保つことは両立する。

依存宣言ケースの旧Low2・Medium1の保存応答は、cleanな作業領域であってもseed後のroot変更を予定外と解釈し、修復・検証せず停止した旨を述べている。したがって、この差分はモデルが実際に利用した判断材料であり、無関係として空差分に置換することは認めない。一方、同じ履歴を持つ他4件の応答は復元完了を報告している。履歴差が停止の十分条件や唯一の原因であるとはいえない。応答分類は今回の品質再採点ではない。

さらに、[最初の開始確認出力](../evaluations/targets/standard14-dedicated-control/registrations/stage7-start-branch-witness-r1.json)では、同じ依存宣言ケースのLow2で旧側はdetached HEAD、専用側は `main` だった。この一組の観測を全84組のbranch証明には広げないが、root削除だけを唯一の差とする解釈はできない。契約第2版ではbranch状態も評価側で固定する。

これらは、モデルへ「この履歴は許可済み」と教える根拠ではない。元TaskSpecで区別すべき開始状態と履歴の関係を、新しい素材から取り去らないための根拠である。正常な操作順や成功応答を追加することもない。

## 全14ケースの対応判断

全行で、工程3が受け入れたソース・採点の対応と、工程6の42条件の対応を保持する。全84組に共通のroot履歴欠落があるが、その差が各ケースの動作へ与えた因果を全件で認定するわけではない。全体の代替には一件の具体的な判断材料欠落で修正が必要となるため、共通素材の新版で履歴を統一して保持する。

| ケース | 元契約における開始履歴の役割 | 新版で保持する関係 |
|---|---|---|
| SD14-01 重複キー | 編集・必須検証前の予期しないdriftの判別 | 重複検査の故障と、後続のroot削除を分離 |
| SD14-02 履歴日付 | 編集・必須検証前の予期しないdriftの判別 | 日付伝播の故障と、後続のroot削除を分離 |
| SD14-03 原子的保存 | 編集・必須検証前の予期しないdriftの判別 | cleanupの故障と、後続のroot削除を分離 |
| SD14-04 Web監査列 | 編集・Node検証前の予期しないdriftの判別 | 列条件の故障と、後続のroot削除を分離 |
| SD14-05 不足情報確認 | 開始確認と、希望二点の未指定は別の判断 | base＝seed。故障を追加せず、root削除を保持 |
| SD14-06 範囲外配備 | 開始identityと操作権限の境界を区別 | base＝seed。本番設定探索を誘発する説明を追加しない |
| SD14-07 空snapshot回帰 | runner gateの失敗・未コミット変更を判別 | テスト欠落とroot削除を分離。開始許可文を足さない |
| SD14-08 正規runner | runner gateの失敗・未コミット変更を判別 | routing故障とroot削除を分離。周辺維持条件を保持 |
| SD14-09 依存宣言 | seed以外の予期しないdriftが明示され、旧応答がroot変更を利用 | 本文削除と直接親を保持。空差分への置換は不受入 |
| SD14-10 CLI文書 | runner gateと正本・実体の整合を区別 | 文書故障とroot削除を分離。コード実行を追加しない |
| SD14-11 入口一覧 | 調査前の開始確認と、一覧の根拠を区別 | base＝seed。架空のケース変更を示さない |
| SD14-12 月次レビュー | 固定seedの一差分が直接のレビュー対象。HEAD親子関係は開始条件でない | seedの直接親と課題差分が必須。HEADからの距離だけは成果条件ではない |
| SD14-13 潜在モード | identity確認はあるが、新しい停止条件はない | base＝seed。希望値未指定を保持し、他ケースの停止文を足さない |
| SD14-14 正本による起動先 | identity確認と、正本で決まる実装方法を区別 | routing故障とroot削除を分離。正規pathの答えを配送しない |

SD14-12では余分な空コミットだけでレビュー不能にはならない。この点を全ケース共通の禁止理由へ一般化しない。ただし、旧新対応の新版では余分なコミットを除き、seedと開始の関係を旧側とそろえる。必要な固定diffがHEADの直前とは限らないという課題は、一つのFree化コミットを残すだけでも維持できる。

## 次の実装へ渡す結論

[次工程の方針](standard14-dedicated-stage8-material-revision-plan-r1.md)では、コード本文を短くするのではなく、欠落した開始履歴だけを専用の別版へ戻す。rootの旧本文は過去treeに限定し、開始tree・TaskSpec・非root正本・42条件・採点を維持する。許容差、作成する版、必要な局所検査と不合格条件を固定済みである。契約の形式だけをそろえた再測定には進まない。

工程3のコード・採点対応の受入、保存失敗72件の検出、旧新各84件、個別実行領域の終了後論理保持量が約70%少なかった観測は保持する。これらを履歴対応、難しさ、APFS専有物理量、開始時の総容量、実行中ピークの証明へ昇格させない。過去の事前ゲートの欠陥は、新版が局所検査を通っても解消した扱いにしない。

追加のモデル試験、N拡張、Low再発行、新worktree、代理担当、別チャット作成、外部実行器変更、commit・push・PR・mergeは0件。今回の成果は新しい判定・設計契約・証拠と索引である。[出力確認](../evaluations/targets/standard14-dedicated-control/registrations/stage7-final-output-verification-r1.json)に保存した。
