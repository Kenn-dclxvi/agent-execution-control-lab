# Candidate257 必要判定・観測値・resultの発行permission対応

## 結論

Candidate257はCandidate147を直接の基準とし、Candidate254の`EVIDENCE_GATE`冒頭を、未完了の必要判定、欠けている具体的な観測値、その判定を確定できるresultの三者関係へ置き換える。Candidate254は成立済みの開始共同発行、相互非依存発行、検証境界を保持するsourceとして使うが、直接の親にはしない。Candidate255の`部分read`禁止文とCandidate256の`発行単位`制限は継承しない。

置換後の段落は次のとおりとする。

> repository内の調査や証拠取得に発行permissionがあるのは、未完了で状態が`unobserved`の必要判定、その判定に欠けている具体的な観測値、その観測値を返して判定を`satisfied`または`unsatisfied`へ確定できるresultが、発行前に直接対応している場合だけである。いずれかが欠ける調査には発行permissionがない。この境界は、対象探索、変更前後の調査、validation準備、recoveryのすべてに適用する。

## Candidate作成前の検討gate

| 項目 | 固定内容 |
| --- | --- |
| 意図しない動作 | read範囲ごとの局所状態やcommandごとの発行単位を後から作り、同じ必要判定の続きへ接続する |
| 最短の失敗経路 | 必要判定と観測値の対応なしで部分resultを取得 → 部分resultを局所状態へ対応づける → 残りを別stepで発行 |
| 閉じる辺 | 発行前の必要判定・欠けた観測値・判定を確定できるresultの直接対応がない調査へのpermission |
| 保持する正常経路 | 三者が直接対応する任意の許可済み調査、既知の相互非依存調査の同一model step発行、実際のmissing、unreadable、具体的矛盾等を受けた既存追加調査 |
| 合法なcarrier | 必要判定を確定できる観測値を返す任意のresult。command、tool、行範囲、調査順は固定しない |
| 直接の基準 | Candidate147 `the-caption-3ce91a4-result-effect-scope-r1` |
| 保持するsource | Candidate254の開始共同発行、相互非依存発行、検証境界 |
| counterexample | Candidate254の1件、Candidate255の2件、Candidate256の5件。直接の親または継承元にはしない |

## C147との対応

C147の`evidence_consumer_ready`は、必要判定がnonterminalで状態が`unobserved`、欠けた観測値がbind済み、requested resultがそのstateをbind可能という関係全体を、発行permissionの成立条件にしている。Candidate257は個別の調査方法や発行単位を規定せず、この関係全体だけを自然文へ戻す。

## 評価gate

固定F04 N=5だけを先に実行する。5 / 5 Score `4`、開始確認と必要readの共同発行5 / 5、相互に影響しない確認の別step化0 / 5、発行前の必要判定を確定できない調査0 / 5、required validationの単一発行判断5 / 5の場合だけ機序成立とする。その後にC147およびCandidate254との総使用token中央値を比較する。

一項目でも不通過なら`mechanism_failed / stopped`とし、追加N、別ケース、Standard14へ進めない。全機序が通ってもtoken中央値がC147未満でなければ`targeted_passed / cost_not_reduced / stopped`とする。

## 変更範囲

- 変更target: root `AGENTS.md`だけ
- 変更範囲: Candidate254の`EVIDENCE_GATE`冒頭一段落を置換
- 維持target: 置換段落以外をCandidate254と同一byteで保持
- 非継承: Candidate255の`部分read`禁止文、Candidate256の`発行単位`制限

## 現在状態

F04 N=5は5 / 5件がScore `4`だったが、開始共同発行、影響しない確認の同一model step発行、発行permissionの直接対応、検証の単一発行判断はいずれも0 / 5件だった。token中央値`170,598`はCandidate147比`+12.85%`、Candidate254比`+15.43%`である。

`f04_n5_completed / quality_passed / mechanism_failed / stopped / standard14_not_started / adoption_not_decided / release_not_created / projection_not_performed`
