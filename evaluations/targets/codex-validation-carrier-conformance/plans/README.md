# Dispatch plans

preflight通過後のwrite-once dispatch plan索引を置く。control-free N=1 qualification planは[`codex-validation-carrier-control-free-heldout-r1-n1-dispatch-r1.json`](codex-validation-carrier-control-free-heldout-r1-n1-dispatch-r1.json)、preflightは[`codex-validation-carrier-control-free-heldout-r1-n1-preflight-r1.json`](codex-validation-carrier-control-free-heldout-r1-n1-preflight-r1.json)へ固定した。両artifactの`issued_slot_count=0`は発行前receiptとして不変に保持し、実際に発行・完了した6 slotは[`qualification result`](../results/codex-validation-carrier-control-free-heldout-r1-n1-qualification-r1.json)へ記録する。

P002 candidate-only N=1は[`codex-validation-carrier-p002-heldout-r1-n1-dispatch-r1.json`](codex-validation-carrier-p002-heldout-r1-n1-dispatch-r1.json)と[`codex-validation-carrier-p002-heldout-r1-n1-preflight-r1.json`](codex-validation-carrier-p002-heldout-r1-n1-preflight-r1.json)へ6 slotを固定した。両artifactの`issued_slot_count=0`は発行前receiptとして不変に保持し、発行・完了した6 slotは[`candidate gate result`](../results/codex-validation-carrier-p002-heldout-r1-n1-candidate-gate-r1.json)へ記録する。

VCC6 P001/P002 N=5は[`vcc6-p001-p002-n5-dispatch-r1.json`](vcc6-p001-p002-n5-dispatch-r1.json)へ60 logical slot、P002再利用6件、新規54件を固定し、[`vcc6-p001-p002-n5-preflight-r1.json`](vcc6-p001-p002-n5-preflight-r1.json)でprompt以外の互換条件一致を確認した。両artifactの`issued_slot_count=0`は発行前receiptとして不変に保持する。

共通runner N=1のr1 plan/preflightは全18 slotがfixture mode driftでmodel開始前に外部失敗となった履歴として保持する。固定Layer 1のmodeを復元したr2はP001の[`plan`](vcc6-p001-shared-runner-n1-dispatch-r2.json)と[`preflight`](vcc6-p001-shared-runner-n1-preflight-r2.json)、P002の[`plan`](vcc6-p002-shared-runner-n1-dispatch-r2.json)と[`preflight`](vcc6-p002-shared-runner-n1-preflight-r2.json)、P003の[`plan`](vcc6-p003-shared-runner-n1-dispatch-r2.json)と[`preflight`](vcc6-p003-shared-runner-n1-preflight-r2.json)へ各6 fresh slotを固定した。全18 slotは同一execution codeへbindし、保存済みresultを再利用しない。

P004 candidate-only N=1は[`plan`](vcc6-p004-shared-runner-n1-dispatch-r1.json)と[`preflight`](vcc6-p004-shared-runner-n1-preflight-r1.json)へfresh 6 slotを固定した。P003 r2とprompt identity以外の実効互換条件を機械照合してから発行した。

P005 candidate-only N=1は[`plan`](vcc6-p005-shared-runner-n1-dispatch-r1.json)と[`preflight`](vcc6-p005-shared-runner-n1-preflight-r1.json)へfresh 6 slotを固定した。P004とprompt identity以外の実効互換条件が完全一致し、private evidence rootが未作成であることを確認してから発行した。

P001・P003・P005のformal N=5はP001の[`plan`](vcc6-p001-shared-runner-n5-dispatch-r1.json)・[`preflight`](vcc6-p001-shared-runner-n5-preflight-r1.json)、P003の[`plan`](vcc6-p003-shared-runner-n5-dispatch-r1.json)・[`preflight`](vcc6-p003-shared-runner-n5-preflight-r1.json)、P005の[`plan`](vcc6-p005-shared-runner-n5-dispatch-r1.json)・[`preflight`](vcc6-p005-shared-runner-n5-preflight-r1.json)へ各30 fresh slotを固定した。発行前に非prompt条件の完全一致、issued 0件、全evidence root不在を確認した。
