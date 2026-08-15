# Candidate255 不完全な部分readの発行除外

## 結論

Candidate255はCandidate147を直接の基準とし、Candidate254で残った一回では観測値を確定できない部分readの発行permissionを、人間語の一文だけで閉じる。Candidate254は成立済み境界を保持するsourceとして使うが、直接の親にはしない。

追加する一文は次のとおりとする。

> 一回の調査resultだけで現在欠けている観測値を確定できない部分readは発行しない。

## Candidate作成前の検討gate

| 項目 | 固定内容 |
| --- | --- |
| 意図しない動作 | 必要な観測値を一回で確定できない部分readを発行し、その不足resultを続きのreadの発行条件にする |
| 最短の失敗経路 | 一つの連続範囲を部分read → 不足result受領 → 同じ観測値の残りを別stepでread |
| 閉じる辺 | 不完全であることが発行時から分かる部分readのresultから、同じ観測値の続きの発行へ向かうdependency |
| 保持する正常経路 | 発行時には十分と判断できたresultが実際には不完全、利用不能、矛盾だった場合の既存追加調査 |
| 合法なcarrier | 一回のresultで観測値を確定できる任意の許可済み調査。command、tool、範囲は固定しない |
| 直接の基準 | Candidate147 `the-caption-3ce91a4-result-effect-scope-r1` |
| 保持するsource | Candidate254の開始共同発行、一般的な相互非依存発行、検証境界 |
| counterexample | Candidate254 run `342cf77221a14660908dbb7e6cf6cc27`。直接の親または継承元にはしない |

## 評価gate

固定F04 N=5だけを先に実行する。5 / 5 Score `4`、開始確認と必要readの共同発行5 / 5、相互に影響しない確認の別step化0 / 5、一回では観測値を確定できない部分read 0 / 5、required validationの単一発行判断5 / 5の場合だけ機序成立とする。その後にC147との総使用token中央値を比較する。

一項目でも不通過なら`mechanism_failed / stopped`とし、追加N、別ケース、Standard14へ進めない。全機序が通ってもtoken中央値がC147未満でなければ`targeted_passed / cost_not_reduced / stopped`とする。

## 変更範囲

- 変更target: root `AGENTS.md`だけ
- 変更範囲: `EVIDENCE_GATE`へ一文追加
- 維持target: 追加一文以外をCandidate254と同一byteで保持

## 現在状態

F04 N=5は5 / 5件がScore `4`だったが、開始確認と必要readの共同発行、影響しない複数確認の同一model step発行、不完全な部分readの除外はいずれも3 / 5件、required validationの単一発行判断は4 / 5件だった。追加文は対象permissionを閉じず、2件で開始確認後の逐次的な部分readを増やした。

`f04_n5_completed / quality_passed / mechanism_failed / stopped / standard14_not_started / adoption_not_decided / release_not_created / projection_not_performed`
