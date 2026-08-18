# Dispatch plans

preflight通過後のwrite-once dispatch plan索引を置く。control-free N=1 qualification planは[`codex-validation-carrier-control-free-heldout-r1-n1-dispatch-r1.json`](codex-validation-carrier-control-free-heldout-r1-n1-dispatch-r1.json)、preflightは[`codex-validation-carrier-control-free-heldout-r1-n1-preflight-r1.json`](codex-validation-carrier-control-free-heldout-r1-n1-preflight-r1.json)へ固定した。両artifactの`issued_slot_count=0`は発行前receiptとして不変に保持し、実際に発行・完了した6 slotは[`qualification result`](../results/codex-validation-carrier-control-free-heldout-r1-n1-qualification-r1.json)へ記録する。

P002 candidate-only N=1は[`codex-validation-carrier-p002-heldout-r1-n1-dispatch-r1.json`](codex-validation-carrier-p002-heldout-r1-n1-dispatch-r1.json)と[`codex-validation-carrier-p002-heldout-r1-n1-preflight-r1.json`](codex-validation-carrier-p002-heldout-r1-n1-preflight-r1.json)へ6 slotを固定した。両artifactの`issued_slot_count=0`は発行前receiptとして不変に保持し、発行・完了した6 slotは[`candidate gate result`](../results/codex-validation-carrier-p002-heldout-r1-n1-candidate-gate-r1.json)へ記録する。

VCC6 P001/P002 N=5は[`vcc6-p001-p002-n5-dispatch-r1.json`](vcc6-p001-p002-n5-dispatch-r1.json)へ60 logical slot、P002再利用6件、新規54件を固定し、[`vcc6-p001-p002-n5-preflight-r1.json`](vcc6-p001-p002-n5-preflight-r1.json)でprompt以外の互換条件一致を確認した。両artifactの`issued_slot_count=0`は発行前receiptとして不変に保持する。
