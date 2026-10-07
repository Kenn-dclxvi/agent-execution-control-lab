# quality rating contract索引

`the-caption` legacy-rootのquality rating contract revisionを引くための索引である。revision固定、model-visible境界、過去resultの再採点禁止は[`evaluations/AGENTS.md`](../AGENTS.md)を正本とし、各revisionの採点条件は対応するcontract JSONを正とする。現行のプロファイルで使用するcontractは[`docs/prompt-comparison-workflow.md`](../../docs/prompt-comparison-workflow.md)と各profile identityで確認する。

## revision一覧

| revision | 主な変更軸 | 状態 |
| --- | --- | --- |
| [`owner-producer-quality-v1`](owner-producer-quality-v1.json) | criterion ownerに対応する独立producer resultをscore `4`の必要条件にする | 履歴 |
| [`owner-producer-quality-v2`](owner-producer-quality-v2.json) | required validation evidenceをrootから到達可能なdescendant sessionまで拡張 | 履歴 |
| [`owner-producer-quality-v3`](owner-producer-quality-v3.json) | evidence不足時もvalid runへ0〜3のscoreを返し、成果と証跡不足を分離 | 履歴 |
| [`owner-producer-quality-v4`](owner-producer-quality-v4.json) | all-agent command evidenceをv2へ更新しstructured command / continuationを収集 | 履歴 |
| [`owner-producer-quality-v5`](owner-producer-quality-v5.json) | command evidenceをv3へ更新しcustom `exec`のname / exit bindingを固定 | 履歴 |
| [`owner-producer-quality-v6`](owner-producer-quality-v6.json) | F05 clarificationのresponse evidenceをsemantic marker groupへ正規化 | 履歴 |
| [`owner-producer-quality-v7`](owner-producer-quality-v7.json) | command evidenceをv4へ更新し`### <name>`と`exit_code=0`のbindingを固定 | 履歴 |
| [`owner-producer-quality-v8`](owner-producer-quality-v8.json) | command evidence v5。attempt / success / failure / protocol violationとmeasurement incompleteを分離 | 履歴 |
| [`outcome-quality-owner-diagnostic-v9`](outcome-quality-owner-diagnostic-v9.json) | owner-producer evidenceをquality gateからdiagnosticへ分離 | 履歴 |
| [`outcome-boundary-owner-diagnostic-v10`](outcome-boundary-owner-diagnostic-v10.json) | model-visible TaskSpec / repository authorityから導ける成果・禁止・必須試験だけを採点 | 履歴 |
| [`outcome-semantic-location-owner-diagnostic-v11`](outcome-semantic-location-owner-diagnostic-v11.json) | F10 Monthlyの数値lineをquality必須条件からdiagnosticへ分離 | 履歴 |
| [`outcome-semantic-evidence-normalized-owner-diagnostic-v12`](outcome-semantic-evidence-normalized-owner-diagnostic-v12.json) | A01 / A02 / F10で再現したsemantic evidenceの偽陰性を正規化 | 履歴 |
| [`outcome-abstract-condition-preserving-owner-diagnostic-v13`](outcome-abstract-condition-preserving-owner-diagnostic-v13.json) | 抽象成果条件を非公開の特定commandへ具体化して必須化することを禁止 | 履歴互換 |
| [`outcome-terminal-state-evidence-owner-diagnostic-v14`](outcome-terminal-state-evidence-owner-diagnostic-v14.json) | v13を維持し、A01をresponse文面分類から`terminal-state-evidence/v1`へ切替 | 現行 |
| [`outcome-terminal-state-evidence-claude-collector-v1`](outcome-terminal-state-evidence-claude-collector-v1.json) | v14のケース規則を変えず、command証跡とproducer証跡のcollectorだけをClaude Code transcript用へ差し替える | Claude Code系列専用 |
| [`outcome-terminal-state-evidence-claude-collector-v2`](outcome-terminal-state-evidence-claude-collector-v2.json) | v1を維持し、F05 clarifyのfallback確認として英語の動詞形`fall back`系も受け付ける | Claude Code系列専用（現行） |

v14はv13以前と異なる互換条件であり、過去resultをv14で再採点したものとして扱わない。既存のv10〜v13プロファイルは履歴再現用として保持する。

`outcome-terminal-state-evidence-claude-collector-v1`はClaude Code実行系列だけで使う。ケース規則はv14と同じだが、証跡collectorが異なるためv14とは別の互換条件であり、Codex resultと同一比較へ入れない。

`outcome-terminal-state-evidence-claude-collector-v2`は、Claude Codeが英語で応答したときにF05の確認を取りこぼしていた採点規則の欠陥を直す。v14（Codex条件）の受理形は変更せず、Codexの判定はそのまま残す。v1で採点済みのClaude resultとLayer 3 ratingは書き換えず、v2での再判定は別の監査記録として保存する。v1とv2は別の互換条件である。

command / producer / terminal-state evidenceのcollector schemaとLayer 3実行手順は[`docs/evaluation-loop-manual.md`](../../docs/evaluation-loop-manual.md)および実装側のversioned contractを参照する。このREADMEへcollector実装の詳細を複製しない。
