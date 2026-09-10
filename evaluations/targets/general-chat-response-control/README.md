# 一般チャット応答制御

一般チャットの確認、根拠要求、部分回答、独立論点および完了判断を、一回応答のsemantic protocolで測るnamespaced targetである。

設計と進行順は[`一般チャット応答制御の評価系列設計 r1`](../../../docs/general-chat-response-control-series-design.md)を正本とする。

## アーティファクト

- [`target.json`](target.json): target identity
- [`cases/`](cases/README.md): model-visible Caseとmodel-invisible oracle
- [`sets/`](sets/README.md): 固定Case集合
- [`rating-contracts/`](rating-contracts/README.md): 品質採点
- [`calibration/`](calibration/README.md): AI grader panel pilot、任意の人間監査、評価統治および未見holdout
- [`prompts/`](prompts/README.md): baselineと後続Candidate
- [`profiles/`](profiles/README.md): 実行条件
- [`plans/`](plans/README.md): preflightとdispatch
- [`results/`](results/README.md): write-once result
- [`runtime/`](runtime/README.md): target固有のpreflight、実行、採点

## 状態

`measurement_qualified / local_slice_passed / c147_chat_coverage_incomplete / integrated_candidate_not_created / overall_evaluation_not_started / adoption_not_eligible / release_not_created / projection_not_authorized`

現行の上位判定は[`C147チャット向けcoverage評価 r1`](docs/c147-chat-coverage-assessment-r1.md)、局所結果は[`RequiredValueCarrier r1 評価記録`](docs/required-value-carrier-r1-evaluation.md)を参照する。r1からr3までの測定未成立resultと局所評価resultは置換せず履歴として保持する。

自然文採点の次方式は[`一般チャット自然文採点方式の選定 r1`](docs/semantic-grading-method-selection-r1.md)へ固定した。現行r1を変更せず、AI grader panel pilot、panel外AIによる不一致裁定、複数承認者による閾値固定、およびpilotと重複しないholdoutでの独立grader適格試験が完了するまでr2を有効化しない。人間監査はpilot開始条件ではなく、`human_aligned`を主張する場合の追加証拠である。
