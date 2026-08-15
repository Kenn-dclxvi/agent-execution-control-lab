# Candidate251 開始確認と必要readの共同発行境界

## 結論

Candidate251はCandidate147を直接の基準とし、開始確認resultで禁止されず、対象や許可も変わらない必要readを、開始確認と同じ判断から発行する境界を復元する。Candidate246はF04で成立した検証境界を保持する人間語のsourceとして使うが、直接の親にはしない。Candidate247からCandidate250までは失敗経路だけを反例として使い、本文を引き継がない。

置換する`DECISION_BOUNDARY`は次の二文とする。

> 開始確認の結果で禁止されず、対象や許可も変わらない読み取りは、その確認と同じ判断から発行する。確認後へ分けられるのは、その結果で読み取りが禁止されるか、対象または許可が変わり得る場合だけとする。

これはread command、toolまたはcommand順を指定しない。開始確認resultから影響を受けないreadを未発行へ残せるpermissionと、必要条件のない分離permissionを閉じる。

## Candidate作成前の検討gate

| 項目 | 固定内容 |
| --- | --- |
| 基準プロンプト | `the-caption-3ce91a4-result-effect-scope-r1`（Candidate147）。Candidate246は保持する人間語のsourceであり、prompt parentではない |
| 基準状態の最短正常経路 | 開始確認resultで禁止、対象、許可が変わらない必要readを開始確認と同じ判断から発行し、共同result後に一度だけ次を判断する |
| 保存済み問題経路 | Candidate250 F04の5 / 5件で、最初の判断から開始確認だけを発行し、必要readを次の判断へ残した |
| 基準挙動 | 互換なCandidate147 F04の5 / 5件では、開始確認と必要readを同じmodel stepから発行した |
| 許していた辺 | Candidate250は確認だけの実行を禁じたが、必要readを同じ判断から発行する義務と、分離できる条件を固定しなかった |
| TaskSpec等で防げない理由 | TaskSpecはdrift時にartifact変更とrequired commandを止めるがreadを禁止せず、必要readをどの発行判断へ含めるかを定めない |
| 置換する条件 | Candidate246の`DECISION_BOUNDARY`一文だけを上記二文へ置換する。Candidate246で成立した`VALIDATION_CLOSURE`とその他の人間語をbyte同一で保持する |
| 消える問題経路 | 開始確認resultでreadの対象や許可が変わらないのに、開始確認だけを発行して必要readを次の判断へ残す経路 |
| 判断順を変えた場合 | 先に開始確認を検討しても、影響を受けない必要readは同じ判断の発行集合へ入る。readを分離できるのは明示した二条件だけである |
| 維持する正常経路 | 開始確認resultでreadが禁止される、read対象が変わる、またはpermissionが変わる場合はreadを確認後へ分けられる。Candidate246の検証境界を維持する |
| 情報の所在と経路 | TaskSpecが開始時点の確認、drift時の停止対象、read許可pathを持つ。新しいrepository read、carrier、worker、外部出力は増やさない |
| 新しい判断・参照・例外 | C147にあるread禁止、対象変化、permission変化だけを分離条件に使い、新しい判断材料を増やさない |
| 評価 | F04 N=5。5 / 5件Score `4`、最初の発行判断に開始確認と必要readが共存すること5 / 5件、Candidate246の検証機序維持5 / 5件を必須とする。通過後に保存済みCandidate147と総使用tokenを比較する |
| 停止条件 | 品質、共同発行機序、Candidate246の検証機序に一件でも反例があれば停止する。全機序を通過しても総使用token中央値がCandidate147より多ければ停止する。通過前に別ケース、追加N、Standard14へ進まない |

## アーティファクト境界

- prompt identity: `the-caption-3ce91a4-start-check-joint-issuance-boundary-r1`
- direct baseline: `the-caption-3ce91a4-result-effect-scope-r1`
- retained source: `the-caption-3ce91a4-validation-result-ai-return-exclusion-r1`
- counterexample only: Candidate247、Candidate248、Candidate249、Candidate250
- 変更target: root `AGENTS.md`だけ
- 変更範囲: `DECISION_BOUNDARY`一文を二文へ置換
- 維持target: `DECISION_BOUNDARY`以外の全targetと全文をCandidate246と同一byteで保持

## 現在状態

`f04_n5_completed / quality_passed / joint_issuance_passed_2_of_5 / validation_mechanism_passed_3_of_5 / mechanism_failed / stopped / standard14_not_started / adoption_not_decided / release_not_created / projection_not_performed`
