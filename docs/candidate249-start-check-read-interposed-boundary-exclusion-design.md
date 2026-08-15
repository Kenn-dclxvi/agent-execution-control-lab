# Candidate249 開始確認と必要readの間の境界許可の閉鎖

## 結論

Candidate249はCandidate147を直接の基準とし、開始状態の確認と、その確認resultによって禁止、対象、許可が変わらないreadとの間に、完了、待機、result受領の境界を置けるpermissionを閉じる。Candidate246はF04で成立した検証境界を保持する人間語のsourceとして使うが、直接の親にはしない。Candidate247とCandidate248は失敗経路だけを反例として使い、本文を引き継がない。

置換する`DECISION_BOUNDARY`は次の一文とする。

> 開始状態の確認と、それによって禁止、対象、許可が変わらない読み取りの間に、完了、待機、結果受領の境界を置いてはならない。

これはread command、tool、同時実行方法または成功runの発行順を指定しない。開始確認と必要readの間へ、read着手前に制御を戻せる境界を挟むpermissionだけを閉じる。

## Candidate作成前の検討gate

| 項目 | 固定内容 |
| --- | --- |
| 基準プロンプト | `the-caption-3ce91a4-result-effect-scope-r1`（Candidate147）。Candidate246は保持する人間語のsourceであり、prompt parentではない |
| 基準状態の最短正常経路 | 開始確認resultによって禁止、対象、許可が変わらない必要readとの間に完了、待機、result受領を挟まず、共同result後に一度だけ次を判断する |
| 保存済み問題経路 | Candidate248 F04の5 / 5件で、開始確認のresultを受け取る境界を必要readの前に置き、その後に必要readを別発行した |
| 基準挙動 | 互換なCandidate147 F04の5 / 5件では、開始確認と必要readの間にresult受領境界を置かなかった |
| 許していた辺 | Candidate248はreadを別作業として後へ残すことを禁じたが、開始確認の完了、待機、result受領をread着手前へ挟めるpermissionを直接閉じなかった |
| TaskSpec等で防げない理由 | TaskSpecはdrift時にartifact変更とrequired commandを止めるがreadを禁止せず、開始確認と必要readの間に結果境界を置いてよいかを定めない |
| 置換する条件 | Candidate246の`DECISION_BOUNDARY`一文だけを上記一文へ置換する。Candidate246で成立した`VALIDATION_CLOSURE`とその他の人間語をbyte同一で保持する |
| 消える問題経路 | 開始確認を完了または待機し、そのresultを受け取ってから必要readを別発行する経路 |
| 判断順を変えた場合 | 禁止、対象、許可が開始resultで変わらない限り、開始確認を先に判断しても必要readとの間へ完了、待機、result受領境界は置けない |
| 維持する正常経路 | driftがreadを禁止する、read対象を変える、またはpermissionを変える場合は境界を置ける。不要なreadを要求しない。Candidate246の検証境界を維持する |
| 情報の所在と経路 | TaskSpecが開始時点の確認、drift時の停止対象、read許可pathを持つ。新しいrepository read、carrier、worker、外部出力は増やさない |
| 新しい判断・参照・例外 | C147にある禁止、対象、許可の変化だけを使い、新しい判断材料や例外を増やさない |
| 評価 | F04 N=5。5 / 5件Score `4`、開始確認と必要readの間の境界不在5 / 5件、Candidate246の検証機序維持5 / 5件を必須とする。通過後に保存済みCandidate147と総使用tokenを比較する |
| 停止条件 | 品質、開始確認/read機序、Candidate246の検証機序に一件でも反例があれば停止する。全機序を通過しても総使用token中央値がCandidate147より多ければ、残るF04コスト差を未解消として停止する。通過前に別ケース、追加N、Standard14へ進まない |

## アーティファクト境界

- prompt identity: `the-caption-3ce91a4-start-check-read-interposed-boundary-exclusion-r1`
- direct baseline: `the-caption-3ce91a4-result-effect-scope-r1`
- retained source: `the-caption-3ce91a4-validation-result-ai-return-exclusion-r1`
- counterexample only: Candidate247、Candidate248
- 変更target: root `AGENTS.md`だけ
- 変更範囲: `DECISION_BOUNDARY`一文だけ
- 維持target: `DECISION_BOUNDARY`以外の全targetと全文をCandidate246と同一byteで保持

## 現在状態

`f04_n5_completed / quality_passed / start_check_read_mechanism_failed_5_of_5 / validation_mechanism_failed_3_of_5 / mechanism_failed / stopped / standard14_not_started / adoption_not_decided / release_not_created / projection_not_performed`
