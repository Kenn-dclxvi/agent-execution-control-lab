# 一般チャットsemantic grader threshold decision r1

## 現在状態

`fixed_before_holdout`

数値とrisk policyを独立AI reviewerが確認し、評価責任者である利用者が最終承認した。threshold contractはholdout resultを見る前に`fixed`へ更新した。

## 判断根拠

- pilot report identity: `sha256:7039ae072aa5af74a48bc46d978e75f40d8474782582c3d73604226869c53194`
- pilot recovery result: `general-chat-semantic-pilot-panel-r1-attempt-r2-recovery-r1`
- AI adjudication result: `general-chat-semantic-pilot-adjudication-r1-run-r1`
- risk policy: `docs/general-chat-semantic-grader-risk-policy-r1.md`

pilotではAI grader 3件が32 assertionを判定し、31件で3者一致した。唯一の不一致はpanel外の固定AI adjudicatorが`fail`と裁定した。32 assertionはすべてreference labelを持つが、人間alignmentは未測定である。

## 決定値

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

利用者は、false pass、major false pass、false failおよびunknownを許容しないと決めた。これと整合させ、reference labelとの完全一致率も`1`とする。1件でも不一致があればgraderを合格にしない。

## レビューと最終承認

役割は次の2者である。

- `independent-ai-reviewer`: `/root/threshold_ai_review`
- `evaluation-owner`

独立AI reviewerは固定資料だけを読み、holdout resultを見ずに`approved`を返した。producer identityと最終resultのSenderはともに`/root/threshold_ai_review`である。評価責任者である利用者は、そのレビューをAIが担当し、自身が最終承認する統治方法を明示したうえで「これでいいよ」と最終承認した。

レビュー記録は`evaluations/targets/general-chat-response-control/calibration/threshold-ai-review-r1.json`を正本とする。固定時刻は`2026-08-20T10:30:33Z`である。

## 固定時に記録したもの

次を同じ一回の変更で記録した。

- threshold contractの`status=fixed`
- `fixed_before_holdout_qualification=true`
- 全閾値値
- `risk_policy_reference=docs/general-chat-semantic-grader-risk-policy-r1.md`
- `decision_record=docs/general-chat-semantic-grader-threshold-decision-r1.md`
- 独立AI reviewerと評価責任者のidentity
- `fixed_at`

schema検証と`prepare_semantic_calibration.py check-threshold`が成功した場合だけ、sealed holdoutの準備へ進む。

## 決定効果

承認完了後に許可するのは、固定条件でのsealed holdout準備と一度だけの正式grader適格試験である。promptの採用、release、projectionまたは本体反映は別の判断とする。
