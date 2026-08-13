# Candidate213 packet provenance review closure 実装監査

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
| Candidate | Candidate213 |
| prompt identity | `the-caption-3ce91a4-packet-provenance-review-closure-r1` |
| direct base | `the-caption-3ce91a4-result-effect-scope-r1`（Candidate147） |
| storage format | `instruction-suffixed/v1` |
| bundle SHA-256 | `64055b5aff47cb1372dcbca9f288d46abe4f6765e627db2545ac0275d2ae5663` |
| root `AGENTS.md` SHA-256 | `ee2418cfe61e48419f7e55b26de5e3a510f335d096cb3eb6f98853cd67a6aa63` |
| changed target | `AGENTS.md`だけ |
| 評価状態 | `not_evaluated` |

## 実装範囲

Candidate147のfull bundleを直接複製し、root `AGENTS.md`だけを変更した。manifestの19 targetのうち、`AGENTS.md`以外の18 targetはentry identityがCandidate147と一致する。

root本文は10,772 bytesから15,222 bytesとなり、差分は+4,450 bytesである。変更は次の二点だけである。

1. `EVIDENCE_GATE`の`implementation_bound`後の遷移を、review不要時のartifact変更と、review必要時の`PRECHANGE_REVIEW`へ分岐させた。
2. `PRECHANGE_REVIEW`を一条項追加し、packetへsemantic valueを供給したrepository source identityをreviewer起動前に閉鎖集合へ固定して、その集合へのreviewer readを禁止した。

Candidate147の`SPEC`、`PRODUCER`、`TERMINAL`、`CONTEXT`、`OWNER_ROLE`、`ROOT`、`INDEPENDENCE`、`DECISION_BOUNDARY`、`VALIDATION_CLOSURE`、`VALIDATION_PLAN`、`METHOD`、`RECOVERY`は逐語で保持した。開始identity制御も変更していない。

## 閉じた辺

```text
packetへsemantic valueを供給したrepository source identity
  -/-> 同じreviewerのrepository read target

別命題 / 直接確認 / provenance確認 / より強い証拠
  -/-> closed sourceへの例外
```

source identity集合が欠けた場合はreviewerを起動せず、reviewerによる集合の推測、拡張または再構成を許さない。値の意味やfield名から同一命題かどうかを判断せず、packet構築に使ったsource identityという直接観測だけでpermissionを閉じる。

## 維持した経路

- packetだけで具体的反例が成立すれば、repository readなしで`counterexample_found`を返せる。
- packetにterminal supportがなく、未投影sourceの値が残るdispositionを分ける場合は、そのsourceだけを読める。
- permission deniedとreview不要の通常経路を保持する。
- admissible `no_counterexample_found`だけが対応変更を開く。

これは「packetを先に判定する」などのtool順または判断順ではなく、read targetと閉鎖source集合のidentity membershipによるpermission境界である。

## 持ち込まなかった制御

- Candidate211のscope名からread対象を決める閉集合とexact JSON interface
- Candidate212のprompt本文
- case identity、固定path、field identity、scope identity、observation identityまたは期待disposition
- 成功runのtool順、判断順またはmodel step

Candidate211とCandidate212は保存traceの反例と正常経路だけに使い、prompt親または本文sourceとして扱っていない。

## 静的検証

次を確認した。

- exporterの`verify_bundle()`が成功した。
- manifestのbundle SHA-256再計算値が一致した。
- Candidate147との差分targetは`AGENTS.md`だけだった。
- 非変更targetは18件だった。
- Candidate147の既存12条項を逐語保持した。
- root本文にADR case identity、固定scope / observation identity、過去Candidate identityまたは`scope_evidence_binding`が含まれない。
- bundle identity snapshotへCandidate213を追記した。
- focused testとbundle storage testが成功した。
- `git diff --check`が成功した。

## 未評価境界

静的検証はsource-read permissionの効果を証明しない。初回評価はADR9 r2全9ケースN=5に限定し、packet投影元source再read 0件、ADR03からADR06のrepository read 0件、ADR07 / ADR09の必要な未投影paired observation保持、45 / 45 Score 4、review result admission / effect一致を確認する。全ゲートを通過するまでStandard14を開始しない。

## ADR9評価結果

ADR9 r2 N=5は45 / 45 valid、Score `4 / 1 = 43 / 2`だった。packet-counterexample readなしは17 / 20まで増え、投影元source再readもCandidate212の22回から6回へ減ったが、zero-toleranceの閉鎖には達しなかった。

ADR06でreviewer未起動の誤`unavailable`、ADR07で必要paired observationの代わりに投影元sourceを読んだ誤`unavailable`が各1件発生した。現在状態は`quality_failed / mechanism_failed / stopped`であり、Standard14を開始しない。

## 参照

- [Candidate213作成前設計](candidate213-packet-provenance-review-closure-design.md)
- [Candidate213方向監査](candidate213-packet-provenance-review-closure-direction-audit.md)
- [Candidate213 manifest](../prompts/candidates/the-caption-3ce91a4-packet-provenance-review-closure-r1/manifest.json)
- [Candidate147 manifest](../prompts/candidates/the-caption-3ce91a4-result-effect-scope-r1/manifest.json)
- [Candidate213 ADR9結果](../evaluations/results/candidate213-packet-provenance-review-closure-adr9-r2-n5_2026-08-14.md)
