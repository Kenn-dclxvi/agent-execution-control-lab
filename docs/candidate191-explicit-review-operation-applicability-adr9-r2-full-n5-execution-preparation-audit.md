# Candidate191 ADR9 r2全9ケースN=5実行準備監査

> **結果**: `execution_preparation_passed / fifteen_slots_authorized / issued_zero_at_preflight`

## 結論

Candidate191のADR9 r2全9ケースN=5について、登録済み30件を再利用し、ADR01、ADR02およびADR08の不足各5件、合計15件だけを発行可能な状態へ固定した。comparison preflightはprompt identity以外の互換条件を全件照合して`ready`となり、監査時点では一件も発行していない。

## 固定identity

- reference result ID: `d3e91302f0d14350906075676c5a2791`
- reused Candidate191 result ID: `b71bcb211b064977900bce9aa0132cd4`
- Candidate191 full pool key: `df4cef435915f62453ce6e8b7053dff32f4d94e585cd20d08fbca27519717d51`
- compatibility key: `1543a80108418ce1f2436f5f1945f6e680cf75378cc308d21adee22fcf0f11d3`
- profile SHA-256: `68edcd3682fb8ba594b566a4f19f6f6343e54f2b325db9778bf461c0f1eb0aca`
- dispatch plan content SHA-256: `66f8fa3fdefcaece526524fca50bf931bc9ef4872fed818d82149c4fa2786144`
- global plan SHA-256: `934792e9f914161c968bcb2b39fb440383015b29c58778c39f967d5be495f226`
- comparison generation content SHA-256: `0eb5c957ab753faa9f80ac1640b9cc90fa9faa62b346b5ef34efca63b2449acf`
- comparison preflight content SHA-256: `de039b746113178314f60f55c35eb8ce36431d78dfc98773149b7efc0968f8c9`
- resource class SHA-256: `86aa0920e9a45248b653ac3c3ac077680012f368b0adfec2e697dd3b4b928c35`
- preparation root: `/Users/kenn/repos/_verification/THE-CAPTION-prompt-ab-measurement/runs/candidate191-explicit-review-operation-applicability-adr9-r2-full-n5-20260812-r2`

`plan-missing`はADR03〜ADR07およびADR09を各5件、ADR01、ADR02およびADR08を0件として認識した。不足は後者三ケースの各5件だけで、global planは15 job、M=24を固定した。

## 停止履歴

- 既存M5 registryの空Candidate191 poolへ登録resultを再importするとappend-only identityが競合したため、resultを変更せず新しいregistryへ基準resultとCandidate191 resultを正規importした。
- receiptを含むLayer 1を参照実体に指定した準備はwrite-once receipt衝突で停止した。
- 通常コピーでfixture modeが変わった準備はADR01 fixture identity不一致で停止した。
- Candidate189 identityのtemplateを渡した準備はprompt identity不一致で停止した。

いずれも比較slot発行前の停止である。最終cycleは保存Layer 1をmode込みで保持し、templateのprompt identity、bundle hashおよびbundle pathだけをCandidate191固定値へ合わせた。TaskSpec、model-visible payload、fixtureまたは評価条件は変更していない。

## 後続実行

固定global planは変更せず発行され、15 / 15 valid、除外0件、runner error 0件で完了した。本監査の発行前状態は上書きせず、現在判断は[`Candidate191 ADR9 r2全9ケースN=5`](../evaluations/results/candidate191-explicit-review-operation-applicability-adr9-r2-full-n5_2026-08-12.md)を正本とする。

`execution_preparation_passed / existing_thirty_reused / missing_fifteen_only / authorized_fifteen / issued_zero_at_preflight / private_boundary_passed / execution_completed_after_preflight`
