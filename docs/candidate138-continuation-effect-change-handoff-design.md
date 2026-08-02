# Candidate138 continuation effect change handoff設計

## 結論

Candidate138はCandidate137を直接親とし、root `AGENTS.md`の`EVIDENCE_GATE`にあるcontinuation後の一つの分岐だけを置換する。continuation後に一部のrequired effectだけが`unsatisfied`、残りが`unobserved`の場合、観測済みcurrent contentへbindできる未充足effectだけを初回artifact変更へ渡す。未観測effectは変更せず、Candidate137のpending validation admissionへ引き渡す。

変更軸はread範囲、検索語、case固有symbol、executor出力制御ではない。C136で導入済みのeffect-local change admissionと、C137で導入済みのpending validation admissionの間に残った競合分岐を一意化する。

## Identity

- candidate number: Candidate138
- prompt identity: `the-caption-3ce91a4-continuation-effect-change-handoff-r1`
- direct parent: `the-caption-3ce91a4-pending-effect-validation-admission-r1`（Candidate137）
- changed target: root `AGENTS.md`
- changed label: `EVIDENCE_GATE`
- evaluation status: `not_evaluated`
- adoption / release / runtime projection: `not_decided / not_created / not_projected`

## 作成前gate

1. 基準prompt setはCandidate137とする。
2. 基準状態の最短正常経路は、全required effectを変更前に観測し、未充足effectだけを変更し、required validationを完了する経路である。
3. 保存済み誤経路はCandidate137 F04 run `ec3d27fea0f74905ab56ac63b05ec194`である。C1の未充足は観測したがC2をmodel decisionへbindできず、artifact変更前にscore `2`で停止した。
4. C136の`unobserved effectを別のunsatisfied effectの変更開始拒否に使わない`規則だけでは防げない。同じ`EVIDENCE_GATE`の後段に、変更predicateと保持constraintの両方をbindできなければ停止する旧分岐が残っているためである。
5. 置換するpredicateは`continuation_effect_change_ready`一つとする。
6. 消す判断点は、`initial_change_effect_set`が非空なのに、別effectが未観測という理由だけで初回artifact変更を拒否する分岐である。
7. 増える判断点は、発行予定の各変更単位が`initial_change_effect_set`内のeffectと、その観測済みcurrent contentだけへbindされているかの一件である。
8. F04 N=5で全件score `4`、必要変更5 / 5、未観測effect変更0 / 5、required validation完備5 / 5を要求する。pending effect状態が発生した場合は、artifact変更前停止0件、Candidate137 validation admission、direct validation result後closureを要求する。
9. score `3`以下、観測していないcontentの推測変更、未観測effectの変更、direct observerなしのvalidation開始、またはvalidation前完了が一件でもあれば停止する。

## 保存挙動からの導出

Candidate137 N=53の52件は通常経路でscore `4`だった。一件だけ、continuationの保存stdoutにはC2行が存在したが、agentは出力切れによりC2を確定できないと判断した。

そのrunではC1の`const hasAuditKey = true;`を直接観測し、C1が未充足であることは確定していた。C136由来の`initial_change_effect_set`へC1を入れられる状態だった。しかし後段のcontinuation分岐は変更predicateと保持constraintの両方を要求し、C2未観測を理由に停止した。

これは取得方法の問題ではない。同じ受領状態に対して、effect-local admissionとcriterion全体の完全性gateが異なる次行動を要求している問題である。

## 置換するpredicate

```text
continuation_effect_change_ready :=
  continuation result受領済み
  ∧ initial_change_effect_setが非空
  ∧ 発行予定artifact変更の各変更単位が、
    initial_change_effect_set内のeffectと
    その観測済みcurrent contentだけへbind済み
```

- `true`なら、`initial_change_effect_set`だけを初回artifact変更へ発行する。
- `unobserved effect`を充足済みとは扱わない。
- `unobserved effect`を初回artifact変更へ入れない。
- artifact変更後はCandidate137の`required_effects_validation_ready`をそのまま使う。
- `false`なら、観測済みの具体的なmissing、unreadable、contradiction、unsatisfied constraintを停止理由にする。
- 追加read、別target、別method、推測によるpreimage補完は開かない。

## 既存制御との関係

- C125のsingle-target continuation回数とscope: 変更しない。
- C135のcriterion span request authority: 変更しない。
- C136のeffect三値分類と`initial_change_effect_set`: 再利用する。
- C137のpending validation admissionとvalidation後closure: 変更しない。
- C128由来のreworkとstop condition: 変更しない。

## 汎用性と非目標

適用対象は、単一target内の複数required effectのうち、観測済み未充足effectだけについてexact current contentへbindした変更を構成でき、他effectが未観測のimplementation taskである。case ID、言語、拡張子、symbol名、行番号をpredicateへ含めない。

次は非目標とする。

- 全effectを変更前に観測するためのread最適化
- executor、adapter、runtime hook、外部wrapperによる出力制御
- 未観測contentを推測した変更
- 複数targetにまたがる未観測dependencyの楽観的変更
- direct validationを持たないpending effectの完了
- validation failure後の新しいrework経路

## 初回評価gate

初回はF04 N=5、M=24だけを実施する。score `3`以下が一件でも出た時点で停止する。pending effect状態が0件なら品質passとmechanism未観測を分け、同じpoolを24件単位で継続する。

| gate | 期待 |
| --- | ---: |
| valid / rateable | 5 / 5 |
| score `4` | 5 / 5 |
| score `3`以下 | 0 / 5 |
| 必要な未充足effect変更 | 5 / 5 |
| 未観測effect変更 | 0 / 5 |
| required validation完備 | 5 / 5 |
| pending effect発生時の変更前停止 | 0件 |
| direct observerなしpending effectでvalidation開始 | 0件 |
| validation result前の全effect完了判定 | 0件 |
