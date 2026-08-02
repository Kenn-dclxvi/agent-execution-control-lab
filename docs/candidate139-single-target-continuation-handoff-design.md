# Candidate139 single-target continuation handoff設計

## 結論

Candidate139はCandidate138を直接親とし、`continuation_effect_change_ready`へ既存の`single_change_target_ready`をANDする。単一targetが全未解決変更criterionを所有する場合だけ、観測済み未充足effectの部分変更をpending validationへ渡す。複数editable targetが共同でrequired outcomeを所有する場合は、Candidate138の部分変更handoffを開かない。

## Identity

- candidate number: Candidate139
- prompt identity: `the-caption-3ce91a4-single-target-continuation-handoff-r1`
- direct parent: `the-caption-3ce91a4-continuation-effect-change-handoff-r1`（Candidate138）
- changed target: root `AGENTS.md`
- changed predicate: `continuation_effect_change_ready`
- evaluation status: `not_evaluated`

## 作成前gate

1. 基準prompt setはCandidate138とする。
2. 基準状態の正常経路は、単一targetのF04で観測済み未充足effectだけを変更し、残りを変更後direct validationへ渡す経路である。
3. 保存済み誤経路はCandidate138 F02 run `a8738c6a810f4e538c210c11c1363089`と`c17f6943b9f54e2dadd3460f2104742b`である。
4. 両runは二つのeditable sourceが共同でoutcomeを所有するが、観測できた`v4_engine.py`だけを変更し、未観測のupdater effectをvalidationへ渡して失敗した。
5. 置換軸は`continuation_effect_change_ready`への`single_change_target_ready`追加だけとする。
6. 消す判断点は、複数editable target taskで一target分だけを部分変更してvalidationへ進む分岐である。
7. 新しいread、検索、validation、rework、executor制御は追加しない。
8. F02 / F04 / F07各N=5で15 / 15 score `4`、F04 handoff保持、複数target部分変更0件を要求する。
9. score `3`以下、F04 handoff消失、またはF02で一targetだけを変更してvalidationへ進むrunが一件でもあれば停止する。

## 置換するpredicate

```text
continuation_effect_change_ready :=
  single_change_target_ready
  ∧ continuation result受領済み
  ∧ initial_change_effect_setが非空
  ∧ 発行予定artifact変更の各変更単位が
    initial_change_effect_set内のeffectと
    その観測済みcurrent contentだけへbind済み
```

`single_change_target_ready=false`では部分変更handoffを開かず、既存のmulti-target evidence waveと停止条件を維持する。

## 汎用性と非目標

このguardはcase ID、言語、path名、symbol名ではなく、required effectを所有するeditable targetのcardinalityへ依存する。

次は非目標とする。

- 複数targetで不足contentを追加取得する新経路
- validation failure後のrework拡張
- executor出力の制御
- 未観測targetの推測変更
- Candidate138のF04 handoffやCandidate137のdirect validation closureの変更

## 初回評価gate

初回はF02 / F04 / F07各N=5、M=24とする。score `3`以下が一件でも出たら停止する。

| gate | 期待 |
| --- | ---: |
| valid / rateable | 15 / 15 |
| score `4` | 15 / 15 |
| score `3`以下 | 0 |
| F02の一target部分変更 | 0 / 5 |
| F04の必要変更 | 5 / 5 |
| F04 handoff発生時のdirect validation | 完備 |
| F07の両dependency変更 | 5 / 5 |
