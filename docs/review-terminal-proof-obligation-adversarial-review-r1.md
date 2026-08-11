# review terminal proof obligation qualification contract r1 敵対的レビュー

> **位置づけ**: 情報封鎖した独立レビュー完了／具体的反例あり／contract r1 rejected／Candidate未作成

## 1. operation receipt

- review operation identity: `review-terminal-proof-obligation-contract-r1-adversarial-review`
- source design identity: `review-terminal-proof-obligation-qualification-contract-r1`
- bound producer execution identity: `terminal_proof_contract_review_r1`
- result sender identity: `terminal_proof_contract_review_r1`
- packet identity: `review-terminal-proof-obligation-adversarial-review-packet-r1`
- packet raw SHA-256 before delivery: `69d48ee30215e14e019d8fe95a0233d86bbc8e5c9c314ddfc31741df556af0fd`
- packet raw SHA-256 after result: `69d48ee30215e14e019d8fe95a0233d86bbc8e5c9c314ddfc31741df556af0fd`
- allowed read: [`review-terminal-proof-obligation-adversarial-review-packet-r1.md`](review-terminal-proof-obligation-adversarial-review-packet-r1.md)だけ
- result admission: producer、sender、design、packetおよび形式が固定値と一致

## 2. independent result

以下は独立producerの返却結果を意味変更せず保存したものである。

```yaml
disposition: counterexample_found
design_identity: review-terminal-proof-obligation-qualification-contract-r1
packet_identity: review-terminal-proof-obligation-adversarial-review-packet-r1
boundary_identity: SCOPE-PACKET-STATE
contract_basis:
  - "第3.1節は全ての許可入力identityをmanifestへ先に固定し、各入力をpacket atomとして保存すると定めるが、manifest identityとpacket atomの一対一対応、input_identityの一意性、同一input_identityに対する競合atomの拒否を定めていない。"
counterexample:
  - "manifestに入力Iを一件固定したpacketへ、同じinput_identity Iとsource_identityを持ちながら、一方はstate=valueかつvalue_identity=V1、他方はstate=valueかつvalue_identity=V2で、V1とV2が異なる二つのatomを保存する。このpacketは全許可入力を含みatom構文にも適合するが、後続certificateはIに対応する都合のよいatomを採用できるため、競合値により本来閉じないterminalを受け入れ得る。"
design_effect:
  - "packet admissionの一般規則へ、manifestの各input_identityに対応するatomが厳密に一件だけ存在すること、manifest外atomがないこと、および重複または競合するinput_identityを持つpacketをterminal判定前に拒否することを追加する必要がある。"
```

## 3. disposition

反例はpacket admissionの一般規則変更を要求するため、contract r1はrejectする。同じidentityを修正または再reviewしない。manifest entryとpacket atomの全単射、input identityの一意性、stateとvalue identityの整合、競合packetのterminal判定前拒否を新しいcontract identityへ固定する。

## 4. 状態

`independent_review_complete / counterexample_found / result_admissible / contract_r1_rejected / revision_required / cases_not_materialized / candidate_not_created`
