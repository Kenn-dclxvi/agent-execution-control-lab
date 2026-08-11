# review terminal proof obligation 敵対的レビュー系列

> **位置づけ**: r1〜r9完了済み設計監査の索引／全revision rejected／r10未作成／最小方向設計へ移行

## 結論

r1〜r9は全て情報封鎖した別producerが一件の具体的反例を返し、各source designをrejectした。r9の後は、反例を汎用schemaへ継ぎ足すほど当初の低密度設計から離れると判断し、r10を作らず系列を停止した。

現在の設計入口は[`review-terminal-proof-obligation-minimal-direction-design.md`](review-terminal-proof-obligation-minimal-direction-design.md)である。以下のrevisionは現在仕様として再利用せず、設計方向を棄却した一次記録として読む。

## revision一覧

| revision | contract | packet | independent result | 最初の反例 |
|---|---|---|---|---|
| r1 | [`contract`](review-terminal-proof-obligation-qualification-contract.md) | [`packet`](review-terminal-proof-obligation-adversarial-review-packet-r1.md) | [`result`](review-terminal-proof-obligation-adversarial-review-r1.md) | 同一input identityの競合atom |
| r2 | [`contract`](review-terminal-proof-obligation-qualification-contract-r2.md) | [`packet`](review-terminal-proof-obligation-adversarial-review-packet-r2.md) | [`result`](review-terminal-proof-obligation-adversarial-review-r2.md) | permission否定経路とreview後certificateの矛盾 |
| r3 | [`contract`](review-terminal-proof-obligation-qualification-contract-r3.md) | [`packet`](review-terminal-proof-obligation-adversarial-review-packet-r3.md) | [`result`](review-terminal-proof-obligation-adversarial-review-r3.md) | non-value stateの直接receipt欠落 |
| r4 | [`contract`](review-terminal-proof-obligation-qualification-contract-r4.md) | [`packet`](review-terminal-proof-obligation-adversarial-review-packet-r4.md) | [`result`](review-terminal-proof-obligation-adversarial-review-r4.md) | 宣言receipt identityと実receipt identityの非結合 |
| r5 | [`contract`](review-terminal-proof-obligation-qualification-contract-r5.md) | [`packet`](review-terminal-proof-obligation-adversarial-review-packet-r5.md) | [`result`](review-terminal-proof-obligation-adversarial-review-r5.md) | finite authority closureの現在snapshot receipt欠落 |
| r6 | [`contract`](review-terminal-proof-obligation-qualification-contract-r6.md) | [`packet`](review-terminal-proof-obligation-adversarial-review-packet-r6.md) | [`result`](review-terminal-proof-obligation-adversarial-review-r6.md) | counterexample claimとpacket atomの非結合 |
| r7 | [`contract`](review-terminal-proof-obligation-qualification-contract-r7.md) | [`packet`](review-terminal-proof-obligation-adversarial-review-packet-r7.md) | [`result`](review-terminal-proof-obligation-adversarial-review-r7.md) | 複数input dependencyの照合単位不足 |
| r8 | [`contract`](review-terminal-proof-obligation-qualification-contract-r8.md) | [`packet`](review-terminal-proof-obligation-adversarial-review-packet-r8.md) | [`result`](review-terminal-proof-obligation-adversarial-review-r8.md) | claim role別reference欠落の検出不能 |
| r9 | [`contract`](review-terminal-proof-obligation-qualification-contract-r9.md) | [`packet`](review-terminal-proof-obligation-adversarial-review-packet-r9.md) | [`result`](review-terminal-proof-obligation-adversarial-review-r9.md) | 観測値の意味内容がpacketにない |

## 状態

`r1_through_r9_review_complete / nine_counterexamples_admissible / all_revisions_rejected / revision_series_stopped / r10_not_created / minimal_direction_probe_passed / candidate_not_created`
