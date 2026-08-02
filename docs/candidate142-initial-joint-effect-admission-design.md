# Candidate142 initial joint effect admission設計

## 結論

Candidate142はCandidate141を直接親とし、`initial_change_effect_set`の初回変更admissionだけを置換する。

TaskSpec上で複数editable targetが同じrequired outcomeを共同所有する場合は、変更前result受領後に全required effectが`satisfied`または`unsatisfied`へbindされた場合だけ、unsatisfied effectを初回変更へ入れる。一effectでも`unobserved`なら部分変更を発行しない。

単一editable targetまたはjoint owner domain外では、C136のeffect-local admissionを維持する。これによりF04の観測済み未充足effectを変更できる一方、F02やdependency pairの一target部分変更を閉じる。

## Identity

- candidate number: Candidate142
- prompt identity: `the-caption-3ce91a4-initial-joint-effect-admission-r1`
- direct parent: `the-caption-3ce91a4-prechange-relation-coverage-r1`（Candidate141）
- changed target: root `AGENTS.md`
- changed predicate: `initial_change_effect_set`
- evaluation status: `f02_f04_f07_n5_evaluated / quality_gate_failed / stopped`

## 作成前gate

1. 基準prompt setはCandidate141とする。
2. C141 F02の限定取得4件は、変更前に両effectを認識して両sourceを変更し、score `4`だった。
3. 全体取得1件はupdater effectを`unobserved`のまま残し、C136のeffect-local admissionによりengineだけを変更してscore `2`となった。
4. C141のrelation coverageはrequest identityへbindされたが、result受領後から初回変更までのadmissionを変更しなかった。
5. C139の`single_change_target_ready`はcontinuation後のhandoffだけをguardし、initial changeには適用されない。
6. 次の一変更軸は、TaskSpec-bound joint owner domainで全required effect state bindを初回変更の条件にすることである。
7. one-wave、single-target continuation、effect witness、validation、reworkは変更しない。
8. F02 / F04 / F07各N=5でscore `4` × 15を要求する。
9. score `3`以下、F02部分変更、F04必要変更抑止、F07 pair欠落が一件でもあれば停止する。

根拠の正本は[`Candidate141 post-result change admission監査`](candidate141-post-result-change-admission-audit.md)とする。

## 置換するpredicate

```text
joint_owner_domain :=
  prechange_evidence_wave_ready
  ∧ single_change_target_ready=false
  ∧ TaskSpec上で複数editable targetが同じrequired outcomeを共同所有する
```

```text
initial_change_effect_set :=
  joint_owner_domain=trueなら、
    全required effectがsatisfiedまたはunsatisfiedへbind済みの場合だけ
    unsatisfiedの全effect
  joint_owner_domain=falseなら、
    従来どおりunsatisfiedの全effect
```

joint owner domainで一effectでも`unobserved`なら、初回artifact変更を発行しない。追加evidenceは開かず、既存のterminal dispositionに従う。

## 維持する制御

- C122: exact target setのone-wave terminal closure
- C125: single-target continuation
- C128: required-effect closure
- C136: joint owner domain外のeffect-local admission
- C138 / C139: continuation後handoffとsingle-target guard
- C140: effect satisfaction witness
- C141: required relation evidence scope
- machine rework上限とrequired validation全体

## 汎用性と非目標

joint owner domainは、application producerとdomain consumer、schema writerとreader、configとruntime consumer、migrationとmodel、dependency declarationとcompiled provenance、API implementationとadapterへ適用できる。

case ID、path、symbol、言語、file数そのものではなく、TaskSpec上のrequired outcome共同所有関係へ依存する。

次は非目標とする。

- 行数、bytes、read回数、commandの固定
- 全file取得の禁止
- 追加evidence waveまたはreworkの追加
- unobserved effectの推測変更
- single-target taskを完全観測gateへ戻すこと
- executor、CLI、tool adapter、runtime hook、外部wrapperの変更

## 初回評価gate

初回はF02 / F04 / F07各N=5、M=24とする。

| gate | 期待 |
| --- | ---: |
| valid / rateable | 15 / 15 |
| score `4` | 15 / 15 |
| score `3`以下 | 0 |
| F02変更前の両effect認識または変更前terminal stop | 5 / 5 |
| F02一target部分変更 | 0 / 5 |
| F04必要変更と既存effect保持 | 5 / 5 |
| F07 dependency pair完備 | 5 / 5 |

quality gateはterminal stopを成功扱いしない。F02で部分変更を防いでも成果未達ならscore `3`以下としてCandidate142を停止する。全gate通過時だけ追加24件またはStandard14を別判断する。

## 実測結果

[`F02 / F04 / F07各N=5結果`](../evaluations/results/candidate142-initial-joint-effect-admission-v14-medium-f02-f04-f07-atomic-n5-stopped-cli0146_2026-08-02.md)はscore `4 / 2 = 12 / 3`だった。F02の一target部分変更は0 / 5へ閉じたが、過大取得でeffectを観測できなかった3件が変更なしで停止した。停止条件に従い、追加24件とStandard14へ進めない。
