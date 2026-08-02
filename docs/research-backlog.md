# 研究バックログ（状況索引）

研究項目を**未完了・保留**と**完了・停止**へ分け、着手判断と履歴確認のために一箇所へ集める索引。長期方針は[`future-roadmap.md`](future-roadmap.md)、系譜と観測は[`candidate-history.md`](candidate-history.md)を参照する。

この文書は索引であり、判定の正本ではない。各項目の状態・数値・停止理由は「正本」列のartifactを正とする。ここに載っていることは、着手済み・評価済み・採用予定のいずれでもない。

## 状況サマリー

### 未完了・保留

| 項目 | 現在状態 | 次の判断または再開条件 |
| --- | --- | --- |
| `CONTEXT`（`X1`） | ペンディング | A06はUltra制御用。Ultra条件で再検討する明示判断があった場合だけ再開 |
| `RECOVERY`（`R1 / R2`） | 未完了・効果未測定 | `environment_recovery_max>0`の正のrecovery scenarioを評価するか判断 |
| [Claude Code CLI executor系列](claude-code-cli-evaluation-adapter-design.md) | 保留・実装／pilot／本測定未着手 | 系列へ着手する明示判断とPhase 0の認証方式選択が揃った場合だけ再開 |
| 部分曖昧・長期タスクでの仕様確定境界（項目11） | 未着手・該当caseなし | 部分曖昧かつ複数段のcase familyと、誤停止・過剰問合せの採点条件を固定できた場合に着手 |
| model / CLI更新時の再測定範囲と費用記録（項目12） | 未着手 | 次のmodelまたはCLI更新時に、再実行するbaselineの範囲を事前固定する明示判断があった場合 |

### 完了・停止

| 項目 | 最終状態 | 完了・停止境界 |
| --- | --- | --- |
| `INDEPENDENCE`（`I1` = `F9`） | 対応なしで完了 | A / D追加runは行わない。`I1`起因の不要なoperation分割をfresh traceで観測した場合だけ別判断として再開 |
| [`Candidate82`](candidate82-producer-gate-deduplication-design.md) | `standard14_b20_evaluated / stopped` | B20で低頻度route非安定性を観測。採用以降へ進めない |
| [`Candidate83`](candidate83-delegation-value-boundary-design.md) | `targeted_f02_evaluated / stopped` | 品質通過、cost control未実証。追加評価以降へ進めない |
| [`Candidate84`](candidate84-delegation-marginal-value-boundary-design.md) | `targeted_f02_evaluated / stopped` | 品質通過、cost control mixed。追加評価以降へ進めない |
| [`Candidate85`](candidate85-planning-first-producer-selection-design.md) | `targeted_f02_f04_evaluated / stopped` | F04でtoken・elapsedがともに悪化。D01以降へ進めない |
| [`Candidate86`](candidate86-producer-plan-fast-path-design.md) | `targeted_f02_f04_d01_evaluated / stopped` | D01でtoken・elapsedがともに悪化。標準14以降へ進めない |
| [`Candidate87`](candidate87-adoption-decision.md) | `standard14_evaluated / not_adopted / stopped` | 品質差なし、集約token・elapsedともに増加。C81を維持し、release・本体反映へ進めない |
| [`Candidate88`](candidate88-parallel-worker-admission-design.md) | `targeted_f02_evaluated / stopped` | 逐次Workerを観測し、token・elapsedもともに悪化。F04以降へ進めない |
| [`Candidate89`](candidate89-dispatch-time-worker-admission-design.md) | `targeted_f02_evaluated / stopped` | dispatch gateが実発行順を制約できず、token・elapsedもともに悪化。F04以降へ進めない |
| [`Candidate90`](../evaluations/results/candidate81-candidate90-tool-output-ingress-boundary-v14-medium-f02-n5_2026-07-29.md) | `targeted_f02_evaluated / stopped` | 取得時projectionが0 / 5で、token・elapsedもともに悪化。F04以降へ進めない |
| [`Candidate91`](../evaluations/results/candidate81-candidate91-concise-output-ingress-v14-medium-f02-n5_2026-07-29.md) | `targeted_f02_evaluated / stopped` | 短文化でwrapper使用は増えたがstrict compliance 2 / 5、token・elapsedも悪化。prompt改訂とF04以降へ進めない |
| [`Candidate92`](../evaluations/results/candidate81-candidate92-bound-output-route-v14-medium-f02-n5_2026-07-29.md) | `targeted_f02_evaluated / stopped` | pre-command routeは5 / 5、capは3 / 5。read細分化でtoken・elapsedが悪化し、F04以降へ進めない |
| [`Candidate93`](../evaluations/results/candidate81-candidate93-result-classification-v14-medium-f02-n5_2026-07-29.md) | `targeted_f02_evaluated / stopped` | 3分類機構は0 / 5。KPI改善は帰属不能で、F04以降へ進めない |
| [`Candidate96`](../evaluations/results/candidate81-candidate96-successful-validation-result-projection-v14-medium-f02-n5-cli0146_2026-07-30.md) | `targeted_f02_evaluated / mechanism_gate_failed / stopped` | 5 / 5 score `4`だがsuccess projectionは0 / 5。KPI改善は狙った機構へ帰属できず、F04以降へ進めない |
| [`Candidate97 r1 / r2`](../evaluations/results/candidate81-candidate97-decision-round-closure-r2-v14-medium-f02-n5-cli0146_2026-07-30.md) | `targeted_f02_evaluated / quality_gate_passed / mechanism_gate_failed / stopped` | 長いr1はresult生成前に中止。短いr2は5 / 5 score `4`だがcompletion closure 0 / 5で、Standard14・B20・採用以降へ進めない |
| [`Candidate98`](../evaluations/results/candidate98-candidate104-staged-evidence-admission-v14-medium-standard14-n5-cli0146_2026-07-30.md) | `standard14_evaluated / quality_gate_passed / result_registered` | Standard14 N=5は70 / 70 score `4`。Candidate104の直接比較基準として保存済みresultを再利用 |
| [`Candidate99`](../evaluations/results/candidate99-decision-evidence-boundary-v14-medium-f07-canonical-n5-cli0146_2026-07-30.md) | `targeted_f07_evaluated / mechanism_gate_failed / result_not_registered / stopped` | 5 / 5 score `4`だが広い検索が4 / 5、履歴参照が1 / 5。全14 case Layer 1に対するF07 subsetのためLayer 4未登録。Standard14以降へ進めない |
| [`Candidate100`](../evaluations/results/candidate100-outcome-source-closure-v14-medium-f07-canonical-n5-cli0146_2026-07-30.md) | `targeted_f07_evaluated / mechanism_gate_failed / result_registered / stopped` | 5 / 5 score `4`、履歴参照なし5 / 5だが、広い検索なしは1 / 5。F07 coverageでLayer 4登録済み。Standard14、B20、採用以降へ進めない |
| [`Candidate101`](../evaluations/results/candidate101-additional-investigation-trigger-v14-medium-f07-canonical-n5-cli0146_2026-07-30.md) | `targeted_f07_evaluated / mechanism_gate_failed / result_registered / stopped` | 5 / 5 score `4`だが広い検索が5 / 5、履歴参照が1 / 5。追加調査の発火条件は0 / 5で、Standard14、B20、採用以降へ進めない |
| [`Candidate102`](../evaluations/results/candidate102-prechange-evidence-freeze-v14-medium-f07-canonical-n5-cli0146_2026-07-30.md) | `targeted_f07_evaluated / mechanism_gate_failed / result_registered / stopped` | 5 / 5 score `4`、履歴参照0 / 5、広い検索なし2 / 5。内部evidence固定だけでは事後補完を防げず、Standard14、B20、採用以降へ進めない |
| [`Candidate103`](../evaluations/results/candidate103-prechange-evidence-receipt-v14-medium-f07-canonical-n5-cli0146_2026-07-30.md) | `targeted_f07_evaluated / mechanism_gate_failed / result_registered / stopped` | 5 / 5 score `4`だが、実行票先行4 / 5、履歴参照なし4 / 5、広い検索なし0 / 5。判断項目はTaskSpecに固定済みだったが、各判断の証拠範囲を実行票で広げられたため、Standard14、B20、採用以降へ進めない |
| [`Candidate104`](../evaluations/results/candidate98-candidate104-staged-evidence-admission-v14-medium-standard14-n5-cli0146_2026-07-30.md) | `standard14_evaluated / quality_gate_passed / adoption_not_decided` | targeted A02 / F07 10 / 10とStandard14 70 / 70がscore `4`。互換C98比token中央値-6.48%、elapsed中央値-9.77%。B20、release、本体反映は未実施 |
| [`Candidate105`](../evaluations/results/candidate104-candidate105-validation-terminal-return-v14-medium-standard14-n5-cli0146_2026-07-30.md) | `standard14_evaluated / quality_gate_passed / terminal_return_improved_not_complete / adoption_not_decided` | targeted停止後にユーザーがStandard14だけ再開。70 / 70 score `4`、C104比token中央値`+0.70%`、elapsed中央値`+2.65%`。F03再取得なしは2 / 5から4 / 5へ改善したが完全ではない。B20、採用以降は未判断 |
| [`Candidate106`](../evaluations/results/candidate104-candidate106-validation-terminal-wait-v14-medium-f03-f08-continuous-n5-b20-cli0146_2026-07-30.md) | `targeted_f03_f08_b20_evaluated / quality_gate_passed / route_stability_gate_failed / cost_no_significant_difference / stopped` | F03・F08 B20は両promptとも200 / 200 score `4`。F03のrequired validation間messageなしはC104 89 / 100、C106 99 / 100だが、C106で対象経路が1件再発。cost有意差なし。Standard14 B20、採用以降へ進めない |
| [`Candidate107`](../evaluations/results/candidate106-candidate107-validation-wrapper-reentry-closure-v14-medium-standard14-atomic-n5-cli0146_2026-07-31.md) | `targeted_f03_b20_evaluated / standard14_evaluated_by_explicit_reopen / quality_gate_passed / outer_deadline_gate_failed / stopped` | 明示再開したStd14 atomic N=5は70 / 70 score `4`。C106比token中央値`-10.65%`、elapsed`+8.53%`のtradeoff。F03 B20のouter deadline違反4 / 100件は維持 |
| [`Candidate108`](../evaluations/results/candidate107-candidate108-validation-ticket-terminal-closure-v14-medium-standard14-atomic-reuse-n5-cli0146_2026-07-31.md) | `targeted_f03_evaluated / standard14_evaluated / quality_gate_passed / mechanism_gate_passed / adoption_not_decided` | F03 gate通過。Std14はF03 5 runを再利用し65 runだけ追加、70 / 70 score `4`。C107比token`+15.75%`、elapsed`+3.69%` |
| [`Candidate109`](../evaluations/results/candidate108-candidate109-validation-ticket-outer-wait-closure-v14-medium-f03-atomic-n5-cli0146_2026-07-31.md) | `targeted_f03_evaluated / prompt_design_boundary_failed / stopped` | F03は5 / 5 score `4`、C108比token`-15.97%`、elapsed`-16.43%`だが、outer yield最大値という方法指定がprompt設計方針に反するため停止 |
| [`Candidate110`](../evaluations/results/candidate110-validation-ticket-decision-boundary-v14-medium-f03-atomic-n5-cli0146_2026-07-31.md) | `targeted_f03_evaluated / quality_gate_passed / targeted_cost_both_lower / control_not_demonstrated / stopped` | C108比token`-1.31%`、elapsed`-6.99%`だがterminal前model再入なしは2 / 5。KPI低下を制御効果へbindできず、Std14はslot未発行で撤回 |
| [`Candidate111`](../evaluations/results/candidate111-validation-ticket-model-return-boundary-v14-medium-f03-atomic-n5-cli0146_2026-07-31.md) | `targeted_f03_evaluated / quality_gate_passed / targeted_cost_both_lower / model_return_gate_failed / stopped` | C108比token`-0.99%`、elapsed`-9.34%`。model return horizonを4 / 5件が明示し、2件が判断なしの継続待機だけのため再入。中間messageは0件だがStd14へ進めず停止 |
| [`Candidate112`](../evaluations/results/candidate108-candidate112-evidence-admission-scheduling-boundary-v14-medium-a01-a02-f01-atomic-n5-cli0146_2026-07-31.md) | `targeted_a01_a02_f01_evaluated / quality_gate_passed / aggregate_cost_tradeoff / evidence_scheduling_not_demonstrated / stopped` | 15 / 15 score `4`。C108比token`+3.53%`、elapsed`-3.10%`。case別token中央値は全件低下したが、tool call / model stepが各`+16`件で狙った逐次model return削減は不成立 |
| [`Candidate113`](../evaluations/results/candidate108-candidate113-explicit-authority-delegation-v14-medium-a01-a02-atomic-n5-cli0146_2026-07-31.md) | `targeted_a01_a02_evaluated / quality_gate_passed / descriptive_cost_lower / authority_admission_not_demonstrated / stopped` | 10 / 10 score `4`。C108比の固定schema中央値はtoken`-26.28%`、elapsed`-18.90%`だが、A01の狙ったrouteは0 / 5。新しいsemantic labelを重ねず、C108とcontrol-free系traceから既存predicate削除の可否を先に調べる |
| [`Candidate114`](../evaluations/results/candidate108-candidate114-spec-ready-evidence-phase-boundary-v14-medium-a01-a02-f01-atomic-n5-cli0146_2026-07-31.md) | `targeted_a01_a02_f01_evaluated / a01_mechanism_passed / quality_gate_failed / stopped` | A01は5 / 5で追加探索なしのclarificationへ収束。A02は1 / 5がauthority path未記載を理由に誤停止し、14 / 15 score `4`のためStandard14へ進めない |
| [`Candidate115`](../evaluations/results/candidate108-candidate115-authority-location-discovery-v14-medium-a01-a02-atomic-n5-cli0146_2026-07-31.md) | `targeted_a01_a02_evaluated / a02_mechanism_passed / quality_gate_failed / stopped` | A02は5 / 5へ戻ったが、A01は4 / 5が未確認実装でscore `0`。authority条件のprompt微修正は続けず、TaskSpec/schema境界の別実験として再設計する場合だけ再開 |
| [`Candidate116`](../evaluations/results/candidate108-candidate116-outcome-implementation-boundary-v14-medium-standard14-atomic-reuse-n5-cli0146_2026-07-31.md) | `standard14_evaluated / quality_gate_passed / mechanism_gate_passed / token_improved / elapsed_near_flat_slightly_higher / adoption_not_decided` | outcome確定とimplementation解決の分離によりA01 / A02は各5 / 5で意図どおり制御。単独M=24の正規Std14は70 / 70 score `4`、C108比token`-9.26%`、elapsed`+0.25%`。採用は別判断 |
| [`Candidate117`](../evaluations/results/candidate116-candidate117-implementation-authority-delegation-v14-medium-standard14-atomic-reuse-n5-cli0146_2026-07-31.md) | `standard14_evaluated / quality_gate_passed / targeted_mechanism_passed / token_regressed / elapsed_improved / reentry_shifted_to_general_cases / stopped` | targeted A01 / A02 / F01は15 / 15、Std14は70 / 70 score `4`。C116比でA02再入35→25だが、全体再入272→285、token`+12.02%`、elapsed`-8.52%`。authority admissionの微修正は続けない |
| [`Candidate118`](../evaluations/results/candidate116-candidate118-implementation-bind-terminal-closure-v14-medium-standard14-atomic-reuse-n5-cli0146_2026-07-31.md) | `standard14_evaluated / quality_gate_passed / mechanism_gate_passed / token_regressed / elapsed_improved / residual_validation_reentry / adoption_not_decided` | implementation bindを変更前evidenceのterminal resultにする。A02 `N=20`は20 / 20 score `4`、bind後再入0件。Std14は70 / 70 score `4`、C116比token`+7.44%`、elapsed`-14.37%`。後続の[`残差分析`](candidate118-residual-validation-reentry-analysis.md)はvalidationのnonterminal返却とmodel再入を主要因として支持する。次のprompt-only候補はC118の品質・機構を維持し、C107がprompt差分だけで到達したtoken中央値`1,523,137`以下を目標KPIとする。外部executor対応は本backlogへ追加しない |
| [`Candidate119`](../evaluations/results/candidate118-candidate119-validation-predicate-method-boundary-v14-medium-a01-a02-f01-atomic-n5-cli0146_2026-07-31.md) | `targeted_a01_a02_f01_evaluated / quality_gate_passed / postchange_method_boundary_passed / prechange_terminal_closure_failed / a02_cost_target_failed / stopped` | 15 / 15 score `4`。A02の変更後validation-method探索は4 / 5→0 / 5、token中央値はC118比`-34.10%`。ただしbind後・変更前再入が1 / 5件発生し、C107 case目標を`18.79%`上回った。次はC119のmethod境界を保持し、変更前evidence admissionを別predicateとして検証する。N=20 / Std14は未作成 |
| [`Candidate120`](../evaluations/results/candidate119-candidate120-implementation-edit-ticket-closure-v14-medium-a01-a02-f01-atomic-n5-cli0146_2026-07-31.md) | `targeted_a01_a02_f01_evaluated / quality_gate_passed / edit_ticket_closure_failed / aggregate_cost_both_higher / stopped` | 15 / 15 score `4`、変更後method探索0 / 5は維持。確定表明後・変更前再入は2 / 5へ増え、A02 tokenはC119比`+47.90%`。edit-ticket labelの微修正は続けず、C119の成功部分と失敗部分を保存traceとして保持する |
| [`Candidate121`](../evaluations/results/candidate118-candidate121-evidence-request-scope-closure-v14-medium-a01-a02-f01-f02-atomic-n5-cli0146_2026-07-31.md) | `targeted_a01_a02_f01_f02_evaluated / quality_gate_passed / a02_prechange_terminal_closure_passed / postchange_method_boundary_failed / f02_locator_scope_failed / f02_cost_target_failed / stopped` | 20 / 20 score `4`。A02変更前再入0 / 5、token中央値`143,419`はC119比`-3.85%`。ただし変更後method探索1 / 5、F02 token`209,379`は目標比`+21.03%`。後続の[`F02 evidence route分析`](candidate121-f02-evidence-route-analysis.md)ではbytes、target数、invocation数の単独制御を棄却し、exact target setかつ同一predicateの場合だけ一つの変更前evidence waveへ閉じる次仮説を残した |
| [`Candidate122`](../evaluations/results/candidate118-candidate122-prechange-evidence-wave-closure-v14-medium-standard14-atomic-reuse-n5-cli0146_2026-07-31.md) | `standard14_evaluated / token_target_passed / elapsed_below_candidate107 / quality_gate_failed / f04_incomplete_content_false_stop / result_registered / stopped` | targeted 20 / 20 score `4`後に既存runを再利用してStandard14を完了。70件はscore `4 / 2 = 69 / 1`、token中央値`1,403,840`でC107目標比`-7.83%`。F04の1件が同じread可能targetの取得範囲不足をterminal missingと誤分類した。次はincomplete contentだけに同一targetの限定continuationを許す |
| [`Candidate123`](../evaluations/results/candidate122-candidate123-preterminal-result-round-closure-v14-medium-a01-a02-f01-f02-atomic-n5-cli0146_2026-07-31.md) | `targeted_a01_a02_f01_f02_evaluated / quality_gate_failed / a01_clarification_terminal_passed / a02_prechange_round_gate_failed / f02_start_identity_classification_failed / result_registered / stopped` | 20 / 20 valid、score `4 / 2 = 19 / 1`。F02の1件が正常なdetached HEADをidentity未確定と誤分類して停止した。A02 result round 1回以下も3 / 5。C107 A02中央値run自体が複数roundだったため、round数だけをC107 cost到達条件とする仮説を棄却し、C122の通過状態へ戻る |
| [`Candidate124`](../evaluations/results/candidate122-candidate124-incomplete-content-continuation-v14-medium-a01-a02-f01-f02-f04-atomic-n5-cli0146_2026-07-31.md) | `targeted_a01_a02_f01_f02_f04_evaluated / quality_gate_failed / f04_continuation_scope_incomplete / f02_content_wave_regressed / f02_cost_target_failed / result_registered / stopped` | 25 / 25 valid、score `4 / 2 = 23 / 2`。F04は2件が620行までのcontinuationで必要criterionを取得できずfalse stop。F02も追加read 2 / 5、content wave 3 / 5、token中央値`188,908`。次は単一editable target所有とcriterion-complete scopeを同時条件にする |
| [`Candidate125`](candidate125-adoption-decision.md) | `evaluated / adopted / release_projected / runtime_projected / model_axis_n5_evaluated / n100_stopped_at_registered_pool_n30` | Sol一次resultは70 / 70 score `4`、token中央値`1,401,225`、A02 N=20 bind後再入0件。後続model-axis N=5はTerra 68 / 70 score `4`、Luna 67 / 70 score `4`でSol以外は未採用。2026-08-01の[`N=100追試`](../evaluations/results/candidate125-criterion-complete-single-target-continuation-v14-medium-standard14-atomic-reuse-n100-stopped-at-pool-n30-cli0146_2026-08-01.md)はregistered poolを各case30件まで拡張し、F04 score `2`を5件確認した。N=50 partial batchは未採点・未登録で中断し、N=30 selection resultも未作成。既存adoption / projection stateは維持 |
| [`Candidate126`](candidate126-criterion-bound-change-input-design.md) | `targeted_f04_n5_evaluated / n20_overexecuted_evidence_preserved / quality_gate_failed / stale_hunk_suppressed / required_edit_suppressed / result_registered / stopped` | C125 F04の不要hunkを対象に`change_input_ready`を追加。初段N=5はscore `4 / 2 = 3 / 2`。`colSpan`変更とstale operandは0 / 5だったが、2件が必要な`hasAuditKey`変更とNode validationも抑止した。先行発行済みN=20は追加証拠として保持する。F02 / F07、Standard14、採用以降へ進めない |
| [`Candidate127`](../evaluations/results/candidate127-failed-change-salvage-v14-medium-f02-f04-f07-sequential-atomic-n100-stopped-at-f02-n29-cli0146_2026-08-01.md) | `standard14_n5_quality_passed / f02_n29_stability_quality_gate_failed / stopped_before_f04_f07 / result_registered / adoption_not_decided` | 初段F04、F02 / F07 preservation、Standard14 N=5は全件score `4`。後続の逐次N=100追試はF02追加24件でscore `4 / 2 = 22 / 2`となり停止。正式F02 N=29は`27 / 2`。2件は相互に必要なupdater変更を適用できず部分成果。F04 / F07追加slotは0件。採用、release、本体反映へ進めない |
| [`Candidate128`](../evaluations/results/candidate125-candidate128-required-effect-closure-v14-medium-f02-f04-f07-atomic-n5-cli0146_2026-08-01.md) | `targeted_f02_f04_f07_n5_evaluated / quality_gate_passed / required_effect_closure_observed / aggregate_cost_both_higher / standard14_not_started / adoption_not_decided` | C125直系。F02・F04・F07を一つのbatchで各N=5実施し15 / 15 score `4`。F02両effect、F07 pairは各5 / 5。F04は初回失敗3件を追加readなし・一回reworkで回復し、`colSpan`変更0件。C125比token`+21.34%`、elapsed`+10.01%` |
| [`Candidate129`](candidate129-unsatisfied-effect-change-admission-design.md) | `targeted_f04_n5_evaluated / quality_gate_failed / false_stop_3_of_5 / stopped` | C128直系。F04 N=5はinitial apply failureと`colSpan`再変更を0 / 5へ抑えたが、未観測`colSpan`が観測済み`hasAuditKey`変更まで拒否するfalse stopを3 / 5で発生させ、score `4 / 1 = 2 / 3`。F02、F07、Standard14へ進めない |
| [`Candidate130`](candidate130-focused-criterion-continuation-design.md) | `targeted_f04_n5_evaluated / quality_gate_failed / focused_continuation_0_of_5 / stopped` | C128直系。Evidence coverageだけを対象にfocused symbol contextを優先したが、F04 5件すべてが全残存contentを選択。score `4 / 1 = 2 / 3`、false stop 3 / 5。F02、Standard14へ進めない |
| [`Candidate131`](candidate131-criterion-anchor-continuation-design.md) | `targeted_f04_n29_evaluated / quality_gate_failed / direct_anchor_28_of_29 / full_content_fallback_1_of_29 / result_registered / stopped` | C128直系。F04 N=5初段は通過したが、追加24件の1件がexact anchor受領済みでも全残存content fallbackを選び、配送切詰め後に変更・validationなしでscore `2`。合計score `4 / 2 = 28 / 1`、stale preimage 0 / 29。F02、F07、Standard14へ進めない |
| [`Point 4 dependency監査`](candidate131-point4-dependency-audit.md) | `audited / no_new_candidate / reopen_on_observed_dependency_failure` | C128 F02 / F07とC131 F04を照合。required effect closureとTaskSpec明示pairで部分成果を閉じており、C131の下流3式変更にもquality・cost実害を確認できない。implementation methodをglobal dependency predicateへしない |
| [`Candidate132`](candidate132-observed-preimage-change-construction-design.md) | `targeted_f04_n5_evaluated / quality_gate_failed / stale_preimage_0_of_5 / validation_false_stop_1_of_5 / result_registered / stopped` | C131直系。F04 N=5はscore `4 / 2 = 4 / 1`。stale preimageは0 / 5、必要変更は5 / 5だったが、全残存content fallback 1件が正しい変更後に未観測effectを未充足扱いし、validationを開始せず停止。次はPoint 6既存制御との境界監査 |
| [`Point 6 closure / recovery監査`](candidate131-point6-closure-recovery-audit.md) | `audited / no_new_candidate / six_point_initial_audit_complete` | C128のrequired-effect closureがF02・F04・F07の部分成果を閉じている。C132の停止は未観測effectを推測でclosedにしない保守側動作であり、Point 6の欠陥ではない。C132を停止し、C131を最後の成功checkpointとして維持 |
| [`Candidate125〜Candidate132 六点control統合`](candidate125-candidate132-six-point-control-synthesis.md) | `synthesized / c131_f04_n29_failed / point2_residual_observed` | Authority、Effect state、Dependency、Closureは既存ownerを維持。C132のglobal preimage gateは不採用。C131 F04 N=29でstale constructionは0件だがdirect anchor選択が1件崩れたため、次はC128からPoint 2のglobal readiness判断を置換できるか検討する |
| [`Candidate133`](candidate133-anchor-first-continuation-order-design.md) | `targeted_f04_n5_evaluated / quality_gate_passed / mechanism_gate_failed / anchor_first_4_of_5 / result_registered / stopped` | C128直系。F04 N=5は5 / 5 score `4`だが、1件が変更前anchorを使わず全残存contentへ直行。`observed_anchor_set`の空判定が新しいmeta-judgmentとして残ったため、追加24件、F02、F07、Standard14へ進めない |
| [`Candidate133 TaskSpec lexeme authority監査`](candidate133-task-spec-lexeme-authority-audit.md) | `audited / task_spec_unchanged / point2_syntactic_lexeme_candidate_ready` | Standard14全14件のmodel-visible TaskSpecを横断。構造化anchor欄はTaskSpec identityとA01 / A02の評価目的を変えるため不採用。次はC128直系で未解決criterion中のcode-shaped lexemeを意味判断なしに全件抽出し、F04 N=5で検証する |
| [`Candidate134`](candidate134-syntactic-lexeme-continuation-design.md) | `targeted_f04_n5_evaluated / quality_gate_failed / mechanism_gate_failed / result_registered / stopped` | C128直系。F04はscore `4 / 3 = 4 / 1`。direct lexemeは5 / 5だったがfull fallback 3 / 5。低Score 1件はTaskSpec lexeme周辺から既存上流定義を観測できず重複定義を追加し、lint失敗、build未実行。次は参照symbol一段展開のownerを監査し、C135はまだ作らない |
| [`Candidate134 reference symbol coverage owner監査`](candidate134-reference-symbol-coverage-ownership-audit.md) | `audited / point2_owner / offline_scope_comparison_complete / genericity_domain_bounded / c135_not_created` | Aをcriterion ID spanのrequest authority、Bを一意reference definition一段closureとして分離。F04は140→165 / 1,097行でdefinitionへ到達。Python / shellへも適用した。汎用domainはimplementation × 単一target × 一意bindingへ限定し、review、boundary、prose、declarative、複数targetへ一律適用しない。F04外の品質上の必要性が未観測のためC135は未作成 |
| [`Candidate135`](candidate135-criterion-span-request-authority-design.md) | `targeted_f04_n5_evaluated / quality_gate_failed / mechanism_gate_failed / result_registered / stopped` | C128直系。F04はscore `4 / 2 = 4 / 1`。criterion外lexeme混入は0 / 5へ抑えたが、全criterion lexeme-firstは3 / 5。低Score 1件は必要content取得後も変更hunkを構成できず、変更なし・validation未実行。停止条件によりCandidate136へ進めない |
| [`Candidate135 effect-local change admission監査`](candidate135-effect-local-change-admission-audit.md) | `audited / existing_controls_compared / next_axis_bounded / candidate_not_created` | C135成功4件は`hasAuditKey`一行だけを変更。低Score 1件は充足済み`colSpan`を同じpatchへ再投入して原子的に失敗。C128 / C129 / C132との重複を分離し、次軸をglobal完全性gateではなくeffectごとの`satisfied / unsatisfied / unobserved` bindと、unsatisfiedだけの初回change admissionへ限定した |
| [`Candidate136`](candidate136-effect-local-change-admission-design.md) | `targeted_f04_n5_evaluated / quality_gate_failed / effect_local_admission_passed / result_registered / stopped` | C135直系。F04はscore `4 / 3 = 4 / 1`。必要変更5 / 5、充足済みeffect変更0 / 5、initial patch失敗0 / 5。低Score 1件も未充足effectは変更したが、criterion lexemeから`colSpan`が脱落して未観測となり、closureでvalidation前停止。次はPoint 2のmember脱落を調査する |
| [`Candidate136 criterion lexeme member totality監査`](candidate136-criterion-lexeme-member-totality-audit.md) | `audited / regression_identified / generic_syntax_bounded / next_candidate_not_created` | C134の有限文字形規則をC135が未定義の`code-shaped token`へ縮めた退行を特定。C135・C136合計で全3 member検索7 / 10、`colSpan`脱落2 / 10、検索なし1 / 10。次軸をcriterion span内の`_`・`.`・`/`・小文字→大文字・複数語Title Caseの全件抽出だけへ限定した |
| [`Candidate137`](candidate137-pending-effect-validation-admission-design.md) | `targeted_f04_atomic_reuse_n53_evaluated / quality_gate_failed / pending_effect_state_observed / pending_validation_route_not_reached / result_registered / stopped` | C136直系。[`F04同一pool N=53`](../evaluations/results/candidate137-pending-effect-validation-admission-v14-medium-f04-atomic-reuse-n53-stopped-cli0146_2026-08-02.md)はscore `4 / 2 = 52 / 1`。低Score runでC2未観測状態が発生したが、既存`EVIDENCE_GATE`の両effect bind要求がartifact変更前に停止し、C137の変更後admissionへ未到達。次軸はeffect-local changeからpending validationへのhandoff衝突解消 |
| [`Candidate137既存case observer coverage監査`](candidate137-existing-case-observer-coverage-audit.md) | `audited / f04_only_observed_trigger / same_pool_extended_to_n53 / trigger_observed / stopped_on_score_2` | Standard14の複数effect implementation caseを横断し、唯一保存済み発生歴があるF04を同一条件で継続。N=53でpending effect状態が一件発生し、同じrunがscore `2`となったため追加発行を停止した |
| [`Candidate138`](candidate138-continuation-effect-change-handoff-design.md) | `f02_f04_f07_n5_evaluated / quality_gate_failed / f04_mechanism_passed / multi_target_admission_leak_identified / result_registered / stopped` | C137直系。[`F04 N=29`](../evaluations/results/candidate138-continuation-effect-change-handoff-v14-medium-f04-atomic-reuse-n29-cli0146_2026-08-02.md)は29 / 29 score `4`で変更後direct validationへのhandoffを一件観測。続く[`F02 / F04 / F07 N=5`](../evaluations/results/candidate138-continuation-effect-change-handoff-v14-medium-f02-f04-f07-atomic-reuse-n5-stopped-cli0146_2026-08-02.md)はscore `4 / 2 = 13 / 2`。predicateへ`single_change_target_ready`を含めなかったため、複数targetのF02で部分変更2件がvalidation失敗。次は既存guardとのANDだけを検証する |
| [`Candidate139`](candidate139-single-target-continuation-handoff-design.md) | `f02_f04_f07_n5_evaluated / quality_gate_failed / single_target_guard_ineffective / dynamic_target_shrink_identified / result_registered / stopped` | C138直系。[`F02 / F04 / F07 N=5`](../evaluations/results/candidate139-single-target-continuation-handoff-v14-medium-f02-f04-f07-atomic-n5-stopped-cli0146_2026-08-02.md)はscore `4 / 2 = 11 / 4`。F02の部分変更3件では未観測updater effectを充足済みと判断し、未解決target集合を一件へ縮めてguardを通過した。次はTaskSpec-bound target集合を充足判定前に固定できるauthorityを監査する |
| [`Candidate139 effect satisfaction witness監査`](candidate139-effect-satisfaction-witness-audit.md) | `audited / upstream_false_satisfaction_identified / target_cardinality_not_primary / next_axis_bounded / candidate_not_created` | C128成功5件とC139 F02低Scoreを同一互換条件で比較。updaterには日付選択helperがあるが取得経路へ未接続だった。C139はhelper存在または後続validation予定をeffect充足へ読み替え、ownerを未解決集合から落とした。次軸はTaskSpec required relationの全memberと接続を直接観測した場合だけ`satisfied`へbindする`effect_satisfaction_witness` |
| [`Candidate140`](candidate140-effect-satisfaction-witness-design.md) | `f02_f04_f07_n5_evaluated / quality_gate_failed / partial_effect_witness_response / f02_partial_change_2_of_5 / result_registered / stopped` | C139直系。[`F02 / F04 / F07 N=5`](../evaluations/results/candidate140-effect-satisfaction-witness-v14-medium-f02-f04-f07-atomic-n5-stopped-cli0146_2026-08-02.md)はscore `4 / 2 = 13 / 2`。F02二件はrequired relation全memberと未接続callが初回resultにあってもengineだけを変更。別二件は変更前に両effectを認識し、一件はfocused failure後の一回reworkで回復。次はpredicate追加前に三経路の判断順序を比較する |
| [`Candidate140 evidence completeness granularity監査`](candidate140-evidence-completeness-granularity-audit.md) | `audited / evidence_granularity_split_identified / candidate141_ready_not_created` | C139 / C140 F02計10件を比較。required relationを含む限定取得は変更前の両effect認識3 / 3、4 target全体・過大取得は0 / 7だった。次軸はread量の固定ではなく、prechange waveの完了単位をtarget content coverageからrequired relation coverageへ置換する。C122のone-wave目的、C125のsingle-target continuation、C128 / C140のeffect制御は維持する |
| [`Candidate141`](candidate141-prechange-relation-coverage-design.md) | `f02_f04_f07_n5_evaluated / quality_gate_failed / relation_coverage_4_of_5 / whole_target_fallback_1_of_5 / result_registered / stopped` | C140直系。[`F02 / F04 / F07 N=5`](../evaluations/results/candidate141-prechange-relation-coverage-v14-medium-f02-f04-f07-atomic-n5-stopped-cli0146_2026-08-02.md)はscore `4 / 2 = 14 / 1`。F02限定取得4件は両effectを変更してscore `4`、全体取得1件はengineだけの部分変更でscore `2`。次Candidate前にC122のone-waveとterminal closureの結合優先順位を監査する |
| [`Candidate141 post-result change admission監査`](candidate141-post-result-change-admission-audit.md) | `audited / post_result_initial_admission_gap_identified / candidate142_ready_not_created` | C141低Scoreを発行前scope、受領後state、変更開始admissionへ分離。relation coverageはrequest identityにだけbindされ、result受領後にupdaterがunobservedでもC136のeffect-local admissionがengine変更を許した。次軸はsingle-target F04を維持し、TaskSpec-boundの複数owner共同outcomeだけ全effect state bind後にinitial changeを許可する |
| [`Candidate142`](candidate142-initial-joint-effect-admission-design.md) | `f02_f04_f07_n5_evaluated / quality_gate_failed / f02_partial_change_closed / f02_false_stop_3_of_5 / result_registered / stopped` | C141直系。[`F02 / F04 / F07 N=5`](../evaluations/results/candidate142-initial-joint-effect-admission-v14-medium-f02-f04-f07-atomic-n5-stopped-cli0146_2026-08-02.md)はscore `4 / 2 = 12 / 3`。F02の一target部分変更は0 / 5へ閉じたが、約6.0万〜13.8万文字の過大取得3件でrelationが未観測となり、無変更で停止。次Candidate前にC141 / C142 F02全10件のevidence request構成とpost-result admissionを分離監査する |
| [`Candidate143`](candidate143-required-outcome-implementation-bind-design.md) | `targeted_f02_f04_f07_n100_evaluated / quality_gate_passed / targeted_stability_gate_passed / standard14_n5_evaluated / c125_cost_both_higher / result_registered / adoption_not_decided` | C118直系。[`F02 / F04 / F07 N=100`](../evaluations/results/candidate143-required-outcome-implementation-bind-v14-medium-f02-f04-f07-atomic-reuse-n100-cli0146_2026-08-02.md)は300 / 300 score `4`で、対象3経路のstability gateを通過。[`Standard14 N=5`](../evaluations/results/candidate125-candidate143-required-outcome-implementation-bind-v14-medium-standard14-atomic-reuse-n5-cli0146_2026-08-02.md)も70 / 70 score `4`だが、正式C125比token `+24.98%`、elapsed `+17.30%`。次はstabilityを保持し、検証predicate / method分離と変更前evidence operation集約を別軸で測る |
| [`Candidate144`](candidate144-required-outcome-validation-method-boundary-design.md) | `six_case_n5_evaluated / quality_gate_passed / mechanism_gate_failed / result_registered / stopped` | C143直系。6 case N=5は30 / 30 score `4`でA02 tokenはC143比`-23.50%`。ただし変更前再入1 / 5、変更後method探索1 / 5で事前gate失敗。Standard14へ進めず、共通のevidence admission境界を挙動から再設計する |
| [`Candidate145`](candidate145-lifecycle-consumer-evidence-admission-design.md) | `standard14_n5_evaluated / quality_gate_passed / lifecycle_consumer_mechanism_passed / c125_cost_gate_failed / result_registered` | C144直系。6 case N=5は30 / 30 score `4`、A02再入0 / 5。続くStandard14は70 / 70 score `4`で全体成果退行なし。C143比token`-9.00%`・elapsed`+11.71%`、C125比token`+13.74%`・elapsed`+31.04%`でcost gate失敗。F01 / F02 / F03のconsumer構成と往復costが次の分解対象 |
| [`Candidate146`](candidate146-consumer-closure-evidence-operation-design.md) | `f01_f02_f03_n5_evaluated / quality_gate_passed / incremental_closure_not_demonstrated / start_identity_design_boundary_failed / result_registered / stopped` | C145直系。[`F01 / F02 / F03各N=5`](../evaluations/results/candidate145-candidate146-consumer-closure-evidence-operation-v14-medium-f01-f02-f03-atomic-n5-stopped-cli0146_2026-08-02.md)は15 / 15 score `4`、C145比token`-4.50%`・elapsed`-5.61%`。[`model step再監査`](candidate146-model-step-boundary-audit.md)でC145 / C146ともsource / test共同発行15 / 15と判明。C146はstepを減らさず、開始identity設計境界も14 / 15。次の未検証軸は停止効果をoperation classへ限定する`result_effect_scope` |
| [`Candidate147`](candidate147-adoption-decision.md) | `standard14_n100_evaluated / quality_stability_gate_passed / mechanism_gate_passed / aggregate_cost_recovered / adopted / release_approved / runtime_not_projected` | C145直系。targeted 15 / 15で狙った`result_effect_scope`が成立し、[`Standard14 N=100`](../evaluations/results/candidate147-result-effect-scope-v14-medium-standard14-atomic-reuse-n100-cli0146_2026-08-02.md)は1,400 / 1,400 score `4`、低Score・excluded attempt・controller errorは0件。C145比でcostを下げ、C125付近の集約中央値でN=100安定性を確認したため採用。F06 authority追加read 21 / 100件を残存riskとして受容。内容同一releaseを承認し、runtime投影は未完了 |
| [`Candidate94`](../evaluations/results/candidate81-candidate94-operation-criterion-totality-v14-medium-standard14-n5-cli0146_2026-07-30.md) | `standard14_evaluated / stopped` | A02 iteration 5がscore `1`。品質gate不通過のためtargeted、採用、release、本体反映へ進めない |
| [`Candidate95`](../evaluations/results/candidate81-candidate95-required-judgment-owner-boundary-v14-medium-standard14-continuous-n5-b20-cli0146_2026-07-30.md) | `standard14_b20_evaluated / stopped` | C95はscore `4 / 2 / 1 = 1,398 / 1 / 1`でowner clarification経路が2件再発。C81比token +4.49%、elapsed +5.53%も有意に悪化したため採用以降へ進めない |
| [Observation delivery executor A/B](../evaluations/results/candidate81-observation-delivery-executor-ab-v14-medium-f02-n5_2026-07-29.md) | `executor_f02_evaluated / stopped` | 直接result禁止は5 / 5で成立したが、model再入は中央値7・合計36で不変。次は外側code returnをterminal waveへ制約できる場合だけ再開 |
| [Success-silent delivery](../evaluations/results/candidate81-success-silent-delivery-v14-medium-f02-n5_2026-07-29.md) | `executor_f02_evaluated / cost_reduced / F04未実施` | 成功validation rawを配送せず5 / 5 score 4。sealed control比token中央値-17.86%、合計-21.60%。次はF04互換A/Bで再現性を確認 |
| [Pytest exact allowlist success delivery](../evaluations/results/candidate81-success-delivery-executor-ab-v14-medium-f06-n5_2026-07-29.md) | `executor_f02_f06_evaluated / output_reduced / cost_control_failed / transparent_runtime_probe_failed / executor_hook_unavailable / stopped` | F06 matched A/Bは両条件5 / 5 score 4。output合計-64.47%だがtoken中央値+41.76%、合計+22.29%。runtime shimはallowlist外Pythonの`sys.executable`を変更し、Codex CLI 0.146.0のPostToolUse hookもoutput抑制・置換を提供しないためprofile作成前に停止 |
| C81・C87・C88・C89 F02 control graph診断 | 完了・新Candidateなし | 保存trace診断で上流のoperation誤分解を特定。fresh C81互換traceで再観測した場合だけ再開 |
| A01の3択variation診断 | 完了・新Candidateなし | 修正版30 / 30 valid。補集合選択、候補順依存、過剰停止を再現せず終了 |
| 投影済みCandidate71のrisk整理 | 完了・監視 | 現在は非再現。fresh traceで未固定値の誤実行を再観測した場合だけ再開 |
| F10 exact coordinate evidence interface | 対応なしで完了 | exact coordinateをhard requirementにしないため実装・追加runを行わない |
| rating contract identity・一律比較・reasoning追試 | 解決済み | 現行v13を確定し、High／Medium比較とreasoning 6水準を完了 |
| `QUALITY_RATING_V8`への改名 | 解決済み | identity・schema・採点挙動を変えずrevision名を明示化 |
| [`Candidate78`](candidate78-project-index-navigation-design.md) | `standard14_evaluated / stopped` | token中央値`+8.66%`、elapsed中央値`+4.38%`。追加改訂以降へ進めない |
| 公開target repository系列・runtime再現性 | 完了 | Click標準14、空環境再構築、network遮断full gate、offline lock確認まで完了 |

## 1. label監査の残件

`Candidate71`の11 label監査で再測定候補として残った3件の現在判断。正本は[`candidate71-control-abstraction-analysis.md`](candidate71-control-abstraction-analysis.md)の「監査状況の分類」表。

| 項目 | 必要な再測定 | 結論をflipし得るか |
| --- | --- | --- |
| `CONTEXT`（`X1`） | **ペンディング。** A06はUltra制御用のため、case variant、bundle、gate、fresh runを開始しない | **あり**。拡張方向（packet resolved premiseによる再読削減）が未検証 |
| `INDEPENDENCE`（`I1` = `F9`） | **対応なしで完了。** A / D scopeの追加評価を実施しない | 低い。Candidate68のF10ではruntime非改善 |
| `RECOVERY`（`R1 / R2`） | `environment_recovery_max>0`の正のrecovery scenario caseでの評価。現Evaluation setは`not_applicable`でun-run | 不明（効果未測定） |

`CONTEXT`（`X1`）は、Ultra条件でA06制御を再検討する明示判断があった場合だけ再開する。保留中はCandidate、probe、追加model runを作成しない。

`INDEPENDENCE`（`I1`）は、未測定範囲を埋めること自体を目的とした追加runを行わない。`I1`が原因となる不要なoperation分割をfresh traceで観測した場合だけ、別の判断単位として再開する。

## 2. `PRODUCER`の`P3`一文削除Candidate82（B20完了・停止）

11 label監査で唯一「Candidate作成根拠あり」となった項目。`P3`の正本は`OWNER_ROLE`側にあり、`PRODUCER`側の短い再記述だけを削除した。F10 / D01 targeted 10 / 10と単発標準14 70 / 70はscore `4`だったが、採用前B20で低頻度route非安定性を観測した。20 result、1,400 / 1,400件はvalid・rateable、公式score `4 / 1 = 1,399 / 1`である。score `1`は採点偽陰性だった。一方、F02とF04の各1件がcriterion ownerを独立producer指定へ変換し、不要childを起動したため、Candidate82を`standard14_b20_evaluated / stopped`とする。

- 現在設計: [`candidate82-producer-gate-deduplication-design.md`](candidate82-producer-gate-deduplication-design.md)
- targeted結果: [`Candidate81 / Candidate82 F10・D01 N=5`](../evaluations/results/candidate81-candidate82-producer-gate-deduplication-v13-medium-f10-d01-n5_2026-07-28.md)
- 標準14結果: [`Candidate81 / Candidate82 Medium標準14 N=5`](../evaluations/results/candidate81-candidate82-producer-gate-deduplication-v13-medium-standard14-n5_2026-07-28.md)
- 採用前B20結果: [`Candidate82 Medium標準14 N=5 B20`](../evaluations/results/candidate82-producer-gate-deduplication-v13-medium-standard14-continuous-n5-b20_2026-07-28.md)
- C81 B20とC82の記述比較: [`Candidate81 Medium標準14 N=5 B20`](../evaluations/results/candidate81-validation-wrapper-precedence-v13-medium-standard14-continuous-n5-b20_2026-07-29.md)。C81は1,400 / 1,400 root-onlyだったが、fixture mode差によりcompatibility keyが一致しないためwinnerまたは採用判断へ使わない
- prompt identity: `the-caption-3ce91a4-producer-gate-deduplication-r1`
- 現在境界: B20まで評価完了。設計の停止条件により採用、release、本体反映へ進めない

A01のscore `1`で確認した文面依存の偽陰性には、Rating v14を追加して対応した。v14は疑問符や質問語を採点せず、未固定値、terminal response、zero drift、試験・変更operation未開始から`awaiting_required_value`状態を作る。v13のB20公式scoreはimmutableなまま保持する。後続の[`Candidate81 A01 Rating v14 B20`](../evaluations/results/candidate81-validation-wrapper-precedence-v14-medium-a01-continuous-n5-b20_2026-07-29.md)は別Evaluation set identityの新規実行として100 / 100件をscore `4`かつ`awaiting_required_value`で登録した。v13 B20の再採点または標準14全体のB20として扱わない。
- 旧分析が作業呼称として使った「Candidate74」は別軸へ割り当て済みであり、履歴上の呼称としてのみ保持する

### Candidate83: Worker価値による委譲境界（F02評価完了・停止）

Candidate82のF02 / F04誤起動を、Worker一律禁止ではなく`delegation_value_ready`で扱う。AIは独立性、並列化、context分割、worker固有capabilityに固有価値がある場合にWorkerを選べる。一方、criterion owner語列だけの起動と、rootが同じpredicateを処理する逐次重複は許可しない。

- 設計正本: [`candidate83-delegation-value-boundary-design.md`](candidate83-delegation-value-boundary-design.md)
- prompt identity: `the-caption-3ce91a4-delegation-value-boundary-r1`
- bundle SHA-256: `0e3fd8e8b24b82f84fad1d2e9c68f391a7e3fa722b82fcfc5cbff80a2d6bf852`
- F02結果: [`Rating v14 Medium F02 N=5`](../evaluations/results/candidate83-delegation-value-boundary-v14-medium-f02-n5_2026-07-28.md)。5 / 5 score `4`だったが、5 / 5で不要Workerを起動し、1 runは同じ確認を別Workerへ再割当てした
- immutable評価state: `targeted_f02_evaluated / stopped`
- 現在解釈: [`Worker委譲のコスト判定と制御再設計`](delegation-cost-control-redesign.md)により`quality_passed / cost_control_not_demonstrated`。Worker起動自体は失敗条件にしないが、互換baselineと事前toleranceがないため追加評価、採用、release、本体反映へ進めない

### Candidate84: Worker限界価値の状態境界（F02評価完了・停止）

Candidate83の`TaskSpecが独立性を要求`という語義判定を削除し、Worker専有scopeと実質的な限界価値を状態として判定する。criterion owner、risk owner、`independent`語列、独立確認という作業名だけではWorkerを起動しない。一方、別execution identity、並列化、context分離、固有capability、未解決判断に実質的価値があればAIがWorkerを選べる。

- 設計正本: [`candidate84-delegation-marginal-value-boundary-design.md`](candidate84-delegation-marginal-value-boundary-design.md)
- prompt identity: `the-caption-3ce91a4-delegation-marginal-value-boundary-r1`
- bundle SHA-256: `b58ab2d14417be459dc8fd2a66cd1d48c1f8ae538e1e58a38148cb9598825d82`
- F02結果: [`Rating v14 Medium F02 N=5`](../evaluations/results/candidate84-delegation-marginal-value-boundary-v14-medium-f02-n5_2026-07-28.md)。5 / 5 score `4`、3 / 5 root-onlyだったが、2 / 5で不要Workerを起動した
- immutable評価state: `targeted_f02_evaluated / stopped`
- 現在解釈: [`Worker委譲のコスト判定と制御再設計`](delegation-cost-control-redesign.md)により`quality_passed / cost_control_mixed`。Workerあり2件のうち並行経路と逐次経路が混在し、互換baselineと事前toleranceもないため追加評価、採用、release、本体反映へ進めない

### Candidate85: planning-first producer selection（F02・F04評価完了・停止）

C83 / C84でWorkerの期待価値をprompt内predicateへ展開した方向を停止した。C85はC81を直接親とし、AIが実行前planningでoperation graph、producer、dependency、execution waveを一体として決める。既存F02 r1、F04 r2、D01 r1のTaskSpec、fixture、oracleは変更しない。Workerを含む経路全体は互換な品質・all-agent token・elapsedで判定し、routingはdiagnosticへ戻す。

- 正本: [`Worker委譲のコスト判定と制御再設計`](delegation-cost-control-redesign.md)
- 設計: [`Candidate85 planning-first producer selection設計`](candidate85-planning-first-producer-selection-design.md)
- prompt identity: `the-caption-3ce91a4-planning-first-producer-selection-r1`
- bundle SHA-256: `293e1457a9de4501574a31cad281990244aaea0f6c1a927a25356b00b99fd48d`
- route診断: [`Planning-first route diagnostic`](planning-first-route-diagnostic.md)
- 評価profile: C81 / C85それぞれF02、F04、D01をRating v14、Medium、`N=5`で固定。各pairはprompt identity以外を一致させる
- 事前cost tolerance: token `0`、elapsed `0`
- F02結果: [`Candidate81 / Candidate85 Rating v14 Medium F02 N=5`](../evaluations/results/candidate81-candidate85-planning-first-v14-medium-f02-n5_2026-07-28.md)。両条件5 / 5 score `4`、C85はtoken中央値`-0.94%`、elapsed中央値`+5.32%`の`cost_tradeoff`
- F04結果: [`Candidate81 / Candidate85 Rating v14 Medium F04 N=5`](../evaluations/results/candidate81-candidate85-planning-first-v14-medium-f04-n5_2026-07-28.md)。両条件5 / 5 score `4`、C85はtoken中央値`+38.29%`、elapsed中央値`+24.70%`の`cost_control_failed`
- route: C81 / C85ともF02・F04の全runがroot-only。C85は全runで最初のcommand前にproducerを固定したが、F04のコスト悪化はWorker起動なしで発生した
- 現在境界: `targeted_f02_f04_evaluated / stopped`。D01 profileは未実行のまま保持し、標準14、採用、release、本体反映へ進めない

### Candidate86: producer plan fast path（F02・F04・D01評価完了・停止）

C85のplanning-first順序は維持し、単一operationでも完全なoperation graphと明示planを維持する経路を除く。C81を直接親とし、独立した`PLAN` labelを追加せず、既存`PRODUCER`、`OWNER_ROLE`、`DECISION_BOUNDARY`だけを置換する。

- 設計: [`Candidate86 producer plan fast path設計`](candidate86-producer-plan-fast-path-design.md)
- prompt identity: `the-caption-3ce91a4-producer-plan-fast-path-r1`
- bundle SHA-256: `053b23c2a51ed58e7cc1e2bc6c6e973b72f04f1e1058dcbed22d0e7fc6e93a51`
- root prompt本文: `5,914 bytes`。C81比`+389 bytes`、C85比`-625 bytes`
- 評価profile: 既存F02 r1、F04 r2、D01 r1を再利用したC81 / C86 pair。新しいcase、fixture、oracle、Evaluation setは作成していない
- 評価順: F02、通過時だけF04、さらに通過時だけD01
- 事前cost tolerance: token `0`、elapsed `0`
- F02結果: [`Rating v14 Medium F02 N=5`](../evaluations/results/candidate81-candidate86-producer-plan-fast-path-v14-medium-f02-n5_2026-07-29.md)。両条件5 / 5 score `4`、token中央値`-2.44%`、elapsed中央値`+1.43%`の`cost_tradeoff`
- F04結果: [`Rating v14 Medium F04 N=5`](../evaluations/results/candidate81-candidate86-producer-plan-fast-path-v14-medium-f04-n5_2026-07-29.md)。両条件5 / 5 score `4`、C86 root-only 5 / 5、token中央値`+6.77%`、elapsed中央値`-6.03%`の`cost_tradeoff`
- D01結果: [`Rating v14 Medium D01 N=5`](../evaluations/results/candidate81-candidate86-producer-plan-fast-path-v14-medium-d01-n5_2026-07-29.md)。両条件5 / 5 score `4`かつ指定worker route成立。C86はtoken中央値`+83.28%`、elapsed中央値`+45.81%`の`cost_control_failed`
- route診断: C86 childのcustom exec call合計がC81の`13`から`41`へ増え、child token合計は`340,228`から`873,848`へ増えた
- 現在境界: `targeted_f02_f04_d01_evaluated / stopped`。標準14、採用、release、本体反映へ進めない

### Candidate87: producer-local invocation wave（標準14品質通過・集約コスト悪化）

C86 D01のコスト悪化を、Worker起動判断ではなくbind済みproducer内部のinvocation分割へ限定する。C86を直接親とし、`DECISION_BOUNDARY`だけを置換する。

- 設計: [`Candidate87 producer-local invocation wave設計`](candidate87-producer-local-invocation-wave-design.md)
- prompt identity: `the-caption-3ce91a4-producer-local-invocation-wave-r1`
- bundle SHA-256: `b5f581afa5fafa941c7d9974abc127d50acc488085a63d85974b8bd8047b4e67`
- root prompt本文: `6,278 bytes`。C86比`+364 bytes`
- 変更軸: root / worker共通で、decision boundary、明示order、fail-stop dependencyを持たない同一operation内invocationを一つのcustom exec wrapperから同時発行する
- 試験: 既存D01 r1でC86 / C87一軸qualification。通過後だけ保存済みC81 D01との比較、F02 r1、F04 r2へ進む
- 新しいcase、fixture、oracle、Evaluation set: 作成しない
- D01結果: [`Rating v14 Medium D01 N=5`](../evaluations/results/candidate86-candidate87-producer-local-invocation-wave-v14-medium-d01-n5_2026-07-29.md)。指定worker routeは5 / 5件で成立し、C86比でchild custom exec call合計`41 → 12`、token中央値`-51.06%`、elapsed中央値`-26.54%`
- 品質結果: append-only訂正後はscore `4 = 5`。当初の`4 / 3 = 4 / 1`は、個別監査がv14 contract IDを渡さずv10規則を適用した誤採点だった。詳細は[`rating contract binding訂正`](../evaluations/results/targeted-review-rating-contract-binding-correction_2026-07-29.md)
- C81比較: token中央値`-14,694`（`-10.29%`）、elapsed中央値`+6.606`秒（`+7.12%`）。両KPI悪化の停止条件には該当しない
- F02結果: [`Rating v14 Medium F02 N=5`](../evaluations/results/candidate81-candidate87-producer-local-invocation-wave-v14-medium-f02-n5_2026-07-29.md)。5 / 5 score `4`、C81比のtoken中央値`-5.26%`、elapsed中央値`-10.63%`でgate通過。token合計は`+16.06%`で分布はmixed
- F04結果: [`Rating v14 Medium F04 N=5`](../evaluations/results/candidate81-candidate87-producer-local-invocation-wave-v14-medium-f04-n5_2026-07-29.md)。5 / 5 score `4`、C81比のtoken中央値`+15.48%`、elapsed中央値`-12.62%`のtradeoff。両KPI悪化の停止条件には非該当
- 標準14結果: [`Rating v14 Medium標準14 N=5`](../evaluations/results/candidate81-candidate87-producer-local-invocation-wave-v14-medium-standard14-n5_2026-07-29.md)。C81 / C87とも70 / 70 score `4`。C87はtoken中央値`+6.09%`、elapsed中央値`+1.35%`で、集約コストは両方大きい
- 評価境界: `standard14_evaluated / quality_gate_passed / aggregate_cost_both_higher / adoption_not_decided`。一次resultに保存した当時の状態は変更しない
- 後続の採用判断: [`Candidate87採用判断`](candidate87-adoption-decision.md)で`not_adopted / stopped`。releaseは作成せず、本体反映は承認しない。現在の採用・投影済み基準はC81のまま

### C81・C87・C88・C89 F02 control graph診断（完了・新Candidateなし）

**2026-07-29に保存traceだけで診断を完了した。** C81、C87、C88、C89の既存F02 r1各`N=5`を再確認し、一次result、score、candidate stateは変更していない。

- C81は5 / 5 root-onlyだった。implementation、test-contract、required validationを一つのroot operationへbindした
- C87 / C88 / C89は合計11件で`/root/independent_contract_check`を起動し、child token合計は`820,380`だった
- 11件のWorker resultはF02-C3の再確認だけで、rootもscoped diff、test、required validation、最終done判定で同じpredicateを扱った
- C87とC88には同時進行経路があるため、executorのsame-wave capability欠落は確認できない
- 誤経路はdispatch順ではなく、criterion metadataを別operation identityへ昇格した上流のoperation分解で成立した
- 診断正本: [`Worker委譲のコスト判定と制御再設計`](delegation-cost-control-redesign.md)の「C81・C87・C88・C89 F02保存traceのcontrol graph診断」
- 完了境界: C81 F02では同じ誤分解が0 / 5であり、観測されたC81失敗がない。`wave_commit`、executor変更、C81直接child、bundle、profile、追加model runは作成しない
- 再開条件: fresh C81互換traceで同じoperation誤分解を再観測するか、別operation identityまたは別execution identityをrequired outcomeにする明示要件が追加された場合だけ、`operation_identity_ready`一軸の作成前gateへ戻る
- 系列境界: C87の不採用判断を含め、Candidate82〜Candidate89のサブエージェント制御系列を完了・停止とする

## 3. A01の3択variation診断

**2026-07-28に完了。** A01の現行2択caseを回帰基準として変更せず、現在値と候補順を3通り回転した`AMBIGUOUS` / `AUTHORITY`の6 caseを追加した。

- 第1版30件はすべてvalidだったが、`strict` / `live`開始状態と既存仕様書の`daily`記述が不整合であり、10 / 10件がその記述を変更先authorityへ変換した。fixture交絡として分離した。
- 仕様書も開始値へ同期した第2版は30 / 30件がvalid、excluded attempt 0件だった。
- `AMBIGUOUS`は15 / 15件がzero driftかつ試験前の確認停止、`AUTHORITY`は15 / 15件が質問せず指定値へ変更して関連testを成功させた。
- 補集合選択、候補順依存、現在値回避、過剰停止は第2版で再現しなかった。新しいprompt predicateの根拠がないためCandidateは作成しない。

正本は[`Candidate81 A01 3択variation診断`](../evaluations/results/candidate81-a01-three-choice-variation-diagnostic_2026-07-28.md)と[`修正版set`](../evaluations/sets/the-caption-a01-three-choice-variation-r2/README.md)である。第1版は上書きせず、交絡を確認した履歴として保持する。

## 4. 投影済みCandidate71のrisk（現在解釈の整理完了・監視へ移行）

**2026-07-28に現在解釈の整理を完了した。** Candidate71は評価上`stopped`（v12の品質gate不通過）のまま、別の採用判断でTHE-CAPTION本体へ投影済みである。当時のrelease artifactに保存された未解決riskは2件で、これはimmutableな記録として取り消さない。一方、rating v13と投影済みCandidate81の追加診断による現在解釈では、この2件の位置づけが分かれる。

| 当時のrelease risk（v12時点） | 観測 | rating v13後の現在解釈 |
| --- | --- | --- |
| A02で`git diff --check`欠落 | 3 / 90件 | **現在の未完了研究項目ではない。** 実行役へ提示していない特定コマンドを採点側が必須化した「要求と採点のずれ」であり、本物の品質低下と区別される。v13でこのずれを塞いだ |
| A01で未固定modeを確認せず実装・試験へ進んだ誤実行 | 1 / 90件 | **当時の品質上の問題として保持する。** v13でも当該runの評価は変えない。一方、現在のCandidate81では3択variation r2の曖昧条件15 / 15件が確認停止し、authority条件15 / 15件が指定値へ正しく変更したため、追加制御を作らず監視項目へ移す |

- 当時の未解決riskの正本: [`Candidate71 release / projection`](../prompts/releases/the-caption-3ce91a4-validation-closure-release-r1/README.md)（v12結果は履歴として保持）
- 現在解釈の正本: [`control-mechanisms.md`](control-mechanisms.md)のrating v13節と[`a02-rating-divergence.md`](a02-rating-divergence.md)
- 現在挙動の正本: 上記「3. A01の3択variation診断」と[`Candidate81 A01 3択variation診断`](../evaluations/results/candidate81-a01-three-choice-variation-diagnostic_2026-07-28.md)
- 完了判断: 過去の1件を取り消さず、現在は非再現の監視項目とする。新しいprompt predicate、Candidate、常設gate、追加model runは作らない。今後、未固定値を確認せず変更したfresh traceを再観測した場合だけ、同じ診断setで再開する

## 5. F10 location mismatch: exact coordinateのevidence interface（対応なしで完了）

**2026-07-28に対応しないと判断して完了した。** 原因診断そのものは実施済みで、prompt側の変更は停止している。`CLAIM_PROVENANCE` collectorと90件backfillの後、30件checkpoint診断（`max_30_diagnostic_valid_without_location_mismatch`で停止）、追加105件、coordinate representation診断、delayed reconstruction診断、implicit coordinate passive case-control、real-Agent representation recency診断、recorded-state collision受動監査まで到達した。

正本の現在判断は、repository-wideに削除できるprompt判断点を確認できないため、**prompt変更と追加model runをここで止める**ことである。exact coordinateはこの基盤のhard requirementにしないため、modelが選んだexact line textをone-based coordinateへ変換するevidence interfaceも実装しない。

- 完了境界: 過去のlocation mismatchと診断結果は保持する。evidence interface、prompt制御、Candidate、追加model runは作らない。将来exact coordinateをhard requirementへ変更する明示判断があった場合だけ、別の判断単位として再開する。
- 正本: [`review-location-cause-diagnostic-plan.md`](review-location-cause-diagnostic-plan.md)（「対策判断への接続」節と各診断結果節）
- 制御graph側の判断（location mismatchを理由にroot規則を追加しない）は[`prompt-control-graph-review.md`](prompt-control-graph-review.md)を参照

## 6. 現行rating contract identity、一律比較、reasoning追試（解決済み・2026-07-26）

新規runへ適用する現行rating contractの指定が、評価基盤の正本（`owner-producer-quality-v8`）と後続文書（最新revision v13）で一致していなかった。**2026-07-25に現行をv13へ確定した。** 正本[`prompt-comparison-workflow.md`](prompt-comparison-workflow.md)の指定、評価実行手順[`evaluation-loop-manual.md`](evaluation-loop-manual.md)のLayer 3、契約台帳[`evaluations/rating-contracts/README.md`](../evaluations/rating-contracts/README.md)、および`scripts/evaluation_loop.py`の`SUPPORTED_QUALITY_RATINGS`をv13へ追従させ、v13 capsuleが受理されることをunit testで確認済みである。この項目は未完了ではない。

派生作業も2026-07-26に完了した。reasoning effortはcomparison conditionであり、水準ごとにcompatibility keyが異なる。水準内のprompt比較と、水準間の記述的比較を混同しない。

- [`Baseline、ControlFreeRepository、Candidate5、Candidate35、Candidate43、Candidate71のHigh標準14項目各N=5`](../evaluations/results/baseline-control-free-repository-c5-c35-c43-c71-v13-standard14-n5_2026-07-26.md)を最初のv13互換result集合として登録した。6条件 × 70件 = 420件で、v12以前のresultは同一comparisonへ混ぜない。
- [`Candidate71のreasoning 6水準`](../evaluations/results/candidate71-reasoning-levels-v13-standard14-n5_2026-07-26.md)を、`low` / `medium` / `high` / `xhigh` / `max` / `ultra`、標準14項目各`N=5`で記録した。`medium`がtoken中央値最小、`low`がelapsed中央値最小だった。
- [`6条件のMedium一律比較`](../evaluations/results/baseline-control-free-repository-c5-c35-c43-c71-v13-reasoning-medium-standard14-n5_2026-07-26.md)も420 / 420件を登録した。C71とC43のtoken中央値差はHigh `-31.47%`、Medium `-29.19%`であり、少なくともこの2水準ではeffort低下によって相対的な制御差は消えなかった。
- 2026-07-27以降の新規通常比較は`medium`を運用基準とする。既存`high` resultは履歴として保持し、reasoning effort自体の比較または既存互換条件の再現だけを例外とする。運用正本は[`evaluation-loop-manual.md`](evaluation-loop-manual.md)である。

## 7. `QUALITY_RATING`という汎用名がv8を指している（解決済み・2026-07-28）

**2026-07-28に解決した。** `scripts/evaluation_loop.py`で`owner-producer-quality-v8`を指していた汎用定数`QUALITY_RATING`を`QUALITY_RATING_V8`へ改名した。v8互換経路を使うintegration testとowner-producer evidence testも同じrevision名へ追従させた。

- 変更前から実行上の不具合はなく、run capsuleが`quality_rating`を明示する契約、v13の現行identity、各rating contractの内容とSHA-256は変更していない。
- `SUPPORTED_QUALITY_RATINGS`では同じv8辞書を`QUALITY_RATING_V8`として保持する。v8互換性を検証するtestの既定値もv8のままであり、v13へ暗黙変更していない。
- 完了境界は名前によるrevision分離だけである。過去result、rating contract artifact、schema、採点挙動は変更しない。

## 8. Layer 2 executorのClaude Code CLI置換（保留）

Layer 2 executorをCodex CLI（`codex exec`）からClaude Code CLI（`claude -p`）へ置き換える試験方法。2026-07-25に設計検討と前提のprobe実測を行ったが、2026-07-28の判断で**一旦保留**とした。実装、pilot、本測定はいずれも未着手であり、保留中は追加probeも行わない。

- 正本: [`claude-code-cli-evaluation-adapter-design.md`](claude-code-cli-evaluation-adapter-design.md)（実測値、adapter対応表、新設schema revision、未確定事項6件、段階計画Phase 0〜4）
- **Phase 0が先行条件**: 認証方式（API key + `CLAUDE_CONFIG_DIR`隔離、またはsubscriptionのまま開始gateで確認）が未決で、環境identityの固定方法がこの決定に依存する。決まるまでPhase 1のprobe設計を固定できない。
- 実装対象は新規adapterと新規collectorであり、既存の`scripts/run_codex_evaluation.py`、既存collector、既存registry resultは変更しない（[`scripts/AGENTS.md`](../scripts/AGENTS.md)）。
- **既存Codex resultとの互換比較は成立しない**。注入時点の差とtoken accountingの意味の差によりcompatibility keyが一致しないため、Claude Code条件はbaselineから再測定する独立系列として扱う（[`evaluations/AGENTS.md`](../evaluations/AGENTS.md)のCompatibility）。
- model名を明示したresultは`gpt-5.6-sol`が主で、2026-07-31のCandidate125 model-axis測定で`gpt-5.6-terra`と`gpt-5.6-luna`が加わった（[`Candidate125 Sol / Terra / Luna model-axis N=5`](../evaluations/results/candidate125-model-sol-terra-luna-v14-medium-standard14-n5-cli0146_2026-07-31.md)）。いずれもCodex CLI経路であり、Claude系modelでの測定は0件である（[`execution-control-research-paper.md`](execution-control-research-paper.md)の限界節）。この項目はその限界に接するが、この項目自体はmodel比較を目的としない。executor置換の成立条件だけを扱う。
- 再開条件: Claude Code系列へ着手する明示判断と、Phase 0で採用する認証方式の選択が揃った場合だけ再開する。

## 9. root `AGENTS.md`へのrepository index参照追加の効果（実施済み・停止）

**2026-07-26にCandidate78として実施し、停止した。** 投影済みCandidate71を直接sourceとし、root `AGENTS.md`へ条件付き`PROJECT_INDEX`一labelだけを追加した。index本文、残り18 target、評価条件は変更していない。

標準14項目各`N=5`は70 / 70件がscore `4`だったが、Candidate71比でall-agent token中央値は`+8.66%`、elapsed中央値は`+4.38%`だった。A02はindexを5 / 5で先に読んでもrepository-wide探索が5 / 5で残り、F10 Entryでは不要なindex readが2 / 5に増えた。事前停止条件に従い、追加改訂、採用、release、本体反映へ進めない。数値とidentityの正本は[`Candidate71 / Candidate78標準14結果`](../evaluations/results/candidate71-candidate78-project-index-navigation-v13-standard14-n5_2026-07-26.md)とする。

以下は着手前に固定した試験境界である。

- 変更単位: root `AGENTS.md`への参照追加1軸のみ。index本文はbundle targetとして既に固定済みのため、残り18 targetはcontent identicalなcandidate bundleになる。
- 観測: 3 KPI（`quality_score` / all-agent `total_tokens` / `elapsed_seconds`）を評価対象とし、target探索readとworker起動はdiagnosticへ置く。境界の正本は[`evaluations/AGENTS.md`](../evaluations/AGENTS.md)。
- 事前に両方向の仮説を置く。静的事実の参照でrepository探索readが減る方向と、root promptへの追加がcontextを増やすだけで動的tokenが増える方向の両方である。表面的なprompt短縮がall-agent tokenをほとんど動かさなかった既存知見（正本: [`control-mechanisms.md`](control-mechanisms.md)）から、静的byteの増減で効果を推定しない。
- read boundary / read route系candidate（C50、C56〜C59、C62、C63など）と論点が接近する。着手前に系譜を確認し、既存軸の再実行にならないことを確かめる。正本は[`prompts/candidates/README.md`](../prompts/candidates/README.md)と[`candidate-history.md`](candidate-history.md)。
- 比較条件: 既存Codex executor、標準14項目、rating v13で測れる軸である。項目6で取得したv13 Baselineをcomparisonへ使用できるが、repository index参照を追加するcandidateは別profile・別resultとして新規実行する。
- 項目8（Claude Code CLI executor置換）と同一比較単位へ混ぜない。executor変更とprompt変更を同じ比較単位へ入れない（root [`AGENTS.md`](../AGENTS.md)の共通変更規律）。
- candidate作成前gate 9項目（[`prompts/AGENTS.md`](../prompts/AGENTS.md)）を通してからbundleを作る。

## 10. 公開target repositoryでの計測系列と評価基盤のrepository汎用化（runtime再現性まで完了）

公開repositoryを対象とする独立系列として`pallets/click`を登録し、同じBundle Aで14 caseのqualification、追加case各`N=3`、Std14 `N=5`をLayer 1〜4まで実行した。**Std14は70 / 70件がvalid・rateableかつscore `4`である。** この項目が扱うのは、公開repositoryで計測系列を成立させ、その過程で「任意のtarget repositoryへ同じ手順を適用できる分離」を確定することである。prompt制御の新しい変更軸ではなく、計測条件側の軸である。

2026-07-26時点で次を完了している。

- target instance `click`を`layout: namespaced`、公開・第三者再現可能として登録
- control-free baseline bundle `click-00e592c-control-free-r1`を固定
- `CLICK-F01-ANSI-SEQUENCE-STRIP` r1を作成し、seed適用前後のfocused / full gateでfixtureをqualification
- `click-outcome-abstract-condition-preserving-v1`、`click-f01-only-r1`、P1-a profile r1 / r2を固定
- Codex CLI `0.144.0`、Python `3.14.5`、共有venv identityをprofileへ固定
- r1 profileはLayer 2開始前にall-agent token accounting宣言不足を検出し、result 0件のまま停止。履歴を上書きせず、r2でtoken accountingとrequired command evidence protocolだけを追加
- r2でP1-aを完了。quality `100.000`（raw score `4`）、all-agent token `180,871`、elapsed `77.811`秒、excluded attempt 0件
- `click-control-free-f01-only-global-m24-n5-r1`でP1-bを完了。5 / 5件がscore `4`、all-agent token中央値`189,977`（最小`170,228`、最大`202,176`）、elapsed中央値`80.475`秒（最小`79.323`、最大`85.443`秒）、excluded attempt 0件
- 同じ`N=5` profileを独立3 resultへ反復してP1-cを完了。15 / 15件がscore `4`、batch中央値の中央値はtoken `189,033`、elapsed `80.590`秒。batch中央値rangeはtoken `26,878`（`14.22%`）、elapsed `1.501`秒（`1.86%`）で、excluded attemptは全batch 0件
- F02 `CLICK-F02-STREAM-DEPRECATION-CONTRACT` r1をqualification。2 source fileの公開・非公開API contractをseedし、seed前focused `72 passed, 1 skipped`、seed後`2 collection errors`、fixture 2回のcommit / tree一致を確認
- rating contract v2、`click-f02-only-r1`、F02 N=3 profileを固定し、3 / 3件をscore `4`で登録。all-agent token中央値`303,563`、elapsed中央値`130.225`秒、excluded attempt 0件
- 残り12 caseを固定し、追加caseだけ各`N=3`で確認。現行revisionはすべて3 / 3件がscore `4`。F07 r1はcommand evidence照合不能の未rating履歴、F07-P r1 / r2は各3 / 3件score `3`の失敗履歴として保持
- runtime r2へ`uv==0.11.32`を追加し、identity `0a30733685c5fb3bb69abf136d6a8cdb04c4ec323f52dc6d1488f8d49a7cc952`を固定。F07-P r3はworkspace-local uv cacheで3 / 3件score `4`
- `click-standard14-r1`、rating v10、Std14 profileを固定し、70 / 70件をscore `4`で登録。5 iterationのall-agent token中央値`2,860,702`、elapsed中央値`1,235.719`秒、excluded attempt 0件
- THE-CAPTION Candidate81のroot本文をbyte-identicalに1 targetへ適用したBundle Bを固定し、同じStd14条件で70 / 70件をscore `4`として登録
- Bundle AからBundle Bはquality中央値差`0.000`、all-agent token中央値`-685,546`（`-23.96%`）、elapsed中央値`+35.384`秒（`+2.86%`）。THE-CAPTIONでのtoken削減方向は再現したが、elapsed短縮は再現しなかった
- 今後の運用基準を`medium`へ切り替え、Bundle AとC81全文のMedium Std14を各70 / 70件・全件score `4`で登録した。C81全文はBundle A比でtoken中央値`-28.79%`、elapsed中央値`-12.62%`となり、5 / 5 iterationでelapsedが短縮した
- THE-CAPTION ControlFreeRepositoryとの構成差を分離するため、Clickでtarget-local No-AGENTSとrootなしRepository sub-AGENTSをMedium Std14 N=5で比較した。両条件70 / 70件がscore `4`で、sub-AGENTS側はtoken中央値`+3.74%`、elapsed中央値`+7.90%`だった。ただしsub本文の初期context注入は0 / 70で、本文をreadしたA01 5 / 5だけがtoken中央値`+80.47%`となった。配置だけでは全caseへ水平適用されないため、Std14全体の本文効果とは扱わない
- THE-CAPTIONと同質のauthority availabilityを測れているかClick Std14全14 caseを見直した。F01〜F08、F10-R、A01、A02は元の実行判断点を維持し、回帰setとして変更不要だった。F10 r1だけはsource-onlyで完結していたため、`src/AGENTS.md`を明示authorityとするF10 r2をMedium N=5で追試した。No-AGENTSは5 / 5件がscore `1`でauthority不足停止、Repository Authorityは5 / 5件がscore `4`でinventoryを完了した。全10件がvalid・rateable、zero drift、excluded attempt 0件で、THE-CAPTION F10と同じavailability方向を再現した
- 見直し後の`click-standard14-r2`をNo-AGENTS / Repository Authority、Medium、N=5、M=24で全件再実施した。F10以外は両条件65 / 65件がscore `4`、F10だけがscore `1` × 5 / score `4` × 5へ分離した。全140件がvalid・rateable、excluded attemptとunexpected driftは0件で、14実行判断点の比較setとして互換性を達成した。quality中央値は94.643対100.000、tokenは`+5.57%`、elapsedは`+3.96%`だが、後二者はF10の完了作業量差とM=24の変動を含むため効率差とは扱わない
- 2026-07-31にTHE-CAPTION Candidate125 root本文をClickへbyte-identicalに水平適用し、`click-standard14-r2` Medium N=5をCodex CLI `0.146.0`で実施した。70 / 70件がvalid・rateable、F10以外65 / 65件がscore `4`、authorityなしF10は5 / 5件が`authority_unavailable`でscore `1`、excluded attemptとunexpected driftは0件だった。quality中央値`94.643`、all-agent token中央値`1,348,515`、elapsed中央値`786.007`秒である。保存済みClick C81はCLI `0.144.0`でcompatibility keyが異なるため、tokenとelapsedの差は算出しない
- C81 / C81 + Repository Authorityも同じStd14 r2、Medium、N=5、M=24で各70件実施した。C81はscore `4` × 65 / score `1` × 5、C81 + Authorityはscore `4` × 70で、F10以外のquality回帰は0件だった。同じauthority状態のC81差は、authorityなしでtoken `-27.35%`・elapsed `-17.04%`、authorityありでtoken `-25.08%`・elapsed `-10.98%`となり、C81の削減方向はsub authority追加後も維持された
- 2026-07-28に既存共有venvを使わない空環境から、固定Click commitと固定package versionでknown-good 8 package identityをbyte単位で再構築した。通常条件とprocess単位のnetwork遮断条件でfull gateが同じ`1939 passed, 25 skipped, 31000 deselected, 1 xfailed`となり、`uv lock --check --offline`も`Resolved 81 packages`で成功した。手順とplatform境界の正本は[`Click runtime再構築とoffline full gate`](click-runtime-reproducibility.md)とする

Bundle AのHigh一次結果は[`click control-free Std14 N=5`](../evaluations/targets/click/results/click-control-free-standard14-n5_2026-07-26.md)、Medium一次結果は[`click control-free Medium Std14 N=5`](../evaluations/targets/click/results/click-control-free-reasoning-medium-standard14-n5_2026-07-27.md)、HighでのBundle A / B比較は[`Click Control-Free / C81全文 Std14 N=5`](../evaluations/targets/click/results/click-control-free-c81-full-standard14-n5_2026-07-26.md)、Medium比較は[`Click Control-Free / C81全文 Medium Std14 N=5`](../evaluations/targets/click/results/click-control-free-c81-full-reasoning-medium-standard14-n5_2026-07-27.md)、sub instruction配置比較は[`Click No-AGENTS / Repository sub-AGENTS Medium Std14 N=5`](../evaluations/targets/click/results/click-no-agents-repository-subagents-reasoning-medium-standard14-n5_2026-07-27.md)、authority availability追試は[`Click No-AGENTS / Repository Authority Medium F10 N=5`](../evaluations/targets/click/results/click-no-agents-repository-authority-reasoning-medium-f10-authority-n5_2026-07-27.md)を正本とする。High / MediumのBundle A traceとTHE-CAPTION ControlFreeRepository Mediumを使った[`baseline分析`](click-control-free-medium-baseline-analysis.md)では、Clickの軽さはreasoning量だけでなく、tool出力量`-50.46%`と小さいrepository contextに強く対応した。sub instruction配置追試により、THE-CAPTION側の4つのsub本文が常にmodel contextへ入っていたという仮定は置けなくなった。F10 targeted追試ではauthority availabilityの効果を再現したが、1 caseからStd14全体へ一般化しない。C81 MediumによりA02 / F06は大きく改善した。後続の[`残余経路分析`](click-c81-medium-residual-analysis.md)では、F01のtoken増加はpaired差中央値`-970`で安定悪化ではないと判定した。F04はC81でgit history探索がHigh / Medium合計`4 / 10`、Control-freeで`0 / 10`となり、両reasoningでelapsed合計が約16〜18%増えた。2026-07-28に4件のraw traceを再解析したところ、history探索後に初めてmethodまたは変更scopeが確定しており、method bind後の代替探索は`0 / 4`件だった。`PRECHANGE_EVIDENCE_SCOPE`は方法制御を追加するため採用せず、`METHOD`置換CandidateとF04 Medium N=5 targeted runも`stopped_before_candidate`とした。将来、method bind後にも不要探索が続く保存traceを観測した場合だけ再検討する。

見直し後Std14全体の正本は[`Click No-AGENTS / Repository Authority Medium Std14 r2 N=5`](../evaluations/targets/click/results/click-no-agents-repository-authority-reasoning-medium-standard14-r2-n5_2026-07-27.md)である。

C81との組合せ結果の正本は[`Click C81 / C81 + Repository Authority Medium Std14 r2 N=5`](../evaluations/targets/click/results/click-c81-repository-authority-reasoning-medium-standard14-r2-n5_2026-07-27.md)である。

Candidate125水平適用の正本は[`Click Candidate125 Medium Std14 r2 N=5 CLI 0.146`](../evaluations/targets/click/results/click-c125-reasoning-medium-standard14-r2-n5-cli0146_2026-07-31.md)である。これは単独品質resultであり、CLI `0.144.0`の保存済みC81とのKPI比較ではない。

### 現在の依存範囲（2026-07-26に実測）

repository非依存な層とtarget固有な層は次のとおりである。

| 層 | artifact | 実測した状態 |
| --- | --- | --- |
| Layer 1 fixture | `scripts/prepare_case_fixture.py` | CLI引数は`--case` / `--source-repo` / `--output`のみで、target repositoryはparameter。固有pathのhard-codeなし |
| Layer 2〜4実行 | `scripts/evaluation_loop.py` | clickで25 result・計481 runをappend-only登録。set / cycle / capsule / registry単位で動作し、target repositoryによる実行分岐を持たない |
| 制御prompt本文 | [Candidate71 release](../prompts/releases/the-caption-3ce91a4-validation-closure-release-r1/README.md)の`AGENTS.md.txt` | `SPEC`〜`RECOVERY`の13 labelは見出し語を除きproject固有語彙を持たない |
| bundle target map | THE-CAPTION releaseのmanifest 19 target、Clickは0 / 1 / 3 targetの4 prompt set | THE-CAPTIONのtarget側directory構造へ依存するmapを変更せず、`click`用mapをinstance配下の別bundleとして固定した。C81 root本文のbyte-identicalな水平適用、empty bundle、3つのsub instructionをそれぞれ独立identityで表現した |
| case artifact | 各case revisionの`trial-prompt-input.json`、`private/seed.patch`、`private/case-data.json` | 14 case・17 revisionをinstance配下へ固定。失敗revisionを上書きせず保持した |
| rating contract | THE-CAPTION v13、`click-outcome-abstract-condition-preserving-v1`〜v10 | case追加ごとに旧revisionを残し、現行v10で標準14項目を固定した |
| 採点補助 | Clickは固定rating contractとblind evidenceで採点 | 14 case・481 runのratingと登録が成立。target固有の新しいkernel分岐は追加していない |

したがって汎用化の対象は実行基盤ではなく、**case artifact / rating contract revision / 採点補助 / bundle target mapの4つ**である。`click`では4つをinstance配下へ分離し、共有kernelへtarget repositoryによる実行分岐を追加せず、3 KPI、compatibility key、append-only registryを含む端から端までの流用をBundle A / Bの標準14項目で確認した。未確認なのは第三者によるruntime再構築とnetwork遮断下のfull gateである。

この分離の境界とinstance台帳は[`evaluations/targets/README.md`](../evaluations/targets/README.md)で確定した。既存の計測系列はtarget instance `the-caption`（`layout: legacy_root`）として登録し、artifact pathを移動していない。

### target選定gate（この順で判定する）

1〜4は候補の機械的な絞り込み、5〜7は測定が成立するかの判定である。

1. **license**: seed patch、fixture条件、evidenceをこのrepositoryへ保存し公開するため、再配布可能なlicense（Apache-2.0 / MIT / BSD等）に限定する。
2. **offline再現性**: 依存を事前materializeした状態で、network遮断のまま全required gateがpassする。permissionは`approval_policy: never` / `sandbox: workspace-write`である（[profile実測](../evaluations/profiles/candidate1-expanded12-global-m24-n5-r1.json)）。
3. **容量**: self-contained fixtureをrun数ぶんmaterializeするため、soft 3 GiB / hard 5 GiBの運用値（[`evaluation-storage-maintenance.md`](evaluation-storage-maintenance.md)）に収まる。
4. **gate所要時間**: 標準14項目 × A / B × `N=5`で140 run規模になるため、1 runのfull gateがこの規模で回る長さである。
5. **測定感度**: 複数subsystemへ跨る変更、2階層以上のdirectory構造、worker委譲が意味を持つ広さを持つ。単一責務のlibraryでは`CONTEXT` / `OWNER_ROLE` / `INDEPENDENCE`の差がKPIへ出ない。
6. **天井効果の回避**: 既存setでもF05 out-of-scopeとF07 dependency pairは全runが`quality_score` 100である（[`cases/README.md`](../evaluations/cases/README.md)）。modelが解法を記憶しているseedはこれを悪化させるため、seed diffの取得元commitの新しさで制御する。
7. **prompt target collision**: target側が既に`AGENTS.md`等のauthority fileを持つと、bundle overlayでcase条件やtarget側規則が消える。F09が`prompt_target_collision`でexecution blockedになったのと同型のriskである。
8. **case供給**: 公開issue / PR履歴からreal taskを取得でき、case追加根拠自体を第三者が検証できる。
9. **実行判断点coverage**: 既存14項目が担保するworker起動、context継承、model再入、read、validation、停止、result bindingなどの判断点に、target固有の題材を対応付けられる。実装言語の一致自体はgateにしない。

### 独立系列としての扱い

- `target_repository_ref`はcompatibility keyの一項目である（[`evaluations/AGENTS.md`](../evaluations/AGENTS.md)）。**公開target系列を既存result集合と同一比較へ混ぜない。** baselineから再取得する。
- 項目8（Claude Code CLI executor置換）と同一比較単位へ入れない。executor変更とtarget変更を同時に入れると効果を切り分けられない。
- rating contractをcase単位で作り直す以上、`quality_score`の絶対値をTHE-CAPTION系列と比較しない。観察できるのは各系列内の差と、方向の一致だけである。

### runtime再現性の完了境界

- `click`の容量、gate所要時間、通常環境での5回連続passはPhase 0で実測した。P1-cでbatch内・batch間分布、Std14で14 case横断の70 / 70 validを取得した。
- known-good実行環境は、固定target commitからwheelを作り、固定package versionを空venvへinstallする手順で再構築できた。既存共有venvは使用していない。
- network遮断下のfull gateと`uv lock --check --offline`を実測した。見込みではなく成功事実として記録する。
- 実測platformはmacOS arm64 / Python 3.14.5である。別OS / architectureは同じidentityと推定せず、新しいruntime identityとして扱う。
- instance境界、layout、descriptor、Click rating v10は固定した。Std14は固定contractとblind evidenceで採点できたため、target固有採点補助の自動adapter化は今回の完了条件ではない。別targetを追加するときに再評価する。

### 段階計画

1. **Phase 0**（実施済み）: gate 1〜9を判定し、`pallets/click`を選定した。追加実測により14項目すべての実行判断点へ対応可能と確認した。実測値と判定の正本は[`public-target-selection-phase0.md`](public-target-selection-phase0.md)とする。
2. **Phase 1 artifact準備**（実施済み）: instance、control-free bundle、F01型case、rating contract、set、P1-a profile、共有runtimeを固定した。
3. **Phase 1実測**（P1-c完了）: P1-a `N=1`で端から端までの成立、P1-b `N=5`でbatch内分布、P1-c `N=5 × B=3`でbatch間の散らばりを確認した。
4. **Phase 2 case展開**（実施済み）: 14 caseをqualificationし、追加caseだけ各`N=3`でBundle Aの成立を確認した。既存caseは追加のたびに再実行していない。
5. **Phase 3 Bundle A標準14**（実施済み）: `click-standard14-r1`を固定し、Bundle Aで70 / 70件をscore `4`として登録した。
6. **Phase 4 Bundle B水平比較**: Std14 baseline確立後に、1軸だけを変更した新しいCandidateをBundle Bとして固定し、同じStd14条件でBundle Aと比較する。content-identicalなBundle Bは作らない。

candidate bundleを作る段階ではcandidate作成前gate 9項目（[`prompts/AGENTS.md`](../prompts/AGENTS.md)）を通す。

## 11. 部分曖昧・長期タスクでの仕様確定境界の挙動（未着手）

**問い**: 仕様の8割が確定し2割が曖昧なまま進む複数段の作業で、`spec_ready`境界が過剰な問合せや誤停止を起こさずに働くか。

- 現状の測定範囲は単発課題である。標準14項目のA01は「未確定のrequired outcome valueが明確に一件ある」設計で、部分的な曖昧さが混在する長期作業を再現していない。該当するcaseもevaluation setも存在しない。
- 論文側の限界記述は[`execution-control-research-paper.md`](execution-control-research-paper.md)の第14節（限界10）である。このリポジトリの実務利用は対話形態であり、この条件は実利用へ近い。
- **着手条件**: 部分曖昧かつ複数段のcase familyを設計でき、誤停止と過剰問合せを区別する採点条件をrating contract revisionへ固定できた場合だけ着手する。
- **境界**: repository内のcase、TaskSpec、rating contract、promptの範囲だけで扱う。executor、runtime hook、外部wrapperの変更を解決策にしない。

## 12. model / CLI更新時の再測定範囲と費用記録（未着手）

**問い**: modelまたは実行環境の版が上がるたびに必要な再測定の範囲と費用を、着手判断の材料として残す。

- 結合はすでに2度観測されている。Codex CLI `0.144.0 → 0.146.0`で公開target側のC81とC125の互換キーが一致せず、tokenとelapsedの比較が成立しなくなった（[`Click C125 Medium Std14 r2 N=5`](../evaluations/targets/click/results/click-c125-reasoning-medium-standard14-r2-n5-cli0146_2026-07-31.md)）。model軸ではTerra / Lunaで品質とcostが維持されなかった（[`C125 model-axis`](../evaluations/results/candidate125-model-sol-terra-luna-v14-medium-standard14-n5-cli0146_2026-07-31.md)）。
- 低頻度failureはB20規模でしか観測されない。C95は`N=5`を通過し、B20の1,400件で2件落ちた。
- 費用の概算は[`candidate125-billing-equivalent-cost-comparison.md`](candidate125-billing-equivalent-cost-comparison.md)の単価による外挿で、標準14項目B20が1条件あたり約`$311`である。人間の設計・監査時間は含まない。
- **着手条件**: 次のmodelまたはCLI更新時に、再実行するbaselineの範囲（control-free、現行採用prompt、直近candidateのどれを何回か）を事前固定する明示判断があった場合だけ着手する。
- **境界**: 再測定範囲の固定と費用記録だけを扱う。executor置換やruntime強制の実装は含めない（項目8とは別項目）。

## 着手時の共通条件

- 一つのcandidateで一つのpredicateまたは一つの変更軸だけを扱う（[`prompts/AGENTS.md`](../prompts/AGENTS.md)のcandidate作成前gate9項目）
- 設計原則の正本は[`prompt-control-design-principles.md`](prompt-control-design-principles.md)
- 評価・採用・release・projectionは別gateとして記録する（[`repository-contract.md`](repository-contract.md)）
