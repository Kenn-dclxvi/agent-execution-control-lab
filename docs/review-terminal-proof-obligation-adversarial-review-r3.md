# review terminal proof obligation qualification contract r3 敵対的レビュー

> **位置づけ**: 情報封鎖した独立レビュー完了／具体的反例あり／contract r3 rejected／Candidate未作成

## 1. operation receipt

- review operation identity: `review-terminal-proof-obligation-contract-r3-adversarial-review`
- source design identity: `review-terminal-proof-obligation-qualification-contract-r3`
- bound producer execution identity: `terminal_proof_contract_review_r3`
- result sender identity: `terminal_proof_contract_review_r3`
- packet identity: `review-terminal-proof-obligation-adversarial-review-packet-r3`
- packet raw SHA-256 before delivery: `5a06c17c4faa9ac9649b8ba0543c0710eaa1db21339b76fae9abf80df0438d60`
- packet raw SHA-256 after result: `5a06c17c4faa9ac9649b8ba0543c0710eaa1db21339b76fae9abf80df0438d60`
- allowed read: [`review-terminal-proof-obligation-adversarial-review-packet-r3.md`](review-terminal-proof-obligation-adversarial-review-packet-r3.md)だけ
- result admission: producer、sender、design、packetおよび形式が固定値と一致

## 2. independent result

以下は独立producerの返却結果を意味変更せず保存したものである。

```yaml
disposition: counterexample_found
design_identity: review-terminal-proof-obligation-qualification-contract-r3
packet_identity: review-terminal-proof-obligation-adversarial-review-packet-r3
boundary_identity: SCOPE-PACKET-STATE
contract_basis:
  - packet_atomはnon-value stateについてvalue_identityが存在しないことだけを要求し、そのstateが現在のsource観測へ直接結び付くreceiptを要求していない
  - non-value stateだけを理由にpacketを未完成とせず、closure frontier上のmissing、unreadable、terminal_failureはno_counterexample_foundを拒否できる
counterexample:
  - manifestで固定されたsourceは実際には読取可能で現在値を返しているが、packet atomをstate=missingかつvalue_identityなしとして保存する。このatomはpacket_atom_bijection_readyの明示条件を全て満たしてadmissionされ得る一方、no-counterexample closureを拒否してunavailableへ進ませ、必要なterminalを拒否できる
design_effect:
  - state=value以外にも、input identity、source identity、snapshot identityおよび観測結果を結び付ける直接receiptを必須化し、そのreceiptなしのnon-value stateをpacket admission前に拒否する一般規則が必要である
```

## 3. disposition

反例はpacket stateのprovenance不足という一般規則変更を要求するため、contract r3はrejectする。同じidentityを修正または再reviewしない。全stateへinput、source、snapshot、観測結果を結び付ける直接receiptを必須化し、receipt結果とstateの一意な対応を新しいcontract identityへ固定する。

## 4. 状態

`independent_review_complete / counterexample_found / result_admissible / contract_r3_rejected / revision_required / cases_not_materialized / candidate_not_created`
