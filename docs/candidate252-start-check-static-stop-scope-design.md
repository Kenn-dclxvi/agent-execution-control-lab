# Candidate252 停止条件から決める開始確認と必要readの共同発行境界

## 結論

Candidate252はCandidate147を直接の基準とし、開始確認の実際のresultではなく、実行前に固定された停止条件からreadを待たせられるかを決める。停止条件が変更や必須コマンドだけを禁じ、readを禁じない場合は、開始確認と必要readを同じ判断から発行する。Candidate246はF04で成立した検証境界を保持する人間語のsourceとして使うが、直接の親にはしない。Candidate251は失敗経路だけを反例として使い、本文を引き継がない。

置換する`DECISION_BOUNDARY`は次の二文とする。

> 開始確認の停止条件が変更や必須コマンドだけを禁じ、読み取りを禁じていない場合は、開始確認と必要な読み取りを同じ判断から発行する。読み取りを確認後へ分けられるのは、停止条件が読み取りも禁じるか、確認結果で読み取りの対象または許可が変わり得る場合だけとする。

これはread command、toolまたはcommand順を指定しない。開始確認のresultを見るまでread可否を保留できるpermissionを閉じ、実行前に固定済みの停止条件を発行集合へ適用する。

## Candidate作成前の検討gate

| 項目 | 固定内容 |
| --- | --- |
| 基準プロンプト | `the-caption-3ce91a4-result-effect-scope-r1`（Candidate147）。Candidate246は保持する人間語のsourceであり、prompt parentではない |
| 基準状態の最短正常経路 | 停止条件がreadを禁じないことを実行前に確定し、開始確認と必要readを同じ判断から発行する。共同result後に一度だけ次を判断する |
| 保存済み問題経路 | Candidate251 F04の失敗3件は、開始確認に問題がなければ次にreadするという条件を作り、必要readを未発行へ残した |
| 基準挙動 | 互換なCandidate147 F04の5 / 5件では、drift時の停止条件がreadを禁じないことから、開始確認と必要readを同じmodel stepで発行した |
| 許していた辺 | Candidate251の「結果で禁止されず」はread可否をresult受領後まで未確定にできた。固定済み停止条件から先にread可否を決める拘束がなかった |
| TaskSpec等で防げない理由 | TaskSpecはdrift時に変更とrequired commandを禁止すると明示するが、その静的な停止範囲を最初の発行集合へどう反映するかは定めない |
| 置換する条件 | Candidate246の`DECISION_BOUNDARY`一文だけを上記二文へ置換する。Candidate246で成立した`VALIDATION_CLOSURE`とその他の人間語をbyte同一で保持する |
| 消える問題経路 | 停止条件がreadを禁じないのに、実際の開始確認resultを待ってread可否を判断し、必要readを次の判断へ残す経路 |
| 判断順を変えた場合 | 開始確認を先に検討しても、固定済み停止条件がreadを禁じないため、必要readは同じ判断の発行集合へ入る |
| 維持する正常経路 | 停止条件がreadも禁じる場合、または確認resultでread対象・permissionが変わり得る場合はreadを確認後へ分けられる。Candidate246の検証境界を維持する |
| 情報の所在と経路 | TaskSpecが開始確認、drift時の停止対象、read許可pathを実行前入力として持つ。新しいrepository read、carrier、worker、外部出力は増やさない |
| 新しい判断・参照・例外 | C147にある固定済み停止条件、read対象変化、permission変化だけを使い、新しい判断材料を増やさない |
| 評価 | F04 N=5。5 / 5件Score `4`、最初の発行判断に開始確認と必要readが共存すること5 / 5件、Candidate246の検証機序維持5 / 5件を必須とする。通過後に保存済みCandidate147と総使用tokenを比較する |
| 停止条件 | 品質、共同発行機序、Candidate246の検証機序に一件でも反例があれば停止する。全機序を通過しても総使用token中央値がCandidate147より多ければ停止する。通過前に別ケース、追加N、Standard14へ進まない |

## アーティファクト境界

- prompt identity: `the-caption-3ce91a4-start-check-static-stop-scope-r1`
- direct baseline: `the-caption-3ce91a4-result-effect-scope-r1`
- retained source: `the-caption-3ce91a4-validation-result-ai-return-exclusion-r1`
- counterexample only: Candidate251
- 変更target: root `AGENTS.md`だけ
- 変更範囲: `DECISION_BOUNDARY`一文を二文へ置換
- 維持target: `DECISION_BOUNDARY`以外の全targetと全文をCandidate246と同一byteで保持

## 現在状態

`f04_n5_completed / quality_passed / joint_issuance_passed_1_of_5 / validation_mechanism_passed_5_of_5 / mechanism_failed / stopped / standard14_not_started / adoption_not_decided / release_not_created / projection_not_performed`
