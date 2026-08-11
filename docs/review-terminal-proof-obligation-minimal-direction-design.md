# review terminal proof obligation 最小方向設計

> **位置づけ**: 方向性確認用の最小設計／実行可能probeあり／完全性未主張／Candidate未作成／Target評価未実施

## 結論

review terminalの完全性を汎用packet schemaで証明し切る方針を停止する。次の設計では、Candidate147が既に持つproducer、context、evidence、terminalおよび`result_effect_scope`を再利用し、追加する判断をterminalごとの証明責務だけへ限定する。

方向性は6条件の表形式試験で確認する。試験は「存在証明が成立した後の無関係なmissingを無視できる」「witness適用性または反例なし閉包に必要なmissingは止める」「authorityが直接閉じた変更はreviewしない」「permission否定を先行resultで回避しない」を区別できれば合格とする。

これは完全なprompt仕様、Target評価、Candidate実装または採用判断ではない。

## r1〜r9系列の停止

qualification contract r1〜r9は全て独立レビューで具体的反例を受け、全版をrejectした。反例を版ごとに閉じる過程で、次の機構が増えた。

- manifestとpacket atomの全単射
- 全stateのsnapshot／observation receipt
- permission否定専用certificate
- authority closureの現在snapshot receipt
- claim、dependency edge、input memberのreference全単射

r9でさらに観測値の意味内容を汎用packetへ持たせる必要が示された。この方向は、当初捨てると決めた全入力record、完全性schemaおよび高密度なidentity照合へ戻る。したがってr10は作らない。r1〜r9は、当該設計方向を採らない根拠として履歴保存する。

## 最小判定

方向性probeが扱う入力は次だけである。

```text
finite_direct_match
review_permission
witness_observed
witness_applicability_complete
witness_applicable
direct_conflict
design_effect_requires_general_change
closure_complete
```

判定は次の順序に限定する。

```text
if finite_direct_match:
    not_required -> completion_ready
elif not review_permission:
    unavailable without review
elif witness_observed and not witness_applicability_complete:
    unavailable
elif witness_observed
     and witness_applicable
     and direct_conflict
     and design_effect_requires_general_change:
    counterexample_found -> blocked
elif closure_complete:
    no_counterexample_found -> completion_ready
else:
    unavailable
```

`unrelated_missing`や`untrusted_prior_result`は入力事実としてcaseへ保持するが、それだけでterminalを変えない。どのmissingがwitness適用性またはclosureを変えるかは、TaskSpecまたは適用中authorityからcase入力へ固定する。新しい汎用dependency graphは作らない。

## 複雑性上限

- C147へ追加する新しいproducer roleは0件。
- review admissionだけを判定する独立workerは追加しない。
- 新しい汎用packet、receipt、registry、locatorまたはreference schemaを作らない。
- terminal値は既存の`counterexample_found | no_counterexample_found | unavailable`を使う。
- rootはreviewerの意味判断を補完しない。
- 方向性probeで不足する完全性はTarget評価caseとtrace oracleで検出する。
- 今後のレビューfindingが新しい汎用schemaを要求する場合は、条項を追加せずその設計方向をrejectする。

## 6条件

| condition | 区別する事実 | 期待route |
|---|---|---|
| Q1 | witness適用性、矛盾、design effectは成立。別のmissingは追加witness数だけに影響 | `counterexample_found / blocked` |
| Q2 | 見えているinstanceのwitness適用性がmissing | `unavailable` |
| Q3 | witnessなし、closureがmissing | `unavailable` |
| Q4 | witnessなし、closure完了 | `no_counterexample_found / completion_ready` |
| Q5 | authorityが複数effectと全件性を直接閉包 | reviewなしで`completion_ready` |
| Q6 | review permission否定、未信頼の先行resultあり | reviewなしで`unavailable` |

Q1とQ2はwitnessに見えるinstanceがある点を揃え、適用性dependencyの完了だけを変える。Q3とQ4はwitness不在を揃え、closure完了だけを変える。

## 実行可能probeの境界

- 公開判定: [`scripts/review_terminal_direction_probe.py`](../scripts/review_terminal_direction_probe.py)
- case入力: [`evaluations/sets/review-terminal-proof-obligation-direction-r1/cases.json`](../evaluations/sets/review-terminal-proof-obligation-direction-r1/cases.json)
- private oracle: [`evaluations/sets/review-terminal-proof-obligation-direction-r1/private/oracle.json`](../evaluations/sets/review-terminal-proof-obligation-direction-r1/private/oracle.json)
- 回帰試験: [`tests/test_review_terminal_direction_probe.py`](../tests/test_review_terminal_direction_probe.py)

probeはLLM挙動を測らない。6条件が同じ小さい判定軸で矛盾なく分離できるかだけを確認する。probe成功後に、同じ6条件を情報封鎖したTarget評価caseへmaterializeする。

## 方向性probe結果

2026-08-12に固定済み6条件を実行し、private oracleと6 / 6件で一致した。

- focused: `.venv/bin/python -m pytest tests/test_review_terminal_direction_probe.py -q`
- 結果: `4 passed`
- full discovery: `.venv/bin/python -m pytest -q`
- 結果: `1112 passed, 1762 subtests passed`

この成功は判定方向の内部整合だけを示す。LLMが同じrouteを安定して選ぶこと、機序trace、品質、採用、releaseまたはprojectionは未確認である。

## 状態

`minimal_direction_fixed / r1_through_r9_rejected / r10_not_created / six_case_probe_passed_6_of_6 / focused_4_passed / full_1112_passed_1762_subtests_passed / completeness_deferred_to_target_tests / candidate_not_created / target_evaluation_not_started`
