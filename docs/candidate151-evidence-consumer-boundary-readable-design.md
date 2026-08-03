# Candidate151 evidence consumer boundary可読版設計

## 結論

Candidate151はCandidate150を直接親とし、証拠を「読む工程」ではなく「未完了成果を決めるconsumerの有無」で許可する境界だけを一文で追加する。

## 作成前gate

1. Candidate145は6 case各N=5を30 / 30 score 4で通過し、consumerのないevidence再入を0 / 30件へ閉じた。
2. 同試験はF04のrequiredな変更後source確認を3 / 3件で保持したため、変更後readの一律禁止ではない。
3. Candidate150の開始境界と成果全体bindは保持する。
4. 証拠回数、bytes、target数、span、command形式、validation closure、委譲、result待機は追加しない。

## 固定する追加文

```text
- EVIDENCE / SEARCH: repository evidenceは、未完了required predicateが未観測で、欠けている観測値とrequested resultがその状態を決めるconsumerへbindできる場合だけ取得し、実行方法を探すだけ・確定済み判断の再確認・念のため・報告材料だけの取得は行わず、artifact変更や失敗resultは入力が変わったpredicateだけを未観測へ戻し、consumerがterminalなら未発行evidenceを失効する。
```

## 挙動と既存processの割り当て

| 挙動境界 | 既存processで主に効く場所 |
| --- | --- |
| 未観測のrequired predicateだけをconsumerにする | 調査、実装前確認、変更後静的確認、failure recovery |
| method探索・再確認・念のため・報告用readを閉じる | 調査終了後、実装後、検証準備、完了報告前 |
| 入力が変わったpredicateだけを失効する | 再修正、検証失敗後の回復 |
| terminal consumerの未発行evidenceを失効する | 各工程の終了境界 |

processは発火場所の説明であり、許可authorityではない。許可は各evidence invocationのconsumer状態で決める。

## Targeted mechanism gate

A01 / A02 / F01 / F02 / F04 / F07 dependencyを各N=5、Rating v14、Medium、M=24で確認する。30 / 30 score 4を品質gateとし、A02はcanonical成果5 / 5、成果bind後のconsumerなし再入0 / 5、変更後method探索0 / 5を要求する。F04は必要変更と3 validation完備5 / 5、requiredな変更後source確認を発行した場合はconsumerへbind 100%を要求する。他caseでもrequired evidenceを欠落させない。一件でも崩れたら停止し、Candidate152とStandard14へ進めない。

## Targeted結果

2026-08-03に6 case各N=5を実施し、30 / 30件がscore 4だった。F04でTaskSpec-requiredな変更後source確認を行った2件は、2 / 2件ともchanged effectを直接確認した。一方、A02の2 / 5件はimplementation choiceを確定して変更した後にtest locatorまたはtest symbolを追加検索したため、事前mechanism gateを通過しなかった。

現在状態は`targeted_six_case_n5_evaluated / quality_gate_passed / a02_postchange_method_search_2_of_5 / mechanism_gate_failed / result_registered / stopped`である。Candidate152とStandard14へは進めない。詳細は[`targeted結果`](../evaluations/results/candidate151-free-evidence-consumer-boundary-readable-v14-medium-a01-a02-f01-f02-f04-f07-atomic-n5-cli0146_2026-08-03.md)を正本とする。
