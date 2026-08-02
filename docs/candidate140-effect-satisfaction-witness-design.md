# Candidate140 effect satisfaction witness設計

## 結論

Candidate140はCandidate139を直接親とし、`effect_prechange_state(effect)=satisfied`の証拠条件だけを置換する。TaskSpec required effectが主張するvalue、call、data flow、branch、order、pair relationの全memberと接続をcurrent contentで直接観測できた場合だけ、開始状態から充足済みへbindする。

helper、symbol、literal、file、relationの片側が存在するだけでは`satisfied`にしない。これによりF02の未接続日付選択helperを充足済みと誤認せず、C139の単一target guardとC128のrequired-effect closureへ正しい三値状態を渡す。

## Identity

- candidate number: Candidate140
- prompt identity: `the-caption-3ce91a4-effect-satisfaction-witness-r1`
- direct parent: `the-caption-3ce91a4-single-target-continuation-handoff-r1`（Candidate139）
- changed target: root `AGENTS.md`
- changed predicate: `effect_prechange_state(effect)=satisfied`
- evaluation status: `not_evaluated`

## 作成前gate

1. C139 F02低Score三件は、`_resolve_market_end_date`の存在を、取得経路への接続確認なしでF02-C2充足へ読み替えた。
2. 同一条件のC128成功五件は、helperが存在しても`_fetch_asset`から未接続であることを不成立として扱い、両sourceを変更した。
3. target cardinality、追加read、validation、rework、executor behaviorは変更しない。
4. 消す判断点は、required relationの一部または関連部品の存在だけでeffect全体を`satisfied`へbindする分岐である。
5. F02 / F04 / F07各N=5で15 / 15 score `4`を要求する。
6. score `3`以下が一件でも出たら停止する。

## 置換するpredicate

```text
effect_satisfaction_witness(effect) :=
  admission済みprechange contentが
  TaskSpec required effectに明示された
  value / call / data flow / branch / order / pair relationの
  全memberと接続をcurrent content上で直接示す
```

```text
effect_prechange_state(effect) :=
  effect_satisfaction_witness(effect)があるならsatisfied
  ∨ current contentがrequired relationの不成立を直接示すならunsatisfied
  ∨ それ以外はunobserved
```

## 汎用性と非目標

このpredicateは言語、path、case ID、特定symbolへ依存しない。未使用helper、dead branch、未接続config、片側だけ更新されたdependency pair、宣言だけ存在するrouteへ適用できる。

次は非目標とする。

- 新しいevidence invocationまたは検索経路
- target集合またはsingle-target domainの変更
- validation failure後のrework拡張
- executor出力の変更
- TaskSpecにないimplementation methodの推測

## 初回評価gate

初回はF02 / F04 / F07各N=5、M=24とする。

| gate | 期待 |
| --- | ---: |
| valid / rateable | 15 / 15 |
| score `4` | 15 / 15 |
| score `3`以下 | 0 |
| F02の一target部分変更 | 0 / 5 |
| F04の既存`colSpan`保持 | 5 / 5 |
| F07 dependency pair完備 | 5 / 5 |
