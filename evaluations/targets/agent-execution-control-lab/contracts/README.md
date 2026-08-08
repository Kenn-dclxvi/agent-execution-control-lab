# PRレビュー実行contract索引

| contract | 状態 | 用途 |
| --- | --- | --- |
| [`pr-review-core-r1`](pr-review-core-r1.json) | `pilot_probe_blocked` | 2026-08-08のCore Review診断条件 |
| [`pr-review-core-r2`](pr-review-core-r2.json) | `qualification_ready`（当時の宣言） | profile identity、quality rating、3 KPIを固定した診断条件 |
| [`baseline-input-mapping-r1`](baseline-input-mapping-r1.json) | `unsatisfied` | 現行Claude workflowとCore Baseline候補の入力対応およびblock条件 |
| [`baseline-input-mapping-r2`](baseline-input-mapping-r2.json) | `unsatisfied` | authority原文接続後の入力対応。差分外repository readだけがblock |
| [`baseline-input-mapping-r3`](baseline-input-mapping-r3.json) | `satisfied` | `.git`なしread-only snapshot接続後のsource-to-Core入力対応 |
| [`baseline-input-mapping-r4`](baseline-input-mapping-r4.json) | `unsatisfied` | 規則identityの欠落は解消したが、Anthropic純正code-review workflowのproducer構成と検証段階が未移植 |
| [`baseline-code-review-workflow-mapping-r1`](baseline-code-review-workflow-mapping-r1.json) | `satisfied_not_executed` | 固定code-review sourceの8段階を新Baseline promptへ対応付けた設計receipt |
| [`baseline-execution-parity-r1`](baseline-execution-parity-r1.json) | 履歴監査・現在gateには不使用 | target repositoryへインストール済みworkflowとの完全一致を要求した監査 |
| [`baseline-measurement-boundary-r1`](baseline-measurement-boundary-r1.json) | `satisfied` | Claude Code純正相当のレビュー条件と測定用の変更との境界 |
| [`baseline-measurement-boundary-r2`](baseline-measurement-boundary-r2.json) | `satisfied` | 固定code-review sourceのsubagent model role、並列review、issue validationを保持する新Baseline測定境界 |
| [`pr-review-workflow-free-boundary-r1`](pr-review-workflow-free-boundary-r1.json) | `satisfied` | 同じ入力、権限、成果条件、root model、Actionを保ち、review方法の指定だけを外す校正境界 |
| [`pr-review-relationship-role-boundary-r1`](pr-review-relationship-role-boundary-r1.json) | `satisfied` | 関係レビュー役を1人に固定し、rootの調査を禁止する校正境界 |
| [`pr-review-relationship-reviewer-model-comparison-preflight-r1`](pr-review-relationship-reviewer-model-comparison-preflight-r1.json) | 実行条件の履歴 | Sonnet条件とOpus条件の構造差分をmodel roleだけに固定した6反復を完了 |
| [`pr-review-r1-case-qualification-audit-r1`](pr-review-r1-case-qualification-audit-r1.json) | `partially_satisfied` | PRR-C02、C03、C05、C06を資格確認へ許可し、C04をseverity不整合で除外 |
| [`baseline-authority-selection-r1`](baseline-authority-selection-r1.json) | 選択・接続済み | 固定target treeのroot `CLAUDE.md`解決とchanged path局所`AGENTS.md`の適用順・content identity |
| [`baseline-repository-snapshot-r1`](baseline-repository-snapshot-r1.json) | 固定済み | target treeとPRR-C01/r2 overlayから生成するrepository snapshot identity |
| [`baseline-repository-snapshot-prr-c01-r3-r1`](baseline-repository-snapshot-prr-c01-r3-r1.json) | 固定済み・qualificationで使用 | target treeと独立監査済みPRR-C01/r3 overlayから生成するqualification用snapshot identity |
| [`baseline-repository-snapshot-prr-c01-r4-r1`](baseline-repository-snapshot-prr-c01-r4-r1.json) | 固定済み・独立監査前 | target treeとPRR-C01/r4 overlayから生成したqualification候補用snapshot identity |
| [`prr-c01-r4-review-eligibility-r1`](prr-c01-r4-review-eligibility-r1.json) | 固定済み・model-visible | live PRのclosed、draft、review要否、既review確認を置換するqualification用eligibility |
| [`pr-review-agentic-retrieval-c01-r3-qualification-n2-r1-preflight`](pr-review-agentic-retrieval-c01-r3-qualification-n2-r1-preflight.json) | 初回実行条件の履歴 | repetition 1はreviewer開始前に`execution_failed`となった。receiptは変更せず保持 |
| [`pr-review-agentic-retrieval-c01-r3-qualification-n2-r2-preflight`](pr-review-agentic-retrieval-c01-r3-qualification-n2-r2-preflight.json) | 二回目の実行条件の履歴 | reviewerは起動したが構造化結果を返せず、結果は`execution_failed`。receiptは変更せず保持 |
| [`pr-review-agentic-retrieval-c01-r3-qualification-n2-r3-preflight`](pr-review-agentic-retrieval-c01-r3-qualification-n2-r3-preflight.json) | 三回目の実行条件の履歴 | reviewerは動作したがターン上限に達し、結果は`execution_failed`。receiptは変更せず保持 |
| [`pr-review-agentic-retrieval-c01-r3-qualification-n2-r4-preflight`](pr-review-agentic-retrieval-c01-r3-qualification-n2-r4-preflight.json) | 四回目の実行条件の履歴 | model-visible workspaceのgit初期化とAction既定turn条件を固定。run 31256216037は`quality_failed` |
| [`pr-review-claude-code-core-c01-r4-qualification-n2-r1-preflight`](pr-review-claude-code-core-c01-r4-qualification-n2-r1-preflight.json) | `ready_not_executed` | 純正相当workflow、PRR-C01/r4、v5 rating、subagent trace gate、repetition 1を固定 |
| [`pr-review-claude-code-core-c01-r4-qualification-n2-r2-preflight`](pr-review-claude-code-core-c01-r4-qualification-n2-r2-preflight.json) | 実行条件の履歴 | `Agent`許可とcollector依存を修正したrun 31263713165はレビュー品質を満たしたが、実並列を確認できず`measurement_incomplete` |
| [`pr-review-claude-code-core-c01-r4-qualification-n2-r3-preflight`](pr-review-claude-code-core-c01-r4-qualification-n2-r3-preflight.json) | 実行条件の履歴 | project設定がartifactから除外され、run 31265402558はreviewer開始前に`execution_failed` |
| [`pr-review-claude-code-core-c01-r4-qualification-n2-r4-preflight`](pr-review-claude-code-core-c01-r4-qualification-n2-r4-preflight.json) | 実行条件の履歴 | run 31265761721で実並列と権限境界は成立したが、required findingをmissして`quality_failed` |
| [`pr-review-workflow-free-c01-r4-calibration-n2-r1-preflight`](pr-review-workflow-free-c01-r4-calibration-n2-r1-preflight.json) | `ready_not_executed` | Free prompt、同じ入力・権限・root model、3 KPI、N=2、品質missで停止しない条件を固定 |
| [`pr-review-relationship-reviewer-sonnet-c01-r4-calibration-n3-r1-preflight`](pr-review-relationship-reviewer-sonnet-c01-r4-calibration-n3-r1-preflight.json) | 実行条件の履歴 | 関係レビュー役Sonnetの3反復を固定し、全件実行済み |
| [`pr-review-relationship-reviewer-opus-c01-r4-calibration-n3-r1-preflight`](pr-review-relationship-reviewer-opus-c01-r4-calibration-n3-r1-preflight.json) | 実行条件の履歴 | 関係レビュー役Opusの3反復を固定し、全件実行済み |
| [`pr-review-control-free-four-qualification-n1-r1-preflight`](pr-review-control-free-four-qualification-n1-r1-preflight.json) | 実行条件の履歴 | 初回4件はschema出力とcollector依存の移植漏れによりreview開始前に`execution_failed` |
| [`pr-review-control-free-four-qualification-n1-r2-preflight`](pr-review-control-free-four-qualification-n1-r2-preflight.json) | `ready_not_executed` | 初回4件のschema出力とcollector依存の移植漏れだけを直すenvironment recoveryを固定 |

r1は新インスタンス登録前に固定された診断アーティファクトであり、profileまたはrating contractへ事後昇格しない。r2はr1を上書きせず、PRR-C01 N=2へ適用した。後続の仕様監査で機能仕様とBaseline admission gateの欠落を確認したため、r2の`qualification_ready`は現在の実行許可ではない。既存JSONを上書きせず、[`diagnostic再分類receipt`](../results/pr-review-core-r2-diagnostic-reclassification_2026-08-08.md)で現在解釈を固定する。

`baseline-input-mapping-r4`はr3で欠けていたmodel-visibleな規則identityを補った一方、旧CoreがAnthropicの[`code-review` plugin](https://github.com/anthropics/claude-code/blob/2bb60696142b493eafaeacfe00eac51d16c50c4f/plugins/code-review/commands/code-review.md)のproducer構成とissue検証段階を移植していないことを固定した。新Baselineは`baseline-measurement-boundary-r2`、独立監査済みPRR-C01/r4、新profileとpreflightへbindした。preflightは実行許可ではなく、外部実行は別に発行する。
