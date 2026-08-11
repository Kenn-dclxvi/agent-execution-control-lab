# review terminal proof obligation qualification contract r5 敵対的レビュー

> **位置づけ**: 情報封鎖した独立レビュー完了／具体的反例あり／contract r5 rejected／Candidate未作成

## 1. operation receipt

- review operation identity: `review-terminal-proof-obligation-contract-r5-adversarial-review`
- source design identity: `review-terminal-proof-obligation-qualification-contract-r5`
- bound producer execution identity: `terminal_proof_contract_review_r5`
- result sender identity: `terminal_proof_contract_review_r5`
- packet identity: `review-terminal-proof-obligation-adversarial-review-packet-r5`
- packet raw SHA-256 before delivery: `f95ad5a6f49c00ee4f9e2b610f5b42f7b471f688e8b8117f180f5e8b744f64e0`
- packet raw SHA-256 after result: `f95ad5a6f49c00ee4f9e2b610f5b42f7b471f688e8b8117f180f5e8b744f64e0`
- allowed read: [`review-terminal-proof-obligation-adversarial-review-packet-r5.md`](review-terminal-proof-obligation-adversarial-review-packet-r5.md)だけ
- result admission: producer、sender、design、packetおよび形式が固定値と一致

## 2. independent result

以下は独立producerの返却結果を意味変更せず保存したものである。

```yaml
disposition: counterexample_found
design_identity: review-terminal-proof-obligation-qualification-contract-r5
packet_identity: review-terminal-proof-obligation-adversarial-review-packet-r5
boundary_identity: SCOPE-FINITE-DIRECT-MATCH
contract_basis:
  - finite direct match certificateは、先行固定authorityによるeffect集合とclosure sourceを要求するが、そのauthorityおよびclosure sourceの内容を現在snapshotで直接観測したreceiptを要求していない。
  - certificate成立時はreview operation、packet、review producerおよびreview invocationを作らず、not_requiredで終端する。
counterexample:
  - authority identityとclosure source identityだけが先行固定されている一方、現在snapshotのauthorityは未観測またはunreadableである。rootが過去に把握したeffect集合、target、end state、保持relationおよび追加effectなしという意味をcertificateへ補完すると、列挙されたcertificate項目を満たした形でnot_requiredを受け入れられる。しかし、現在authorityが同じ閉包を直接定めていることを証明するreceiptは存在せず、実際には追加effectがある可能性を排除できない。
design_effect:
  - finite direct match certificateへ、authorityとclosure sourceのsnapshot identity、直接observation identity、success receipt、およびreceiptが各effect、保持relation、一対一対応、追加effectなしの閉包へ直接結び付くことを必須化する。必要なreceiptがmissing、unreadableまたはterminal_failureならnot_requiredを受け入れず、rootによる過去状態や意味の補完を禁止する。
```

## 3. disposition

反例はreview不要判定の閉包根拠に現在snapshot receiptがない一般規則の欠陥を示すため、contract r5はrejectする。同じidentityを修正または再reviewしない。authorityとclosure sourceの現在snapshot直接receiptおよびeffect・relation・全件性との直接結合を新しいcontract identityへ固定する。

## 4. 状態

`independent_review_complete / counterexample_found / result_admissible / contract_r5_rejected / revision_required / cases_not_materialized / candidate_not_created`
