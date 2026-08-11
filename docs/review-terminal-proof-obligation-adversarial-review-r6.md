# review terminal proof obligation qualification contract r6 敵対的レビュー

> **位置づけ**: 情報封鎖した独立レビュー完了／具体的反例あり／contract r6 rejected／Candidate未作成

## 1. operation receipt

- review operation identity: `review-terminal-proof-obligation-contract-r6-adversarial-review`
- source design identity: `review-terminal-proof-obligation-qualification-contract-r6`
- bound producer execution identity: `terminal_proof_contract_review_r6`
- result sender identity: `terminal_proof_contract_review_r6`
- packet identity: `review-terminal-proof-obligation-adversarial-review-packet-r6`
- packet raw SHA-256 before delivery: `4c7b0399eef7f3792b0c3cc2ae38ee733560b8cce2d5e4ee5a06e59bc4302fef`
- packet raw SHA-256 after result: `4c7b0399eef7f3792b0c3cc2ae38ee733560b8cce2d5e4ee5a06e59bc4302fef`
- allowed read: [`review-terminal-proof-obligation-adversarial-review-packet-r6.md`](review-terminal-proof-obligation-adversarial-review-packet-r6.md)だけ
- result admission: producer、sender、design、packetおよび形式が固定値と一致

## 2. independent result

以下は独立producerの返却結果を意味変更せず保存したものである。

```yaml
disposition: counterexample_found
design_identity: review-terminal-proof-obligation-qualification-contract-r6
packet_identity: review-terminal-proof-obligation-adversarial-review-packet-r6
boundary_identity: SCOPE-COUNTEREXAMPLE-CERTIFICATE
contract_basis:
  - counterexample_certificateはpositive applicability predicateの全入力値にだけsuccess receiptを要求し、concrete witness、normative contract、fixed design treatment、直接矛盾、design effectをadmission済みpacket atomの現在値へ直接結び付けるreceiptまたはvalue identityを要求していない。
  - rootはreview実行経路でcertificate、dependency receipt、producerおよびpacket identityの一致だけを機械検査し、意味判断を補完しない。
counterexample:
  - positive applicability predicateの全入力値とsuccess receiptは揃っているが、certificateに記載されたconcrete witness identityが現在snapshotで観測されておらず、fixed design treatmentと直接矛盾もpacket atomのvalue identityへ結び付いていない状態で、各記載欄だけを埋めたcertificateを返す。このcertificateは現行の明示要件を満たしてrootの機械検査を通り得る一方、存在しないwitnessまたは実際には矛盾しない内容による誤ったcounterexample_foundを終端受入れさせる。
design_effect:
  - counterexample_certificateのconcrete witness、normative contract、fixed design treatment、required same-treatmentまたは禁止condition、直接矛盾、design effectの各前提を、事前固定dependency上のadmission済みpacket atom、現在snapshotのsuccess receiptおよびvalue identityへ直接結び付け、rootがそのidentity一致を機械検査できる一般規則を追加する。
```

## 3. disposition

反例はreviewerの意味判断が参照した根拠identityをpacketへ閉じていない一般規則の欠陥を示すため、contract r6はrejectする。同じidentityを修正または再reviewしない。counterexample certificateの全前提を事前固定dependency、admission済みatom、現在snapshot receiptおよびvalue identityへ完全一致で結び付ける規則を新しいcontract identityへ固定する。

## 4. 状態

`independent_review_complete / counterexample_found / result_admissible / contract_r6_rejected / revision_required / cases_not_materialized / candidate_not_created`
