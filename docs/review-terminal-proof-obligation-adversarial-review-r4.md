# review terminal proof obligation qualification contract r4 敵対的レビュー

> **位置づけ**: 情報封鎖した独立レビュー完了／具体的反例あり／contract r4 rejected／Candidate未作成

## 1. operation receipt

- review operation identity: `review-terminal-proof-obligation-contract-r4-adversarial-review`
- source design identity: `review-terminal-proof-obligation-qualification-contract-r4`
- bound producer execution identity: `terminal_proof_contract_review_r4`
- result sender identity: `terminal_proof_contract_review_r4`
- packet identity: `review-terminal-proof-obligation-adversarial-review-packet-r4`
- packet raw SHA-256 before delivery: `8b547d22697414bbd20d1c70b0dd1a4ff569c50eee4cc02b5fccce09deac1b0b`
- packet raw SHA-256 after result: `8b547d22697414bbd20d1c70b0dd1a4ff569c50eee4cc02b5fccce09deac1b0b`
- allowed read: [`review-terminal-proof-obligation-adversarial-review-packet-r4.md`](review-terminal-proof-obligation-adversarial-review-packet-r4.md)だけ
- result admission: producer、sender、design、packetおよび形式が固定値と一致

## 2. independent result

以下は独立producerの返却結果を意味変更せず保存したものである。

```yaml
disposition: counterexample_found
design_identity: review-terminal-proof-obligation-qualification-contract-r4
packet_identity: review-terminal-proof-obligation-adversarial-review-packet-r4
boundary_identity: SCOPE-STATE-RECEIPT
contract_basis:
  - packet_atomはobservation_receipt_identityを保持するが、state_receipt_validはreceipt semantic identityとatom.observation_receipt_identityの一致を要求していない
counterexample:
  - atom.observation_receipt_identityがR-CLAIMEDである一方、対応する唯一の直接receiptのsemantic identityがR-ACTUALであり、input、source、snapshot、observation、resultおよびvalueの各条件だけは一致するpacketは、現在の形式条件を通過できる
design_effect:
  - state_receipt_validへreceipt semantic identity == atom.observation_receipt_identityを追加し、宣言されたreceipt identityと実際の直接receiptを一対一に拘束する必要がある
```

## 3. disposition

反例は宣言receipt identityと実receiptの結合不足を示すため、contract r4はrejectする。同じidentityを修正または再reviewしない。`state_receipt_valid`へsemantic receipt identityの等値条件を新しいcontract identityで追加する。

## 4. 状態

`independent_review_complete / counterexample_found / result_admissible / contract_r4_rejected / revision_required / cases_not_materialized / candidate_not_created`
