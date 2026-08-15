# Candidate259 同一artifactの二度目の追加read除外

## 結論

Candidate259はCandidate147を直接の基準とし、Candidate254の開始共同発行、相互非依存発行、検証境界をsourceとして保持する。Candidate254とCandidate258で各一件ずつ残った経路だけを対象に、同じ変更方針を決めるための同一artifactの追加readを一度に限定し、正常なresultの後に二度目の追加readへ進めるpermissionを閉じる。Candidate255からCandidate258まではcounterexampleとして使い、本文は継承しない。

追加する一文は次のとおりとする。

> 同じ変更方針を決めるために同じartifactを読み足せるのは一度だけであり、そのresultがmissingまたはunreadableでない限り、さらに同じartifactを読み足すpermissionはない。

## Candidate作成前の検討gate

| 項目 | 固定内容 |
| --- | --- |
| 必要な成果 | F04の要求を満たす`App.tsx`の限定変更と、固定済み検証の完了 |
| 直接の基準 | Candidate147 `the-caption-3ce91a4-result-effect-scope-r1` |
| 基準状態の最短正常経路 | 開始確認と必要readを共同発行し、同一artifactを一度だけ読み足して変更方針を確定し、変更後の固定済み検証を一つの発行境界から完了する |
| 保存済み誤経路 | Candidate254 run `342cf77221a14660908dbb7e6cf6cc27`とCandidate258 run `cecace75ac6744e1879cc6c610f8abed`で、初回read後に同じ`App.tsx`を二度に分けて追加readした |
| 既存境界で防げない理由 | Candidate254の相互非依存境界とCandidate258の途中result依存除外は、同じartifactの各部分を別の必要情報と分類する余地を残し、正常な一度目の追加read後も二度目のpermissionを閉じなかった |
| 閉じる辺 | 同じ変更方針に対する正常な一度目の同一artifact追加read resultから、二度目の同一artifact追加readへ向かうpermission |
| 保持する正常経路 | 初回read、任意の一度の追加readまたは検索、`missing`または`unreadable`からの回復、開始共同発行、相互非依存発行、検証の単一発行判断 |
| 合法なcarrier | 同じartifactの必要箇所を一度の追加readまたは検索で観測できる任意の手段。command、tool、行範囲は固定しない |
| 変更するpredicate | `DECISION_BOUNDARY`の同一変更方針・同一artifact・追加read回数に対するpermissionだけ |
| 新たに増える判断 | artifact identity、同じ変更方針への帰属、一度目のresultが`missing`または`unreadable`か |
| 品質維持 | 固定F04 N=5でScore `4`を5 / 5件維持する |
| 逆結果の停止条件 | 二度目の同一artifact追加readが一件でも残る、既存境界のいずれかが不通過、または品質が一件でもScore `4`未満なら停止する |

## 保存traceでの境界

Candidate254とCandidate258の全10件を、変更前に`App.tsx`を読むinvocation数で再集計した。成功8件は初回readと一度の追加readの計2回であり、失敗2件だけが初回readと二度の追加readの計3回だった。この差はread方法や行範囲ではなく、同じartifactに対して二度目の追加readを開始できるpermissionの有無で表せる。

## C147との対応

C147は追加evidenceを具体的な欠落、読取不能、矛盾または充足不能へ限定し、一件だけ許可する。Candidate259はその境界を同じ変更方針とartifact identityへ対応づけ、正常なresultごとに別の追加evidenceとして数え直せる経路を閉じる。成功runの検索語、read範囲、command順は実行義務へ変換しない。

## 評価gate

固定F04 N=5だけを先に実行する。5 / 5 Score `4`、開始確認と必要readの共同発行5 / 5、相互に影響しない確認の別step化0 / 5、正常な一度目の追加read後に同じartifactを二度目に追加readしたrun 0 / 5、required validationの単一発行判断5 / 5の場合だけ機序成立とする。その後にCandidate147およびCandidate254との総使用token中央値を比較する。

一項目でも不通過なら`mechanism_failed / stopped`とし、追加N、別ケース、Standard14へ進めない。全機序が通ってもtoken中央値がCandidate147未満でなければ`targeted_passed / cost_not_reduced / stopped`とする。

## 変更範囲

- 変更target: root `AGENTS.md`だけ
- 変更範囲: Candidate254の`DECISION_BOUNDARY`へ一文追加
- 維持target: 追加一文以外をCandidate254と同一byteで保持
- 非継承: Candidate255、Candidate256、Candidate257、Candidate258の追加文

## 現在状態

F04 N=5は5 / 5件がScore `4`で、開始共同発行、相互非依存発行、同一artifactの二度目の追加read除外、検証境界がすべて5 / 5件で成立した。token中央値`145,917`はCandidate147比`-3.47%`、Candidate254比`-1.27%`である。

`f04_n5_completed / quality_passed / mechanism_passed / cost_reduced / targeted_gate_passed / standard14_not_started / adoption_not_decided / release_not_created / projection_not_performed`
