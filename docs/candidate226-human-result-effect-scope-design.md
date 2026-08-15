# Candidate226 結果影響範囲の人間語翻訳設計

## 結論

Candidate226は、Candidate147 `the-caption-3ce91a4-result-effect-scope-r1`を直接の基準とし、root `AGENTS.md`の「結果の影響範囲」一機能だけを人間語へ翻訳する。ほかの12条項と18 targetはCandidate147から変更しない。

このCandidateは、Candidate225の10節を修正するものではない。Candidate225の保存済みtraceは、一般的な「独立した確認はまとめる」という表現でも、開始状態の結果を許可済みreadの待機条件にする経路が残った反例としてだけ使う。

## 作成前gate

| 項目 | 固定内容 |
| --- | --- |
| 基準prompt | Candidate147 `the-caption-3ce91a4-result-effect-scope-r1` |
| 基準状態の正常経路 | 開始状態が想定と違った場合に禁止される作業だけを待たせ、禁止されていないreadは開始状態の結果から停止効果を受けない。変更と必須commandは、TaskSpecが指定した開始状態の確認が完了するまで始めない |
| 保存済み問題経路 | Candidate225のA02 N=5では5 / 5件で開始状態の確認を一度受け取った後にrepository readを始めた。TaskSpec上、開始状態の不一致は変更と必須commandを禁止するがreadは禁止せず、read targetまたはpermissionも変えないため、この待機依存は不要だった |
| 既存authorityだけでは防げない理由 | A02のTaskSpecは不一致時に禁止する操作を限定しているが、禁止されていないreadを開始状態の結果待ちにしてはならないとは定めない。Candidate225の一般的な集約表現でも、この分割はprompt準拠のまま実行できた |
| 変更する条件 | Candidate147の`DECISION_BOUNDARY`一条項だけを、結果が影響できる後続作業の範囲、無関係な待機・停止・失効の禁止、開始状態による限定停止、禁止されていないreadへの待機依存禁止を表す日本語一条項へ置換する |
| 変更しない条件 | 利用者結果の確定、証拠取得、実装方針、実行者、完了、検証、手段失敗、環境回復の12条項はCandidate147と同一byteで保持する。TaskSpec、case、fixture、rating、runtime、permissionも変更しない |
| 閉じる問題経路 | 開始状態の結果によって要否、対象、permission、methodまたは停止条件が変わらない許可済みreadを、その結果の受領まで待たせる経路 |
| 維持する正常経路 | 開始状態の不一致によってread自体が禁止される場合、またはread targetかpermissionが変わり得る場合は、そのreadを開始状態の確認から分離したままにできる。変更と必須commandに対する既存の停止条件も維持する |
| 新しく増える判断 | 新しい分類、label、ticket、実行順またはtool手段は追加しない。既存の対象、permission、method、停止条件への影響だけを人間語で表す |

## 置換する本文

Candidate147の`DECISION_BOUNDARY`一条項を次へ置換する。

> 結果の影響範囲: 受け取った結果が影響してよいのは、その結果によって対象、許可された操作、実行方法、停止条件のいずれかが変わり得る、これから行う作業だけとする。ある結果を理由に、影響しない作業やタスク全体を待機または停止させず、確定済みの無関係な結果を失効させない。開始時の状態が想定と違う場合に止める作業が指定されているときも、その範囲だけを止める。readが禁止されておらず、その対象やpermissionも変わらないなら、開始時の状態を確認した結果をreadの待機条件にしない。

この文は、C147の成功runで観測したtool順、model step数、wrapperまたはcommand構成を実行手順へ転記しない。閉じるのは、影響範囲外の結果から待機依存を作るpermissionだけである。

## 対象評価

### 第一段階: A02 N=5

- case: `TC-A02-REPOSITORY-RESOLVABLE-V4-ROUTING` r2
- quality: 5 / 5 validかつrateable、5 / 5 Score `4`
- 機序: 各runについて、開始状態の結果がreadの要否、対象、permission、methodまたは停止条件を変え得ないにもかかわらず、その結果をreadの待機条件にした経路が0 / 5
- 停止: 1件でもScore `4`未満、または上記の待機依存を観測した場合は停止し、A01へ進まない

機序は、C147と同じtool順または同じmodel stepになったかでは判定しない。分離があった場合に、その先行結果が後続readの判断を変え得る真正な依存を持っていたかで判定する。

### 第二段階: A01 N=5

A02が通過した場合だけ、変更対象外の対照として実施する。

- case: `TC-A01-LATENT-MODE-POLICY` r2
- quality: 5 / 5 validかつrateable、5 / 5 Score `4`
- 対象外影響: 利用者が決める値を質問する前のrepository read、変更またはtestが0 / 5
- 停止: 1件でもScore `4`未満、または質問前のrepository read、変更、testを観測した場合は停止する

## 比較条件とKPI

- Evaluation set: `the-caption-standard14-r1` r1の同一case revisionと固定Layer 1
- baseline result: Candidate147 Standard14 N=5 `f7baeadc5bd44399ac13cc0e0a8aff48`
- diagnostic counterexample: Candidate225 Standard14 N=5 `89c3babd670c461f8b075e7c9a329248`
- model / reasoning: `gpt-5.6-sol / medium`
- runtime: Codex CLI 0.146.0、Python 3.14.5
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- permission: `workspace-write / never`
- configured M: 24
- token accounting: all-agent v1

Candidateだけを先に発行する。A02とA01の品質、機序、対象外影響が通過した後に限り、保存済み互換resultとのtokenとelapsedの記述的比較を行う。N=5の結果を未評価ケース、安定性、採用、releaseまたはprojectionへ一般化しない。

## 現在状態

`a02_n5_completed / quality_passed / mechanism_failed_4_of_5 / stopped / a01_not_started / adoption_not_decided`

A02は5 / 5件がScore `4`だったが、4 / 5件で開始状態の結果を受け取ってからreadを別に発行した。事前停止条件に従い、A01は発行しない。結果は[`candidate226-human-result-effect-scope-a02-n5_2026-08-14.md`](../evaluations/results/candidate226-human-result-effect-scope-a02-n5_2026-08-14.md)を正本とする。
