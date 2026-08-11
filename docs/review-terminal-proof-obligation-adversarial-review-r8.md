# review terminal proof obligation qualification contract r8 敵対的レビュー

> **位置づけ**: 情報封鎖した独立レビュー完了／具体的反例あり／contract r8 rejected／Candidate未作成

## 1. operation receipt

- review operation identity: `review-terminal-proof-obligation-contract-r8-adversarial-review`
- source design identity: `review-terminal-proof-obligation-qualification-contract-r8`
- bound producer execution identity: `terminal_proof_contract_review_r8`
- result sender identity: `terminal_proof_contract_review_r8`
- packet identity: `review-terminal-proof-obligation-adversarial-review-packet-r8`
- packet raw SHA-256 before delivery: `cdb3974ec8f19309d528467f4ebf6ec8e77e46e9bad74a1dae4f3951ebb2fd76`
- packet raw SHA-256 after result: `cdb3974ec8f19309d528467f4ebf6ec8e77e46e9bad74a1dae4f3951ebb2fd76`
- allowed read: [`review-terminal-proof-obligation-adversarial-review-packet-r8.md`](review-terminal-proof-obligation-adversarial-review-packet-r8.md)だけ
- result admission: producer、sender、design、packetおよび形式が固定値と一致

## 2. independent result

以下は独立producerの返却結果を意味変更せず保存したものである。

```yaml
disposition: counterexample_found
design_identity: review-terminal-proof-obligation-qualification-contract-r8
packet_identity: review-terminal-proof-obligation-adversarial-review-packet-r8
boundary_identity: SCOPE-CERTIFICATE-REFERENCE-CLOSURE
contract_basis:
  - terminal_claim_reference_readyは、claim roleごとのrequired dependency edge集合を固定する一方、結果との完全一致をroleを含まないdependency member key集合だけで判定している。
  - required_dependency_member_setはdependency edge identityとdomain member input identityの集合であり、同じedgeが複数のclaim roleに必要な場合、そのrole別の必要referenceを区別しない。
counterexample:
  - claim role Aとclaim role Bが同じdependency edge Eの同じdomain member Mを必須入力とすることを事前固定する。reviewer resultがAに対するcertificate_referenceだけを持ち、Bに対するreferenceを欠いていても、結果のdependency member key集合は重複除去されたrequired_dependency_member_setの一要素「EとM」と完全一致し、存在するreferenceもadmission済みatomへ正しく結び付くため、現在の定義ではterminal_claim_reference_readyを満たし得る。これによりBのclaimを裏付けないresultが誤ってterminal受入れされる。
design_effect:
  - 必須reference集合をclaim role identity、dependency member key、dependency edge identityの組として定義し、resultのcertificate_referenceがそのrole別集合と重複なしで全単射になることを要求する一般規則へ変更する必要がある。
```

## 3. disposition

反例はclaim role別referenceの欠落をmember keyだけでは検出できないことを示すため、contract r8はrejectする。同じidentityを修正または再reviewしない。必須reference keyを`claim role identity × dependency edge identity × input identity`へ変更する規則を新しいcontract identityへ固定する。

## 4. 状態

`independent_review_complete / counterexample_found / result_admissible / contract_r8_rejected / revision_required / cases_not_materialized / candidate_not_created`
