# Candidate145 lifecycle consumer evidence admission設計

## 結論

Candidate145はCandidate144を直接親とし、`EVIDENCE_GATE`を変更前だけのgateから、全lifecycleで未完了のrequired predicateを変えられるevidenceだけを許可するgateへ置換する。

変更前・変更後という時点、read回数、target数、bytes、command順序では制御しない。各evidence invocationについて、結果を受け取る未完了predicate、現在欠けている観測値、そのresultで変わる状態をbindできる場合だけ発行する。

## Identity

- candidate number: Candidate145
- prompt identity: `the-caption-3ce91a4-lifecycle-consumer-evidence-admission-r1`
- direct parent: `the-caption-3ce91a4-required-outcome-validation-method-boundary-r1`（Candidate144）
- changed target: root `AGENTS.md`
- changed axis: lifecycle-wide `evidence_consumer_ready`
- evaluation status: `standard14_n5_evaluated / quality_gate_passed / lifecycle_consumer_mechanism_passed / c125_cost_gate_failed`
- adoption / release / runtime projection: `not_decided / not_created / not_projected`

## 作成前gate

1. Candidate143 A02は5 / 5件がartifact変更後・最初のvalidation前にtest methodを追加探索した。
2. Candidate144は同経路を1 / 5件へ減らしたが、0件には閉じられなかった。qualityは6 case 30 / 30 score `4`だった。
3. Candidate144の再発runは、TaskSpecが既に`shell syntax / 既存test / 最終diff`をvalidation predicateとして明示しているのに、変更後にtest file locator、`tests/AGENTS.md`、test symbolを追加取得した。未固定だったのは実行methodであり、required predicateではない。
4. Candidate121でも同じA02経路が1 / 5件発生した。C121の`evidence_request_ready`は変更前evidenceへ限定され、locator identityとspan取得方法も同時に制御していた。今回その手続きを継承しない。
5. 変更後evidenceを一律禁止できない。F04 TaskSpecはsource behaviorの静的確認をrequiredとし、Candidate144でも変更後source確認がrequired predicateを判定した。F02のdiff / statusも成果差分と許可外driftの判定に使う。
6. Candidate125 A02の保存20 traceでは、implementation bind後・変更前再入は0 / 20件だった。追加15 traceを含む変更後method探索も0件だった。ただしC125のexact-target waveをC143へ戻すと、C122系列の取得範囲制約とF04 false stopを再導入するため継承しない。
7. Candidate143のrequired outcome全体の`implementation_bound`、Candidate144のvalidation predicate / method境界、変更前追加観測の自由度は保持する。
8. executor、CLI、runtime hook、wrapper、rating contractは変更しない。
9. 初回はA01 / A02 / F01 / F02 / F04 / F07 dependency各N=5、M=24とする。一件でもscore `3`以下、required evidence欠落、またはconsumerを持たないevidence再入があれば停止する。

## 置換する境界

```text
required_predicate_state := satisfied | unsatisfied | unobserved

evidence_consumer_ready :=
  required predicateがnonterminal
  ∧ state = unobserved
  ∧ 現在欠けている観測値がbind済み
  ∧ requested resultがそのstateをbindできる
```

repository evidence invocationは、target探索、変更前、artifact変更後、validation準備、recoveryのどの時点でも`evidence_consumer_ready=true`の場合だけ許可する。

TaskSpecが既にvalidation predicateを固定している場合、exact command、test locator、既存test symbol、一般的なrepository慣行が未固定なだけでは、そのpredicateを`unobserved`へ戻さない。これらをexecution method選択だけのために追加取得しない。

artifact変更や失敗resultは、そのresultが入力を変えたpredicateだけを失効できる。他の充足済みpredicateを一括で`unobserved`へ戻さない。consumerがterminalになった時点で未発行evidenceを失効する。

## 汎用性

この境界はtest探索専用ではない。

- 実装前に未観測のrequired effectを調べるread
- 変更後にTaskSpec-requiredなsource behaviorを静的確認するread
- 変更差分や許可外driftを判定するdiff / status
- 失敗resultで失効したeffectだけを再判定するrecovery evidence

はいずれも、未完了predicateと欠けている観測値をbindできれば許可される。

一方、一般的安全確認、念のための再読、実行method選択、既に充足済みpredicateの再確認、報告材料だけの取得はconsumerを持たないため許可しない。

## 初回評価gate

| gate | 期待 |
| --- | ---: |
| valid / rateable | 30 / 30 |
| score `4` | 30 / 30 |
| score `3`以下 | 0 |
| A01 clarification停止、変更・testなし | 5 / 5 |
| A02 canonical成果 | 5 / 5 |
| A02 implementation bind後・変更前consumerなし再入 | 0 / 5 |
| A02 artifact変更後・validation前method探索 | 0 / 5 |
| F01明示required command完備 | 5 / 5 |
| F02両source変更 | 5 / 5 |
| F04単一target必要変更とrequired静的確認 | 5 / 5 |
| F07 dependency pair完備 | 5 / 5 |
| required predicateを変える変更後evidence | 維持 |

## Cost判定

- Candidate144 A02 token中央値`180,039`を直接基準とする。
- Candidate143 A02 token中央値`235,359`、Candidate125 A02 token中央値`141,143`を補助比較とする。
- 6 case全体のCandidate144中央値はtoken`862,697`、elapsed`499.791秒`である。
- targeted N=5からStandard14全体のcost改善を主張しない。

## 非目標

- evidence回数、bytes、target数、span、locator形式の制限
- artifact変更後readの一律禁止
- exact validation commandの事前固定
- C122 / C125のprechange evidence waveまたはsingle-target continuationの再導入
- Candidate143の`implementation_bound`変更
- required validation、静的確認、diff / statusの省略
- executor、CLI、runtime hook、wrapper変更

## 初回試験

- cases: A01 r2 / A02 r2 / F01 r3 / F02 r1 / F04 r2 / F07 dependency r1
- Rating: v14
- model / reasoning: `gpt-5.6-sol` / `medium`
- CLI / Python: `0.146.0` / `3.14.5`
- repetition / configured M: 各`N=5` / `24`
- direct reference: Candidate144同case atomic run
- prompt以外の互換条件: Candidate144と完全一致

Candidate144の既存runは再実行しない。Candidate145の不足30 slotだけを発行する。全gate通過時だけ次の比較または追加試験を別判断する。

## 初回試験結果

2026-08-02に6 case各N=5を実施した。30 / 30件がscore `4`で、A02のimplementation bind後・変更前evidence再入と変更後method evidence探索はともに0 / 5件だった。F04のTaskSpec-requiredな変更後source確認は3 / 5件で保持された。詳細は[`Candidate144 / Candidate145 6 case N=5比較結果`](../evaluations/results/candidate144-candidate145-lifecycle-consumer-evidence-admission-v14-medium-a01-a02-f01-f02-f04-f07-atomic-n5-cli0146_2026-08-02.md)を正本とする。

## Standard14結果

同日に既存30 runを再利用し、不足8 caseの40 runを追加した。Standard14は70 / 70件がscore `4`で、成果退行は観測しなかった。しかしCandidate125比でtoken中央値`+13.74%`、elapsed中央値`+31.04%`のためcost gateは失敗した。詳細は[`Candidate145 Standard14 N=5`](../evaluations/results/candidate125-candidate145-lifecycle-consumer-evidence-admission-v14-medium-standard14-atomic-reuse-n5-cli0146_2026-08-02.md)を正本とする。
