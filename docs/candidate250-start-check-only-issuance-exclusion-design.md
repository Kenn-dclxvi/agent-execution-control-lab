# Candidate250 開始確認だけを実行対象に選べる許可の閉鎖

## 結論

Candidate250はCandidate147を直接の基準とし、開始状態の確認で対象や許可が変わらない、成果に必要な読み取りがあるときに、開始確認だけを実行対象へ選べるpermissionを閉じる。Candidate246はF04で成立した検証境界を保持する人間語のsourceとして使うが、直接の親にはしない。Candidate247からCandidate249までは失敗経路だけを反例として使い、本文を引き継がない。

置換する`DECISION_BOUNDARY`は次の一文とする。

> 開始状態の確認で対象や許可が変わらない、成果に必要な読み取りがある場合、確認だけを実行に移すことはできない。

これはread command、tool、同時実行方法または成功runの発行順を指定しない。必要readを発行せず、開始確認だけを最初の実行対象として選べるpermissionを閉じる。

## Candidate作成前の検討gate

| 項目 | 固定内容 |
| --- | --- |
| 基準プロンプト | `the-caption-3ce91a4-result-effect-scope-r1`（Candidate147）。Candidate246は保持する人間語のsourceであり、prompt parentではない |
| 基準状態の最短正常経路 | 開始確認resultで対象や許可が変わらない必要readを未発行のまま残さず、両方のresultがそろった後に一度だけ次を判断する |
| 保存済み問題経路 | Candidate247からCandidate249までのF04全15件で、最初の実行対象に開始確認だけを選び、必要readを未発行のまま残した |
| 基準挙動 | 互換なCandidate147 F04の5 / 5件では、開始確認だけを最初の実行対象に選ばなかった |
| 許していた辺 | 従来文は結果返却、作業分離、途中境界を禁じたが、それらより前に開始確認だけを実行対象へ選べるpermissionを直接閉じなかった |
| TaskSpec等で防げない理由 | TaskSpecはdrift時にartifact変更とrequired commandを止めるがreadを禁止せず、最初の実行対象へ必要readも含めるかを定めない |
| 置換する条件 | Candidate246の`DECISION_BOUNDARY`一文だけを上記一文へ置換する。Candidate246で成立した`VALIDATION_CLOSURE`とその他の人間語をbyte同一で保持する |
| 消える問題経路 | 必要readを未発行のまま、開始確認だけを最初の実行対象へ選ぶ経路 |
| 判断順を変えた場合 | 開始確認を先に検討しても、対象や許可が変わらない成果に必要なreadがあれば、確認だけを実行対象にはできない |
| 維持する正常経路 | 開始確認でread対象またはpermissionが変わる場合は、確認だけを実行対象にできる。不要なreadを要求しない。Candidate246の検証境界を維持する |
| 情報の所在と経路 | TaskSpecが開始時点の確認、drift時の停止対象、read許可pathを持つ。新しいrepository read、carrier、worker、外部出力は増やさない |
| 新しい判断・参照・例外 | C147にある対象または許可の変化と、成果に必要なreadだけを使い、新しい判断材料や例外を増やさない |
| 評価 | F04 N=5。5 / 5件Score `4`、最初の発行境界に開始確認と必要readが共存すること5 / 5件、Candidate246の検証機序維持5 / 5件を必須とする。通過後に保存済みCandidate147と総使用tokenを比較する |
| 停止条件 | 品質、開始確認/read機序、Candidate246の検証機序に一件でも反例があれば停止する。全機序を通過しても総使用token中央値がCandidate147より多ければ、残るF04コスト差を未解消として停止する。通過前に別ケース、追加N、Standard14へ進まない |

## アーティファクト境界

- prompt identity: `the-caption-3ce91a4-start-check-only-issuance-exclusion-r1`
- direct baseline: `the-caption-3ce91a4-result-effect-scope-r1`
- retained source: `the-caption-3ce91a4-validation-result-ai-return-exclusion-r1`
- counterexample only: Candidate247、Candidate248、Candidate249
- 変更target: root `AGENTS.md`だけ
- 変更範囲: `DECISION_BOUNDARY`一文だけ
- 維持target: `DECISION_BOUNDARY`以外の全targetと全文をCandidate246と同一byteで保持

## 現在状態

`f04_n5_completed / quality_passed / start_check_only_issuance_failed_5_of_5 / validation_mechanism_failed_1_of_5 / mechanism_failed / stopped / standard14_not_started / adoption_not_decided / release_not_created / projection_not_performed`
