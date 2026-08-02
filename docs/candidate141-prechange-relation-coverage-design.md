# Candidate141 prechange relation coverage設計

## 結論

Candidate141はCandidate140を直接親とし、`prechange_evidence_wave_ready`の完了単位だけを置換する。exact target setを一つの変更前waveで扱う既存目的は維持する。waveの完全性はtarget artifact全体のcontent量ではなく、TaskSpecが明示する各required effectのstateを決める全memberと接続の直接coverageで判定する。

行数、bytes、read command、file全体取得の禁止は追加しない。変更するのは実行方法ではなく、evidenceを完全とみなす意味である。

## Identity

- candidate number: Candidate141
- prompt identity: `the-caption-3ce91a4-prechange-relation-coverage-r1`
- direct parent: `the-caption-3ce91a4-effect-satisfaction-witness-r1`（Candidate140）
- changed target: root `AGENTS.md`
- changed predicate: `prechange_evidence_wave_ready`
- evaluation status: `f02_f04_f07_n5_evaluated / quality_gate_failed / relation_coverage_4_of_5 / stopped`

## 作成前gate

1. 基準prompt setはCandidate140とする。
2. C139 / C140 F02計10件では、required relationを含む限定取得3件は変更前の両effect認識3 / 3だった。
3. 4 target全体または過大範囲を集約した7件は、変更前の両effect認識0 / 7だった。
4. 過大取得で最終score `4`へ回復した1件も、focused validation失敗後の一回reworkで回復した。変更前判断はengineだけだった。
5. C140の初回保存outputには低Score二件を含めrequired memberの文字列が存在した。単純な文字列欠落だけでは分岐を説明できない。
6. C122のone-wave terminal closureはunder-read後の不要な再入を防いだ。この目的は削除しない。
7. C125のsingle-target continuationはF04用であり、F02の直接分岐ではない。回数とterminal closureを変更しない。
8. 次の一変更軸は、prechange waveの完了単位をtarget content coverageからrequired relation coverageへ置換することである。
9. F02 / F04 / F07各N=5でscore `4` × 15と、F02変更前の両effect認識5 / 5を要求する。score `3`以下が一件でも出たら停止する。

根拠の正本は[`Candidate140 evidence completeness granularity監査`](candidate140-evidence-completeness-granularity-audit.md)とする。

## 置換するpredicate

```text
required_relation_evidence_scope :=
  TaskSpecが明示する各未解決required effectについて、
  そのstateを決める全memberと接続を
  current content上で直接示す必要範囲の集合
```

```text
prechange_evidence_wave_ready :=
  spec_ready
  ∧ TaskSpecが同じ未解決predicateを共同で決めるexact target setを列挙済み
  ∧ target全件がadmission済み
  ∧ required_relation_evidence_scopeを一つの変更前waveのrequest identityへbind済み
  ∧ result受領後の判断がedit-readyまたはterminal stopへ限定済み
```

readyの場合、exact target set内で`required_relation_evidence_scope`へ直接bindするcontent evidenceを一つのinvocationで取得する。target artifact全体、終端までのcontent、relationへbindしない周辺contentの量だけではcoverage completeにしない。

## 維持する制御

- C122: exact target setを一waveで扱い、locator-only resultと複数wave再入を開かない
- C125: single-target continuationの適用条件、回数、terminal closure
- C128: required-effect closure
- C136: satisfied / unsatisfied / unobservedとunsatisfied effectだけの変更単位
- C138 / C139: continuation handoffとsingle-target guard
- C140: required relationの全memberと接続によるsatisfied witness
- machine rework上限とrequired validation全体

## 汎用性と非目標

required relationは、functionとcall site、producerとconsumer、branchとeffect、configとreader、schema writerとreader、dependency pair、commandと説明対象の接続へ適用できる。case ID、path、特定symbol、言語、file数へ依存しない。

TaskSpecがrequired relationを固定していない探索型課題、repository-wide review、単純なprose校正へ同じfast pathを強制しない。

次は非目標とする。

- 行数、bytes、read回数、command、output capの固定
- 全readの細分化または全fileの全体取得禁止
- 追加evidence waveまたはcontinuation回数の増加
- validation failure後のrework拡張
- executor、CLI、tool adapter、runtime hook、外部wrapperの変更

## 初回評価gate

初回はF02 / F04 / F07各N=5、M=24とする。

| gate | 期待 |
| --- | ---: |
| valid / rateable | 15 / 15 |
| score `4` | 15 / 15 |
| score `3`以下 | 0 |
| F02変更前の両effect認識 | 5 / 5 |
| F02一target部分変更 | 0 / 5 |
| F04の必要変更と既存effect保持 | 5 / 5 |
| F07 dependency pair完備 | 5 / 5 |

狙ったrelation coverageが0 / 5、全体・過大取得が変更前判断を再び支配する、または一件でもscore `3`以下なら停止する。全gate通過時だけ、追加24件またはStandard14を別判断する。

## 評価結果

[`F02 / F04 / F07各N=5`](../evaluations/results/candidate141-prechange-relation-coverage-v14-medium-f02-f04-f07-atomic-n5-stopped-cli0146_2026-08-02.md)はscore `4 / 2 = 14 / 1`だった。F02の限定取得4件は変更前に両effectを認識してscore `4`、全体取得1件はengineだけの部分変更でscore `2`となった。停止条件により追加24件とStandard14は未発行である。
