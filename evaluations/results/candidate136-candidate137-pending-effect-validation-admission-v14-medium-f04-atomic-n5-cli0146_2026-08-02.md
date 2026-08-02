# Candidate136 / Candidate137 F04 targeted result

## 結論

Candidate137のF04 N=5は5 / 5件すべてscore `4`だった。score `3`以下は0件で、必要な`hasAuditKey`変更、既存`colSpan`の保持、required validation 3件の成功も5 / 5だった。

ただし、Candidate137固有の`pending_effect_validation_admitted`経路は0 / 5件だった。全runがartifact変更前に`audit_match_key`、`Audit Key`、`colSpan`を同一targetから直接観測したため、未観測effectをrequired validationで閉じる状態へ入らなかった。

したがって品質gateは通過したが、C136低Scoreのfalse stopを解消したmechanism evidenceは得られていない。F02、F07、追加N、Standard14へは進めず、Candidate137を`mechanism_not_exercised / stopped`とする。

## 固定条件

- candidate: `the-caption-3ce91a4-pending-effect-validation-admission-r1`
- parent: `the-caption-3ce91a4-effect-local-change-admission-r1`
- bundle SHA-256: `1e8f777017c837c3bd696efdbcfc795d05d0d0c59f9fe9bcdd47cd36f3a44ad2`
- case: `TC-F04-WEB-AUDIT-COLUMN-VISIBILITY/r2`
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`
- model / reasoning: `gpt-5.6-sol` / `medium`
- Codex CLI / Python: `0.146.0` / `3.14.5`
- N / M: `5` / `24`
- pool: `404b6fd4127512442d6e25c5b95932cc9a930db8506344aa50ec21085b8b0a6f`
- compatibility key: `1a3b75ac2311cda9630a15db6ee0ab8c3d8e51bb46d4c63c44954fc5a958c24a`
- selection: `1ed4418b46af4e33b871bfc93d0fca29`
- analysis: `a77cee77582147c1809f03f97e612724`
- registered result: `7826a926b37a4ff59b2205ed509dfcc0`
- excluded attempt: 0

保存済みF04 reference result `cea34faab78149119808da7c59628955`を実行前にbindした。prompt以外のEvaluation set、case、fixture、TaskSpec、rating、model、reasoning、Agent/runtime/CLI、permission、executor挙動、token accountingを機械照合し、preflightが5 slotを承認した後だけ発行した。

## 結果

| iteration | run | score | prechange effect観測 | artifact変更 | validation |
| ---: | --- | ---: | --- | --- | --- |
| 1 | `1229d2761fd14e088cdcad71d972bf7b` | 4 | 3 member直接観測 | `hasAuditKey`一行 | 3 / 3成功 |
| 2 | `14032ce0e0b4420d8c8256e31d64bece` | 4 | 3 member直接観測 | `hasAuditKey`一行 | 3 / 3成功 |
| 3 | `5fb1761e663544088c228898e32cb323` | 4 | 3 member直接観測 | `hasAuditKey`一行 | 3 / 3成功 |
| 4 | `63be0d8725244903abd53d03544ccd25` | 4 | 3 member直接観測 | `hasAuditKey`一行 | 3 / 3成功 |
| 5 | `edf1c9a4183e4641bb1da38d7410d801` | 4 | 3 member直接観測 | `hasAuditKey`一行 | 3 / 3成功 |

5件中央値はquality `100.000`、token `166,806`、elapsed `81.108`秒だった。mechanism gateが未成立なので、効率改善または採用の根拠には使わない。

## 挙動の判定

全5件の最初のevidence waveは`App.tsx`のcontentを取得し、次の変更前invocationで`audit_match_key|Audit Key|colSpan`を同一targetから検索した。その後に`hasAuditKey = true`だけを一行変更した。

このため次は成立した。

- 観測済み未充足effectの必要変更: 5 / 5
- 観測済み充足済み`colSpan`の保持: 5 / 5
- initial patch failure: 0 / 5
- required validation完備: 5 / 5
- 許可外artifact変更: 0 / 5

一方、`effect_prechange_state(effect)=unobserved`になったrunは0件だった。したがって`required_effects_validation_ready`がpending observerを根拠にvalidationへ進んだrunも0件である。5 / 5 score `4`は、C136でも成立していた通常経路の再現であり、C137の追加経路の成功を示さない。

## 汎用性の解釈

Candidate137のpredicateはcase ID、言語、symbol名を含まず、複数effect taskへ一般化した形である。しかし今回の実測はF04の通常経路だけであり、次をまだ証明していない。

- 未観測effectを持つ変更後状態でdirect observerだけをadmitできること
- 一般的なtest、lint、build成功をeffectの直接証明へ誤変換しないこと
- direct observerのないpending effectで停止を維持すること
- F02の複数source effectやF07のdependency pairで同じ境界が成立すること

F04 Nを単純に増やせば低頻度でpending経路が出る可能性はある。ただしそれはmechanismを直接切り分ける試験ではない。次は保存traceまたは評価artifactの範囲で、開始状態を作為的に欠落させずにpending observer admissionを直接観測できる既存caseがあるかを先に監査する。

## 状態

`targeted_f04_n5_evaluated / quality_gate_passed / required_edit_5_of_5 / satisfied_effect_change_0_of_5 / initial_apply_failure_0_of_5 / validation_complete_5_of_5 / pending_effect_route_0_of_5 / mechanism_not_exercised / result_registered / stopped`

## 結論表

| gate | 期待 | 実測 | 判定 |
| --- | ---: | ---: | --- |
| valid / rateable | 5 / 5 | 5 / 5 | pass |
| score `4` | 5 / 5 | 5 / 5 | pass |
| score `3`以下 | 0 / 5 | 0 / 5 | pass |
| 必要な未充足effect変更 | 5 / 5 | 5 / 5 | pass |
| 充足済みまたは未観測effectの変更 | 0 / 5 | 0 / 5 | pass |
| initial patch failure | 0 / 5 | 0 / 5 | pass |
| required validation完備 | 5 / 5 | 5 / 5 | pass |
| pending effect observer経路 | 発生時にfalse stop 0件 | 発生0 / 5 | not exercised / stop |
| direct observerなしpending effectでvalidation開始 | 0 / 5 | 0 / 5 | pass（対象経路なし） |
| validation result前の全effect完了判定 | 0 / 5 | 0 / 5 | pass |
