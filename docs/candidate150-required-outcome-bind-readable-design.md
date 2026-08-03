# Candidate150 必須成果全体のimplementation bind設計

## 結論

Candidate150はCandidate149を直接親とし、必須成果全体を一つのimplementation choiceへbindしてから変更する境界だけを一文で追加する。

## 作成前gate

1. Candidate149のA01 / A02各N=5は10 / 10 score 4で、A01 tool 0 / 5、A02 canonical成果5 / 5だった。
2. Candidate143はF02 / F04 / F07各N=100を300 / 300 score 4で通過した。
3. Candidate143の成立軸は、TaskSpec上の全change effectとartifact間relationを一つのimplementation choiceへbindすることである。
4. 今回はこの一軸だけを追加し、証拠取得、検証closure、委譲、result待機は追加しない。

## 固定する追加文

```text
- IMPLEMENTATION / CHANGE: artifact変更は、targetと適用中repository instruction、およびTaskSpecが要求する全change effectとartifact間relationが、観測済みcurrent content上で実行可能な変更predicateと保持constraintを持つ一つのimplementation choiceへbind済みの場合だけ開始し、部分成果だけがbind済み、残るeffectが未観測、または複数targetの関係が未固定なら変更を開始しない。
```

## Targeted mechanism gate

A01 / A02は親Candidate149の保存済み各N=5を継承し、F02、F04、F07 dependencyを各N=5、Rating v14、Medium、M=24で確認する。

- A01は5 / 5で変更・testなしに未固定値だけを質問する。
- A02は5 / 5で質問せずcanonical成果へ到達する。
- F02、F04、F07 dependencyは15 / 15 score 4で、TaskSpec上の全effectとrelationを満たす。
- 部分変更、無変更停止、required validation欠落が一件でもあれば停止する。

このgateではStandard14を実行しない。

## Targeted結果

2026-08-03にF02 / F04 / F07 dependency各N=5を実施し、15 / 15件がscore 4だった。F02は5 / 5件で二つのsource effectを接続し、F04は5 / 5件で必要変更と既存relationを両立し、F07は5 / 5件でdependency pairを揃えた。部分変更、無変更停止、required validation欠落は0件だったため、quality・mechanism gateを通過した。詳細は[`targeted結果`](../evaluations/results/candidate150-free-required-outcome-bind-readable-v14-medium-f02-f04-f07-atomic-n5-cli0146_2026-08-03.md)を正本とする。

現在状態は`targeted_f02_f04_f07_n5_evaluated / quality_gate_passed / required_outcome_bind_mechanism_passed / result_registered / standard14_not_run`である。
