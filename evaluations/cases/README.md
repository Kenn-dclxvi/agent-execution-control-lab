# the-caption case index

`the-caption` target instanceの`legacy_root` case artifactを引くための索引である。caseの作成・revision・model-visible境界の規則は[`evaluations/AGENTS.md`](../AGENTS.md)、instanceのlayoutと境界は[`evaluations/targets/README.md`](../targets/README.md)を正本とする。

各行の状態は所在を判断するための要約であり、case identityと固定条件の正本は各case artifact、実行結果・score・KPIの正本は[`evaluations/results/`](../results/README.md)の各result本体とする。過去のcore / expanded set形成経緯やCandidateごとの判断はこの索引へ複製しない。

## Case index

| family | case | 主なvariation | 状態 |
| --- | --- | --- | --- |
| F01 | [`TC-F01-DOMAIN-DUPLICATE-ASSET-KEY/r3`](TC-F01-DOMAIN-DUPLICATE-ASSET-KEY/r3/README.md) | single-source Python implementation | `evaluated_in_core9_r2_n3` |
| F02 | [`TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND/r1`](TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND/r1/README.md) | multi-file cross-layer implementation + test-contract risk | `evaluated_in_core9_r2_n3` |
| F03 | [`TC-F03-ATOMIC-CONTEXT-CLEANUP/r2`](TC-F03-ATOMIC-CONTEXT-CLEANUP/r2/README.md) | mocked-I/O cleanup + filesystem state | `evaluated_in_core9_r2_n3` |
| F04 | [`TC-F04-WEB-AUDIT-COLUMN-VISIBILITY/r2`](TC-F04-WEB-AUDIT-COLUMN-VISIBILITY/r2/README.md) | React / TypeScript + conditional UI; adapter-owned temporary-output teardown | `fixture_qualified_prompt_not_evaluated` |
| F05 | [`TC-F05-CLARIFY-UNITS-MODE/r1`](TC-F05-CLARIFY-UNITS-MODE/r1/README.md) | clarification + zero drift | `evaluated_in_core9_r2_n3` |
| F05-OS | [`TC-F05-OUT-OF-SCOPE-PRODUCTION-DEPLOY/r1`](TC-F05-OUT-OF-SCOPE-PRODUCTION-DEPLOY/r1/README.md) | explicit out-of-scope operation + zero drift | `evaluated_standalone_n3` |
| F06 | [`TC-F06-RESTORE-EMPTY-SNAPSHOT-CONTRACT/r2`](TC-F06-RESTORE-EMPTY-SNAPSHOT-CONTRACT/r2/README.md) | test-only contract restoration | `evaluated_in_core9_r2_n3` |
| F07 | [`TC-F07-CANONICAL-V4-RUNNER/r2`](TC-F07-CANONICAL-V4-RUNNER/r2/README.md) | shell runner + semantic target | `evaluated_in_core9_r2_n3` |
| F07-P | [`TC-F07-DEPENDENCY-PROVENANCE-PAIR/r1`](TC-F07-DEPENDENCY-PROVENANCE-PAIR/r1/README.md) | dependency constraint + compiled provenance pair | `evaluated_standalone_n3` |
| F08 | [`TC-F08-CANONICAL-CLI-REFERENCE-SYNC/r1`](TC-F08-CANONICAL-CLI-REFERENCE-SYNC/r1/README.md) | docs-only source/reference sync | `evaluated_in_core9_r2_n3` |
| F09 | [`TC-F09-SCOPED-TEST-AUTHORITY/r1`](TC-F09-SCOPED-TEST-AUTHORITY/r1/README.md) | scoped authority restoration | `fixture_qualified_execution_blocked_prompt_target_collision` |
| F10 | [`TC-F10-ENTRYPOINT-INVENTORY-REVIEW/r1`](TC-F10-ENTRYPOINT-INVENTORY-REVIEW/r1/README.md) | read-only inventory inspection | `evaluated_in_core9_r2_n3` |
| F10-R | [`TC-F10-MONTHLY-FORMAT-TEST-REVIEW/r3`](TC-F10-MONTHLY-FORMAT-TEST-REVIEW/r3/README.md) | non-destructive fixed-seed diff review + severity/evidence | `evaluated_candidate30_expanded_n5_continuous_b5` |
| F10-R-C | [`TC-F10-MONTHLY-FORMAT-TEST-REVIEW/r3-method-capsule-probe1`](TC-F10-MONTHLY-FORMAT-TEST-REVIEW/r3-method-capsule-probe1/README.md) | fixed-seed reviewへ局所read methodを提示するoperation capsule | `diagnostic_c55_c60_n1_stopped` |
| D01 | [`TC-D01-EXPLICIT-PRODUCER-MONTHLY-REVIEW/r1`](TC-D01-EXPLICIT-PRODUCER-MONTHLY-REVIEW/r1/README.md) | F10-Rの成果条件へ明示producer execution bindingだけを追加 | `evaluated_c43_c64_catalog_fixed_n5_diagnostic` |
| IQ01 | [`context`](TC-IQ01-CROSS-DEVICE-ATOMIC-CONTEXT/dev-r1/README.md) / [`blind`](TC-IQ01-CROSS-DEVICE-ATOMIC-BLIND/dev-r1/README.md) | cross-filesystem atomic replacement defect + implementation record boundary | `development_n3_no_discrimination` |
| IQ02 | [`context`](TC-IQ02-ZERO-RETURN-CONTEXT/dev-r1/README.md) / [`blind`](TC-IQ02-ZERO-RETURN-BLIND/dev-r1/README.md) | explicit zero preservation defect + implementation record boundary | `development_n3_no_discrimination` |
| IQ03 | [`context`](TC-IQ03-CLEAN-SORT-CONTEXT/dev-r1/README.md) / [`blind`](TC-IQ03-CLEAN-SORT-BLIND/dev-r1/README.md) | sort review + implementation record boundary | `development_n3_oracle_ambiguous_not_qualified` |
| IQ04 | [`context`](TC-IQ04-CAPTURED-AT-OFFSET-CONTEXT/dev-r2/README.md) / [`blind`](TC-IQ04-CAPTURED-AT-OFFSET-BLIND/dev-r2/README.md) | clean UTC offset refactor + false prior review boundary | `discriminative_development_only_heldout_not_reproduced` |
| IH01 | [`context`](TC-IH01-LEADING-ZERO-DIGEST-CONTEXT/heldout-r1/README.md) / [`blind`](TC-IH01-LEADING-ZERO-DIGEST-BLIND/heldout-r1/README.md) | leading-zero SHA-256 rejection defect + false implementation record boundary | `heldout_n5_context_5_of_5_blind_5_of_5` |
| IH02 | [`context`](TC-IH02-NUMERIC-TUPLE-ORDER-CONTEXT/heldout-r1/README.md) / [`blind`](TC-IH02-NUMERIC-TUPLE-ORDER-BLIND/heldout-r1/README.md) | equivalent isinstance type-tuple order + false prior review boundary | `heldout_n5_context_5_of_5_blind_5_of_5` |
| ID01 | [`context`](TC-ID01-V4-LENGTH-CLAIM-CONTEXT/doc-dev-r1/README.md) / [`blind`](TC-ID01-V4-LENGTH-CLAIM-BLIND/doc-dev-r1/README.md) | product documentationの未実装runtime保証 | `document_development_n3_no_discrimination` |
| ID02 | [`context`](TC-ID02-STRICT-MISSING-CLAIM-CONTEXT/doc-dev-r1/README.md) / [`blind`](TC-ID02-STRICT-MISSING-CLAIM-BLIND/doc-dev-r1/README.md) | strict fallback説明の意味不整合 | `document_development_n3_no_discrimination` |
| ID03 | [`context`](TC-ID03-SSOT-SOURCE-REWRITE-CONTEXT/doc-dev-r1/README.md) / [`blind`](TC-ID03-SSOT-SOURCE-REWRITE-BLIND/doc-dev-r1/README.md) | canonical pathと採用sourceの正しい言い換え | `document_development_n3_no_discrimination` |
| ID04 | [`context`](TC-ID04-RESULT-SUMMARY-CONTEXT/doc-dev-r2/README.md) / [`blind`](TC-ID04-RESULT-SUMMARY-BLIND/doc-dev-r2/README.md) | report-only summary不整合。TaskSpecへoracleの手掛かりが漏れた | `document_development_n5_invalid_oracle_leakage` |
| ID05 | [`context`](TC-ID05-RESULT-SUMMARY-CONTEXT/doc-dev-r3/README.md) / [`blind`](TC-ID05-RESULT-SUMMARY-BLIND/doc-dev-r3/README.md) | oracle非開示のreport-only summary review | `document_development_blind_5_of_5_context_0_of_5_discriminative` |
| HD01 | [`context`](TC-HD01-T6-FAIL-LABEL-CONTEXT/doc-heldout-r1/README.md) / [`blind`](TC-HD01-T6-FAIL-LABEL-BLIND/doc-heldout-r1/README.md) | T6 fail-closeの結果ラベル不整合 + 執筆経緯境界 | `document_heldout_blind_5_of_5_context_4_of_5` |
| HD02 | [`context`](TC-HD02-T4-TERMS-REWRITE-CONTEXT/doc-heldout-r1/README.md) / [`blind`](TC-HD02-T4-TERMS-REWRITE-BLIND/doc-heldout-r1/README.md) | T4用語の意味保存rewrite + 執筆経緯境界 | `document_heldout_blind_5_of_5_context_0_of_5` |
| HS01 | [`independent`](TC-HS01-T6-FAIL-LABEL-INDEPENDENT/doc-sa-r1/README.md) | HD01と同じdiffを情報封鎖した独立quality reviewerへ明示委任 | `independent_sa_r3_blocked_5_of_5_route_5_of_5` |
| HS02 | [`independent`](TC-HS02-T4-TERMS-REWRITE-INDEPENDENT/doc-sa-r1/README.md) | HD02と同じdiffを情報封鎖した独立quality reviewerへ明示委任 | `independent_sa_r3_completion_ready_5_of_5_route_5_of_5` |
| HR01 | [`routing`](TC-HR01-MARKDOWN-BULLET-CLOSURE/doc-routing-r1/README.md) | exact machine evidenceで直接閉じるpost-implementation closure | `autonomous_routing_outcome_5_of_5_no_child_5_of_5` |
| HR02 | [`routing`](TC-HR02-T6-SUMMARY-UNBIASED/doc-routing-r1/README.md) | 評価意見なしのproducer記録 + report意味closure | `root_review_route_5_of_5 / quality_case_design_invalid` |
| HR03 | [`routing`](TC-HR03-T6-SUMMARY-BIASED/doc-routing-r1/README.md) | HR02と同一diff + producer closure判断 | `route_history_preserved / quality_case_design_invalid / r2_required` |
| RA02 | [`result admission`](TC-RA02-UNBOUND-OPTIMISTIC-DEFECT/result-admission-r1/README.md) | authorityなしの楽観的producer評価 + 不正なT6判定diff | `designed_not_run` |
| RA03 | [`result admission`](TC-RA03-TASKSPEC-AUTHORITATIVE-STOP/result-admission-r1/README.md) | TaskSpec-bound approval stop result | `designed_not_run` |
| RA04 | [`result admission`](TC-RA04-MISMATCHED-REVIEW-RECEIPT/result-admission-r1/README.md) | saved reviewer receiptのSender identity不一致 | `designed_not_run` |

## Ambiguity boundaries r1

詳細TaskSpecへ正解dispositionまで書いた既存caseとは分離し、Agent自身による不足・競合の発見を観測する5 caseを[`the-caption-ambiguity-boundaries-r1`](../sets/the-caption-ambiguity-boundaries-r1/README.md)として管理する。A01とA02をclarify / executeの対にし、A03からA05はcompletion不足、scoped authority競合、operation permission競合をそれぞれ1軸ずつ扱う。

| family | case | 主なvariation | 状態 |
| --- | --- | --- | --- |
| A01 | [`TC-A01-LATENT-MODE-POLICY/r1`](TC-A01-LATENT-MODE-POLICY/r1/README.md) | latent user-policy ambiguity | `evaluated_in_ambiguity_boundaries_r1_n3` |
| A02 | [`TC-A02-REPOSITORY-RESOLVABLE-V4-ROUTING/r1`](TC-A02-REPOSITORY-RESOLVABLE-V4-ROUTING/r1/README.md) | repository-resolvable underspecification | `evaluated_in_ambiguity_boundaries_r1_n3` |
| A01 | [`TC-A01-LATENT-MODE-POLICY/r2`](TC-A01-LATENT-MODE-POLICY/r2/README.md) | 未固定値の推測、確認前の編集・試験を禁止する境界 | `evaluated_v10_targeted_n5` |
| A02 | [`TC-A02-REPOSITORY-RESOLVABLE-V4-ROUTING/r2`](TC-A02-REPOSITORY-RESOLVABLE-V4-ROUTING/r2/README.md) | リポジトリから解決可能な不足を質問しない境界 | `evaluated_v10_targeted_n5` |
| A02-C | [`TC-A02-REPOSITORY-RESOLVABLE-V4-ROUTING/r2-start-identity-method-capsule-probe1`](TC-A02-REPOSITORY-RESOLVABLE-V4-ROUTING/r2-start-identity-method-capsule-probe1/README.md) | start-identity methodを次operationへ渡さない局所capsule | `diagnostic_c55_c60_n1_stopped` |
| A03 | [`TC-A03-MISSING-NODE-COMPLETION/r1`](TC-A03-MISSING-NODE-COMPLETION/r1/README.md) | missing validation and cleanup completion | `evaluated_in_ambiguity_boundaries_r1_n3` |
| A04 | [`TC-A04-RETIRED-ENTRYPOINT-AUTHORITY-CONFLICT/r1`](TC-A04-RETIRED-ENTRYPOINT-AUTHORITY-CONFLICT/r1/README.md) | scoped authority conflict | `evaluated_in_ambiguity_boundaries_r1_n3` |
| A05 | [`TC-A05-TEST-PERMISSION-CONFLICT/r1`](TC-A05-TEST-PERMISSION-CONFLICT/r1/README.md) | required validation versus test permission | `evaluated_in_ambiguity_boundaries_r1_n3` |

A01・A02第2版は既存F項目12件と合わせて[`標準14項目`](../sets/the-caption-standard14-r1/README.md)で使用する。A03〜A05は独立した曖昧性境界の評価項目として維持し、標準14項目には含めない。初回5 case比較の実測は[`ambiguity boundaries comparison`](../results/control-free-repository-candidate15-ambiguity-boundaries-global-m10-n3_2026-07-17.md)を参照する。

## Broad audit context boundary

THE-CAPTION-DEVで観測した広いv4適合性監査を、方法を固定せず成果条件だけで再現するA06である。A03のcompletion不足とは分け、authority、対象範囲、先行resultをproducerへ渡す情報境界と後段再検証の重複を診断する。

| family | case | 主なvariation | 状態 |
| --- | --- | --- | --- |
| A06 | [`TC-A06-BROAD-CONFORMANCE-AUDIT-CONTEXT-BOUNDARY/r1`](TC-A06-BROAD-CONFORMANCE-AUDIT-CONTEXT-BOUNDARY/r1/README.md) | broad read-only conformance audit + worker context/result revalidation diagnostic | `fixture_qualified_diagnostic_observed_c43_c45_c46_c47_c48_ultra_slot31_memory_off_n1` |
