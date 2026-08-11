# review terminal proof obligation qualification contract r9 敵対的レビュー

> **位置づけ**: 情報封鎖した独立レビュー完了／具体的反例あり／contract r9 rejected／revision系列停止／Candidate未作成

## 1. operation receipt

- review operation identity: `review-terminal-proof-obligation-contract-r9-adversarial-review`
- source design identity: `review-terminal-proof-obligation-qualification-contract-r9`
- bound producer execution identity: `terminal_proof_contract_review_r9`
- result sender identity: `terminal_proof_contract_review_r9`
- packet identity: `review-terminal-proof-obligation-adversarial-review-packet-r9`
- packet raw SHA-256 before delivery: `105e77b153ca67a2e7b007f4cad63dd1489dd74387430215884d25305f872886`
- packet raw SHA-256 after result: `105e77b153ca67a2e7b007f4cad63dd1489dd74387430215884d25305f872886`
- allowed read: [`review-terminal-proof-obligation-adversarial-review-packet-r9.md`](review-terminal-proof-obligation-adversarial-review-packet-r9.md)だけ
- result admission: producer、sender、design、packetおよび形式が固定値と一致

## 2. independent result

以下は独立producerの返却結果を意味変更せず保存したものである。

```yaml
disposition: counterexample_found
design_identity: review-terminal-proof-obligation-qualification-contract-r9
packet_identity: review-terminal-proof-obligation-adversarial-review-packet-r9
boundary_identity: SCOPE-PACKET-STATE
contract_basis:
  - packet_atomはstate=valueの場合にもvalue_identityだけを保存し、reviewerが意味判断に使う観測値そのものまたはpacket内の意味内容を要求していない。
  - reviewerの許可入力はpacketだけであり、packet外からvalue_identityの内容を取得できない。
counterexample:
  - 現在snapshotの直接receiptがstate=valueとvalue_identityを正しく返し、全identity照合も成立する一方、具体的な観測値の意味内容がpacketに含まれない入力では、reviewerはwitness適用性、直接矛盾またはdesign effectを判定できず、本来形成可能なterminal certificateを拒否してunavailableにする。
design_effect:
  - state=valueのpacket atomへ観測値の意味内容を追加し、その内容、value_identity、直接receiptが同一の現在値へ結び付くことをadmission条件にする一般規則変更が必要である。
```

## 3. disposition

反例自体は受け入れる。ただし、この修正をr10へ追加すると汎用packet schemaがさらに増え、当初の「terminalごとの最小dependency certificate」「roleと中間stateを減らす」という設計境界から外れる。r9はrejectするがr10を作らず、本系列を停止して設計ドリフトを監査する。

## 4. 状態

`independent_review_complete / counterexample_found / result_admissible / contract_r9_rejected / revision_series_stopped_for_design_drift / r10_not_created / cases_not_materialized / candidate_not_created`
