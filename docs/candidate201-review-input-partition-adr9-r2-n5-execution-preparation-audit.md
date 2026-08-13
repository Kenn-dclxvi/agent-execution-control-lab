# Candidate201 review入力分割 ADR9 r2全9ケースN=5実行準備監査

> **結果**: `execution_preparation_passed / comparison_preflight_ready / forty_five_slots_authorized / issued_zero`

## 結論

Candidate201のADR9 r2全9ケース各5件は、Candidate199登録resultと保存Layer 1へbindし、prompt identity以外の互換条件を機械照合して発行直前まで準備できた。comparison preflightは`ready`で、不足45件だけを許可した。監査時点の発行数は0件である。

## 固定identity

- profile SHA-256: `438f80f2d2a46449f464a5d4593a6409996ecfae3ec00f705b1b0cc00e53e5f7`
- reference result: `7751ae31151d48dd87a75b2a71a8a527`
- reference result content SHA-256: `53e4b60bd54777bd22289ac08983687e2ba8d1534721e564855cb99a1c3d7d5c`
- compatibility key: `1543a80108418ce1f2436f5f1945f6e680cf75378cc308d21adee22fcf0f11d3`
- Candidate199 reference pool: `c7a7e594226c484bf56c459de6510bb81637bad5c46ed0e7996bd85a1f28f0a6`
- Candidate201 pool: `a8133a2c521465e5ec3a530b8310f361e103eb21f81d4183ca7e1a50d36d87c9`
- dispatch plan content SHA-256: `86e4deaa640ead913db51a1ba9abe0e6997b6b12b7b62d24258c3ffb321dea7b`
- global plan SHA-256: `6d4c6a5c0ae9eafdec68f0b739d59dbde2e6d048d79f0d01082361e170c1d0d0`
- comparison generation receipt content SHA-256: `176fc1f689b3593f8cdabc37c7ab7492d9c844d42973ae5c42844abb017ba46a`
- comparison preflight receipt content SHA-256: `4912a80b6d569cb63471a7578dc202800aa0bf6db6cf47b602360f51368f0df4`
- preparation root: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate201-review-input-partition-adr9-r2-n5-20260813-r3`

`seed-pool`はCandidate201の空poolを作り、`plan-missing --desired-count 5`はADR01〜ADR09のexistingを各0、missingを各5、合計45件と固定した。45 capsuleは独立sample IDを持つ。

Evaluation set、case revision、fixture、TaskSpec、rating、model、reasoning、Agent/runtime/CLI、permission、executor、command evidence protocol、token accounting、target commit/treeおよびM=24はCandidate199登録resultと一致する。異なるのは事前宣言したprompt identity、bundle hashおよびbundle pathだけである。

比較準備の最初の二回は、comparison receiptを含むcycle Layer 1をreferenceとして指定したためwrite-once保護が再生成を拒否した。評価スロットは発行していない。既存物を上書きせず、receiptを含まない保存reference Layer 1を使う新しい`r3`準備rootへ切り替えた。

`candidate201_existing_0 / candidate201_missing_45 / authorized_45 / issued_0 / comparison_preflight_ready / candidate201_not_evaluated`
