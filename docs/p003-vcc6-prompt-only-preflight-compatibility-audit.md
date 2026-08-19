# P003 VCC6 prompt-only preflight互換性監査

> [!IMPORTANT]
> **状態**: `p003_bundle_bound / vcc6_fixed / prompt_only_required / existing_dispatch_entrypoints_candidate_specific / separate_foundation_maintenance_authorized / shared_runner_implemented / first_dispatch_external_failure_before_model / fixture_modes_recovered / fresh_p001_p002_p003_n1_valid_18 / n1_no_stability_claim`

## 結論

P003 Candidate bundleは固定できたが、現行VCC6実行entrypointのままP003用Profileとpreflightを作ることはできない。

- `runner_p002.py`はP002のProfile、dispatch series、prompt identity、candidate bindingおよび`candidate_only_p002_gate`を定数として要求する。
- `runner_vcc6_paired.py`は比較armをP001とP002へ固定し、Profile、plan、preflightおよびcomparison contractもP001/P002専用identityへ固定する。
- P003用にいずれかを複製または変更すると、preflightがbindするexecution code hashも変わる。P001/P002保存済みresultと比較したとき、prompt identity以外も差分になる。

したがって、P003の6 slotを発行してから参考値へ降格する進め方は採らない。P003 Profile、dispatch plan、preflightおよび評価slotは作成していない。

## 固定済み目的との関係

VCC6固定benchmark policyは、case、fixture、TaskSpec、oracle、rating、model、reasoning、Agent/runtime/CLI、permission、executor挙動、token accountingおよび集計方法を固定し、prompt identityだけを実験変数とする。Candidate固有runnerを新設する案は、このうちexecutorの実装identityを変えるため、現在の比較系列には入れられない。

これはP003 promptの失敗ではなく、評価発行前に検出した旧実行経路の互換性gate不通過である。

## 次に必要な別作業

評価を再開するには、Candidate identityをデータとして受け取る一つの共通実行entrypointを先に固定し、比較する全promptを同じentrypoint bytes、同じProfile schema、同じpreflight contractおよび同じexecutor挙動へbindする必要がある。

この作業はprompt Candidateの変更ではなく評価基盤の保守である。利用者の明示的な続行依頼後、Candidate名を持たない[`runner_prompt_only.py`](../evaluations/targets/codex-validation-carrier-conformance/runtime/runner_prompt_only.py)を別作業として実装した。新しい共通entrypointでは既存P001/P002 resultを再利用せず、P001、P002、P003を同じrunner bytesでfresh N=1へbindした。

3 Profileはidentityとprompt bundle以外の条件が一致し、各preflightは同じadapter、base runnerおよびprompt-only runner hashを持つ。初回18 slotはfixture file modeが固定値より狭くなっていたためmodel開始前に全件外部失敗となった。この履歴を再利用禁止で保持し、modeを固定Layer 1へ復元して新しいdispatch identityを発行した。

回復後の18件はすべてvalidかつScore 4だった。mechanismはP001が2 / 6、P002とP003が6 / 6である。P003のtokens合計は284,313でP001比29.97%、P002比10.39%少なく、elapsed合計は216.02秒でP001比19.22%、P002比5.64%多い。これはN=1の選択gateであり、安定したcost傾向とは扱わない。一次値は[`shared runner N=1 result`](../evaluations/targets/codex-validation-carrier-conformance/results/vcc6-p001-p002-p003-shared-runner-n1-result-r1.json)を正とする。

## 禁止する回避

- P003 identityだけをP002として偽装する。
- P003用runnerを作り、executor差を無視して既存resultと比較する。
- preflightを省略して6 slotを先に発行する。
- VCC6のCase、ratingまたはruntime条件をP003向けに変える。
- 不一致を発行後に発見して参考値へ降格する。
