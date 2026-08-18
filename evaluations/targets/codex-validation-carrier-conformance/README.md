# Codex validation carrier conformance target

> **状態**: `registered / namespaced / heldout_r1_source_frozen / runtime_measurement_qualified / p002_candidate_gate_passed / vcc6_p001_p002_n5_valid_60 / p002_score4_30 / tokens_minus_9_47_percent / elapsed_plus_10_72_percent / cost_gate_failed / standard14_not_allowed / vcc6_fixed_benchmark_prompt_only`

Codex上でvalidation planの途中result ingress、fail-fast、continuationおよびterminal projectionを実行traceと3 KPIで測るrepository targetである。target identityは[`target.json`](target.json)、登録理由と立ち上げgateは[`target登録設計`](../../../docs/codex-validation-carrier-target-registration-design.md)を正とする。

target固有のmaterializer、capability preflight、graderおよびtrace診断は[`runtime/adapter.py`](runtime/adapter.py)、qualification-only実行entrypointは[`runtime/runner.py`](runtime/runner.py)へ実装した。control-free N=1は6件すべてvalidで3 KPIを取得し、測定経路をqualificationした。ratingとruntimeの有効範囲は`target.json`を遡及変更せず、[`heldout-r1-runtime-registration-r1`](registrations/heldout-r1-runtime-registration-r1.json)へappend-onlyで固定する。

P002 bundleは固定済み一差分から作成し、[`p002-composition-binding-r1`](registrations/p002-composition-binding-r1.json)でP001直接親、Candidate用composition、生成bytesおよびtarget固有bundleを結び付けた。candidate-only N=1通過後にVCC6 P001/P002 N=5を実施し、60件すべてvalid、P002は30 / 30件がScore 4となった。tokensは9.47%減ったがelapsedは10.72%増えたため、[`comparison registration`](registrations/vcc6-p001-p002-n5-comparison-registration-r1.json)はcost gate不通過とStandard14非許可を固定する。これは採用、releaseまたはprojectionを意味しない。

VCC6は今後も同一portable full-agent改善系列の固定benchmarkとして再利用する。P002の結果を次Candidateの設計へ使った後も、case、fixture、TaskSpec、oracle、rating、runtimeおよび集計方法を変えず、prompt identityだけを比較変数とする。以後のVCC6 resultはblind evidenceとは呼ばず、VCC6内の比較根拠として扱う。この適用は[`VCC6固定benchmark policy`](registrations/vcc6-fixed-benchmark-policy-r1.json)を正とする。
