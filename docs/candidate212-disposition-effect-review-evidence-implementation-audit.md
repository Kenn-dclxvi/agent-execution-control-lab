# Candidate212 disposition効果限定review evidence 実装監査

## 状態

- `candidate_created`
- `static_verification_passed`
- `ADR9_completed`
- `quality_passed`
- `mechanism_failed`
- `stopped`
- `adoption_not_decided`
- `release_not_created`
- `projection_not_performed`

## Candidate identity

| 項目 | 値 |
|---|---|
| Candidate | Candidate212 |
| prompt identity | `the-caption-3ce91a4-disposition-effect-review-evidence-r1` |
| direct base | `the-caption-3ce91a4-result-effect-scope-r1`（Candidate147） |
| storage format | `instruction-suffixed/v1` |
| bundle SHA-256 | `81b2f788f4bb0079c1af9e874948f8029bb949c6318dc343a0f56f1c29cd5c1c` |
| root `AGENTS.md` SHA-256 | `3c32f53af82075e0ac798c0fa4fc109d69341628c64f2d46cd3bee4cb82e19f4` |
| changed target | `AGENTS.md`だけ |
| 評価状態 | `not_evaluated` |

## 実装範囲

Candidate147のfull bundleを直接複製し、root `AGENTS.md`だけを変更した。manifestの19 targetのうち、`AGENTS.md`以外の18 targetはentry identityがCandidate147と一致する。

root本文は10,772 bytesから14,555 bytesとなり、差分は+3,783 bytesである。変更は次の二点だけである。

1. `EVIDENCE_GATE`の`implementation_bound`後の遷移を、review不要時のartifact変更と、review必要時の`PRECHANGE_REVIEW`へ分岐させた。
2. `PRECHANGE_REVIEW`を一条項追加し、terminal supportが未成立で、requested resultの異なる値が残るterminal dispositionを分け得る場合だけrepository evidence consumerを成立させる。

Candidate147の`SPEC`、`PRODUCER`、`TERMINAL`、`CONTEXT`、`OWNER_ROLE`、`ROOT`、`INDEPENDENCE`、`DECISION_BOUNDARY`、`VALIDATION_CLOSURE`、`VALIDATION_PLAN`、`METHOD`、`RECOVERY`は逐語で保持した。開始identity制御も変更していない。

## 閉じた辺

```text
manifest membership / scope label / reviewer ownership
  -/-> unresolved proposition

model-visible packet value
  -/-> direct sourceが存在するという理由だけでunobservedへ再分類

terminal dispositionを変えないrequested result
  -/-> repository evidence consumer
```

packetまたはadmission済み観測で一つのallowed terminal kindがsupportされた時点で、そのkindを変えない未発行観測は失効する。terminal kindがまだsupportされず、具体的命題が未確定であり、requested resultの取り得る値が残るdispositionを分ける場合だけreadを許可する。

## 維持した経路

- packetだけで具体的反例が成立すれば、readなしで`counterexample_found`を返せる。
- packetだけでは反例がなく、必須観測のsuccessとnon-valueが`no_counterexample_found`と`unavailable`を分ける場合はreadを許可する。
- permission deniedとreview不要の通常経路を保持する。
- admissible `no_counterexample_found`だけが対応変更を開く。

これらは「packetを先に判定する」などのtool順または判断順ではなく、read発行時のpermission predicateとして実装した。

## 持ち込まなかった制御

- Candidate211の`scope_evidence_binding`、scope名からread対象を決める閉集合およびexact JSON interface
- Candidate208からCandidate210までのresult-kind状態機械、certificate deficitおよび四状態frontier
- case identity、固定path、scope identity、observation identityまたは期待disposition
- 成功runのtool順、判断順またはmodel step

Candidate208、Candidate210、Candidate211は保存traceの反例と正常経路だけに使い、prompt親または本文sourceとして扱っていない。

## 静的検証

次を確認した。

- exporterの`verify_bundle()`が成功した。
- manifestのbundle SHA-256再計算値が一致した。
- Candidate147との差分targetは`AGENTS.md`だけだった。
- 非変更targetは18件だった。
- Candidate147の既存12条項を逐語保持した。
- root本文にADR case identity、固定scope / observation identity、過去Candidate identityまたは`scope_evidence_binding`が含まれない。
- bundle identity snapshotへCandidate211とCandidate212を追記した。
- focused testとbundle storage testが成功した。
- `git diff --check`が成功した。

## ADR9評価結果

ADR9 r2 N=5は45 / 45 valid、45 / 45 Score 4だった。terminal、artifact境界、reviewer cardinality、review result admissionおよびeffectは全件一致した。

一方、packet-counterexample 20件でrepository readは17回、readなしは9 / 20件だった。必要なADR07 / ADR09のpaired-scope observationは各5 / 5で保持したが、projection元sourceの追加readにより、固定した単一direct observation経路との一致はADR07が3 / 5、ADR09が2 / 5だった。

詳細は[ADR9結果](../evaluations/results/candidate212-disposition-effect-review-evidence-adr9-r2-n5_2026-08-13.md)を参照する。現在状態は`quality_passed / mechanism_failed / stopped`であり、Standard14は開始しない。

## 参照

- [Candidate212作成前設計](candidate212-disposition-effect-review-evidence-design.md)
- [Candidate212方向監査](candidate212-disposition-effect-review-evidence-direction-audit.md)
- [Candidate212 manifest](../prompts/candidates/the-caption-3ce91a4-disposition-effect-review-evidence-r1/manifest.json)
- [Candidate147 manifest](../prompts/candidates/the-caption-3ce91a4-result-effect-scope-r1/manifest.json)
- [Candidate212 ADR9結果](../evaluations/results/candidate212-disposition-effect-review-evidence-adr9-r2-n5_2026-08-13.md)
