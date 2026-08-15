# Candidate238 影響しない結果を前提にしない設計

## 結論

Candidate238はCandidate147を直接の基準とし、Candidate237で成立した人間語、TaskSpec進捗出力の抑制、担当起動境界、観測済み値の再取得境界を保持したまま、開始状態の確認結果を影響しないreadの前提にできる許可だけを閉じる。Candidate229とCandidate230は、待機禁止だけでは逐次発行が残った反例として使い、prompt本文や評価状態を継承しない。Candidate234は同じ未評価案の設計記録として参照するが、そのbundleを親にしない。

## Candidate作成前の検討gate

| 項目 | 固定内容 |
| --- | --- |
| 基準プロンプト | `the-caption-3ce91a4-result-effect-scope-r1`（Candidate147）。Candidate237は現在の人間語と成立済み境界を供給するsourceであり、直接基準ではない |
| 基準状態の最短正常経路 | 開始状態の確認結果が対象、permission、method、stop conditionを変え得る作業だけをその結果へ依存させ、影響しないreadはその結果へ依存させない。変更とrequired commandはdrift時の停止条件を維持する |
| 保存済みの問題経路 | Candidate229 A02の4 / 5件とCandidate230 A02の2 / 5件で、開始状態の結果がreadの対象・permissionを変えず、drift時にもreadが禁止されないのに、開始状態の結果を受け取るまでreadが未発行だった |
| TaskSpec等で防げない理由 | A02のTaskSpecはdrift時にartifact変更とrequired commandを止めるがreadを禁止せず、read対象とpermissionも開始結果では変わらない。Candidate229の待機禁止文も、開始結果をreadの前提として扱う余地を閉じなかった |
| 変更する条件と責務境界 | `DECISION_BOUNDARY`で、結果がreadの対象・permissionを変え得ず、想定外でもread自体を禁止しない場合、その結果をreadの先行条件にできないと固定する。結果受領までreadを未発行にする経路を、その不正な依存関係として禁止する |
| 消える問題経路 | 開始状態の確認結果をread開始の前提として扱い、結果受領後にreadを別発行する経路 |
| 維持する正常経路 | 開始状態によって禁止されるartifact変更とrequired commandは結果へ依存する。read自体が禁止されるか、その対象またはpermissionが変わり得る場合はreadも結果へ依存できる。Candidate237で成立したF02の各境界も維持する |
| 新しい判断・参照・例外 | 新しいticket、自己判定、tool順、model step、command、wrapperを追加しない。結果がreadの対象・permissionを変えるか、想定外でreadを禁止するかという既存の影響範囲だけを使う |
| 評価 | A02 N=5。5 / 5件Score `4`、開始状態の結果に影響されないreadを結果受領後まで未発行にしたrun 0 / 5件を必須とする。all-agent total token中央値を互換なCandidate147 A02と比較する |
| 停止条件 | 品質または対象機序に一件でも反例があれば停止する。通過してもtoken中央値がCandidate147より増えた場合はA02のコスト差を未解消として止め、別機序を同Candidateへ追加しない |

## C147から復元する境界

追加するのは成功時の発行順ではなく、次の依存関係の制限である。

> 開始状態の確認結果によってreadの対象やpermissionが変わらず、想定外の状態でもread自体は禁止されないなら、その確認結果はreadの先行条件ではない。確認結果を受け取るまでreadを未発行にする経路は、影響しない作業の間に待機依存を作るため許可しない。

この境界は、同じmodel step、特定のtool call数、commandの結合または発行順を要求しない。禁止するのは、結果の値が変えていないreadへ、その結果から待機依存を作ることだけである。

## アーティファクト境界

- prompt identity: `the-caption-3ce91a4-independent-result-prerequisite-exclusion-r1`
- direct baseline: `the-caption-3ce91a4-result-effect-scope-r1`
- retained source: `the-caption-3ce91a4-taskspec-progress-suppression-r1`
- 変更target: root `AGENTS.md`だけ
- 維持target: ほかの18 targetをCandidate237と同一byteで保持
- Candidate229、Candidate230: 保存反例だけを使用
- Candidate234: 未評価設計の重複確認だけに使用し、bundleは継承しない

## 現在状態

`design_fixed / candidate_created / a02_n5_completed / quality_passed / mechanism_failed / stopped`

## A02 N=5結果

品質は5 / 5件がScore `4`だったが、開始状態の確認結果に影響されないreadを結果受領後まで未発行にした経路が5 / 5件に残った。all-agent total token中央値は`183,521`で、Candidate229比`-59.76%`、Candidate147比`+42.17%`だった。機序不通過のため追加NとStandard14へ進まない。
