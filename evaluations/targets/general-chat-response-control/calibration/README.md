# Semantic grader calibration

このディレクトリは、一般チャット自然文を判定するAI grader panelの開発用pilot、任意の人間監査、および未見holdoutでの正式適格試験を分離して保持する。

## アーティファクト

- [`calibration-input-core-r1.json`](calibration-input-core-r1.json): 固定8 Case、16回答、32 assertionからなる開発用pilot。正式適格試験へ再利用しない
- [`ai-grader-panel-r1.json`](ai-grader-panel-r1.json): `gpt-5.6-terra`の独立3実行、panel外adjudicator、`codex-cli 0.148.0`および人間監査の位置づけを固定
- [`rater-packet-r1.schema.json`](rater-packet-r1.schema.json): 回答の出自、正本IDおよび過去scoreを隠した共通packet
- [`organizer-map-r1.schema.json`](organizer-map-r1.schema.json): 不透明な採点IDを正本IDへ戻す運営者専用map。graderへ渡さない
- [`ai-grader-label-template-r1.schema.json`](ai-grader-label-template-r1.schema.json): AI grader用の未記入template
- [`ai-grader-label-r1.schema.json`](ai-grader-label-r1.schema.json): AI grader一実行分の完了済み有限label
- [`ai-panel-pilot-report-r1.schema.json`](ai-panel-pilot-report-r1.schema.json): 全員一致率、名義尺度のKrippendorff's alpha、label分布および不一致一覧
- [`ai-panel-adjudication-r1.schema.json`](ai-panel-adjudication-r1.schema.json): panel外AIによる不一致裁定
- [`ai-adjudicator-run-preflight-r1.schema.json`](ai-adjudicator-run-preflight-r1.schema.json)と[`ai-adjudicator-run-result-r1.schema.json`](ai-adjudicator-run-result-r1.schema.json): 固定adjudicator一件の発行前receiptと実行result
- [`ai-grader-run-preflight-r1.schema.json`](ai-grader-run-preflight-r1.schema.json): 固定runtime、正本、runnerおよび3件の実行入力をslot発行前にbindするreceipt
- [`ai-grader-panel-run-result-r1.schema.json`](ai-grader-panel-run-result-r1.schema.json): 3件のprocess結果、token、labelおよびpilot reportを保持するrun result
- [`ai-grader-panel-recovery-result-r1.schema.json`](ai-grader-panel-recovery-result-r1.schema.json): 完了済みJSONLのusage形式差で`unrateable`になったrunを再発行せず回復するresult
- [`qualification-threshold-r1.json`](qualification-threshold-r1.json): pilotとrisk policyに基づき複数承認者が固定する適格条件
- [`threshold-ai-review-r1.schema.json`](threshold-ai-review-r1.schema.json)と[`threshold-ai-review-r1.json`](threshold-ai-review-r1.json): 独立AI reviewerのproducer identity、holdout未閲覧、判断理由および承認結果を固定するレビュー記録
- [`qualification-holdout-r1.schema.json`](qualification-holdout-r1.schema.json)と[`qualification-holdout-r1.json`](qualification-holdout-r1.json): pilotと回答文、項目IDおよびassertion IDが重複しない16回答、32 assertionのsealed holdout
- [`qualification-holdout-plan-r1.schema.json`](qualification-holdout-plan-r1.schema.json)と[`qualification-holdout-plan-r1.json`](qualification-holdout-plan-r1.json): reference生成、必要時の裁定、reference seal、一度だけの資格graderおよび閾値照合の発行順と停止条件
- [`qualification-reference-r1.schema.json`](qualification-reference-r1.schema.json)と[`qualification-reference-r1.json`](qualification-reference-r1.json): 独立AI grader 3件が32 assertionですべて一致し、裁定不要でsealしたholdout reference
- [`qualification-metric-contract-r1.schema.json`](qualification-metric-contract-r1.schema.json)と[`qualification-metric-contract-r1.json`](qualification-metric-contract-r1.json): exact agreement、false pass、false fail、unknownおよびmajor false passの分母と数え方を資格grader実行前に固定
- [`qualification-grader-preflight-r1.schema.json`](qualification-grader-preflight-r1.schema.json)、[`qualification-grader-dispatch-r1.schema.json`](qualification-grader-dispatch-r1.schema.json)、[`qualification-grader-run-result-r1.schema.json`](qualification-grader-run-result-r1.schema.json): reference labelを入力へ含めない単独資格graderの発行前receipt、一度だけの発行および生result
- [`holdout-organizer-map-r1.schema.json`](holdout-organizer-map-r1.schema.json)と[`holdout-reference-preflight-r1.schema.json`](holdout-reference-preflight-r1.schema.json): holdoutの正本IDをgrader packetから隠す運営者mapと、reference panel 3件を未発行状態で固定するreceipt
- [`holdout-reference-panel-dispatch-r1.schema.json`](holdout-reference-panel-dispatch-r1.schema.json)、[`holdout-reference-panel-report-r1.schema.json`](holdout-reference-panel-report-r1.schema.json)、[`holdout-reference-panel-run-result-r1.schema.json`](holdout-reference-panel-run-result-r1.schema.json): 一度だけの3 slot発行、consensusまたは不一致、および生実行結果を分離して固定する
- [`holdout reference panel preflight r1 結果`](../docs/holdout-reference-preflight-r1-result.md): 外部run rootへ固定した3 slot、runtime identityおよび`ready_not_issued`状態
- [`holdout reference panel r1 結果`](../docs/holdout-reference-panel-r1-result.md): 3件の有効result、32件の全員一致、label分布およびreference seal
- [`semantic grader資格試験 preflight r1 結果`](../docs/qualification-grader-preflight-r1-result.md): reference非開示、単独grader identity、測定式および`ready_not_issued`状態
- [`grader-qualification-report-r1.schema.json`](grader-qualification-report-r1.schema.json): pilotと重複しないsealed holdoutを一度だけ測る正式result
- [`human-label-r2.schema.json`](human-label-r2.schema.json): 人間監査を追加する場合のlabel形式。pilot開始には必須でない
- [`pilot-report-r1.schema.json`](pilot-report-r1.schema.json)と[`pilot-adjudication-r1.schema.json`](pilot-adjudication-r1.schema.json): 人間だけでpilotを行う任意経路
- [`calibration-report-r1.schema.json`](calibration-report-r1.schema.json): 初期方式の履歴schema。新しい正式適格resultには使わない

## 証拠の意味

AI panelの全員一致またはpanel外AIの裁定から得たreferenceは`multi_grader_consensus_reference`である。同じmodelを複数実行した場合もあり得るため、異なるmodel間の一致とは主張しない。AIだけで生成したresultを`human gold`または`human_aligned`と呼ばない。人間監査がない場合は`human_alignment_state=unmeasured`を保持する。

pilot reportの一致率とKrippendorff's alphaはrubricとgrader identityを直すための観測値であり、pilotの合否やgraderの正式適格性を表さない。AI graderのlabel、AI裁定および人間監査を同じ証拠種別へまとめない。

## 標準実施順

1. `ai-grader-panel-r1.json`へ3件以上のpanel memberと、panelに含まれないadjudicatorの固定identityを記録する。評価対象モデルと同じmodel identityは使わない。
2. panel memberごとに`prepare-ai`を実行する。各memberは別contextで実行し、他memberの出力を渡さない。
3. 完了済みlabelを`ai-grader-label-r1.schema.json`で検証し、対応するmapと同じ順で`analyze-ai-panel`へ渡す。
4. 不一致があればpanel memberではない固定adjudicatorだけへ渡し、`ai-panel-adjudication-r1.schema.json`で記録する。多数決だけでreferenceにしない。
5. 人間監査を行う場合は、panel不一致、`unknown`、major assertionおよび固定seedによる層化抽出を対象にする。人間監査を行わなくてもpilotは開始できる。
6. pilot report、裁定result、任意の人間監査およびrisk policyを独立AI reviewerが確認し、評価責任者が最終承認して閾値を固定する。
7. pilotと重複しないsealed holdout、reference、grader identityおよび判定方法を固定する。`check-threshold`成功前にholdout graderを発行しない。
8. holdout grader resultを一度だけ閾値へ照合する。holdout resultを見て閾値を変え、同じholdoutで合格を主張しない。

現在はpilot入力、AI panel identity、schema、packet生成、隔離runner、3件のAI label、pilot report、不一致1件のAI裁定、risk policy、独立AI reviewおよび評価責任者の最終承認までが存在する。裁定labelは`fail`で、pilotの32 assertionはすべてreference labelを持つ。threshold contractはholdout確認前に`fixed`となった。pilotと重複しない16回答、32 assertionのholdoutを用いたreference panelは3件とも有効で、全32 assertionが一致したため、裁定を発行せずreferenceをsealした。単独資格graderの測定式とpreflightも固定済みで、状態は`ready_not_issued`である。人間判断との一致、資格grader result、正式resultおよびr2有効化authorityは存在しない。各runnerはpreflightと発行を分離し、外部run rootだけへ生出力を保存する。

```text
prepare_semantic_calibration.py prepare-ai --calibration-input <path> --cases <path> --grader-execution-id <id> --packet-output <path> --organizer-map-output <path> --label-template-output <path>
prepare_semantic_calibration.py analyze-ai-panel --organizer-map <map-1> --organizer-map <map-2> --organizer-map <map-3> --ai-grader-label <label-1> --ai-grader-label <label-2> --ai-grader-label <label-3> --output <path>
prepare_semantic_calibration.py check-ai-panel --panel <path> --model-under-test <model>
prepare_semantic_calibration.py check-threshold --threshold <path>
run_ai_grader_panel.py preflight --run-root <repository外の空path>
run_ai_grader_panel.py run --preflight <run-root>/preflight.json
run_holdout_reference_panel.py preflight --run-root <repository外の空path>
run_holdout_reference_panel.py validate --preflight <run-root>/preflight.json
run_holdout_reference_panel.py run --preflight <run-root>/preflight.json
run_semantic_grader_qualification.py preflight --run-root <repository外の空path>
run_semantic_grader_qualification.py validate --preflight <run-root>/preflight.json
run_semantic_grader_qualification.py run --preflight <run-root>/preflight.json
```
