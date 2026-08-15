# Candidate253 開始確認と必要readの同一model step発行境界

## 結論

Candidate253はCandidate147を直接の基準とし、Candidate252で「同じ判断」とした発行時点をC147の機能語`同一model step`へ戻す。停止条件が変更や必須コマンドだけを禁じ、readを禁じない場合は、開始確認と必要readを同一model stepから発行する。Candidate246はF04で成立した検証境界を保持する人間語のsourceとして使うが、直接の親にはしない。Candidate252は失敗経路だけを反例として使う。

置換する`DECISION_BOUNDARY`は次の二文とする。

> 開始確認の停止条件が変更や必須コマンドだけを禁じ、読み取りを禁じていない場合は、開始確認と必要な読み取りを同一model stepから発行する。読み取りを別stepへ置けるのは、停止条件が読み取りも禁じるか、確認結果で読み取りの対象または許可が変わり得る場合だけとする。

command、toolまたはcommand順は指定しない。`同一model step`は成功runの手順ではなく、開始確認resultをAIが受け取る前に必要readを発行済みにするpermission境界として使う。

## Candidate作成前の検討gate

| 項目 | 固定内容 |
| --- | --- |
| 基準プロンプト | `the-caption-3ce91a4-result-effect-scope-r1`（Candidate147）。Candidate246は保持する人間語のsourceであり、prompt parentではない |
| 基準状態の最短正常経路 | 停止条件がreadを禁じない場合、開始確認と必要readを同一model stepから発行し、共同result後に一度だけ次を判断する |
| 保存済み問題経路 | Candidate252 F04の4 / 5件で、「同じ判断」と書いても開始確認だけを最初のmodel stepから発行した |
| 基準挙動 | 互換なCandidate147 F04の5 / 5件では、開始確認と必要readを同一model stepから発行した |
| 許していた辺 | 「同じ判断」はmodel stepの境界と対応せず、開始確認resultを受領してからreadを別発行できた |
| TaskSpec等で防げない理由 | TaskSpecはdrift時の停止対象を固定するが、result受領をまたいでよい発行の境界を定めない |
| 置換する条件 | Candidate246の`DECISION_BOUNDARY`一文だけを上記二文へ置換する。Candidate246のその他の本文をbyte同一で保持する |
| 消える問題経路 | 停止条件がreadを禁じないのに、開始確認だけを一つのmodel stepから発行し、result受領後の別stepへ必要readを残す経路 |
| 判断順を変えた場合 | 開始確認を先に検討しても、必要readは同一model stepの発行集合へ入り、result受領後の別stepへ残せない |
| 維持する正常経路 | 停止条件がreadも禁じる場合、または確認resultでread対象・permissionが変わり得る場合は別stepへ置ける。Candidate246の検証境界を維持する |
| 情報の所在と経路 | TaskSpecが開始確認、停止対象、read許可pathを持つ。新しいread、carrier、worker、外部出力は増やさない |
| 新しい判断・参照・例外 | 新しい判断材料は増やさず、C147で実証済みのmodel step境界を名称ごと保持する |
| 評価 | F04 N=5。5 / 5件Score `4`、共同発行5 / 5件、Candidate246の検証機序維持5 / 5件を必須とする。通過後にCandidate147と総使用tokenを比較する |
| 停止条件 | 品質または二つの機序に一件でも反例があれば停止する。全機序を通過しても総使用token中央値がCandidate147より多ければ停止する。通過前に別ケース、追加N、Standard14へ進まない |

## アーティファクト境界

- prompt identity: `the-caption-3ce91a4-start-check-same-model-step-r1`
- direct baseline: `the-caption-3ce91a4-result-effect-scope-r1`
- retained source: `the-caption-3ce91a4-validation-result-ai-return-exclusion-r1`
- counterexample only: Candidate252
- 変更target: root `AGENTS.md`だけ
- 変更範囲: `DECISION_BOUNDARY`一文を二文へ置換
- 維持target: `DECISION_BOUNDARY`以外の全targetと全文をCandidate246と同一byteで保持

## 現在状態

`f04_n5_completed / quality_passed / mechanism_passed / targeted_passed / cost_not_reduced / stopped / standard14_not_started / adoption_not_decided / release_not_created / projection_not_performed`
