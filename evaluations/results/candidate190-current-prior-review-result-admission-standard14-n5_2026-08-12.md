# Candidate190 current/prior review result admission Standard14 N=5

> **結果**: `70 / 70 valid / Score 4 = 70 / quality_passed / mechanism_failed / M7_stopped`

## 結論

Candidate190をCandidate176の保存済みStandard14 N=5 resultへ互換bindし、14ケースを各5件、合計70件発行した。70 / 70件がvalid、除外0件、Score `4 = 70`で、品質とartifact変更境界は満たした。

一方で、M7の機序条件は通過しなかった。Standard14のTaskSpecは`owner=independent ... check`をnon-machine riskの担当情報として示すだけで、独立review operationや独立producer executionを要求していない。それにもかかわらずCandidate190はF02の3件、F03の1件、F04の4件、合計8件でreview producerを起動した。子agentのread 37件はmachine-bound exit codeを持たず、Candidate176では0件だったcommand protocol violationが37件へ増えた。

したがってCandidate190のStandard14は、品質上は70 / 70 Score 4でも、`不要producer起動なし`を満たさず`mechanism_failed`である。結果を置き換えず保持し、M1の原因分析へ戻る。M8、採用、releaseおよびprojectionへ進まない。

## 互換性

- prompt: `the-caption-3ce91a4-current-prior-review-result-admission-r1`
- bundle SHA-256: `63d8a79139e2b1e89268455cf997ccf7bd078b37d1bf44e51e0079aa05bfc30c`
- reference result ID: `a0702207f03a4cb18c8b501329b74023`
- compatibility key: `cc0c022ac026b55c51597e82c4a7216d4b7fdf498250c6a299d24203f1027561`
- pool key: `4f894eb7973e77c12beec6bfb114d3039947c6b3c182aa474c14ad757ddf6ef9`
- selection ID: `df044c8c441443ecb025d5156c771a09`
- analysis ID: `cb8a73b6a7594f50a93501230bc10241`
- registered result ID: `333508e7f37545218bea8f71fc9d3d1c`
- result content SHA-256: `2cf13bb1d861558fda31922456608f7fbccd7063c9a32af6717553bb1faadaf1`
- raw root: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate190-current-prior-review-result-admission-v14-medium-standard14-n5-cli0146-20260812-r1`

最初のatomic planはcomparison preflightが許可しない`repetition_condition`を含んだため0件発行で停止し、当該fieldを除いた。次のpreflightはF01 fixture identity不一致で0件発行のまま停止した。Candidate176 resultへ実際にbindされた保存済みLayer 1へ直した後、互換条件を緩和せず70件を承認した。並列上限はM=24を維持した。

## 品質と機序の分離

| 判定 | Candidate176 | Candidate190 | 結論 |
|---|---:|---:|---|
| valid | 70 / 70 | 70 / 70 | 同等 |
| Score 4 | 70 / 70 | 70 / 70 | 同等 |
| command protocol violation | 0 | 37 | 退行 |
| violation affected run | 0 | 8 | 退行 |
| owner-producer診断適格 | 15 | 25 | 品質gateではなく参考値 |
| monthly numeric location exact | 5 / 5 | 4 / 5 | 1件は品質非影響の診断差 |

owner-producer evidenceはv14契約上`diagnostic_only`であるため、criterion ownerどおりのworker resultがない45件をScoreへ混ぜていない。逆に10件の`available`をそのまま成功とも扱わない。TaskSpecが独立producer executionを要求しないのに起動した8件を、不要producerとして機序失敗へ数えた。

37件の違反はすべて`descendant_rollout_tool_call`の`missing_machine_bound_exit_code`であり、F02、F03、F04の独立確認workerが行ったreadである。required validation自体は成功しており、品質監査のfailureは0件だった。

## 原因と修正境界

Candidate190の`PRODUCER_BINDING`はcriterion ownerだけでproducerを選ばないと述べていたが、`REVIEW_REQUIREMENT`の適用条件は「独立review criterion等が直接固定済み」という抽象表現だった。このため`owner=independent contract check`、`owner=independent state check`または`owner=independent source check`をreview controlの明示と解釈し、欠けているreview operation、allowed result kind、consumerおよびproducerを補完する経路が残った。

修正は、review適用に`reviewを必要な独立operationとして直接名指ししたこと`を要求し、criterion owner、non-machine risk、静的確認または独立確認の語列だけではreview operation、packet、producer、spawnおよびresultを作らないことに限定する。Candidate190の履歴は書き換えず、新しいprompt identityへ分離する。

## 一次証拠

- [登録result](333508e7f37545218bea8f71fc9d3d1c.json)
- [品質監査](candidate190-current-prior-review-result-admission-standard14-n5-audit-r1.json)
- [機序監査](candidate190-current-prior-review-result-admission-standard14-n5-mechanism-audit-r1.json)
- [評価profile](../profiles/candidate190-current-prior-review-result-admission-v14-reasoning-medium-standard14-global-m24-n5-cli0146-r1.json)
- [評価設計](../../docs/candidate190-current-prior-review-result-admission-standard14-n5-evaluation-design.md)
- [実行準備監査](../../docs/candidate190-current-prior-review-result-admission-standard14-n5-execution-preparation-audit.md)

## 状態

`M7_completed_failed / 70_valid / 70_score4 / unwanted_review_producer_8 / command_protocol_violation_37 / mechanism_failed / M1_reopened / M8_not_started / adoption_not_decided / release_not_created / projection_not_performed`
