# review terminal proof obligation qualification contract r7 敵対的レビュー

> **位置づけ**: 情報封鎖した独立レビュー完了／具体的反例あり／contract r7 rejected／Candidate未作成

## 1. operation receipt

- review operation identity: `review-terminal-proof-obligation-contract-r7-adversarial-review`
- source design identity: `review-terminal-proof-obligation-qualification-contract-r7`
- bound producer execution identity: `terminal_proof_contract_review_r7`
- result sender identity: `terminal_proof_contract_review_r7`
- packet identity: `review-terminal-proof-obligation-adversarial-review-packet-r7`
- packet raw SHA-256 before delivery: `b1ecd5151de471f5ff35960966d16fa97d1dd11466c6ecd594a5b49d939ce5b6`
- packet raw SHA-256 after result: `b1ecd5151de471f5ff35960966d16fa97d1dd11466c6ecd594a5b49d939ce5b6`
- allowed read: [`review-terminal-proof-obligation-adversarial-review-packet-r7.md`](review-terminal-proof-obligation-adversarial-review-packet-r7.md)だけ
- result admission: producer、sender、design、packetおよび形式が固定値と一致

## 2. independent result

以下は独立producerの返却結果を意味変更せず保存したものである。

```yaml
disposition: counterexample_found
design_identity: review-terminal-proof-obligation-qualification-contract-r7
packet_identity: review-terminal-proof-obligation-adversarial-review-packet-r7
boundary_identity: SCOPE-CERTIFICATE-REFERENCE-CLOSURE
contract_basis:
  - dependency_edgeは一つの閉じたinput identity domainを持てる一方、terminal_claim_reference_readyはresultのreference集合とrequired dependency edge集合の重複なし完全一致を要求する。
  - positive applicability predicateが複数入力を取る場合、全入力のatom referenceをcounterexample certificateへ含める必要がある。
counterexample:
  - positive applicability predicateの一つのdependency edgeが、二つのinput identityからなる閉じたdomainを持ち、両atomのsuccess receiptが揃って反例の適用性を証明している状態。このcertificateには同じdependency edge identityへ結び付く二つのatom referenceが必要だが、reference集合を一件のrequired dependency edge集合と重複なしで完全一致させられないため、成立すべきcounterexample terminalが拒否される。
design_effect:
  - terminal claimの完全一致単位をdependency edge集合ではなくdependency edgeとdomain member input identityの組の集合に変更するか、閉じたdomainの各memberへ一意なdependency edge identityを事前固定する一般規則が必要である。
```

## 3. disposition

反例は複数inputを持つdependency edgeの完全一致単位が不適切であることを示すため、contract r7はrejectする。同じidentityを修正または再reviewしない。required reference集合を`dependency edge identity × domain member input identity`の組へ展開する規則を新しいcontract identityへ固定する。

## 4. 状態

`independent_review_complete / counterexample_found / result_admissible / contract_r7_rejected / revision_required / cases_not_materialized / candidate_not_created`
