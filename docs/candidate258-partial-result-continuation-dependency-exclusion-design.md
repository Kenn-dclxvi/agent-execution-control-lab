# Candidate258 途中resultから残りのreadへの依存関係除外

## 結論

Candidate258はCandidate147を直接の基準とし、Candidate254の開始共同発行、相互非依存発行、検証境界をsourceとして保持する。Candidate254で残った一件だけを対象に、同じ判定に必要な情報の一部だけを返すresultから残りのreadへ向かう依存関係を`DECISION_BOUNDARY`で閉じる。Candidate255からCandidate257までの`EVIDENCE_GATE`変更は継承しない。

追加する一文は次のとおりとする。

> 同じ判定に必要な情報の一部だけを返す結果から、残りの情報を取得する読み取りの開始、待機、停止への依存関係を作ってはいけない。

## Candidate作成前の検討gate

| 項目 | 固定内容 |
| --- | --- |
| 意図しない動作 | 一つの判定に必要なreadを途中で区切り、必要情報がまだないという途中resultを残りのreadの開始条件にする |
| 最短の失敗経路 | 必要な情報の一部だけをread → result受領 → 同じ判定の残りを別stepでread |
| 閉じる辺 | 同じ判定の途中resultから、残りのreadの開始、待機、停止へ向かうdependency |
| 保持する正常経路 | 完結したresult、実際のmissing・unreadable・具体的矛盾を受けた既存追加調査、開始共同発行、相互非依存発行、検証の単一発行判断 |
| 合法なcarrier | 同じ判定に必要な情報を一部resultへ分割しない任意のreadまたは検索。command、tool、行範囲は固定しない |
| 直接の基準 | Candidate147 `the-caption-3ce91a4-result-effect-scope-r1` |
| 保持するsource | Candidate254の開始共同発行、相互非依存発行、検証境界 |
| counterexample | Candidate254 run `342cf77221a14660908dbb7e6cf6cc27`。Candidate254を直接の親とせず、Candidate255～257も継承しない |

## C147との対応

C147は、受領resultが次の対象、permission、method、stop conditionを変える範囲だけを依存先とする。Candidate258は、同じ判定の必要情報を意図的に分けた途中resultを、新しい依存元として作れる経路だけを閉じる。成功runのread方法や範囲は実行義務へ変換しない。

## 評価gate

固定F04 N=5だけを先に実行する。5 / 5 Score `4`、開始確認と必要readの共同発行5 / 5、相互に影響しない確認の別step化0 / 5、同じ判定の途中resultから残りのreadへ依存したrun 0 / 5、required validationの単一発行判断5 / 5の場合だけ機序成立とする。その後にCandidate147およびCandidate254との総使用token中央値を比較する。

一項目でも不通過なら`mechanism_failed / stopped`とし、追加N、別ケース、Standard14へ進めない。全機序が通ってもtoken中央値がCandidate147未満でなければ`targeted_passed / cost_not_reduced / stopped`とする。

## 変更範囲

- 変更target: root `AGENTS.md`だけ
- 変更範囲: Candidate254の`DECISION_BOUNDARY`へ一文追加
- 維持target: 追加一文以外をCandidate254と同一byteで保持
- 非継承: Candidate255、Candidate256、Candidate257の`EVIDENCE_GATE`変更

## 現在状態

F04 N=5は5 / 5件がScore `4`で、開始共同発行と検証境界は5 / 5件だった。しかし途中resultから残りのreadへの依存関係が1 / 5件残り、Candidate254と同じ4 / 5で機序不成立だった。token中央値`186,450`はCandidate147比`+23.34%`、Candidate254比`+26.15%`である。

`f04_n5_completed / quality_passed / mechanism_failed / stopped / standard14_not_started / adoption_not_decided / release_not_created / projection_not_performed`
