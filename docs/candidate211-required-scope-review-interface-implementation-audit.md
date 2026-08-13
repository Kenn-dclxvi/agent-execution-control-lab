# Candidate211 必須scope消費review入出力境界 実装監査

## 状態

- `candidate_created`
- `static_verification_passed`
- `ADR9_completed`
- `quality_failed`
- `mechanism_failed`
- `stopped`
- `adoption_not_decided`
- `release_not_created`
- `projection_not_performed`

## Candidate identity

| 項目 | 値 |
|---|---|
| Candidate | Candidate211 |
| prompt identity | `the-caption-3ce91a4-required-scope-review-interface-r1` |
| direct base | `the-caption-3ce91a4-result-effect-scope-r1`（Candidate147） |
| storage format | `instruction-suffixed/v1` |
| bundle SHA-256 | `40b9c14cadf390a02fa242469f0e0c8bb6fcb53d94de239ca039b74321e265b9` |
| changed target | `AGENTS.md`だけ |
| 評価状態 | `not_evaluated` |

## 実装範囲

Candidate147のfull bundleを直接複製し、root `AGENTS.md`だけを変更した。manifestの19 targetのうち、`AGENTS.md`以外の18 targetはentry identityがCandidate147と一致する。

root本文は10,772 bytesから14,415 bytesとなり、差分は+3,643 bytesである。変更は次の二点だけである。

1. `EVIDENCE_GATE`の`implementation_bound`後の遷移を、review不要時のartifact変更と、review必要時の`PRECHANGE_REVIEW`へ分岐させた。
2. `PRECHANGE_REVIEW`を一条項追加し、review applicability、permission、packet封鎖、必須scopeを消費するdirect read閉集合、三terminal判定、exact external `disposition`、result admissionおよび対応変更への局所effectを一つのlifecycleとして固定した。

Candidate147の`SPEC`、`PRODUCER`、`TERMINAL`、`CONTEXT`、`OWNER_ROLE`、`ROOT`、`INDEPENDENCE`、`DECISION_BOUNDARY`、`VALIDATION_CLOSURE`、`VALIDATION_PLAN`、`METHOD`、`RECOVERY`は逐語で保持した。開始identity制御も変更していない。

## 閉じた辺

### 入力側

```text
manifest membership
  -/-> reviewer direct read

packet projection source
  -/-> same review direct reread
```

`review_allowed_read_set`へ入るのは、packet projectionで未充足の必須scopeを直接かつ一意に充足するTaskSpec-fixed manifest targetだけである。manifestにあるだけのtarget、packet projection元source、必須scopeのconsumerを持たないtargetは除外する。reviewerによる集合の追加、置換、再分類も禁止した。

### 出力側

```text
internal predicate name or prose
  -/-> admitted external disposition
```

外部resultはexact field `disposition`へ`counterexample_found | no_counterexample_found | unavailable`のいずれか一つを返す。内部名、別名、説明文は代替にならず、対応するready predicate、producer identity、subject identity、使用input、forbidden input不使用が一致した場合だけadmitする。

## 持ち込まなかった制御

- Candidate196以降の複数adjudication operation
- Candidate208のresult-kind evidence domain
- Candidate209のcertificate deficit
- Candidate210の四つのdescriptor stateとobservation frontier
- case identity、特定observation identity、特定path、期待disposition
- 成功runのtool順、判断順、model step

Candidate175、Candidate179、Candidate210は設計根拠となる観測と反例に限定し、prompt親または本文sourceとして扱っていない。

## 静的検証

次を確認した。

- exporterの`verify_bundle()`が成功した。
- manifestのbundle SHA-256再計算値が一致した。
- Candidate147との差分targetは`AGENTS.md`だけだった。
- 非変更targetは18件だった。
- root本文にADR case identity、特定paired-scope observation identity/path、過去Candidate identity、多値state名が含まれない。
- `git diff --check`が成功した。
- Candidate bundle、設計、方向監査および索引の参照先が存在する。

## ADR9評価結果

ADR9 r2 N=5は45 / 45 valid、Score `4 / 1 = 39 / 6`だった。品質不通過6件はADR03とADR04で期待`blocked`に対して`unavailable`となった。

packet-counterexample 20件でrepository readは18回、readなしは6 / 20件、scope外paired readは13回、packet projection元source再readは11回だった。必要なADR07とADR09のdirect observationは各5 / 5で保持したが、exact JSON `disposition` fieldは24 / 30、期待値一致は20 / 30だった。

詳細は[ADR9結果](../evaluations/results/candidate211-required-scope-review-interface-adr9-r2-n5_2026-08-13.md)を参照する。現在状態は`quality_failed / mechanism_failed / stopped`であり、Standard14は開始していない。

## 次のgate

停止条件に従い、Candidate211のrepair rerun、ADR9累積N=20、Standard14、採用、releaseおよびprojectionへ進めない。

## 参照

- [Candidate211作成前設計](candidate211-required-scope-review-interface-design.md)
- [Candidate211方向監査](candidate211-required-scope-review-interface-direction-audit.md)
- [Candidate211 manifest](../prompts/candidates/the-caption-3ce91a4-required-scope-review-interface-r1/manifest.json)
- [Candidate147 manifest](../prompts/candidates/the-caption-3ce91a4-result-effect-scope-r1/manifest.json)
- [Candidate210 ADR9 N=5結果](../evaluations/results/candidate210-review-evidence-state-closure-adr9-r2-n5_2026-08-13.md)
