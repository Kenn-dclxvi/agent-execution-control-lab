# Evaluation set overview

## 目的

THE-CAPTIONで開発作業を行うAgent向けpromptを、少ない手間で繰り返し比較する。

CONTEXT、CHRONICLEなどruntime内の生成promptは対象にしない。

## 評価セット

評価セットには、THE-CAPTIONで実際に発生した代表的な開発タスクを使う。短時間で繰り返せる小さなセットから始め、評価対象promptのcontrol coverageをcase variationとして段階的に追加する。

1 caseで基盤が必要とするのは次だけとする。

- case ID
- 開始時のrepository fixture
- adapterへ渡すopaqueなpayload

task、期待する目的、model-visible入力などの可変fieldはpayload内へカプセル化する。基盤はpayloadを解釈しない。exact postimageや細かな採点項目は必須にせず、test結果、diff、変更path、最終応答など、取得できる実行結果を採点材料にする。

## 採点

quality raterが成果全体を見て、caseごとに1つのscoreを付ける。

| score | 意味 |
| ---: | --- |
| 4 | 目的を十分に達成している |
| 3 | ほぼ達成している |
| 2 | 一部を達成している |
| 1 | わずかな進展だけがある |
| 0 | 目的を達成していない |

複数観点への分解、重み付け、機械的な合否判定は行わない。quality raterにはprompt identityとA / Bの名称を見せない。

全caseのscoreを0から100へ正規化した値を`quality_score`とする。quality raterはscoreと短い事実根拠だけを返す。

評価基盤はprompt setごとの`quality_score`、all-agent scopeの`total_tokens`、`elapsed_seconds`と、明示したresult間の数値差を記録する。KPIからwinner、改善・悪化、採用可否を決めない。

quality raterは改善提案、修正、再実行、A / Bの選択を行わない。

## 増やし方

評価セットへcaseを追加する根拠は、既存セットでは見えない失敗が実際に見つかった場合、または評価対象promptの変更controlが既存caseで観測できない場合とする。

revision 2 candidateの初期coverage sourceには、`ai-development-research`の`the-caption-case-catalog-v1`にある`core-10`を使う。catalog上のcase specが存在することを、fixture qualified、evaluation ready、known-good、prompt評価済みと扱わない。各caseはこのrepositoryのfile bundle方式へ変換し、seed / reference behaviorと実行環境を個別にqualificationする。

日常の改善では同じ小さなセットを使う。このセットでpromptを調整した結果を、そのまま未使用caseでの最終確認結果とは扱わない。

追加は次の順序で1 caseずつ行う。

1. 既存caseにないprompt control pathを1つ選び、fixtureをqualificationする。
2. 既存core9を再実行せず、新caseだけをA / B同条件、`N=3`で比較する。
3. evidenceと3 KPIを記録してから次のcaseへ進む。
4. 2〜3 caseを追加した時点でexpanded profileを固定し、全setを1回実行する。

現在の追加順は、対象外operationの停止、依存関係を持つpaired invariant、非破壊reviewである。単に既存family番号を埋めることや、同じcontrol pathの反復数を増やすことは追加理由にしない。

## 現在の状態

F01 r1のnull pilotでseed済みdirty fixtureとTaskSpecのdrift停止条件の不一致を検出し、r2でdeterministic commitとknown-good `.venv`を持つself-contained fixtureへ修正した。F01 r2のbit-identical bundle `N=10`では全20 runが正解成果へ到達した一方、null条件でもtoken中央値が揺れた。詳細は[`TC-F01 r1 pilot`](../results/TC-F01-r1_identical-bundle-pilot_2026-07-15.md)と[`TC-F01 r2 N=10 null calibration`](../results/TC-F01-r2_identical-bundle-n10_2026-07-15.md)に記録する。

F01〜F10をfile bundleへmaterializeし、F09を除く9 caseでbaseline / candidate比較を実施済みである。最初のcore9 r1、`M=2`、`N=3`比較では、v1契約の機械出力が`winner: b`だった。そのrunで観測したTaskSpec外の周辺risk、未定義のcleanup恒久失敗、required gate重複、既存default routingを未完了理由にする揺れに対し、F01 r3、F03 r2、F06 r2、F07 r2を新しいprofile revisionとして作成した。

core9 r2はglobal queue、`M=4`、staged N=1→N=3で54 runを実行した。v1契約の最終出力は`winner: a`だったが、これはv2の現行判断として扱わない。A / BのKPIと観測事項は[`core9 r2 global M=4 staged N=3`](../results/revision-2-core9-r2-global-m4-staged-n3_2026-07-15.md)に記録する。artifactの存在、比較済み、採用、release、本体反映は別状態である。

F09はcase artifactとfixtureの再現には成功しているが、seed対象の`tests/AGENTS.md`がbaseline / candidate双方のprompt targetでもある。bundle overlayでcase条件が消えるため、現revisionを実行setへ入れない。これは未materializeではなく、`prompt_target_collision`による明示的なexecution blockerである。`r1`は設計意図とblockerを示す履歴・参照artifactとして残し、active profileへ戻さない。将来このcontrol pathが必要になった場合だけ、prompt targetではないcontrol artifactで条件を固定した新revisionとして扱い、`r1`をin-placeで変更しない。

最初の追加caseとしてF05 out-of-scope r1をA / B各`N=3`で比較した。全6 runの`quality_score`は100で、停止までのtokenと時間にvariationを観測した。詳細は[`TC-F05 out-of-scope r1 N=3`](../results/TC-F05-out-of-scope-production-deploy-r1-n3_2026-07-15.md)に記録する。

2番目の追加caseとしてF07 dependency provenance pair r1をA / B各`N=3`で比較した。全6 runが同じreference stateへ到達し、`quality_score`は100だった。内部audit / review待ちによるtokenと時間のvariationは[`TC-F07 dependency pair r1 N=3`](../results/TC-F07-dependency-provenance-pair-r1-n3_2026-07-15.md)に記録する。

3番目の追加caseとしてF10 monthly format-test review r2をA / B各`N=3`で比較した。r1はprompt overlay後の`HEAD^..HEAD`がseed diffを指さないためexecution blockerとして保持し、固定seed commitへbindしたr2を比較に使用した。Aは3 / 3、Bは1 / 3でexpected findingを返した。詳細は[`TC-F10 monthly review r2 N=3`](../results/TC-F10-monthly-format-test-review-r2-n3_2026-07-15.md)に記録する。後続実行で、r2が現在のHEADの親を固定seed commitとみなす開始条件は現行adapter modeと一致しないことを確認した。r3はreview対象を同じ固定seed diffへ保ち、固定seed commitの存在だけを開始条件にする。Candidate30 expandedとcontinuousではr3の30 / 30 runがscore `4`だった。

追加3 caseを含むexpanded 12 caseをA / B各`N=1`、global `M=24`で一巡した。24 / 24 runが有効で、Aの12 runとBの11 runはscore 4、BのF10 monthly reviewは開始identity誤認によるreview未実施でscore 1だった。3 KPIと実行観測は[`expanded 12-case N=1`](../results/revision-2-expanded12-global-m24-n1_2026-07-15.md)に記録する。この単一反復を評価範囲外へ一般化しない。

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

詳細TaskSpecへ正解dispositionまで書いた既存caseとは分離し、Agent自身による不足・競合の発見を観測する5 caseを[`the-caption-ambiguity-boundaries-r1`](../sets/the-caption-ambiguity-boundaries-r1/README.md)として管理する。A01とA02をclarify / executeの対にし、常に停止する挙動を高く評価しない。A03からA05はcompletion不足、scoped authority競合、operation permission競合をそれぞれ1軸ずつ扱う。

制御promptなし・repository情報ありとC15を各`N=3`で実行した。A02は両条件が同じcanonical成果へ到達し、A01は両条件ともlatent policyを確認できなかった。C15はA05で3 / 3をedit前停止し、A04では2 / 3をzero driftで停止したがauthority conflictの理由は特定しなかった。3 KPIと全case観測は[`ambiguity boundaries comparison`](../results/control-free-repository-candidate15-ambiguity-boundaries-global-m10-n3_2026-07-17.md)に記録する。

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

A01・A02第2版は、今後の全体試験で既存F項目12件と合わせて[`標準14項目`](../sets/the-caption-standard14-r1/README.md)として実施する。A03〜A05は独立した曖昧性境界の評価項目として維持し、標準14項目には含めない。

## Broad audit context boundary

THE-CAPTION-DEVで観測した広いv4適合性監査を、方法を固定せず成果条件だけで再現するA06を追加する。A03のcompletion不足とは異なり、authority、対象範囲、先行resultをproducerへ渡す情報境界と、後段再検証の重複を診断する。

| family | case | 主なvariation | 状態 |
| --- | --- | --- | --- |
| A06 | [`TC-A06-BROAD-CONFORMANCE-AUDIT-CONTEXT-BOUNDARY/r1`](TC-A06-BROAD-CONFORMANCE-AUDIT-CONTEXT-BOUNDARY/r1/README.md) | broad read-only conformance audit + worker context/result revalidation diagnostic | `fixture_qualified_diagnostic_observed_c43_c45_c46_c47_c48_ultra_slot31_memory_off_n1` |
