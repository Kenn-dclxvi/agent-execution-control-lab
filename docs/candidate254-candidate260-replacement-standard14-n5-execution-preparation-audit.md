# Candidate254採用判断 Standard14 N=5実行準備監査

## 結論

保存済みCandidate147 Standard14 N=5 result `f7baeadc5bd44399ac13cc0e0a8aff48`と保存Layer 1へ対応付けた。Candidate254のprompt identity以外の比較条件は一致し、比較前receiptは`ready`、承認65件、発行0件である。Candidate254の既存F04 atomic run 5件は再利用し、F04を再発行しない。

## 発行前固定

- 判断対象: Candidate254を正式採用するか、採用せず追加制御を検討するか。
- 評価対象: 既存Candidate254 `the-caption-3ce91a4-independent-check-same-model-step-r1`。
- 比較基準: Candidate147 Standard14 N=5。
- Evaluation set: `the-caption-standard14-r1` r1、14ケース。
- 件数: 各ケース5件、合計70 run。既存F04 5件を再利用し、新規発行は残る13ケース各5件、合計65件。
- model / reasoning: `gpt-5.6-sol / medium`。
- runtime: Codex CLI 0.146.0、Python 3.14.5。
- target: commit `3ce91a403f9e0c83f29d56bbe9e7b449b713445d`、tree `88eecfa29f7016b4d77061d3aabe3e7d176fea9b`。
- rating: `outcome-terminal-state-evidence-owner-diagnostic-v14`。
- permission: `workspace-write / never`。
- 設定上の同時実行上限: 24。
- token accounting: all-agent v1。
- compatibility key: `cc0c022ac026b55c51597e82c4a7216d4b7fdf498250c6a299d24203f1027561`。
- Candidate254 bundle SHA-256: `7cd564be0904efb5cee59ce8d72935971d080282686e5ff7be9e85e62aa0fd52`。

`seed-pool`はCandidate147のStandard14 pool `2a0816816b146f2083f9d2507e2ac485ecaecf62269e834495347f5bc2be99e5`からCandidate254 pool `e71ba5db8f3766df39c9c9af10970888e820ff04761b4f709cd543faa01e8b38`を作成した。`plan-missing --desired-count 5`は既存Candidate254 F04を5件、F04の不足を0件、その他13ケースの不足を各5件、合計65件へ固定した。

比較用Layer 1はCandidate147 Standard14 resultを実生成した保存実体から複製した。templateのfixture、TaskSpec、rating、runtime、permissionおよびexecutor条件を変えず、prompt identity、bundle hash、bundle pathだけをCandidate254へ置換した。

`prepare-comparison-layer1`、`prepare_atomic_plan.py`、`preflight-comparison`、`verify-comparison-preflight`はすべて成功した。最終receiptはprofile SHA-256 `5c7c19fa66a094b42b713b8c68c7b96ba850ea142665cc20d45dab1721391ea2`、global plan SHA-256 `5e53746e82c09102e8ffcec239285c4b6a42d2a4482c60345569c1edd8fe5e96`、receipt content SHA-256 `d7f6271c13adee4ddeecedb92f33e3d19df747ee03653c6f96607ad55b7c0eff`、承認65件、発行0件を固定する。

## 判定境界

Standard14では、70件すべてが有効かつ採点可能で、70件すべてScore `4`であることを品質条件とする。品質を維持した後にCandidate147と品質、all-agent総token、経過時間を比較する。機序成立率は原因診断として記録するが、品質再現性との対応が100％ではないため全件成立を停止条件にしない。

この比較が通過しても、Candidate254の採用、releaseまたはtarget本体への反映を意味しない。

この監査の作成時にはCandidate254をCandidate260の置換候補と表現していたが、その位置づけは訂正する。Candidate260は失敗履歴であり、preflight receipt、比較条件、発行済みrunまたはCandidate254の評価値には影響しない。

## 現在状態

この監査が固定したreceiptから65件を発行し、65 / 65件が有効かつ採点可能で、65 / 65件すべてScore `4`だった。既存F04 5件と合わせた結果は[Candidate254 Standard14 N=5](../evaluations/results/candidate254-independent-check-same-model-step-standard14-n5_2026-08-16.md)へ分離して記録する。

`preflight_completed / existing_f04_5 / authorized_65 / issued_65 / registered_result_59117fe7924f4b718df4ff32491551cc`
