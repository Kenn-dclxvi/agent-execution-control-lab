# Candidate262 Standard14 N=5実行準備監査

## 結論

Candidate147 Standard14 N=5の保存済みresult `f7baeadc5bd44399ac13cc0e0a8aff48`と保存Layer 1へ固定した。Candidate262のprompt identity以外の比較条件は一致し、比較前receiptは`ready`、既存A01 / F03各5件を再利用して不足60件だけを許可した。Candidate147と既存Candidate262の再実行は許可していない。

## 発行前固定

- Evaluation set: `the-caption-standard14-r1` r1、14ケース。
- 件数: 各ケース5件、合計70 run。
- 既存run: A01 5件、F03 5件、合計10件。
- 新規発行: 残る12ケース各5件、合計60件。
- Candidate262 bundle SHA-256: `61c0735fc0cadcb0d45d2132346d01540d8366040ce886bb3f4332279915ba33`。
- Candidate147 reference result: `f7baeadc5bd44399ac13cc0e0a8aff48`。
- compatibility key: `cc0c022ac026b55c51597e82c4a7216d4b7fdf498250c6a299d24203f1027561`。
- Candidate147 pool: `2a0816816b146f2083f9d2507e2ac485ecaecf62269e834495347f5bc2be99e5`。
- Candidate262 Standard14 pool: `aa7a3c32d91c661ad5aba5452cdeb920a103f3ee0b923955172caac9cc15d7b7`。
- model / reasoning: `gpt-5.6-sol / medium`。
- runtime: Codex CLI 0.146.0、Python 3.14.5。
- permission: `workspace-write / never`。
- 設定上の同時実行上限: 24。
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`。
- token accounting: all-agent v1。

Candidate262のA01 / F03 targeted poolに登録済みの10件を、同じrun内容のままStandard14 poolへ登録した。pool側のケース別実効条件との機械照合は10件すべて成功した。`plan-missing --desired-count 5`はA01とF03の不足を0件、他12ケースを各5件、合計60件へ固定した。

`prepare-comparison-layer1`、`prepare_atomic_plan.py`、`preflight-comparison`、`verify-comparison-preflight`はすべて成功した。最終receiptは60件だけを許可し、statusは`ready`である。

## 判定境界

70件すべてが有効かつ採点可能であること、70件すべてScore `4`であることを品質条件とする。品質の後にCandidate147と、全体およびケース別のquality、all-agent `total_tokens`、`elapsed_seconds`を比較する。

Candidate262の変更対象は`spec_ready=false`時の開始状態読み取りpermissionである。A01以外のケースでは品質と費用の非対象回帰を確認する。A01の開始状態読み取り、F03の開始identityと必要readの初回発行関係は既存5件の診断を保持するが、それだけでStandard14のKPI比較を止めない。

この実行はCandidate262の採用、releaseまたはtarget本体への反映を承認しない。

## 現在状態

許可60件を発行し、60 / 60件がvalid、excluded 0、実行エラー0だった。60 / 60件すべてScore `4`で、既存10件と合わせた結果は[Candidate262 Standard14 N=5](../evaluations/results/candidate262-spec-false-start-state-consumer-permission-standard14-n5_2026-08-16.md)へ分離して記録する。

`preflight_completed / existing_a01_5 / existing_f03_5 / authorized_60 / issued_60 / valid_60 / score4_60 / reference_rerun_0 / registered_result_21fc9d743aa14251a7a17c63425ff4c0`
