# Candidate242 開始確認だけを先に完了する許可の閉鎖

## 結論

Candidate242はCandidate147を直接の基準とし、開始状態の確認だけを先に完了できる許可を一文で閉じる。Candidate237は変更対象外の人間語を保持するsource、Candidate241は対象機序が2 / 5件にとどまった反例としてだけ使い、いずれも直接の親にはしない。

置換する境界は次の一文とする。

> 開始状態の確認によって読み取りが禁止されず、その対象や許可も変わらない場合、開始状態の確認だけを先に完了してはならない。

これはreadを先に行うか、確認と一緒に始めるかを指定する実行手順ではない。Candidate241の失敗3件で成立した「開始確認だけを完了し、そのresultを使ってからreadを選ぶ」経路の許可だけを削除する。

## Candidate作成前の検討gate

| 項目 | 固定内容 |
| --- | --- |
| 基準プロンプト | `the-caption-3ce91a4-result-effect-scope-r1`（Candidate147）。Candidate237は保持する本文のsource、Candidate241は反例であり直接の親ではない |
| 基準状態の最短正常経路 | 開始確認がreadを禁止せず、その対象や許可も変えない場合、開始確認だけを先に完了しない。影響を受けるartifact変更と必須実行は確認結果まで始めない |
| 保存済み問題経路 | Candidate241 A02のiteration 1、4、5で、開始確認だけを完了し、cleanな開始状態を説明した後に`run.sh`とcanonical entrypointを読んだ |
| 問題経路の影響 | 3件で開始確認resultをreadの選択より前に消費し、許可済みreadとの間に不要な判断往復が残った。対象機序は2 / 5件にとどまった |
| 許していた記述 | Candidate241は開始時点で影響しない作業を未着手にしないよう求めたが、モデルがreadをまだ作業として選んでいない場合に、開始確認だけを先に完了することを直接禁止していなかった |
| TaskSpec等で防げない理由 | A02のTaskSpecはdrift時にartifact変更とrequired commandを禁止するがreadを禁止しない。read対象とpermissionも変わらないが、開始確認だけを先に完了してよいかはTaskSpecとrepository authorityだけでは制限されない |
| 置換する条件 | Candidate237の`DECISION_BOUNDARY`にある環境依存の共同発行説明を上記一文へ置換する。Candidate241の着手範囲列挙、結果利用禁止、例外再記述は引き継がない |
| 消える問題経路 | 開始確認だけを先にterminalにし、そのresultを説明または判断へ使った後で、影響しない許可済みreadを新たに選ぶ経路 |
| 判断順を変えた場合 | readをまだ選んでいないという内部解釈でも、条件に該当する開始確認だけを先に完了する行為自体が禁止される。readを先に行う経路と、開始確認とreadを一つの判断で選ぶ経路はどちらも残る |
| 維持する正常経路 | 確認結果がread自体を禁止する場合、read対象またはpermissionを変え得る場合はこの禁止を適用しない。結果によって禁止され得るartifact変更とrequired commandは、既存の影響範囲規則により結果受領まで保留できる |
| 情報の所在と経路 | TaskSpecが開始確認の停止条件とread permissionを持ち、repository authorityがread対象を定める。rootは既存入力と各resultを直接受け取る。新しいcarrier、worker、外部出力は増やさない |
| 新しい判断・参照・例外 | 新しいlabel、実行手段、runtime、worker判断は増やさない。条件は開始確認がreadを禁止するか、対象または許可を変え得るかだけで、C147の既存影響範囲と同じ入力から判断できる |
| 評価 | A02 N=5。5 / 5件Score `4`、開始確認だけを先に完了したrun 0 / 5件を必須とする。all-agent total token中央値を互換なCandidate147、Candidate239、Candidate240、Candidate241と比較する |
| 停止条件 | 品質または対象機序に一件でも反例があれば停止する。機序を通過してもtoken中央値がCandidate147より増えた場合はA02のコスト差を未解消として停止する。通過前に別ケース、追加N、Standard14へ進まない |

## アーティファクト境界

- prompt identity: `the-caption-3ce91a4-start-check-only-completion-exclusion-r1`
- direct baseline: `the-caption-3ce91a4-result-effect-scope-r1`
- retained source: `the-caption-3ce91a4-taskspec-progress-suppression-r1`
- counterexample: `the-caption-3ce91a4-result-issuance-frontier-r1`
- 変更target: root `AGENTS.md`だけ
- 維持target: ほかの18 targetをCandidate237と同一byteで保持

## 現在状態

`design_gate_fixed / candidate_created / profile_created / a02_n5_completed / quality_passed / mechanism_failed / stopped / next_case_not_started / standard14_not_started / adoption_not_decided / release_not_created / projection_not_performed`
