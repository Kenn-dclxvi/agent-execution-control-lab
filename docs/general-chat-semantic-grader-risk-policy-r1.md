# 一般チャットsemantic grader risk policy r1

## 適用範囲

このrisk policyは、一般チャット回答のsemantic graderを正式holdoutで適格判定する現在のr1系列へ適用する。固定済みのcase、reference、rubric、grader identity、model、reasoning、runtimeおよび実行条件の範囲だけを扱う。

このpolicyに基づく合格は、graderの正式holdout適格性だけを表す。評価対象promptの採用、release、projectionまたは本体有効化を意味しない。

## 防ぐ誤判定

次の誤判定を一件も許容しない。

- `false pass`: 固定referenceが`fail`の回答をgraderが`pass`にする
- `major false pass`: severityが`major`の`false pass`
- `false fail`: 固定referenceが`pass`の回答をgraderが`fail`にする
- `unknown`: 判定可能な固定入力に対してgraderがlabelを確定できない
- reference labelとのその他の不一致

一件でも該当すればgraderを不合格にする。この方針に対応する閾値は次のとおりである。

```json
{
  "minimum_exact_agreement_rate": 1,
  "maximum_false_pass_rate": 0,
  "maximum_false_fail_rate": 0,
  "maximum_unknown_rate": 0,
  "maximum_major_false_pass_count": 0,
  "ambiguous_gold_items_allowed": false
}
```

## referenceの扱い

reference labelを一意に決められない項目を正式holdoutへ含めない。曖昧な項目が見つかった場合はgraderへ有利または不利なlabelを推測せず、holdout artifactの欠陥として実行または判定を停止する。

pilotのAI grader 3件とpanel外AI adjudicatorによって32 assertionのreference labelは形成されたが、人間専門家との一致は未測定である。そのため、この系列から人間alignmentを主張しない。

## 固定と見直し

閾値はsealed holdoutを発行する前に、独立AI reviewerが根拠と値を確認し、評価責任者が最終承認して、決定時刻とともに固定する。holdout resultを見た後で閾値を緩和し、同じholdoutを合格根拠へ再利用しない。

運用実績から見直す場合は、現在のr1 resultを遡及変更せず、別threshold revisionと、それに対応する新しい未見holdoutを用意する。

## 外部指針との関係

OpenAIの評価ベストプラクティスが推奨する、task-specificな成功条件、明確なrubric、典型・edge・adversarial case、人間feedbackによる自動採点の校正を根拠にする。ただし、同指針はこの対象に共通する普遍的な閾値数値を定めていない。r1の数値は、利用者が全誤判定を許容しないと決めたrisk policyに基づく。
