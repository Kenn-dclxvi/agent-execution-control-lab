# Registrations

heldout r1のsource、rating、runtime実装およびcontrol-free qualification resultのappend-only bindingは[`heldout-r1-runtime-registration-r1.json`](heldout-r1-runtime-registration-r1.json)を正とする。

`target.json`を遡及変更せず、P002 bundle bindingは[`p002-composition-binding-r1.json`](p002-composition-binding-r1.json)、candidate-only gate通過とpaired N=5許可は[`p002-candidate-gate-registration-r1.json`](p002-candidate-gate-registration-r1.json)へ追記した。VCC6 P001/P002 N=5のcost gate不通過とStandard14非許可は[`vcc6-p001-p002-n5-comparison-registration-r1.json`](vcc6-p001-p002-n5-comparison-registration-r1.json)を正とする。

P002後続でもVCC6を変更せずprompt identityだけを変える比較規則は[`vcc6-fixed-benchmark-policy-r1.json`](vcc6-fixed-benchmark-policy-r1.json)を正とする。これは既存source freezeまたはresultを変更せず、blind性と固定benchmark内の比較可能性を分離するappend-only policyである。

P001を直接親、P002を非継承の失敗反例とするP003 bundle bindingは[`p003-composition-binding-r1.json`](p003-composition-binding-r1.json)を正とする。このbinding単独ではVCC6 Profile、dispatch planまたは評価slotを許可せず、後続N=1の状態は下記result registrationを正とする。

P001を直接親、P002とP003を非継承の反例とし、Codex carrier contractをtask実行前に固定するP004 bundle bindingは[`p004-composition-binding-r1.json`](p004-composition-binding-r1.json)を正とする。このbinding単独ではVCC6 Profile、dispatch planまたは評価slotを許可せず、後続N=1の状態は下記result registrationを正とする。

P004 candidate-only N=1の共通runner実行gateは[`vcc6-p004-prompt-only-shared-runner-foundation-r1.json`](vcc6-p004-prompt-only-shared-runner-foundation-r1.json)を正とする。6 / 6件valid、Score 4が5件、Score 1が1件となった停止判断とN=5不許可は[`vcc6-p004-shared-runner-n1-result-registration-r1.json`](vcc6-p004-shared-runner-n1-result-registration-r1.json)を正とする。

P001を直接親、P002からP004までを非継承の反例とし、terminal projectionだけへouter output permissionを固定するP005 bundle bindingは[`p005-composition-binding-r1.json`](p005-composition-binding-r1.json)を正とする。共通runner実行gateは[`vcc6-p005-prompt-only-shared-runner-foundation-r1.json`](vcc6-p005-prompt-only-shared-runner-foundation-r1.json)、6 / 6件Score 4・機序成立とN=5許可は[`vcc6-p005-shared-runner-n1-result-registration-r1.json`](vcc6-p005-shared-runner-n1-result-registration-r1.json)を正とする。

P001・P003・P005のfresh N=5実行gateは[`vcc6-p001-p003-p005-shared-runner-n5-foundation-r1.json`](vcc6-p001-p003-p005-shared-runner-n5-foundation-r1.json)、発行前互換性は[`preflight registration`](vcc6-p001-p003-p005-shared-runner-n5-preflight-registration-r1.json)を正とする。P005の品質・機序通過、P003比2 KPI改善、P001比elapsed増によるStandard14不許可は[`result registration`](vcc6-p001-p003-p005-shared-runner-n5-result-registration-r1.json)を正とする。

P005を直接親とし、全member commit前のfrontier途中result ingressだけをCodex platform blockで閉じるP006 bundle bindingは[`p006-composition-binding-r1.json`](p006-composition-binding-r1.json)を正とする。P006は構成・一枚化・bindingまで完了したが、Standard14 preflight未作成、評価slot 0件の`candidate_bundle_bound_not_evaluated`である。

Candidate名を持たない共通runnerのN=1実行gateは[`vcc6-prompt-only-shared-runner-foundation-r1.json`](vcc6-prompt-only-shared-runner-foundation-r1.json)を正とする。初回18 slotのmodel開始前外部失敗は[`issuance failure r1`](vcc6-p001-p002-p003-shared-runner-n1-issuance-failure-r1.json)、固定Layer 1へのmode復元は[`fixture mode recovery receipt`](vcc6-heldout-r1-fixture-mode-recovery-receipt-r1.json)へ保持する。回復後のP001・P002・P003のprompt以外の条件一致とfresh 18 slotの発行前状態は[`global preflight r2`](vcc6-p001-p002-p003-shared-runner-n1-preflight-registration-r2.json)を正とし、旧resultは再利用しない。

回復後N=1の18 / 18 valid、Score 4およびP003 mechanism 6 / 6と、安定傾向を主張せずN=5だけを許可するgateは[`shared runner N=1 result registration`](vcc6-p001-p002-p003-shared-runner-n1-result-registration-r1.json)を正とする。
