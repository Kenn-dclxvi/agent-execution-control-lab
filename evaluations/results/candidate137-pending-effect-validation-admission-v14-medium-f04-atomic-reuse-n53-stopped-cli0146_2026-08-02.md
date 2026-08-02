# Candidate137 F04 N=53追試停止結果

## 結論

Candidate137の同一F04 atomic poolを、既存29件から24件追加して合計53件まで測定した。追加24件はscore `4 / 2 = 23 / 1`だった。score `2`が一件出たため、事前停止条件どおり追加発行を停止した。累計はscore `4 / 2 = 52 / 1`である。

score `2`のrunでは、待っていた「一方のrequired effectが変更前に未観測」の状態が発生した。ただしCandidate137の`pending_effect_validation_admitted`には到達しなかった。変更前continuationの出力切れを受け、`EVIDENCE_GATE`がartifact変更前に停止したためである。

原因は、C136で追加した「unobserved effectを別のunsatisfied effectの変更開始拒否に使わない」という規則と、既存の「continuation resultで変更predicateと保持constraintの両方をbindできなければ停止する」という規則が同じ`EVIDENCE_GATE`内に併存していることである。後者が先に適用され、C137の変更後validation admissionへ制御を渡せなかった。

## 固定条件

- candidate: `the-caption-3ce91a4-pending-effect-validation-admission-r1`
- parent: `the-caption-3ce91a4-effect-local-change-admission-r1`
- bundle SHA-256: `1e8f777017c837c3bd696efdbcfc795d05d0d0c59f9fe9bcdd47cd36f3a44ad2`
- case: `TC-F04-WEB-AUDIT-COLUMN-VISIBILITY/r2`
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- model / reasoning: `gpt-5.6-sol` / `medium`
- Codex CLI / Python: `0.146.0` / `3.14.5`
- cumulative N / configured M: `53` / `24`
- reused / newly issued: `29` / `24`
- pool: `404b6fd4127512442d6e25c5b95932cc9a930db8506344aa50ec21085b8b0a6f`
- compatibility key: `febab57766c77c3de04f3dab752b20e1e3233bb3360f5c214aab6c488c7378e7`
- selection: `a1240b8ceab44918aa6b16a8dfa57c8a`
- analysis: `3f2e2a7b2dc0446f86734a08833d87c6`
- registered result: `1146581dcd624de8ae260f077bb3b4f3`
- excluded attempt: `0`

保存済みF04 reference result `cea34faab78149119808da7c59628955`を実行前にbindした。prompt以外のEvaluation set、case、fixture、TaskSpec、rating、model、reasoning、Agent/runtime/CLI、permission、executor挙動、token accountingを機械照合した。atomic run identityへNを混ぜず、同じpoolの不足24件だけを発行した。

## 品質結果

追加24件は24 / 24がvalidかつrateableだった。score分布は`4 = 23`、`2 = 1`である。外部失敗と除外attemptはなかった。

累計53件の中央値はquality `100.000`、token `193,902`、elapsed `117.097`秒だった。中央値は低頻度の停止を表さないため、品質gateはscore `2`の一件で不通過とする。

## score 2の挙動

- run: `ec3d27fea0f74905ab56ac63b05ec194`
- dispatch iteration: `14`
- artifact変更: なし
- required validation: 3件とも未実行
- failure: required changed path欠落、`npm ci`、lint、build未実行

最初のcontent waveで`const hasAuditKey = true;`を観測し、`[F04-C1]`が未充足であることは確定した。その後、同じtargetのcontinuationを一件発行した。

保存されたcommand stdoutには後方の`colSpan={hasAuditKey ? 7 : 6}`行が含まれる。しかしagentの受領判断は「出力が途中で切れ、`[F04-C2]`を確定できない」だった。agentはC2を`unobserved`として扱い、追加read、artifact変更、validationを行わず停止した。ここで重要なのは保存stdoutに文字列があるかではなく、次のmodel decisionへそのeffectの充足状態がbindされたかである。

## 制御の衝突

Candidate137が追加した規則はartifact変更後の`RECOVERY`にある。今回のrunはartifact変更前に停止したため、その規則は評価されていない。

一方、`EVIDENCE_GATE`には次の二つがある。

1. `unobserved effect`を、別の`unsatisfied effect`の変更開始拒否に使わない。
2. continuation後は、変更predicateと保持constraintの両方をbindできた場合だけartifact変更へ進み、そうでなければ停止する。

今回、C1は`unsatisfied`、C2は`unobserved`だった。規則1ならC1だけを変更できる。規則2はC2がbindされないため停止を要求する。実測では規則2が選ばれた。

したがって次の軸は、validation admissionの追加ではない。既存のeffect-local change admissionからCandidate137のpending validation admissionへ到達するhandoffを一意にすることである。具体的には、同一targetで`initial_change_effect_set`が非空なら、そのeffectだけの変更を発行し、未観測かつ変更対象外のeffectを変更後direct validationへ渡す。case名、symbol名、言語、executor出力制御には依存させない。

## 状態

`targeted_f04_atomic_reuse_n53_evaluated / score_2_observed / quality_gate_failed / pending_effect_state_observed / pending_validation_route_not_reached / evidence_gate_conflict_identified / result_registered / stopped`

## 結論表

| gate | 期待 | 実測 | 判定 |
| --- | ---: | ---: | --- |
| 追加valid / rateable | 24 / 24 | 24 / 24 | pass |
| 追加score `4` | 24 / 24 | 23 / 24 | fail |
| score `3`以下 | 0 | score `2`が1件 | stop |
| 累計score分布 | 全件`4` | `4 / 2 = 52 / 1` | fail |
| 変更前pending effect状態 | 1件以上発生まで継続 | 1件発生 | observed |
| pending validation admission | 発生runで到達 | artifact変更前停止 | not reached |
| 低Score原因 | Candidate137 predicateを判定可能 | 前段`EVIDENCE_GATE`衝突 | next boundary identified |
| F02 / F07 / 追加24 | score `3`以下なしの場合だけ | score `2`あり | not issued |
