# Candidate143 required outcome implementation bind設計

## 結論

Candidate143はCandidate118を直接親とし、変更前evidence operationをterminalにする`implementation_bound`の意味だけを置換する。

一つのartifactに対する実行可能な変更predicateが分かっただけではterminalにしない。TaskSpecがrequired outcomeに明示した全change effectとartifact間relationを、観測済みcurrent content上で一つのimplementation choiceとしてbindできた時点だけterminalにする。

C122以降のone-wave、single-target continuation、effect-state再判定、joint-owner gateは継承しない。

## Identity

- candidate number: Candidate143
- prompt identity: `the-caption-3ce91a4-required-outcome-implementation-bind-r1`
- direct parent: `the-caption-3ce91a4-implementation-bind-terminal-closure-r1`（Candidate118）
- changed target: root `AGENTS.md`
- changed predicate: `implementation_bound`
- evaluation status: `targeted_f02_f04_f07_n100_evaluated / quality_gate_passed / targeted_stability_gate_passed / required_outcome_implementation_bind_stable_on_targeted_cases / standard14_n5_evaluated / c125_cost_both_higher / result_registered / adoption_not_decided`

## 作成前gate

1. 基準prompt setはCandidate118とする。
2. C118 F02 N=5は5 / 5 score `4`で、変更前evidence invocationは2〜8回だった。一回で全targetを返すことは正常経路の必須条件ではない。
3. C141のF02低Scoreはupdater effectが未観測でもengine変更へ進んだ。C142はその変更を停止へ置き換えたが、正常進行を回復しなかった。
4. C122はone-wave terminal closureとC125のsingle-target continuationを継承すると、複数editable targetのF02は初回取得後にrelation不足を補えない。
5. C118のterminal条件は`target artifact / instruction / 実行可能な変更predicate / 保持constraint`であり、required outcomeが複数artifact間relationを求める場合の全体bindを明示していない。
6. 置換する一軸は、artifact-localな変更可能性をoperation terminalとする選択肢を消し、required outcome全体のimplementation bindをterminalにすることである。
7. C118のoutcome / implementation分離、evidence default deny、追加evidence admission、validation closure、recoveryは変更しない。
8. F02 / F04 / F07各N=5で成果品質と対象外経路の維持を確認する。
9. score `3`以下、F02の一source部分変更または無変更停止、F04の必要変更欠落、F07 pair欠落が一件でもあれば停止する。

## 置換する境界

```text
implementation_bound :=
  TaskSpecがrequired outcomeに明示した
  全change effectとartifact間relationが、
  admission済みcurrent content上で
  実行可能な変更predicateと保持constraintを持つ
  一つのimplementation choiceへbind済み
```

`implementation_bound=true`のresultだけを変更前evidence operationのterminal resultにする。

この境界は次を導入しない。

- evidence取得回数の上限または下限
- exact target setの一括取得
- file全体、行数、bytes、output配送の制御
- effect別の`satisfied / unsatisfied / unobserved`状態
- single-targetまたはjoint-owner分類
- 追加のstopまたはrework手順

## 汎用性

境界はfile数やcase名ではなく、TaskSpecがrequired outcomeとして明示したchange effectとartifact間relationに依存する。applicationからdomainへの引数伝播、schemaとreader、configとconsumer、APIとadapter、dependency declarationとlock provenanceに同じ境界を適用できる。

TaskSpecがartifact間relationを要求しない単一target taskでは、C118の最短正常経路を変えない。

## 初回評価gate

初回はF02 / F04 / F07各N=5、M=24とする。

| gate | 期待 |
| --- | ---: |
| valid / rateable | 15 / 15 |
| score `4` | 15 / 15 |
| score `3`以下 | 0 |
| F02変更前にC1 / C2の実装方法bind | 5 / 5 |
| F02両sourceの必要変更 | 5 / 5 |
| F02部分変更 / false stop | 0 / 5 |
| F04必要変更と既存contract保持 | 5 / 5 |
| F07 dependency pair完備 | 5 / 5 |

全gate通過時だけ、追加試験を別判断する。

## 初回評価結果

[`F02 / F04 / F07各N=5`](../evaluations/results/candidate143-required-outcome-implementation-bind-v14-medium-f02-f04-f07-atomic-n5-cli0146_2026-08-02.md)は15 / 15がscore `4`だった。

F02は5 / 5でengineとupdaterを変更した。一source部分変更と無変更停止は0 / 5だった。初回に広い検索結果を受け取った一件も、focusedな追加readでrequired relationをbindして成功した。

F04は5 / 5で単一targetだけを変更した。F07は5 / 5でdependency pairを揃えた。これにより初回N=5では、required outcome全体をterminal条件にする境界と、caseに応じた単一target / 複数targetの正常経路が両立した。

この初回評価時点では、stability、Standard14、採用、releaseは未判断だった。

## Standard14評価結果

[`Standard14各N=5`](../evaluations/results/candidate125-candidate143-required-outcome-implementation-bind-v14-medium-standard14-atomic-reuse-n5-cli0146_2026-08-02.md)は70 / 70 score `4`だった。初回F02 / F04 / F07の15 runを再利用し、残り55 runだけを新規発行した。

同一互換条件のCandidate125比はtoken中央値`+24.98%`、elapsed中央値`+17.30%`だった。品質gateは通過したがcostは両方増えた。保存済みCandidate81との差はLayer 1 identityとfixture digestが異なるため参考値に限定する。

## 対象stability評価結果

[`F02 / F04 / F07各N=100`](../evaluations/results/candidate143-required-outcome-implementation-bind-v14-medium-f02-f04-f07-atomic-reuse-n100-cli0146_2026-08-02.md)は、既存各5件を再利用し、不足95件ずつを24、24、24、23件の順で追加した。3 case合計300 / 300件がscore `4`で、score `3`以下、controller error、excluded attemptは0件だった。

これによりCandidate143の追加境界は、直接対象にしたF02の複数editable target、F04の単一target、F07のdependency pairで各N=100のstability gateを通過した。Standard14の残り11 caseは各N=5であり、Standard14全体N=100は未評価である。C125比のcost増加と採用判断も未解決のまま保持する。
