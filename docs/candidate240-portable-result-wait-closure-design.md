# Candidate240 結果待機境界の環境非依存再構成

## 結論

Candidate240はCandidate147を直接の基準とし、Candidate239で落とした結果待機の発行境界を、実行環境に依存しない自然な日本語で復元する。Candidate237は変更対象外の人間語とF02境界を保持するsource、Candidate239は待機依存を5 / 5件残した反例としてだけ使い、いずれも直接の親にはしない。

置換する境界は次の四文とする。

> ある結果によって対象、許可、方法、停止条件が変わらない作業は、その結果が返るまで保留してはならない。結果を待つ間に保留できるのは、その結果によって判断が変わり得る作業だけとし、影響しない作業の結果がすべてそろうまでは、それらの一部の結果を次の作業の選択や停止に使わない。
>
> 開始状態の確認が変更や必須実行だけを止め、読み取りを禁止しない場合、その確認を理由に読み取りを保留してはならない。確認によって読み取り自体が禁止されるか、その対象または許可が変わり得る場合だけ、読み取りを確認後へ分ける。

これは成功runのtool順を転記するものではない。先行結果を受け取るまで影響しない作業を未着手にできる許可、一部の結果を使って残りの発行を選び直せる許可、および開始確認の停止効果を許可済みreadへ広げられる依存関係を閉じる。

## Candidate作成前の検討gate

| 項目 | 固定内容 |
| --- | --- |
| 基準プロンプト | `the-caption-3ce91a4-result-effect-scope-r1`（Candidate147）。Candidate237は保持する本文のsource、Candidate239は反例であり、直接の親ではない |
| 基準状態の最短正常経路 | 先行結果が対象、許可、方法、停止条件を変えない作業は、その結果を判断へ使う前に着手済みとなる。開始確認が変更と必須実行だけを止める場合は、許可済みreadを待機対象にせず、必要な結果がそろってから変更可否を判断する |
| 保存済み問題経路 | Candidate239 A02の5 / 5件で、モデルは「まずcheckoutを確認し、その後run.shを読む」と宣言し、開始確認のterminal resultを受け取るまで許可済みreadを未発行にした |
| 問題経路の影響 | 変更前のmodel往復が一段増え、開始確認とreadの間に待機依存が生じた。Candidate239のtoken中央値はC147比`+24.69%`だった |
| TaskSpec等で防げない理由 | A02のTaskSpecはdrift時にartifact変更とrequired commandを禁止するがreadを禁止しない。readの対象とpermissionも開始結果では変わらないため、TaskSpecとrepository authorityだけではreadを後へ保留する逐次経路を違反にできない |
| 置換する条件 | Candidate237の`DECISION_BOUNDARY`にある環境依存の共同発行説明を、上記四文の保留permission、部分result消費禁止、開始確認の局所停止およびread分離例外へ置換する |
| 分離できない理由 | 一般的な保留禁止だけではCandidate239のように開始確認をreadの先行工程と再解釈できる。開始確認の局所停止とread分離例外だけでは、別の非依存作業で一部resultを消費して残りを保留できる。四境界は同じ待機依存を閉じる一構造である |
| 消える問題経路 | 開始結果を受け取るまでreadを未発行にする経路、一部resultを受け取ってから残りの作業を選択・停止する経路、開始確認の停止効果を許可済みreadへ広げる経路 |
| 維持する正常経路 | 開始確認の結果がread自体を禁止する場合、またはread対象・permissionを変え得る場合はreadを確認後へ分ける。共同結果がそろうまではartifact変更とrequired commandを保留する。Candidate237で成立したF02境界と他の12制御群を維持する |
| 新しい判断・参照・例外 | 新しいlabel、tool、runtime、worker判断は増やさない。例外はC147と同じく、確認結果がread自体を禁止するか、read対象またはpermissionを変え得る場合だけ |
| 評価 | A02 N=5。5 / 5件Score `4`、開始確認のresult受領後まで許可済みreadを未発行にしたrun 0 / 5件、部分resultを使った残りreadの選択0 / 5件を必須とする。all-agent total token中央値を互換なCandidate147、Candidate238、Candidate239と比較する |
| 停止条件 | 品質または対象機序に一件でも反例があれば停止する。機序を通過してもtoken中央値がCandidate147より増えた場合はA02のコスト差を未解消として停止する。通過前に別ケース、追加N、Standard14へ進まない |

## アーティファクト境界

- prompt identity: `the-caption-3ce91a4-portable-result-wait-closure-r1`
- direct baseline: `the-caption-3ce91a4-result-effect-scope-r1`
- retained source: `the-caption-3ce91a4-taskspec-progress-suppression-r1`
- counterexample: `the-caption-3ce91a4-plain-result-dependency-boundary-r1`
- 変更target: root `AGENTS.md`だけ
- 維持target: ほかの18 targetをCandidate237と同一byteで保持

## 評価結果

A02 N=5は5 / 5件がScore `4`だったが、開始確認の結果を待ってから許可済みreadを別発行した経路と、その結果を残るreadの選択へ使った経路がともに5 / 5件に残った。token中央値は`193,418`でCandidate147比`+49.84%`、Candidate239比`+20.17%`だった。

## 現在状態

`a02_n5_completed / quality_passed / wait_closure_failed_5_of_5 / partial_result_barrier_failed_5_of_5 / mechanism_failed / stopped / next_case_not_started / standard14_not_started / adoption_not_decided / release_not_created / projection_not_performed`
