# review terminal proof obligation qualification contract r2 敵対的レビュー

> **位置づけ**: 情報封鎖した独立レビュー完了／具体的反例あり／contract r2 rejected／Candidate未作成

## 1. operation receipt

- review operation identity: `review-terminal-proof-obligation-contract-r2-adversarial-review`
- source design identity: `review-terminal-proof-obligation-qualification-contract-r2`
- bound producer execution identity: `terminal_proof_contract_review_r2`
- result sender identity: `terminal_proof_contract_review_r2`
- packet identity: `review-terminal-proof-obligation-adversarial-review-packet-r2`
- packet raw SHA-256 before delivery: `893ee31c635939f8db5628c046437ff5523e3c6b8792f3d146028105c047669f`
- packet raw SHA-256 after result: `893ee31c635939f8db5628c046437ff5523e3c6b8792f3d146028105c047669f`
- allowed read: [`review-terminal-proof-obligation-adversarial-review-packet-r2.md`](review-terminal-proof-obligation-adversarial-review-packet-r2.md)だけ
- result admission: producer、sender、design、packetおよび形式が固定値と一致

## 2. independent result

以下は独立producerの返却結果を意味変更せず保存したものである。

```yaml
disposition: counterexample_found
design_identity: review-terminal-proof-obligation-qualification-contract-r2
packet_identity: review-terminal-proof-obligation-adversarial-review-packet-r2
boundary_identity: SCOPE-ORDER-PERMISSION
contract_basis:
  - 第3.7節3項は、finite direct match certificateが不成立でpermissionが否定された場合、review operation、packet、producer、invocationを作らず現在subjectをunavailableにすると定める。
  - 第3.6節は、unavailableに、先に形成を試みたterminal certificate identity、欠けたdependency identityとstate、および解消時に閉じるpredicate identityを要求する。
  - 第3.7節7項は、rootの検査対象にproducer identityとpacket identityの一致を要求する。
counterexample:
  - finite direct match certificateは不成立だがreview permissionが否定されている状態では、第3.7節3項によりpacket、producer、invocationが存在せず、terminal certificateの形成も試みられない。それでも同項はsubjectをunavailableとして受け入れるため、第3.6節のcertificateと第3.7節7項のroot検査を満たせないterminal受入れになる。
design_effect:
  - permission否定専用の機械検査可能なunavailable certificateを定義し、その必要identityとreceiptをpacketやproducerを生成せず固定できるようにするか、permission否定時はcertificate付きterminalではなく非terminalな停止状態として扱うよう一般規則を変更する。
```

## 3. disposition

反例はreview前permission停止とreview後result admissionを同じcertificateへ載せた一般規則の矛盾を示すため、contract r2はrejectする。同じidentityを修正または再reviewしない。review operation作成前にrootが機械判定するpermission否定専用certificateと、reviewerが返すfrontier certificateを新しいcontract identityで分離する。

## 4. 状態

`independent_review_complete / counterexample_found / result_admissible / contract_r2_rejected / revision_required / cases_not_materialized / candidate_not_created`
