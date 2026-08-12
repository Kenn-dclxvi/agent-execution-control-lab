# Candidate193 frontier-bound dispatch transition ADR9 r2全9ケースN=5実行準備監査

> **結果**: `execution_preparation_passed / forty_five_slots_authorized / issued_zero_at_preflight`

## 結論

Candidate193のADR9 r2全9ケース各5件は、Candidate191の登録済み45 atomic runを参照resultへbindし、prompt identity以外の互換条件を機械照合して発行直前まで準備できた。comparison preflightは`ready`で、Candidate193の不足45件だけを許可した。監査時点の発行数は0件であり、評価runは開始していない。

## 固定identity

- reference result ID: `e599690689294c658b52a6a9e301697f`
- reference result content SHA-256: `2f969876645f5e2f3bfc37acaafab85b68a004dba474e21ec6b1055359d8edac`
- compatibility key: `1543a80108418ce1f2436f5f1945f6e680cf75378cc308d21adee22fcf0f11d3`
- Candidate191 reference pool key: `df4cef435915f62453ce6e8b7053dff32f4d94e585cd20d08fbca27519717d51`
- Candidate193 pool key: `6922f60afac508cef6e254a08108e32f6eed2ad32814dc7bc7fce048b63ed3af`
- evaluation set identity SHA-256: `ba9e62614b62904d301c9b303e1bb2dccd5951f7bdf15c330f01b716bca16931`
- profile SHA-256: `768f26d66889e7f67bd2a81d31c0c301a1c41799ed632e901025a5286e529477`
- dispatch plan content SHA-256: `b0f4e77c6af0635d9bcf9ea358046265bb9f6582533773e8f629aa6199291d49`
- global plan SHA-256: `73204948f3c3cdf3842e142457684b8fdc03a5657d678afa909b36d9aa180e25`
- comparison generation content SHA-256: `286ef41462a6f15d3efa847363ebf3334fdf823c04d874f1878bf2159dbb6bd8`
- comparison preflight content SHA-256: `3f93d5724b2e091de3eba5c1980557130256aaf76ec4301f279b0f9c5a58c7c3`
- resource class SHA-256: `86aa0920e9a45248b653ac3c3ac077680012f368b0adfec2e697dd3b4b928c35`
- preparation root: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate193-frontier-bound-dispatch-transition-adr9-r2-n5-20260812-r1`

## 不足計画

Candidate191の登録resultはADR01〜ADR09の各5件、合計45件を参照側へ保持する。Candidate193 poolは各case 0件でseedされ、`plan-missing --desired-count 5`は各caseの不足を5件、合計45 slotと固定した。既存runをCandidate193のrunとして流用または再実行扱いにしていない。

45 capsuleはCandidate191 templateのprompt name、bundle hashおよびbundle pathだけをCandidate193へ置換した。case、fixture、TaskSpec、model-visible input、rating、model、reasoning、runtime、permission、executor parameters、token accounting、command evidence protocol、保存Layer 1およびM=24は変更していない。

## 基準判定の境界

Candidate191の参照45件は、登録resultだけでなく全9ケース機序監査r1と再利用30件のcommand evidence訂正機序監査r3を一組として扱う。旧collectorの誤検出を新しい違反として復活させず、同時にScore `4`やterminalだけでCandidate193の機序を通過させない。Candidate193では評価設計に固定したfrontier完全性、dependency越境禁止、不要分割禁止、個別tool call、全result収集およびconsumerなし発行0件を生traceで別途判定する。

## 発行境界

comparison receiptは`authorized_slots = 45`、`issued_slots = 0`、`max_workers = 24`を固定し、検証結果は`ready`だった。preparation rootに`parallel-run`はなく、cycleはLayer 1までである。この監査は評価実行を承認または開始した記録ではない。固定global planを使うrun発行は、利用者の次の明示的な継続判断まで行わない。

固定global planは後続の明示指示で発行され、45 / 45 valid、除外0件、runner error 0件で完了した。本監査の発行前状態は上書きせず、現在判断は[`Candidate193 ADR9 r2全9ケースN=5`](../evaluations/results/candidate193-frontier-bound-dispatch-transition-adr9-r2-n5_2026-08-12.md)を正本とする。

`execution_preparation_passed / comparison_preflight_ready / candidate191_reference_45_reused / candidate193_missing_45 / authorized_45 / issued_0_at_preflight / execution_completed_after_preflight`
