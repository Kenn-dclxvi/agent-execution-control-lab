# Candidate256 発行前判定と調査resultの直接対応

## 結論

Candidate256はCandidate147を直接の基準とし、調査の発行単位を、発行前から固定されている必要な判定へ直接対応づける。Candidate254は成立済みの開始共同発行、相互非依存発行、検証境界を保持するsourceとして使うが、直接の親にはしない。Candidate255の禁止文は継承しない。

Candidate254へ追加する一文は次のとおりとする。

> 調査を発行できる単位は、発行前から固定されている必要な判定を、そのresultだけで確定できるものに限る。

## Candidate作成前の検討gate

| 項目 | 固定内容 |
| --- | --- |
| 意図しない動作 | read範囲ごとに新しい局所的な未確認状態を作り、そのresultを同じ必要判定の続きのreadへ接続する |
| 最短の失敗経路 | 必要判定を固定 → 判定全体を確定できないreadを発行 → 読めた範囲を局所状態として確定 → 残りを別stepで発行 |
| 閉じる辺 | 発行後に作った局所状態から、発行前の必要判定を満たす残りの調査へ向かうdependency |
| 保持する正常経路 | 発行前の必要判定を一回で確定できる任意の許可済み調査と、resultがmissing、unreadable、具体的矛盾等を実際に観測した場合の既存追加調査 |
| 合法なcarrier | 発行前から固定されている必要判定を、そのresultだけで確定できる調査。command、tool、行範囲は固定しない |
| 直接の基準 | Candidate147 `the-caption-3ce91a4-result-effect-scope-r1` |
| 保持するsource | Candidate254の開始共同発行、相互非依存発行、検証境界 |
| counterexample | Candidate254 run `342cf77221a14660908dbb7e6cf6cc27`およびCandidate255の2件。直接の親または継承元にはしない |

## C147との対応

C147の`evidence_consumer_ready`は、`現在欠けている観測値がbind済み`かつ`requested resultがそのstateをbind可能`な場合だけ発行を許す。Candidate254の人間語は「その状態」をread後の小さな状態として解釈できた。Candidate256は、調査の種類を禁止せず、発行前から固定された必要判定とrequested resultの対応だけを戻す。

## 評価gate

固定F04 N=5だけを先に実行する。5 / 5 Score `4`、開始確認と必要readの共同発行5 / 5、相互に影響しない確認の別step化0 / 5、発行前の必要判定を一回で確定できない調査0 / 5、required validationの単一発行判断5 / 5の場合だけ機序成立とする。その後にC147およびCandidate254との総使用token中央値を比較する。

一項目でも不通過なら`mechanism_failed / stopped`とし、追加N、別ケース、Standard14へ進めない。全機序が通ってもtoken中央値がC147未満でなければ`targeted_passed / cost_not_reduced / stopped`とする。

## 変更範囲

- 変更target: root `AGENTS.md`だけ
- 変更範囲: `EVIDENCE_GATE`へ一文追加
- 維持target: 追加一文以外をCandidate254と同一byteで保持
- 非継承: Candidate255の`部分readは発行しない`という禁止文

## 現在状態

F04 N=5は5 / 5件がScore `4`だったが、発行前の必要判定を一回で確定できない調査が5 / 5件、required validationの分割発行が5 / 5件で発生した。「発行単位」という表現は各commandを一単位として逐次化する方向へ作用した。

`f04_n5_completed / quality_passed / mechanism_failed / stopped / standard14_not_started / adoption_not_decided / release_not_created / projection_not_performed`
