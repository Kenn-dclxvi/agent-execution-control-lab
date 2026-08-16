# Candidate259 同一artifact二度目継続read除外 Standard14 N=5実行準備監査

## 結論

保存済みCandidate147 Standard14 N=5 result `f7baeadc5bd44399ac13cc0e0a8aff48`と保存Layer 1へbindした。Candidate259のprompt identity以外の互換条件は一致し、比較前receiptは`ready`、承認65件、発行0件である。Candidate259の既存F04 atomic run 5件は再利用し、F04を再発行しない。

## 発行前固定

- Evaluation set: `the-caption-standard14-r1` r1、14ケース。
- N: 各ケース5件、合計70 run。既存F04 5件を再利用し、新規発行は残る13ケース各5件、合計65件。
- model / reasoning: `gpt-5.6-sol / medium`。
- runtime: Codex CLI 0.146.0、Python 3.14.5。
- target: commit `3ce91a403f9e0c83f29d56bbe9e7b449b713445d`、tree `88eecfa29f7016b4d77061d3aabe3e7d176fea9b`。
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`。
- permission: `workspace-write / never`。
- configured M: 24。
- token accounting: all-agent v1。
- compatibility key: `cc0c022ac026b55c51597e82c4a7216d4b7fdf498250c6a299d24203f1027561`。
- Candidate259 bundle SHA-256: `93d1874f285dc1381122248fd4786a13c05ce04ef976d39050cb8892f9616eac`。

`seed-pool`はCandidate147のStandard14 pool `2a0816816b146f2083f9d2507e2ac485ecaecf62269e834495347f5bc2be99e5`からCandidate259 pool `ab15aeb5d62a1989282fca16a1e4b6f609c3f28e1528e9eaafce754df4280849`を作成した。既存Candidate259 F04 resultの5件をpoolへ保持したうえで、`plan-missing --desired-count 5`はF04を不足0件、その他13ケースを不足各5件、合計65件へ固定した。

比較用Layer 1はCandidate147 Standard14 resultを実生成した保存実体からmaterializeした。templateのfixture、TaskSpec、rating、runtime、permissionおよびexecutor条件を変えず、prompt identity、bundle hash、bundle pathだけをCandidate259へ置換した。

`prepare-comparison-layer1`、`prepare_atomic_plan.py`、`preflight-comparison`、`verify-comparison-preflight`はすべて成功した。最終receiptはprofile SHA-256 `ba60a7ec8ad32926fb9018907cd27cebf4e46423302ecc1b82843553db75c51f`、global plan SHA-256 `15039dd5f9856676760ce3379cc80b6f6f6988dd9b988e7e284cf5b007213a99`、receipt content SHA-256 `47c39ba038fc6c1faad0adfe6e3278eb7996749f5e4ac80edb78929f59e853e6`、承認65件、発行0件を固定する。

## 解釈境界

このStandard14測定は、実行有効性、品質、非対象経路および3 KPIを測る。Candidate259の回数ベースread制限と正本設計原則との衝突は、別の[後続監査](candidate259-design-principle-conflict-followup-audit.md)に固定済みである。したがって、Standard14が全件通過しても、その衝突の解消、機序成立、採用、releaseまたはprojectionを意味しない。

## 現在状態

この監査が固定したreceiptから65件を発行し、65 / 65 validかつrateable、65 / 65 Score `4`で完了した。既存F04 5件と合わせた結果は[Candidate259 Standard14 N=5](../evaluations/results/candidate259-same-artifact-second-continuation-exclusion-standard14-n5_2026-08-15.md)へ分離して記録する。

`preflight_completed / existing_f04_5 / authorized_65 / issued_65 / registered_result_1d27ee8fc6b74946aa76132aee5478aa`
