# Candidate237 TaskSpec進捗出力抑制設計

## 結論

Candidate237はCandidate147を直接の基準とし、TaskSpecを固定した事実と固定内容を利用者向けの進捗へ出力できる許可だけを閉じる。これは利用者が明示した変更後の動作であり、保存traceから推測したものではない。Candidate236は「固定が完了した事実は伝えられる」として、この境界を閉じ切らなかった反例としてだけ使う。成功したrunのcommand構成、tool順、custom exec wrapperの書き方は指示へ転記しない。

## Candidate作成前の検討gate

| 項目 | 固定内容 |
| --- | --- |
| 基準プロンプト | `the-caption-3ce91a4-result-effect-scope-r1`（Candidate147）。Candidate235は保持する人間語と再取得境界のsource、Candidate236は出力境界の反例であり、どちらもprompt parentではない |
| 基準の最短正常経路 | TaskSpecを利用者へ報告せず内部で固定し、必要な証拠だけを受け取り、一つの実装方針へ固定して変更し、固定済みの検証を完了して最終結果を返す |
| 保存反例 | Candidate236は`SPEC`で内部項目の項目別出力を禁止した一方、「固定が完了した事実は伝えられる」と明示した。このため、TaskSpec固定そのものを進捗結果へ変換する経路がprompt準拠で残った |
| 利用者が決めた結果 | TaskSpecを固定した事実も固定内容も利用者向け進捗へ出力しない。利用者が決める必要のある成果の値の確認、permission拒否による停止、完了したoperationの最終結果は、それぞれ必要な結果として返す |
| TaskSpec等で防げない理由 | TaskSpec、repository authority、repository stateは内部で固定する値を与えるが、その固定自体を利用者向け進捗へ複製できるかを制限しない。Candidate236は固定完了の出力を明示的に許している |
| 変更する条件 | Candidate235の`SPEC`へ、TaskSpecへの固定と固定項目は内部状態であり、固定した事実と内容を利用者向け進捗へ出力できない境界を追加する。既存の確認結果、拒否結果、最終結果の出力は維持する |
| 消える問題経路 | 「TaskSpecを固定した」「仕様を固定した」等の固定完了報告、およびpredicate、owner、permission、constraint等の固定内容を、利用者が求める成果でないまま進捗として再生成する経路 |
| 維持する正常経路 | TaskSpecは全項目を内部で固定する。未確定のrequired outcome valueだけを質問し、permission拒否と未完了結果を必要な範囲で報告し、完了時はterminal resultを返す。F02の許可済みread、変更、検証も維持する |
| 変更しないもの | 開始identityとの同時発行、変更方法、validation、wait、custom exec wrapper、commandのまとめ方、worker packet、担当起動条件、観測済み値の再取得境界、TaskSpec以外について必要な利用者向け説明 |
| 新しい判断・例外 | 新しい調査判断、tool発行条件、実行順は増やさない。出力時にTaskSpec固定を進捗結果へ変換するpermissionだけを削除する |
| 評価 | F02 N=5。5 / 5 Score `4`、最初の進捗でTaskSpecまたは仕様を固定した事実の報告0 / 5、TaskSpec内部値の列挙0 / 5、担当名起動0 / 5、観測済み値の再取得0 / 5を必須とする。all-agent total token中央値を互換なCandidate147、Candidate231、Candidate233、Candidate235、Candidate236と比較する |
| 停止条件 | 品質、対象の出力機序、保持する担当起動境界または観測済み値境界に一件でも反例があれば停止する。すべて通過してもtoken中央値がCandidate235より減らなければ停止する。nonterminal validation waitは補正しない |

## 責務境界

- TaskSpecの固定は、実行を制御する内部処理として残す。
- TaskSpecを固定した事実と固定内容は、利用者向け進捗結果へ変換しない。
- required outcome valueの確認、permission拒否による停止、terminal resultは、それぞれの結果として利用者へ返す。
- TaskSpec以外の必要な説明まで一括で禁止せず、今回の出力境界だけを局所的に閉じる。

## 現在状態

`design_fixed / candidate_created / f02_n5_completed / quality_passed / mechanism_passed / cost_reduced / targeted_passed`

## F02 N=5結果

品質は5 / 5 Score `4`、TaskSpec固定の事実または内容の進捗出力、判断責任者名からのworker起動、観測済み値の再取得はすべて0 / 5件だった。all-agent total token中央値は`128,940`で、Candidate235比`-24.92%`、Candidate147比`+0.55%`だった。1件のrequired validation再実行による`219,052` tokensは補正せず公式値へ含めた。
