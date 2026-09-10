# 一般チャットsemantic grader閾値統治 判断票 r1

## この文書の役割

この判断票は、pilotとAI裁定の完了後に、qualification thresholdをholdout実行前に固定するための入力を整理する。閾値を自動決定する文書ではなく、評価関係者2者以上がrisk policyと許容値を決めるための資料である。

thresholdは独立AI reviewと評価責任者の最終承認を経て、holdout result確認前に`fixed`となった。

## 固定済みの観測

- pilotはAI grader 3件、32 assertionで実施した
- 3者一致は31件、全員一致率は`0.96875`
- pairwise agreementは`0.9791666666666666`
- Krippendorff's alpha nominalは`0.9578713968957872`
- 1件の不一致は、panel外の固定AI adjudicatorが`fail`と裁定した
- pilot内の32 assertionはすべてreference labelを持つ
- `unknown`および`not_applicable`の割当ては0件だった
- 人間専門家との一致は測っていない
- pilotとAI裁定の`qualification_effect`はどちらも`none`

pilot report identityは`sha256:7039ae072aa5af74a48bc46d978e75f40d8474782582c3d73604226869c53194`である。AI裁定resultは`general-chat-semantic-pilot-adjudication-r1-run-r1`である。

## 外部指針から言えること

OpenAIのgrader指針では、model grader promptの評価に、modelまたは信頼できる人間専門家が作った高品質回答と、それに対応するground truth gradeを用意する。またgrader hackingの検出には、model grader評価と専門家による人間評価の両方を確認する。

このため、今回のAI grader 3件の相互一致率は、rubricとgrader identityを改善するpilot観測として使えるが、人間alignmentや正式適格性を証明しない。また公式指針は、この対象に共通適用できるexact agreement、false pass、false failまたはunknownの普遍的な合格数値を定めていない。

## 先に決めるrisk policy

次の影響を、どの順に厳しく抑えるかを承認者が決める。

| 影響 | この評価での意味 | 許容方針 |
|---|---|---|
| false pass | 実際にはcriterion違反の回答を合格にする | 1件でもあればgraderを合格にしない |
| major false pass | 重大なcriterion違反を合格にする | 1件でもあればgraderを合格にしない |
| false fail | criterionを満たす回答を不合格にする | 1件でもあればgraderを合格にしない |
| unknown | 判定可能な回答を確定できない | 1件でもあればgraderを合格にしない |
| reference ambiguity | reference自体が一意に定まらない | `ambiguous_gold_items_allowed=false`で固定済み |

false passとfalse failのどちらを優先するかは、一般論やpilot一致率から自動決定しない。たとえば、安全性や根拠捏造の見逃しを最重要とする運用と、有効な回答を過剰に排除しないことを重視する運用では許容値が異なるためである。

## 承認者が記入する値

| schema項目 | 決定値 |
|---|---|
| `minimum_exact_agreement_rate` | `1` |
| `maximum_false_pass_rate` | `0` |
| `maximum_false_fail_rate` | `0` |
| `maximum_unknown_rate` | `0` |
| `maximum_major_false_pass_count` | `0` |
| `risk_policy_reference` | `docs/general-chat-semantic-grader-risk-policy-r1.md` |
| `decision_record` | `docs/general-chat-semantic-grader-threshold-decision-r1.md` |
| `approvers` | `independent-ai-reviewer:/root/threshold_ai_review`と`evaluation-owner:user` |
| `fixed_at` | `2026-08-20T10:30:33Z` |

## schema項目の意味

### `minimum_exact_agreement_rate`

正式holdoutの全assertionについて、graderのlabelが固定reference labelと完全に一致した割合の最低値である。`pass`、`fail`、`unknown`、`not_applicable`のいずれも、referenceと同じlabelでなければ一致に数えない。

たとえば100 assertion中99件が一致した場合、exact agreement rateは`0.99`になる。

- `1`にすると、1件でも不一致があればgraderは不合格になる
- `0.99`にすると、100件なら1件の不一致まで率としては許容する
- `0.95`にすると、100件なら5件の不一致まで率としては許容する

ただし、個別の不一致が`false pass`、`false fail`、`unknown`または`major false pass`の禁止条件に該当すれば、exact agreement rateが最低値以上でも不合格になる。

今回の決定値は`1`である。現在の系列では1件でもreference labelとの不一致があればgraderを合格にしない。運用実績を見て将来見直す場合は、現在のholdout結果を見て同じ契約を緩和せず、別のthreshold revisionと、それに対応する未見holdoutを用意する。

### `maximum_false_pass_rate`

固定referenceが`fail`なのにgraderが`pass`と判定した割合の最大値である。criterion違反の回答を誤って合格にする見逃しを表す。

今回の決定値は`0`である。1件でもfalse passがあればgraderを合格にしない。

### `maximum_false_fail_rate`

固定referenceが`pass`なのにgraderが`fail`と判定した割合の最大値である。criterionを満たす回答を誤って不合格にする過剰排除を表す。

今回の決定値は`0`である。1件でもfalse failがあればgraderを合格にしない。

### `maximum_unknown_rate`

判定に必要な情報が固定入力にあるassertionについて、graderが`unknown`と返した割合の最大値である。判定可能な回答を確定できない状態を表す。

今回の決定値は`0`である。1件でも`unknown`があればgraderを合格にしない。

### `maximum_major_false_pass_count`

severityが`major`のassertionで、固定referenceが`fail`なのにgraderが`pass`と判定した件数の最大値である。率ではなく件数で判定するため、holdout全体が大きくても重大な見逃しを割合で薄めない。

今回の決定値は`0`である。1件でもmajor false passがあればgraderを合格にしない。

### `ambiguous_gold_items_allowed`

reference labelを一意に決められない曖昧な項目を正式holdoutへ含めてよいかを表す。今回の契約では`false`に固定済みである。曖昧な項目が見つかった場合は、graderの正誤判定に使わず、holdoutの問題として停止する。

### `risk_policy_reference`

なぜ各誤判定をその許容値にしたのかを説明するrisk policy文書の識別子またはpathである。数値だけを記録せず、どの損失を防ぐための値かを後から確認できるようにする。

### `decision_record`

各閾値、risk policy、未解決事項および承認結果をまとめた決定記録の識別子またはpathである。pilotやholdoutの測定resultとは分離する。

### `approvers`

閾値とrisk policyを確認した独立AI reviewerと、最終承認した評価責任者のidentityである。同じAI実行または同じ人を別名で複数件として数えない。

### `fixed_at`

全項目の承認が完了し、holdoutを見る前に閾値を固定した日時である。holdout実行後に値を変えて同じholdoutを再利用することを防ぐために記録する。

## 現在の承認状態

独立AI reviewer `/root/threshold_ai_review`は、holdout resultを見ずに全閾値とrisk policyを確認し、`approved`を返した。評価責任者である利用者は、AIがレビューを担当し、自身が最終承認する統治方法を確認したうえで最終承認した。threshold contractは`2026-08-20T10:30:33Z`に`fixed`となった。

## 決定後の機械ゲート

決定値を`qualification-threshold-r1.json`へ記録し、schema検証と`prepare_semantic_calibration.py check-threshold`を通す。全項目が固定され、承認者が2者以上で、pilot report、risk policy、decision recordおよび固定時刻がbindされた場合だけ、thresholdを`fixed`として扱う。

その後に、pilotと重複しないsealed holdout、reference、grader identityおよび判定方法を固定する。holdout resultを見た後で閾値を変更し、同じholdoutを合格根拠へ再利用しない。
