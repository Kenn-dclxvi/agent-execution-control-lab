# Candidate236 TaskSpec出力境界設計

## 結論

Candidate236はCandidate147を直接の基準とし、Candidate235の待機なしF02 traceで確認した、TaskSpecへ固定した内部項目を利用者向け進捗へ項目別に書き出す経路だけを閉じる。TaskSpecの固定責任、F02の正常な調査・変更・検証、Candidate233の担当起動境界、Candidate235の観測済み値再取得境界は維持する。成功したrunのcommand構成やcustom exec wrapperの書き方は指示へ転記しない。

## Candidate作成前の検討gate

| 項目 | 固定内容 |
| --- | --- |
| 基準プロンプト | `the-caption-3ce91a4-result-effect-scope-r1`（Candidate147）。Candidate235は人間語と保存反例のsourceであり、prompt parentではない |
| 基準の最短正常経路 | TaskSpecを内部で固定し、開始identityと許可済み対象を同じmodel stepで確認し、一つの実装方針へ固定して変更し、固定済み実行票を完了して結果を返す |
| 保存反例 | Candidate235の待機なし2件は、最初の利用者向け進捗で実装、required validation、contract確認を別operationとして挙げ、producer、owner、permission、constraint、合格条件を列挙した。C147の待機なし3件の最初の説明は、TaskSpec固定の事実と次に確認する対象だけだった |
| 後続への影響 | 最初の列挙はそのturnの出力を増やし、後続turnの入力contextとして再計上された。Candidate235の待機なし2件は`134,702`と`135,181`、C147の待機なし3件は`125,269`、`127,699`、`128,236`だった |
| 許していた辺 | 人間語の`SPEC`は各operationの固定項目を列挙するが、それらが内部の実行状態であり、それ自体を利用者向け進捗resultにできないことを固定していない。このため、全項目の外部化がprompt準拠で残る |
| TaskSpec等で防げない理由 | TaskSpec、repository authority、repository stateは固定する値を与えるが、rootがその内部値を進捗出力へ複製できるかを制限しない |
| 変更する条件 | `SPEC`へ、TaskSpec固定項目の値は内部の実行状態であり、それ自体を利用者向け進捗resultにしない境界を追加する。固定完了の事実は伝えられる。required outcome valueの確認、permission denial、terminal resultに属する値は各resultとして返せる |
| 消える問題経路 | 実行前に固定したpredicate、criterion owner、permission、constraint、producer等を、利用者が求める結果ではないのに進捗として項目別に再生成する経路 |
| 維持する正常経路 | TaskSpecの全項目を内部で固定する。必要な利用者判断だけを質問し、拒否された操作と未完了結果を報告し、完了時は必要なterminal resultを返す。短い進捗で固定完了の事実を伝えることも妨げない |
| 変更しないもの | F02の許可済みread、開始identityとの同時発行、変更方法、validation、wait、custom exec wrapper、commandのまとめ方、worker packet、担当起動条件、観測済み値の再取得境界 |
| 新しい判断・例外 | 新しい調査判断やtool発行条件は増やさない。既存resultの種類に対応しないTaskSpec内部値は進捗resultとして出力できない、という出力permissionだけを狭める |
| 評価 | F02 N=5。5 / 5 Score `4`、最初の進捗でTaskSpec内部値の項目別列挙0 / 5、担当名起動0 / 5、観測済み値の再取得0 / 5を必須とする。all-agent total token中央値を互換なCandidate147、Candidate231、Candidate233、Candidate235と比較する |
| 停止条件 | 品質、対象機序、保持する担当起動境界または観測済み値境界に一件でも反例があれば停止する。品質と機序を通過してもtoken中央値がCandidate235より減らなければ停止する。nonterminal validation waitは補正しない |

## 責務境界

- TaskSpecの固定はrootまたはbind済みproducerが実行前に行う内部制御である。
- 利用者向け出力は、利用者が決める値の確認、権限拒否による停止、受領済みterminal resultを運ぶ。
- 内部で固定したschema値を、その固定だけを理由に進捗へ複製しない。
- custom exec wrapperの短さやcommandの構成は実装方法であり、このCandidateの成果条件にしない。

## 現在状態

`design_fixed / candidate_created / f02_n5_completed / quality_passed / taskspec_output_gate_passed / retained_reread_gate_failed / mechanism_failed / stopped`

## F02 N=5結果

品質は5 / 5 Score `4`、対象としたTaskSpec内部値の項目別進捗出力は0 / 5件だった。最初の説明は短くなったが、1 / 5件で最初の全文read後に同じ値と行位置を検索し直し、保持条件を失った。token中央値は`180,024`でCandidate235比`+4.82%`、Candidate147比`+40.38%`だった。事前停止条件に従い追加Nへ進めない。
